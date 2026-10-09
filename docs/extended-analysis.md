# Extended Ghidra analysis metadata

Use the clean USA Rev.0 ROM in its own Ghidra program and complete the original `ApplyMkmszAnalysis.java` step first. Then run **ApplyMkmszExtended.java**, selecting the repository root. Repeat both after `git pull`. Nothing updates automatically.

**Scope is a safety boundary.** `global` accepts only a Ghidra executable SHA-256 matching the original USA Rev.0 ROM. Stage overlays have overlapping virtual addresses. Add an overlay scope only with a separately imported, explicitly identified program and an exact original-input SHA-256; do **not** insert guessed stage-specific addresses into global files. All metadata entries declare a scope. The importer refuses unknown programs.

## Columns / conventions

Each table starts with the exact header in `analysis/`. Use tab delimiters (TSV). Empty files with headers are valid; add rows only after investigating the underlying evidence. Do not treat speculative names/types as confirmed.

- `types.tsv`: `scope kind name size field offset datatype value evidence note`. `struct` declares size; `field` fills at exact byte offset and uses a named parent; `enum` declares an integer width; `member` adds an enum member with numeric value. The importer creates types in Ghidra category `/MKMSZ` and retains existing types on conflict.
- `signatures.tsv`: `scope address return_type parameters evidence note`. Parameters are comma-separated `name:type`. Only functions with a non-user-defined signature may be modified. No calling-convention changes.
- `locals.tsv`: `scope function_address name datatype stack_offset evidence note`. Explicit verified stack offsets only. Existing variables and clashes are preserved.
- `data.tsv`: `scope address datatype label evidence note`. Define only undefined bytes (never overwrite existing instructions or different typed data). On equivalent existing typed data, reconcile the requested **primary label** as a separate guarded action. A Ghidra-generated default label is replaceable; a different `USER_DEFINED` primary label is preserved and reported.
- `comments.tsv`: `scope address kind evidence text`; kind is `plate`, `pre`, `post`, `eol` or `repeatable`. Non-MKMSZ local comments are preserved.
- `bookmarks.tsv`: `scope address category evidence note` — informational bookmarks, idempotently applied.
- `relations.tsv`: `scope from to kind operand evidence note`. `NOTE` creates a relationship bookmark without forcing references; `DATA_REF` / `CALL_REF` require a verified operand index and free reference slot. They never replace existing references.
- `scopes.tsv`: `scope program_name sha256`. Global scope is pinned to the supported clean ROM hash. Any additional entry needs real provenance and a separate import.

Type DSL: `u8`, `u16`, `u32`, `s32`, `void`, `ptr32`, `TypeName` (within /MKMSZ), and fixed `u8[16]` arrays. Do not apply a speculative field layout. Causal call relationships can be recorded as notes until proven references are available.

## What is NOT automatic

The text metadata is not the full Ghidra database. Ghidra's inferred references, decompiler temporaries, and auto-generated analysis remain local; only explicitly reviewed records are shared. We do not synthesize structures from prose, infer missing local-variable storage, or automatically parse wiki pages. No pipeline currently updates this repository on finding evidence: future research must explicitly create/review commits here.

## Limits and validation

The extended importer is **Ghidra/implementation-confirmed** on the maintainer's supported clean-ROM program (including the fifth batch: `applied=12, skipped=12`, where 11 type conflicts and one protected bookmark were already understood). The source-hash and local-conflict safeguards remain mandatory. Additional analysis files staged on the current draft PR have **not** been imported locally yet. Save the existing Ghidra project before running scripts, inspect skip diagnostics, and check new annotations manually; see [local migration handoff](local-migration-handoff.md).

Before committing rows, cross-check the canonical Wiki owner, exact address space and stage scope, confidence label, collision-free bytes and relevant negative evidence. For local discoveries, export with `ExportMkmszNames.java` and review a diff rather than overwriting the curated TSV files.

## Verify the import, not just the apply/skip totals

After importing, run `AuditMkmszImportedState.java` from Ghidra Script Manager against the **same clean global program** and checkout root. This audit is **read-only**: it checks the manifest global function names, global labels, internal code labels, existing type sizes/field names/enum members, typed-data instances **and their primary labels**, managed comments and bookmarks. It reports exact matches by category and itemized mismatches, including intentionally preserved local edits. A passing audit is a consistency check of **enumerated manifests**, not a claim that all Wiki findings are represented or that any emulator behavior is validated.

**Correction after PR #3 local test:** At `0x800B0F68`, the 0x2C-byte `MKMSZ_SpecialActionDescriptor` was correctly typed, but its generated `MKMSZ_SpecialActionDescriptor_800b0f68` label remained instead of `stock_low_kick_special_descriptor`. This exposed an importer bug: `getSymbolAt(at) != null` improperly blocked label creation. The fixed importer processes the label separately from the type, on both first and repeat runs, without overwriting a different user-defined symbol. An earlier `applied 31, skipped 12` report therefore **did not certify complete label fidelity**. This fix and the audit require user-local Ghidra validation after the corrective PR is merged; GitHub CI only checks source/manifest safety.
