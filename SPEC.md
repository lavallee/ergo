# ergo — the data page format

**Status:** draft v0.5 · 2026-07-31
**What this is:** a spec for documenting datasets the way working data
journalists actually need them documented — schema and provenance, yes, but
above all a structured, code-linked registry of the **known issues** in the
data: the misspelled columns, the suppression rules, the format drift, the
categories whose meaning quietly changed, and the social/definitional nuance
that isn't a bug but will still wreck a story.

ergo is the tooling; the **data page** is the artifact. One page per dataset:
a markdown document any human can read top to bottom, carrying embedded TOML
blocks any program (or agent) can parse without guesswork. Data + documented
caveats ⇒ justified use. Hence the name.

The format was distilled from a comparative survey of dataset-documentation
practice: formal metadata standards (DCAT, schema.org/Dataset, DDI/ICPSR
codebooks, CSVW, FAIR), ML dataset documentation (Datasheets for Datasets,
Data Cards, Hugging Face dataset cards, Croissant/Croissant-RAI, Data
Nutrition Labels), validation and data-contract tooling (Frictionless, Great
Expectations, pandera, pointblank, dbt, ODCS), data journalism's own culture
(the Quartz bad-data guide, NICAR data diaries, newsroom data repos,
Datasette), government-data documentation exemplars (IPUMS, Census errata,
ALFRED vintages), and the emerging norms of agent-readable documentation
(skills, AGENTS.md, progressive disclosure, context budgets). See
[docs/survey.md](docs/survey.md).

The survey's one-line conclusion: **every existing format traps caveats in
prose.** None of them make an issue *scoped* (which columns, which years),
*typed* (what kind of problem, what happens if you ignore it), *versioned*
(is it still true), and *code-linked* (where is the workaround) — all four at
once. That is the quadrant ergo occupies. Agents left to rediscover dataset
issues on their own find roughly a third of them (DCA-Bench); the rest have
to be handed over, and this is the format for handing them over.

ergo is a sibling of [flip](https://github.com/lavallee/flip) (reporter's
notebooks) and shares its commitments: plain files, no services, no required
dependencies, canonical artifact with derived renders.

---

## 1. Principles

1. **The issue is the unit.** Every oddity worth knowing gets an ID, a type,
   a scope, and a home. A gotcha that lives only in a prose paragraph — or
   only in a code comment — is a gotcha the next reader re-derives the hard
   way, or worse, doesn't.
2. **One source of truth.** An issue is fully defined in exactly one place:
   its entry on the data page. Code, narrative, indexes, and renders
   *reference* the issue ID; they never restate the rule. Duplication drifts.
3. **Scoped, not vibes.** The years, columns, tables, and entities an issue
   affects are machine-readable fields, not adjectives. "Some years are
   affected" is a bug report, not documentation.
4. **Co-locate the caveat and the fix.** Every mitigated issue points at the
   code that handles it (`handled_by`), and the code points back with a
   greppable anchor comment (`ergo: <dataset>/<issue-id>`). The validator
   enforces the round trip.
5. **Name the misuse.** The most valuable caveat names the *foreseeable
   misread*: "don't plot the Federal rate as a trend — it has one point."
   Data journalism's contribution to documentation is skepticism with a
   target; the `misuse` field is its slot.
6. **Social context is data too.** Definitional and institutional nuance —
   what a "census designated place" is, why charter schools share a
   pseudo-county — belongs in the registry with `effect = "context"`, not in
   an appendix nobody loads. It is not strictly a technical problem; it is
   still a way to be wrong.
7. **Human page, machine registry, one artifact.** The page reads as a
   reporter's notebook; the embedded TOML blocks *are* the registry. Machine
   views (JSON, index digests, public explainers, interop exports) are
   generated from the page, never authored separately.
8. **Plain files, stdlib parsing.** Markdown + TOML. Readable with `less`,
   diffable with `git`, parseable with Python ≥ 3.11's `tomllib` alone. The
   validator is one file you can vendor into a zero-dependency repo.
9. **Validation is documentation.** "How we checked the work" — extracted
   figures reconciled against independently published ones, dated
   confirmations from real files — is a first-class section, because a caveat
   you haven't tested is a hypothesis.
10. **Render, don't fork.** Public-facing explainer pages, catalog metadata
    (DCAT, Data Package, Croissant), and agent digests are derived from the
    page. Edits flow back to the page, never directly to a render.
11. **Look for what the publisher already said.** Agencies put their cautions
    in places that are not data: a readme sheet, a cover page, a legend, a
    technical guide, an introduction, a notes tab. They add them *precisely in
    the editions where something went wrong* — a pandemic year, a waiver, a
    methodology change — which is when a process that only reads the data is
    least likely to look. Go and read them, quote them (§8), and record where
    you looked and found nothing, because "the publisher was silent" and
    "nobody checked" are different claims.

## 2. Definitions

- **Data page** — one markdown file conforming to this spec; the canonical
  documentation for one dataset as used by one project.
- **Dataset** — a source you ingest: an agency's published series, an API, a
  scraped corpus. Identified by a kebab-case **slug**.
- **Issue** — one discrete thing a user of the data must know: a defect, a
  trap, a definitional nuance. Identified by `<dataset-slug>/<issue-id>`.
  **An issue is true whether or not you exist.** A fact about how your project
  handles the data is not an issue about the data; it belongs on the page for
  the dataset your project produces (below), or, where that is more ceremony
  than it is worth, is marked `about = "handling"` (§5).
- **Produced dataset** — a dataset this project makes rather than fetches: a
  warehouse table, a curated seed list, a joined layer. It has a page like any
  other, but declares `produced_from` instead of `source_urls` (§4), because
  there is no publisher and no URL to be honest about.
- **Anchor** — the comment `ergo: <dataset-slug>/<issue-id>` placed in code
  that implements an issue's workaround.
- **Manifest** — the `[dataset]` TOML block at the top of a page.
- **Digest** — the generated one-line-per-dataset index that serves as the
  agent entry point.
- **Render** — any artifact generated from pages (JSON export, digest,
  public explainer, catalog record).

## 3. The data page

One file per dataset, kebab-named after the slug: `<slug>.md`. Pages live
together in one directory of the host project (conventionally `docs/data/`
or `docs/data-sources/`), alongside the generated `INDEX.md` digest.

A page is ordinary markdown with **ergo blocks**: fenced code blocks whose
info string is `toml ergo`, each containing exactly one top-level TOML table
— `[dataset]`, `[issue]`, `[practice]` (§6), `[reference]` (§8), `[quote]`
(§8), `[validation]` (§8), or `[change]` (§15).

````markdown
# NJ School Performance Reports

Reporter's notebook for the SPR dataset: where it comes from, how it joins,
and every oddity worth knowing before you trust a number.

```toml ergo
[dataset]
slug = "spr"
title = "NJ School Performance Reports"
# … (§4)
```

## What it is
…prose…

## Issues

### Rate cells are strings, with prose suppression mixed in

```toml ergo
[issue]
id = "rate-prose-suppression"
# … (§5)
```

…the story, the examples, the numbers…
````

Rules:

- The **first** ergo block on the page must be the `[dataset]` manifest.
- Each `[issue]` and `[practice]` block sits **directly under the heading of
  its own section**; the prose that follows, up to the next heading of the
  same or higher level, is that entry's narrative. Structured facts go in the
  block; the story, evidence, and worked examples go in the prose. Never both
  — facts stated in the block are not restated in the prose.
- `[reference]`, `[quote]` and `[validation]` blocks may appear anywhere. A
  quote belongs
  beside whatever it backs — under the issue it evidences, or in the section
  whose claim it settles; validations conventionally live in a "Validation"
  section (§8) and `[change]` blocks in a "Changelog" section (§15).
- Parsers must accept a plain ` ```toml ` fence as a fallback when the block's
  sole top-level table is `dataset`, `issue`, `practice`, `reference`,
  `quote`, or `validation` — but authors should always write ` ```toml ergo `.

### Conformance — core format and supplemental affordances

The spec itself splits core from supplemental, so adoption never demands
the whole apparatus at once:

- **Core** (what makes a valid data page — everything `ergo check` errors
  on): the manifest with its required fields, issues with id/title/effect/
  type/status/scope, `handled_by` on mitigated issues. A repo that adopts
  only this — pages plus an occasional `check` run — is conformant.
- **Supplemental** (adopt independently, in any order): code anchors and
  the `--repo` round trip, `[practice]` entries (§6), `[reference]`,
  `[quote]` and `[validation]` records (§8),
  `[change]` changelogs, the generated digest and agent-memory pointer, the
  served bundle (§9), `missingness`/`unknowns`/`version` on the manifest,
  `core`/`misuse`/`instead`/`detect` on issues, the skill, interop exports.

Supplemental affordances are where the compounding value is, but a page
that documents real issues with correct scopes beats a fully-instrumented
page with thin content. Start core, grow supplemental. (flip's rule again:
empty structure is worse than absent structure.)

### What the prose is for

Assume the page is read by an agent and shown to a person a paragraph at a
time. Almost nobody opens the whole file, and almost nobody writes one by
hand. That does not make the narrative worthless — it changes its job. The
prose is not an explanation of the dataset; it is the **evidence** a later
reader needs to check a claim, or to repeat it accurately to someone else.

Three consequences for how it is written:

- **Prefer what can be quoted back.** A number, a filename, a date, a row
  count, a verbatim sentence from the publisher. These survive being pulled
  out of context. General explanation does not, and it is the part a reader
  can reconstruct without you.
- **Where the publisher already says it, quote them** — `[quote]` (§8) —
  rather than restating it in your own words. Restatement is where a caveat
  quietly becomes something the publisher never said, and that failure is
  much likelier when the page is being drafted by a model that is fluent
  regardless of whether it checked.
- **Do not restate the block.** Facts belong in the TOML once. The prose
  carries what the block cannot hold: how it was found, the example that
  shows it, the figure that lets the next person confirm it still happens.

### The stages a page covers

A dataset is worked with in four stages, and a page has something to say about
each:

| stage | the question | where it lands |
|---|---|---|
| **acquisition** | how do I get the bytes, and how do I know I got them? | `[dataset.acquisition]` (§4); issues typed `acquisition` or `availability` |
| **parsing** | what do the bytes mean once read? | most of the issue registry — `format`, `coding`, `entry`, `suppression`, `identity` |
| **storage** | what is kept, at what grain, and what is now derived? | `[dataset.coverage]`, `keys`, `missingness`; issues typed `revision`, `measurement` |
| **rendering** | what may be computed and said from it? | `[practice]` (§6), and `misuse`/`instead` on issues |

Acquisition is the stage most documentation skips and the one that breaks
pipelines most often — a review of one 94-source corpus found roughly a third
of all recorded defects were defects in *fetching*, not in the data.

**Rendering is in scope; a house style is not.** A page may record that a
rate below one percent cannot be shown without its denominator, because that
is a fact about the data. It may not record that *your* newsroom prints
"<1%" — that is an editorial decision, and a different desk will rightly make
it differently. The dividing line is already in the format: a rendering
decision is a `[practice]`, which requires `authority` and accepts
`contested = true` precisely so the page can carry a call without claiming it
is the only defensible one. Nothing in this spec should grow a field that
encodes one publication's style.

### Recommended section arc

Not mandatory — profiles of use differ — but pages converge on:

**What it is** (orientation, why we use it) · **Access** (where it lives, how
it's fetched, URL/format quirks) · **Structure** (the shape after
normalization; format eras summarized, with the drift itself registered as
issues) · **Joins** (keys, match rates — quantify them — and join caveats by
issue reference) · **Issues** (the registry, §5) · **Practices** (what may be
computed and how, §6) · **Validation** (§8) · **Provenance** (vintage, fetch
history, publisher revision policy) · **Changelog** (dated `[change]`
records, §15).

Quotes are not a section of their own. A `[quote]` sits wherever the words it
carries do work — a definition under **What it is**, a suppression rule under
the issue it explains, a publisher's own caveat under **Practices** where it
establishes `authority = "publisher"`.

## 4. The manifest — `[dataset]`

```toml
[dataset]
ergo = "0.3"                    # format version (required)
slug = "spr"                    # kebab id, unique in the project (required)
title = "NJ School Performance Reports"          # (required)
publisher = "NJ Dept. of Education, Office of Performance Reports"  # (required)
subject = "https://www.nj.gov/education/spr/"    # what dataset this documents — the identity claim (§11)
source_urls = ["https://www.nj.gov/education/spr/"]                 # (required; `source_url` string also accepted)
pitfall = "Two graduation-rate calculations are published; only the State one has a trend — plotting Federal as a trend is the classic misread."   # (required)
status = "live"                 # live | acquiring | dormant | archived (required)
version = "2024-25 edition"     # the source's own version/edition label, if it has one
confidence = "A"                # A | B | C | ? — source reliability, flip-style
updated = "2026-07-10"          # last substantive page edit
unknowns = [                    # where this page's knowledge stops
  "Pre-2015-16 editions have not been examined.",
]

[dataset.coverage]
years = "2015-16 → 2024-25"     # native year labels of the source
grain = "school year × entity × student group"
entities = "every NJ public school, district, and the state"

[dataset.missingness]
zero_is_missing = true          # the source writes 0 where it means "no value"
source_tokens = ["*", "N", "Fewer than 10 valid scores"]   # literals that mean "not a number"

[dataset.access]
keys = ["county_code", "district_code", "school_code", "school_year"]
raw = "data/raw/spr/"           # local cache of source files
builders = ["tools/build_spr_db.py"]     # ingestion code
feeds = ["grad_rate", "assessment", "absenteeism"]  # tables/pages produced

[dataset.acquisition]           # how ANYONE gets the bytes (optional table)
access = "public"               # public | conditional | restricted (required in this table)
terms = "Public state education records; preserve the source's own terms."
credentials = "none"            # what kind of credential, never a secret
format = "One XLSX workbook per year; ZIP before 2015-16."
method = "Published index page, then direct per-year file URLs."
cadence = "annual"
lag = "Published the autumn after the school year it describes."
verification = "Watch the index for a new workbook and record the first date seen."
size = "~330 MB at school level for the current year."
```

Field notes:

- **`pitfall`** (required) — one sentence: the single thing most likely to trip up
  someone who touches this data cold. It feeds the digest (§9); write it for
  a reader deciding whether they need to open the page. (After Data Is
  Plural's discipline of the one-line caveat.)
- **`confidence`** — a judgment on the *source*, using the household A/B/C/?
  scale (A authoritative primary we extracted ourselves · B official
  document, figures read directly · C reporting/secondary · ? not yet
  judged). Same scale as flip's source ledger.
- **`implementation`** (optional) — a public URL for the project's code
  (the repo). This is the one pointer a served page keeps to *our*
  implementation: everything else that names internal paths, scripts, or
  runbooks stays out of the public projection (§9).
- **`produced_from`** (list, required *instead of* `source_urls` when the
  dataset is one this project makes) — the upstreams it is built from, as page
  slugs in this corpus or absolute URLs for upstreams with no page here. A
  produced dataset has no publisher to name and no URL to fetch, so demanding
  `source_urls` forces an author to invent one. Such a page also has no
  `subject`: nobody else publishes this dataset, so there is nothing to cluster
  it with, and `ergo directory` leaves it out rather than emitting an entry
  that no one could match.

  This is the page that keeps source pages honest. A fact about your own
  identifiers, your own period labels, your own joined layer is a fact about
  *your* dataset — put it here, where it is true, rather than on the
  publisher's page, where it is not.

- **`source_urls`** (required) — a list. A dataset routinely has more than
  one face: FDA's adverse-event data is published both as a continuously
  refreshed dashboard and as frozen quarterly extracts, and the two return
  different counts by design. A single `source_url` string is still accepted
  and means a one-element list; new pages should use the plural.
- **`[dataset.acquisition]`** (optional table) — the acquisition stage. Not to
  be confused with `[dataset.access]` above it, which describes *this
  project's* pipeline — join keys, local cache, ingestion code — and is
  partly stripped from the public projection (§9). `acquisition` describes how
  **anyone** gets the bytes, and is public in full.

  | key | what it holds |
  |---|---|
  | `access` | **required when the table is present** — `public`, `conditional`, or `restricted` |
  | `terms` | rights, attribution, reuse limits, in prose |
  | `credentials` | what kind of credential is needed — an API key, a token, a signed agreement, `none`. **Never a secret** |
  | `format` | what actually arrives, including by era |
  | `method` | how you get it: a published index, an API, a bulk download, a scrape |
  | `via` | whose copy you are fetching, when it is not the publisher's — a mirror or re-host is a separate provenance hop and often a separate release schedule |
  | `cadence` | how often it is published |
  | `lag` | how far behind the world the data is |
  | `verification` | how you would know a new release actually landed |
  | `size` | what a consumer is committing to |

  Everything but `access` is prose, deliberately: a survey of 94 real sources
  found 76 distinct rights statements and 37 distinct credential
  descriptions, so a closed vocabulary would be wrong for all of them. The one
  exception is `access`, which is closed because a tool has to branch on it —
  it is what lets an agent decide whether a lesson about this dataset may be
  offered anywhere public (§9). "Public" prose that a program cannot read is
  the same as no answer.

- **`contribute`** (optional) — one http(s) URL where corrections to *this
  page* are accepted: an issue tracker, a repository, a mailbox. It travels
  into the served bundle and into directory entries (§10), and it is how a
  reader who finds a mistake in a page they did not write knows where to say
  so. Exactly one page has exactly one of these; see the one-home rule (§10).

- **`subject`** (recommended) — one URL naming **what dataset this page is
  about**. Distinct from `source_urls`, which say where *you* get the bytes:
  two projects documenting the same census product through a mirror and an
  API share a `subject` and differ in `source_urls`. It is the identity claim
  a directory clusters on (§11), it is explicitly a *best guess*, and nobody
  assigns it — pick the most durable public URL a reader would recognise as
  "this dataset," usually the program or product landing page. Singular by
  design; if you genuinely document two products that disagree, that is two
  pages.
- **`derived_from`** (optional, array of tables) — where this page came from,
  when a page is a remix rather than an original:

  ```toml
  [[dataset.derived_from]]
  url = "https://example.org/ergo/acs-5year.md"    # required
  retrieved = "2026-07-20"                          # required
  note = "Forked for housing questions; dropped the education issues."
  ```

  Several entries mean a merge of several upstreams. Recording lineage is
  what makes remixing safe: with a URL and a date, a reader (or later, a
  tool) can fetch the upstream and see what it has added since you forked,
  rather than discovering months later that a fork went stale. Ergo does not
  ask the upstream to cooperate and does not model relationship types — a
  URL and a date carry the weight.
- **`version`** (optional) — the *source's* own version or edition label,
  not the page's. GHCN-Daily ships `Version 3.34` and asks to be cited by
  it; IRS 990 filings carry a schema version; a survey has an edition. The
  `updated` field is a freshness signal for the page — it is not a version
  of the data, and pages that conflate the two cannot answer "which release
  did this describe?"
- **`unknowns`** (optional, list of sentences) — **where this page's
  knowledge stops.** A page records what we know; without this, silence is
  indistinguishable from a clean bill of health, and an agent cannot tell
  "no issues here" from "nobody looked." Write plainly: *"We have not
  examined the pre-2010 archive," "New codes appear in this column and we do
  not track them," "Coverage claims stop at format version 3.0."* This is
  the cheapest honesty in the format; a page with no `unknowns` is claiming
  a completeness almost nothing deserves.

### Missingness — `[dataset.missingness]` (optional)

The most common defect across surveyed government datasets is not a broken
file; it is **a zero that means "no value"** and a blank that means something
specific. FEC leaves `entity_tp` blank for paper filings, NOAA flags values
"missing presumed zero," NCHS writes zero for a county that ceased to exist,
NJDOE stored pre-2006 race counts as `0` rather than null. Four publishers,
four domains, one shape.

| key | form |
|---|---|
| `zero_is_missing` | bool — the source writes `0` where it means "no value" |
| `source_tokens` | list of the literals that mean "not a number" (`"*"`, `"N/A"`, `"Fewer than 10 valid scores"`) |

Both are page-level facts, not per-cell state. ergo says *this dataset does
this*; typing individual values is a data-plane job and out of scope (§14).
Where `zero_is_missing` is true, expect an `[issue]` carrying the detail —
the manifest flag exists so the shape is hard to miss, not to replace the
issue.
- `coverage` and `access` keys are recommended, not exhaustive; add what the
  dataset needs (`grain`, `disaggregation`, `cadence`, …). Unknown keys are
  legal everywhere in ergo blocks — validators warn on unknown *top-level*
  tables only.

## 5. The issue registry — `[issue]`

The heart of the format. One block + one prose section per issue.

```toml
[issue]
id = "rate-prose-suppression"   # kebab, unique within the page (required)
title = "Rate cells are strings carrying %, with prose suppression sentences and capped extremes mixed in"   # symptom-first one-liner (required)
effect = "breaks"               # breaks | corrupts | misleads | context (required)
type = "suppression"            # taxonomy below (required)
status = "mitigated"            # open | mitigated | resolved | monitor (required)
discovered = "2026-06"
handled_by = ["tools/build_spr_db.py#rate"]   # required when mitigated
detection = "value fails float() after stripping a trailing % — includes '>90%', '<10%', and full suppression sentences"
misuse = "Treating NULL as zero, or averaging the raw strings. Capped extremes also go NULL: fine for All Students, a real loss for small subgroups."

[issue.scope]
tables = ["grad_rate", "assessment", "absenteeism"]
columns = ["*Rate*", "*Percent*"]
years = "all"
```

### Required fields

| field | values / form |
|---|---|
| `id` | kebab-case, stable forever; renames leave a tombstone (§15) |
| `title` | one line, symptom first — what you'd notice, not the diagnosis |
| `effect` | **closed vocabulary**, below |
| `type` | recommended vocabulary, below |
| `status` | **closed vocabulary**, below |
| `scope` | sub-table; at least one key, or `all = true` |

### `effect` — what happens if you ignore it (closed)

| value | meaning |
|---|---|
| `breaks` | the pipeline fails: unparseable, unfetchable, wrong encoding |
| `corrupts` | the pipeline succeeds and the numbers are silently wrong: bad joins, zeros-as-missing, dropped rows |
| `misleads` | the numbers are faithful to the source and a natural reading of them is still wrong: two calculation methods, changed universes, incomparable categories |
| `context` | not a defect at all — institutional or definitional background you must hold to report on this data responsibly |

`breaks` announces itself; `corrupts` and `misleads` are the dangerous ones;
`context` is the one only a human (or a well-documented page) will ever tell
you. Validators reject values outside this list.

### `type` — what kind of problem (recommended)

`definitional` (a label's meaning differs from the natural reading, or
carries institutional judgment) · `universe` (who is counted changed) ·
`coverage` (systematic exclusions or gaps) · `suppression` (privacy
withholding, thresholds, capping) · `geography` (boundary or entity changes
across time) · `revision` (published values change after release; vintages)
· `coding` (category schemes added/removed/restructured) · `format`
(container, layout, encoding drift) · `entry` (mis-entered or
anomalous-but-faithfully-reported values) · `linkage` (crosswalk/join
failures between sources) · `uncertainty` (sampling error, margins of error,
disclosure-avoidance noise) · `availability` (access quirks, URL weirdness,
discontinued releases) · `acquisition` (defects in *getting* the bytes:
filenames that change case, archives whose member names move, a landing page
that stops being a file locator, an API that returns a 200 with a partial
layer, a cache that outlives the release it holds) · `measurement` (how the published number is
computed; what may not be recomputed or compared) · `identity` (publisher
identifiers do not map cleanly to the consuming system) · `policy`
(interpretation depends on a publisher rule, threshold, or designation).

Validators warn — not error — on other values; recurring new types should be
proposed upstream (§16).

### `status` — is it still true (closed)

| value | meaning |
|---|---|
| `open` | known, not yet handled; approach the data with this in mind |
| `mitigated` | handled in code — `handled_by` required, anchors expected |
| `resolved` | no longer applies (publisher fixed it; era passed out of use) |
| `monitor` | not currently biting, but watch new releases for it |

`mitigated` covers *enforced invariants* as well as patched defects: a
design guarantee (a CHECK constraint, a rebuild-from-source rule) that
actively holds a `context` issue true is a mitigation, and gets anchored
like one.

Resolved issues stay on the page. They document eras of the data that still
exist in archives, and they are the record that stops issue rediscovery.

### `scope` — where it applies

At least one of: `years` (list or string in the source's native labels; or
`"all"`), `tables`, `columns` (glob patterns allowed), `rows` (a prose
predicate: "subgroups with cohort < 10"), `entities` (prose: "charter
schools"), or `all = true`. Scope is what lets an agent ask *does this issue
touch the slice I'm using?* without an LLM call.

### Core issues — `core = true`

Most issues are **supplemental**: they matter when a task's scope touches
theirs, and an agent filters them by `scope`. A few are **core**: they must
be loaded before *any* contact with the dataset, whatever the slice —
usually because exposure is universal (a suppression regime across every
rate column) or because one misread poisons published work. Mark those
`core = true`.

Semantics for consumers: read every core issue before touching the data;
filter the rest by scope. Under context pressure, degrade in this order:
supplemental issues to their one-line titles first, core issues stay whole,
the manifest and `pitfall` never leave. Mark core sparingly — a page where
half the registry is core has no core (frank-style constitution tiers run
under 10%); the validator warns past one third.

### Optional fields

`about` (`data` — the default — or `handling`; see below) · `core` (bool,
above) · `discovered` (`YYYY-MM`) · `handled_by` (list of
`path` or `path#symbol` code refs, repo-relative) · `detection` (how to
spot it: a symptom, a check, a query sketch) · `misuse` (the foreseeable
misread — strongly recommended for `misleads` and `context`) · `instead`
(the sanctioned move that replaces the misuse — one line; a misuse/instead
pair is a fail/pass example, the shape LLMs follow best) · `refs` (list:
source docs, errata URLs, tickets) · `superseded_by` / `supersedes` (issue
ids, §15).

### `about` — whose fact is this (closed)

Defaults to `data` and is normally omitted. `about = "handling"` marks an
issue that is really about **your project's handling** rather than about the
dataset — the one deliberate exception to §2's rule that an issue is true
whether or not you exist.

It exists because the alternative is worse. Without it, a fact about your own
canonical identifiers has two homes: a page for the produced dataset that may
not otherwise be worth writing, or, in practice, the publisher's page, where
it is simply false. The escape hatch keeps such a fact visible and labelled
rather than disguised.

Two things follow from the label, which is the point of having it:

- `ergo publish` (§9) reports every `handling` issue that reaches the public
  projection. Someone else's copy of this dataset is not handled the way yours
  is, so shipping the fact to them is at best noise. Move it to the produced
  dataset's page, or wrap its section in `ergo:internal` markers.
- `check` warns when more than a third of a page's issues are `handling`. A
  page that is mostly about your pipeline is a page about your pipeline; give
  the produced dataset its own page (`produced_from`, §4).

Use it sparingly and prefer the produced-dataset page. A registry where the
label is common has stopped describing a dataset.

### Structured detection — `[issue.detect]` (optional)

`detection` stays prose. When the symptom is mechanically matchable, add a
`detect` sub-table so tools and agents can *look* rather than read:

```toml
[issue.detect]
regex = ['^(>|<)\d+%$', 'Fewer than 10 (students|valid scores)']  # match raw values/filenames
query = ["SELECT count(*) FROM grad_rate WHERE rate IS NULL AND raw != ''"]  # sketch, not executed yet
semantic = ["a rate column parses for some rows and not others"]
```

The validator compiles each `regex` entry (an invalid pattern is an error)
and type-checks the rest; executing `query` entries is later territory
(§16). All three keys are optional lists.

## 6. The practice registry — `[practice]`

An issue is a **defect**: something true about the data whether or not you
exist. A practice is a **handling**: a decision about what may be computed
from the data, and how. Both belong on the page; conflating them costs
readers the ability to tell what they may argue with.

Two tests, and they disagree usefully:

- **Deletion.** Would this still be true if we deleted all our code?
  Yes → issue. No → practice.
- **Disagreement.** Could a competent team look at the same data and rightly
  decide otherwise? Yes → practice, and say so with `contested`.

The second catches what the first misses. *"Blank `entity_tp` means a paper
filing"* survives deleting our code and no competent team disagrees — issue.
*"We don't fold a donor's LLCs under the person"* has no code to delete and
reasonable people differ — practice.

### Why this is a separate block

Because the cardinality differs. One defect can have several handlings,
selected by the question being asked. Conduit contributions are double-counted
in FEC data — one issue — but for a committee topline you exclude the memo
lines, and to list the individual donors behind that money you do the
opposite and drop the conduit's single large check. No `[issue]` can carry
two opposite handlings, and `instead` is one line.

The reverse also happens: a practice with **no** defect underneath it. Total
receipts is not a defective field; it is a correct field that answers a
different question than "how much did they raise from donors?" Filing that as
an issue mislabels clean data as broken.

```toml ergo
[practice]
id = "raised-from-donors"       # kebab; shares the page's id namespace with issues (required)
title = "Raised from donors is individual contributions, not total receipts"  # (required)
question = "How much has this candidate raised?"   # the task this serves (required)
authority = "project"           # publisher | project | community (required)
rule = "Use ttl_indiv_contrib from the candidate summary."   # (required)
because = "Reporting receipts as 'raised from supporters' credits donors with money that came from the candidate's own pocket or another committee."   # (required)
naive = "ttl_receipts, which folds in the candidate's own money, loans, and inter-committee transfers."
addresses = ["itemization-threshold-200"]     # issue ids this practice answers
implemented_by = ["queries/candidate_summary.sql#raised"]
```

### Required fields

| field | values / form |
|---|---|
| `id` | kebab-case, unique across issues *and* practices on the page |
| `title` | one line, stating the rule's conclusion |
| `question` | the task this serves — practices are found by what you're computing, not by what's broken |
| `authority` | **closed vocabulary**, below |
| `rule` | the sanctioned move: a string, or a list of strings for an ordered procedure |
| `because` | the rationale — what lets a future reader overrule this honestly |

### `authority` — who decided (closed)

| value | meaning | if you disagree |
|---|---|---|
| `publisher` | sanctioned upstream; part of what the data *is* | you are departing from the published definition — say so loudly |
| `project` | our editorial call | reasonable people differ; `contested` and `because` carry the argument |
| `community` | convention among practitioners, no upstream blessing | the weakest claim; cite who else does it |

Authority is not severity. The useful question is not *how bad is this* but
*who says so, and in what register* — the distinction the GTFS validator
draws by deriving ERROR from "must" and WARNING from "should" in its own
specification.

`authority = "publisher"` is the case that matters most: it tells a reader **do
not re-litigate this**. NOAA's precedence order for resolving duplicate
station-days is a normalization practice we inherit, not one we chose.

### `naive` — the move this replaces

Strongly expected, and it is the honesty check. If there is no plausible
wrong move a competent person would make instead, this is documentation, not
a practice — write it in the narrative. A practice deserves its own block when
getting it wrong produces a wrong published number. The validator warns on a
practice with no `naive`.

### Optional fields

| field | holds |
|---|---|
| `stops_at` | where **our** automation stops and a human takes over — the recoverable boundary |
| `irreversible` | what was decided upstream and which input no longer exists — the *un*recoverable case |
| `residual` | the error we accept, **and its direction** |
| `because_not` | the rationale for a road not taken, and what it cost |
| `contested` | bool — reasonable teams differ. Independent of `authority` |
| `addresses` | issue ids on this page that this practice answers (validated) |
| `implemented_by` | code refs, same form and anchor round trip as `handled_by` (§7) |

`stops_at` and `irreversible` are different situations and a consumer acts
differently on each. Compare:

```toml
# recoverable — go look at the candidates view
stops_at = "Exact normalized match only. Near-miss names (trigram >= 0.5, same ZIP) surface in a candidates view for a person to judge — never merged silently."

# unrecoverable — nothing to look at, ever
irreversible = "NCHS bridges multiple-race decedents to one category before publication. The multi-race response is not in the public data and cannot be recovered."
```

`residual` exists because `status = "mitigated"` on an issue implies the
problem went away, and it usually hasn't — it was traded for a smaller one.
Name the trade and its direction: *"we would rather fuse two real donors than
undercount one, and we show each person's reported employers so a fusion is
detectable."*

`because_not` holds the expensive knowledge: *"employer and occupation are
deliberately excluded from the key — hashing them in split one real megadonor
into several keys and undercounted them."* That is an experiment someone
actually ran, and it is the first thing a well-meaning successor will redo.

### When the rule is "don't"

Prohibitions are a common shape, especially in health and safety data, and
they fit without a schema change — `rule` states the prohibition, `naive`
names the computation being forbidden:

```toml ergo
[practice]
id = "no-incidence-rates"
title = "Report counts cannot be turned into occurrence rates"
question = "How often does this adverse event happen?"
authority = "publisher"
rule = "Do not compute incidence or occurrence rates from these reports. Report counts of reports, described as reports."
naive = "Dividing report counts by prescription or exposure volume to get a rate."
because = "The publisher states the data cannot estimate incidence: causality is unproven, reporting is voluntary and incomplete, volume moves with publicity, and duplicates are unremoved."
addresses = ["duplicate-reports", "no-denominator"]
```

`implemented_by` is legitimately absent here — a prohibition has nothing to
implement — and the validator does not ask for it.

### Scope note

Practices take no `scope` table. An issue needs scope because a consumer must
ask *does this touch my slice?*; a practice is reached through `question`,
which is the task, not the data.

**When the constraint really is scoped, the scoped thing is an issue.** This
comes up in long series, where a publisher's caution lands on one edition out
of many. Take NJDOE's note that pandemic-year discipline counts are not
comparable to adjacent years: the durable fact is that one edition's data
means something different, which is an `[issue]` with `effect = "misleads"`,
`type = "measurement"`, `[issue.scope] years = ["2020-21"]`, a `misuse` of
plotting a trend straight through it, and an `instead` that breaks the series.
Quote the publisher on it (§8). *Then*, if a particular question needs a rule
of its own, write a practice that `addresses` that issue.

Composed that way a renderer gets what it needs mechanically — it reads the
issue's scope to know which point in a ten-point series to flag — and the
prohibition still has a home. Putting scope on the practice instead would
duplicate the machinery and split one fact across two blocks. If you find a
practice that is genuinely edition-specific and has **no** issue underneath
it, that is the counterexample this rule wants to hear about (§16).

## 7. Code linkage — the round trip

Documentation that doesn't know where its workaround lives goes stale;
workaround code that doesn't name its issue gets "cleaned up." ergo binds
them both ways:

- **Page → code:** every `mitigated` issue lists `handled_by` refs. A ref is
  a repo-relative path, optionally `#symbol` (function/class name). The
  validator errors on missing paths and warns on unfindable symbols.
- **Code → page:** the handling code carries an anchor comment, matching
  `ergo:\s*<dataset-slug>/<issue-id>`, adjacent to the workaround:

  ```python
  def rate(v):
      # ergo: spr/rate-prose-suppression — non-numeric → None, capped extremes too
      ...
  ```

- **The round trip is checked.** `ergo check --repo .` scans tracked text
  files: an anchor naming an unknown issue is an **error** (the doc was
  deleted or renamed out from under the code); a mitigated issue with no
  anchor in any of its `handled_by` files is a **warning** (the code no
  longer admits what it's doing). Comments are the only place anchors
  belong — never string literals that ship.

The anchor replaces the restated rule: write `# ergo: spr/rate-prose-suppression`,
not a paragraph paraphrasing the page (principle 2). One line of *why this
looks weird* alongside the anchor is good manners; three lines is a fork.

## 8. What backs the page — `[quote]`, `[reference]`, `[validation]`

Three blocks answering three different questions, none of which requires
trusting the page's author. A `[quote]` shows what the source itself says. A
`[reference]` points at what other people have already built or written about
this dataset. A `[validation]` records what happened when a claim met real
files.

### `[quote]` — the source's own words

```toml
[quote]
text = "Because the ACS is based on a sample, estimates are subject to sampling error, which is measured by the margin of error."   # verbatim (required)
source = "https://www.census.gov/programs-surveys/acs/guidance/estimates.html"   # where it appears (required)
retrieved = "2026-07-30"        # when it was seen there (required)
supports = ["moe-required"]     # issue or practice ids this backs (optional)
note = "The publisher, not us, calls the margin the measure of the error."      # why it is here, in your words (optional)
```

| field | rule |
|---|---|
| `text` | **required** — the source's exact words. Not a summary, not a tidied version |
| `source` | **required** — one http(s) URL where those words appear |
| `retrieved` | **required** — the date they were seen there; publisher pages move and get rewritten |
| `supports` | list of ids on this page, checked by `ergo check` |
| `note` | your framing, clearly separate from the quotation |

The point is the boundary. Everything in `text` is theirs; everything in
`note` is yours; a reader can always tell which is which, and an agent asked
"what does the publisher actually say?" can answer without paraphrasing.

`retrieved` is required for the same reason `derived_from` carries a date:
agency documentation is edited without notice, and a quote with no date
cannot be re-checked, only believed.

Quote when the wording carries the weight — a definition, a suppression rule,
a stated universe, an explicit caveat, a refusal to support a comparison.
Do not quote decoration; a page that quotes everything has quoted nothing,
and the block costs more than a sentence of narrative would.

A quote is also the strongest support a `[practice]` with
`authority = "publisher"` can have (§6): it shows the decision really is
upstream rather than an inference someone drew.

### `[reference]` — other people's work on this dataset

```toml
[reference]
id = "tidycensus"               # optional; shares the page's id namespace with issues and practices
kind = "implementation"         # recommended vocabulary, below (required)
url = "https://github.com/walkerke/tidycensus"      # (required)
observed = "2026-07-31"         # when you last looked (required)
covers = "ACS 1- and 5-year detailed tables through the Census API, tidy or wide"
commit = "5461f0386f46f3ca26bb13bfb1ff37b1d9b2054e"  # pin the revision when it is code
edition = "2019 EDGE shapefiles"   # which edition of the SOURCE it serves
maintenance = "active"          # active | dated | archived | unknown (closed)
caveat = "Collapses nine typed ACS sentinels to a single NA, so 'not applicable' and 'too few sample cases' become indistinguishable."
supports = ["jam-values-typed"]    # ids on this page it bears on
```

Most datasets have no page anywhere, and most of the people who could write
one do not publish the code that would justify it. What they *can* contribute
cheaply is a pointer: someone has already parsed this, someone has already
written about it, here is where. That is a low-cost claim — anyone can check
it by following the link, and it fails loudly by rotting — which makes it the
contribution that a stranger can make first.

| field | rule |
|---|---|
| `kind` | **required** — recommended vocabulary, below |
| `url` | **required** — one http(s) URL |
| `observed` | **required** — when you looked; a pointer with no date cannot be aged out |
| `covers` | what it actually does, in one line — the field a reader scans |
| `commit` | pin the revision when the reference is code; without it the citation rots |
| `edition` | which edition of the **source** it serves, which is often not the current one |
| `maintenance` | closed vocabulary: `active`, `dated`, `archived`, `unknown` |
| `caveat` | what is wrong or limited about it — kept in its own field, see below |
| `supports` | issue or practice ids on this page |

`edition` and `maintenance` are the two fields that decide whether anyone
should use the thing at all. A wrapper around a 2019 snapshot, last touched in
2021, is right for reproducing an old analysis and wrong for current work —
and neither fact is usually visible from its own documentation.

**`caveat` is separate on purpose.** Everything else in the block states that
something exists, which anyone can verify by clicking. `caveat` is a judgment
about a project someone maintains, and its maintainers are the people most
likely to arrive with a rebuttal. Keeping the two apart lets the checkable
part be checked mechanically and the contestable part be reviewed by a person.

### `kind` — what it is (recommended)

`implementation` · `documentation` · `article` · `schema` · `discussion` ·
`dataset` · `notebook`

Recommended rather than closed. The one real corpus available used thirteen
distinct words for this, so closing the vocabulary now would close it wrong;
the validator warns on an unfamiliar value and accepts it.

### A reference is not an endorsement

A reference records that something exists and what shape it is in. It does not
say the thing is correct, and a page carrying a reference has not vouched for
it. Where you *have* judged it, say so in `caveat` and nowhere else.

Referencing an implementation you did not write is expected and encouraged:
it is how a page for a dataset nobody owns gets started. Cite the code by
permalink at a pinned commit; never copy it into the page. Their license
governs their code, not the facts about a public dataset you learned by
reading it.

### `[validation]` — dated checks against reality

Dated, methodical records that the page's claims were checked against
reality. Two shapes matter:

```toml
[validation]
date = "2026-06-14"
method = "reconciled extract against district-published figures"
result = "7/7 spot figures match within rounding (SOMSD White % 1998-99: ours 43.8, published 44)"
evidence = "soma-student-population/SOURCES.md#validation"
```

```toml
[validation]
date = "2026-06-02"
method = "confirmed from real data — 2024-25 District/State file"
result = "codes are zero-padded TEXT (county 2, district 4); join is clean with no coercion"
```

```toml
[validation]
date = "2026-07-31"
method = "opened the non-data sheets (notes, legend, cover) on all 10 editions looking for publisher guidance"
result = "guidance found only in 2020-21 (COVID caution on discipline, ELP waiver, DLM/ACCESS in-person only); the other nine editions carry no notes sheet"
```

The first is **reconciliation** (our numbers vs. an independent publication
of the same facts); the second is **confirmation** (a claim on this page,
verified against actual files, with the date and vintage). The third is a
**search that came back empty**, and it is worth recording for the same reason
the others are: "the publisher said nothing" and "nobody looked" are different
claims, and only one of them is evidence. `unknowns` on the manifest says
where you did *not* look; a validation record like this says where you did and
found nothing. Both accumulate —
never edit an old record, add a new one. Prose context (the full
reconciliation table, say) lives in the surrounding section.

## 9. The index and the agent entry point

A directory of pages carries a generated `INDEX.md`: for each page, one row —
slug, title, status, last-updated date, issue counts by effect (core
flagged), and the `pitfall` line. Regenerate with `ergo digest` (§12); never
hand-edit.

The digest exists because of a blunt finding from the survey: **agents do
not discover documentation at well-known paths; they go where they are
pointed.** So the convention has two halves:

1. Generate `INDEX.md` next to the pages.
2. Plant a pointer in the project's agent-facing memory (`CLAUDE.md`,
   `AGENTS.md`, or equivalent): where the pages live, that issues carry IDs
   anchored in code, and that `python3 tools/ergo.py check` validates the
   contract. Two or three lines; the digest and pages carry the weight.

Progressive disclosure, three levels: digest (one line per dataset) → page
manifest + issue titles (a skim) → the issue's section (full story). An
agent starting work on a dataset reads the digest, opens the page, reads
every **core** issue in full (§5), and loads supplemental issue sections as
their scopes intersect the work. Page authors keep the manifest and issue
titles carrying enough signal that the skim works; `ergo digest --long`
emits the per-page issue table (core issues flagged) for exactly this use.

### Serving — the bundle over HTTP

Pages that document *published* data should themselves be published. An
agent working outside the repo must be able to fetch the documentation from
a stable URL — not spelunk through a code host. The unit is the **bundle**,
generated by `ergo publish` (§12) into a directory the host site serves
verbatim:

```
<base>/index.json      # the directory: every dataset's manifest facts,
                       # issue list (id/title/effect/type/status/core),
                       # counts, updated date, and page URL
<base>/<slug>.md       # each data page's PUBLIC PROJECTION
```

`index.json` is the middle disclosure tier over HTTP (what the page skim is
locally); the served `.md` is the full tier. The bundle is deterministic —
same pages in, same bytes out — so it can live in generated-site output
without churn.

### The public projection

The served page is for someone **building their own implementation** on the
same dataset — its job is to spare them the pitfalls, not to document your
pipeline. `publish` therefore derives it from the canonical page by
removing internal process material:

- **Marked regions.** Wrap internal-only sections (rebuild runbooks, how
  your own surfaces consume the data, editorial leads, loading inventories)
  in markdown comments; whole lines between them are dropped:

  ```markdown
  <!-- ergo:internal -->
  ## Rebuild
  …commands, script names, local paths…
  <!-- /ergo:internal -->
  ```

- **Repo-pointing fields.** `handled_by` (issues), `evidence`
  (validations), and `access.builders` / `access.raw` / `access.feeds`
  (manifest) are stripped from the projected blocks. A `mitigated` status
  survives — it tells a reimplementer the issue is tractable — while the
  *where* stays with the repo. The manifest's `implementation` URL is the
  sanctioned pointer for readers who want the code.
- **A smell check.** After projection, `publish` warns line-by-line where
  the output still looks internal (script invocations, tool paths, raw-
  cache paths) — wrap or reword until the warnings are gone or deliberate.

A projection is a render, not a canonical page: it is not expected to
re-validate under `check` (a `mitigated` issue whose `handled_by` was
stripped would fail §5) — `check` governs sources, `publish` governs what
ships.

The test for what stays public is the same as §11's registry test, applied
to prose: *would this sentence help someone rebuilding from the source
files with none of our code?* Issue prose describing **what** the
workaround does ("non-numeric rate values parse to NULL") is exactly what
they need; **how we run ours** ("rerun build_x.py") is not. `check` errors
on unbalanced markers; `export` (the in-repo machine view) is never
projected.

Three rules make it findable and trustworthy:

1. **Stable base URL**, stated in the bundle itself (`base_url` in
   index.json when known) and never moved casually.
2. **Advertise, don't assume discovery.** Point to the bundle from wherever
   agents and humans already look: the site's `llms.txt` if it has one, the
   project's CLAUDE.md/AGENTS.md, and the human-facing data pages (a visible
   link plus `<link rel="alternate" type="text/markdown">` per dataset).
   The survey's llms.txt finding governs here: files at well-known paths are
   not discovered passively.
3. **Human pages render, the bundle is canonical.** Public explainer pages
   consistently carry the ergo elements — the manifest facts, the pitfall, the
   issue registry, the changelog — rendered from the same pages the bundle
   serves, and link to the bundle for the full machine-readable form.

This is the decentralized half of a larger shape: every publisher serves
its own bundle, and directories index those bundles (§10).

## 10. Directories — where pages live, and how they are found

A **directory** answers one question: *does anyone document this dataset?*
It carries an index of entries clustered by subject, and — for pages that have
nowhere else to live — the pages themselves.

Nothing here is required to use ergo. A project that documents its own
datasets and never joins a directory is unaffected by this section.

### Two kinds of entry, and why the second is the common one

| | canonical page lives | corrections go to |
|---|---|---|
| **indexed** | the publisher's own repository | that repository |
| **hosted** | this directory | this directory |

Earlier drafts of this spec allowed only the first, on the grounds that a
directory holding content would become a fork of every page in it. That
argument is sound and it is preserved below — but it defends against a
specific harm, and the harm needs somewhere else to exist. **A directory
cannot fork a page that has no other home.**

And most pages have no other home. Three things are true at once in practice:

- the dataset's publisher will not write a page — agencies do not, and will
  not;
- the projects that *do* write pages are very often private, because a data
  team's repository contains more than its documentation;
- a public bundle served from a private repository is **published but
  unpatchable**. You can fetch the page. There is nowhere to send a
  correction, no pull request to open, and no one else can ever improve it.

That third case is the one that matters, and an index alone cannot serve it.
A page nobody can patch is a document, not a commons. So the default runs the
other way from the earlier draft: **a page is canonical in the directory
unless its author can accept corrections publicly.** A public repository that
takes pull requests keeps its own page and is indexed; everyone else
contributes the page itself.

### The constraint that survives

> **One home per page.** Exactly one place holds the canonical copy and
> accepts corrections to it. A directory must never hold a second copy of a
> page that is canonical somewhere else.

That is the anti-fork rule, stated in terms of what actually goes wrong. It
forbids the directory from shadowing a maintained page; it does not forbid
the directory from being where a page lives.

A directory that hosts pages is, for those pages, **a publisher like any
other** — it serves a bundle (§9), its entries point at that bundle, and its
`contribute` names itself truthfully. No new entry field is required.

### Contributing a page from a private project

The loop for a team whose repository cannot be public:

1. Author the page privately, next to the code it describes.
2. `ergo publish` produces the public projection — internal regions and
   repo-pointing fields removed (§9).
3. Open a pull request adding that projection to the directory, which becomes
   the canonical copy.
4. Record the lineage in the local copy: `[[dataset.derived_from]]` with the
   directory's URL, the date, and the `hash` (§4).
5. `ergo diverge` (§12) then keeps the two in step — it reports what the
   canonical page has gained since you last took it, and what your local copy
   carries that the canonical one does not. The second list is what you owe
   upstream.

Step 5 is what makes this a sync rather than a hand-off. The private copy
stays the working copy; the public one stays the copy anyone can fix.

### The premise: many pages per dataset, and that is correct

At any scale, several projects will document the same dataset. A newsroom's
ACS page, a housing nonprofit's, and a state agency's will disagree — about
what is `core`, about which practices apply, about what the `pitfall` is —
because their questions differ, and a `[practice]` is by definition a
decision reasonable teams make differently (§6).

So a directory **clusters; it never decides.** It answers *who documents
this?* with an attributed list. There is deliberately no precedence, no
shadowing, no merge-on-read, and no cross-directory deduplication. Those
would impose an authority ranking that does not exist and would hide exactly
the diversity worth having.

### Clustering on `subject`

Pages declare `subject` (§4) — one URL, the author's best guess at what
dataset the page is about. To compare two subjects, normalize both: fold the
scheme to `https` (nobody means a different dataset by `http`), lowercase the
host, drop a leading `www.`, drop a trailing slash, drop a trailing
`index.`/`default.` page of any common extension (`.html`, `.htm`, `.shtml`,
`.php`, `.asp`, `.aspx`, `.jsp` — agencies use all of them for the same
landing page), drop the fragment. **Keep the query string** —
for some publishers the query *is* the dataset identity, and dropping it would
silently fuse distinct sources.

Then:

- Equal normalized subjects → the same cluster, automatically.
- Same host and a shared path prefix → a **candidate** cluster, reported for
  a human to judge, never merged silently.
- Otherwise → separate clusters.

The residual risk runs in a named direction: this will sometimes show two
clusters for one dataset, and that is the error worth accepting, because
fusing two datasets into one cluster tells a reader something false.

### The directory file

One JSON document at a stable URL.

```json
{
  "ergo_directory": "1",
  "name": "Example directory",
  "updated": "2026-07-26",
  "entries": [
    {
      "subject": "https://www.census.gov/programs-surveys/acs",
      "bundle": "https://example.org/data/ergo/",
      "slug": "acs-5year",
      "title": "ACS 5-year estimates, New Jersey",
      "publisher": "US Census Bureau",
      "updated": "2026-07-22",
      "recognizes": {
        "domains": ["census.gov"],
        "filenames": ["acs5*.csv"],
        "columns": ["GEO_ID", "NAME", "B01001_001E"]
      }
    }
  ]
}
```

`subject` and `bundle` are required per entry; the rest are conveniences
copied from the bundle so a directory can be browsed without fetching
everything it lists. `contribute` is the exception and is discussed below. They are a **cache, not a source of truth** — the
bundle wins on any disagreement.

For a hosted page the `bundle` is the directory's own served location and
`contribute` is the directory's own repository. For an indexed page both point
outward. Nothing distinguishes the two structurally, which is deliberate: a
consumer resolving a page should not have to care where it happens to live.

`recognizes` is optional and answers the harder question: an agent holding an
unfamiliar file, with no idea what it is, can match on publisher domain,
filename pattern, or column fingerprint and find a page that way. A column
fingerprint is the strongest signal for a file that arrived with no
provenance at all. Report a signature match with its basis ("matched 14 of
16 column names"); never assert identity from one silently.

### Where corrections go — `contribute`

A directory that holds no content still has to answer the question a reader
arrives with: *this page is wrong, where do I say so?*

```json
{
  "subject": "https://www.census.gov/programs-surveys/acs",
  "bundle": "https://example.org/data/ergo/",
  "contribute": "https://github.com/example/data/issues"
}
```

`contribute` is optional and copied from the page's manifest (`contribute`,
§4) like the other conveniences. What makes it worth a field of its own is the
rule it carries:

> **One home per page.** Exactly one place accepts corrections to a given
> page, and it is the place that serves the page's bytes. A directory must
> never name itself in `contribute` for a page it does not serve.

That is §10's opening constraint stated as something a maintainer can check
rather than a principle they have to remember. A directory that starts
accepting patches to other people's pages has become a fork of every page in
it; a directory that points at each publisher's own repo has not.

### Hosting a page nobody else will

The constraint above forbids a directory from patching someone else's page. It
does not forbid a directory from being the home of a page that has no other
home — and most datasets have none, because most publishers will never write
one and most of the projects that could are private.

Such an entry is not structurally special. Its `bundle` is the directory's own
serving location and its `contribute` is the directory's own repository,
because the directory really is where that page lives. The rule holds
unchanged: one home, and it is whoever serves the bytes.

What a directory must not do is hold a *second* copy of a page that already
has a home elsewhere. The test is not "does the directory store content" but
"does this page have exactly one place to correct it."

### When a publisher takes over

If a publisher starts serving their own bundle for a dataset the directory has
been hosting, the hosted page hands off: the entry's `bundle` and `contribute`
change to the publisher's, and the directory's copy is deleted rather than
kept in parallel. There is no new mechanism — it is an edit to one entry — but
it is the expected end state and worth planning for rather than discovering.

Do not keep the old copy "for reference". Two copies with one subject is the
condition this whole section exists to prevent.

### Configuring directories

Consumers list directories in `ergo-sources.toml`, in the project root or
alongside the pages:

```toml
[[source]]
name = "default"
url = "https://raw.githubusercontent.com/lavallee/ergo-directory/main/directory.json"

[[source]]
name = "my-newsroom"
url = "https://data.example-news.org/ergo/directory.json"
```

Every configured directory is queried and every hit is returned, tagged with
the directory it came from. Adding one is a two-line edit; running your own
is a JSON file in a git repo.

Resolution order for a consumer looking for documentation, cheapest first:
in-repo pages → the publisher's own bundle, if the dataset has one → the
configured directories. Stop at the first hit; the first two are free and
authoritative for the project at hand.

### Lineage and remixing

Forking someone's page is expected and encouraged — it is how a page finds
the questions it actually serves. Record it with `derived_from` (§4): the
upstream URL and the date you took it.

That record is what keeps a remix honest. With a URL, a date, and a `hash` of
the bytes you took, a reader can see what the upstream has registered since —
instead of discovering a year later that the original grew twelve issues
nobody carried across. `ergo diverge` (§12) computes it.

The `hash` is what makes the answer trustworthy rather than approximate. A
date alone cannot distinguish an upstream that never moved from one that
changed and changed back, and it cannot tell you whether the copy in front of
you is the copy that was fetched. The receipt costs one line at fork time and
is the difference between a comparison and a guess. It is a warning, not an
error, to omit it — a fork recorded without a hash is still better than a fork
recorded not at all.

## 11. Authoring discipline

- **Register at the moment of discovery.** The workaround commit and the
  issue entry are the same change. An issue discovered but not registered is
  the next agent's re-discovery (and the next reporter's error).
- **Symptom first.** Title issues by what you'd observe ("rate cells are
  strings"), not the diagnosis ("inconsistent typing") — that's how the next
  person searches. (After the Quartz guide's organization.)
- **Quantify.** "Federal rate populated in 5,423 of 27,201 trend rows" beats
  "Federal rate is mostly missing." Reconciliation tables beat "we checked."
  Numbers are what let the *next* check detect drift.
- **Name the misuse** for anything `misleads` or `context` — the wrong
  conclusion a careless-but-reasonable reader would publish.
- **Separate the data's problems from your choices.** How a chart uses the
  proposed-budget column is *your* methodology and belongs in narrative (or
  the consuming app's docs); the fact that the file mixes four budget bases
  is *the dataset's* issue and belongs in the registry. The test: would this
  still be true if we rebuilt all our tooling from scratch?
- **Read the non-data parts of every edition.** Notes sheets, readmes, cover
  pages, legends, technical guides. A workbook tab called "Important Notes —
  Please Read Before Using Data" is the publisher handing you issues already
  written; nothing in the values will tell you it exists. Do this per edition,
  not once per dataset: the year that has a notes sheet is usually the year
  that needed one.
- **Write for the cold reader.** No unexplained house jargon in titles,
  `pitfall`, or `misuse` — those travel into digests and agent contexts alone.
- **Don't pad.** A dataset with three issues has three issues. Empty
  sections and boilerplate erode the trust that makes agents load pages at
  all. (flip's rule: empty structure is worse than absent structure.)

## 12. Tooling — `ergo.py`

One stdlib-only Python file (≥ 3.11, for `tomllib`). Vendor it by copying
`tools/ergo.py` into the host repo; it carries its version in a header
comment. No install, no dependencies.

```
python3 tools/ergo.py check   [PATHS...] [--repo ROOT] [--strict] [--require-manifest]
python3 tools/ergo.py digest  [PATHS...] [--long] [--write FILE]
python3 tools/ergo.py export  [PATHS...] [--out FILE]
python3 tools/ergo.py publish [PATHS...] --dir OUT [--base-url URL]
python3 tools/ergo.py directory [PATHS...] [--bundle URL] [--entries-only]
python3 tools/ergo.py scan    [PATHS...] [--json] [--out FILE]
python3 tools/ergo.py diverge [PATHS...] [--json] [--timeout SECONDS]
python3 tools/ergo.py new     SLUG [--dir DIR]
```

- **check** — parses pages, enforces §3–7: manifest first and singular,
  required fields, closed vocabularies, id uniqueness and shape, scope
  non-empty, `mitigated ⇒ handled_by`. With `--repo`: `handled_by` paths
  exist, symbols findable, anchor round trip (§7). Errors exit 1; warnings
  exit 0 unless `--strict`. For a closed data-page corpus,
  `--require-manifest` also errors on every Markdown file except `INDEX.md`
  that contains no Ergo blocks; omit it for mixed documentation directories.
- **digest** — the `INDEX.md` markdown to stdout (or `--write`).
- **export** — everything machine-readable as one JSON document (datasets,
  issues, validations, changes, with page paths and section line numbers),
  for downstream renders and interop.
- **publish** — write the servable bundle (§9): `index.json` plus each
  page's public projection as `<slug>.md`, deterministic, into a directory
  the host site serves; warns where projected output still smells internal.
- **directory** — emits this project's entries for a directory file (§10):
  subject and its normalized form, bundle URL, and recognition signatures
  derived from the manifest. `--entries-only` gives just the array, to open
  as a PR against someone else's directory.
- **diverge** — for every page carrying `derived_from` (§4), fetch the
  upstream and answer three questions in the order they get cheaper to
  answer: has it moved at all (the `hash` receipt), what does it *say* it
  changed since you took it (its own `[change]` records dated after your
  `retrieved`), and which ids does each side carry that the other does not.
  The last list is the offer-back queue — what you learned that the upstream
  has not.

  The only command that touches the network. `http(s)://` and `file://` only,
  no auth, no retries; an upstream that cannot be read exits 1 rather than
  reporting no difference, because "unreachable" and "unchanged" must never
  look alike. It prints the upstream's current hash so you can paste it back
  into `derived_from` once you have reconciled.

  It also reports when the receipt and the upstream's changelog disagree — a
  hash claiming the upstream never moved, on a page recording changes dated
  after you took it. One of the two is wrong, and believing either silently is
  worse than saying so.
- **scan** — read code that already works with a dataset and list the places
  its author handled something: sentinel comparisons, null filling, year-keyed
  parser branches, column rename maps, sheet and header offsets, fixed-width
  layouts, identifier padding, encoding fallbacks, parse guards, hardcoded
  source URLs, and comments flagged `HACK`/`FIXME`/`GOTCHA`. Lines already
  carrying an anchor — or sitting just under one — are skipped as documented.

  This is the way into a dataset nobody has written up: a working
  implementation is a record of what its author learned, in the only notation
  they were willing to maintain. But **a hit proves a workaround exists, not
  that the reading behind it was right.** A `fillna(0)` shows someone chose to
  fill nulls; it does not show the publisher writes nulls meaning zero. Scan
  output is a worklist for an author, never a page: what it can prove goes
  straight into `handled_by` and `discovered`, and everything else stays a
  hypothesis until a `[validation]` record says otherwise. A page built this
  way carries `confidence = "?"` and an `unknowns` entry saying the code was
  read and the data was not.

  `--json` for tooling and agents. Expect `hardcoded-source-url` to be the
  noisiest signal outside an ingestion codebase, and the most useful inside
  one.
- **new** — scaffold a fresh page from the template.

## 13. Skills — teaching agents the format

The repo ships `skills/ergo/SKILL.md`, an agent skill covering both roles,
plus `skills/ergo/reading-implementations.md`, loaded on demand when
bootstrapping a page from a codebase (§12, `scan`):

- **Consuming:** on first contact with a dataset, read the digest, then the
  page manifest and issue titles; load issue sections whose scope intersects
  the task; honor `misuse` fields when writing analysis or prose; treat
  anchors met in code as links to authority, not decoration.
- **Authoring:** on hitting an unexplained oddity, check the registry first
  (someone may have already paid for this lesson); on working around
  anything, register the issue, scope it, anchor the code, and run
  `ergo.py check` before committing.

- **Reading an implementation:** when a dataset has no page anywhere but code
  in some repository already parses it, that code is a record of what its
  author learned. The reference file carries the procedure — what to read and
  in what order (tests and fixtures first, parsing code sixth), how to cluster
  scattered sites into one issue, how to sort a finding between the data, a
  practice, and the library's own behavior, and the evidence rules that keep a
  fluent draft from becoming a page.

Host projects reference or copy the skill; the two-line CLAUDE.md pointer
(§9) is what makes it fire.

## 14. Interop (generated, never canonical)

The page is canonical; catalog formats are exports. The manifest maps
losslessly onto the common standards — and the issue registry mostly maps
onto *nothing*, which is why ergo exists. Sketch:

| ergo | DCAT / schema.org | Data Package | Croissant |
|---|---|---|---|
| `slug`, `title` | `dct:identifier`, `dct:title` / `name` | `name`, `title` | `@id`, `name` |
| `publisher` | `dct:publisher` | `sources` | `creator` |
| `source_url` | `dcat:landingPage` | `homepage` | `url` |
| `coverage.years` | `dct:temporal` | — | — |
| `access.keys` | — | `schema.primaryKey` | `RecordSet.key` |
| issues (whole registry) | `dqv:QualityAnnotation` (thin) | — | `rai:dataLimitations` (prose dump) |
| `pitfall` + issue titles | `dct:description` (appended) | `description` | `description` |

`ergo export` emits JSON; DCAT/Data Package/Croissant emitters are
v0.2 candidates. For variable-level semantics the mapping target is
DDI-Codebook's `<var>` (whose `<drvcmd>` — actual code attached to a derived
variable — and `<undocCod>` are the registry's closest formal ancestors);
SDMX's `OBS_STATUS` flag vocabulary (break-in-series, suppressed,
provisional, …) is prior art for the `type` taxonomy at cell grain. Nothing
in a host project may depend on an export that the page can't regenerate.

## 15. Versioning and evolution

- The manifest's `ergo = "0.5"` names the format version the page conforms
  to. Breaking format changes bump the minor pre-1.0.
- **Issue ids are permanent.** To rename: create the new id, mark the old
  entry `status = "resolved"` with `superseded_by = "new-id"`, keep its
  block (a tombstone) for one release of the page so stale anchors fail
  loudly rather than silently.
- Issue *content* evolves in place; git history is one temporal record
  (flip's rule) — but a served page (§9) reaches consumers who cannot see
  git. The **changelog** is the versioning record that travels with the
  page:

  ```toml
  [change]
  date = "2026-07-10"
  note = "Registered pre-2006 race fields stored as 0 (not NULL) — found and verified during the ergo conversion."
  issues = ["pre-2006-race-fields-zero"]   # optional: issue ids touched
  ```

  Required: `date`, `note`. Optional: `issues` (validated against the
  page's registry). Append-only, newest last, in a "Changelog" section.
  Record what changes a consumer's picture of the dataset: a new issue, a
  status transition, a scope correction, a coverage extension. Don't record
  copyediting.
- The manifest's `updated` field is the freshness signal for served
  consumers; it must be ≥ the newest `[change]` date (the validator
  checks). Learn something new about the data → new `[change]` + bump
  `updated`, in the same edit as the issue change itself.
- Pages track the dataset relationship, not the dataset release: a new
  annual file lands as edits to coverage, new issues, new validation
  records, and a `[change]` entry — not a new page.

## 16. Open questions

- **Executable detection.** `[issue.detect]` gives detection a structured
  form (compiled regexes, query sketches) but nothing runs the queries yet.
  v0.2: execute `query` entries against the host warehouse à la dbt's
  `warn_if` / pointblank's threshold tiers — a documented issue whose
  detector stops firing is either resolved or drifted, and both are worth
  knowing. Held back to keep a page authorable in an afternoon.
- **Activity routing.** frank's obligation skills route by activity/pass
  (`pass_invokes`) on top of an always-loaded constitution tier. ergo's
  `core` + scope filtering is the small-registry version of the same idea;
  if hosts grow to dozens of datasets and hundreds of issues, a
  per-activity field (ingest / join / aggregate / compare-years /
  visualize / write) may be worth its cost. Not before.
- **Taxonomy candidates.** `constraint` (restricted-vocabulary/enum rules
  on curated columns — rights gates, grade letters) came up during the
  njschooldata conversion and got shoehorned into `coding`. Needs a second
  independent example (CONTRIBUTING's bar) before joining the taxonomy.
- **Curated-internal datasets.** *Settled:* such a dataset declares
  `produced_from` instead of `source_urls` and carries no `subject` (§4).
  What remains open is whether a produced page should be able to state which
  of its upstream's issues it inherits, rather than leaving a reader to follow
  `produced_from` and work it out.
- **A directory at more than one publisher's scale.** One exists —
  [ergo-directory](https://github.com/lavallee/ergo-directory), the default
  in `ergo-sources.toml`, with its own validator that enforces the one-home
  rule mechanically. Every entry in it today comes from a single publisher,
  so nothing has yet tested the parts a format cannot settle: who merges, who
  adjudicates a disputed issue claim, and how either survives contributions
  arriving faster than a person can read them. Those costs are real and an
  index does not have them; a second independent publisher is what would make
  them concrete rather than hypothetical.
- **Digest freshness enforcement.** `check` doesn't yet verify INDEX.md is
  current; regenerate-on-commit is convention. A `--check-index` flag is
  cheap if drift shows up in practice.
- **Render helpers.** Public explainer pages (the reader-facing narrative
  HTML) are renders in principle; whether ergo should ship a reference
  renderer or leave it to hosts is open.
