#!/usr/bin/env python3
"""Ensure existing guarded patch sites and Ghidra types have traceable Wiki owners.

The source-row manifest annotates existing 151 guarded-site entries. Multiple
matching offset strings are disambiguated by the original owner/purpose column.
This does not grant patch permission or assert that proof sites are production.
"""
import csv
from pathlib import Path
R=Path(__file__).resolve().parents[1]/"analysis"
def table(p):
    with (R/p).open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f,delimiter="\t"))
provenance=table("patch_registry_provenance.tsv")
typemap=table("type_owner_provenance.tsv")
claims={r["fact_id"]:r for r in table("known_knowledge_claims.tsv")}
patch={r["record_id"]:r for r in table("rom_patch_sites.tsv")}
types={(r["name"],r["kind"]):r for r in table("types.tsv") if r["kind"] in ("struct","enum")}
assert len(provenance)==len(patch)==151
assert len(typemap)==len(types)==11
assert len({r["record_id"] for r in provenance})==151
assert len({r["type_name"] for r in typemap})==11
for r in provenance:
    c=claims["PATCH-"+r["record_id"].replace("reg_","")]
    assert c["target_path"]=="analysis/rom_patch_sites.tsv"
    assert c["target_key"]==r["record_id"]
    assert c["owner_page"]=="Address-and-Patch-Site-Registry.md"
    assert c["wiki_source_anchor"]==r["rom_or_location"]
    assert int(r["source_line"])>0 and int(r["source_match_count"])>=1
    assert len(r["source_blob_sha"])==40
    assert patch[r["record_id"]]["rom_or_location"]==r["rom_or_location"]
for r in typemap:
    c=claims["DTYPE-"+r["type_name"]]
    assert c["owner_page"]=="Data-Structures-and-Encodings.md"
    assert c["migration_status"]=="ghidra-confirmed"
    assert c["target_path"]=="analysis/types.tsv"
    assert c["target_key"]==r["type_name"]+"|"
    assert (r["type_name"],r["type_kind"]) in types
    assert types[(r["type_name"],r["type_kind"])]["size"]==r["type_size"]
    assert len(r["source_blob_sha"])==40
print("151 guarded sites source-linked; 11 already imported curated types owner-linked.")
