# Changelog

## 0.1.1 — 2026-07-22

Aquifer dogfood amendment:

- Added `check --require-manifest` after a 24-file source-documentation
  corpus revealed that pages with no Ergo blocks were silently omitted from
  the directory check. The default remains permissive for mixed directories.
- Promoted `identity` and `policy` into the recommended issue taxonomy after
  independent NJDOE, Census/NCES, and public-library source contracts needed
  those distinctions without treating them as generic coding problems.
- Added stdlib regression tests for closed-corpus discovery and the expanded
  taxonomy; tool version is now 0.1.1 while the page format remains 0.1.

## 0.1 — 2026-07-10

Initial draft.

Amended same-day after review of frank's obligation-skill system (its
constitution tier, fail/pass example pairs, structured triggers, and
severity-ranked context degradation):

- `core = true` issue field — the always-load tier — with digest flagging,
  a >⅓ lint warning, and degradation-order semantics (SPEC §5, §8).
- `instead` field pairing with `misuse` to form fail/pass examples.
- Optional `[issue.detect]` sub-table (`regex` — validator-compiled,
  `query`, `semantic`) as the structured form of `detection`.
- Conformance split: core format vs. supplemental affordances (SPEC §3).
- Clarified `mitigated` covers enforced invariants, not only patched
  defects; new open questions (activity routing, `constraint` type
  candidate, curated-internal-dataset profile) from the njschooldata
  conversion.
- `check --repo` on a subset of pages: anchors naming datasets outside the
  checked set downgrade from error to warning (unknown ids within a
  checked dataset still error) — a full-directory run remains the
  authoritative gate. Surfaced twice during the njschooldata conversion.

Second same-day amendment — serving and versioning:

- **Serving convention** (SPEC §8): the bundle — `index.json` (per-dataset
  facts + issue list) plus each page's verbatim `.md` — published at a
  stable URL by the new `ergo publish` subcommand, deterministic. Agents
  fetch documentation over HTTP; they don't spelunk the code host. Human
  explainer pages render the ergo elements and link to the bundle.
- **`[change]` blocks** (SPEC §13): the append-only, dated changelog that
  travels with a served page — `date`, `note`, optional `issues` (validated
  against the registry). Manifest `updated` must be ≥ the newest change
  date (checked). Digest and bundle carry `updated`/`latest_change`.
- Directory-of-bundles vision added to §14 (decentralized maintenance,
  centralized discovery).
- **Public projection** (SPEC §8): the served `.md` is derived, not
  verbatim — `<!-- ergo:internal -->` regions and repo-pointing fields
  (`handled_by`, `evidence`, `access.builders/raw/feeds`) are stripped, an
  internal-smell check warns on what's left, and the new optional manifest
  field `implementation` is the one sanctioned pointer to the publisher's
  code. The served page exists so someone else can build their own
  implementation without our pitfalls — not to document our pipeline.

- SPEC.md v0.1: the data page (markdown + fenced `toml ergo` blocks), the
  `[dataset]` manifest, the `[issue]` registry (effect/type/status
  vocabularies, machine-readable scope, `misuse`, `handled_by`), two-way
  code linkage via `ergo: <slug>/<id>` anchors, `[validation]` records, the
  generated digest/INDEX, authoring discipline, interop mappings.
- `tools/ergo.py` 0.1.0: `check` (page + repo round-trip validation),
  `digest`, `export` (JSON), `new` — single file, stdlib only, Python ≥ 3.11.
- `skills/ergo/SKILL.md`: agent skill for consuming and authoring pages.
- `docs/survey.md`: the comparative landscape survey the format distills.
- Template and worked example (NJ School Performance Reports).
- First proving ground: the njschooldata data pages.
