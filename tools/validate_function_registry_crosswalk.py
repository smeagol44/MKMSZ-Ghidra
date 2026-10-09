#!/usr/bin/env python3
"""Validate Function Registry crosswalk without creating new Ghidra functions."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "analysis"

def table(filename):
    with (ROOT / filename).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))

registry = table("function_registry_crosswalk.tsv")
globals_ = {row["address"].lower() for row in table("functions.tsv")}
labels = {(row["scope"], row["address"].lower()) for row in table("code_labels.tsv")}
overlays = {(row["scope"], row["address"].lower()) for row in table("overlay_functions.tsv")}
claims = {row["fact_id"]: row for row in table("known_knowledge_claims.tsv")}
assert len(registry) == 166
assert len({r["registry_id"] for r in registry}) == 166
stats = {"all-addresses-indexed": 0, "partially-indexed": 0, "no-direct-address-index": 0}
for item in registry:
    key = item["registry_id"]
    scope = item["scope"]
    declared = item["addresses"].split(",")
    assert declared and all(a.startswith("0x") and len(a) == 10 for a in declared)
    found = [a for a in declared if ((a in globals_ or ("global", a) in labels)
                                      if scope == "global" else (scope, a) in overlays)]
    missing = [a for a in declared if a not in found]
    assert item["indexed_addresses"] == ",".join(found), key
    assert item["unindexed_addresses"] == ",".join(missing), key
    category = ("all-addresses-indexed" if not missing else
                "partially-indexed" if found else "no-direct-address-index")
    assert item["address_index_status"] == category, key
    assert len(item["source_blob_sha"]) == 40 and item["documented_contract"]
    record = claims[key]
    assert record["wiki_source_anchor"] == item["wiki_source_anchor"]
    if category == "all-addresses-indexed":
        assert record["migration_status"] == "ghidra-confirmed", key
    else:
        assert record["target_path"] == "analysis/function_registry_crosswalk.tsv"
        assert record["target_key"] == key
    stats[category] += 1
assert stats == {"all-addresses-indexed": 144, "partially-indexed": 4, "no-direct-address-index": 18}, stats
print("Function Registry crosswalk: 166 known rows; 144 fully indexed; "
      "4 partially indexed; 18 lacking direct address entries; all contracts preserved.")
