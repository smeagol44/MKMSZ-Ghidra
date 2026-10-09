#!/usr/bin/env python3
"""Verify static and bounded runtime Stage Flow contracts have stable owner links."""
import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"analysis"
def read(name):
    with (ROOT/name).open(encoding="utf-8",newline="") as file:
        return list(csv.DictReader(file,delimiter="\t"))
rows=read("stage_flow_contracts.tsv")
claims={x["fact_id"]:x for x in read("known_knowledge_claims.tsv")}
assert len(rows)==len({x["fact_id"] for x in rows})==17
for row in rows:
    c=claims[row["fact_id"]]
    assert c["owner_page"]==row["canonical_owner"]=="Stage-Flow-and-Selector.md"
    assert c["target_path"]=="analysis/stage_flow_contracts.tsv"
    assert c["target_key"]==row["fact_id"]
    assert c["wiki_source_anchor"]==row["source_anchor"]
    assert int(row["source_line"])>0 and len(row["source_blob_sha"])==40
    assert row["behavior_or_constraint"] and row["limitation"] and row["evidence"]
negative=[r for r in rows if r["scope"].endswith("negative")]
assert len(negative)>=2
assert any("unbuilt" in r["scope"] for r in rows)
assert any("only immediate" in r["behavior_or_constraint"] for r in rows)
print("17 stage-flow claims source-linked; bounded, rejected and unbuilt paths preserved.")
