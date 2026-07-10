# ergo — the data page format

**Status:** draft v0.1 · 2026-07-10
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

## 2. Definitions

- **Data page** — one markdown file conforming to this spec; the canonical
  documentation for one dataset as used by one project.
- **Dataset** — a source you ingest: an agency's published series, an API, a
  scraped corpus. Identified by a kebab-case **slug**.
- **Issue** — one discrete thing a user of the data must know: a defect, a
  trap, a definitional nuance. Identified by `<dataset-slug>/<issue-id>`.
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
— `[dataset]`, `[issue]`, `[validation]`, or `[change]` (§13).

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
- Each `[issue]` block sits **directly under the heading of its own
  section**; the prose that follows, up to the next heading of the same or
  higher level, is that issue's narrative. Structured facts go in the block;
  the story, evidence, and worked examples go in the prose. Never both —
  facts stated in the block are not restated in the prose.
- `[validation]` blocks may appear anywhere but conventionally live in a
  "Validation" section (§7); `[change]` blocks in a "Changelog" section
  (§13).
- Parsers must accept a plain ` ```toml ` fence as a fallback when the block's
  sole top-level table is `dataset`, `issue`, or `validation` — but authors
  should always write ` ```toml ergo `.

### Conformance — core format and supplemental affordances

The spec itself splits core from supplemental, so adoption never demands
the whole apparatus at once:

- **Core** (what makes a valid data page — everything `ergo check` errors
  on): the manifest with its required fields, issues with id/title/effect/
  type/status/scope, `handled_by` on mitigated issues. A repo that adopts
  only this — pages plus an occasional `check` run — is conformant.
- **Supplemental** (adopt independently, in any order): code anchors and
  the `--repo` round trip, `[validation]` records, `[change]` changelogs,
  the generated digest and agent-memory pointer, the served bundle (§8),
  `core`/`misuse`/`instead`/`detect` on issues, the skill, interop exports.

Supplemental affordances are where the compounding value is, but a page
that documents real issues with correct scopes beats a fully-instrumented
page with thin content. Start core, grow supplemental. (flip's rule again:
empty structure is worse than absent structure.)

### Recommended section arc

Not mandatory — profiles of use differ — but pages converge on:

**What it is** (orientation, why we use it) · **Access** (where it lives, how
it's fetched, URL/format quirks) · **Structure** (the shape after
normalization; format eras summarized, with the drift itself registered as
issues) · **Joins** (keys, match rates — quantify them — and join caveats by
issue reference) · **Issues** (the registry, §5) · **Validation** (§7) ·
**Provenance** (vintage, fetch history, publisher revision policy) ·
**Changelog** (dated `[change]` records, §13).

## 4. The manifest — `[dataset]`

```toml
[dataset]
ergo = "0.1"                    # format version (required)
slug = "spr"                    # kebab id, unique in the project (required)
title = "NJ School Performance Reports"          # (required)
publisher = "NJ Dept. of Education, Office of Performance Reports"  # (required)
source_url = "https://www.nj.gov/education/spr/"                    # (required)
bite = "Two graduation-rate calculations are published; only the State one has a trend — plotting Federal as a trend is the classic misread."   # (required)
status = "live"                 # live | acquiring | dormant | archived (required)
confidence = "A"                # A | B | C | ? — source reliability, flip-style
updated = "2026-07-10"          # last substantive page edit

[dataset.coverage]
years = "2015-16 → 2024-25"     # native year labels of the source
grain = "school year × entity × student group"
entities = "every NJ public school, district, and the state"

[dataset.access]
keys = ["county_code", "district_code", "school_code", "school_year"]
raw = "data/raw/spr/"           # local cache of source files
builders = ["tools/build_spr_db.py"]     # ingestion code
feeds = ["grad_rate", "assessment", "absenteeism"]  # tables/pages produced
```

Field notes:

- **`bite`** (required) — one sentence: the single thing most likely to bite
  someone who touches this data cold. It feeds the digest (§8); write it for
  a reader deciding whether they need to open the page. (After Data Is
  Plural's discipline of the one-line caveat.)
- **`confidence`** — a judgment on the *source*, using the household A/B/C/?
  scale (A authoritative primary we extracted ourselves · B official
  document, figures read directly · C reporting/secondary · ? not yet
  judged). Same scale as flip's source ledger.
- **`implementation`** (optional) — a public URL for the project's code
  (the repo). This is the one pointer a served page keeps to *our*
  implementation: everything else that names internal paths, scripts, or
  runbooks stays out of the public projection (§8).
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
| `id` | kebab-case, stable forever; renames leave a tombstone (§13) |
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
discontinued releases) · `measurement` (how the published number is
computed; what may not be recomputed or compared).

Validators warn — not error — on other values; recurring new types should be
proposed upstream (§14).

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
the manifest and `bite` never leave. Mark core sparingly — a page where
half the registry is core has no core (frank-style constitution tiers run
under 10%); the validator warns past one third.

### Optional fields

`core` (bool, above) · `discovered` (`YYYY-MM`) · `handled_by` (list of
`path` or `path#symbol` code refs, repo-relative) · `detection` (how to
spot it: a symptom, a check, a query sketch) · `misuse` (the foreseeable
misread — strongly recommended for `misleads` and `context`) · `instead`
(the sanctioned move that replaces the misuse — one line; a misuse/instead
pair is a fail/pass example, the shape LLMs follow best) · `refs` (list:
source docs, errata URLs, tickets) · `superseded_by` / `supersedes` (issue
ids, §13).

### Structured detection — `[issue.detect]` (optional)

`detection` stays prose. When the symptom is mechanically matchable, add a
`detect` sub-table so tools and agents can *look* rather than read:

```toml
[issue.detect]
regex = ['^(>|<)\d+%$', 'Fewer than 10 (students|valid scores)']  # match raw values/filenames
query = ["SELECT count(*) FROM grad_rate WHERE rate IS NULL AND raw != ''"]  # sketch, not executed in v0.1
semantic = ["a rate column parses for some rows and not others"]
```

The validator compiles each `regex` entry (an invalid pattern is an error)
and type-checks the rest; executing `query` entries is v0.2 territory
(§14). All three keys are optional lists.

## 6. Code linkage — the round trip

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

## 7. Validation — `[validation]`

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

The first is **reconciliation** (our numbers vs. an independent publication
of the same facts); the second is **confirmation** (a claim on this page,
verified against actual files, with the date and vintage). Both accumulate —
never edit an old record, add a new one. Prose context (the full
reconciliation table, say) lives in the surrounding section.

## 8. The index and the agent entry point

A directory of pages carries a generated `INDEX.md`: for each page, one row —
slug, title, status, last-updated date, issue counts by effect (core
flagged), and the `bite` line. Regenerate with `ergo digest` (§10); never
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
generated by `ergo publish` (§10) into a directory the host site serves
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

The test for what stays public is the same as §9's registry test, applied
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
   consistently carry the ergo elements — the manifest facts, the bite, the
   issue registry, the changelog — rendered from the same pages the bundle
   serves, and link to the bundle for the full machine-readable form.

This is the decentralized half of a larger shape: every publisher serves
its own bundle; a *directory of bundles* (an index of index.json URLs
across publishers) is the natural aggregation layer, kept as an open
question (§14) until more than one bundle exists in the wild.

## 9. Authoring discipline

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
- **Write for the cold reader.** No unexplained house jargon in titles,
  `bite`, or `misuse` — those travel into digests and agent contexts alone.
- **Don't pad.** A dataset with three issues has three issues. Empty
  sections and boilerplate erode the trust that makes agents load pages at
  all. (flip's rule: empty structure is worse than absent structure.)

## 10. Tooling — `ergo.py`

One stdlib-only Python file (≥ 3.11, for `tomllib`). Vendor it by copying
`tools/ergo.py` into the host repo; it carries its version in a header
comment. No install, no dependencies.

```
python3 tools/ergo.py check   [PATHS...] [--repo ROOT] [--strict]
python3 tools/ergo.py digest  [PATHS...] [--long] [--write FILE]
python3 tools/ergo.py export  [PATHS...] [--out FILE]
python3 tools/ergo.py publish [PATHS...] --dir OUT [--base-url URL]
python3 tools/ergo.py new     SLUG [--dir DIR]
```

- **check** — parses pages, enforces §§3–7: manifest first and singular,
  required fields, closed vocabularies, id uniqueness and shape, scope
  non-empty, `mitigated ⇒ handled_by`. With `--repo`: `handled_by` paths
  exist, symbols findable, anchor round trip (§6). Errors exit 1; warnings
  exit 0 unless `--strict`.
- **digest** — the `INDEX.md` markdown to stdout (or `--write`).
- **export** — everything machine-readable as one JSON document (datasets,
  issues, validations, changes, with page paths and section line numbers),
  for downstream renders and interop.
- **publish** — write the servable bundle (§8): `index.json` plus each
  page's public projection as `<slug>.md`, deterministic, into a directory
  the host site serves; warns where projected output still smells internal.
- **new** — scaffold a fresh page from the template.

## 11. Skills — teaching agents the format

The repo ships `skills/ergo/SKILL.md`, an agent skill covering both roles:

- **Consuming:** on first contact with a dataset, read the digest, then the
  page manifest and issue titles; load issue sections whose scope intersects
  the task; honor `misuse` fields when writing analysis or prose; treat
  anchors met in code as links to authority, not decoration.
- **Authoring:** on hitting an unexplained oddity, check the registry first
  (someone may have already paid for this lesson); on working around
  anything, register the issue, scope it, anchor the code, and run
  `ergo.py check` before committing.

Host projects reference or copy the skill; the two-line CLAUDE.md pointer
(§8) is what makes it fire.

## 12. Interop (generated, never canonical)

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
| `bite` + issue titles | `dct:description` (appended) | `description` | `description` |

`ergo export` emits JSON in v0.1; DCAT/Data Package/Croissant emitters are
v0.2 candidates. For variable-level semantics the mapping target is
DDI-Codebook's `<var>` (whose `<drvcmd>` — actual code attached to a derived
variable — and `<undocCod>` are the registry's closest formal ancestors);
SDMX's `OBS_STATUS` flag vocabulary (break-in-series, suppressed,
provisional, …) is prior art for the `type` taxonomy at cell grain. Nothing
in a host project may depend on an export that the page can't regenerate.

## 13. Versioning and evolution

- The manifest's `ergo = "0.1"` names the format version the page conforms
  to. Breaking format changes bump the minor pre-1.0.
- **Issue ids are permanent.** To rename: create the new id, mark the old
  entry `status = "resolved"` with `superseded_by = "new-id"`, keep its
  block (a tombstone) for one release of the page so stale anchors fail
  loudly rather than silently.
- Issue *content* evolves in place; git history is one temporal record
  (flip's rule) — but a served page (§8) reaches consumers who cannot see
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

## 14. Open questions

- **Executable detection.** `[issue.detect]` gives detection a structured
  form (compiled regexes, query sketches) but nothing runs the queries yet.
  v0.2: execute `query` entries against the host warehouse à la dbt's
  `warn_if` / pointblank's threshold tiers — a documented issue whose
  detector stops firing is either resolved or drifted, and both are worth
  knowing. Held back to keep v0.1 authorable in an afternoon.
- **Activity routing.** frank's obligation skills route by activity/pass
  (`pass_invokes`) on top of an always-loaded constitution tier. ergo's
  `core` + scope filtering is the small-registry version of the same idea;
  if hosts grow to dozens of datasets and hundreds of issues, a
  per-activity field (ingest / join / aggregate / compare-years /
  visualize / write) may earn its ceremony. Not before.
- **Taxonomy candidates.** `constraint` (restricted-vocabulary/enum rules
  on curated columns — rights gates, grade letters) came up during the
  njschooldata conversion and got shoehorned into `coding`. Needs a second
  independent example (CONTRIBUTING's bar) before joining the taxonomy.
- **Curated-internal datasets.** A knowledge layer whose source of truth is
  a seed list in the repo has no honest `source_url`. A profile for
  internally-curated datasets (publisher = the project, source = a code
  path) fit awkwardly in v0.1; consider first-classing it.
- **Cross-project issue sharing and the directory of bundles.** Two
  projects ingesting the same NJDOE files currently each carry a page. With
  bundles served over HTTP (§8), the aggregation layer becomes concrete: a
  directory that indexes many publishers' `index.json` URLs, so an agent
  asks one place "who has documented this dataset?" and fetches the
  publisher's own bundle — maintenance stays decentralized, discovery
  centralizes. An "issues-first awesome list" (the survey found none exists
  anywhere) is the low-tech first version.
- **Digest freshness enforcement.** `check` doesn't yet verify INDEX.md is
  current; regenerate-on-commit is convention. A `--check-index` flag is
  cheap if drift shows up in practice.
- **Render helpers.** Public explainer pages (the reader-facing narrative
  HTML) are renders in principle; whether ergo should ship a reference
  renderer or leave it to hosts is open.
