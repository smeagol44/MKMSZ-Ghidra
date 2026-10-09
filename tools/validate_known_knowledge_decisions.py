#!/usr/bin/env python3
"""Validate source-linked project knowledge decisions, not runtime behavior."""
import csv
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]/"analysis"
def read(name):
    with (BASE/name).open(encoding="utf-8",newline="") as stream:
        return list(csv.DictReader(stream,delimiter="\t"))
rows=read("known_knowledge_decisions.tsv")
claims={r["fact_id"]:r for r in read("known_knowledge_claims.tsv")}
assert len(rows)==len({r["fact_id"] for r in rows})==63
for r in rows:
    id=r["fact_id"]
    c=claims[id]
    assert c["target_path"]=="analysis/known_knowledge_decisions.tsv" and c["target_key"]==id
    assert r["source_anchor"]==c["wiki_source_anchor"] and r["source_owner"]==c["owner_page"]
    assert len(r["source_blob_sha"])==40
    assert all(r[k] for k in ("canonical_wiki_owner","documented_finding","evidence","scope","interpretation_kind","review_caution"))
    if r["interpretation_kind"]=="release-requirement":
        assert "requirement" in r["review_caution"].lower()
    if r["interpretation_kind"]=="rejected-or-superseded":
        assert "rejected" in r["review_caution"].lower()
print("63 bounded canonical decisions indexed and claim-linked.")
