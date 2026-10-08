#!/usr/bin/env python3
"""Extract verified raw stage overlays from a private clean USA Rev.0 ROM.

Outputs remain local and are NEVER committed. Exact source hashes guard ranges.
Import each output as a separate Ghidra raw MIPS big-endian program at 0x802ECE30.
"""
from pathlib import Path
import hashlib
import sys

EXPECTED = "9c18254abf6722b95aa782fcd310bd95f6bcf147da66beb77ce32ca90673ffc6"
SOURCES = {
    "temple_a0": (0x000CA510, 0x000CF160, "eab72de2e8a9104bcb050807bff3cb0ae3ce1640b76857c90d30ec66346b89ce"),
    "wind_a2": (0x000CF160, 0x000D8B90, "f7339eebe4f44efcafdf6da994f7709e9e21ac3895650f59ad194537c508164b"),
    "water_a1": (0x000B4FC0, 0x000BAF60, "9e1c1491b8665822ade09697abb6dd53f62c7950a4eadbabf34fa6536e3cfac4"),
    "fire_9d": (0x000E1B80, 0x000E6610, "ee65b26e06694ff36412fdcbb30e20b4ba15ab6fe76e96c1a7c689cac20e36a4"),
    "earth_9c": (0xD8B90, 0xE1B80, "f4152a08069f42890136f6ccca97061475661dd707434c379df4ee1ce555dbc0"),
    "prison_9f": (0xC4C70, 0xCA510, "a7f5e4999a74e65c576af1e823cfd3f9e68725d2683eba3dd53b9f344e5ff8fd"),
    "bridge_9b": (0xBAF60, 0xC0330, "3ab3439c99d5c857599f29657e66a798fa5a347ff949e7be9ea30a20b63438e7"),
    "fortress_9e": (0xC0330, 0xC4C70, "bd46bf0ecb461a62fe9d3534f1be127b3dd2597021317c53117311ee5596c6c8"),
}
if len(sys.argv) != 3:
    raise SystemExit("Usage: python tools/extract_overlays.py CLEAN_ROM.z64 OUTPUT_DIR")
rom = Path(sys.argv[1]).read_bytes()
if hashlib.sha256(rom).hexdigest() != EXPECTED:
    raise SystemExit("Refusing unsupported input: clean USA Rev.0 SHA mismatch")
out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
for name, (start, end, expected) in SOURCES.items():
    data = rom[start:end]
    if hashlib.sha256(data).hexdigest() != expected:
        raise SystemExit(f"Overlay {name} digest mismatch")
    dest = out / f"mkmsz_overlay_{name}.bin"
    dest.write_bytes(data)
    print(f"{dest.name}: {len(data):#x} bytes; sha256 {expected}")
print("Do not commit these extracted copyrighted ROM bytes.")
