#!/usr/bin/env python3
"""Validate the Wiki's classified memory ownership; never infer new free bytes."""
import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"analysis"
def read(file):
    with (ROOT/file).open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f,delimiter="\t"))
memory=read("memory_ownership_intervals.tsv")
claims={x["target_key"]:x for x in read("known_knowledge_claims.tsv")
        if x["target_path"]=="analysis/memory_ownership_intervals.tsv"}
assert len(memory)==len(claims)==89
assert len({m["region_id"] for m in memory})==89
assert sum(m["space"]=="rom" for m in memory)==54
assert sum(m["space"]=="rdram-physical" for m in memory)==35
assert not any(m["classification"]=="confirmed-free" for m in memory)
for row in memory:
    key=row["region_id"]
    assert key in claims and claims[key]["wiki_source_anchor"] == "<code>"+key+"</code>"
    assert len(row["source_blob_sha"])==40
    assert row["space"] in ("rom","rdram-physical")
    segments=[pair.split(":") for pair in row["segments"].split(";")]
    assert len(segments)==int(row["segment_count"])
    for pair in segments:
        assert len(pair)==2
        start,end=[int(v,16) for v in pair]
        assert 0<=start<end
        if row["space"]=="rdram-physical":
            assert end<=0x400000, key
    if len(segments)==1:
        assert row["start"]==segments[0][0] and row["end_exclusive"]==segments[0][1]
    else:
        assert not row["start"] and not row["end_exclusive"], key
    if row["classification"] in ("proof-only","stock-unknown","rejected/conflict"):
        assert row["production_safe"] not in ("yes","global output"),key
    # KSEG views must represent same physical start as canonical record,
    # never be counted as additional space.
    if row["space"]=="rdram-physical":
        start=int(segments[0][0],16)
        aliases=row["aliases"]
        assert "0x"+format(0x80000000+start,"X") in aliases,key
        assert "0x"+format(0xA0000000+start,"X") in aliases,key
print("Memory ownership validated: 54 ROM + 35 RDRAM records; no confirmed-free promotion.")
