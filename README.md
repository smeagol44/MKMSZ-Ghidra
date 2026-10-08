# MKMSZ-Ghidra

Living Ghidra analysis metadata for **Mortal Kombat Mythologies: Sub-Zero (Nintendo 64, USA Rev. 0)**.

This repository exists so the reverse-engineering work can be inspected directly in Ghidra, shared between researchers, and improved over time without distributing the game ROM or relying on an opaque Ghidra project database as the only copy of the knowledge.

## Supported target

- Game: Mortal Kombat Mythologies: Sub-Zero
- Platform: Nintendo 64
- Region/revision: USA Rev. 0
- Game ID: `NMYE`
- Canonical byte order: big-endian `.z64`
- Size: `0x01000000` bytes (16 MiB)
- SHA-256: `9c18254abf6722b95aa782fcd310bd95f6bcf147da66beb77ce32ca90673ffc6`

**No ROM bytes are stored in this repository.**

## Current setup

The MKMSZR research baseline uses:

- Ghidra 12.1.2
- JDK 21
- N64LoaderWV 12.1.2

Ghidra runs natively on Linux. The repository is intended to work on Linux first, but the analysis files themselves are platform-independent.

## Quick start

1. Install Ghidra and the N64LoaderWV extension.
2. Clone this repository.
3. Import your own clean USA Rev. 0 ROM into a local Ghidra project using the N64 loader.
4. Let Ghidra finish its normal auto-analysis.
5. In **Window -> Script Manager**, add this repository's `ghidra_scripts/` directory as a script directory.
6. Run `ApplyMkmszAnalysis.java`.
7. Select the root of this cloned repository when prompted.

The script verifies the imported file hash when Ghidra exposes it, then applies the shared function/global names and managed comments from `analysis/`.

Unknown functions remain unknown. The goal is not to hide the unfinished analysis; it is to make the same partially-understood program visible to everyone.

## Repository layout

```text
analysis/
    functions.tsv      conservative shared function names and semantics
    globals.tsv        conservative shared global labels
config/
    mkmsz-usa-rev0.json
ghidra_scripts/
    ApplyMkmszAnalysis.java
    ExportMkmszNames.java
    ExportMkmszExtended.java
```

The TSV files are intentionally human-readable and diffable in Git.

## Extended analysis (new)

**Extended import support is implemented but not yet validated in a live Ghidra 12.1.2 session.** The established naming script remains usable on its own.

The `analysis/` directory now has scoped record formats for types/structures/enums, function signatures, verified locals, typed data, comments, bookmarks and explicit relations. After pulling new commits, run **ApplyMkmszAnalysis.java**, then **ApplyMkmszExtended.java** from Script Manager. Save your Ghidra project first.

Read [Extended analysis schemas and safeguards](docs/extended-analysis.md) before populating them. The extended importer rejects unrecognized program identities and does not overwrite existing local types, typed data, variable bindings or non-MKMSZ comments. Run **ExportMkmszExtended.java** optionally to produce a read-only review snapshot; it does not update the curated TSV files. Stage overlays need a separate authenticated imported program; a stage VA is not a globally unique symbol.

These new TSVs deliberately start as empty schemas rather than manufactured analysis. Future investigations should add verified entries alongside the canonical Wiki owner. This currently requires an explicit research update/commit; discovery does not automatically trigger GitHub synchronization.

## Analysis workflow

The intended loop is:

```text
inspect/trace in Ghidra
        ->
confirm a function/global meaning
        ->
rename/comment it in the shared analysis
        ->
commit the text metadata
        ->
other researchers git pull + re-run ApplyMkmszAnalysis
```

The companion export script writes a local snapshot of user-defined names for review. It does **not** automatically overwrite the canonical analysis files.

## Evidence

Descriptions use the MKMSZR evidence vocabulary where useful:

- Runtime-confirmed
- Static-confirmed
- Implementation/CI-confirmed
- Hypothesis / strong inference
- Rejected / failed
- Pending

The current MKMSZR Wiki remains the owner of project conclusions and evidence scope. This repository mirrors analysis-facing names/comments so Ghidra becomes progressively easier to navigate.

## Scope rules

- Do not commit ROMs, savestates, generated patched ROMs, or extracted copyrighted assets.
- Do not assume a function name is globally valid merely because one stage overlay uses that virtual address.
- Global functions are seeded first. Overlay-specific symbols will be added with explicit overlay/stage ownership rather than flattened into one address namespace.
- Generated Ghidra databases are local working state. The durable source of shared names/comments/types should remain reviewable text plus scripts.
