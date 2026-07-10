# Changelog

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
