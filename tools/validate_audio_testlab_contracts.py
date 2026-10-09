#!/usr/bin/env python3
"""Check bounded host SFX and TEST LAB HUD findings; do not import into Ghidra."""
import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"analysis"
def read(name):
    with (ROOT/name).open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f,delimiter="\t"))
facts=read("audio_testlab_known_contracts.tsv")
claims={c["fact_id"]:c for c in read("known_knowledge_claims.tsv")}
functions={f["address"] for f in read("functions.tsv")}
by_owner={owner:[r for r in facts if r["owner_page"]==owner]
    for owner in ("Sounds-and-Music.md","Test-Lab-Inventory-Hang-Static-Diagnosis.md")}
assert len(facts)==36 and len({f["fact_id"] for f in facts})==36
assert {len(rows) for rows in by_owner.values()}=={18}
direct=[f for f in facts if f["disposition"]=="ghidra"]
assert {f["ghidra_target"] for f in direct}=={
    "0x80064C18","0x80080A88","0x8007EC4C"}
assert set(f["ghidra_target"] for f in direct).issubset(functions)
for f in facts:
    c=claims[f["fact_id"]]
    assert f["owner_page"]==c["owner_page"]
    assert f["source_anchor"]==c["wiki_source_anchor"]
    assert f["source_section"]==c["section"]
    assert len(f["source_blob_sha"])==40
    assert int(f["source_line"])>0
    assert f["conclusion"] and f["evidence"] and f["review_caution"]
    if f["disposition"]=="ghidra":
        assert c["migration_status"]=="ghidra-confirmed"
        assert c["target_path"]=="analysis/functions.tsv"
        assert c["target_key"]==f["ghidra_target"]
    else:
        assert f["disposition"]=="companion" and not f["ghidra_target"]
        assert c["migration_status"]=="wiki-or-sidecar-routed"
        assert c["target_path"]=="analysis/audio_testlab_known_contracts.tsv"
        assert c["target_key"]==f["fact_id"]
assert any("Pending" in f["evidence"] for f in by_owner["Sounds-and-Music.md"])
assert any("v20" in f["conclusion"] for f in by_owner["Test-Lab-Inventory-Hang-Static-Diagnosis.md"])
print("36 canonical audio/TEST LAB contracts verified; three reuse existing Ghidra functions.")
print("No new Ghidra code and no production Inventory-audio root-cause assertion.")
