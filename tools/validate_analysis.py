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
}
HEX = re.compile(r"^0[xX][0-9a-fA-F]+$")
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
            if not SCOPE.fullmatch(row[0]):
                errors.append(f"{path}:{n}: invalid scope")
            for idx in {
                "signatures.tsv": (1,), "locals.tsv": (1, 4),
                "data.tsv": (1,), "comments.tsv": (1,),
                "bookmarks.tsv": (1,), "relations.tsv": (1, 2)
            }.get(path, ()):
                if not HEX.fullmatch(row[idx]):
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
    if file in ("scopes.tsv", "functions.tsv", "globals.tsv"):
        continue
    for n, r in enumerate(rows, 2):
        if r and not r[0].startswith("#") and r[0] not in scopes:
            errors.append(f"{file}:{n}: unknown scope {r[0]}")
if errors:
    print("\n".join("ERROR " + x for x in errors))
    sys.exit(1)
print("OK: headers, row widths, address formats, scope identities")
