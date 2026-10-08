# Canonical research knowledge migration — 2026-10-07

**2026-10-08 upstream Inventory/audio additions: Static-confirmed; local Ghidra import Pending.** Added 17 native scheduler/audio functions, 21 globals, focused ownership/comments and six relations from exact clean-ROM disassembly plus paired diagnostic state decoding. The maintainer-confirmed earlier 122/122 import does not cover these additions. No causal Inventory-operation name, ROM/RAM/PCM payload, backend hypothesis or guest diagnostic overlay is imported. Re-run the guarded name/extended importers after pulling and preserve local conflicts. Canonical evidence: [upstream investigation](https://github.com/smeagol44/MKMSZ-Randomizer/blob/main/wiki/Production-Rich-Inventory-Music-Static-Investigation.md).

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

**Local Ghidra importer validation — maintainer report, 2026-10-07:** On the supported clean-ROM program, `ApplyMkmszAnalysis.java` finished with **119 function entries, 14 globals**, and reported 5 missing Ghidra Function objects at `0x80003314`, `0x8000C6D8`, `0x80015088`, `0x8004B82C`, and `0x80066420`. `ApplyMkmszExtended.java` compiled and completed in the same installation with **scope=global, applied=132, skipped=2**. Given the exact manifest counts and the prior successful two-type import, this is consistent with 7 new structures + 125 new comments and 2 already-existing types. No unexpected errors were reported. Follow-up screenshot confirms **0x80003314 is an internal Type-5 switch-case arm (`switchD_80003278::caseD_5`), not a function entry**. The function record has been replaced by a scoped code label. The four other initially missing function entries were then inspected individually (historical state; see global function import closure below). Separately, the initial manual Ghidra function at 0x80030974 was also shown to be a switch arm owned by animation interpreter 0x800304C0. The clean ROM confirms entry 0x800AD478 in the dispatch jump table points to 0x80030974. It was moved from functions.tsv to code_labels.tsv; a previously manually defined standalone function must be reviewed/removed locally before a nested internal label can apply. The separately staged **Prison overlay pickup importer has now passed its first maintainer-observed Ghidra execution** (10/10 records typed; 0 conflicts, 0 pre-existing records); full overlay function import and the other three stage pickup imports remain unvalidated. CI does not imply Ghidra-runtime API compatibility, but the global extended importer has now passed a maintainer-observed execution test. Prison raw-overlay pickup data creation was subsequently confirmed in the staged draft PR #1; check `docs/overlay-pickup-import.md` for the exact 10/10 output. Note that imported raw-overlay program names must match `analysis/scopes.tsv` (excluding extensions where Ghidra drops them); if identity checks refuse a program, do **not** bypass them—inspect exact program name, source SHA and loader configuration.

## Global function import closure — maintainer Ghidra confirmation, 2026-10-08

**Implementation/Ghidra-confirmed:** The maintainer's final Script Manager console reports `MKMSZ analysis applied: 122 function entries, 14 global entries` with no missing-function messages. All entries in the **current global function manifest** are now represented in the local Ghidra project; this does **not** establish complete game-wide function coverage or validate every function boundary.

The former misses were resolved as follows: `0x80003314` and `0x80030974` are internal switch-case arms, not functions; `0x8000C6D8`, `0x80015088`, `0x8004B82C`, and `0x80066420` were separately disassembled/created as functions and the rename importer subsequently succeeded. The screenshot for the last function shows `arena_remaining_capacity` at `0x80066420` with instruction sequence `lui/lw/lui/addiu/subu/jr/sra`; the delay-slot `sra` divides the remaining byte count by eight. The global importer and local Ghidra recognition are confirmed; extracted-stage-overlay imports remain Pending.

## Prison stage-function importer — maintainer confirmation, 2026-10-08

**Ghidra/implementation-confirmed bounded:** With separately imported Prison raw overlay `0x9F`, the maintainer manually verified/disassembled and created the `0x802F1E44` MIPS32 function. The decompiler shows trigger-table iteration and callback dispatch plus `process_sleep(2)` in the repeating process. After pulling the overlay-qualified metadata, `ApplyMkmszExtended.java` reported `scope=overlay_prison`, `applied 3, skipped 2`, and renamed that function to `prison_trigger_dispatch`, while creating bookmarks for `0x802EE320` (`prison_scene_actor_update`) and `0x802F0754` (`prison_capture_grunt_present`). Screenshot confirms the renamed decompiler function and retained body. Those two bookmarks were subsequently resolved: the maintainer manually disassembled and created `0x802EE320` and `0x802F0754` as MIPS32 functions, provided their decompilations, and the canonical Function Registry and stage-qualified metadata were reconciled against them. `0x802EE320` was subsequently imported as `prison_scene_actor_update` (screenshot confirmed name/comment). The final `ApplyMkmszExtended.java` run reports `scope=overlay_prison`, **`applied 1, skipped 0`**, consistent with importing `prison_capture_grunt_present` at `0x802F0754`. Thus **all 3 of the currently cataloged Prison overlay function entries are Ghidra/implementation-confirmed imported**. This does not imply exhaustive Prison function discovery, fully verified function endings, or additional emulator runtime coverage. Next: Earth stage functions in its separate verified overlay program.

## Guarded bulk overlay function importer — maintainer Prison baseline, 2026-10-08

The new `ApplyMkmszOverlayFunctions.java` script successfully ran in the previously analyzed Prison `0x9F` program. It matched all 3 cataloged entries and reported `created=0, renamed=0, unchanged=3, disassembled=0, review=0`. This establishes **Ghidra/implementation-confirmed** idempotent handling of the three existing Prison functions and stage identity/entry-guard acceptance. Fresh MIPS32 decoding, automatic creation, and overlay-specific function boundaries in Earth/Bridge/Fortress remain **Pending** until their first maintainer Ghidra runs. The nine entry prefixes have stock-ROM static evidence; CI checks alone do not validate Ghidra's creation path. Refer to `docs/overlay-function-bulk-import.md` for the bounded procedure and exact console record.

## Bulk overlay function creation — Earth maintainer confirmation, 2026-10-08

The same guarded bulk importer ran on the separately imported Earth `0x9C` program, reporting **`created=2, renamed=2, unchanged=0, disassembled=2, review=0`** for `earth_key_award` at `0x802F52B0` and `earth_boss_construct` at `0x802EDF50`. This moves automatic MIPS32 entry disassembly and function creation from Pending to **Ghidra/implementation-confirmed bounded for Earth**. Together with the Prison idempotent test, **5/9** cataloged overlay function entries are now imported in two separate stage programs. Bridge and Fortress (2 entries each) remain Pending. Full function boundaries/semantics outside the verified evidence are not claimed.

## Bulk overlay function creation — Bridge maintainer confirmation, 2026-10-08

The bulk importer on the separately imported Bridge `0x9B` program returned **`created=2, renamed=2, unchanged=0, disassembled=2, review=0`**, for `bridge_icon_award` (`0x802EF178`) and `bridge_scene_trigger_dispatch` (`0x802ED888`). **Ghidra/implementation-confirmed bounded** for these two entries and automated MIPS32 function creation. Overall status is now **7/9** in Prison, Earth and Bridge; Fortress (two functions) still Pending. The function bodies have not been exhaustively audited.

## Future work

Populate grounded full signatures/locals and expanded data types during focused RE; map and import remaining stage overlays independently; add safe ROM-space navigation for patch sites and stage catalogs; consider a direct cross-referenced ROM offset view rather than conflating RAM and ROM.

**Additional maintainer Ghidra inspection:** `0x8000C6D8` and `0x80015088` were manually disassembled and made into separate functions. At `0x80015088`, the decompiler confirms one shared dispatcher for Pause (process state `2`) and stage reconstruction (`0x18`); `analysis/functions.tsv` now uses `pause_stage_event_dispatch`, correcting the overly narrow `stage_transition_handler`. Exact full boundaries remain to be exhaustively checked; `0x8004B82C` and `0x80066420` were subsequently inspected and correctly imported; see the closure above.
