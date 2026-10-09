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

**Implementation/CI-confirmed:** 38 new manifest comments and 38 bookmarks once CI passes. **Ghidra runtime Pending** for their local application. **Static-confirmed:** existing Wiki-researched meanings on their bounded routes only. **Ghidra/implementation-confirmed** for the previously applied eight-stage cataloged pickup/known function imports only. Unknown function bodies remain unknown; no ROM modifications or emulator testing were performed.

Current Wiki provenance: `Function-Registry.md`, `Production-Rich-Inventory-Music-Static-Investigation.md`, `Native-HUD-and-UI.md`, `Persistence-Inventory-and-Lifecycle.md`, `Memory-and-Allocation-Map.md`, `Data-Structures-and-Encodings.md`.
