# Separate overlay pickup import (staged; not Ghidra-runtime validated)

The four previously verified raw overlays (Earth 0x9C, Prison 0x9F, Bridge 0x9B, Fortress 0x9E) have independently SHA-256-matched byte ranges in the clean N64 USA Rev.0 ROM. No ROM bytes are distributed.

This staged branch introduces:
- `ApplyMkmszOverlayPickups.java` — a separate script that uses `overlays.tsv` and `rom_pickups.tsv` to assign **native 0x30-byte pickup structures** to 20 Earth, 10 Prison, 10 Bridge, and 9 Fortress record locations, separately in each overlay's raw program.
- Strict source-program name plus imported-source SHA, big-endian language, mapped region, ROM-coordinate bounds, and six original word guards; existing typed data or code is never cleared. Other stages remain pending independent overlay mappings.
- Two additional documented shared struct formats: conditional enemy spawn opcode 6 and the Type-5 model table header.

**Import procedure, when ready to validate manually:** save the current project. Extract your own verified raw binaries locally using `tools/extract_overlays.py`, import each *separately* as raw big-endian MIPS at `0x802ECE30`, and run `ApplyMkmszOverlayPickups.java` for that active raw-overlay program. It prompts for the repository root. Do not use the separate pickup script on the clean 16 MiB cartridge program.

**Status:** Implementation/repository only. Java/Ghidra runtime import remains **Pending**, including raw binary source SHA identity behavior and data-type creation. Do not claim this as already applied in the user's Ghidra project. On first validation, inspect the exact console results and Ghidra Data Type Manager, and report missing functions/typed records without forcing overlapping definitions.
