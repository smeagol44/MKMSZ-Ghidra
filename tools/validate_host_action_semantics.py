#!/usr/bin/env python3
"""Validate pinned native host facts and staged special-action descriptor safely."""
import csv
from pathlib import Path
A=Path(__file__).resolve().parents[1]/"analysis"
def read(p):
    with (A/p).open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f,delimiter="\t"))
facts=read("host_action_semantic_contracts.tsv")
claims={r["fact_id"]:r for r in read("known_knowledge_claims.tsv")}
funcs={r["address"]:r for r in read("functions.tsv")}
comments={(r["scope"],r["address"],r["kind"]):r for r in read("comments.tsv")}
types=[r for r in read("types.tsv") if r["name"]=="MKMSZ_SpecialActionDescriptor"]
data=read("data.tsv")
assert len(facts)==32 and {r["fact_id"] for r in facts}=={f"HAC-{i:02d}" for i in range(1,33)}
assert {r["source_blob_sha"] for r in facts}=={"2e78935342111ce60168ac7d08b6c03d7ea1a6fe"}
assert len({r["source_section"] for r in facts})==21
assert len(types)==8 and types[0]["kind"]=="struct" and types[0]["size"]=="0x2C"
expected={"legal_button_masks":(0x00,4,"u16[2]"),"transfer_selector":(0x04,4,"u32"),
          "condition_callback":(0x08,4,"ptr32"),"action_callback":(0x0C,4,"ptr32"),
          "history_window":(0x10,2,"u16"),"facing_right_tokens":(0x12,12,"u16[6]"),
          "facing_left_tokens":(0x1E,14,"u16[7]")}
used=set()
for r in types[1:]:
    off,size,dt=expected[r["field"]]
    assert r["kind"]=="field" and int(r["offset"],16)==off and r["datatype"]==dt
    bs=set(range(off,off+size))
    assert not used.intersection(bs)
    used.update(bs)
assert used==set(range(0x2C)) and len(types[1:])==len(expected)
assert len(data)==1 and data[0]["scope"]=="global"
assert data[0]["address"]=="0x800B0F68" and data[0]["datatype"]=="MKMSZ_SpecialActionDescriptor"
assert "0x800B0F94" in data[0]["note"]
assert sum(r["disposition"]=="ghidra-existing" for r in facts)==17
assert sum(r["disposition"]=="ghidra-staged" for r in facts)==2
for r in facts:
    c=claims[r["fact_id"]]
    assert r["owner_page"]==c["owner_page"]=="Player-Actions-and-Special-Moves.md"
    assert r["source_anchor"]==c["wiki_source_anchor"] and r["source_section"]==c["section"]
    assert int(r["source_line"])>0 and r["review_caution"]
    if r["disposition"]=="ghidra-existing":
        assert c["migration_status"]=="ghidra-confirmed" and c["target_path"]=="analysis/functions.tsv"
        assert c["target_key"]==r["ghidra_target"] and c["target_key"] in funcs
    elif r["disposition"]=="ghidra-staged":
        assert c["migration_status"]=="wiki-or-sidecar-routed"
        assert c["target_path"] in ("analysis/types.tsv","analysis/data.tsv")
    else:
        assert r["disposition"]=="companion"
        assert c["target_path"]=="analysis/host_action_semantic_contracts.tsv"
        assert c["target_key"]==r["fact_id"]
for va in ("0x80028F3C","0x80032CD4","0x8004CC50","0x80017F80","0x8004CBC4"):
    assert "Player-Actions-and-Special-Moves.md" in funcs[va]["comment"]
    assert "Player-Actions-and-Special-Moves.md" in comments[("global",va,"repeatable")]["text"]
assert "self-reenters" in funcs["0x80032CD4"]["comment"]
print("32 source-pinned host claims, 17 preexisting function links and five enriched comments validated.")
print("New 0x2C descriptor type plus stock global instance staged, not yet locally imported.")
