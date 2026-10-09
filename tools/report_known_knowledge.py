#!/usr/bin/env python3
"""Report audited, already-documented MKMSZR knowledge migration (no ROM/emulator).

This is not a game reverse-engineering coverage metric. Structured records and
current Wiki owner-page reconciliation are DIFFERENT denominators. Do not combine
them into a fabricated overall percentage.
"""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEWS = {"partial-crosswalk", "unreviewed", "fully-reconciled"}
DISPOSITIONS = {"ghidra-confirmed", "versioned-sidecar"}

def records(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))

def count_rule(path, rule):
    entries = records(path)
    if rule == "rows":
        return len(entries)
    if rule == "definitions":
        return sum(r["kind"] in ("struct", "enum") for r in entries)
    if rule == "trace-sites":
        # A trace-site is an explicitly categorized stock code trace bookmark.
        return len({(r["scope"], r["address"].lower()) for r in entries
                    if r["category"].startswith("trace-")})
    if rule == "retail-data":
        return len({(r["scope"], r["address"].lower()) for r in entries
                    if r["category"] == "stock-data-navigation"})
    raise ValueError(f"Unknown count rule: {rule}")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, default=None, help="Write JSON metrics")
    parser.add_argument("--wiki-dir", type=Path, default=None,
                        help="Optional local Wiki directory: verify owner files exist")
    args = parser.parse_args()
    families = records(ROOT / "analysis/known_knowledge_families.tsv")
    owners = records(ROOT / "analysis/known_knowledge_owners.tsv")
    if not owners or not families:
        raise ValueError("Knowledge inventory missing")
    if len({r["owner_page"] for r in owners}) != len(owners):
        raise ValueError("Duplicate Wiki owner records")
    if len({r["family"] for r in families}) != len(families):
        raise ValueError("Duplicate knowledge family records")
    states = Counter()
    for row in owners:
        state = row["reconciliation"]
        if state not in REVIEWS:
            raise ValueError(f"Unknown owner state: {state}")
        states[state] += 1
        if args.wiki_dir and not (args.wiki_dir / row["owner_page"]).is_file():
            raise ValueError(f"Missing canonical Wiki owner: {row['owner_page']}")
    totals = Counter()
    rows = []
    for row in families:
        status = row["disposition"]
        if status not in DISPOSITIONS:
            raise ValueError(f"Unknown disposition: {status}")
        actual = count_rule(ROOT / row["manifest"], row["count_rule"])
        expected = int(row["expected"])
        if expected != actual:
            raise ValueError(f"{row['family']}: expected {expected}, actual {actual}. "
                             "Update reviewed ledger together with manifest changes.")
        totals[status] += actual
        rows.append({"family": row["family"], "count": actual, "disposition": status})
    n = len(owners)
    started = states["partial-crosswalk"] + states["fully-reconciled"]
    summary = {
        "definition": "Already-documented and curated MKMSZR research, NOT unknown game content",
        "structured_known_objects": sum(totals.values()),
        "ghidra_confirmed_structured_objects": totals["ghidra-confirmed"],
        "versioned_sidecar_objects": totals["versioned-sidecar"],
        "structured_objects_recorded_percent": 100.0,
        "canonical_known_owner_pages_in_ledger": n,
        "owner_pages_with_some_crosswalk": started,
        "owner_pages_with_some_crosswalk_percent": round(100 * started / n, 2),
        "owner_pages_fully_reconciled": states["fully-reconciled"],
        "owner_pages_fully_reconciled_percent": round(100 * states["fully-reconciled"] / n, 2),
        "owner_pages_not_yet_systematically_reviewed": states["unreviewed"],
        "known_finding_coverage_percent": None,
        "why_no_single_percent": (
            "Structured imports and owner-page review are different unit sizes. "
            "Current Wiki behavioral findings need atomic source-to-Ghidra crosswalk "
            "before a meaningful percentage of ALL ALREADY-KNOWN facts can be given."
        ),
        "families": rows,
    }
    print(f"Known structured records preserved: {summary['structured_known_objects']} "
          f"({totals['ghidra-confirmed']} Ghidra-confirmed; "
          f"{totals['versioned-sidecar']} intentionally sidecar)")
    print(f"Current Wiki owner pages: {n}; started crosswalk: {started} "
          f"({summary['owner_pages_with_some_crosswalk_percent']}%); "
          f"fully reconciled: {states['fully-reconciled']} "
          f"({summary['owner_pages_fully_reconciled_percent']}%)")
    print("ALL already-documented finding-level coverage: NOT YET MEASURED.")
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {args.json}")

if __name__ == "__main__":
    main()
