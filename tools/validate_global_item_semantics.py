#!/usr/bin/env python3
"""Validate established global item/solver crosswalk against native function metadata."""
import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"analysis"
def read(name):
    with (ROOT/name).open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))
facts=read("global_item_semantic_contracts.tsv")
claims={x["fact_id"]:x for x in read("known_knowledge_claims.tsv")}
functions={x["address"]:x for x in read("functions.tsv")}
comments={(x["scope"],x["address"],x["kind"]):x for x in read("comments.tsv")}
assert len(facts)==28 and {r["fact_id"] for r in facts}=={f"GXC-{i:02d}" for i in range(1,29)}
assert {r["source_blob_sha"] for r in facts}=={"aa0c57ec35faa8e892a3d0f34bcf5912a28ae8d3"}
assert len({r["source_section"] for r in facts})==23
direct={r["ghidra_target"] for r in facts if r["disposition"]=="ghidra"}
assert direct=={"0x80038770","0x8003BF4C","0x80062D60","0x80038ACC","0x80075448","0x80003428"}
assert direct<=functions.keys()
for r in facts:
    c=claims[r["fact_id"]]
    assert r["owner_page"]==c["owner_page"]=="Global-Item-Materialization-and-Solvability.md"
    assert r["source_anchor"]==c["wiki_source_anchor"] and r["source_section"]==c["section"]
    assert r["source_section"].startswith(("## ","### "))
    assert int(r["source_line"])>0 and r["conclusion"] and r["review_caution"]
    if r["disposition"]=="ghidra":
        assert c["migration_status"]=="ghidra-confirmed" and c["target_path"]=="analysis/functions.tsv"
        assert c["target_key"]==r["ghidra_target"]
    else:
        assert r["disposition"]=="companion" and not r["ghidra_target"]
        assert c["migration_status"]=="wiki-or-sidecar-routed" and c["target_path"]=="analysis/global_item_semantic_contracts.tsv"
        assert c["target_key"]==r["fact_id"]
native=functions["0x80038ACC"]["comment"]
assert "0x800393BC..0x800393D0" in native and "does not pass destination ordinal" in native
note=comments[("global","0x80038ACC","repeatable")]["text"]
assert "without destination ordinal" in note
assert any(r["scope"]=="temple-a0-overlay" and r["disposition"]=="companion" for r in facts)
assert any("Pending" in r["evidence"] for r in facts)
print("28 source-pinned global-item contracts verified: six native links, one updated pickup-manager Ghidra comment.")
print("Temple/Fortress overlay coordinates remain companion-only; no cross-ROM donor mapping or production patch.")
