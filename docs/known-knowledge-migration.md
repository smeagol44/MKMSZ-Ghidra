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
| Curated global code trace sites | 86 | Ghidra comments/bookmarks | Ghidra-confirmed via aggregate import |
| Internal branch labels | 2 | Ghidra code labels | Prior import confirmed; not function entries |
| Retail global table navigation | 2 | Ghidra bookmarks | Fifth batch Ghidra-confirmed |
| Stage resource slot descriptions | 150 | Versioned `stage_resource_slots.tsv` | Conserved as sidecar; not all independently typed in Ghidra |
| Guarded ROM patch/proof locations | 151 | Versioned `rom_patch_sites.tsv` | Conserved as sidecar; ROM offsets are NOT stock VA labels |
| **Total registered structured records** | **674** | **373 Ghidra + 301 intentional sidecar** | **All recorded; doesn't exhaust narrative findings** |

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
