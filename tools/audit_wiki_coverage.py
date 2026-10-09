#!/usr/bin/env python3
"""Read-only, conservative Wiki address coverage report. No source or Ghidra mutation.

Coverage means direct scoped manifest entry, NOT complete semantics, code bounds, or
presence in a user's local Ghidra database. ROM offsets, production aliases and
stage-overlay virtual addresses are intentionally not treated as global coverage.
"""
import argparse
import csv
import json
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

def summarize(report, wiki):
    """Deterministic raw address-visibility proxy, not RE completion."""
    counts = defaultdict(int)
    for _, _, _, status, _, _ in report:
        counts[status] += 1
    indexed = counts["direct-global-manifest"]
    absent = counts["not-directly-indexed"]
    denominator = indexed + absent
    return {
        "metric": "wiki_0x800_direct_global_index_visibility",
        "wiki_files_scanned": sum(1 for p in wiki.glob("*.md") if p.name not in EXCLUDE),
        "wiki_files_with_address_occurrences": len({row[0] for row in report}),
        "unique_page_section_address_occurrences": len(report),
        "direct_global_manifest": indexed,
        "not_directly_indexed": absent,
        "scope_ambiguous_review": counts["scope-ambiguous-review"],
        "eligible_raw_0x800_occurrences": denominator,
        "direct_index_percent": round(indexed * 100.0 / denominator, 2) if denominator else None,
        "not_direct_indexed_percent": round(absent * 100.0 / denominator, 2) if denominator else None,
        "limitations": (
            "This is a lexical address-navigation proxy, NOT a percentage of "
            "reverse-engineering completeness. 0x800 PS1 addresses, stock/production "
            "aliases and data/inside-function sites may occur; 0x801/0x802 stage/arena "
            "addresses are withheld from the direct-global denominator. Local Ghidra "
            "application and semantic fidelity are not checked by this scan."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wiki-dir", type=Path, required=True,
                        help="Path to versioned MKMSZ-Randomizer/wiki; never modifies it")
    parser.add_argument("--output", type=Path, default=None,
                        help="Optional CSV output path; stdout summary always shown")
    parser.add_argument("--summary-json", type=Path, default=None,
                        help="Optional machine-readable visibility summary output")
    args = parser.parse_args()
    if not args.wiki_dir.is_dir():
        parser.error("wiki directory does not exist")
    root = Path(__file__).resolve().parents[1]
    report = scan(args.wiki_dir, load(root))
    summary = summarize(report, args.wiki_dir)
    print(f"Wiki files scanned: {summary['wiki_files_scanned']}")
    print(f"Files with address occurrences: {summary['wiki_files_with_address_occurrences']}")
    print(f"Unique page/section/address occurrences: {summary['unique_page_section_address_occurrences']}")
    print(f"direct-global-manifest: {summary['direct_global_manifest']}")
    print(f"not-directly-indexed: {summary['not_directly_indexed']}")
    print(f"scope-ambiguous-review: {summary['scope_ambiguous_review']}")
    print(f"Raw 0x800 direct index coverage: {summary['direct_index_percent']}% "
          f"({summary['direct_global_manifest']}/{summary['eligible_raw_0x800_occurrences']}); "
          f"not directly indexed: {summary['not_direct_indexed_percent']}%")
    print("THIS IS AN ADDRESS VISIBILITY PROXY, NOT WHOLE-MIGRATION COMPLETENESS.")
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
    if args.summary_json:
        args.summary_json.parent.mkdir(parents=True, exist_ok=True)
        with args.summary_json.open("w", encoding="utf-8") as out:
            json.dump(summary, out, indent=2, sort_keys=True)
            out.write("\n")
        print(f"Wrote summary {args.summary_json}")

if __name__ == "__main__":
    main()
