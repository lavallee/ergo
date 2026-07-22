# Roadmap — ergo

## Outcome 1 — Consolidate and release the 0.1 contract

- Resolve lessons from the njschooldata conversion into the spec, template,
  validator, and skill without adding ceremony unsupported by real use.
- Make canonical checks, repository linkage, public projection, deterministic
  bundles, and change/version rules pass from a clean install.
- Publish a small compatibility corpus covering good pages and every important
  failure mode.

*Graduation:* njschooldata's full page set passes strict checks and publishes a
leak-free deterministic bundle using a released Ergo version. *Kill:* any core
requirement that cannot be maintained in that proving ground becomes
supplemental or is removed.

## Outcome 2 — Prove transfer to different datasets and repositories

- Adopt data pages in at least two additional projects with materially
  different data shapes and issue types.
- Measure which issues agents find with and without the page, and whether code
  anchors prevent regression during ingestion changes.
- Build a directory-level reader or index over served bundles without turning
  the directory into a new source of truth.

*Graduation:* a cold human or agent avoids known misuses in multiple projects
and can trace each mitigation from page to code. *Kill:* if the format only
fits njschooldata, narrow its claim and stop expanding the taxonomy.

Evidence, 2026-07-22: Aquifer's 25-page, 120-issue multi-publisher corpus
passed strict manifest and code-anchor checks, recovered all 56 migrated
njschooldata v1 issues, and exposed two semantic regressions that frozen
output-parity hashes had preserved. It also supplied the independent examples
that promoted `identity` and `policy` into the recommended taxonomy.

## Outcome 3 — Add executable detection and interop selectively

- Define a minimal portable detection-check contract for issues whose symptoms
  can be tested without reimplementing project logic.
- Generate the highest-value catalog exports from the canonical page and prove
  round-trip expectations explicitly.
- Version the format only when real pages require an incompatible semantic
  change, with migration tooling and fixtures.

*Graduation:* executable checks catch a real regression and at least one
external consumer uses a generated representation. *Kill:* checks or exports
that duplicate project code or drift from the page remain out of core.

## Keeping this file honest

Released capabilities move to `CHANGELOG.md`. Roadmap items require evidence
from an adopting repository, not only design plausibility.
