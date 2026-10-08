# Separate overlay pickup import (Prison importer execution confirmed)

The four previously verified raw overlays (Earth 0x9C, Prison 0x9F, Bridge 0x9B, Fortress 0x9E) have independently SHA-256-matched byte ranges in the clean N64 USA Rev.0 ROM. No ROM bytes are distributed.

This staged branch introduces:
- `ApplyMkmszOverlayPickups.java` — a separate script that uses `overlays.tsv` and `rom_pickups.tsv` to assign **native 0x30-byte pickup structures** to 20 Earth, 10 Prison, 10 Bridge, and 9 Fortress record locations, separately in each overlay's raw program.
- Strict source-program name plus imported-source SHA, big-endian language, mapped region, ROM-coordinate bounds, and six original word guards; existing typed data or code is never cleared. Other stages remain pending independent overlay mappings.
- Two additional documented shared struct formats: conditional enemy spawn opcode 6 and the Type-5 model table header.

**Import procedure, when ready to validate manually:** save the current project. Extract your own verified raw binaries locally using `tools/extract_overlays.py`, import each *separately* as raw big-endian MIPS at `0x802ECE30`, and run `ApplyMkmszOverlayPickups.java` for that active raw-overlay program. It prompts for the repository root. Do not use the separate pickup script on the clean 16 MiB cartridge program.

**Maintainer Ghidra validation (2026-10-08):** Running `ApplyMkmszOverlayPickups.java` on the imported Prison raw overlay completed without a reported error:

```
ApplyMkmszOverlayPickups.java> Running...
Overlay Prison pickup records: expected=10, typed=10, already typed=0, conflicts=0
ApplyMkmszOverlayPickups.java> Finished!
```

**Ghidra/implementation-confirmed for Prison only:** compilation/execution, imported program identity acceptance, all six per-record byte guards, and ten data creations succeeded without importer-reported conflicts. **Visual inspection confirmed:** the maintainer's Ghidra screenshot at `0x802F21F0` shows the expanded `pickup_prison_01` structure (`MKMSZ_PickupRecord`, 0x30 bytes), its 12 named fields, stock callback `0x80038770`, presentation `0x800B1D18`, and adjacent typed records `pickup_prison_02` (`0x802F2220`) and `pickup_prison_03` (`0x802F2250`). This is a targeted visual confirmation of structure layout, not manual inspection of all ten fields in every record.  the same workflow for Earth, Bridge and Fortress is **Pending**. Do not generalize Prison's successful result to all 49 records or to exhaustive overlay function analysis. The branch remains draft until the remaining local checks are reviewed.
