# Changelog

## 0.2 — 2026-07-26

Ergo becomes a methodology record, not only a defect registry. Driven by a
corpus of seven surveyed datasets, parsers and validators (FEC, NOAA
GHCN-Daily, FDA FAERS/AEMS, CDC WONDER, IRS 990, GTFS) and by grading v0.1
against a second adopting project's 120-issue registry.

**Backward compatible.** `ergo = "0.1"` pages validate unchanged under the
0.2 tool; every field below is additive and all but one are optional.

- **`[practice]` — the second block.** An `[issue]` is a defect that would
  exist without you; a practice is a decision about what may be computed and
  how. The block exists because the cardinality differs: one defect can have
  several handlings selected by the question asked (a conduit topline
  excludes memo lines; a donor list does the opposite), and some practices
  have no defect underneath them at all. Required `id`, `title`, `question`,
  `authority`, `rule`, `because`; expected `naive`; optional `stops_at`,
  `irreversible`, `residual`, `because_not`, `contested`, `addresses`,
  `implemented_by` (SPEC §6).
  - `authority` (`publisher | project | community`) says who decided, and
    therefore whether you may disagree. It is not severity.
  - `naive` is the honesty check: no plausible wrong move being ruled out
    means this is documentation, not a practice. The validator warns.
  - `stops_at` (our automation's boundary, recoverable) and `irreversible`
    (the publisher already decided, input gone) are different situations and
    a reader acts differently on each.
  - Practices share the page's id namespace with issues, so anchors stay
    kind-free; `implemented_by` gets the same two-way anchor round trip as
    `handled_by`, and is legitimately absent on prohibitions.
  - Practices are *more* public than issues: the served bundle carries
    `rule`, `naive`, `because` and the rest, stripping only
    `implemented_by`.
- **`[dataset.missingness]`** — `zero_is_missing` (bool) and `source_tokens`
  (the literals meaning "not a number"). A zero that means "no value" was
  the single most common defect shape across surveyed publishers; the
  manifest flag makes it hard to miss rather than replacing the issue.
- **`unknowns`** — a list of plain sentences naming where the page's
  knowledge stops. Without it, silence is indistinguishable from a clean
  bill of health and a reader cannot tell "no issues" from "nobody looked."
- **`source_urls`** (list) replaces `source_url` (string, still accepted) —
  a dataset routinely has more than one face, and two official products of
  the same data can disagree by design.
- **`version`** — the *source's* own edition label, distinct from `updated`,
  which is a freshness signal for the page and never a version of the data.
- Digest gains a practices column, a per-page practice table under `--long`,
  and prints `unknowns`; `export` and `publish` carry practices and the new
  manifest fields; `new` scaffolds a practice section.
- **`tests/`** — the repo ships a test suite for the first time:
  `tests/negative.md` triggers every error class, `tests/run.py` asserts the
  positive fixtures stay clean, the negative counts hold, and 0.1 pages still
  validate. Run `python3 tests/run.py`.
- SPEC sections 6–14 renumbered to 7–15 to seat the practice registry beside
  the issue registry.

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
