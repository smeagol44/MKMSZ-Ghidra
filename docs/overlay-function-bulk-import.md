# Guarded overlay function bulk importer

**Status:** First maintainer Ghidra 12.1.2 execution **passed on Prison's three previously manually defined functions**; automatic disassembly/function creation on an undefined stage entry is still Pending. This is a staged replacement for repeating F11, F, and manual renaming at every *known* entry. It does not infer unknown function identities.

## Prerequisites (in order)

1. Save all open Ghidra programs. Remain on `research/overlay-pickup-migration` and run `git pull`.
2. Use your existing separately imported raw programs (Earth 0x9C, Prison 0x9F, Bridge 0x9B, Fortress 0x9E), each imported as **Raw Binary, MIPS big-endian 32-bit, load base `0x802ECE30`**. Do **not** run the importer on the global N64 cartridge program.
3. In one overlay program, open Script Manager and run **`ApplyMkmszOverlayFunctions.java`**, selecting the repository root. The completed baseline test used **Prison first** because its three entries were already individually confirmed.
4. Inspect its final counters. The maintainer-observed Prison run returned **`created=0, renamed=0, unchanged=3, disassembled=0, review=0`**, matching the expected no-recreation behavior. `disassembled` counts newly decoded entries. Do not assume exact counters if you manually changed an entry.
5. Once Prison passes, run the same script individually in Earth, Bridge, and Fortress. These six previously unverified local Ghidra entries may require review. Report any `REVIEW` lines before forcing a function.
6. Run **`ApplyMkmszExtended.java`** afterward in each overlay to apply other qualified metadata; **`ApplyMkmszOverlayPickups.java`** is only needed for new pickup-record imports. Save the project afterward.

## Safety model

- Checks exact stage-specific **imported program name**, SHA-256, 32-bit big-endian MIPS language, and exact raw image mapping against `analysis/scopes.tsv` and `analysis/overlays.tsv`.
- Reads the nine audited function identities from `analysis/overlay_functions.tsv`. Every entry requires a matching original 16-byte prefix in `analysis/overlay_function_guards.tsv`. The prefixes come from the supported clean USA Rev.0 ROM; ROM bytes are not committed.
- Uses Ghidra's dedicated **MIPS32 disassembly command**, not the MIPS16-prone default. Restricts new flow to the current overlay, a 0x1000-byte window, before the next cataloged entry and before any cataloged ordinary pickup record. It does not clear any existing instructions, defined data, custom function boundaries, or manually named functions.
- Creates a function only when a valid 32-bit entry is present; applies the stage-qualified name and a managed plate comment while respecting unrelated user edits.
- Reports created, renamed, unchanged, disassembled, and review counts. **A zero review count means guarded operations completed**, not that complete end boundaries, semantics, or cross-overlay calls have all been proven. Manual inspection remains required for new or ambiguous behavior.
- The script is idempotent on unchanged named entries. Unknown overlays, mismatched originals, wrong processor, preexisting MIPS16 instructions, overlaps, or conflicting user symbols fail closed. It never patches ROM bytes or requires an emulator.

## Verified stock entry offsets

| Stage | Function name | Runtime VA |
|---|---|---|
| Earth | `earth_key_award` | `0x802F52B0` |
| Earth | `earth_boss_construct` | `0x802EDF50` |
| Prison | `prison_trigger_dispatch` | `0x802F1E44` |
| Prison | `prison_scene_actor_update` | `0x802EE320` |
| Prison | `prison_capture_grunt_present` | `0x802F0754` |
| Bridge | `bridge_icon_award` | `0x802EF178` |
| Bridge | `bridge_scene_trigger_dispatch` | `0x802ED888` |
| Fortress | `fortress_assassin_reward_manager` | `0x802EFDB0` |
| Fortress | `fortress_crystal_progression_dispatch` | `0x802EF30C` |

**Evidence classifications:** All nine stock prefixes, stage mappings, and previously researched identities are **Static-confirmed**. The three Prison entries were manually created, decompiled and named by the maintainer (**Ghidra/implementation-confirmed**). The bulk script's identity/guard recognition, conflict-free idempotent naming, and execution **passed on Prison**. Its new-entry MIPS32 disassembly and function-creation paths and Earth/Bridge/Fortress behavior remain **Pending maintainer Ghidra validation**.

## First bulk importer execution — 2026-10-08

Maintainer's already populated Prison program, original 0x9F raw stage image:

```text
ApplyMkmszOverlayFunctions.java> Running...
MKMSZ overlay function import scope: overlay_prison (Prison), entries=3
OK prison_trigger_dispatch at 802f1e44 (body instructions are bounded by decoded flow; inspect if truncated)
OK prison_scene_actor_update at 802ee320 (body instructions are bounded by decoded flow; inspect if truncated)
OK prison_capture_grunt_present at 802f0754 (body instructions are bounded by decoded flow; inspect if truncated)
MKMSZ overlay function import: created=0, renamed=0, unchanged=3, disassembled=0, review=0 (scope=overlay_prison)
Run ApplyMkmszExtended.java afterward only for other scoped metadata.
ApplyMkmszOverlayFunctions.java> Finished!
```

**Ghidra/implementation-confirmed** for existing entry verification, stage matching and idempotence. Does not test creation or unknown-function discovery. Next bounded test: the two Earth entries in the separately imported Earth program.
