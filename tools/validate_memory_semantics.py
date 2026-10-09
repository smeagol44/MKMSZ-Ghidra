#!/usr/bin/env python3
"""Validate established Memory Map semantic contracts; no ROM, emulator or Ghidra writes."""
import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"analysis"
def read(n):
    with (ROOT/n).open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f,delimiter="\t"))
facts=read("memory_semantic_contracts.tsv")
claims={x["fact_id"]:x for x in read("known_knowledge_claims.tsv")}
functions={x["address"] for x in read("functions.tsv")}
regions=read("memory_ownership_intervals.tsv")
assert len(facts)==24 and {r["fact_id"] for r in facts}=={f"MEC-{i:02d}" for i in range(1,25)}
assert len(regions)==89
assert {r["source_blob_sha"] for r in facts}=={"baab85791306bdd386d11d5a946753f22081bdc5"}
native={r["ghidra_target"] for r in facts if r["disposition"]=="ghidra"}
assert native=={"0x80066390","0x8006643C","0x80066478"}
assert native<=functions
for r in facts:
    c=claims[r["fact_id"]]
    assert c["owner_page"]==r["owner_page"]=="Memory-and-Allocation-Map.md"
    assert c["wiki_source_anchor"]==r["source_anchor"] and c["section"]==r["source_section"]
    assert int(r["source_line"])>0 and r["source_section"].startswith(("## ", "### "))
    assert r["conclusion"] and r["evidence"] and r["scope"] and r["review_caution"]
    if r["disposition"]=="ghidra":
        assert c["migration_status"]=="ghidra-confirmed" and c["target_path"]=="analysis/functions.tsv"
        assert c["target_key"]==r["ghidra_target"]
    else:
        assert r["disposition"]=="companion" and not r["ghidra_target"]
        assert c["migration_status"]=="wiki-or-sidecar-routed"
        assert c["target_path"]=="analysis/memory_semantic_contracts.tsv"
        assert c["target_key"]==r["fact_id"]
sem={r["fact_id"]:r["conclusion"] for r in facts}
assert "0x1AF420,0x1B3420" in sem["MEC-15"] and "0x801B3420" in sem["MEC-15"]
assert "0x800EECD0" in sem["MEC-16"] and "0x80111ECC" in sem["MEC-16"]
assert "Water" in sem["MEC-18"] and "stage-specific" in sem["MEC-18"]
assert "no" in sem["MEC-20"].lower() and "free" in sem["MEC-20"].lower()
assert "aliases" in sem["MEC-21"] and "overlaps" in sem["MEC-21"]
assert all(r["classification"]!="confirmed-free" for r in regions)
print("24 source-pinned Memory Map contracts, 89 prior intervals, 3 pre-imported functions verified.")
print("ROM/RDRAM alias, proof, stage overlay, lifetime and no-free-space safety retained.")
