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
| Guarded ROM patch/proof locations | 151 | Versioned `rom_patch_sites.tsv` | Conserved as sidecar; ROM offsets are NOT stock VA labels |
| **Total registered structured records** | **680** | **379 Ghidra + 301 intentional sidecar** | **All recorded; doesn't exhaust narrative findings** |

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
