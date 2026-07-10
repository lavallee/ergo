# The landscape: how dataset issues get documented today

The comparative survey behind ergo's design (conducted 2026-07). Six bodies
of practice were reviewed with one question: when a dataset has a known
issue — a defect, a trap, a definitional nuance — where does that knowledge
live, and can a program (or an agent) act on it?

The short answer, everywhere: **in prose.** Every tradition surveyed has a
place to *say* "this data has problems"; none makes the individual issue a
first-class object that is scoped (which columns, which years), typed (what
kind of problem, what happens if you ignore it), versioned (is it still
true), and code-linked (where the workaround lives). ergo's issue registry
is that object; everything else in the format is inherited, gratefully, from
the traditions below.

## 1. Formal metadata standards

**DCAT / DCAT-US** (what data.gov and most open-data portals speak): strong
dataset-level identity, versioning primitives (`versionNotes`,
`previousVersion`, `DatasetSeries`), and in DCAT-US 3.0 real structured
classes — but quality content degenerates to free text (`liabilityStatement`)
and there is no column-level metadata at all. The **W3C Data Quality
Vocabulary (DQV)** adds `QualityAnnotation` and even `UserQualityFeedback` —
the closest formal class to a user-reported gotcha — as RDF that, in
practice, nobody hand-writes.

**DDI / ICPSR codebooks** (social science's tradition, the deepest of the
lot): named slots for nearly everything ergo cares about — `undocCod`
(values whose meaning is unknown), `missType` (reason for missingness),
`universe` with explicit inclusion/exclusion, dated `security`
(suppression), attributed `notes`, and — the strongest precedent found
anywhere for code linkage — `drvcmd`, the *actual SPSS/SAS syntax* attached
to a derived variable. DDI-Lifecycle's Comparison module types cross-wave
discontinuities (Commonality/Difference/graded similarity). Weaknesses:
hostile hand-authoring (abbreviated XML, ID/IDREF webs), an uncontrolled
notes taxonomy, and code linkage scoped only to derived-variable
construction, never to "this raw column is dirty, the fix is here."

**SDMX** (aggregate statistics exchange): the single best mechanism found —
`OBS_STATUS`, a closed flag vocabulary attachable at any grain from dataset
to single cell (`B` break in series, `Q` suppressed for confidentiality,
`P` provisional, `I` imputed, five distinct missingness reasons…), always
pairable with free text. A machine-filterable enum plus human elaboration,
at a chosen attachment level: ergo's `effect`/`type` + prose section is this
pattern, ported to markdown.

**CSVW**: worth stealing `null` (a list of sentinel strings meaning missing),
the `titles`/`name` split (published header vs. canonical identifier — the
misspelled-column problem, solved structurally), and dialect/schema
separation. Moribund governance, no versioned schema history, no code links.

**FAIR**: not a schema but a rubric; its follow-up literature supplies
ergo's rationale verbatim — "FAIR data are not per se high quality data,"
and unreflective reuse "may facilitate the introduction and perpetuation of
errors… because of lack of familiarity with the details and limitations of
the original study."

## 2. ML dataset documentation

**Datasheets for Datasets** established the reflection-question canon
(including "are there errors, sources of noise, or redundancies?" and
"tasks for which the dataset should not be used" — the ancestor of ergo's
`misuse`). **Google's Data Cards** added a limitations mini-schema
(type/scope/description/recommendation) and audience-tiered disclosure.
**Hugging Face dataset cards** proved the YAML-header/prose-body split at
scale — and a 7,433-card empirical study found the "Considerations for Using
the Data" section is the *least-filled* section on the Hub (2.1% of card
text): unstructured, optional caveat sections don't get written. **Croissant**
(+ its RAI extension) made dataset structure machine-loadable, but its
limitation fields are free-text strings inside a machine-readable envelope —
machine-findable, not machine-actionable. The **Data Nutrition Project**
contributed the standout idea of use-case-conditioned alerts ("safe for
trend reporting, flagged for subgroup analysis").

The ML world's verdict: naming a mandatory caveats *slot* changes behavior
even without enforcement; but across every format, the caveat content is
prose — never scoped to a column or a year, never linked to remediation
code, never versioned against releases.

## 3. Validation and data-contract tooling

Where the caveat-as-object *almost* exists — as a test. **Great
Expectations** co-locates severity + free-text `meta` with each check and
generates docs *from* the checks (docs can't drift from what's validated).
**dbt** has the richest severity model (`severity`, `warn_if`/`error_if`
thresholds, per-environment overrides) plus `store_failures` — a literal
quarantine table of known-bad rows. **pandera** (`raise_warning=True`, lazy
validation → quarantine split) and **pointblank** (fractional
warn/stop/notify thresholds; a separate "informant" for narrative metadata)
give per-check tolerance for known-dirty data. **Frictionless Data**
(datapackage.json/Table Schema, with data-journalism roots via OKFN) made
one descriptor serve as both doc and executable schema. The **data
contracts** movement (ODCS under the Linux Foundation) defines
`quality.severity` and `businessImpact` fields — present in the schema,
documented nowhere, used by no published example: the industry sees the
need and hasn't filled it.

What's missing across all of them: a *scope* ("years 2019–2021 only"), a
*reason* attached to a tolerated violation, and a pointer from the check to
the imperative transform that compensates. ergo's `detection` field stays
prose in v0.1, but the severity/threshold patterns here are the roadmap for
making it executable.

## 4. Data journalism's own culture

The content is the best anywhere; the structure is nearly absent.

- **The Quartz Guide to Bad Data**: a symptom-first troubleshooting manual
  organized by *who can fix it* (source / you / expert / programmer) — the
  responsibility axis no formal standard has.
- **The Washington Post's Fatal Force data**: epistemic status as columns —
  `race_source`, `location_precision` — per-record provenance instead of a
  prose disclaimer.
- **FiveThirtyEight × Marshall Project's police-settlements README**: the
  bluntest misuse framing in the wild ("This data should not be compared
  across cities… we don't want you to use it this way"), naming the
  foreseeable wrong conclusion rather than the abstract limitation.
- **NICAR data diaries**: the process log — what was checked, who was asked,
  what the agency said the field means — documentation of *how we know*.
- **Data Is Plural**: caveat-writing as compression; the one-sentence "here
  is the thing that will bite you," written for a reader deciding whether to
  open the data at all (ergo's required `bite` field).
- **Datasette**: metadata rendered at the point of use, and git-scraping —
  change history as a queryable record rather than a prose changelog.

Weaknesses, uniformly: no machine readability, no consistency across (or
within) newsrooms, no binding between the README's caveats and the
processing code beside it.

## 5. Government-data documentation exemplars

**IPUMS** is the structural gold standard: every harmonized variable gets
the same tabs — Description, Codes, **Comparability**, **Universe**,
Availability, Source Variables — so comparability and universe changes (the
most dangerous silent gotchas in longitudinal data) are *expected* sections,
not footnotes, and every harmonized value links back to its source variable
and original questionnaire text. **ALFRED** (St. Louis Fed) models revisions
properly: every observation carries `realtime_start`/`realtime_end`, so
"what did this number say as of last March" is a query. **Census Bureau**
errata are numbered, dated, and permalinked, and its "substantial county
change" definition is quantitative (≥ 200 people) — a falsifiable threshold
where most standards would write "significant." **BLS/BEA** name their
revision stages (advance/second/third; preliminary/benchmark).

And the negative exemplar: **open-data portals**. DCAT-US gives data.gov
the *capacity* to carry quality metadata; in practice catalog descriptions
run one truncated sentence, and the harvester is a pass-through. The
standards exist; the discipline doesn't. A format has to make the
discipline cheap.

## 6. Agent-readable documentation

The newest body of evidence, and the most directly load-bearing for ergo's
mechanics:

- **DCA-Bench**: LLM agents doing dataset QA surface only ~30% of known
  issues unaided. Pre-documented issues aren't a nicety; they're most of the
  value.
- **Context rot** (measured across 18 models): performance degrades with
  input length well below context limits, and long coherent documents fare
  *worse* than chunked material → issues must be small, independently
  loadable sections, not one long gotchas essay.
- **AGENTS.md/CLAUDE.md smell studies**: context bloat past ~200 lines,
  duplication that drifts, and "blind references" (pointers with no
  when-to-follow) are the documented failure modes → a tiny generated
  digest, one-line bites, and scope fields that say when an issue is
  relevant.
- **Agent Skills / progressive disclosure**: name + one-liner always loaded;
  the body on activation; deep references only when pointed to → ergo's
  three levels (digest → page skim → issue section).
- **llms.txt's cautionary tale**: files at well-known paths are not
  discovered passively; agents go where they're pointed → the required
  CLAUDE.md/AGENTS.md pointer, and the skill.
- **Stable greppable IDs** (session-kit pattern): a permanent ID that
  appears in the doc heading *and* in the code comment makes
  `grep <id>` return the definition and every use at once → ergo's
  anchors, validated in both directions.

## The empty quadrant

Put the six together and the shape of the gap is exact. Formal standards
have structure without issue content; ML cards have issue *slots* without
structure; validation tools have enforcement without documentation;
journalism has the content without structure; agencies have depth without
machine readability; agent-doc research has the delivery mechanics without
a domain. An issue that is **scoped + typed + versioned + code-linked** —
all four — exists in none of them. That is the object ergo's `[issue]`
block defines, and the round-trip anchor check is the mechanism that keeps
it true.

---

*Primary references: W3C DCAT 3 / DCAT-US 3.0 / DQV; DDI-Codebook 2.5 and
DDI-Lifecycle Comparison; SDMX `CL_OBS_STATUS`; W3C CSVW; Wilkinson et al.
2016 (FAIR) and critiques; Gebru et al., "Datasheets for Datasets"; Pushkarna
et al., "Data Cards"; Hugging Face dataset-card docs and the ICLR 2024
completion study (arXiv:2401.13822); MLCommons Croissant + RAI; Data
Nutrition Project; Frictionless Data specs; Great Expectations, dbt,
pandera, pointblank docs; Bitol ODCS; Quartz bad-data-guide;
washingtonpost/data-police-shootings; fivethirtyeight/police-settlements;
Cronkite data-diary curriculum; data-is-plural.com; IPUMS variable
documentation; ALFRED; Census errata and county-change documentation;
DCA-Bench (arXiv:2406.07275); Chroma "Context Rot"; "Configuration Smells in
AGENTS.md Files"; Anthropic Agent Skills engineering notes; llmstxt.org and
adoption studies. The R package* tidycensus *deserves special mention: its
margins-of-error vignette states the gotcha, quantifies it, cites the
authority, and hands over the correcting function in one place — the best
single co-location of caveat and fix found anywhere in the survey.*
