#!/usr/bin/env python3
"""Verify owner-pinned enemy construction and resource lifetime metadata."""
import csv
from pathlib import Path
A=Path(__file__).resolve().parents[1]/"analysis"
def tsv(name):
    with (A/name).open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f,delimiter="\t"))
facts=tsv("enemy_semantic_contracts.tsv")
claims={r["fact_id"]:r for r in tsv("known_knowledge_claims.tsv")}
functions={r["address"]:r for r in tsv("functions.tsv")}
comments={(r["scope"],r["address"],r["kind"]):r for r in tsv("comments.tsv")}
types={(r["name"],r["field"]) for r in tsv("types.tsv")}
overlays={(r["scope"],r["address"].lower()) for r in tsv("overlay_functions.tsv")}
assert len(facts)==30 and {r["fact_id"] for r in facts}=={f"ECS-{i:02d}" for i in range(1,31)}
assert {r["source_blob_sha"] for r in facts}=={"2eeb8c913d93220fcba826fcfa462522daeabcff"}
assert len({r["source_section"] for r in facts})==21
assert sum(r["disposition"]=="ghidra" for r in facts)==11
for r in facts:
    c=claims[r["fact_id"]]
    assert c["owner_page"]==r["owner_page"]=="Enemy-Randomization.md"
    assert c["wiki_source_anchor"]==r["source_anchor"] and c["section"]==r["source_section"]
    assert int(r["source_line"])>0 and r["source_section"].startswith(("## ","### "))
    assert r["conclusion"] and r["evidence"] and r["review_caution"]
    assert c["finding"].startswith(r["conclusion"])
    if r["disposition"]=="companion":
        assert not r["ghidra_target"] and c["target_path"]=="analysis/enemy_semantic_contracts.tsv"
        assert c["target_key"]==r["fact_id"] and c["migration_status"]=="wiki-or-sidecar-routed"
    else:
        assert c["migration_status"]=="ghidra-confirmed"
        p=c["target_path"];target=r["ghidra_target"]
        if p=="analysis/functions.tsv":
            assert target in functions
        elif p=="analysis/types.tsv":
            t=target.split("|");assert len(t)==2 and tuple(t) in types
        else:
            assert p=="analysis/overlay_functions.tsv"
            t=target.split("|");assert len(t)==2 and (t[0],t[1].lower()) in overlays
for addr in ("0x80071500","0x800719F0","0x80071B20","0x8002FCDC"):
    assert "Enemy-Randomization.md" in functions[addr]["comment"]
    assert "Enemy-Randomization.md" in comments[("global",addr,"repeatable")]["text"]
assert "overlay_prison|0x802F0754" in {r["ghidra_target"] for r in facts}
assert "MKMSZ_EnemySpawnConditionalRecord|required_mask" in {r["ghidra_target"] for r in facts}
assert any("Pending" in r["evidence"] for r in facts)
print("30 enemy/resource lifetime claims; 11 prior Ghidra object links; 4 updated native comments validated.")
