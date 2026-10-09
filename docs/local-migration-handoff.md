# Local Ghidra knowledge migration — prepared handoff

**Current status and latest counts:** [Known-knowledge dashboard](current-known-knowledge-dashboard.md). This handoff becomes actionable only after explicit approval and PR merge; the seven new bookmarks are still not local Ghidra-confirmed.

**State: ready to follow after draft PR #3 is finalized and merged, NOT a request for immediate local testing.**

This repository stores ROM-free analysis metadata and native proof catalogs, while the latest canonical behavioral facts stay in `smeagol44/MKMSZ-Randomizer/wiki/`. This is a handoff checklist, not a claim that the Ghidra database or the entire 40-owner Wiki has been exhaustively migrated.

## 1. What is already locally confirmed

- Supported global program: USA Rev. 0 clean ROM, 16 MiB, big-endian SHA-256 `9c18254abf6722b95aa782fcd310bd95f6bcf147da66beb77ce32ca90673ffc6`.
- Maintainer confirmed imported **139/139** curated global functions and **35/35** global symbols. Eleven existing `/MKMSZ` type definitions matched an exact read-only audit (81 fields, eight enum members, zero mismatches).
- Latest maintainer extended importer returned `applied=12, skipped=12` (11 preserved existing types plus one protected locally edited bookmark at `0x80030974`); that run precedes this branch's seven new `known-stock-navigation` bookmarks.
- Eight independent stage-overlay programs and their ROM/source hashes are recorded in `analysis/overlays.tsv`; stage-specific VAs are not safe to flatten into the global image.
- Known Function Registry navigation is **166/166 source rows represented** in scoped functions, internal labels, existing comments/bookmarks. This is *address visibility*, not proof of 166 separate function boundaries.

## 2. One global update after approval/merge

1. Back up the existing local Ghidra project. Keep the ROM and clean baseline unchanged.
2. Pull `MKMSZ-Ghidra` once PR #3 is merged (`git pull --ff-only` on `main`). Before it merges, the new files live on branch `research/wiki-ghidra-coverage-reconciliation` and are **not** automatically present on local `main`.
3. Open the existing **clean N64 global Ghidra program**, not a separately imported stage overlay. Ensure it matches the pinned ROM SHA-256.
4. In Ghidra Script Manager, with this checkout's `ghidra_scripts/` directory enabled, run `ApplyMkmszAnalysis.java`, select the checkout root, then run `ApplyMkmszExtended.java`, selecting the same root. Save the Ghidra program when satisfied.
5. Specifically inspect the seven new `MKMSZ/known-stock-navigation` bookmarks at:
   `0x800B1BAC`, `0x800B1BD0`, `0x800B1D18`, `0x800B1D38`, `0x802E82B8`, `0x80038BE4`, `0x80038BFC`.
   These are intentionally **not** standalone function creations or typed-data overlays. The stage resource-base slot is dynamic; code sites are interior instructions.
6. Report importer `applied / skipped` totals, notable skip diagnostics, and whether those seven markers appear. Do not assume a specific applied count, because the importer preserves local edits and skips unmapped/previously annotated sites. If needed, rerun the read-only `AuditMkmszTypes.java`; do not replace matching local types.

The title palette descriptor at **ROM offset `0x000B3360`** and the following palette at `0x000B3364` are recorded in `analysis/stock_rom_navigation.tsv`, without inventing a Ghidra global virtual address. They require **no global importer operation**.

## 3. Separately scoped stage programs

If stage overlays need refreshing, follow `docs/overlay-function-bulk-import.md` and `docs/migration-status.md`: extract only from the maintainer's own clean ROM, import eight original overlay files as **separate MIPS32 big-endian programs** at runtime base `0x802ECE30` with the exact `analysis/scopes.tsv` identity. Apply only the appropriate guarded stage scripts. Never use the global importer to write overlay addresses into the stock executable. No new stage overlay source entries were created in this knowledge-only audit.

## 4. Portable evidence and progress

- `analysis/known_knowledge_claims.tsv` gives stable claim IDs and exact original owner/source anchors.
- `analysis/function_registry_crosswalk.tsv` distinguishes function definitions, scoped callbacks, internal labels, bookmarks and comments.
- `analysis/memory_ownership_intervals.tsv` carries classifications and half-open ROM/physical RDRAM bounds; **no confirmed-free interval** is claimed.
- `analysis/known_knowledge_decisions.tsv`, `analysis/lifecycle_contracts.tsv`, `analysis/stage_resource_files.tsv` and related sidecars preserve non-code knowledge without forcing it into Ghidra.
- Run `python tools/report_known_knowledge.py` from this repository for reproducible audited-scope counts; optionally `--wiki-dir /path/to/MKMSZ-Randomizer/wiki` to catch stale source anchors against a current local Wiki checkout.
- A high first-class coverage percentage is only for **the enumerated audited subset**. More canonical owner facts remain unenumerated. Do not claim all Wiki research finished merely because every currently enumerated claim has a target.



### Section-level migration census (all 40 tracked Wiki owners)

After checking out/updating the current `MKMSZ-Randomizer` Wiki locally, run this **read-only** census in the Ghidra repository:

```bash
python tools/audit_wiki_section_coverage.py --wiki-dir ../MKMSZ-Randomizer/wiki --csv /tmp/mkmsz-section-coverage.tsv --json /tmp/mkmsz-section-coverage.json
```

It reads only the current Wiki, `analysis/known_knowledge_owners.tsv`, and the first-class known-claims ledger. It counts all level-2/3 headings in **all 40 tracked owner pages**, marks a section as *source-navigable* only when at least one uniquely identifiable, nonstale known claim points inside it, and prints stale, ambiguous and preamble claims separately. A heading with one linked claim is **not** an exhausted section: the percentage is a bounded source-navigation metric, not a measure of complete reverse engineering or even all Wiki facts. Nothing is committed, patched, or imported by running this audit; the CSV/JSON paths are optional outputs.

The nine formerly unreviewed owners already have an immutable 242-heading source snapshot in `analysis/remaining_owner_sections.tsv`. The live census deliberately reconstructs **all** owner headings from the current source rather than copying/versioning the full Wiki again. If the current Wiki changes, update it first, rerun the census, and distinguish stale anchors from newly established findings.

**Native XP follow-on:** `analysis/xp_progression_contracts.tsv` contains 18 additional source-linked facts, including links to three *already imported* global functions. It adds no new Ghidra importer item; the seven staged bookmarks and one-pass local handoff are unchanged. Fortress gate coordinates remain stage-overlay scoped.

**Memory ownership interpretation:** `analysis/memory_semantic_contracts.tsv` provides 24 additional source-pinned safety contracts and three links to already-imported stock allocator functions. These are companion facts, not new code/data import items; the seven staged bookmarks and one-pass local handoff remain unchanged.

**Global-item follow-on:** `analysis/global_item_semantic_contracts.tsv` records 28 new source-linked native/materialization/solver facts, six linked to already-imported MKMSZ functions. The function and repeatable comments for **existing** stock `0x80038ACC` gain the verified callback ABI limitation; those *revised comments* are repository-staged pending the eventual importer run and must not be described as locally confirmed. No extra symbol, new function, or bookmark is required; the seven bookmark handoff remains unchanged. Temple/Fortress overlay coordinates remain scoped to their stage programs, not the global executable.

## 5. Sign-off gates still open

- The **40 tracked Wiki owners now all have a partial first-pass crosswalk**. Complete the deeper section-by-section semantic review and explicitly certify evidence-exhaustive owners before claiming an all-known-facts migration denominator. Use the read-only section census above to find unlinked, ambiguous and stale areas.
- Apply/verify seven staged navigation bookmarks in the maintainer's local Ghidra program.
- Review PR #3, merge when approved, then pull and run the importers once. There is **no new ROM, emulator, or production-integration gate** created by this metadata handoff.
