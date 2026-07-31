# Changelog

## 0.5 — 2026-07-31

The release that stops treating a data page as a description of a file and
starts treating it as the record of working with a dataset: how the bytes are
acquired, what the publisher already said about them, what other people have
already built, and which facts are the dataset's rather than yours.

**Backward compatible.** Every 0.1–0.4 page validates unchanged. Everything
here is additive; nothing new is required.


### The lifecycle a page covers

- **The four stages a page covers**, stated in §3: acquisition, parsing,
  storage, rendering. Parsing and storage were always covered; rendering was
  covered without being named (`[practice]`, `misuse`/`instead`); acquisition
  was missing entirely, and a review of one 94-source corpus found roughly a
  third of all recorded defects were defects in *fetching* rather than in the
  data.
- **Rendering is in scope; a house style is not.** A page may record that a
  rate below one percent cannot be shown without its denominator — a fact
  about the data. It may not record that your newsroom prints "<1%". The line
  is already in the format: a rendering decision is a `[practice]`, which
  requires `authority` and accepts `contested = true` so a page can carry a
  call without claiming it is the only defensible one. The spec now says no
  field should ever encode one publication's style.
- **`[dataset.acquisition]` — how anyone gets the bytes.** Optional table:
  `access`, `terms`, `credentials`, `format`, `method`, `via`, `cadence`,
  `lag`, `verification`, `size`. Distinct from `[dataset.access]`, which
  describes *this project's* pipeline and is partly stripped from the public
  projection; acquisition is public in full.
- **`access` is the one closed field, and it is required when the table is
  present.** `public` | `conditional` | `restricted`. Everything else is prose
  because 94 real sources produced 76 distinct rights statements and 37
  distinct credential descriptions — a closed vocabulary would be wrong for
  all of them. `access` is closed because a tool has to branch on it when
  deciding whether a lesson about this dataset may be offered anywhere public.
  Prose a program cannot read is the same as no answer.
- **`via` records a provenance hop.** Fetching a mirror or a re-host is not
  fetching the publisher, and the copy has its own release schedule. This came
  out of reading a package that presented itself as an NCES client and
  contained no NCES URL anywhere.
- **`acquisition` joins the recommended issue taxonomy** — filenames that
  change case, archive members that move, a landing page that stops being a
  file locator, a 200 response carrying a partial layer, a cache that outlives
  its release. Two independently read implementations produced defects of this
  shape, which is CONTRIBUTING's bar.

### What backs a page

- **§8 is now "What backs the page"** — `[quote]`, `[reference]`,
  `[validation]`: what the source says, what others have built, and what
  happened when a claim met real files.
- **`[quote]` — the source's own words, with a URL and a date.** A new block
  kind (§8, now "Evidence"): `text` verbatim, `source`, `retrieved`, optional
  `supports` (issue/practice ids, checked) and `note`. Additive and backward
  compatible — no existing page changes, nothing new is required.
- **Why it exists.** It is the way into a dataset nobody has written up, and
  it inverts the request: not *write documentation for this dataset* but *run
  this on your repository and check what it found*, where the reviewer already
  understands the code. Run against open-source data libraries, it produces
  pages about the datasets, not about the libraries.
- **`[reference]` — other people's work on this dataset.** Required `kind`,
  `url`, `observed`; optional `id` (shares the page namespace), `covers`,
  `commit`, `edition`, `maintenance`, `caveat`, `supports`. `kind` is
  recommended rather than closed — one real corpus used thirteen distinct words
  for it — while `maintenance` (`active`/`dated`/`archived`/`unknown`) is
  closed, because a consumer's behaviour branches on it. A reference naming
  code with no `commit` warns: a citation into a moving repository rots.
- **Why it exists, on three independent lines of evidence.** Most datasets have
  no page and most publishers will never write one, so the cheapest useful
  contribution a stranger can make is a pointer — a claim anyone can check by
  following the link. All three mining trials produced findings the format had
  nowhere to put: which edition of a source an implementation actually serves,
  and whether it is still maintained. Together those two decide whether anyone
  should use the thing at all.
- **`caveat` is its own field.** Everything else in a reference states that
  something exists, which is mechanically checkable; `caveat` is a judgment
  about a project someone maintains. Keeping them apart is what lets the
  checkable part be checked automatically and the contestable part be read by a
  person. A reference is explicitly not an endorsement.
- **A third `[validation]` shape: the search that came back empty.** §8 now
  shows one — *opened the non-data sheets on all ten editions; guidance found
  only in 2020-21* — because "the publisher said nothing" and "nobody looked"
  are different claims and only one is evidence. `unknowns` says where you did
  not look; a validation record says where you did and found nothing.

### Whose fact is it

- **An issue is true whether or not you exist — now enforced by giving the
  alternative a home.** §2 says so plainly, and a fact about your own handling
  gets a page of its own rather than leaking onto the publisher's.
- **`produced_from` — a page for a dataset you make rather than fetch.** A
  warehouse table, a curated seed list, a joined layer. It replaces
  `source_urls`, which such a dataset cannot honestly supply, and the page
  carries no `subject` because nobody else publishes it — so `ergo directory`
  leaves it out instead of emitting an entry nobody could match, and the
  no-subject warning no longer fires on a page that correctly has none.
- **`about = "handling"` — the narrow escape hatch.** For a fact about your own
  handling where a produced-dataset page is more ceremony than it is worth.
  Two things follow from the label, which is the whole point of it: `publish`
  reports every `handling` issue that reaches the public projection, because
  someone else's copy is not handled the way yours is; and `check` warns when
  more than a third of a page's issues carry it, since a page mostly about
  your pipeline is a page about your pipeline.
- **§6 says what to do when a constraint really is scoped.** Practices still
  take no `scope` table, but the reason is now stated positively: in a
  long series a publisher's caution lands on one edition, and *the scoped thing
  is an issue* — `effect = "misleads"`, `type = "measurement"`, scope on the
  year, with a `misuse` and an `instead`. A practice that needs its own rule
  then `addresses` that issue. A renderer reads the issue's scope to know which
  point in a ten-point series to flag; putting scope on the practice would
  duplicate the machinery and split one fact across two blocks.
- **§16 loses a question.** Curated-internal datasets are settled. What stays
  open is narrower: whether a produced page should state which of its
  upstream's issues it inherits, rather than making a reader follow
  `produced_from` and work it out.

### Starting from code that already works

- **`ergo scan` — read a page out of code that already works.** Eleven signals
  over tracked source files: sentinel comparisons, null filling, year-keyed
  parser branches, column rename maps, sheet and header offsets, fixed-width
  layouts, identifier padding, encoding fallbacks, parse guards, hardcoded
  source URLs, and `HACK`/`FIXME`/`GOTCHA` comments. Lines already carrying an
  anchor, or sitting just under one, are skipped as documented. `--json` for
  agents.
- **A scan hit is a workaround, not a defect.** A `fillna(0)` proves someone
  chose to fill nulls; it does not prove the publisher writes nulls meaning
  zero. The output is a worklist, never a page: the code proves `handled_by`
  and `discovered`, and everything else stays a hypothesis under
  `confidence = "?"` until a `[validation]` record says otherwise. Both the
  command's own output and the skill say so, because the failure mode here is
  a fluent draft that reads like documentation.
- **`skills/ergo/reading-implementations.md` — the procedure `scan` cannot be.**
  Loaded on demand: read tests and fixtures first, then NEWS/CHANGELOG,
  then long comments, then docs, then the tracker, and the parsing code
  *sixth*; cluster scattered sites into single issues; sort each finding
  between the data, a practice, and the library's own behavior; cite a
  `file:line` or a commit for every issue or delete it. `scan` is restated as
  a pre-pass throughout — eleven regexes find places to look, and nothing more.
  Two rules came from the trials rather than from design: open the file named
  after the concept instead of grepping the entry point for its keyword, and
  follow integration seams, where a library joining two sources substitutes a
  vintage and leaves two clocks in one row.
- **Measured three times, against a hand-built reference catalog.** On
  `almartin82/njschooldata@9c34401` the regex pass returned 17 candidates over
  the enrollment sources and missed both findings that mattered, while the
  ordered read found them in `NEWS.md` — one matching the catalog and one
  absent from it: NJ DOE ships "Eight Grade" (sic) as a *row value*, so ~100k
  state 8th-graders landed in an NA-grade row for every year from 2020. On
  `walkerke/tidycensus@5461f038`, the same commit the catalog inspected, the
  read recovered 2½ of its 4 entries and added 6 with citations — among them
  that nine typed ACS sentinels are collapsed to a single `NA`, so "not
  applicable", "too few sample cases" and "controlled estimate" become
  indistinguishable. On `ivelasq/leaidr@66e91d0` — the one run where the
  answer key had never been seen in any form — both of its entries were
  recovered and eight were added, among them a datum discarded on read,
  visible only in the README's own example output. All three runs, their
  misses, and their contamination limits are in `docs/distribution.md`.

### What the words are for

- **Principle 11: look for what the publisher already said.** Agencies put
  their cautions in places that are not data — a notes tab, a readme sheet, a
  cover page, a legend — and they add them precisely in the editions where
  something went wrong, which is when a process that reads only values is least
  likely to look. Go read them, quote them, and record where you looked and
  found nothing. Prompted by a field report from an education pilot that lost a
  day to an NDOE workbook tab titled "Important 2020-2021 Notes - Please Read
  Before Using Data in this Database".
- **The prose has a stated job now** (§3). Nobody reads a page top to bottom;
  an agent shows one paragraph of it to someone. So the narrative is evidence,
  not explanation — figures, filenames, dates, examples, and the publisher's
  own words — and where the source already says it, quote rather than restate.
- **Plainer language in the spec.** Four coinages removed: a practice
  "deserves" rather than "earns" its block, a field "may be worth its cost"
  rather than "earn its ceremony", `authority = "publisher"` is "the case that
  matters most" rather than "load-bearing", and a profile is given rather than
  something being "first-classed". Invented process vocabulary costs a reader
  — human or model — a definition, for nothing. Same reasoning as 0.4's
  `bite` → `pitfall`.

### Positioning and docs

- **README and VISION lead with the work, not the format.** *ergo helps you and
  your agents work around data pitfalls, and share what you've learned* — then
  the loop, then the way into a dataset with no documentation, then what
  actually gets written down. VISION gains a fourth strategy bet: capture
  happens at the moment of learning, which is why the skill rather than the
  format is what gets adopted, and restates the canonical-artifact bet on
  grounds that survive nobody reading these files by hand.
- **A design note on discovery and distribution**, `docs/distribution.md`:
  who actually writes and reads these files, why most contributions will be
  about datasets nobody owns, what a registry should look like (with
  precedent from DefinitelyTyped, OSV/CVE, Homebrew, SPDX), and a field-by-field
  diff against a 94-source catalog built independently of ergo. Nothing there
  is specified yet.
- **A documentation site**, in `website/`, published to GitHub Pages by
  `.github/workflows/pages.yml`. Five routes: the argument, a walkthrough of
  one page being built, the format map, the repository's example page rendered
  from its own export, and a start guide.
- **The site's facts are derived, and drift fails the build.** `website/build.py`
  runs the real `tools/ergo.py` against a scratch project to generate every
  frame of the walkthrough, imports the validator's own vocabularies and
  cross-checks them against SPEC.md, parses the spec's section anchors, reads
  the command list out of `--help`, and runs the test suite for the count it
  quotes. A vocabulary the spec stops naming, a command that disappears, or a
  refusal that stops refusing fails the site rather than shipping stale.

## 0.4 — 2026-07-26

- **`bite` is renamed `pitfall`.** Same field, same required one sentence,
  same digest column. The old name was a coinage — a noun invented from "the
  thing that will bite you" — and it read as made-up, which is a real cost
  for a format meant to be adopted by publishers who had no hand in writing
  it. `pitfall` is the word this domain already uses.
- **Breaking, deliberately.** A page still carrying `bite` fails its check
  with an actionable message naming the rename, rather than silently passing
  under a deprecated alias. Pre-1.0 with two adopting projects is the
  cheapest this will ever be; both were migrated in the same change.

## 0.3 — 2026-07-26

Directories: how you find pages you didn't write, and how many people can
document the same dataset without anyone arbitrating.

**Backward compatible.** 0.1 and 0.2 pages validate unchanged; the one new
warning (a page with no `subject`) is a warning, not an error.

- **`subject`** (manifest, recommended) — one URL naming *what dataset this
  page is about*. Distinct from `source_urls`, which say where **you** get
  the bytes: two projects documenting the same census product through a
  mirror and an API share a `subject`. It is the identity claim directories
  cluster on, it is explicitly a best guess, and nobody assigns it.
- **`derived_from`** (manifest, optional, array of tables) — `url` and
  `retrieved` per upstream, plus an optional `note`. Several entries mean a
  merge of several upstreams. Forking a page is expected; recording the fork
  is what later lets anyone see what the upstream has added since.
- **§10, Directories.** A directory is an index of bundles at a stable URL,
  holding **no page content** — a directory that accepted content patches
  would become a fork of everything in it, and corrections would stop
  flowing to the publishers who own them. Entries carry `subject`, `bundle`,
  and optional `recognizes` signatures (publisher domain, filename glob,
  column fingerprint) so an agent holding a mystery file can still find a
  page.
  - **Directories cluster; they never decide.** Several projects documenting
    one dataset legitimately disagree about what is `core` and which
    practices apply, because their questions differ. So there is deliberately
    no precedence, no shadowing, no merge-on-read, and no cross-directory
    deduplication — every hit is returned, attributed to the directory it
    came from.
  - **Subject normalization** is specified so clustering is reproducible:
    fold the scheme to `https`, lowercase the host, drop a leading `www.`, a
    trailing slash, a trailing `index.html`/`default.aspx`, and the fragment.
    The **query string is kept** — for some publishers it carries the dataset
    identity. Exact normalized match clusters automatically; same host with a
    shared path prefix is reported as a *candidate* for a human, never merged
    silently.
  - **Multiple directories are the default assumption.** Consumers list them
    in `ergo-sources.toml`; adding one is two lines, and running your own is
    a JSON file in a git repo.
- **`ergo directory`** — new subcommand emitting this project's entries,
  with `--bundle` and `--entries-only`, so contributing to a directory is one
  command and a PR.
- Skill gains the outward lookup path (in-repo → publisher bundle →
  directories), the never-merge rule, how to add a directory, and how to fork
  a page without losing its lineage.

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

## 0.1.1 — 2026-07-22

Second-adopter dogfood amendment:

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
