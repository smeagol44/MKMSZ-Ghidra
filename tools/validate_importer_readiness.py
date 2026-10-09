#!/usr/bin/env python3
"""ROM-free static preflight for draft PR importer safety and staged handoff.

This is source/manifest validation only, NOT a Ghidra launch, compiler or local import.
"""
import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
analysis=ROOT/"analysis"
script=(ROOT/"ghidra_scripts/ApplyMkmszAnalysis.java").read_text(encoding="utf-8")
extended=(ROOT/"ghidra_scripts/ApplyMkmszExtended.java").read_text(encoding="utf-8")
def table(name):
    with (analysis/name).open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f,delimiter="\t"))
scopes=table("scopes.tsv")
assert len([r for r in scopes if r["scope"]=="global"])==1
clean=next(r["sha256"] for r in scopes if r["scope"]=="global")
assert clean=="9c18254abf6722b95aa782fcd310bd95f6bcf147da66beb77ce32ca90673ffc6"
assert clean in script and clean in extended
assert "sha == null || !sha.equalsIgnoreCase(EXPECTED_SHA256)" in script
assert "function.getSymbol().getSource() == SourceType.USER_DEFINED" in script
assert 'prior.getSource() == SourceType.USER_DEFINED' in script
assert "getPrimarySymbol(address)" in script
assert "previous != null && !previous.startsWith(\"[MKMSZ]\")" in script
assert "applyManagedPlateComment(address, evidence, comment);" in script
# Confirm both paths are checked and that the extended importer does not flatten stage VAs.
assert 'scope = identifyScope();' in extended and 'if (scope == null)' in extended
assert 'if (!scope.equals("global")) applyOverlayFunctions();' in extended
assert 'if (existing != null && !Undefined.isUndefined(existing.getDataType()))' in extended
assert 'if (!existing.isEquivalent(entry.getValue()))' in extended
assert 'if (previous != null && !previous.startsWith("[MKMSZ]"))' in extended
assert len(table("functions.tsv"))==139 and len(table("globals.tsv"))==35
assert len(table("overlay_functions.tsv"))==14 and len(table("rom_pickups.tsv"))==84
bookmark=[r for r in table("bookmarks.tsv") if r["scope"]=="global" and r["category"]=="known-stock-navigation"]
assert len(bookmark)==7 and {r["address"] for r in bookmark}=={
    "0x800B1BAC","0x800B1BD0","0x800B1D18","0x800B1D38",
    "0x802E82B8","0x80038BE4","0x80038BFC"}
types=table("types.tsv")
new=[r for r in types if r["name"]=="MKMSZ_SpecialActionDescriptor"]
assert len(new)==8 and len([r for r in new if r["kind"]=="struct" and r["size"]=="0x2C"])==1
assert len([r for r in types if r["kind"] in ("struct","enum") and r["name"]!="MKMSZ_SpecialActionDescriptor"])==11
typed=table("data.tsv")
assert len(typed)==1 and typed[0]["scope"]=="global"
assert typed[0]["address"]=="0x800B0F68" and typed[0]["datatype"]=="MKMSZ_SpecialActionDescriptor"
assert "0x800B0F94" in typed[0]["note"] and "0x800B0F98" in typed[0]["note"]
assert not table("signatures.tsv") and not table("locals.tsv")
print("PASS: original importer fail-closed identity and local comment/name conflict policy (static source check)")
print("PASS: extended scoped importer conflict policy and ROM-free manifest handoff (static source check)")
print("PASS: 139 global functions, 35 globals, 14 overlay functions, 84 pickups; 7 staged bookmarks")
print("PASS: 11 locally established types separated from 1 staged 0x2C descriptor + 1 data instance")
print("PENDING: Ghidra compilation, actual import, data type application, and preservation in maintainer project")
