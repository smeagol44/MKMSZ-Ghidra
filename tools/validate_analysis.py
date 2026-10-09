#!/usr/bin/env python3
"""Validate ROM-free MKMSZ analysis TSV format and scope consistency."""
from pathlib import Path
import csv
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "analysis"
HEADERS = {
    "scopes.tsv": "scope program_name sha256",
    "functions.tsv": "address name evidence comment",
    "globals.tsv": "address name evidence comment",
    "types.tsv": "scope kind name size field offset datatype value evidence note",
    "signatures.tsv": "scope address return_type parameters evidence note",
    "locals.tsv": "scope function_address name datatype stack_offset evidence note",
    "data.tsv": "scope address datatype label evidence note",
    "comments.tsv": "scope address kind evidence text",
    "bookmarks.tsv": "scope address category evidence note",
    "relations.tsv": "scope from to kind operand evidence note",
    "overlays.tsv": "scope stage file_id rom_start rom_end_exclusive runtime_base sha256 evidence",
    "overlay_functions.tsv": "scope address name evidence comment",
    "overlay_function_guards.tsv": "scope address first16_be_hex evidence",
    "global_function_guards.tsv": "address name first16_be_hex preceding8_be_hex registration_address registration8_be_hex evidence",
    "code_labels.tsv": "scope address name evidence comment",
    "overlay_pending.tsv": "stage address description evidence note source status",
    "rom_patch_sites.tsv": "record_id section rom_or_location va owner_or_purpose guard_or_existing change_or_note source",
    "rom_pickups.tsv": "stage native_stage_id ordinal identity rom_base rdram_base type parameter callback resource_slot presentation collected token requires source",
    "stage_resource_slots.tsv": "stage slot name outer_offset format frames pickup_users source",
}
HEX = re.compile(r"^0[xX][0-9a-fA-F]+$")
ENTRY_BYTES = re.compile(r"^[0-9a-fA-F]{32}$")
SIGNED_HEX = re.compile(r"^-?0[xX][0-9a-fA-F]+$")
SHA = re.compile(r"^[0-9a-fA-F]{64}$")
SCOPE = re.compile(r"^[a-z][a-z0-9_-]*$")
errors = []
tables = {}
for path, fields in HEADERS.items():
    file = BASE / path
    if not file.is_file():
        errors.append(f"missing {path}")
        continue
    with file.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle, delimiter="\t"))
    if not rows or rows[0] != fields.split():
        errors.append(f"{path}: header mismatch")
        continue
    tables[path] = rows[1:]
    for n, row in enumerate(rows[1:], 2):
        if not row or (len(row) == 1 and row[0].startswith("#")):
            continue
        if len(row) != len(fields.split()):
            errors.append(f"{path}:{n}: expected {len(fields.split())} columns")
            continue
        if path == "scopes.tsv":
            if not SCOPE.fullmatch(row[0]) or not SHA.fullmatch(row[2]):
                errors.append(f"{path}:{n}: invalid scope or hash")
        elif path in ("functions.tsv", "globals.tsv"):
            if not HEX.fullmatch(row[0]):
                errors.append(f"{path}:{n}: invalid address")
        else:
            if path not in ("overlay_pending.tsv", "rom_patch_sites.tsv", "rom_pickups.tsv", "stage_resource_slots.tsv") and not SCOPE.fullmatch(row[0]):
                errors.append(f"{path}:{n}: invalid scope")
            for idx in {
                "signatures.tsv": (1,), "locals.tsv": (1, 4),
                "data.tsv": (1,), "comments.tsv": (1,), "overlay_functions.tsv": (1,), "code_labels.tsv": (1,),
                "bookmarks.tsv": (1,), "relations.tsv": (1, 2)
            }.get(path, ()):
                if not (SIGNED_HEX if path == "locals.tsv" and idx == 4 else HEX).fullmatch(row[idx]):
                    errors.append(f"{path}:{n}: invalid address in column {idx}")
            if path == "types.tsv" and row[1] not in ("struct", "field", "enum", "member"):
                errors.append(f"{path}:{n}: invalid type kind")
            if path == "relations.tsv" and row[3] not in ("NOTE", "DATA_REF", "CALL_REF"):
                errors.append(f"{path}:{n}: invalid relation kind")
scopes = {r[0] for r in tables.get("scopes.tsv", []) if len(r) == 3}
expected = "9c18254abf6722b95aa782fcd310bd95f6bcf147da66beb77ce32ca90673ffc6"
if not any(len(r)==3 and r[0] == "global" and r[2].lower() == expected for r in tables.get("scopes.tsv", [])):
    errors.append("global scope must be pinned to clean USA Rev.0 SHA")
for file, rows in tables.items():
    if file in ("scopes.tsv", "functions.tsv", "globals.tsv", "overlay_pending.tsv", "rom_patch_sites.tsv", "rom_pickups.tsv", "stage_resource_slots.tsv"):
        continue
    for n, r in enumerate(rows, 2):
        if r and not r[0].startswith("#") and r[0] not in scopes:
            errors.append(f"{file}:{n}: unknown scope {r[0]}")
# Global function creation is limited to exact source and contextual-byte guards.
for row in tables.get("global_function_guards.tsv", []):
    if len(row) != 7:
        continue
    if not HEX.fullmatch(row[0]) or not HEX.fullmatch(row[4]) or (
        not ENTRY_BYTES.fullmatch(row[2]) or
        not re.fullmatch(r"[0-9a-fA-F]{16}", row[3]) or
        not re.fullmatch(r"[0-9a-fA-F]{16}", row[5])
    ):
        errors.append(f"invalid global function entry/context guard: {row[:2]}")
    elif (row[0], row[1]) not in {(r[0], r[1]) for r in tables.get("functions.tsv", []) if len(r) == 4}:
        errors.append(f"global function guard lacks function manifest identity: {row[:2]}")

# Every candidate function requires one scoped, exact stock 16-byte signature.
function_keys = {(row[0], row[1]) for row in tables.get("overlay_functions.tsv", [])
                 if len(row) == 5}
guards = tables.get("overlay_function_guards.tsv", [])
guard_keys = set()
for row in guards:
    if len(row) != 4: continue
    key = (row[0], row[1])
    if key in guard_keys:
        errors.append(f"duplicate overlay function guard: {key}")
    guard_keys.add(key)
    if not HEX.fullmatch(row[1]) or not ENTRY_BYTES.fullmatch(row[2]):
        errors.append(f"invalid overlay function guard: {key}")
    if key not in function_keys:
        errors.append(f"guard for unknown overlay function: {key}")
    overlay = next((x for x in tables.get("overlays.tsv", []) if x[0] == row[0]), None)
    if overlay is None:
        errors.append(f"guard has no mapped overlay: {key}")
    else:
        base = int(overlay[5], 16)
        end = base + int(overlay[4], 16) - int(overlay[3], 16)
        addr = int(row[1], 16)
        if not (base <= addr and addr + 16 <= end and addr % 4 == 0):
            errors.append(f"guard outside mapped overlay: {key}")
for key in sorted(function_keys - guard_keys):
    errors.append(f"missing overlay function entry guard: {key}")

if errors:
    print("\n".join("ERROR " + x for x in errors))
    sys.exit(1)
print("OK: headers, row widths, address formats, scope identities")

# Exactly 84 researched ordinary records; prevent silent catalog truncation.
if len(tables.get("rom_pickups.tsv", [])) != 84:
    errors.append("expected 84 ordinary pickup records")
# Overlay source scopes must have manifest provenance.
for row in tables.get("overlays.tsv", []):
    if len(row) == 8 and (not SHA.fullmatch(row[6]) or row[0] not in scopes):
        errors.append("invalid overlay hash/scope")
if errors:
    print("\\n".join("ERROR " + x for x in errors))
    sys.exit(1)
