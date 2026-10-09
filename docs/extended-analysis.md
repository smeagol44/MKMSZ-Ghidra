# Extended Ghidra analysis metadata

Use the clean USA Rev.0 ROM in its own Ghidra program and complete the original `ApplyMkmszAnalysis.java` step first. Then run **ApplyMkmszExtended.java**, selecting the repository root. Repeat both after `git pull`. Nothing updates automatically.

**Scope is a safety boundary.** `global` accepts only a Ghidra executable SHA-256 matching the original USA Rev.0 ROM. Stage overlays have overlapping virtual addresses. Add an overlay scope only with a separately imported, explicitly identified program and an exact original-input SHA-256; do **not** insert guessed stage-specific addresses into global files. All metadata entries declare a scope. The importer refuses unknown programs.

## Columns / conventions

Each table starts with the exact header in `analysis/`. Use tab delimiters (TSV). Empty files with headers are valid; add rows only after investigating the underlying evidence. Do not treat speculative names/types as confirmed.

- `types.tsv`: `scope kind name size field offset datatype value evidence note`. `struct` declares size; `field` fills at exact byte offset and uses a named parent; `enum` declares an integer width; `member` adds an enum member with numeric value. The importer keeps `/MKMSZ` manifest types up-to-date: exact matches are no-ops; verified name/category/kind/size matches with changed fields or descriptions are synchronized through Ghidra's reference-preserving type replacement; different size or kind is reported as a conflict rather than forcibly changed.
- `signatures.tsv`: `scope address return_type parameters evidence note`. Parameters are comma-separated `name:type`. Only functions with a non-user-defined signature may be modified. No calling-convention changes.
- `locals.tsv`: `scope function_address name datatype stack_offset evidence note`. Explicit verified stack offsets only. Existing variables and clashes are preserved.
- `data.tsv`: `scope address datatype label evidence note`. Define only undefined bytes (never overwrite existing instructions or different typed data). On equivalent existing typed data, reconcile the requested **primary label** as a separate guarded action. A Ghidra-generated default label is replaceable; a different `USER_DEFINED` primary label is preserved and reported.
- `comments.tsv`: `scope address kind evidence text`; kind is `plate`, `pre`, `post`, `eol` or `repeatable`. Non-MKMSZ local comments are preserved.
- `bookmarks.tsv`: `scope address category evidence note` — informational, versioned **MKMSZ-owned** bookmarks. Exact matches are idempotent; existing `Info` bookmarks in the same `MKMSZ/<manifest-category>` at the same address receive the current manifest note. Bookmarks outside this owned namespace/category are not touched.
- `relations.tsv`: `scope from to kind operand evidence note`. `NOTE` creates a relationship bookmark without forcing references; `DATA_REF` / `CALL_REF` require a verified operand index and free reference slot. They never replace existing references.
- `scopes.tsv`: `scope program_name sha256`. Global scope is pinned to the supported clean ROM hash. Any additional entry needs real provenance and a separate import.

Type DSL: `u8`, `u16`, `u32`, `s32`, `void`, `ptr32`, `TypeName` (within /MKMSZ), and fixed `u8[16]` arrays. Do not apply a speculative field layout. Causal call relationships can be recorded as notes until proven references are available.

## What is NOT automatic

The text metadata is not the full Ghidra database. Ghidra's inferred references, decompiler temporaries, and auto-generated analysis remain local; only explicitly reviewed records are shared. We do not synthesize structures from prose, infer missing local-variable storage, or automatically parse wiki pages. No pipeline currently updates this repository on finding evidence: future research must explicitly create/review commits here.

## Limits and validation

The earlier extended importer was **Ghidra/implementation-confirmed** on the maintainer's supported clean-ROM program (including the fifth batch: `applied=12, skipped=12`, where 11 type conflicts and one protected bookmark were already understood). The source-hash and local-conflict safeguards remain mandatory. Additional analysis files staged on the current draft PR have **not** been imported locally yet. Save the existing Ghidra project before running scripts, inspect skip diagnostics, and check new annotations manually; see [local migration handoff](local-migration-handoff.md).

Before committing rows, cross-check the canonical Wiki owner, exact address space and stage scope, confidence label, collision-free bytes and relevant negative evidence. For local discoveries, export with `ExportMkmszNames.java` and review a diff rather than overwriting the curated TSV files.

## Verify the import, not just the apply/skip totals

After importing, run `AuditMkmszImportedState.java` from Ghidra Script Manager against the **same clean global program** and checkout root. This audit is **read-only**: it checks the manifest global function names, global labels, internal code labels, existing type sizes/field names/enum members, typed-data instances **and their primary labels**, managed comments and bookmarks. It reports exact matches by category and itemized mismatches, including intentionally preserved local edits. A passing audit is a consistency check of **enumerated manifests**, not a claim that all Wiki findings are represented or that any emulator behavior is validated.

**Correction after PR #3 local test:** At `0x800B0F68`, the 0x2C-byte `MKMSZ_SpecialActionDescriptor` was correctly typed, but its generated `MKMSZ_SpecialActionDescriptor_800b0f68` label remained instead of `stock_low_kick_special_descriptor`. This exposed an importer bug: `getSymbolAt(at) != null` improperly blocked label creation. The fixed importer processes the label separately from the type, on both first and repeat runs, without overwriting a different user-defined symbol. An earlier `applied 31, skipped 12` report therefore **did not certify complete label fidelity**. This fix and the audit require user-local Ghidra validation after the corrective PR is merged; GitHub CI only checks source/manifest safety.

## Repository-owned Ghidra metadata policy (PR #4 correction)

The local project is intended as a **derived working copy of the versioned `analysis/` manifests**, not a separate manual source of truth. `TYPE ALREADY PRESENT` in an earlier run usually meant a previously imported type, not an end-user change. `isEquivalent` disagreement alone cannot prove who edited the type; it may reflect field/comment changes in GitHub. The previous `Existing locally edited type MKMSZ_PersistenceV2` message was unjustified attribution. The previously audited 11 types were exact as to documented fields, but the current local mismatch must still be measured with `AuditMkmszTypes.java` before claiming its origin.

For exact clean-ROM scope, `ApplyMkmszExtended.java` now converges only **explicitly listed names inside `/MKMSZ`**: create missing types; ignore already-equivalent types; replace same-name, same-kind, same-length definitions that differ; and reject kind/length collisions. Ghidra's `DataTypeManager.replaceDataType` updates existing uses of that type. No unlisted types, stage-scoped types, or unrelated categories are touched. Always back up the local project first, and independently run `AuditMkmszTypes.java` and `AuditMkmszImportedState.java` afterward. CI checks manifest and source properties only; Ghidra runtime acceptance is still **Pending**.

This is **not full Ghidra database replication**. Auto-analysis, decompiler-inferred locals, undocumented symbols/references and private project settings do not become available on GitHub merely by importing reviewed metadata. New verified changes must be exported/reconciled and committed before they are shared through the manifests.

## Import verification closure for the 2026-10-09 local run

Maintainer executed the PR #4 synced importer in the clean global program: **12/12** type names/sizes/88 field layouts/8 enum members matched before and after; `TYPE SYNCED: MKMSZ_PersistenceV2` despite that pass revealed the old read-only type audit omitted **field descriptions**. `stock_low_kick_special_descriptor` now applied automatically. The full read-only import audit then reported **622/623 exact checks**: 139 functions, 35 global labels, 2 code labels, 12 types, 8 enum members, 88 fields, 1 typed data and its label, 232 comments all exact, but bookmark `0x80030974` had an obsolete description. Git history establishes the exact correction from an old standalone animation-token handler guess to an internal `0x800304C0` switch arm (jump table `0x800AD478`), versioned in `analysis/bookmarks.tsv` since `5a0b47938484`.

The updated importer now refreshes the note on existing **manifest-owned `MKMSZ/` Info bookmarks** rather than assuming the older content was manually edited. The detailed `AuditMkmszTypes.java` additionally compares field descriptions to distinguish documentation drift from real ABI/layout changes. **Both changes still require local Ghidra execution** after merging this correction; CI is a static manifest/source check, and the earlier 622/623 result is not yet claimed to be 623/623.
