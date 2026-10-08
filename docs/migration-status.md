# Canonical research knowledge migration — 2026-10-07

**Source:** Current versioned `wiki/` in `smeagol44/MKMSZ-Randomizer` at migration time. This is not a second authoritative manual. Wiki owns semantics and evidence state.

## Imported, or recorded with correct coordinate provenance

- Global Function Registry: existing 67 + 57 initially cataloged names, corrected to **122 true function entries plus two internal switch-case labels** after maintainer Ghidra inspection; 125 scoped descriptions retained.
- Function names at stage-overlay addresses are never stored in the global function TSV.
- All **84** ordinary pickup records (4 Temple, 6 Wind, 9 Water, 20 Earth, 10 Prison, 16 Fire, 10 Bridge, 9 Fortress) in `rom_pickups.tsv`; addresses there are explicitly **ROM offsets**.
- Stage outer-slot catalogs in `stage_resource_slots.tsv` (150 entries); these are stage-relative selectors, not global identities.
- The guarded patch and proof registry in `rom_patch_sites.tsv` (151 location/evidence rows). Not blindly imported as disassembly edits.
- Verified raw overlay mappings: Earth 0x9C, Prison 0x9F, Bridge 0x9B, Fortress 0x9E. `overlays.tsv` records exact stock ROM spans, destination VA 0x802ECE30, and independently verified original bytes SHA-256.
- Nine stage-qualified named overlay functions in `overlay_functions.tsv`; other unresolved functions remain in `overlay_pending.tsv`.
- Nine total /MKMSZ analysis types: the existing item enum and four-box structure, plus seven additional evidence-backed structures.
- Existing verified bookmarks and relationships retained. New metadata should be checked against the current Wiki owner.

## Not yet fully represented by importable Ghidra objects

This migration is substantial but not exhaustive. Stage catalogs and guarded patch sites are searchable TSV provenance, not fully materialized Ghidra data objects. Many function signatures, custom calling conventions, locals, per-record cross-references and stage-specific code remain untyped or unresolved. The complete Memory Map, patch guards and every proof-history paragraph are not copied into Ghidra: the Wiki remains the owner of those facts.

Unknown overlay mappings (including other stages) are intentionally not guessed. PS1 program addresses remain separate, not part of the N64 global project. There are no new retroactively claimed runtime confirmations.

## User application order

1. Save or back up the existing Ghidra project.
2. `git pull` the analysis repository.
3. Run `ApplyMkmszAnalysis.java` in the clean N64 program, selecting the repo root.
4. Run `ApplyMkmszExtended.java` in that same program.
5. Save the analysis project.
6. **Optional separately staged overlay setup:** run `python tools/extract_overlays.py /path/to/clean.z64 /path/to/local/output` locally. Import each extracted binary into its own Ghidra program using **Raw Binary, MIPS big-endian 32-bit**, with a **loaded base at 0x802ECE30**, not the N64 cartridge loader. Check language variant/processor option in Ghidra, run analysis, then run the **extended script only** in each hash-verified overlay program. It applies names only to already recognized functions and leaves bookmarks when they are missing. The overlay programs are separate from the 16 MiB imported cartridge image.
7. Do not commit extracted overlay files, project databases, or copyrighted bytes.

**Local Ghidra importer validation — maintainer report, 2026-10-07:** On the supported clean-ROM program, `ApplyMkmszAnalysis.java` finished with **119 function entries, 14 globals**, and reported 5 missing Ghidra Function objects at `0x80003314`, `0x8000C6D8`, `0x80015088`, `0x8004B82C`, and `0x80066420`. `ApplyMkmszExtended.java` compiled and completed in the same installation with **scope=global, applied=132, skipped=2**. Given the exact manifest counts and the prior successful two-type import, this is consistent with 7 new structures + 125 new comments and 2 already-existing types. No unexpected errors were reported. Follow-up screenshot confirms **0x80003314 is an internal Type-5 switch-case arm (`switchD_80003278::caseD_5`), not a function entry**. The function record has been replaced by a scoped code label. The other four missing function entries require individual inspection; do not create them blindly. Separately, the initial manual Ghidra function at 0x80030974 was also shown to be a switch arm owned by animation interpreter 0x800304C0. The clean ROM confirms entry 0x800AD478 in the dispatch jump table points to 0x80030974. It was moved from functions.tsv to code_labels.tsv; a previously manually defined standalone function must be reviewed/removed locally before a nested internal label can apply. The separate raw-overlay workflow remains **unvalidated**. CI does not imply Ghidra-runtime API compatibility, but the global extended importer has now passed a maintainer-observed execution test. Note that imported raw-overlay program names must match `analysis/scopes.tsv` (excluding extensions where Ghidra drops them); if identity checks refuse a program, do **not** bypass them—inspect exact program name, source SHA and loader configuration.

## Future work

Populate grounded full signatures/locals and expanded data types during focused RE; map and import remaining stage overlays independently; add safe ROM-space navigation for patch sites and stage catalogs; consider a direct cross-referenced ROM offset view rather than conflating RAM and ROM.
