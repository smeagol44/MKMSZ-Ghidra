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
    if rule == "baseline-definitions":
        return sum(r["kind"] in ("struct","enum") and r["name"] != "MKMSZ_SpecialActionDescriptor" for r in entries)
    if rule == "new-special-action-definition":
        return sum(r["kind"]=="struct" and r["name"]=="MKMSZ_SpecialActionDescriptor" for r in entries)
    if rule == "trace-sites":
        # Counts trace-category bookmark sites: 86 new trace locations plus 6 supplemental existing-site bookmarks.
        return len({(r["scope"], r["address"].lower()) for r in entries
                    if r["category"].startswith("trace-")})
    if rule == "staged-navigation":
        return len({(r["scope"], r["address"].lower()) for r in entries
                    if r["category"] == "known-stock-navigation"})
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
    audited = records(ROOT / "analysis/known_knowledge_claims.tsv")
    if not audited or len({r["fact_id"] for r in audited}) != len(audited):
        raise ValueError("Missing or duplicate claim IDs")
    legal = {"ghidra-confirmed", "wiki-or-sidecar-routed", "known-in-wiki-unlinked"}
    owner_names = {row["owner_page"] for row in owners}
    claim_status = Counter()
    for claim in audited:
        status = claim["migration_status"]
        if status not in legal or claim["owner_page"] not in owner_names:
            raise ValueError(f"Invalid claim ownership or status: {claim['fact_id']}")
        if not claim["wiki_source_anchor"] or not claim["finding"]:
            raise ValueError(f"Missing claim evidence: {claim['fact_id']}")
        if args.wiki_dir:
            actual = (args.wiki_dir / claim["owner_page"]).read_text(encoding="utf-8")
            if claim["wiki_source_anchor"] not in actual:
                raise ValueError(f"Stale Wiki anchor: {claim['fact_id']}")
        path, key = claim["target_path"], claim["target_key"]
        if status == "known-in-wiki-unlinked":
            if path or key:
                raise ValueError(f"Unlinked claim has mapped target: {claim['fact_id']}")
        elif path.startswith("analysis/"):
            target = ROOT / path
            if not target.is_file() or not key:
                raise ValueError(f"Missing analysis target: {claim['fact_id']}")
            rows = records(target)
            if path.endswith("audio_testlab_known_contracts.tsv") or path.endswith("xp_progression_contracts.tsv") or path.endswith("memory_semantic_contracts.tsv") or path.endswith("global_item_semantic_contracts.tsv") or path.endswith("enemy_semantic_contracts.tsv") or path.endswith("host_action_semantic_contracts.tsv"):
                matched = any(r.get("fact_id") == key for r in rows)
            elif path.endswith("stage_flow_contracts.tsv"):
                matched = any(r.get("fact_id") == key for r in rows)
            elif path.endswith("remaining_owner_facts.tsv"):
                matched = any(r.get("fact_id") == key for r in rows)
            elif path.endswith("owner_product_findings.tsv"):
                matched = any(r.get("fact_id") == key for r in rows)
            elif path.endswith("owner_research_findings.tsv"):
                matched = any(r.get("fact_id") == key for r in rows)
            elif path.endswith("core_runtime_invariants.tsv") or path.endswith("xp_thresholds.tsv"):
                matched = any(r.get("fact_id") == key for r in rows)
            elif path.endswith("stock_rom_navigation.tsv"):
                matched = any(r.get("fact_id") == key for r in rows)
            elif path.endswith("known_knowledge_decisions.tsv"):
                matched = any(r.get("fact_id") == key for r in rows)
            elif path.endswith("memory_ownership_intervals.tsv"):
                matched = any(r.get("region_id") == key for r in rows)
            elif path.endswith("function_registry_crosswalk.tsv"):
                matched = any(r.get("registry_id") == key for r in rows)
            elif path.endswith("stage_resource_caveats.tsv"):
                matched = any(r.get("stage") == key for r in rows)
            elif path.endswith("lifecycle_contracts.tsv"):
                matched = any(r.get("fact_id") == key for r in rows)
            elif path.endswith("stage_resource_files.tsv"):
                parts = key.split("|")
                matched = (any(r.get("stage") == key for r in rows) if len(parts) == 1
                           else len(parts) == 2 and parts[0] == "ALL" and len(rows) == int(parts[1]))
            elif path.endswith("rom_pickups.tsv") or path.endswith("stage_resource_slots.tsv"):
                parts = key.split("|")
                matched = (len(parts) == 2 and
                           (len(rows) == int(parts[1]) if parts[0] == "ALL"
                            else sum(1 for r in rows if r.get("stage") == parts[0]) == int(parts[1])))
            elif path.endswith("overlay_functions.tsv"):
                parts = key.split("|")
                matched = (len(parts) == 2 and
                           any(r.get("scope", "").lower() == parts[0].lower() and
                               r.get("address", "").lower() == parts[1].lower() for r in rows))
            elif path.endswith("overlay_functions.tsv"):
                parts = key.split("|")
                matched = len(parts) == 2 and any(
                    r.get("scope") == parts[0] and r.get("address", "").lower() == parts[1].lower()
                    for r in rows)
            elif path.endswith("overlays.tsv"):
                matched = any(r.get("scope", "").lower() == key.lower() for r in rows)
            elif path.endswith("types.tsv"):
                parts = key.split("|")
                matched = (len(parts) == 2 and
                           any(r.get("name") == parts[0] and r.get("field") == parts[1]
                               for r in rows))
            else:
                keyfield = "record_id" if path.endswith("rom_patch_sites.tsv") else "address"
                matched = any(r.get(keyfield, "").lower() == key.lower() for r in rows)
            if not matched:
                raise ValueError(f"Unresolved manifest target: {claim['fact_id']}")
        elif path.startswith("wiki/") and not key:
            if args.wiki_dir and not (args.wiki_dir / path[5:]).is_file():
                raise ValueError(f"Missing routed Wiki owner: {claim['fact_id']}")
        else:
            raise ValueError(f"Invalid target routing: {claim['fact_id']}")
        claim_status[status] += 1
    scoped_total = len(audited)
    scoped_reusable = claim_status["ghidra-confirmed"] + claim_status["wiki-or-sidecar-routed"]
    directly_migrated = sum(
        claim["migration_status"] == "ghidra-confirmed" or
        (claim["migration_status"] == "wiki-or-sidecar-routed" and
         claim["target_path"].startswith("analysis/"))
        for claim in audited
    )
    wiki_only = sum(
        claim["migration_status"] == "wiki-or-sidecar-routed" and
        claim["target_path"].startswith("wiki/")
        for claim in audited
    )
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
        "audited_known_claims": scoped_total,
        "audited_reusable_claims": scoped_reusable,
        "audited_unlinked_claims": claim_status["known-in-wiki-unlinked"],
        "audited_ghidra_claims": claim_status["ghidra-confirmed"],
        "audited_routed_claims": claim_status["wiki-or-sidecar-routed"],
        "audited_known_claim_reuse_percent": round(100.0 * scoped_reusable / scoped_total, 2),
        "audited_directly_migrated_claims": directly_migrated,
        "audited_direct_migration_percent": round(100.0 * directly_migrated / scoped_total, 2),
        "audited_wiki_only_routed_claims": wiki_only,
        "audited_scope": "Selected source-anchored known findings across multiple owners; corpus not fully enumerated",
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
    print(f"Audited known findings: {scoped_reusable}/{scoped_total} reusable "
          f"({summary['audited_known_claim_reuse_percent']}%); "
          f"{claim_status['known-in-wiki-unlinked']} unlinked")
    print(f"First-class Ghidra / explicit sidecar migration: {directly_migrated}/{scoped_total} "
          f"({summary['audited_direct_migration_percent']}%); "
          f"Wiki-only routed: {wiki_only}. Do not equate Wiki-only with migrated metadata.")
    print("ALL already-documented finding-level coverage: NOT YET MEASURED.")
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {args.json}")

if __name__ == "__main__":
    main()
