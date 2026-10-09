#!/usr/bin/env python3
"""Bounded manifest/claim integrity for canonical lifecycle findings."""
import csv
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]/"analysis"
def read(file):
    with (BASE/file).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))
contract=read("lifecycle_contracts.tsv")
claims=read("known_knowledge_claims.tsv")
assert len(contract)==22
assert len({r["fact_id"] for r in contract})==len(contract)
claimsById={c["fact_id"]:c for c in claims}
for r in contract:
    id=r["fact_id"]
    assert id.startswith("PERS-") and r["owner_page"]=="Persistence-Inventory-and-Lifecycle.md"
    assert len(r["source_blob_sha"])==40
    assert all(r[x] for x in ("canonical_behavior","wiki_anchor","evidence","scope","reproduction_boundary"))
    c=claimsById[id]
    assert c["wiki_source_anchor"]==r["wiki_anchor"]
    assert c["target_path"]=="analysis/lifecycle_contracts.tsv" and c["target_key"]==id
    assert c["migration_status"]=="wiki-or-sidecar-routed"
assert any("v04" in r["fact_id"] or "v04" in r["canonical_behavior"] for r in contract)
assert any("Temple" in r["canonical_behavior"] for r in contract)
print("22 lifecycle contracts resolved, source-qualified and claim-linked.")
