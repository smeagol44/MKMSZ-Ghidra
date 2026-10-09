#!/usr/bin/env python3
"""Read-only, conservative patch-site vs Memory Map navigation audit.

No match does NOT mean free: the canonical Memory Map is not a ROM partition.
"""
import argparse
import csv
import re
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "analysis"
HEX = re.compile(r"^0x[0-9A-Fa-f]+$")
ROM = re.compile(r"\bROM\s+\x60?(0x[0-9A-Fa-f]+)\x60?")

def read(name):
    with (BASE / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, help="Optional audit CSV output path")
    args = parser.parse_args()
    intervals = []
    for row in read("memory_ownership_intervals.tsv"):
        if row["space"] != "rom":
            continue
        for pair in row["segments"].split(";"):
            start, end = pair.split(":")
            intervals.append((int(start,16), int(end,16),
                              row["region_id"], row["classification"]))
    output, stats = [], Counter()
    patches = read("rom_patch_sites.tsv")
    assert len(patches) == 151
    for row in patches:
        raw = row["rom_or_location"].strip()
        matches = ROM.findall(raw)
        if HEX.fullmatch(raw):
            offset, kind = int(raw,16), "literal-rom-offset"
        elif len(matches) == 1 and ".." not in raw:
            offset, kind = int(matches[0],16), "explicit-rom-offset"
        else:
            offset, kind = None, "ambiguous-or-other-coordinate"
        owners = ([f"{region} ({klass})" for lo,hi,region,klass in intervals
                   if lo <= offset < hi] if offset is not None else [])
        if offset is not None:
            stats["point_offsets"] += 1
            stats["matched_points"] += bool(owners)
            stats["unmapped_points"] += not bool(owners)
            stats["overlapping_points"] += len(owners) > 1
        else:
            stats["withheld"] += 1
        output.append({
            "record_id": row["record_id"],
            "source_section": row["section"],
            "source_location": raw,
            "parse_kind": kind,
            "rom_offset": f"0x{offset:08X}" if offset is not None else "",
            "bounded_map_matches": "; ".join(owners),
            "disposition": ("coordinate-needs-review" if offset is None else
                            "bounded-map-present" if owners else
                            "not-in-bounded-map-NOT-FREE"),
        })
    assert len(output) == 151
    print("151 patch/proof records evaluated.")
    print(f"{stats['point_offsets']} conservatively parsed point offsets, "
          f"{stats['withheld']} range/multi/non-ROM expressions withheld.")
    print(f"{stats['matched_points']} bounded-map matches, "
          f"{stats['unmapped_points']} without a bounded-map match, "
          f"{stats['overlapping_points']} overlapping entries.")
    print("NO MATCH DOES NOT MEAN FREE SPACE.")
    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(output[0]))
            writer.writeheader()
            writer.writerows(output)
        print(f"Wrote {args.csv}")

if __name__ == "__main__":
    main()
