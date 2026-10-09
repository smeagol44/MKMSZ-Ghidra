#!/usr/bin/env python3
"""Verify current Core Runtime and native XP source-specific knowledge records."""
import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"analysis"
def read(name):
    with (ROOT/name).open(encoding="utf-8",newline="") as stream:
        return list(csv.DictReader(stream,delimiter="\t"))
core=read("core_runtime_invariants.tsv")
xp=read("xp_thresholds.tsv")
claims={r["fact_id"]:r for r in read("known_knowledge_claims.tsv")}
assert len(core)==18
for r in core:
    assert r["fact_id"] in claims
    assert r["owner_page"]=="Core-Runtime-and-Address-Database.md"
    assert r["source_anchor"]==claims[r["fact_id"]]["wiki_source_anchor"]
    assert claims[r["fact_id"]]["target_path"]=="analysis/core_runtime_invariants.tsv"
    assert len(r["source_blob_sha"])==40
assert [int(r["tier"]) for r in xp]==list(range(1,10))
assert [int(r["xp"]) for r in xp]==[85,258,834,1410,2323,3315,4503,5911,7354]
for r in xp:
    assert len(r["source_blob_sha"])==40
    assert claims[r["fact_id"]]["target_path"]=="analysis/xp_thresholds.tsv"
    assert claims[r["fact_id"]]["wiki_source_anchor"]==r["source_anchor"]
print("18 core runtime invariants and 9 native XP thresholds validated.")
