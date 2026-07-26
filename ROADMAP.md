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
  different data shapes and issue types. **One of two.** A second project — a
  governed data platform, not a website — now carries 24 pages and 120 issues
  across survey estimates, modeled health data, library administrative
  records, boundary files, and PDF/OCR extraction: shapes njschooldata does
  not have. A third adopter is still wanted, ideally outside this household.
- Measure which issues agents find with and without the page, and whether code
  anchors prevent regression during ingestion changes. **Not yet measured.**
  A registry existing is not evidence that anyone was saved by it, and this
  bullet is the one that actually carries Outcome 2's claim.
- Build a directory-level reader or index over served bundles without turning
  the directory into a new source of truth.

Evidence the second adoption did produce, which this roadmap did not think to
ask for: a **measured migration** of a registry between two repositories, with
a receipt recording 60 issues in, 56 migrated, 4 deliberately retained, and 3
new defects found *during* the migration. Two independent conversions have now
each surfaced real defects, which suggests adopting the format is itself a
detection method. The migration also settled a boundary question the spec had
left open — a page belongs to whoever fetches the bytes, not to whoever reads
them.

*Graduation:* a cold human or agent avoids known misuses in multiple projects
and can trace each mitigation from page to code. *Kill:* if the format only
fits njschooldata, narrow its claim and stop expanding the taxonomy.

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

## Outcome 4 — A directory that publishes its own vocabulary

Agents are effectively the entire audience for these pages, and they read
unfamiliar vocabulary without difficulty. The goal is therefore faithful
transmission, not a complete classification of every data problem on earth.
That changes what the format should be strict about: **close a vocabulary only
where a reader's behaviour branches on it.** `effect`, `status`, `core`,
`scope` and `authority` all change what a consumer does; `type` does not — it
is a browsing aid, and adopters already write values outside the recommended
list without anything breaking.

- Stand up a directory that indexes served bundles by URL — publishers keep
  their own pages, discovery centralizes, corrections are PRs to the
  publisher, never to the directory.
- Have it publish the **observed vocabulary**: every `type` value in use,
  with counts and one example each, so authors converge by looking rather
  than by decree.
- Open `type` in the spec once that exists. Not before: without a mirror,
  an open vocabulary drifts and cross-publisher questions stop working.
- Carry recognition signatures (publisher domain, filename patterns, column
  fingerprints) so a consumer holding an unfamiliar file can ask one place
  whether anyone documents it.

*Graduation:* an agent that has never seen a dataset finds its page from the
file alone, and two independent publishers converge on the same word for the
same kind of problem without being told to. *Kill:* if the directory starts
accepting content patches it has become a fork of every page in it — stop.

## Keeping this file honest

Released capabilities move to `CHANGELOG.md`. Roadmap items require evidence
from an adopting repository, not only design plausibility.
