#!/usr/bin/env python3
"""Validate eight stage resource-file maps without interpreting resources as code."""
import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"analysis"
def data(name):
    with (ROOT/name).open(encoding="utf-8",newline="") as stream:
        return list(csv.DictReader(stream,delimiter="\t"))
resources=data("stage_resource_files.tsv")
overlays=data("overlays.tsv")
pickups=data("rom_pickups.tsv")
slots=data("stage_resource_slots.tsv")
assert len(resources)==len(overlays)==8
assert sorted(int(x["compact_selector"]) for x in resources)==list(range(8))
assert sorted(int(x["native_stage_id"]) for x in resources)==[0,1,2,3,4,5,8,9]
for row in resources:
    stage=row["stage"]
    assert len([x for x in overlays if x["stage"]==stage])==1
    assert sum(x["stage"]==stage for x in pickups)==int(row["ordinary_pickups"])
    assert sum(x["stage"]==stage for x in slots)==int(row["outer_slots"])
    assert int(row["resource_rom_end_exclusive"],16)-int(row["resource_rom_start"],16)==int(row["resource_size"],16)
    assert row["file_table_flag"]=="0" and len(row["source_blob_sha"])==40
    assert not row["runtime_base"] or row["runtime_base"]!="0x802ECE30"
earth=next(r for r in resources if r["stage"]=="Earth")
assert earth["resource_file_id"]=="0x30" and earth["runtime_publication_slot"]=="0x802E82B8" and not earth["runtime_base"]
prison=next(r for r in resources if r["stage"]=="Prison")
assert prison["resource_file_id"]=="0x49"
assert next(x for x in overlays if x["stage"]=="Prison")["file_id"]=="0x9F"
assert len(pickups)==84 and len(slots)==150
print("Eight resource-file maps validated against 84 pickups, 150 selector slots and distinct code overlays.")
