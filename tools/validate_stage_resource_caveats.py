#!/usr/bin/env python3
"""Verify existing stage-bound caveats are first-class versioned metadata."""
import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"analysis"
def records(file):
    with (ROOT/file).open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f,delimiter="\t"))
facts=records("stage_resource_caveats.tsv")
claims={x["fact_id"]:x for x in records("known_knowledge_claims.tsv")}
stages={x["stage"] for x in records("stage_resource_files.tsv")}
assert len(facts)==len(stages)==8
assert {x["stage"] for x in facts}==stages
for item in facts:
    assert item["claim_id"]=="STAGE-"+item["stage"].upper()+"-BOUND"
    assert len(item["source_blob_sha"])==40
    assert all(item[x] for x in ("canonical_finding","evidence","source_anchor","caveat_kind"))
    claim=claims[item["claim_id"]]
    assert claim["target_path"]=="analysis/stage_resource_caveats.tsv"
    assert claim["target_key"]==item["stage"]
    assert claim["wiki_source_anchor"]==item["source_anchor"]
print("Eight stage-specific caveats crosslinked and scope-qualified.")
