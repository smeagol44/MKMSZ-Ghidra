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
# Managed /MKMSZ types are converged on repeated runs rather than being
# mistakenly classified as locally edited simply because they already exist.
assert "if (existing.isEquivalent(incoming)) {" in extended
assert 'println("TYPE UP TO DATE: " + entry.getKey());' in extended
assert "manager.replaceDataType(existing, incoming, true)" in extended
assert "manager.getDataType(expectedPath)" in extended
assert "existing.getLength() != incoming.getLength()" in extended
assert "TYPE CONFLICT:" in extended and "TYPE SYNC FAILED:" in extended
assert 'DataTypePath expectedPath = new DataTypePath(CATEGORY, entry.getKey());' in extended
assert 'if (previous != null && !previous.startsWith("[MKMSZ]"))' in extended
assert len(table("functions.tsv"))==145 and len(table("globals.tsv"))==37
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
# Regression: a Ghidra-generated dynamic symbol must not suppress an explicit
# data.tsv label; existing equivalent typed data must still be reconciled.
assert "applyCuratedDataLabel(at, r[3]);" in extended
assert "getPrimarySymbol(at)" in extended
assert "wantedName.equals(primary.getName())" in extended
assert "primary.getSource() == SourceType.USER_DEFINED" in extended
assert "createLabel(at, wantedName, true, SourceType.USER_DEFINED)" in extended
assert "DATA LABEL UNRESOLVED" in extended
assert 'getSymbolAt(at) == null' not in extended
assert 'if (!existing.getDataType().isEquivalent(wanted)) {' in extended
audit=(ROOT/"ghidra_scripts/AuditMkmszImportedState.java").read_text(encoding="utf-8")
for expected in ('auditFunctions()', 'auditGlobals()', 'auditCodeLabels()',
                 'auditTypes()', 'auditTypedData()', 'auditComments()', 'auditBookmarks()',
                 'expected " + r[3] + ", found " + primary(addr)', 'MISMATCH',
                 'CLEAN_SHA.equalsIgnoreCase(currentProgram.getExecutableSHA256())'):
    assert expected in audit
assert "createLabel(" not in audit and "createData(" not in audit and "setBookmark(" not in audit
# Regression: all manifest-owned MKMSZ/Info bookmark notes refresh on repeat
# imports. Locally added categories elsewhere in the program are never touched.
assert 'old.set(category, content);' in extended
assert 'println("BOOKMARK REFRESHED at " + at + " category " + category);' in extended
assert 'SKIP bookmark " + at + " category " + category' not in extended
# A field-description-only change must be visible to type audits; a former
# 12/12 size/name/field match was insufficient to certify annotation fidelity.
typeAudit=(ROOT/"ghidra_scripts/AuditMkmszTypes.java").read_text(encoding="utf-8")
assert "String fieldName = value[0], datatype = value[1], fieldNote = value[2];" in typeAudit
assert "component.getComment()" in typeAudit
assert "new String[] {row[4], row[6], row[9]}" in typeAudit
print("PASS: original importer fail-closed identity and local comment/name conflict policy (static source check)")
print("PASS: extended scoped importer conflict policy and ROM-free manifest handoff (static source check)")
print("PASS: 145 global functions, 37 globals, 14 overlay functions, 84 pickups; 7 staged bookmarks")
print("PASS: 11 locally established types separated from 1 staged 0x2C descriptor + 1 data instance")
print("PASS: automatic curated type/data-label/bookmark convergence and deep type-notes audit statically guarded")
print("PENDING: Ghidra compilation, actual import, data type application, and preservation in maintainer project")
