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
  governed data platform rather than a website — now carries 25 pages and 120
  issues across survey estimates, modeled health data, library administrative
  records, boundary files, and PDF/OCR extraction: shapes njschooldata does
  not have. A third adopter is still wanted, ideally outside this household.
- Measure which issues agents find with and without the page, and whether code
  anchors prevent regression during ingestion changes. **Not yet measured.**
  A registry existing is not evidence that anyone was saved by it, and this
  bullet is the one that actually carries Outcome 2's claim.
- Build a directory-level reader or index over served bundles without turning
  the directory into a new source of truth.

Evidence, 2026-07-22: that corpus passed strict manifest and code-anchor
checks and supplied the independent examples that promoted `identity` and
`policy` into the recommended taxonomy.

Evidence the second adoption produced that this roadmap did not think to ask
for: a **measured migration** of a registry between two repositories, with a
receipt recording 60 issues in, 56 migrated, 4 deliberately retained, and 3
new findings — among them two semantic regressions that frozen output-parity
hashes had preserved. Two independent conversions have now each surfaced real
defects, which suggests adopting the format is itself a detection method. The
migration also settled a boundary question the spec had left open: a page
belongs to whoever fetches the bytes, not to whoever reads them.

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

## Outcome 4 — A directory that is where most pages live

*Revised 2026-08 (ergo 0.5). The earlier version of this outcome said the
directory holds no page content and killed on accepting patches. That inverted:
a public bundle served from a private repository is **published but
unpatchable**, and a directory cannot fork a page that has no other home. Most
pages have none.*

Agents are effectively the entire audience for these pages, and they read
unfamiliar vocabulary without difficulty. The goal is therefore faithful
transmission, not a complete classification of every data problem on earth.
That changes what the format should be strict about: **close a vocabulary only
where a reader's behaviour branches on it.** `effect`, `status`, `core`,
`scope`, `authority` and `access` all change what a consumer does; `type` does
not — it is a browsing aid, and adopters already write values outside the
recommended list without anything breaking.

- **Done (0.5).** The one-home rule is mechanical: `ergo-directory`'s `check.py`
  errors on an entry naming the directory while its bundle is served elsewhere,
  and on a hosted page with no file. `contribute` says where corrections go.
- Get a **second independent publisher** into the directory. Today 11 of 12
  entries come from one, so nothing has tested who merges, who adjudicates a
  disputed claim, or how either survives agent-paced contribution.
- Have it publish the **observed vocabulary**: every `type` value in use, with
  counts and one example each, so authors converge by looking rather than by
  decree. One real corpus used 92 distinct `type` values across 105 findings,
  so convergence will not happen by publication alone — the skill has to
  propose existing values while an issue is being written.
- Open `type` in the spec once that exists.
- Carry recognition signatures (publisher domain, filename patterns, column
  fingerprints) so a consumer holding an unfamiliar file can ask one place
  whether anyone documents it.

*Graduation:* an agent that has never seen a dataset finds its page from the
file alone, and a publisher outside this household contributes and is merged.
*Kill:* if the directory ends up holding a second copy of a page that is
canonical elsewhere, the anti-fork rule has failed and the hosting model was
wrong.

## Outcome 5 — Cover the failure modes the literature actually measures

*Opened 2026-08 from twelve sources on how models fail at data work. The format
turned out to be thin in places nobody here would have guessed, and ahead of
the evidence in others.*

- **Column-level structure.** Schema linking is the most-measured failure in
  the entire literature — 41.6% (BIRD), 27.6% (Spider 2.0), 35.2% (BEAVER),
  81.2% of all execution failures — and ergo has none. §14 leaves DDI `<var>`
  as future work. Decide whether a page carries per-column facts or
  deliberately refuses to, and say which in the spec.
- **Mixed-grain tables.** The largest single error category on real government
  open data, 32.4% — files mixing "male / female / total" rows. This is a
  structural file property with the same claim to a manifest flag that
  `zero_is_missing` already has.
- **Units, magnitudes, scaling.** No field anywhere records units, "figures in
  thousands", currency year, or percent-versus-proportion.
- **General lore.** Some knowledge is true of every dataset of a shape, not of
  one dataset — unarmored zip codes, Excel serial dates, money as floats.
  `tools/ergo.py`'s `SCAN_SIGNALS` already encodes eleven such rules as Python
  regexes, which is exactly the failure this project names for parsers: earned
  wisdom baked into code and nowhere else.
- **Say publicly where ergo is ahead of the evidence.** No evaluation exists
  for numeric sentinels, suppressed cells, survey weights and margins of error,
  or comparing incompatible vintages. Those are gaps in the literature, not the
  format, and worth stating.

*Graduation:* a documented failure mode from the literature can be expressed in
a page, and an adopting corpus uses the affordance without being told to.
*Kill:* an affordance that no adopter populates after two releases is ceremony
and comes out.

## Keeping this file honest

Released capabilities move to `CHANGELOG.md`. Roadmap items require evidence
from an adopting repository, not only design plausibility.

Numbers cited here carry their date, because they move. DABstep's hard split
went from 14.55% to 89.95% in eighteen months; BIRD's external-knowledge gain
held across three years. An undated benchmark figure in this file is a bug.
