#!/usr/bin/env python3
"""Audit already-established N64 XP/progression crosswalk without ROM or emulator."""
import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"analysis"
def read(n):
    with (ROOT/n).open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f,delimiter="\t"))
rows=read("xp_progression_contracts.tsv")
claims={r["fact_id"]:r for r in read("known_knowledge_claims.tsv")}
functions={r["address"] for r in read("functions.tsv")}
assert len(rows)==18 and {r["fact_id"] for r in rows}=={f"XPS-{i:02d}" for i in range(1,19)}
assert {r["source_blob_sha"] for r in rows}=={"817b1ed3efd1b83fa142cb929b976763f94a6f46"}
direct=[r for r in rows if r["disposition"]=="ghidra"]
assert {r["ghidra_target"] for r in direct}=={"0x8002E104","0x80074FBC","0x80078A18"}
assert {r["ghidra_target"] for r in direct}<=functions
for r in rows:
    c=claims[r["fact_id"]]
    assert c["owner_page"]==r["owner_page"]=="XP-and-Progression.md"
    assert c["wiki_source_anchor"]==r["source_anchor"] and c["section"]==r["source_section"]
    assert int(r["source_line"])>0 and r["source_section"].startswith("## ")
    assert r["conclusion"] and r["evidence"] and r["scope"] and r["review_caution"]
    if r["disposition"]=="ghidra":
        assert c["migration_status"]=="ghidra-confirmed"
        assert c["target_path"]=="analysis/functions.tsv"
        assert c["target_key"]==r["ghidra_target"]
    else:
        assert r["disposition"]=="companion" and not r["ghidra_target"]
        assert c["migration_status"]=="wiki-or-sidecar-routed"
        assert c["target_path"]=="analysis/xp_progression_contracts.tsv"
        assert c["target_key"]==r["fact_id"]
assert any("Pending" in r["evidence"] for r in rows)
assert any("stage-overlay" in r["scope"] for r in rows)
assert any("rejected" in r["scope"] for r in rows)
print("18 XP/progression contracts source-pinned; 3 reuse existing Ghidra functions.")
