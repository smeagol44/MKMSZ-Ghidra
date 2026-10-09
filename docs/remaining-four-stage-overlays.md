# Remaining four native stage overlay mappings — static evidence (2026-10-08)

**Static-confirmed on the supported clean N64 USA Rev.0 ROM; new local Ghidra import remains Pending.** The file table at ROM `0xA5010` contains 12-byte records (start, end-exclusive, raw flag). The permanent MIPS routine calls `0x80065D64` with stage file ID and destination `0x802ECE30`. Each new mapping was independently verified from its table entry, native-stage loader call and all of that stage's cataloged ordinary pickup records. Five preexisting stage-specific function identities were also mapped to exact 16-byte entry guards.

| Stage | File | ROM interval | Native loader call (ROM/VA) | SHA-256 |
|---|---|---|---|---|
| Temple | `0xA0` | `[0xCA510,0xCF160)` | `0xEE0C / 0x8000E20C` | `eab72de2e8a9104bcb050807bff3cb0ae3ce1640b76857c90d30ec66346b89ce` |
| Wind | `0xA2` | `[0xCF160,0xD8B90)` | `0xFD64 / 0x8000F164` | `f7339eebe4f44efcafdf6da994f7709e9e21ac3895650f59ad194537c508164b` |
| Water | `0xA1` | `[0xB4FC0,0xBAF60)` | `0x104C4 / 0x8000F8C4` | `9e1c1491b8665822ade09697abb6dd53f62c7950a4eadbabf34fa6536e3cfac4` |
| Fire | `0x9D` | `[0xE1B80,0xE6610)` | `0x115F0 / 0x800109F0` | `ee65b26e06694ff36412fdcbb30e20b4ba15ab6fe76e96c1a7c689cac20e36a4` |

The mapped stage record counts are **Temple 4, Wind 6, Water 9, Fire 16** (35 total). All record spans and their native callback pointers were checked in the original ROM. Temple's scripted Map special actor is separate from the four ordinary Temple records.

## Local workflow — no ROM files committed

1. Save the current Ghidra project and run `git pull` on branch `research/remaining-four-stage-overlays` after checkout (do not switch away with uncommitted work).
2. Run `python3 tools/extract_overlays.py "/path/to/clean/Mortal Kombat Mythologies - Sub-Zero (USA).z64" ~/mkmsz-overlays` on your own supported clean file. The extractor refuses an unexpected SHA and checks each of the eight exact output hashes before writing that overlay. Do not commit extracted files.
3. Import each **new** `mkmsz_overlay_temple_a0.bin`, `mkmsz_overlay_wind_a2.bin`, `mkmsz_overlay_water_a1.bin`, `mkmsz_overlay_fire_9d.bin` as a **distinct raw binary program**. Choose MIPS big-endian 32-bit, loaded at `0x802ECE30`; do not flatten their overlapping virtual addresses. Disable automatic analysis when prompted if using the previously accepted raw overlay workflow. Preserve existing four programs.
4. Save program. Run `ApplyMkmszOverlayPickups.java` in each new program and check that expected counts are **4, 6, 9, 16**, all conflict-free. Do not force conflicted entries.
5. Run `ApplyMkmszOverlayFunctions.java` in each program; entries: Temple `temple_scripted_map_actor` at `0x802EEC54`; Wind `wind_spatial_trigger_dispatch` at `0x802EE9FC` and `wind_mixed_icon_award` at `0x802F2CB4`; Water `water_icon_award` at `0x802F2448`; Fire `fire_icon_award` at `0x802F0EBC`. The existing importer enforces imported-source SHA, mapping, byte guards and bounded MIPS32 decoding; report any `REVIEW` line before forcing code creation.
6. Run `ApplyMkmszExtended.java` for other stage-scoped metadata after the named function import. Save each program and send the console output. Review function bodies/boundaries separately when needed; no source-level semantic confirmation follows automatically from successful import.

## Boundaries and risks

- **Static-confirmed:** file IDs/ranges/hashes, loader call operands, original entry bytes, stage catalog pickup containment, and stage-qualified names already documented in the canonical Function Registry.
- **Implementation/CI-confirmed:** shared manifests and extractor changes have repository checks; **All four new stages—Fire, Water, Wind and Temple—have passed their guarded Ghidra importer runs (2026-10-08).** All eight stage programs now have imported cataloged records and functions; ongoing RE of unknown functions and complete function-body boundaries remains Pending.
- **No emulator test or ROM patch.** This is a ROM-free manifest/script update; no extracted binary is stored in Git.
- Stage 7/TEST LAB may load Fire file `0x9D` as an extra diagnostic resource; its normal owner remains the Fire stage.
- An importer success means the known entry was defined, not that every instruction, function endpoint, or unknown callback in the overlay was reconstructed. Additional function discovery is a separate investigation.

## Fire importer validation — maintainer Ghidra console, 2026-10-08

The maintainer imported stock raw overlay `mkmsz_overlay_fire_9d.bin` in its own big-endian MIPS32 Ghidra program at `0x802ECE30`, then ran all three importers:

```text
ApplyMkmszOverlayPickups.java> Running...
Overlay Fire pickup records: expected=16, typed=16, already typed=0, conflicts=0
ApplyMkmszOverlayPickups.java> Finished!
ApplyMkmszOverlayFunctions.java> Running...
MKMSZ overlay function import scope: overlay_fire (Fire), entries=1
OK fire_icon_award at 802f0ebc (body instructions are bounded by decoded flow; inspect if truncated)
MKMSZ overlay function import: created=1, renamed=1, unchanged=0, disassembled=1, review=0 (scope=overlay_fire)
Run ApplyMkmszExtended.java afterward only for other scoped metadata.
ApplyMkmszOverlayFunctions.java> Finished!
ApplyMkmszExtended.java> Running...
MKMSZ extended analysis scope: overlay_fire
MKMSZ extended analysis: applied 0, skipped 0 (scope=overlay_fire)
ApplyMkmszExtended.java> Finished!
```

**Ghidra/implementation-confirmed, bounded:** all 16 Fire ordinary pickup records were typed with six original-word guard checks each; the existing Fire icon award entry was automatically decoded and named with no importer review items; no additional extended metadata was applicable. Overall imports now **65/84** ordinary records and **10/14** currently cataloged stage-overlay function entries across five programs. This is not exhaustive function discovery, proof of the full function body, or emulator validation. Water subsequently passed. Wind subsequently passed. Temple subsequently passed; the eight-stage cataloged-entry import is complete.

## Water importer validation — maintainer Ghidra console, 2026-10-08

The maintainer's separate Water `0xA1` raw MIPS32 Ghidra program at `0x802ECE30` successfully executed all three importers:

```text
ApplyMkmszOverlayPickups.java> Running...
Overlay Water pickup records: expected=9, typed=9, already typed=0, conflicts=0
ApplyMkmszOverlayPickups.java> Finished!
ApplyMkmszOverlayFunctions.java> Running...
MKMSZ overlay function import scope: overlay_water (Water), entries=1
OK water_icon_award at 802f2448 (body instructions are bounded by decoded flow; inspect if truncated)
MKMSZ overlay function import: created=1, renamed=1, unchanged=0, disassembled=1, review=0 (scope=overlay_water)
Run ApplyMkmszExtended.java afterward only for other scoped metadata.
ApplyMkmszOverlayFunctions.java> Finished!
ApplyMkmszExtended.java> Running...
MKMSZ extended analysis scope: overlay_water
MKMSZ extended analysis: applied 0, skipped 0 (scope=overlay_water)
ApplyMkmszExtended.java> Finished!
```

**Ghidra/implementation-confirmed bounded:** Water 9/9 ordinary pickup structures typed, one known stock Water callback function created, named, and disassembled, with no reported review items. Extended importer found no further scoped entries to apply. Across six imported programs, overall confirmed totals are **74/84 ordinary records** and **11/14 cataloged overlay function entries**. This does not verify entire function bodies or previously undocumented procedures. Wind subsequently passed; only Temple (four ordinary pickup records and one scripted Map entry) remains.

## Wind importer validation — maintainer Ghidra console, 2026-10-08

The maintainer's separate Wind `0xA2` raw overlay program at `0x802ECE30` successfully executed all three scoped importers:

```text
ApplyMkmszOverlayPickups.java> Running...
Overlay Wind pickup records: expected=6, typed=6, already typed=0, conflicts=0
ApplyMkmszOverlayPickups.java> Finished!
ApplyMkmszOverlayFunctions.java> Running...
MKMSZ overlay function import scope: overlay_wind (Wind), entries=2
OK wind_spatial_trigger_dispatch at 802ee9fc (body instructions are bounded by decoded flow; inspect if truncated)
OK wind_mixed_icon_award at 802f2cb4 (body instructions are bounded by decoded flow; inspect if truncated)
MKMSZ overlay function import: created=2, renamed=2, unchanged=0, disassembled=2, review=0 (scope=overlay_wind)
Run ApplyMkmszExtended.java afterward only for other scoped metadata.
ApplyMkmszOverlayFunctions.java> Finished!
ApplyMkmszExtended.java> Running...
MKMSZ extended analysis scope: overlay_wind
MKMSZ extended analysis: applied 0, skipped 0 (scope=overlay_wind)
ApplyMkmszExtended.java> Finished!
```

**Ghidra/implementation-confirmed bounded:** all 6 cataloged ordinary Wind records passed the guarded structure import, and two function entries were automatically disassembled, created, and named without importer review items. The additional scoped metadata script had nothing to apply. Across seven stage programs, cumulative coverage is **80/84 ordinary pickup records and 13/14 cataloged overlay function entries**. This validates imported known entries, not complete function bodies/semantics or game runtime. Temple subsequently passed; this eight-stage cataloged-entry migration is complete.

## Temple importer validation — maintainer Ghidra console, 2026-10-08

The maintainer's separately imported Temple `0xA0` stock raw MIPS32 program at `0x802ECE30` successfully executed the three existing guarded importers:

```text
ApplyMkmszOverlayPickups.java> Running...
Overlay Temple pickup records: expected=4, typed=4, already typed=0, conflicts=0
ApplyMkmszOverlayPickups.java> Finished!
ApplyMkmszOverlayFunctions.java> Running...
MKMSZ overlay function import scope: overlay_temple (Temple), entries=1
OK temple_scripted_map_actor at 802eec54 (body instructions are bounded by decoded flow; inspect if truncated)
MKMSZ overlay function import: created=1, renamed=1, unchanged=0, disassembled=1, review=0 (scope=overlay_temple)
Run ApplyMkmszExtended.java afterward only for other scoped metadata.
ApplyMkmszOverlayFunctions.java> Finished!
ApplyMkmszExtended.java> Running...
MKMSZ extended analysis scope: overlay_temple
MKMSZ extended analysis: applied 0, skipped 0 (scope=overlay_temple)
ApplyMkmszExtended.java> Finished!
```

**Ghidra/implementation-confirmed bounded:** Temple's four ordinary pickup structures were typed with no reported conflicts. The previously cataloged Temple scripted Map actor entry was explicitly disassembled, created and named with zero review items. The scripted Map is separate from those four ordinary pickups. No additional extended metadata was applicable.

## Eight-stage migration closure (2026-10-08)

All **84/84 cataloged ordinary pickup records** are now imported as separately scoped stage data, and all **14/14 currently cataloged stage-overlay function entries** have been recognized or created/named in Ghidra. Each of eight independently authenticated stock raw overlays is a separate Ghidra program with runtime base `0x802ECE30`. The four new-stage results were Fire (16 records + 1 function), Water (9 + 1), Wind (6 + 2), Temple (4 + 1). Together with the earlier 49 records and nine functions, every entry in the current manifests is accounted for. All reported pickup conflicts and function review counts were zero. The `ApplyMkmszExtended.java` run for each of the four new overlays had no further entries to apply.

**Limits:** this is Ghidra/implementation-confirmed entry and import coverage only, not exhaustive reconstruction of overlay functions, complete function body bounds, manual visual inspection of all records, or gameplay/runtime validation. No emulator or ROM patch was used; no copyrighted ROM bytes are committed.
