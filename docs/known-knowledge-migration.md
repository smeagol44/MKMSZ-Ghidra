# Migration of established MKMSZR knowledge — living ledger

## Why this exists

**Goal:** avoid paying for the same reverse engineering twice. The source-of-truth for known behavior is current `MKMSZ-Randomizer/wiki/`; the living Ghidra repository mirrors verified names, shapes, code comments, addresses, scoped relationships, and reusable ROM/stage catalogs. A future research chat should consult **Project-Status first, then the appropriate current Wiki owner, then these manifests**, and re-trace only when a documented gap or contradiction justifies it. We are **not** trying to measure how much of the unknown retail ROM has been solved.

A 'known finding' is an evidence-qualified, bounded assertion in an authoritative Wiki owner. It may be a function contract, data layout, stage identity, lifecycle rule, negative control, known failure, or production-only behavior. Copying a long Wiki paragraph to a stock ROM address is not automatically appropriate: ROM offsets, production wrappers, donor platforms and overlapping overlay VAs must retain their scope.

## Current confirmed structured knowledge

| Knowledge family | Curated known records | Reusable destination | Local validation |
|---|---:|---|---|
| Global function identities | 139 | Ghidra names | Ghidra-confirmed |
| Global symbols | 35 | Ghidra names | Ghidra-confirmed |
| Stage function identities | 14 | Eight separate Ghidra overlay programs | Ghidra-confirmed |
| Ordinary pickup records | 84 | Typed Ghidra stage records | Ghidra-confirmed |
| Named type definitions | 11 | Ghidra struct/enum types | Ghidra-confirmed exact 11/11 definitions |
| Trace-category bookmarks | 92 | Ghidra comments/bookmarks | 86 newly reconciled trace locations plus 6 supplemental previously indexed sites |
| Internal branch labels | 2 | Ghidra code labels | Prior import confirmed; not function entries |
| Retail global table navigation | 2 | Ghidra bookmarks | Fifth batch Ghidra-confirmed |
| Stage resource slot descriptions | 150 | Versioned `stage_resource_slots.tsv` | Conserved as sidecar; not all independently typed in Ghidra |
| Eight stage ordinary resource-file mappings | 8 | Versioned `stage_resource_files.tsv` | File identity separate from code overlays; Earth base left unverified |
| Source-qualified project decisions/constraints | 63 | Versioned `known_knowledge_decisions.tsv` | Bounded proofs, requirements and rejected/historical conclusions; source owner remains canonical |
| Classified ROM/RDRAM ownership intervals | 89 | Versioned `memory_ownership_intervals.tsv` | Original owned ranges, classes, scopes and negative controls; not free-space claims |
| Guarded ROM patch/proof locations | 151 | Versioned `rom_patch_sites.tsv` | Conserved as sidecar; ROM offsets are NOT stock VA labels |
| Established persistence/lifecycle contracts | 22 | Versioned `lifecycle_contracts.tsv` | Source-anchored bounded ownership and proof/failure limits |
| Stage-specific resource caveats | 8 | Versioned `stage_resource_caveats.tsv` | Preserves negative controls and stage-scope warnings |
| **Total registered structured records** | **1071** | **379 locally imported Ghidra + 692 sidecar/staged** | **All recorded; doesn't exhaust narrative findings** |

These rows have different granularity and are **not** a percentage of all Wiki knowledge. Do not count 81 type fields as new 81 structures or confuse 150 resource-slot entries with 150 loaded functions. Latest local extended import result: **`applied=12, skipped=12`**, all 12 skips explained (11 existing types; one preserved animation note). No additional Ghidra action for this batch.

## Audit of known behavioral / semantic findings

There are **40** current technical/focused Wiki owner pages in `analysis/known_knowledge_owners.tsv`, based on the current Home routing plus the three focused active evidence topics and failure index. **20 pages have had partial owner-to-metadata reconciliation (50.0%)**. The remaining **20** are not yet systematically audited. **Zero are recorded as fully reconciled**, including the partially examined pages. That means a page can contain already-mirrored facts *and* unmigrated details; it is never counted completed just because some addresses have been bookmarked.

**This 50.0% is an 'owner topics touched' workflow figure, NOT a percentage of known facts captured.** It is useful for avoiding duplicate work and for prioritizing the unfinished crosswalk. The exact percentage of **all already-documented findings** is currently *unmeasured*, rather than the previous unrelated 44.24% direct-address visibility proxy. We will replace that unmeasured field with a legitimate numerator/denominator once every current owner has been broken into source-qualified, deduplicated verified claim units.

## How to use this before a new investigation

1. **Find the canonical owner**, current Project Status, and the exact implementation/proof scope. The Wiki stays authoritative when an old Library report differs.
2. **Search the living metadata** for the address, name, stage and owner; check `functions.tsv`, `globals.tsv`, `types.tsv`, `comments.tsv`, `bookmarks.tsv`, `relations.tsv`, overlay manifests, ROM catalog sidecars, and owner notes as applicable. Do not assume a Wiki fact absent from Ghidra is unknown.
3. **Classify an existing finding** as `ghidra-confirmed`, `versioned-sidecar`, `known-in-wiki-unlinked`, `historical/rejected`, `scope-ambiguous`, or `pending`. Only the third category is a migration gap; do not re-trace it just to rediscover what its canonical Wiki page already proved.
4. **Reconcile the unlinked finding** by adding the smallest accurate first-class metadata and its source/evidence, or a deliberate Wiki-sidecar cross-reference when the fact cannot safely live in stock Ghidra. Preserve overlay scope, false caves, original-byte guards and ownership.
5. **Record local importer evidence** separately from GitHub CI. After the maintainer confirms the exact operation count, update the ledger; do not falsely infer runtime confirmation or full decompiler correctness.
6. **Track owner reconciliation to completion only after reviewing ALL its established findings and known negative controls**, not when a subset of addresses has visible bookmarks. Historical records are preserved as provenance, not promoted as current facts.

## Repeatable progress report

```bash
python3 tools/report_known_knowledge.py --json /tmp/mkmsz-known-knowledge.json
# optional: validate that all owners exist in a local current Wiki checkout
python3 tools/report_known_knowledge.py --wiki-dir ../MKMSZ-Randomizer/wiki
```

The tool validates that the recorded structured counts still match versioned manifests (failing if they drift) and reports separate structured-Ghidra, sidecar and owner-crosswalk results. These are **knowledge reuse / migration statuses**, not a reverse-engineering completion score. The old `tools/audit_wiki_coverage.py` and 44.24% baseline remain useful for *prioritizing navigation gaps* only.

## Next accounting step

For each current owner, generate a claim-level crosswalk with `owner + section + stable fact ID + evidence + N64 scope + current Wiki conclusion + Ghidra/sidecar representation + import proof + review status`. Deduplicate repeated facts across multiple Wiki pages by canonical owner. Don't invent missing signatures/locals or try to type production-only code into a clean-ROM program. Only then calculate **verified facts represented / total current verified facts**, with *unknown ROM knowledge explicitly excluded*. This is the user's desired whole-known-knowledge percentage, and it can grow as claims are reviewed without causing repeated RE.


## Known-finding claim crosswalk v01 — Native HUD rendering (2026-10-09)

**First fully enumerated *bounded subsection*, not an entire-page review.** Audited all established findings in current `Native-HUD-and-UI.md` from `Confirmed gameplay HUD path` through `Rejected or bounded renderer approaches`, retaining source anchors and unique `HUD-RENDER-001..022` IDs in `analysis/known_knowledge_claims.tsv`. Source revision for this pass: Wiki blob `d285ce6554ef77e4036f71fe08c224a3b9f1ccb1`. Historical/production-only facts are routed to their existing Wiki or guarded patch-site sidecar, never invented as retail native functions.

**Measured audited-scope reuse:** 22 known facts, **12** mapped to locally confirmed Ghidra metadata, **6** correctly routed to existing Wiki or versioned sidecars, **4** known but lacking direct reusable navigation metadata. Thus **18/22 = 81.82%** of *this explicit established-finding set* is already appropriately represented; **4/22 = 18.18%** is migration work remaining for this set. The four gaps are original pickup presentation descriptors `0x800B1BAC`, `0x800B1BD0`, `0x800B1D18`, and `0x800B1D38`. All four already have confirmed meanings in the Wiki; **do not re-trace the ROM to rediscover them**. A future batched safe stock-data bookmark import can make them navigable.

Other sections of `Native-HUD-and-UI.md` (including rich Inventory, controls frontend, and full proof chronology) are **not counted** in this denominator and the owner stays `partial-crosswalk`. The 40-owner global research percentage remains Pending until the rest of the established findings have an atomic crosswalk. **No ROM, emulator or new Ghidra annotations** in this pass; no user import action needed. PR #3 stays draft.


## Second source-to-knowledge audit — Native HUD inventory, requirements, frontend (2026-10-09)

This batch enumerates **43 additional already-established findings** using current `Native-HUD-and-UI.md` anchors: top-level rich Inventory/current runtime evidence, accepted Inventory legend/switch/wording, HUD requirements and source/safety routing, and the production GAME SETTINGS + rejected/fixed frontend proofs. No new retail-ROM analysis was needed. Historical wrong-menu and wrong-audio assertions stay clearly **rejected/superseded**, not production guidance; pending audio causation and Water portrait runtime remain pending.

**Cumulative explicitly audited claims:** **65 total**, **16 Ghidra-indexed**, **45 appropriately routed to Wiki/sidecar sources**, **4 documented but lacking direct navigation metadata**, giving **61/65 = 93.85%** reusable *of the enumerated claims only*. The four remaining known navigation gaps are unchanged: original pickup portrait/presentation descriptor addresses `0x800B1BAC`, `0x800B1BD0`, `0x800B1D18`, `0x800B1D38`. None requires redoing the original finding. Coverage of the full 40-owner known corpus remains **unknown**; an audited subset may have a different reuse rate and can expand/shift as further owner sections are reviewed.

**Validation improvement:** `tools/report_known_knowledge.py` now checks stable IDs, owner membership, nonempty source anchors, expected destination availability, and optional current-Wiki anchor matches, and computes the audited numerator and denominator directly from `analysis/known_knowledge_claims.tsv`. No source code or Ghidra metadata changes; no importer run required. PR #3 remains draft/unmerged.

## Resource loading and eight-stage overlay crosswalk (2026-10-09)

Audited the **current canonical** `ROM-Overlay-and-Resource-Map.md` (Wiki blob `5572c7225d9f8123d42fb1c8d2da61a4ddbc8687`) for **42 established, source-anchored claims**, now `RES-001..RES-042`. These include the 12-byte retail global file table; bootstrap raw-file loader; global file-ID versus stage selector; +0x24 pickup field and the base+selector*4 ordinary pickup lookup; embedded/external resource storage, Type-4 image codec, title LZW packaging, eight independently scoped main-stage overlays, and the negative allocation/scope rules. All eight canonical overlay rows were checked against existing `analysis/overlays.tsv` by **scope**, including stage-specific file ID, ROM boundaries, source hash and runtime base; no overlay VA was flattened or created as global code. No ROM read, generated build or emulator run occurred: this is knowledge reconciliation against previously proven owner facts.

**New knowledge gaps only (no new RE needed):** `0x802E82B8` loaded resource-file base slot, exact selector reads `0x80038BE4` and index addition `0x80038BFC`, and title palette data at ROM `0x000B3360`/ `0x000B3364` are established in the Wiki but lack direct first-class navigation entries in the checked manifests. They should be staged as exact-scope bookmarks/labels only after confirming source-map boundaries and avoiding inferred types. Preserve the four older HUD presentation descriptor gaps. Current known facts are not missing knowledge.

**Cumulative source-anchored audited subset:** 107 claims, 35 mapped to existing Ghidra objects, 64 routed to Wiki/sidecars, and 8 unlinked: **99/107 (92.52%) discoverable/reusable**. A more demanding and more useful **first-class migration** measure explicitly excludes self-routes to the canonical Wiki: **37/107 (34.58%)** have a confirmed Ghidra object or *independent versioned sidecar target*; **62** are currently only Wiki-routed, and **8** have no direct reusable target. These are audited-subset percentages; do not extrapolate to all 40 technical owners. The earlier 93.85% figure measured broad existing-source accessibility, **not** successful transfer to the Ghidra repository. Full-owner knowledge coverage stays unmeasured.

`tools/report_known_knowledge.py` now verifies `analysis/overlays.tsv` scope keys and `analysis/types.tsv` exact name+field keys, and reports both percentages directly from the claim ledger. **No Ghidra metadata/import scripts were edited, so the maintainer needs no local Ghidra action.** PR #3 remains draft/unmerged.


## Canonical eight-stage resource-file sidecar and claim crosswalk (2026-10-09)

Added `analysis/stage_resource_files.tsv` containing **8 already established ordinary-pickup resource-file mappings**, separate from the eight code overlays in `analysis/overlays.tsv`. Each row retains the stage's native selector identity, retail table entry, ROM range (converted to end-exclusive, arithmetic checked), size, runtime-base confirmation only where known, picker/outer-slot counts, stage Wiki owner and SHA revision. **Earth's publication slot at `0x802E82B8` is not a verified numerical runtime allocation base**; Temple/Wind file IDs stay blank where the canonical stage file does not name them. Prison file `0x49` is its *resource file*; the code overlay remains `0x9F`. The source remains the current stage Wiki; the sidecar is a searchable, versioned research index, not newly reverse-engineered data.

**43 source-anchored known-finding claims**: for each stage, resource file, pickup count, selector table, code overlay scope and one notable stage-specific limit; three shared stage-index rules. The existing 84 pickup and 150 selector records are counted as preserved structured data, not recounted as 234 new discoveries. A new CI validator checks all eight resource-file intervals, selector IDs/counts, distinct stage overlay scopes, and Earth/Prison identity. `tools/report_known_knowledge.py` now checks composite stage|count and scoped callback targets. No ROM/emulator run or new Ghidra importer required; draft PR #3 is unchanged in state.

**Current auditable total after stage-resource batch:** 150 known findings; 73 first-class represented in verified Ghidra or an independent sidecar (48.67%), 69 still Wiki-only, 8 unlinked. Structured totals updated to 688 including 8 separately versioned resource-file identities. See the live report script; no new Ghidra import.

## Persistence and lifecycle contract crosswalk (2026-10-09)

Transferred **22 source-anchored established lifecycle contracts** from current `Persistence-Inventory-and-Lifecycle.md` blob `54a70762796dc0970510ae6e1cd28220173e711a` into `analysis/lifecycle_contracts.tsv`. These cover MKSV state ownership and capture/restore, Fire's 19-to-16 mapping, XP under Powers-OFF, four-box authority and credential gate exceptions, foreign-key masking, lifecycle v05 rejection and v06 accepted HP path, guarded final reset, and the independent Temple scripted check. Each record includes its exact current Wiki anchor, evidence qualifier, stock/production/historical scope, and limitation. This is independent versioned research metadata, **not retail ROM function labeling**, and no runtime behavior was changed.

Source anchors were explicitly checked against the canonical Wiki before promotion. The report verifies contract IDs resolve from the claim ledger and counts the new 22 sidecar records. The audited (still incomplete) corpus now contains **172** established facts with **95** first-class migrated (55.23%), **69** Wiki-only and **8** without direct navigation metadata. The structured known inventory is **710 records = 379 Ghidra imported + 331 versioned sidecar**. Avoid extrapolating this audited subset to every finding in the 40 owners. No user Ghidra importer action needed; PR #3 remains draft.

## Stage-specific research caveats promoted to independent metadata (2026-10-09)

The eight existing `STAGE-*-BOUND` facts are now source-anchored in `analysis/stage_resource_caveats.tsv` beside their stage identity, evidence, and proof/negative-control limitation. This **does not claim eight new discoveries** or transform stage overlays into global code. Six had only Wiki routes and now gain independently versioned metadata; two were already linked to Water/Fortress scoped callback functions, so those are *relinked*, not newly counted as migrated. **Audited first-class transfer now 101/172 (58.72%)**; 63 Wiki-only, 8 unlinked. The curated structured inventory now counts 8 additional caveat sidecar records: **718 = 379 Ghidra + 339 sidecar**. No Ghidra importer action.

## Verified Function Registry known-contract crosswalk — 2026-10-09

A full **166-row source-anchored** reconciliation of the current N64 function/dispatch tables in `Function-Registry.md` (Wiki blob `0a808dd6cc840b47ac6d61fe26ecb56c9c4590bd`) now lives at `analysis/function_registry_crosswalk.tsv`. Each row retains the **existing Wiki semantics and evidence text**, owner section, native code/address expression, scope, individually indexed and nonindexed addresses, and direct navigation status. This is a *transfer of established explanations* into a durable, searchable sidecar, **not** 166 newly discovered functions.

- **144/166 (86.75%) registry rows** have every named address present in the existing global function, internal-code-label, or appropriately scoped overlay-function manifest.
- **4** are partially indexed multi-address families; **18** do not have an exact address index for their literal listed sites. These **22** are *navigation/reconciliation review*, not proof that 22 functions are missing. Some entries are **instruction interior seams or ranges** (for example the ordinary-pickup `0x800393BC..0x800393D0` dispatch and `0x8002DF28` reaction seam), and multi-routine handlers; investigate function boundaries before creating any new function metadata.
- The internal `0x80030974` animation switch case is mapped to its **existing code label**, not a standalone function. Wind/Prison addresses within the main registry and all six overlay-table entries preserve their stage-specific `overlay_*` scope. PS1 counterparts are **not imported into N64 global metadata**.

The new `tools/validate_function_registry_crosswalk.py` checks each row against the current exact manifests, including overlay identity, and ensures the separate claims ledger agrees. **All 166 facts are now independently recorded**, with 144 also directly navigable through imported scoped Ghidra metadata and 22 preserved as verified Wiki-sourced contracts awaiting careful navigation resolution. CI validates the crosswalk; **no local Ghidra import** and no ROM tracing occurred.

**Cumulative audited-scope first-class knowledge transfer:** **267/338 (78.99%)** source-anchored facts; **63** remain Wiki-only and **8** unlinked. The curated structured inventory is now **884 records = 379 previously Ghidra-confirmed entries + 505 independent sidecar entries**. The 166 contracts overlap the existing function-name records semantically, so the structured inventory is **not** a total of unique research discoveries; do not sum heterogeneous rows to claim game-wide RE completion. Audit of additional Wiki owner facts still remains incomplete.

## Canonical memory ownership interval migration (2026-10-09)

Migrated **all 89 explicit row-identified intervals** in the bounded Memory Map tables into independent `analysis/memory_ownership_intervals.tsv` metadata: **54 ROM-side records (including proof footprints)** and **35 physically addressed RDRAM records**. Each retains its exact Wiki region ID, one-or-more original half-open segments, ownership class, original wording on scope/lifecycle/evidence, documented production-safety field, reference, negative-control notes and source provenance. Aliases are kept as display-only; they are NOT additional allocations. The one three-segment proof-only artifact is represented with multiple segments and **no fabricated single encompassing interval**. One Toasty record omits a separate lifecycle table column, so no lifecycle was inferred.

**Zero intervals are promoted to confirmed-free**; this sidecar does not prove new space, compose overlapping proof allocations, or change runtime behavior. `tools/validate_memory_ownership.py` verifies segment bounds, physical 4 MiB RDRAM limits, alias starts, source linkage, and no confirmed-free promotion. Remaining dynamic/unbounded allocator observations in the Wiki are **not** incorrectly folded into this interval catalog; that is a separate audit.

Cumulative audited established-finding coverage **356/427 (83.37%)** first-class via existing Ghidra objects or independent sidecars, with **63 Wiki-only and 8 unlinked**. This tracks only enumerated known facts, not the unknown game. Curated structured records now total **973 = 379 Ghidra + 594 sidecar**; those heterogeneous records are not unique discoveries. No Ghidra importer change.

## Non-authorizing patch-site to bounded-Memory-Map audit (2026-10-09)

Reproducible read-only `tools/audit_patch_site_ownership.py` compares all **151** existing guarded patch/proof registry records to the known bounded **ROM interval** entries without editing either source. It accepts only an unambiguous literal offset or one explicitly stated ROM point; ranges, multi-offset and file/overlay coordinate expressions are withheld pending source review. The optional `--csv /tmp/mkmsz-patch-map-audit.csv` writes ID-qualified observations.

**No-match does not imply a free interval.** The Memory Map is intentionally **not** a complete ROM partition; a patch-site may be covered by stock code not cataloged as a standalone continuous interval. Overlaps can be parent/child reservations or mutually exclusive proof artifacts; neither implies that two features can compose. This audit does not verify guards, bytes, allocations, runtime behavior, or generate permissions. No new claim records or Ghidra importer operations are introduced.

## 63 canonical Wiki-only decisions indexed without inventing stock ROM behavior (2026-10-09)

Every previously source-only claim in the **currently audited 427-claim subset** now has an independent `analysis/known_knowledge_decisions.tsv` record. It carries the stable claim ID, original owner and exact checked Wiki text anchor, source blob revision, selected target canonical Wiki owner, evidence/scope, decision and nonpromotion caveat. All 63 original-owner anchors were checked against the current live versioned Wiki before committing. The sidecar is a **research navigation index and bounded claim digest**, *not* a new source of authority, new runtime proof, or native Ghidra code.

**419/427 (98.13%) currently audited claims have first-class source-linked metadata** after this promotion, **8 retain no first-class navigation**. However, only **187 claims point directly to existing imported Ghidra manifest objects**; this is not 98% Ghidra program annotation coverage, and the 40-page owner corpus is not yet completely enumerated. Structured catalog rows rise to **1,036 = 379 curated Ghidra-confirmed + 657 independent companion rows**, which are **not** a count of unique discoveries. The importer needs no new run for this particular sidecar batch. Canonical Wikis remain up-to-date sources for statuses, especially the open rich-Inventory audio failure.


## Eight existing stock navigation gaps closed in repository metadata, local import still pending (2026-10-09)

Added **seven source-qualified global navigation bookmarks** to `analysis/bookmarks.tsv` in category `known-stock-navigation`: four preexisting stock pickup presentation descriptor addresses, the dynamic stage resource-base slot `0x802E82B8`, and two exact pickup-selector lookup instructions. These are **navigation markers only**, not new functions, structure data declarations or verified writable storage. They are staged and protected by the existing scope/hash-guarded non-destructive importer; **local application is not yet confirmed**. A separate one-row `analysis/stock_rom_navigation.tsv` preserves the last gap's palette ROM descriptor `0x000B3360` and following palette `0x000B3364` without inventing a global Ghidra VA.

The 427 audited-known claims now have source-qualified first-class destinations (**427/427 in this explicitly enumerated subset**); this is **not a claim that Ghidra contains all those facts or that all current Wiki owners have been exhausted**. Exactly **7 newly staged bookmarks** require a future maintainer pull + importer run and confirmation. Locally confirmed baseline remains the previous 379 curated Ghidra catalog records. The new seven staged bookmarks and one ROM-coordinate record are counted as **versioned-sidecar/pending** until actual import logs are supplied. Curated heterogeneous structured totals: **1,044 = 379 locally Ghidra-confirmed + 665 versioned-sidecar/pending**.

The next pass must audit additional previously unenumerated known behavior in the other canonical owners; otherwise the high audited-subset percentage is misleading.


## Canonical Core Runtime invariants and XP tier table (2026-10-09)

After correcting the canonical `Core-Runtime-and-Address-Database.md` and `Data-Structures-and-Encodings.md` in production source PR #158, **18 exact-anchored runtime invariants** now live in `analysis/core_runtime_invariants.tsv` and **nine exact native tier thresholds** in `analysis/xp_thresholds.tsv` (tier 9 = **7354**, not superseded 7345). Source blob hashes and verified owner anchors are retained. This preserves arena floor/cursor distinctions, no-bounds-check warning, 16 KiB reservation, file-1B bootstrap, pickup manager ABI, correct current-controller slot, and the rejected stage-init tier-evaluator call. No Ghidra signatures or ROM bytes changed. The existing `MKMSZ_PersistenceV2.reserved_tail` type note now describes the established transient GAME SETTINGS editor usage; width/offset remain unchanged.

**The audited subset is now 454 source-anchored findings**, all with a versioned target. That numerator deliberately says only that selected findings are **discoverable**, not that Ghidra imported every fact. Only 187 source-anchored claims currently point to locally/manifest-known Ghidra identities, with 7 new bookmark locations staged for later local importer validation; the rest are canonical proof/ROM/behavior sidecars. Total heterogeneous structured inventory: **1071 = 379 confirmed Ghidra catalog entries + 692 companion/staged records**. Core Runtime and XP owners move from unreviewed to **partial-crosswalk**; not claimed exhaustive, and other owners remain unreviewed.


## Corrected Function Registry navigation census — 2026-10-09

A second manifest-inclusive audit **supersedes** the earlier `144 fully indexed / 4 partially indexed / 18 missing` count. That earlier check mistakenly restricted visibility to `functions.tsv`, `overlay_functions.tsv`, and `code_labels.tsv` while **omitting already recorded Ghidra code bookmarks and comments**. The 22 perceived navigation gaps are already covered by those separately imported/curated annotation manifests. The corrected `analysis/function_registry_crosswalk.tsv` includes **per-address navigation source** (`function`, `overlay-function`, `internal-label`, `bookmark`, `comment`) and validates every source-defined address against those manifests.

**Result: 166/166 currently documented N64 Function Registry rows have complete scoped address navigation in versioned Ghidra manifests.** Some entries are internal instructions, multi-routine families, or annotated call sites, not standalone functions. This is not a binary-wide function count. This correction adds **no Ghidra metadata or importer operations** and prevents redundant future ROM traces. The first-class versioned-claim numerator is unchanged; the number of audited claims **directly linked to Ghidra manifests rises from 187 to 209**, purely by fixing previously misclassified references (454 claims currently audited).
