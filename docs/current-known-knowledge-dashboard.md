# Current MKMSZR established-knowledge migration dashboard

**Audited snapshot: 2026-10-09.** Canonical behavior, acceptance and evidence still live in `smeagol44/MKMSZ-Randomizer/wiki/`. This is a **routing/portability** dashboard over research the project already established, **not** a reverse-engineering percentage of unknown game code.

## Numbers that can actually be measured

| Independent axis | Current | What it means |
|---|---:|---|
| Tracked canonical Wiki owners with an initial research crosswalk | **40/40** | All forty are **partial**, none certified exhaustive |
| Individually enumerated, already-known findings with an explicit versioned destination | **795/795 currently enumerated** | No remaining unlinked **enumerated** facts. The full Wiki fact denominator remains uncounted |
| Audited claims directly targeting established Ghidra objects | **223/795** | Curated native function, scoped code and type metadata. Not every knowledge claim belongs in Ghidra |
| Level-2/3 sections with at least one uniquely located fact anchor | **174/713 (24.4%)** | Source navigation, **not** semantic completion of the section or research |
| Locally confirmed curated Ghidra catalog records | **379** | Prior maintainer-import baseline, not newly proved today |
| Companion / versioned / Ghidra-pending catalog records | **1,113** | Source-owned semantics and catalog rows, including 242 heading-only navigators |
| Total heterogeneous structured catalog records | **1,492** | Not distinct discoveries; the types of entries vary and can overlap |
| Additional global Ghidra bookmarks awaiting maintainer local import | **7** | Explicitly **Pending** until user observes importer results |
| Known N64 Function Registry records with scoped address navigation | **166/166** | A row may be an interior instruction or dispatch family rather than a standalone function |

**Do not average these axes.** The requested percentage of *all established facts*, as opposed to selected audited facts or reviewed pages, still requires a certified semantic census. The 174/713 heading metric is a transparent triage proxy; it does **not** mean 75.6% of the known game remains to be researched or migrated.

## Latest scoped evidence index (no new ROM discoveries)

`analysis/audio_testlab_known_contracts.tsv` stores 36 current-source, evidence-qualified known findings (18 each) from:
- `Sounds-and-Music.md`: stock 10-byte SFX descriptor layout, stock pickup control, native event/voice path, bank namespace/liveness, accepted/rejected bounded Temple donor carriers, and general music **Pending**. Three stock functions (`0x80064C18`, `0x80080A88`, `0x8007EC4C`) directly reuse existing imported Ghidra function definitions.
- `Test-Lab-Inventory-Hang-Static-Diagnosis.md`: v14 first-load `a0` bug in the disposable rich HUD, observed v16-v19 failures and bounded v20 correction, live process-pointer semantics, KSEG alias caution, signed resource-base pointer `0x802E82B8`, and the independent unforwarded fifth font argument. **Do not claim this is the cause of current rich-Inventory music acceleration.**

Exact Git blob SHAs, source lines, evidence classifications and nonpromotion cautions are preserved in the TSV. `tools/validate_audio_testlab_contracts.py` and `tools/validate_owner_section_snapshot.py` run in CI.

## Prevent duplicated future investigations

1. Start with current `wiki/Project-Status.md`; for feature/release work read `wiki/1.0-Requirements-and-Roadmap.md`.
2. Read the relevant current canonical Wiki owner. It owns truth and supersession; *new Wiki updates outrank old TSV excerpts*.
3. Inspect `analysis/known_knowledge_claims.tsv` by owner and `analysis/known_knowledge_families.tsv` to find Ghidra definitions, overlay-scoped functions, or companion catalogs **before re-tracing the ROM**.
4. For source-ambiguity, run the read-only `tools/audit_wiki_section_coverage.py --wiki-dir ../MKMSZ-Randomizer/wiki` against the updated Wiki. Repeated raw anchors are **not missing facts**; use exact source-line provenance when available.
5. Preserve evidence words: Runtime-confirmed, Static-confirmed, Implementation/CI-confirmed, Hypothesis, Rejected/failed and Pending. Do not flatten donor/PS1 addresses, overlay VAs, production aliases, or proof-only ROM caves.
6. The rich Inventory audio investigation is concurrently active. Its current trigger remains **Pending**. Merge its later changes first or reconcile carefully; **do not** retry AI enqueue on full FIFO as an unapproved production workaround.

## Handoff remaining

- Complete a **semantic** triage of the unlinked Wiki sections: distinguish already-archived historical proof entries from reusable current facts rather than mechanically cloning every old experiment.
- Recheck recent changes to the Wiki audio owner and Ghidra `main` before final PR review. The previously observed `0x8007D4A8` main-branch audio function note has been preserved in draft PR #3.
- Keep PR #3 **draft/unmerged** until user review and approval. Once merged, use `docs/local-migration-handoff.md` for a single bounded local import and confirmation of seven staged bookmarks.

**No clean ROM modification, emulator run, new production patch or new runtime claim was introduced by this dashboard.**
