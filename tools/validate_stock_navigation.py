#!/usr/bin/env python3
"""Validate seven staged Ghidra navigation anchors and one ROM-only coordinate.

Staged means versioned in import manifests; it does not claim a local Ghidra run.
"""
import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"analysis"
def read(n):
    with (ROOT/n).open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f,delimiter="\t"))
bookmarks=[x for x in read("bookmarks.tsv") if x["category"]=="known-stock-navigation"]
claims={r["fact_id"]:r for r in read("known_knowledge_claims.tsv")}
assert len(bookmarks)==7
assert len({(r["scope"],r["address"]) for r in bookmarks})==7
for bookmark in bookmarks:
    assert bookmark["scope"]=="global"
    assert bookmark["address"].startswith("0x") and len(bookmark["address"])==10
    assert "Pending" in bookmark["evidence"]
    assert any(c["target_path"]=="analysis/bookmarks.tsv" and c["target_key"]==bookmark["address"]
               for c in claims.values())
palette=read("stock_rom_navigation.tsv")
assert len(palette)==1
r=palette[0]
assert r["fact_id"]=="RES-027" and r["coordinate_space"]=="rom-clean-usa-rev0"
assert r["stock_rom_offset"]=="0x000B3360" and r["related_rom_offset"]=="0x000B3364"
assert r["ghidra_va_status"]=="not-mapped-to-global-VA"
assert claims[r["fact_id"]]["target_key"]=="RES-027"
print("7 global bookmarks staged for local Ghidra import; 1 title palette retained ROM-only.")
