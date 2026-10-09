#!/usr/bin/env python3
"""Validate provenance-pinned 40-owner section snapshot and audited claim sums."""
import csv
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]/"analysis"
def read(path):
    with (BASE/path).open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f,delimiter="\t"))
entries=read("owner_section_audit_snapshot.tsv")
claims=read("known_knowledge_claims.tsv")
owners=read("known_knowledge_owners.tsv")
assert len(entries)==len(owners)==40
assert {r["owner_page"] for r in entries}=={r["owner_page"] for r in owners}
assert len(claims)==sum(int(r["existing_claims"]) for r in entries)==759
assert sum(int(r["level_2_3_headings"]) for r in entries)==713
assert sum(int(r["headings_with_unique_anchor"]) for r in entries)==160
assert sum(int(r["stale_claims"]) for r in entries)==0
assert sum(int(r["ambiguous_claims"]) for r in entries)==30
assert sum(int(r["preamble_claims"]) for r in entries)==32
for entry in entries:
    assert len(entry["wiki_source_blob_sha"])==40
    assert entry["audit_scope"]=="raw anchor scan; not semantic exhaustiveness"
    assert 0<=int(entry["headings_with_unique_anchor"])<=int(entry["level_2_3_headings"])
print("40 pinned Wiki owners: 160/713 heading anchors, 759 claims, 30 ambiguous, 0 stale.")
print("This is source navigation only, NOT percent of all known knowledge.")
