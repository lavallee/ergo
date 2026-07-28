# Design brief — the ergo site

Private working document. Artoo keeps this file outside `site/`; it is not deployed.

## Reader decision

A person who maintains a data pipeline over somebody else's published data — a
newsroom data reporter, a civic-data engineer, an analyst on a public-sector
beat — should be able to decide whether **ergo is where their dataset caveats
go from now on**, and be able to write their first page within ten minutes of
deciding yes.

The decision is small and reversible, and the site should say so: adopting ergo
is copying one file into `tools/` and writing one markdown page. It is not a
platform migration, and any page written today survives the tool being
abandoned tomorrow.

Secondary reader, served but never allowed to blur the front door: the **agent
author** wiring a coding agent into a data project, who wants to know what
lands in the model's context and how much it costs to load. The three
disclosure tiers and the `core` flag are for them.

## Headline claim

**A schema tells you what the columns are; it can't tell you which ones lie.**
ergo is a markdown format whose unit is the *issue* — one defect, trap, or
piece of definitional nuance, with a stable id, a machine-readable scope, a
typed effect, and a checked link to the code that works around it. Every
surveyed alternative traps that material in prose.

## Supported claims

Each resolves against the repository at the deployed revision; the build fails
the site rather than shipping a stale number.

- A data page is one markdown file with fenced `toml ergo` blocks in it,
  parseable by Python ≥ 3.11's stdlib alone (SPEC §3, §12).
- `effect` and `status` on issues, `authority` on practices, and `status` on
  the manifest are closed vocabularies; `type` and the scope keys are
  recommended and warn rather than error (enforced in `tools/ergo.py`, and the
  build cross-checks every value against SPEC.md).
- A scaffolded page does not validate: `publisher`, `source_urls` and
  `pitfall` are required (SPEC §4; shown as real `check` output).
- An issue with no `[issue.scope]` table is an error (SPEC §5).
- An issue typed `misleads` or `context` with no `misuse` is a warning
  (SPEC §5).
- A `mitigated` issue with no `handled_by` is an error; an anchor naming an
  unknown issue is an error; a mitigated issue with no anchor in its
  `handled_by` files is a warning (SPEC §5, §7).
- `publish` strips repo-pointing fields and internal-marked regions from the
  served projection (SPEC §9; the build asserts this on the generated bundle
  and fails if `handled_by` survives).
- The tool is one stdlib-only file with six commands, and the site's command
  list is checked against the tool's own `--help`.
- The shipped test suite passes with N named checks at the built revision.

## Unsupported claims and counter-reading

- **Thin adoption evidence.** Two projects, one of them the author's. No case
  studies, no testimonials, no "trusted by". Say two, name them, stop.
- **No effectiveness measurement.** Nothing here shows a project with data
  pages makes fewer errors than one without. The DCA-Bench ~30% figure
  (arXiv:2406.07275) measures what agents miss *unaided*; it motivates handing
  issues over and says nothing about this format being the way to do it. It
  must never be presented as an ergo result.
- **The test count is not a quality measure.** It counts named assertions in
  the shipped suite that ran and passed. Not coverage.
- **Draft spec, and it has moved.** v0.4, with a breaking rename (`bite` →
  `pitfall`) one release back.
- **Strongest counter-reading: the registry rots.** Twelve issues written in a
  burst, the dataset changes, nobody updates the page, and a reader trusts a
  stale scope — worse than nothing, because it was believed. The honest answer
  is partial and must be given as partial: the round trip catches the half that
  involves code, validation records make an untested caveat visibly untested,
  `unknowns` makes silence say something, and none of that notices a publisher
  changing something nobody looked at. The format does not detect issues. Say
  so on the home page, not in a footnote.
- **Second counter-reading: this is one team's opinion about a dataset.** True,
  and by design — a `[practice]` is a call reasonable teams make differently.
  Directories cluster and refuse to rank. The site must not imply a page is
  authoritative about a dataset.

## Data vintages and denominators

- Format version, tool version: the banner in `tools/ergo.py`; spec status
  line from `SPEC.md`; repository revision stamped at build.
- Walkthrough frames: real `ergo.py` runs against a scratch project in a temp
  directory, at build time. Vintage = the build.
- Example page figures: `ergo.py export examples/spr.md`, plus the page's own
  `check` line quoted verbatim.
- Passing checks: `python3 tests/run.py` at the built revision, counted from
  its own output. Test functions are not counted; this suite is a list of named
  assertions and that is the honest unit.

## Licit comparisons

**Valid axes** — what a maintainer is actually choosing between:

- What the artifact is *for* (discovery / description / assertion / defects).
- Where a caveat physically goes.
- Whether scope is machine-readable.
- Whether the caveat is linked to the workaround, and whether the link is
  checked.
- Whether non-executable material (definitional, institutional) has a home.

Valid comparison set: catalog metadata (DCAT, schema.org/Dataset), ML dataset
documentation (Datasheets, Croissant), validation and data-contract tooling
(Frictionless, Great Expectations, dbt), and a prose README or data diary.

**Invalid comparisons** — must not appear:

- Any ranking, score, or feature count. ergo's own §14 says catalog formats are
  export targets, not rivals; a project may need all of them.
- Implying ergo replaces validation tooling. A failing expectation and a
  documented issue are different artifacts; the site says so.
- Any performance or accuracy benchmark. None has been run.

## Selected forms

- **The walkthrough** (`walkthrough.html`) — the load-bearing interactive. A
  reporter and an agent in conversation, sixteen exchanges, every command run
  for real at build time, three of them refusals. It exists to make the
  round trip *concrete*: the abstract promise "the code and the doc cannot
  drift apart" becomes an exit code the reader watches happen. Under-the-hood
  detail is closed by default so the conversation reads as a conversation.
- **The example page** (`page.html`) — the payoff, rendered from
  `ergo.py export` over the repository's own example: manifest, pitfall, five
  issues with scopes and misuses, two practices, the validation table. The
  filter row uses the same four-colour effect scale as everything else.
- **The format map** (`format.html`) — the five blocks with their real required
  and optional keys, the vocabularies read out of the validator, and the issue
  lifecycle. A way *into* SPEC.md, cross-linked by section, never a
  replacement that can drift from it.
- **The comparison strip** on the home page — categorical, adjacent, no
  ranking, one row per valid axis above.
- Rejected: a chart of any kind. There is no measured distribution here, and a
  quantitative form would invent rigor the evidence does not have.
- Rejected: an ER diagram of the format. A data page has five block types and
  no topology worth drawing; a list of blocks with real examples is more useful
  and survives at 390px.

## Closest DES reference

- **Marketing** for the home page: a prospective adopter must understand
  distinction and credibility. Proof is real validator output, never decorative
  terminal chrome.
- **Public-data** for the format map and the example page: exact values,
  provenance, overview-to-detail, adjacent comparison.
- **Editorial** for the argument sections and the counter-reading.
- **Operator** for `start.html`: exact commands, copyable, no invented output.

Design DNA held constant: artoo-kit type roles and spacing rhythm; one accent
(rust, so the four-value effect scale keeps red and amber for severity); the
monospace record voice for anything that is literal file content; and the
recurring **block → prose → code** triad that a data page is actually made of.

## Anti-reference

- The generic developer-tool landing page: gradient hero, three feature cards,
  logo strip, "Trusted by". There are no logos to strip.
- A fake terminal with typing animation. Motion that pretends to be a demo
  while proving nothing.
- Any invented dataset content a reader might mistake for real documentation.
  The walkthrough's county is fictional and its URLs are `example.gov`; the
  only real dataset on the site is the repository's own example page, and that
  page is labelled as what it is.
- A "compliance meter" or completeness score for a data page. ergo's own
  non-goals rule out treating metadata completeness as evidence that a dataset
  is safe to use; the site must not commit that sin in its own furniture.
- Internal tooling names anywhere in the deployed tree.

## Proof required

- **Factual proof:** every command, flag, key, vocabulary value, count and spec
  reference on the site resolves against the repository at the deployed
  revision. Generated by running `ergo.py`, importing its constants, and
  parsing SPEC.md — not from prose typed by hand. Drift fails the build.
- **Visual and editorial proof:** keyboard operation of the two stateful
  surfaces (the block picker, the issue filters), visible focus, reduced-motion
  behaviour, contrast in both themes, and responsive recomposition at 1440 /
  768 / 390.
- **Offline and firewall proof:** zero CDN and runtime dependencies; renders
  from `file://`; `artoo build`, `artoo status` and `artoo doctor` clean; the
  firewall keeps `work/` out of the deployed tree; the name-leak grep passes
  over `website/` including every generated data file.
