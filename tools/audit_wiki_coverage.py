#!/usr/bin/env python3
"""Read-only, conservative Wiki address coverage report. No source or Ghidra mutation.

Coverage means direct scoped manifest entry, NOT complete semantics, code bounds, or
presence in a user's local Ghidra database. ROM offsets, production aliases and
stage-overlay virtual addresses are intentionally not treated as global coverage.
"""
import argparse
import csv
from collections import defaultdict
from pathlib import Path
import re

ADDR = re.compile(r"(?<![0-9A-Za-z])0x(80[0-9a-fA-F]{6})(?![0-9a-fA-F])")
FILES = {
    "functions.tsv": (None, 0),
    "globals.tsv": (None, 0),
    "comments.tsv": ("global", 1),
    "bookmarks.tsv": ("global", 1),
    "code_labels.tsv": ("global", 1),
    "relations.tsv": ("global", 1),
    "overlay_functions.tsv": ("overlay", 1),
}
EXCLUDE = {"Project-Status.md", "Home.md", "1.0-Requirements-and-Roadmap.md"}

def load(root):
    found = defaultdict(set)
    for filename, (scope, col) in FILES.items():
        with (root / "analysis" / filename).open(encoding="utf-8", newline="") as source:
            for row in csv.DictReader(source, delimiter="\t"):
                if scope == "overlay":
                    address = row["address"]
                    group = row["scope"]
                elif scope == "global":
                    address = row["address"] if filename != "relations.tsv" else row["from"]
                    group = "global"
                else:
                    address = row["address"]
                    group = "global"
                if re.fullmatch(r"0x80[0-9a-fA-F]{6}", address, re.I):
                    found[(group, address.lower())].add(filename)
    return found

def scan(wiki, found):
    report = []
    for page in sorted(wiki.glob("*.md")):
        if page.name in EXCLUDE:
            continue
        section = ""
        addresses = set()
        for line_no, line in enumerate(page.read_text(encoding="utf-8").splitlines(), 1):
            if line.startswith("#"):
                section = line.lstrip("# ").strip()
            for match in ADDR.finditer(line):
                address = "0x" + match.group(1).lower()
                key = (section, address)
                if key in addresses:
                    continue
                addresses.add(key)
                if address.startswith("0x800"):
                    manifest = found.get(("global", address), set())
                    status = "direct-global-manifest" if manifest else "not-directly-indexed"
                else:
                    # Same 0x802E... VA can refer to different stages. Without
                    # stage-specific identity a name-only match is unsafe.
                    manifest = set()
                    status = "scope-ambiguous-review"
                report.append((page.name, section, address, status,
                               ",".join(sorted(manifest)), line_no))
    return report

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wiki-dir", type=Path, required=True,
                        help="Path to versioned MKMSZ-Randomizer/wiki; never modifies it")
    parser.add_argument("--output", type=Path, default=None,
                        help="Optional CSV output path; stdout summary always shown")
    args = parser.parse_args()
    if not args.wiki_dir.is_dir():
        parser.error("wiki directory does not exist")
    root = Path(__file__).resolve().parents[1]
    report = scan(args.wiki_dir, load(root))
    counts = defaultdict(int)
    for _, _, _, status, _, _ in report:
        counts[status] += 1
    print(f"Pages sampled: {len(set(row[0] for row in report))}")
    print(f"Unique page/section/address occurrences: {len(report)}")
    for status in sorted(counts):
        print(f"{status}: {counts[status]}")
    print("DISCLAIMER: absence of direct manifest index does not imply unknown code;")
    print("a direct index does not prove semantics, boundaries, or local application.")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8", newline="") as out:
            writer = csv.writer(out)
            writer.writerow(("wiki_page", "section", "address", "coverage_bucket",
                             "direct_manifest_files", "first_occurrence_line"))
            writer.writerows(report)
        print(f"Wrote {args.output}")

if __name__ == "__main__":
    main()
