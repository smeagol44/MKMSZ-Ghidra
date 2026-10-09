# Wiki-to-Ghidra RE coverage audit — first bounded pass (2026-10-08)

## Purpose

Make established reverse engineering visible where investigators work, and make the **remaining gaps** explicit, while retaining the canonical Wiki as the authority for scope, evidence and outcomes. This is not a bulk paste of product or experiment prose into Ghidra.

## Current inventory of shared metadata

| Record | Current count / state | What that means |
|---|---|---|
| `analysis/functions.tsv` | 139 function entries | Includes 17 scheduler/audio additions beyond the maintainer-confirmed earlier 122 imports; **newest entries are NOT yet confirmed applied locally** |
| `analysis/globals.tsv` | 35 labels | Earlier 14 confirmed; newer 21 audio/scheduler globals still need local reapplication |
| `analysis/overlay_functions.tsv` | 14 entries | **Ghidra/implementation-confirmed** applied in eight separate stage programs |
| `analysis/rom_pickups.tsv` | 84 entries | **Ghidra/implementation-confirmed** typed in eight separate stage programs |
| `analysis/stage_resource_slots.tsv` | 150 rows | Catalogued metadata, **not** 150 Ghidra typed data objects |
| `analysis/rom_patch_sites.tsv` | 151 rows | ROM provenance, **not** implicitly disassembled runtime VAs |
| `analysis/types.tsv` | 100 rows (types and members) | Shared type definitions; the latest added schemas not exhaustively visually verified in Ghidra |
| `analysis/signatures.tsv`, `locals.tsv`, `data.tsv` | 0 rows each | **Explicit RE representation gaps**; no inferred signatures, stack locals or data declarations may be fabricated |
| `analysis/code_labels.tsv` | 2 internal switch-arm labels | Never turn these into distinct functions |
| `analysis/relations.tsv` | 10 notes | Limited traced relationships, not a complete call graph |

## Function Registry reconciliation: first pass

Reviewed the **Global N64 functions** section of the current canonical `wiki/Function-Registry.md` against names, global addresses, preexisting code labels, bookmarks and scoped comments in the shared Ghidra manifests. Found **38 global address occurrences** with documented traces but no first-class imported annotation from those manifests. These are **not proven to be independent function entries**.

Added 38 lightweight, evidence-qualified `repeatable` comments and 38 scoped `Info` bookmarks, each referencing its short original Wiki function-role description. These can be viewed/searchable in Ghidra after running `ApplyMkmszExtended.java` in the global clean-ROM program. The importer preserves non-MKMSZ local comments and differing bookmarks. We deliberately **did not disassemble, create functions, overwrite Ghidra-generated references, or rename uncertain functions**.

Key cases now navigable: ordinary pickup ABI `0x800393BC/0x800393D0`; enemy construction/reset `0x80070710`; projectile resource paths `0x80046F74/0x80047160`; player/pause/inventory gates `0x80028EAC/0x80016300/0x80014FC0`; ordinary Water reaction root select `0x800321D0/0x80032580`; stage icon *use* handlers `0x800720F0..0x80072464`. Five of these new addresses belong to rows whose evidence includes unresolved reaction/root semantics. Those entries are tagged `trace-open`; the rest are `trace-known`. The full boundary/identity of all 38 entries remains **Pending verification** (some may be internal code), and the imported comments are intentionally not an assertion otherwise.

### Why a registry row may still be represented only partly

A Wiki row may describe an entire family with multiple addresses; one known function or address does not establish all related entry points. A patch seam can be inside an existing function; a known callback can be a switch arm rather than an independent function; and a ROM coordinate is not automatically a mapped VA in a raw-overlay program. **Visibility** (mark/bookmark) and **proven function boundary** (create/rename) are separate states.

## Unresolved local application: audio and scheduler functions

The existing migration status identifies **17 additional native scheduler/audio functions and 21 globals** derived from the latest production rich Inventory music root-cause investigation. They are recorded in the manifest and Wiki, but the maintainer's earlier **122/122 global function** import pre-dates these additions. It would be misleading to say the current local Ghidra database already has all 139 named objects.

After pulling this branch, save/back up the Ghidra project and run, in the **global supported clean-ROM program only**, `ApplyMkmszAnalysis.java` then `ApplyMkmszExtended.java`. Capture and report **every** `No function at ...; skipped`, conflict/skipped counter, and the final applied counts. Do **not** force missing entries or rerun the Ghidra stage overlay importers. If new audio functions are missing in Ghidra, resolve exact boundaries/ISA in a separate guarded follow-up, ideally via bulk script rather than one-by-one manual creation.

## Gaps and priorities after this first pass

1. **Get the global metadata into your current Ghidra project**, including the 17 audio/scheduler names, 21 globals, and these 38 trace markers. Verify actual importer results.
2. **Reconcile the remaining canonical domain owners** (Memory/Allocation Map, Native HUD/UI, Persistence/Inventory/Lifecycle, Stage-Flow, Data Structures, enemy/player systems, audio), extracting only supported code/structure-level facts. Use named bookmarks and scoped managed comments with negative controls and open questions, not wholesale prose copy.
3. **Identify missing existing function boundaries** for the now-visible global trace markers by examining instruction callers and confirmed program flow. Only stage precise, byte-guarded function creation for high-confidence entries.
4. **Fill signature/local/data manifests conservatively** as evidence supports them; all three are currently empty. Do not synthesize stack locals, native calling convention, or global data solely from prose.
5. **Improve deterministic per-page coverage:** a future audit can include Wiki owner / address / scope / evidence / representation / confirmed-import columns and compare manifest deltas, while preserving open questions. Existing CI currently validates TSV formatting/scope rather than Wiki semantic parity.

### Evidence and non-goals

**Implementation/CI-confirmed:** 38 new manifest comments and 38 bookmarks once CI passes. **Ghidra/implementation-confirmed bounded** for the combined extended import execution; a full manual per-entry visual audit is not claimed. **Static-confirmed:** existing Wiki-researched meanings on their bounded routes only. **Ghidra/implementation-confirmed** for the previously applied eight-stage cataloged pickup/known function imports only. Unknown function bodies remain unknown; no ROM modifications or emulator testing were performed.

Current Wiki provenance: `Function-Registry.md`, `Production-Rich-Inventory-Music-Static-Investigation.md`, `Native-HUD-and-UI.md`, `Persistence-Inventory-and-Lifecycle.md`, `Memory-and-Allocation-Map.md`, `Data-Structures-and-Encodings.md`.

## Maintainer global importer run — 2026-10-08

The maintainer ran both importers on the existing clean N64 global program:

```text
ApplyMkmszAnalysis.java> Running...
No function at 80015950; skipped vi_input_callback
MKMSZ analysis applied: 138 function entries, 35 global entries.
ApplyMkmszAnalysis.java> Finished!
ApplyMkmszExtended.java> Running...
MKMSZ extended analysis scope: global
MKMSZ extended analysis: applied 106, skipped 10 (scope=global)
ApplyMkmszExtended.java> Finished!
```

**Ghidra/implementation-confirmed bounded:** All 35 global names were accepted; 138/139 function names applied. The 38 new trace markers are included in the extended manifest, but the aggregate extended counters alone cannot prove every new annotation is present or explain all 10 skips. Prior existing types or locally-owned annotations may explain skips; do **not** classify them as confirmed harmless without diagnostics.

### Precise VI callback gap closure prepared (Ghidra execution Pending)

The clean supported ROM has at VA `0x80015950` / ROM `0x16550` the first 16 original bytes `3c02802f9442cd443c03802f8463ce2c`. At `0x80015948` immediately preceding, `03e00008 00000000` is the previous function's `jr ra` plus delay slot. At `0x800147AC`, `lui a0,0x8001; addiu a0,a0,0x5950` loads `0x80015950` before a stock registration call at `0x800147B4`. The target body also contains the documented store to `0x802E7DC0` at `0x80015998`. These are **Static-confirmed** ROM-local facts and distinguish the entry from an internal switch arm.

`analysis/global_function_guards.tsv` records those exact three context checks, and `ApplyMkmszGuardedGlobalFunctions.java` performs a **single-entry** MIPS32 disassembly and function creation, bounded to `0x80015B80`. It refuses unsupported source hashes, wrong processor/endian, byte mismatches, typed entry data, MIPS16 entry, or overlap with an existing function. It preserves local custom names and other analysis. The script has not yet been run in the maintainer's Ghidra: **Ghidra/implementation Pending**.

**Local order after pulling the feature branch:** save/back up current clean-ROM Ghidra program; run `ApplyMkmszGuardedGlobalFunctions.java`, then `ApplyMkmszAnalysis.java` to verify **139/139 function entries, 35/35 globals**. Rerun `ApplyMkmszExtended.java`: enhanced console messages now attribute locally existing-type, comment, and bookmark skips so they can be distinguished from genuine failures. Capture full console output rather than interpreting `skipped=10` by itself. Do not manually disassemble the missing function or reimport the eight stage overlays.

## Maintainer global gap closure — 2026-10-08

The maintainer reran all three guarded/global scripts on the same clean N64 program after the diagnostic change:

```text
ApplyMkmszGuardedGlobalFunctions.java> Running...
OK vi_input_callback at 80015950
Guarded global function import: created=1, already=0, review=0
ApplyMkmszGuardedGlobalFunctions.java> Finished!
ApplyMkmszAnalysis.java> Running...
MKMSZ analysis applied: 139 function entries, 35 global entries.
ApplyMkmszAnalysis.java> Finished!
ApplyMkmszExtended.java> Running...
MKMSZ extended analysis scope: global
TYPE ALREADY PRESENT: MKMSZ_ItemId (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_BoxBacking (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_PickupRecord (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_PersistenceV2 (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_EnemySpawnRecord (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_AuxTriggerRecord (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_RenderNode (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_DynamicTextureSlot (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_Type5ImageHeader (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_EnemySpawnConditionalRecord (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_Type5ModelTableHeader (existing definition preserved)
SKIP bookmark 80030974 category MKMSZ/animation: preserving locally owned note
MKMSZ extended analysis: applied 0, skipped 12 (scope=global)
ApplyMkmszExtended.java> Finished!
```

**Ghidra/implementation-confirmed bounded:** the source/context-guarded script created the previously missing native VI callback without reported conflicts; global names are now **139/139**, globals **35/35**. The extended script ran and every one of its **12 skips is identified**: 11 previously present named types and one pre-existing locally owned animation bookmark at `0x80030974`. Preserve that bookmark (the address is an internal switch arm, not a standalone function). The importer preserves existing type definitions, but the log does **not** prove the 11 existing type definitions are structurally equivalent to their current manifests; a separate type-equivalence audit would be required for that stronger conclusion. The prior initial extended run had `applied=106`; its follow-up `applied=0` is consistent with all unchanged applicable scoped metadata already being present, not with 106 new operations on each execution. No emulator was used.

**Remaining audit work:** other canonical Wiki domain owners (memory/allocation, Inventory/HUD/lifecycle, native audio, enemies and resource mechanics) still contain useful code-level cross-references not exhaustively reconciled; global function-body completeness, signature/local/data manifests and stable per-finding status/navigation also remain incomplete.

## Domain-owner reconciliation — second bounded pass (2026-10-08)

Compared current Wiki `Native-HUD-and-UI.md`, `Persistence-Inventory-and-Lifecycle.md`, `Production-Rich-Inventory-Music-Static-Investigation.md`, `Memory-and-Allocation-Map.md`, `Stage-Flow-and-Selector.md`, and `Data-Structures-and-Encodings.md` against existing Ghidra metadata.

Added **17 conservative stock-program trace points** to both `analysis/comments.tsv` and `analysis/bookmarks.tsv` (34 records): scheduler setup and SP/DP/VI/pre-NMI event registrations (5); inventory capture/HP/SEALED/live-store routes (5); death/Continue/frontend life ownership, player startup, Fire normal overlay load, and Stage-7 entry (6); and the already rejected caller-saved-register hazard at native draw `0x8001CA88` (1). Three of the 17 are explicit warnings and one records an unresolved Stage-7 question. These are comments/bookmarks only; no code was created, bytes patched or function boundaries inferred.

**Important scope separation:** The Inventory/HUD and Memory Map also describe production-only wrappers at addresses such as `0x800AEE24` and allocator/ROM boundaries. They are not stock program code merely because the address falls into a mapped ROM image. Do not apply those entries as stock function names. Similarly a referenced address might be a data pointer, control-site inside another function, or address *end*, rather than a function beginning.

Added reproducible, **read-only** `tools/audit_wiki_coverage.py` to scan a locally available, versioned MKMSZ-Randomizer `wiki/` and compare addressed sections with Ghidra manifests. Example (from the MKMSZ-Ghidra root):

```bash
python3 tools/audit_wiki_coverage.py --wiki-dir ../MKMSZ-Randomizer/wiki --output /tmp/mkmsz-wiki-ghidra-coverage.csv
```

Coverage buckets intentionally mean only **direct-global-manifest**, **not-directly-indexed**, or **scope-ambiguous-review**, with source page/section/line and applicable manifest names in the CSV. No auto-import, automatic semantic parity claims, unverified function creation or overlay VA flattening. Script execution on a complete local Wiki clone remains to be confirmed; static CI validity is a separate check. Absence of a manifest marker is not proof that the binary was never analyzed. This audit is an index to prioritize focused manual/evidence-backed reconciliation, not a scoring system for reverse engineering completeness.

**State:** Both second-pass manifest additions and **Ghidra local application of all 34 new annotations are confirmed** by the maintainer's 2026-10-08 console (see below). Prior 139/139 function and 35/35 global import remains confirmed. The larger cross-domain audit remains incomplete, and PR #3 stays draft.

## Second-pass import closure — maintainer Ghidra console (2026-10-08)

```text
ApplyMkmszExtended.java> Running...
MKMSZ extended analysis scope: global
TYPE ALREADY PRESENT: MKMSZ_ItemId (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_BoxBacking (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_PickupRecord (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_PersistenceV2 (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_EnemySpawnRecord (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_AuxTriggerRecord (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_RenderNode (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_DynamicTextureSlot (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_Type5ImageHeader (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_EnemySpawnConditionalRecord (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_Type5ModelTableHeader (existing definition preserved)
SKIP bookmark 80030974 category MKMSZ/animation: preserving locally owned note
MKMSZ extended analysis: applied 34, skipped 12 (scope=global)
ApplyMkmszExtended.java> Finished!
```

**Ghidra/implementation-confirmed bounded:** exactly 34 new second-pass operations applied, matching 17 comments plus 17 bookmarks. No unexplained skips: 11 preexisting type names and one deliberately preserved local animation bookmark. This does **not** establish strict byte-for-byte field-equivalence for those 11 types. In the preceding pass 38 trace sites were applied; 55 distinct added trace sites are now represented. Imported data in the local project remains distinct from Wiki evidence of stock or production behavior. No ROM tests or edits occurred.

## Read-only Ghidra type-equivalence audit — Ghidra/implementation-confirmed (2026-10-08)

The user requested field-level confirmation of 11 named types previously preserved by `ApplyMkmszExtended.java` rather than relying only on the log `TYPE ALREADY PRESENT`. Added `ghidra_scripts/AuditMkmszTypes.java` for the **global clean USA Rev0 program**. It reads `analysis/types.tsv`, resolves the 11 curated `/MKMSZ` definitions, and compares the local Ghidra definitions without modifying them:

- Structure kind, total byte size, every defined field name/offset, data type (including array length, fixed pointer and signedness), and unexpected extra defined components.
- Enum kind, storage width, all member names/values, and unexpected extra members.
- Prints `MATCH`, `MISMATCH`, or `MISSING` for every curated type plus final totals. A mismatch means review is required; the script deliberately has **no repair/overwrite path**.
- Rejects unknown program hashes or non-big-endian programs, requires the repository root to read the checked-in manifest, and performs no filesystem writes.

To run after pulling PR #3 branch: **save your main Ghidra program**, open the global `MKMSZ.z64` clean-ROM program, then run **`AuditMkmszTypes.java`** in Script Manager and select the repository root. Do not run it in stage overlays. Send the complete console output. The maintainer subsequently ran this script in Ghidra 12.1.2 and confirmed all 11 current definitions match; see exact console below. This is an imported-metadata equivalence check, not proof of exhaustive binary recovery.

### Maintainer type audit validation — exact Ghidra console, 2026-10-08

```text
AuditMkmszTypes.java> Running...
MKMSZ read-only type audit: definitions=11, scope=global, category=/MKMSZ
MATCH MKMSZ_ItemId (0x4 bytes, 8 members)
MATCH MKMSZ_BoxBacking (0xa8 bytes, 6 fields)
MATCH MKMSZ_PickupRecord (0x30 bytes, 12 fields)
MATCH MKMSZ_PersistenceV2 (0x50 bytes, 18 fields)
MATCH MKMSZ_EnemySpawnRecord (0x1c bytes, 7 fields)
MATCH MKMSZ_AuxTriggerRecord (0x3c bytes, 7 fields)
MATCH MKMSZ_RenderNode (0x58 bytes, 12 fields)
MATCH MKMSZ_DynamicTextureSlot (0x10 bytes, 6 fields)
MATCH MKMSZ_Type5ImageHeader (0xc bytes, 3 fields)
MATCH MKMSZ_EnemySpawnConditionalRecord (0x20 bytes, 8 fields)
MATCH MKMSZ_Type5ModelTableHeader (0x4 bytes, 2 fields)
MKMSZ read-only type audit: match=11, mismatch=0, missing=0, checked=11, fields=81, enum_members=8
NO CHANGES MADE: differences require separate review; do not automatically overwrite types.
AuditMkmszTypes.java> Finished!
```

**Ghidra/implementation-confirmed:** all **11/11** current `/MKMSZ` definitions match the versioned `analysis/types.tsv` audit's checked dimensions: **81 named/typed fields**, **8 enum name/value pairs**, storage sizes, array lengths, unexpected defined components, and expected structure/enum kinds. **0 mismatches, 0 missing, no Ghidra mutations.** This closes the earlier field-equivalence uncertainty for these 11 declared definitions. It does **not** imply unknown bytes or unmodeled fields are now researched or that interpretations in the Wiki are independently proven correct by type parity.

## Third Wiki→Ghidra reconciliation batch — native audio chronology (2026-10-08)

**Source:** canonical `Production-Rich-Inventory-Music-Static-Investigation.md`, compared against the existing function/global manifests, previous 55 trace annotations, and `relations.tsv`. Supported clean USA Rev. 0 ROM SHA-256 verified as `9c18254abf6722b95aa782fcd310bd95f6bcf147da66beb77ce32ca90673ffc6`. Each added global site is MIPS word-aligned and original instruction bytes were inspected under stock global mapping `ROM=(VA-0x80000000)+0xC00`; this does not establish entire function boundaries.

**Ghidra/implementation-confirmed bounded (maintainer local import recorded below):** **11 distinct code sites**, 11 repeatable comments, 11 Info bookmarks, and **one new NOTE-only indirect callback relationship** `0x80000F24→0x80015950`. Existing `0x80000EF4→0x8007D3FC`, `0x8007D4E8→0x8008A500`, and `0x8007D55C→0x8008910C` relationships were deliberately not duplicated. This batch yields **23 expected new metadata operations** if no local conflicts. There are now **66 reconciled new trace locations across PR #3: 55 previously maintainer-imported + 11 newly maintainer-imported**, not 66 newly discovered functions.

| Code points | Verified meaning | Explicit uncertainty |
|---|---|---|
| `0x80000E44`, `0x80000F80`, `0x80000F88` | Fresh task clear; single queued→active task transfer and queued clear | `trace-open`: overwritten generations/reused buffer before completion not observed |
| `0x80000EF4`, `0x80000F24` | VI generates next task; input/VI callback follows audio service | not a glyph-induced extra VI service |
| `0x8007D4E8`, `0x8007D55C` | Previous PCM enqueue and continuing synthesis after failure | downstream retry is rejected as a root-cause fix |
| `0x8007D98C`, `0x80089270` | Native audio frame and ALSynth sample time advance | no first-failure timing chronology from paired endpoint states |
| `0x8008A550`, `0x8008A57C` | FIFO-full check and successful AI DMA register writes | acceptance is not guaranteed by synthesis |

**Scope:** stock instruction behavior is Static-confirmed; the diagnostic audio rejection is runtime-observed on the bounded supplied route. No particular rich Inventory renderer/resource operation is causally identified. The first producer/consumer phase violation, task generation ownership and complete audible loss budget remain **Pending**. No functions, signatures, locals, types, real cross-reference operands, byte patches, emulator tests or root-cause changes were introduced.

**Batched local validation procedure (completed successfully; exact console below):** after `git pull` (maintainer is already on this branch), back up/save the global clean-ROM Ghidra program and run `ApplyMkmszExtended.java` **once** from Script Manager with the checkout root. Without local conflicts, expect 23 new operations and the 12 already explained skips (11 existing types; one preserved locally owned `0x80030974` bookmark). Record the full console, inspect any additional skips, and spot-check queued handoff/PCM bookmarks. Do not rerun overlay imports, global names, guarded function creation or the 11-type audit for this annotation-only batch. PR #3 stays draft/unmerged.

### Maintainer Ghidra extended import — successful third batch (2026-10-08)

The maintainer ran `ApplyMkmszExtended.java` in the supported global program after pulling the third audio chronology batch and supplied this exact Script Manager console:

```text
ApplyMkmszExtended.java> Running...
MKMSZ extended analysis scope: global
TYPE ALREADY PRESENT: MKMSZ_ItemId (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_BoxBacking (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_PickupRecord (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_PersistenceV2 (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_EnemySpawnRecord (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_AuxTriggerRecord (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_RenderNode (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_DynamicTextureSlot (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_Type5ImageHeader (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_EnemySpawnConditionalRecord (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_Type5ModelTableHeader (existing definition preserved)
SKIP bookmark 80030974 category MKMSZ/animation: preserving locally owned note
MKMSZ extended analysis: applied 23, skipped 12 (scope=global)
ApplyMkmszExtended.java> Finished!
```

**Ghidra/implementation-confirmed bounded:** `applied=23` exactly matches 11 new scoped repeatable comments, 11 new categorized bookmarks, and one NOTE relationship. No new unexplained skips. All 12 skips are 11 preexisting `/MKMSZ` types (already separately field-equivalent in the earlier 11/11 read-only type audit) plus the intentionally preserved locally owned `0x80030974` animation bookmark. This confirms successful batched import into the maintainer's global Ghidra program; it does not independently audit each visual annotation, validate complete function-body boundaries, or resolve the root cause of rich Inventory audio acceleration.

**Coverage after local import:** 66 distinct Wiki-reconciled trace locations are now Ghidra/implementation-confirmed at the aggregate import-operation level, in addition to the separately confirmed 139 global function names, 35 globals, 14 cataloged overlay function entries, 84 typed pickup records, and 11 type definitions. No rerun is needed for unchanged metadata; continue domain-owner coverage analysis and preserve draft PR #3.

## Fourth focused reconciliation batch — Inventory/render/resource lifetime (2026-10-08)

**Canonical owners consulted:** `Native-HUD-and-UI.md`, `Persistence-Inventory-and-Lifecycle.md`, `Test-Lab-Inventory-Hang-Static-Diagnosis.md`, `Production-Rich-Inventory-Music-Static-Investigation.md`, its original `Production-Rich-Inventory-Music-Initial-Static-Manifest.md` for historical correction, `Data-Structures-and-Encodings.md`, and `Function-Registry.md`. Inspected existing 139 function entries, curated comments/bookmarks, relationships, and the clean supported USA Rev. 0 N64 ROM (SHA-256 `9c18254abf6722b95aa782fcd310bd95f6bcf147da66beb77ce32ca90673ffc6`). All new stock global sites are MIPS word aligned and have mapped non-empty retail instruction bytes under `ROM=(VA-0x80000000)+0xC00`. No exact function boundary is inferred from a trace location.

**Ghidra/implementation-confirmed bounded (see maintainer log below):** 15 newly indexed original-code sites with 15 repeatable comments plus 15 categorized bookmarks; 6 new warning/open bookmarks at already annotated function/code sites; and 4 source-qualified `NOTE` relationships (36 bookmarks/comments + 4 notes = **40 expected new import operations**). The new stock sites bring the discrete Wiki-to-Ghidra trace-site total from **66 confirmed to 81 (66 previously confirmed + 15 now confirmed)**; the 6 supplemental bookmarks improve existing entries and must not be miscounted as six new locations. This batch does not rename/create functions or add unverified signatures/stack locals/data.

| Cluster | Stock trace site(s) | What the annotation makes discoverable | Status / avoid inference |
|---|---|---|---|
| Inventory lifetime | `80073688`, `80073BC8`, `800728B0`, `800741EC`, `80074260` | Suspend at open, restore at exit, repeated row/panel draw, stock label pointer origin | **Static-confirmed**, not a repeated Inventory prologue |
| Production/stock seam warnings | `80073124`, `80074F88` | Source call sites that generated rich modules repoint to reclaimed stock code addresses | **Static-confirmed** site provenance; rich trampoline is **production-only**, not a native clean-ROM function |
| Palette miss and freeing | `8001C81C`, `8001C6D0`, `8001C898` | Miss allocation, full 256-color conversion path and conditional free | **Static-confirmed**; no observed corrupt release or proven audio victim |
| Graphics processing | `8001EBB8`, `8001EC20`, `8001ED00`, `80020108`, `8001BA84` | Glyph node submit, render-bucket processing, pipe-sync and first/second bank correction | **Static-confirmed**; past second-bank-only decoder assumption **rejected** |

Supplemental warning/open bookmarks on existing code: `80066478` (arena rewind does not invalidate a *production* HUD pointer; stale-write risk **Pending**), `8001C628` (reference counter wrap is not automatically a free/damage event), `8001C2B4` (reused slot +0x08 source width is caller-owned), `80073CEC` (per-glyph CPU work not proven tempo trigger), `8001C64C` (releasing handles before queued GPU use may be unsafe), and `8001E578` (context-specific glyph builder is not a universal HUD API). No source claim is promoted beyond its original static/runtime scope.

New relation NOTE-only records, no synthetic operand cross-references: `80073688→80028870` stock suspend call, `80073BC8→800288A8` stock restore call, `8001C64C→8001C898` conditional free, and `8001EC20→8001ED00` kind-2 render dispatch. Existing `80073CEC→8001C528` acquisition and `80073DB8→8001E578` builder notes remain unchanged.

**Important rejected shortcut:** custom rich-module entry `A01B3210`, its pointer slot `A01B2DE0`, and reclaimed generated helpers at `800742B8..800743A8` must not be imported as stock-code functions, labels or production-safe reusable caves. The accepted custom first-load `a0=0x1200` correction is Runtime-confirmed for a bounded TEST LAB proof; its unsafe historical v14-v19 null-path allocator call is not a retail function. The static stale-cache-after-rewind counterexample is independent of audio; no captured Fortress stale write or identified upstream audio cause is claimed. The paired state graphics cursor 180/377 samples are **partial phases**, not measured workload rate.

**Validation gate (one batched run):** maintainer pulls the existing PR #3 branch, saves/backups clean-ROM global Ghidra program, and runs `ApplyMkmszExtended.java` once, selecting checkout root. Expected with no newly owned conflicts: **applied=40, skipped=12**, the 12 unchanged skips being 11 field-equivalent existing types and protected `0x80030974` animation note. Save full console; any additional skip needs inspection. No overlay importer, guarded global function creator, names importer or type audit rerun is required. Keep PR #3 draft.

### Maintainer Ghidra fourth-batch import confirmed — 2026-10-09

The maintainer ran `ApplyMkmszExtended.java` against the global supported clean-ROM program and supplied the complete console:

```text
ApplyMkmszExtended.java> Running...
MKMSZ extended analysis scope: global
TYPE ALREADY PRESENT: MKMSZ_ItemId (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_BoxBacking (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_PickupRecord (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_PersistenceV2 (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_EnemySpawnRecord (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_AuxTriggerRecord (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_RenderNode (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_DynamicTextureSlot (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_Type5ImageHeader (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_EnemySpawnConditionalRecord (existing definition preserved)
TYPE ALREADY PRESENT: MKMSZ_Type5ModelTableHeader (existing definition preserved)
SKIP bookmark 80030974 category MKMSZ/animation: preserving locally owned note
MKMSZ extended analysis: applied 40, skipped 12 (scope=global)
ApplyMkmszExtended.java> Finished!
```

**Ghidra/implementation-confirmed bounded:** all 40 newly staged metadata operations were reported applied, matching **15 code comments + 15 bookmarks** for new stock code sites, **6 additional bookmarks** on existing annotated code, and **4 NOTE-only relationships**. All 12 skips are explained: eleven existing `/MKMSZ` types already separately verified as equivalent (11/11) and one protected, locally edited animation bookmark at `0x80030974`. No unexpected skip or collision is reported.

This brings the PR's **81 Wiki-to-Ghidra trace-site entries** to confirmed aggregate local import, in addition to 139 global function names, 35 globals, 14 scoped overlay entries, 84 ordinary pickup record structures, and 11 verified matching types. Import success does **not** prove that every code-unit semantics or function boundary is correct, that all Wiki knowledge is represented, or that stale HUD/palette/graphics operations caused accelerated music. The upstream audio root-cause investigation remains Pending. No further local importer run is needed for unchanged manifests. PR #3 remains draft/unmerged.

## Fifth bounded research batch and measurable migration dashboard (2026-10-09)

The canonical versioned Wiki was enumerated at main and read across **64 Markdown pages**. Excluding `Project-Status.md`, `Home.md` and `1.0-Requirements-and-Roadmap.md` per the existing read-only audit gives **61 scanned pages**. The independent scan uses the same per-page/section/address deduplication and the same `0x80[0-9a-fA-F]{6}` address regex as `tools/audit_wiki_coverage.py`.

**Pre-fifth-batch lexical address visibility:** **2,873** total page/section/address occurrences; **975** direct global-manifest matches; **1,229** raw `0x800...` occurrences without a direct global manifest match; **669** `0x801...`/`0x802...`/other occurrences withheld for scope review. The eligible *raw-prefix* denominator is `975 + 1229 = 2204`, giving **44.24% directly indexed and 55.76% not directly indexed**. It is deliberately NOT an estimate that 44.24% of N64 game code, Wiki knowledge, structures or whole reverse engineering is complete. Specific failure modes include PS1-origin `0x800...` addresses (e.g. `PS1-Research.md`), native data pointers, production-only patch addresses, instruction interiors, stage-overlapping VAs, documentation echoes and rejected historical observations. The metric can move when a Wiki editor adds/reorganizes sections, even if reverse engineering does not change. The full scope, imported-manifest status and still-unknown work are documented in `docs/migration-progress.md`.

**Fifth batch staging:** added 5 paired stock-code comments + search bookmarks at `80028870`, `800288A8`, `8002867C`, `8002877C`, `8007CAF8`, and separate **data-only bookmarks** at `800A633C` (item-label pointer table) and `800A4410` (12-byte global file-descriptor table). Their stock coordinates were checked against the supported clean ROM; SHA-256 `9c18254abf6722b95aa782fcd310bd95f6bcf147da66beb77ce32ca90673ffc6`, 16,777,216 bytes, big-endian `.z64`. The five code positions map to ROM offsets `0x29470`, `0x294A8`, `0x2927C`, `0x2937C`, `0x7D6F8`. The data tables map to `0xA6F3C` and `0xA5010`. The research evidence is on current Wiki `Test-Lab-Inventory-Hang-Static-Diagnosis.md`, `Function-Registry.md` and `ROM-Overlay-and-Resource-Map.md`.

**Local application Pending** for precisely **12** new extended metadata operations if Ghidra has no local conflicts. This changes **known-location navigation only**; neither the 139 globally named functions, 11 type definitions nor the stage overlay imports require rerunning. After `git pull`, run `ApplyMkmszExtended.java` once in the verified global program; the expected no-conflict summary is `applied=12, skipped=12` (11 existing matching types plus the protected `0x80030974` bookmark). Record any extra skip. The upstream Inventory audio root cause and the independent stale-HUD lifetime correction remain Pending. PR #3 remains draft.
