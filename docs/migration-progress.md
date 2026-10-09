# MKMSZ-Ghidra migration progress — 2026-10-09

## The intended metric: migration of what we ALREADY know (2026-10-09)

The user specifically wants **the percentage of verified/documented research knowledge transferred into a reusable Ghidra + companion repository**, to stop agents repeating Ghidra/ROM traces. The unknown portion of the game is excluded by definition. The earlier **44.24% raw-address index** is **not** the requested answer; it is retained below only as a triage aid.

See [Known-knowledge migration ledger](known-knowledge-migration.md), source manifests `analysis/known_knowledge_families.tsv` and `analysis/known_knowledge_owners.tsv`, and `tools/report_known_knowledge.py` for the ongoing, reproducible ledger.

**Measured curated inventory: 688 structured known records preserved**, consisting of **379 locally Ghidra-confirmed records** and **309 companion ROM-only catalog rows** that deliberately should not become Ghidra objects. **20/40 (50.0%) Wiki owner pages have had some targeted reconciliation**, but every such page remains only partially audited; **0/40 fully reconciled**. A single percentage of *all already-established semantic findings* is not yet justified: outstanding narratives/constraints/failures still need an enumerated claim-level denominator. These status counts are not percentages of unknown game code and are not to be averaged.

**Fifth batch verified:** maintainer's full console reports `applied 12, skipped 12` in the global Ghidra program; 5 new code trace sites and 2 data-only bookmarks are now Ghidra/implementation-confirmed. All skips were identified and harmless. No further import required for this unchanged metadata.


## What does a migration percentage actually mean?

The migration is **not** synonymous with decompiling or fully reversing the N64 game. The task here is to transfer *already established, scoped, evidence-qualified project knowledge* from the authoritative MKMSZR Wiki into a living, ROM-free Ghidra workspace. Complete reverse engineering has an **unknown denominator**, so a single genuine percentage of all possible functions, types, semantics or game code cannot currently be calculated.

The most useful answer is a **multi-axis progress dashboard** with exact denominators and a separate, intentionally limited Wiki address-visibility proxy. Do not average these rows: they measure different things and their curated inventories are not a census of every discoverable item.

## Validated import of currently curated metadata (before fifth batch)

| Metric | Confirmed imported | Curated denominator | Share | Caveat |
|---|---:|---:|---:|---|
| Named global N64 function entries | 139 | 139 | **100%** | Does not imply all original functions identified or all bodies/ends verified |
| Named global symbols | 35 | 35 | **100%** | Only the 35 currently curated globals |
| Stage-qualified function entries | 14 | 14 | **100%** | 8 independently hash-verified overlay programs; not a full stage decompilation |
| Ordinary pickup records typed | 84 | 84 | **100%** | Current eight-stage ordinary catalog, not all stage objects |
| Curated structure/enum definitions | 11 | 11 | **100%** | Maintainer audit matched all 81 declared fields and 8 enum members; other unknown structures remain |
| Individually reconciled Wiki trace locations | 86 | 86 | **100%** | Maintainer aggregate importer logs include fifth batch; distinct from six supplemental warning bookmarks |

**Fifth batch locally confirmed (2026-10-09):** maintainer reported `applied=12, skipped=12`, with all skips accounted for. Five stock code locations and two data-navigation bookmarks are already in the local Ghidra program.

## Broader Wiki-to-global-manifest visibility (measurable proxy)

**Baseline before fifth batch, sourced from current main Wiki (2026-10-09):** the read-only address scan examined **61 pages** (64 Markdown files minus `Project-Status.md`, `Home.md`, and `1.0-Requirements-and-Roadmap.md`). It deduplicates every exact hexadecimal `0x80xxxxxx` address **within a page section** and asks only whether a matching raw `0x800...` address has an entry in the global function/global/comment/bookmark/internal-label/relation manifests.

| Address-index visibility bucket | Occurrences | Share of eligible raw `0x800...` mentions |
|---|---:|---:|
| Directly indexed in at least one global manifest | **975** | **44.24%** |
| Not directly indexed | **1,229** | **55.76%** |
| **Total eligible raw `0x800...` page/section/address occurrences** | **2,204** | **100%** |
| Separately withheld non-`0x800...` occurrences (scope ambiguous) | 669 | *Excluded from percentage* |
| **Total extracted hexadecimal address occurrences** | **2,873** | *Includes ambiguous* |

**Important:** **44.24% is the address-navigation visibility proxy, NOT the percentage of the whole migration done.** It is neither a count of unique native code facts nor a function/decompilation completeness score. The raw `0x800...` group includes some PS1 addresses, data pointers, generated production locations, internal code sites, historical rejected findings and repeated addresses in different sections. A raw match also does not verify the entry's meaning, import into the user's local Ghidra, or exact scope. The 669 withheld references include overlays sharing virtual addresses and global/dynamic memory needing manual scope handling; they are not 669 missing functions.

A site can already be represented indirectly under its containing function, as part of a structure or as a ROM-only patch-site record. Therefore **1,229 is a classification/review queue, not 1,229 required new annotations**. Increasing this proxy through speculative labels, guessed code/data typing or blanket comments is **not** an objective. This baseline predates the fifth-batch new entries; recompute for the current branch instead of silently treating this static snapshot as a live post-batch figure.

## Provenance-only records versus verified Ghidra objects

| Other durable knowledge | Status |
|---|---|
| 150 stage resource slot records | Catalogued TSV, not 150 separately typed Ghidra objects |
| 151 guarded ROM patch/proof provenance records | Catalogued TSV; ROM offsets are not automatically runtime VA/code objects |
| Function signatures manifest | No records; no valid total target size established |
| Stack locals manifest | No records; no valid total target size established |
| Typed global data manifest | No records; no valid total target size established |
| Cross-reference relationships | Bounded selected notes only; no complete native call-graph claim |
| Remaining unknown code, overlays, semantic conflicts | Pending by definition; there is no exhaustive denominator |

## Reproducible recalculation

From the `MKMSZ-Ghidra` checkout with a neighboring current `MKMSZ-Randomizer` checkout:

```bash
python3 tools/audit_wiki_coverage.py \\
  --wiki-dir ../MKMSZ-Randomizer/wiki \\
  --output /tmp/mkmsz-wiki-address-visibility.csv \\
  --summary-json /tmp/mkmsz-wiki-address-visibility.json
```

The script prints both numerator/denominator and percentages and writes a structured JSON summary with explicit limitations. Always record both repositories' Git commit IDs for reproducibility. The script **reads Wiki and analysis metadata without modifying either**; only its explicitly requested CSV/JSON outputs are written. It cannot test Ghidra runtime import or semantic correctness.

## How to make useful progress from here

1. **Classify high-value missing N64 stock-code and native-data addresses** in current canonical owners. Inventory process ownership and table pointers are the current fifth batch. Avoid blindly adding one marker per mention.
2. **Review ROM-only catalog navigation** (150 resource slots and 151 guarded patch-site rows), keeping file offsets distinct from RAM addresses and protecting overlapping stage overlays.
3. **Add verified function signatures, typed data and locals only where instruction/register/stack evidence supports them**, and require local Ghidra import validation rather than inferring types from prose.
4. **Maintain a reproducible per-owner coverage report and unresolved-review queue**, separating *directly indexed*, *already represented indirectly*, *genuinely missing*, *production-only/PS1*, and *scope-ambiguous* records before asserting any stronger overall percentage.
5. Continue only within accepted release and research requirements. The production rich Inventory audio trigger and stale-HUD lifecycle risk remain open; this metadata transfer is not a substitute for their root-cause analysis.

**Current overall migration completion percentage: unknown / not yet legitimately quantifiable.** The two defensible progress signals are **100% of currently curated, maintainer-validated import batches** and **44.24% direct raw Wiki `0x800...` address visibility in the pre-fifth-batch snapshot**. They answer different questions and must never be averaged.

## First source-anchored known-finding progress score (2026-10-09)

Within the audited Native HUD renderer + descriptor subsection only: **18/22 existing known findings are reusable (81.82%)**, with **4/22 known-but-unlinked stock descriptor addresses (18.18%)**. The scope and exact evidence anchors are versioned in `analysis/known_knowledge_claims.tsv`. This is the correct kind of metric requested, but **the global known-research completion percentage remains not measured** until the other owner findings are enumerated. No user import action is required for this docs-only pass.


## Audited known-finding expansion — Native HUD current state and controls

The source-anchored, claim-level ledger now contains **65 established findings** across bounded Native HUD/UI subsections. **61/65 (93.85%)** are already reusable through imported Ghidra annotations or explicitly routed Wiki/companion evidence; **4** currently lack direct stock-data navigation. This is a *subset completion* metric and cannot be extrapolated to unreviewed owners or full game knowledge. The audit report script now validates these target links and recalculates the denominator automatically.

## Resource/overlay owner audited and first-class migration split (2026-10-09)

Added **42** source-anchored established facts from the ROM/overlay resource owner, with eight matching stage-scoped overlay metadata records. **107** current audited facts across HUD and resource areas: **99/107 (92.52%)** accessible through either native Ghidra mapping or existing routed documentation; more strictly, **37/107 (34.58%)** are first-class Ghidra/independent sidecar representations, **62** are only Wiki-routed, and **8** have no dedicated mapping. Neither measure is total research migration because full-claim enumeration of the other owners is pending. Prefer the **first-class** measure for tracking real transfer into the Ghidra project. See `docs/known-knowledge-migration.md` and the maintained claim ledger for evidence.

## Eight stage-resource files indexed — 2026-10-09

Added 43 known, source-anchored stage facts plus the complete eight-row resource-file sidecar (separate from eight code overlays); CI validates against 84 pickup records and 150 selector slots. Run `tools/report_known_knowledge.py` to recalculate first-class migration % on the growing audited claim subset; the rest of the known Wiki corpus is not yet enumerated. No local importer required.

## Validated stage-resource migration dashboard (2026-10-09)

**73/150 (48.67%) first-class imported or sidecar-migrated findings** in the current *audited* owner subset; **69/150 Wiki-only routed findings** and **8/150 known but not directly linked**. **142/150 (94.67%)** accessible through either metadata or existing Wiki. The newly preserved eight stage-resource mapping records bring the independently curated structured-record inventory to **688 = 379 Ghidra + 309 sidecar**. Coverage outside this audited subset remains unmeasured, not assumed complete. These percentages exclude unknown game content.
