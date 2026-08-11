# Discovery and distribution: how ergos are found, contributed, and carried

A design note (2026-07-30). It argues for a direction and records the evidence
and precedent behind it, so the format changes that follow can be judged
against something.

**Most of its arguments shipped in 0.5** and are no longer proposals:
`[quote]` and `[reference]` (§8), `[dataset.acquisition]` with a closed
`access` field (§4), `produced_from` and `about = "handling"` (§4–5), and
`ergo scan` plus `skills/ergo/reading-implementations.md` (§12–13). Where a
section below says a thing has "no home", read it as the argument that
produced the change rather than a description of the format. What remains
unspecified: the fetch receipt (a content hash on `derived_from`, so
divergence can be computed rather than guessed), and the registry itself.

Ergo 0.1–0.4 answered *what does a page say*. This note is about *how a page
reaches someone who needs it*, and it argues that answering the second
question changes the first. The format should be downstream of the working
loop, not the other way around.

## Who writes these files

Assume no human ever authors an ergo page by hand, and that almost nobody
reads one directly. Agents write them, agents read them, and a person
encounters the contents through an agent that quotes the relevant part. That
is not a concession; it is the observed lifecycle, and designing against a
different one produces a format optimised for a reader who never shows up.

Four things follow.

**The markdown page survives, for a different reason than the one on record.**
VISION's second strategy bet says one human page is the canonical artifact,
and argues it from human readability. That argument is gone. The form is still
right, on other grounds: it sits in the repository next to the code it
describes, it diffs legibly in a pull request — which is the one place a human
reliably does look — and an agent reads it with nothing in between. Keep the
shape, change the reason.

**Prose is quoted, not generated.** The failure mode of an agent-authored
caveat is a fluent sentence nobody checked. The prose worth carrying is the
publisher's own words with a URL beside them, so an agent can show what the
source actually says rather than paraphrase it into something subtly
different. Ergo has `refs` and dated `[validation]` records; it has no way to
mark a sentence as quoted rather than composed. That distinction is worth more
than most of the fields proposed below.

**The tool should stay a reader.** `tools/ergo.py` parses with `tomllib`,
which is parse-only, and never rewrites an existing page's TOML — `new`
writes a template string, `publish` projects text. So pages are edited as
text, by agents, and comments survive because nothing round-trips them. That
is the right arrangement and it should be protected: a structured writer would
silently delete every comment in every file it touched.

**Use the words the field already uses.** When the reader is a model,
established terms of art are not decoration — they are the difference between
a reader that already knows what a word means and one that has to guess.
Suppression, top-coding, universe, margin of error, vintage, crosswalk, grain,
cardinality, imputation, disclosure avoidance, sentinel values — the Census
itself says "jam values". Invented words cost a definition and invite a wrong
match. 0.4 renamed `bite` to `pitfall` for exactly this reason; the rename was
an instance of a rule, and the rule is: prefer plain language, borrow the
field's real vocabulary when it is more precise, and coin nothing. That
applies to process language too — describe what happens rather than naming it.

## The loop

The goal is not a format. It is a set of defaults for how data work gets
done, such that each step is the path of least resistance:

| step | when | what it needs |
|---|---|---|
| **Orient** | before acquiring bytes | find pages for this dataset, from configured sources |
| **Acquire** | fetching, caching, refreshing | recorded acquisition practice — cadence, auth, rights, verification |
| **Implement** | building, grafting, pressure-testing | issues and practices in scope; anchors on every workaround |
| **Record** | when something bites | a lesson captured locally, at the moment of learning |
| **Offer** | periodically, explicitly | the shareable subset proposed upstream, never sent automatically |

Every format decision below is justified by which step it unblocks. The
steps in the middle already work. **Orient**, **Record**, and **Offer** are
where the format and the distribution story are thin.

## 1. The default contribution is about resources nobody owns

SPEC §10 assumes publishers keep their own pages and directories index them.
Two pieces of evidence say that assumption does not survive contact.

**Aquifer carries 38 pages.** Their subjects are ACS, CDC PLACES, NCES EDGE,
SAIPE, IMLS Public Libraries, Census TIGER, KIDS COUNT, and NJDOE's report
suite. Not one of those publishers will ever write an ergo page, and aquifer
cannot serve a bundle because aquifer is private. Under the current model the
public network for these datasets is empty — not sparsely populated, empty.

**The njschooldata landscape catalog carries 94 sources**, and for each one it
already holds what a stranger would most want: `access` (format, method, auth,
rights, reuse restrictions, size), `release` (cadence, window, lag,
confidence, and how to verify a new drop landed), `grain`, `entity_levels`,
`identifiers`, `joins`, `answers` — plus `implementations[]` describing *other
people's* parsers by entry point, artifact role, and language, `sites[]`
pointing at articles other people wrote, and `gotchas[]` already annotated
with an explicit `ergo_implication` for each.

That catalog is what the first step needs, built by hand, in a private repo,
in a schema that is not ergo. It is the strongest available statement of what
people actually want to know first.

So: **contributions about resources you do not own are not an edge case, they
are the default mode.** The catalog's `implementation_projects` block is the
proof — 14 entries covering tidycensus, tigris, census-reporter, the Urban
Institute education portal, leaidr, edfinr, a CDC PLACES MCP server. All
public open-source work, catalogued by someone with no relationship to any of
it, carrying `repository_url`, `commit`, `license`, `maintenance`, `languages`,
`capabilities`, and `inspected`. That is the missing entry kind, already
designed, in the wild, by an author who was not trying to extend ergo.

Note `commit` in particular: §7 below argues external code references must pin
a revision. The catalog reached that conclusion independently.

### Lessons sort by who they are true for

From aquifer's `acs-5year.md`, one page, four issues:

| issue | true for |
|---|---|
| `jam-values-are-typed-states` | everyone who touches ACS |
| `moe-required` | everyone who touches ACS |
| `geography-not-lea` | anyone joining ACS to NJ district records |
| `b17024-is-identified-by-a-canonical-hash` | aquifer only — it describes aquifer's own convention |

This axis is orthogonal to the public/private split that §9's public
projection handles. §9 filters at the **field** level — strip `handled_by`,
strip runbooks. Splitting a page for public use is an **issue**-level
judgment, and nothing in the format records it. `[practice]` requires
`authority` (`publisher` | `project` | `community`); `[issue]` has no
equivalent. Without it, splitting 38 pages and ~120 issues means reading every
issue and deciding by hand, which means it does not happen.

## 2. What the format cannot hold today

Field by field, over all 94 sources:

| landscape field | fill | ergo home | verdict |
|---|---|---|---|
| `caveats`, `gotchas[]` | 94, 105 | `[issue]` | partial — see below |
| `answers`, `joins` | 94 | `[practice]`, manifest prose | fits |
| `grain`, `entity_levels`, `identifiers`, `coverage` | 94 | manifest (`grain`, `keys`, `coverage`) | fits, thinly |
| `schema_summary`, `time_basis` | 94 | manifest prose | fits |
| `access.{format,method,auth,rights,reuse_restriction,size_notes}` | 94 | — | **no home** |
| `release.{cadence,window,lag,confidence,verification}` | 94 | — | **no home** |
| `implementations[]` + `implementation_projects[]` | 44 / 14 | — | **`[reference]`, since specified** |
| `sites[]` (third-party docs and articles) | 45 | `refs`, on an issue | **`[reference]`, since specified** |
| `artifacts[]` (role, path, language) | 154 | — | still no home |
| `evidence_state`, `release.confidence` | 94 | `confidence` (page-level) | wrong granularity |
| `inspected` (when this claim was checked) | 94 | `updated` (page-level) | wrong granularity |

`refs` exists, but it hangs off an individual `[issue]`. "almartin82/njschooldata
has a working R implementation covering 1999–2026" is about the *dataset*, not
about any one defect, so it has nowhere to live. The fix is a page-scoped
entry kind — provisionally `[reference]` — carrying a typed kind
(implementation / article / schema / discussion / notebook), a URL, a pinned
revision where it is code, what it covers, and who observed it when.

Acquisition guidance belongs on the manifest. It is what the first step needs:
someone starting out wants to know how to get the bytes correctly before they
want a list of defects. `source_url` alone does not carry that.

### Half the gotchas are not about the dataset

Classifying all 105 `gotchas[]` by what the defect is *in*:

| class | count | ergo can express it |
|---|---|---|
| dataset-intrinsic — suppression, uncertainty, identity, comparability | 54 (51%) | yes, today |
| **acquisition and tooling** — url drift, filename drift, archive drift, auth, pagination, cache staleness, parser era, workbook layout | 37 (35%) | **no** |
| **assessment of a third-party layer** — a hosted profile, a convenience wrapper, a simplified geometry | 14 (13%) | **no** |

The middle row is the sharper version of "acquisition has no home." These are
not facts about how to fetch — they are *defects in fetching*, and they bite
exactly as hard. "A 200 response is not proof of a complete layer." "Filename
success is not payload validation." "Cache age is not source vintage." An
`[issue]` whose `effect` is `breaks` and whose subject is the retrieval path,
not the data, is currently unwritable except by pretending it is about the
data.

### Retrieval custody is the most-repeated implication

Each gotcha carries an `ergo_implication` — 105 statements of what ergo ought
to record, written by someone reasoning about ergo from the outside. The
single most common theme is a per-fetch custody record that ergo has no object
for:

> *Store the resolved URL and rule version with each retrieval. · Parser layout
> is source evidence and needs its own version/hash. · Resolved container and
> member names belong in custody. · Cache age is not source vintage. ·
> Convenience aliases must resolve to immutable release IDs before facts enter
> ergo. · A cache hit must be tied to source hash, dictionary hash, geography,
> and edition. · Two convenient routes to the same nominal release are
> different provenance chains.*

Ergo has `source_urls` and `version` on the manifest and dated `[validation]`
records. It has nothing that says *this fetch, on this date, resolved to this
URL, this hash, this parser version, this edition*.

**Caveat, and it is a real one:** this evidence comes from one project whose
entire design centre is custody — aquifer carries `custody_refs` on every
source and a custody-reconciliation document. CONTRIBUTING asks for a second independent
example before promoting anything, and retrieval custody does not
have one. Record it as the strongest single signal in the diff and the one
most likely to be one adopter's preoccupation rather than a format gap.

## 3. Structural precedent

Four systems have solved recognizable versions of this. What each settles:

**DefinitelyTyped — the contribution model.** Third-party metadata about
software the contributors do not own; one monorepo, one directory per
subject, thousands of entries, per-directory owners files, contribution by
fork and PR. It settles three things:

- *Review volume.* PRs are sorted by risk, and the low-risk ones merge
  automatically once CI passes. This is the answer to agent-drafted contributions
  arriving faster than a human can read them.
- *Scale shape.* One git repo at that entry count works. No service is
  needed, which matters because a hosted catalog is an explicit VISION
  non-goal.
- *What happens when upstream takes over.* When a package ships its own types,
  the DefinitelyTyped entry is **removed and points at upstream**. That is the
  one-home-per-page rule with a way out: if a publisher ever serves their own
  bundle, the registry entry becomes a redirect rather than a competitor.

**OSV and CVE — the record model.** Databases of defects in artifacts nobody
controls. Semantically the closest analog ergo has.

- IDs are permanent, records are mutable, and removal is a *state*
  (`withdrawn`, `REJECTED`) rather than a deletion. Ergo reached the same
  conclusion independently at §15 (`superseded_by`), which is a good sign.
- References are **typed** — OSV's `references[]` carries a kind enum
  (advisory, article, fix, report, web, package, …). Ergo's `refs` is
  untyped. Types are what let a consumer ask for "an implementation" rather
  than reading every URL.
- Affectedness is expressed as ranges over versions, not as a version of the
  record. The ergo analog is issue scope over dataset vintage.
- CVE assigns IDs through federated numbering authorities under one
  namespace: stable identifiers without centralizing content.

**Homebrew taps and nixpkgs — the topology.** A fat central default plus
user-configured additional sources, all plain git, maintainers declared
per-file, no auth system anywhere. `ergo-sources.toml` is already a tap list.
The precedent says that shape holds, and that the default source being much
larger than the others is normal rather than a failure of decentralization.

**SPDX-License-Identifier — the code convention.** One greppable comment,
trivially cheap to add, mechanically checkable, and as a result close to
universal. `ergo: <slug>/<id>` is already that shape. The other half of SPDX's
success is that tools can scan a tree and report on it, which is what makes
the convention valuable to people who did not write the comments.

**What not to copy:** npm/PyPI publisher ownership (wrong — the publisher is
absent), and semantic versioning of pages (wrong — see below).

## 4. Registry design

- **One home per page.** A page has exactly one place that accepts patches.
  The registry may be the home for pages whose subject nobody documents, and
  an index for pages that live elsewhere — never a second home for a page
  that already has one. This preserves SPEC §10's argument (a directory that
  patches other people's pages becomes a fork of all of them) while allowing
  a commons for orphaned datasets, which is the majority case.
- **A publisher can take over at any time**, as in DefinitelyTyped: the hosted
  entry becomes a redirect once they serve their own bundle.
- **GitHub for the default registry.** Not familiarity — mechanics. PRs give
  review, attribution, history, and revert at no build cost. CODEOWNERS gives
  per-page ownership without an auth system. Forking means contributing about
  a resource you do not own needs no permission grant. Raw URLs serve the
  bundle directly, which SPEC's own `ergo-sources.toml` example already
  assumes. `gh` lets a skill file a PR with no hosted API at all.
- **How much review a change needs depends on what it claims.** Without that
  split, the merge queue becomes the bottleneck:

  | kind of change | example | review |
  |---|---|---|
  | reference *existence* | "this repo implements a parser, at this commit" | CI resolves the URL and the rev → near-automatic |
  | acquisition fact | "annual, released each autumn" | mechanically checkable against source → light |
  | reference *assessment* | "this wrapper drops uncertainty" | a claim about someone's software → human review |
  | issue or practice | "this column is corrupt" | a claim about truth → human review, always |

  The third row is a correction the diff forced. A pointer looked like a
  uniformly low-stakes claim; 14 of the catalog's 105 gotchas are evaluative
  judgments *about third-party implementations* — "a friendly hosted profile
  is product evidence, not primary-source custody", "library defaults are not
  a freshness policy", "a convenient derived package can be analytically
  useful while still violating ergo's uncertainty contract". Those are
  contestable statements about maintained open-source projects, and the
  maintainers are exactly the people most likely to arrive with a rebuttal.

  So a `[reference]` must keep *existence* and *assessment* in separate
  fields, reviewed differently. That is a second, independent argument for it
  being its own entry kind: only a distinct kind makes the split visible to a
  tool, and the split is what lets the checkable part actually be checked
  automatically.

### Convergence has to happen while the issue is being written

ROADMAP Outcome 4 proposes opening `type` once a directory publishes the
observed vocabulary, and treats it as working when "two independent publishers
converge on the same word for the same kind of problem without being told to."

The catalog's 105 gotchas carry **92 distinct `type` values** — very nearly one
per gotcha. `suppression` appears four times; `schema-era` and `meaning` three;
almost everything else once. A single author, working in one sitting, in one
schema, did not converge with *themselves*.

Two consequences. First, this strongly confirms that `type` is a browsing aid
rather than a field anyone branches on — nothing broke, because nothing reads
it. Opening it is right. Second, it disconfirms the hope that publication alone
produces convergence. A published list that an author must go look at will not
be looked at. Convergence has to happen at authoring time: the skill proposing
existing types ranked by use *while the issue is being written*, with a free
value always available. That makes the mirror a write-path feature, not a
directory page.

## 5. Reading pages out of code that already works

The hardest part of the loop is the first step for a dataset nobody has
documented. There is a way around it: a working implementation is already a
record of everything its author learned, written in the only notation they
were willing to maintain. Read the code, recover the lessons.

**This is not speculative — it is where the catalog came from.** Its 105
gotchas were produced by reading 44 implementations, among them
almartin82/njschooldata's R source, tidycensus, tigris, and census-reporter.
Someone did this by hand, at scale, and it yielded specific, checkable
findings: *the annual ZIP filename changed from lowercase to uppercase in
2026*, *a reported >95 value is converted to 97.5 in one 2020 path*, *pre-2009
files combine identifiers and names*. None of that is in any publisher's
documentation. All of it was in somebody's parser.

### Split it the way the tool is already split

`ergo.py` does the mechanical part, the skill does the judgment — the same
division as `check --repo`, which already walks tracked files looking for
anchors.

A scan finds **candidate sites**, using `repo_files()` and regexes over
tracked text:

| signal in code | what it usually means |
|---|---|
| hardcoded source URLs, URL built by year rule | acquisition, url drift |
| `== -999`, `== "*"`, `replace("N/A", …)`, `fillna(0)` | sentinels, suppression, missingness |
| `if year < 2009`, parser dispatch keyed by year | format era, coverage |
| column rename maps, normalization dictionaries | coding, format drift |
| `skiprows=`, `sheet_name=`, header offsets | workbook layout |
| magic constants in rate conversion (`97.5`) | derived values |
| `try`/`except` around a parse, bare excepts | availability, known failure |
| `# HACK`, `# XXX`, `# NOTE` next to data handling | anything |
| existing `ergo:` anchors | already documented — exclude |

That is a worklist, not documentation, and it is cheap enough to be stdlib
Python over any language's source text.

### One rule the agent has to hold

**Code is evidence of a workaround, not evidence of a defect.** A `fillna(0)`
proves someone chose to fill nulls. It does not prove the publisher writes
nulls meaning zero — the author may have been wrong, or solving a different
problem, or working around a bug of their own.

So a mined page is honest about what it knows:

- `handled_by` — mining gets this exactly right; it is the one field the code
  proves outright.
- `discovered` — from the blame of the workaround, not guessed.
- `status = "mitigated"` — true by construction: a workaround exists.
- the nature of the defect — **inferred**, and marked so. `confidence = "?"`
  on the manifest until someone has checked it against real files, and
  `unknowns` naming what was read (the code) and what was not (the data).

That is what `unknowns`, `confidence`, and `[validation]` are already for. A
mined page is a good hypothesis with its provenance stated, and the first
`[validation]` record is what turns it into documentation.

### Git history is the richest part

The commit that introduced a workaround usually says why, and its diff shows
what the data did. `git log -S` on a sentinel constant finds the moment
somebody learned something. A commit message is a **quotable source** — it has
an author, a date, and a SHA, so it can be cited by permalink rather than
paraphrased, which is the same discipline `[quote]` applies to publisher
prose.

### Running it on other people's libraries

Mining tidycensus produces a page about **ACS**, not about tidycensus, and
that distinction keeps it clean: facts about a public dataset, recovered from
public code. Cite the code by permalink; never copy it into the page.

The exception is the 13% that are judgments about the implementation itself
("this wrapper drops uncertainty"). Those are claims about a maintained
project and belong in the human-reviewed group — and the courteous move is to
tell the maintainers, who are frequently the people best placed to say the
finding is wrong.

### First trial: almartin82/njschooldata, 2026-07-30

Run against the R package at `9c34401`, targeting NJ fall enrollment, with
the catalog's own hand-built findings for that project as a comparison.

**The regex pre-pass** over the three enrollment source files returned 17
candidates across 5 signals — almost all `identifier-padding` and
`hardcoded-source-url`. It did not surface either of the two findings that
matter.

**The ordered read** found them in the first two files it opened, both in
`NEWS.md`, in the author's own words:

- *"the 2025-26 file shipped as `Enrollment_2526.zip` (capital E) versus the
  historical lowercase `enrollment_*.zip`. The fetcher now tries both."* —
  matches the catalog's `url-drift` entry for this project.
- *"NJ DOE ships the label 'Eight Grade' (sic) as a **row value** on the State
  worksheet; the existing typo fix only corrected column names, so state
  8th-grade enrollment (~100k students) silently landed in an NA-grade row for
  all 2020+ years."* — **not in the catalog's entry for this project.** A
  `corrupts` issue, scoped to 2020+ and to state rows, that went undetected
  for years and is invisible to any regex.

Both then corroborated in code, as the evidence rules require: the second at
`R/fetch_enrollment.R:57`, a five-line comment explaining it at `:76`, the
handling at `:83`, and a regression test at
`tests/testthat/test-enrollment-year-coverage.R:337`.

**The limit of this trial:** the catalog's findings had already been read
before the run, so this measures whether the procedure can locate and *cite*
real findings, not blind recall. A clean measurement needs a repository whose
answer key nobody has looked at. What it does establish is the ordering claim
— `NEWS.md` outperformed the parsing code by a wide margin, and the regex pass
was useful only for orientation.

### Second trial: walkerke/tidycensus, 2026-07-30

Run against `5461f038` — the same commit the catalog inspected, so the two
readings see identical bytes. Findings were written before the catalog entry
was opened.

The catalog carries **4** gotchas for tidycensus. The read recovered two and a
half of them and added six the catalog does not have.

**Recovered:** the API-key requirement (`credentials`), and the 90 percent
margin of error (`uncertainty`) — though only half of the latter. The
catalog's version also covers derived sums, proportions and ratios needing
distinct formulas, which lives in `R/moe.R`, a file that was listed and never
opened because `acs.R` was grepped for "moe" instead. Its documentation states
the trap outright: *"If the associated estimates are not specified, the user
risks inflating the derived margin of error in the event of multiple zero
estimates."* That is a `[practice]` with its `naive` alternative already
written, and it was missed by reading around the file rather than opening it.

**Not recovered:** `geography-vintage` / `dual-vintage` — `geometry = TRUE`
substitutes a different boundary year when the requested one is unavailable,
so one row carries an attribute vintage and a geometry vintage that differ.
The substitution is `tigris_yr <- 2010` at `R/acs.R:241`, inside a block that
had already been printed to screen and read past, because it looks like
ordinary defaulting.

**Added, with citations:**

| finding | evidence |
|---|---|
| Nine typed negative sentinels are all collapsed to `NA`, so "not applicable", "too few sample cases" and "controlled estimate" become indistinguishable | `R/acs.R:729-737` |
| Block group estimates are not published for the 2008-2012 ACS or earlier — a structural gap, not a fetch failure | `R/acs.R:231-232`, with the author's own error text |
| The 2020 1-year ACS does not exist | `NEWS.md`, 1.2 |
| Decennial variable IDs are reused across the PL and DHC files and may mean different things | `NEWS.md`, 1.4 |
| Some decennial endpoints return state-prefixed ZCTA GEOIDs, breaking joins | `NEWS.md`, 1.8 |
| 1990 and 2000 SF3 endpoints were withdrawn by Census and later partly restored | `NEWS.md`, 0.10.2 and 0.11 |

The sentinel finding is the notable one: aquifer's own `acs-5year.md` page
carries `jam-values-are-typed-states`, so the *dataset* is documented — but
nothing recorded that this widely used client erases the distinction. That is
precisely the gap between a page about a dataset and a note about an
implementation, and it argues again for keeping the two separable.

**Contamination:** all 105 `ergo_implication` strings had been read earlier in
the session, unattributed, so the *kinds* of finding in the key were known
even though their assignment was not. That the two geometry-vintage findings
were still missed suggests the foreknowledge did little work.

**Fed back into the skill:** open the file named after the concept rather than
grepping the entry point for its keyword, and follow integration seams where a
library joins two sources.

### Third trial: ivelasq/leaidr, 2026-07-30 — clean

The only run where the catalog entry had never been seen in any form.
Findings were written to a file before it was opened. Same commit as the
catalog inspected, `66e91d0`.

**Both of the catalog's two entries were recovered**, one of them reframed:

- `republisher-auth` — matched, and split into its two constituent facts with
  citations: the state files come from `github.com/datalorax/us-district-shapefiles`
  (`R/lea_get.R:18`) and the national file from a GitHub release asset in the
  maintainer's own repository, with no NCES URL anywhere in the code; and the
  README requires a `GITHUB_PAT` to fetch public federal geography.
- `stale-snapshot` — reached from a different direction. The catalog frames it
  as maintenance ("not pushed since 2021"); the read framed it as vintage
  invisibility: the edition is SY 2018-19 / TIGER-Line 2019, and it appears
  only inside a hardcoded filename at `R/lea_prep.R:21` and one README
  sentence. Nothing in the returned object carries a year.

**Eight findings the catalog does not have**, including three that would
change what someone does:

- The shapefiles carry an unrecognized datum. The author's own README example
  output shows `Discarded datum D_unknown in CRS definition: +proj=longlat
  +ellps=GRS80 +no_defs` — the CRS degrades on read, which matters for any
  area or distance calculation.
- `lea_prep()` reads `schooldistrict_sy1819_tl19.shp`, which **neither**
  `lea_get()` path produces — the state path writes `<fip>.shp` to a temp
  directory, the national path loads an `.rda`.
- Four files per state are fetched with `download.file` and no status check
  (`R/lea_get.R:56-63`), so a 404 writes an HTML page into `47.shp` and
  surfaces later as an unrelated read error.

Plus: LEAID is never exposed for filtering though the README calls joining on
it the point of the dataset; the state lookup omits the Northern Mariana
Islands; a bare numeric state argument loses its leading zero and builds
`6.shp`; `lea_prep()`'s filter branch returns invisibly; and `rgdal`/`sp`
were retired from CRAN, so the package no longer installs.

**Contamination, stated:** the 105 unattributed implication strings read
earlier included both of this project's. The citations are independent, but
the *shape* of those two findings was in the session.

**Fed back into the skill:** rendered example output in a README is a fixture
in disguise — the warnings in a shown console block are what the data did on
the author's machine, and here they were the only evidence of the datum defect
anywhere in the repository. And two implementation facts are worth carrying
every time, because they decide whether to use the thing at all: what edition
of the source it actually serves, and whether it is still maintained. Ergo has
nowhere to put either, which is a third argument for the `[reference]` kind in
§2 — the catalog's `implementation_projects` block already has `version` and
`maintenance` fields for exactly this.

### Why this is the bootstrap

It inverts the contribution request. Instead of *please write documentation
for a dataset*, it is *run this on your repository and review what it found* —
and the reviewer is reading claims about code they already understand. For the
34 of 94 sources that do have a public implementation, it pays immediately.
For the other 60 it does nothing, which is a reason to run it against every
open-source data library worth reading rather than only against one's own
work.

## 6. Versioning: four axes, one gap

An ergo page is a living record about a moving target, not a released
artifact. Advisory databases deliberately do not version records — they carry
a modification date, permanent IDs, and withdrawal states. Ergo should not
grow a page semver.

| what versions | mechanism | status |
|---|---|---|
| the format | `ergo = "0.5"` | exists |
| the directory schema | `ergo_directory = "1"` | exists |
| the dataset's vintage | issue scope (`years`, `tables`) | exists |
| **what a consumer last saw** | fetch receipt | **missing** |

The last row is the real gap. `derived_from` records an upstream URL and a
date, which is enough to *describe* a fork and not enough to *compute* one:
§10 admits divergence is untooled. The precedent is a lockfile — `Cargo.lock`,
and `flake.lock` in particular, which pins a metadata source by URL, revision,
and content hash. Adding a hash to `derived_from` makes `ergo diverge` exact:
what upstream has added since you copied, and what you hold that upstream does
not. The second half is the queue for the **Offer** step.

## 7. Carrying references into code

Anchors are how the **Implement** step pays back into the loop. Two additions,
neither of which needs new syntax:

1. **Anchor obligations follow the referent.** References share the page's ID
   namespace, so an anchor resolving to a reference is self-evidently a "see
   also". `check` requires the `handled_by` round-trip for issue anchors and
   requires nothing for reference anchors. The kind of the resolved ID
   determines the rule; the comment format is unchanged.
2. **Cite other people's code by revision.** An anchor into an external repo
   rots without a pinned commit — the reason GitHub has permalinks and Go has
   pseudo-versions. The landscape's `artifacts[]` (role, path, language) needs
   a repo and a rev to be citable at all.

And the SPDX lesson in full: the convention is worth adopting because tools
read it. `ergo scan` over a repo — *this code touches six datasets; here are
their pitfalls and the core issues you have not anchored* — is what makes a
newcomer's first encounter with ergo a read rather than a chore.

## 8. Sharing is never automatic

Two questions, and a lesson is only worth proposing if both answers are yes:

1. **Is the dataset public?** A world-true lesson about a private dataset is
   still not shareable; it leaks the data's existence and shape.
2. **Is the lesson about the world or about us?** (§1's issue-level
   authority.)

Only public-dataset × world-true is a candidate. Everything else records
locally and stays.

**The first question cannot currently be answered by a tool.** The landscape's `access.auth` has 37
distinct values across 94 sources and `access.rights` has 76 — free prose,
almost entirely unique, written to be read by a person. 75 of 94 begin with
"none", but only by string prefix, and the interesting ones are precisely the
irregular tail: *"none for public aggregates"*, *"none for documentation;
district-linked Homeroom/PIN access for records"*, *"public-use without
restriction; restricted files contain confidential details"*. Nine sources
carry FERPA, confidentiality, or explicit restriction language. Deciding this
automatically needs a short closed field — public / conditional / restricted —
declared alongside the prose rather than inferred from it. The prose stays; it
is what someone actually needs to read. The field is what a tool can act on.

The rule, because the agent is writing in the background while someone works: **draft locally, never transmit.** Silent accumulation is the
feature. Silent publication would be a breach. Offering is a distinct,
explicit, human action, and it should be batched — *you have learned six
things about three public datasets; offer any of them?* — rather than prompted
per lesson, which trains people to click through.

## What this note does not settle

- **Governance labor.** A commons needs someone to merge and to adjudicate
  disputed issue claims. That is ongoing human cost an index does not have,
  and it is the reason §10 avoided it. Sorting changes by what they claim
  reduces it; it does not remove it.
- **Whether sorted review survives agent volume.** DefinitelyTyped's process
  works against human-paced contribution. Nobody has run it against agents
  drafting during every session.
- **The measurement still owed.** ROADMAP Outcome 2's second bullet — whether
  an agent with the page avoids issues an agent without it does not — remains
  unmeasured. Everything above increases the value of a page being *found*.
  None of it is evidence that finding one helps.
- **Unowned pages and accountability.** A commons page asserting a defect in a
  government dataset has no accountable publisher. Attribution and
  `[validation]` records are the available answer; whether they are sufficient
  is untested. The 14 third-party assessments sharpen this: they name real
  maintained projects.
- **Whether retrieval custody generalizes.** The strongest signal in the diff
  comes from the one adopter built around custody. One example is not enough.
- **How much of the commons is worth building for.** 60 of 94 sources have no
  known public implementation at all. That is the argument for the pages —
  and a warning that "find an existing parser" will come back empty two times
  in three.

---

*Evidence: aquifer's 38 pages (`docs/data-sources/`) and its njschooldata
landscape catalog (`registry/njschooldata-landscape-2026-07-30.json`) — 94
sources, 44 implementations across 34 of them, 14 catalogued third-party
projects, 154 artifacts, 45 sites, 105 gotchas each with an `ergo_implication`;
both repositories private. Precedent: DefinitelyTyped's contribution and
contribution model and its hand-off to upstream;
OSV schema (`references[].type`, `affected[].ranges`, `withdrawn`) and the CVE
numbering-authority and REJECTED-state model; Homebrew taps and nixpkgs
per-package maintainers; SPDX-License-Identifier; `Cargo.lock` and `flake.lock`
as metadata pins; GitHub blob permalinks and Go pseudo-versions for citing
external code by revision.*
