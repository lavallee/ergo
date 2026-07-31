---
name: ergo
description: >
  Work with ergo data pages — the per-dataset documentation format with a
  structured, code-linked registry of known defects and sanctioned practices.
  Use when starting work with a documented dataset (read the digest, the core
  issues, and the practices for your question first), when hitting an
  unexplained oddity in data (check the registry before diagnosing), when
  working around a data problem in code (register the issue and anchor the
  fix), when deciding how a number may be computed (check for a practice
  before inventing one), or when authoring/revising a data page. Spec:
  https://github.com/lavallee/ergo
---

# Working with ergo data pages

A data page is one markdown file per dataset carrying fenced `toml ergo`
blocks: a `[dataset]` manifest, `[issue]` entries, `[practice]` entries, and
`[validation]` records. Pages live together (conventionally `docs/data/` or
`docs/data-sources/`) next to a generated `INDEX.md` digest. The project's
CLAUDE.md/AGENTS.md says where. IDs are `<dataset-slug>/<id>` — issues and
practices share one namespace — and appear in code as anchor comments:
`# ergo: spr/rate-prose-suppression`.

**Issues are defects; practices are handlings.** An issue is true whether or
not you exist. A practice is a decision about what may be computed and how —
sometimes ours, sometimes the publisher's. Read both.

**A fact about how this project handles the data is not an issue about the
data.** It belongs on the page for the dataset the project *produces* — one
that declares `produced_from` instead of `source_urls` and carries no
`subject`, because nobody else publishes it. Where that page is more ceremony
than it is worth, the issue is marked `about = "handling"`: true here, not
true for whoever else uses this dataset. Never carry such a claim into work
about the publisher's data.

## Consuming (before you touch the data)

1. **Read the digest** (`INDEX.md`): one line per dataset, with the `pitfall` —
   the single most likely way to get burned.
2. **Read `[dataset.acquisition]` before you fetch anything.** It is the
   acquisition stage in one table: `access` (`public`/`conditional`/
   `restricted`), `terms`, what `credentials` are needed, what `format`
   actually arrives, the `method`, `cadence` and `lag`, how to `verify` a new
   release landed, and `via` — whose copy you are fetching, when it is not the
   publisher's. A mirror is a separate provenance hop with its own schedule.
   Defects in fetching are issues like any other (`type = "acquisition"`).
3. **Skim the page** for the dataset you're using: the manifest (keys,
   builders, coverage) and the issue titles.
4. **Read every `core = true` issue in full before touching the data** —
   core issues apply regardless of your slice. Then load supplemental
   issue sections whose scope intersects your task; scope fields (`years`,
   `tables`, `columns`, `rows`, `entities`) are structured for exactly this
   test. An issue with `effect = "breaks"` or `"corrupts"` constrains
   ingestion; `"misleads"` and `"context"` constrain analysis and prose.
   Under context pressure, drop supplemental issues to their titles first;
   core issues stay whole; the manifest and `pitfall` never leave.
5. **Honor `misuse` fields** when writing analysis, charts, or copy — they
   name the foreseeable misread, and `instead` names the sanctioned move.
   If your draft does the thing a `misuse` field warns about, that is a bug
   in the draft.
6. **Read the practices before computing anything.** They are indexed by
   `question` — find the one matching the task you are doing. `rule` is the
   sanctioned move and `naive` is the wrong move it replaces; if your plan
   is the `naive` one, stop. `authority = "publisher"` means the decision is
   upstream and you do not get to re-derive it — departing from it means
   departing from the published definition, and you must say so in the
   output. `authority = "project"` plus `contested = true` means a competent
   team could rightly differ; you may too, deliberately and in writing.
   Check `irreversible` before assuming you can recover an underlying value,
   and `residual` before describing a mitigated number as clean.
7. **Read `unknowns` in the manifest.** It names where the page's knowledge
   stops. Absence of an issue in an area listed there is not evidence of
   absence — treat it as unexamined and say so rather than implying it is
   clean. A page with no `unknowns` is claiming completeness; be sceptical.
8. **Prefer a `[quote]` to your own paraphrase.** A `[quote]` block carries
   the source's exact words with the URL and the date they were seen there.
   When someone asks what the publisher actually says, show `text` — do not
   restate it. Everything in `text` is theirs; everything in `note` is the
   page author's. Keep that boundary when you repeat either one.
9. **Check `[reference]` blocks before writing a loader.** They name what
   already exists for this dataset — implementations, documentation, articles.
   Read `covers` to see whether it does what you need, `edition` for which
   vintage of the source it actually serves, and `maintenance` for whether it
   is still alive. `caveat` is the page author's judgment of it, not a fact
   about the dataset; weigh it as an opinion with a name attached. A reference
   is not an endorsement.
10. **Treat anchors as links to authority.** A comment `ergo: <slug>/<id>`
   means the weird code below it is deliberate; read that issue before
   "fixing" the code.
11. **No page in this repo? Look outward before writing a loader.** Order,
   cheapest first — stop at the first hit:
   1. **In-repo** — grep for `toml ergo` fences and `INDEX.md`.
   2. **The publisher's own bundle**, if the dataset has one: `<base>/index.json`.
   3. **Configured directories.** Read `ergo-sources.toml` (project root or
      beside the pages) and fetch each `[[source]]` url. Each is a JSON file
      with an `entries` array; match on `subject` — or, when you only have a
      mystery file, on `recognizes` (publisher domain, filename glob, column
      fingerprint). Report a signature match **with its basis** ("matched 14
      of 16 column names"); never assert identity silently.

   **Several pages will document the same dataset, and that is correct** —
   different projects ask different questions, so their `core` marks and
   practices legitimately differ. Present all of them, say which directory
   each came from, and let the human choose. Never merge them, never rank
   them, never silently prefer one.

   Adding a directory is two lines — offer it when a lookup misses:

   ```toml
   # ergo-sources.toml
   [[source]]
   name = "my-newsroom"
   url = "https://data.example-news.org/ergo/directory.json"
   ```

   To contribute your own pages to a directory:
   `python3 tools/ergo.py directory <pages-dir> --bundle <your-bundle-url>
   --entries-only` and open a PR against that directory's repo. Corrections
   to *someone else's* page go to that publisher's repo, never to the
   directory — a directory that accepts content patches becomes a fork of
   everything in it.
12. **Forking a page you found?** Set `subject` to the same URL so it still
   clusters, and record `[[dataset.derived_from]]` with the upstream url and
   today's date. That is what later lets anyone see what the upstream has
   added since you forked, instead of drifting quietly out of date.
13. **Working outside the repo?** Projects that serve a bundle expose
   `<base>/index.json` (every dataset's facts + issue list) and
   `<base>/<slug>.md` (the full page) over HTTP — fetch those instead of
   spelunking the code host. Check `updated` and the page's Changelog
   against when you last read it; the changelog tells you what's new.

## Bootstrapping a page from code that already works

When a dataset has no page anywhere — not in the repo, not in a bundle, not in
a configured directory — but something in the codebase already reads it, the
implementation is the record of what its author learned.

1. `python3 tools/ergo.py scan <src-dir>` (add `--json` to consume it). It
   lists candidate sites: sentinel comparisons, null filling, year-keyed
   parser branches, rename maps, sheet/header offsets, identifier padding,
   encoding fallbacks, parse guards, source URLs, and flagged comments.
   Anything already anchored is skipped.

   **This is a pre-pass, not an analysis.** Eleven regexes find places to
   look; they cannot tell whether a workaround was right, cannot see that
   four scattered branches are one problem, and cannot read the paragraph
   above the function explaining why. For anything beyond a quick survey,
   read **[reading-implementations.md](reading-implementations.md)** and
   follow it — it puts tests, fixtures, NEWS files, and commit history ahead
   of the parsing code, because that is where the reasons are.
2. **Read the candidate in context before believing it.** A hit proves someone
   handled something; it does not prove the reading behind it was right. They
   may have been wrong, or solving a different problem, or working around a
   bug of their own.
3. **Use git for the why.** `git log -S'<the constant>' -- <file>` finds the
   commit that introduced the workaround; the message usually says what the
   data did, and the diff shows it. A commit message is quotable — author,
   date, SHA — so cite it by permalink rather than paraphrasing it.
4. Draft the page honestly. The code proves `handled_by` and (via blame)
   `discovered`, and `status = "mitigated"` is true by construction. The
   nature of the defect is **inferred**: set `confidence = "?"` on the
   manifest and put an `unknowns` entry saying the implementation was read and
   the data was not. That is the difference between a good hypothesis and a
   claim.
5. Confirm what you can against real files and add a `[validation]` record for
   each. That is what turns a mined page into documentation.

Scanning someone else's library produces a page about **the dataset**, not
about the library: cite their code by permalink, never copy it in. Judgments
about the implementation itself ("this wrapper drops the margin of error") are
claims about a maintained project — keep them separate from claims about the
data, and tell the maintainers, who are best placed to say you are wrong.

## Acquiring an edition — read the parts that are not data

Publishers put their cautions where a parser never looks: a notes tab, a
readme sheet, a cover page, a legend, a technical guide. They add them
**precisely in the editions where something went wrong** — a pandemic year, a
waiver, a methodology change — which is exactly when a process that reads only
values will miss them.

1. On every edition you acquire, list the non-data parts and open them. A
   workbook tab called "Important Notes — Please Read Before Using Data" is
   the publisher handing you issues already written.
2. What you find is usually an `[issue]`, scoped to that edition, with a
   `misuse` naming what a reasonable reader would wrongly do. A caution that
   one year's figures are not comparable to adjacent years is
   `effect = "misleads"`, `type = "measurement"`, `[issue.scope] years = [...]`
   — not a general warning in prose.
3. **Quote them, do not paraphrase them** (`[quote]`, with `source` and
   `retrieved`). For a publisher caution the defensible artifact is their
   wording and where it appeared, not your summary of it.
4. If a specific question needs a rule on top of the issue, write a
   `[practice]` with `authority = "publisher"` that `addresses` it.
5. **Record where you looked and found nothing.** A `[validation]` record —
   *opened the notes sheets on all ten editions; guidance present only in
   2020-21* — is the difference between "the publisher was silent" and "nobody
   checked". Only one of those is evidence.

## When you hit something weird in the data

1. **Check the registry first** — grep the page (and `INDEX.md --long`
   output) for the symptom. Someone may have already paid for this lesson.
2. If it's genuinely new, **diagnose it, then register it** (below). Do not
   work around an undocumented issue silently: an unrecorded discovery is
   the next agent's re-discovery.

## Authoring an issue

Register the issue in the same change as the workaround:

1. Add a section + block to the dataset's page:

   ```toml ergo
   [issue]
   id = "kebab-symptom-name"        # permanent; never reuse or renumber
   title = "Symptom-first one-liner — what you'd notice, not the diagnosis"
   effect = "corrupts"              # breaks | corrupts | misleads | context
   type = "format"                  # see SPEC §5 taxonomy
   status = "mitigated"             # open | mitigated | resolved | monitor
   discovered = "2026-07"
   handled_by = ["tools/build_x.py#fix_fn"]   # required when mitigated
   detection = "how to spot it"
   misuse = "the wrong conclusion a reasonable reader would draw"

   [issue.scope]
   years = ["2019-20", "2020-21"]   # or "all"; also: tables, columns, rows, entities
   ```

2. Follow the block with prose: how it was found, concrete examples,
   quantities ("non-empty in 27,115 of 27,201 rows" beats "mostly
   populated"). Facts in the block are not restated in the prose.

   Before writing it, ask whether it is a fact about the data or about your
   pipeline. If it would stop being true the day your project shut down, it is
   not an issue about the dataset: put it on the produced dataset's page, or
   mark it `about = "handling"` if that page is not worth writing.

   The prose is **evidence, not explanation**. Nobody reads this page top to
   bottom; an agent pulls a paragraph out and shows it to someone. Write what
   survives that: a figure, a filename, a date, a row count, an example.
   General exposition is the part a reader can reconstruct without you.

   **Where the source already says it, quote it instead of composing a
   sentence.** This is the one place a fluent draft does real damage — a
   caveat you phrased becomes a caveat the publisher never wrote. Quote only
   words you have actually seen at a URL you have actually loaded; if you
   have not, say so and leave the quote out rather than reconstructing what
   the agency probably says.

   ```toml ergo
   [quote]
   text = "the source's exact words, verbatim"
   source = "https://…"             # the page they appear on
   retrieved = "2026-07-30"         # when you saw them there
   supports = ["kebab-symptom-name"]  # ids on this page it backs
   note = "why it is here — your framing, kept out of `text`"
   ```

   A quote is the strongest support a `[practice]` with
   `authority = "publisher"` can carry: it shows the decision is genuinely
   upstream rather than something someone inferred was upstream.
3. **Anchor the code**: put `# ergo: <slug>/<id>` in a comment adjacent to
   the workaround. Anchor + one line of "why this looks weird" — never a
   paraphrase of the page.
4. **Log the change**: anything that alters a consumer's picture of the
   dataset (new issue, status transition, scope correction, coverage
   extension) gets a `[change]` record in the page's Changelog section —
   `date`, `note`, `issues = [ids touched]` — and the manifest `updated`
   bumps in the same edit. Copyediting doesn't.
5. **Validate**: `python3 tools/ergo.py check <pages-dir> --repo .` must
   pass. Add `--require-manifest` when the directory is a closed data-page
   corpus so an unmarked Markdown file cannot disappear from the check.
   Regenerate the digest if titles/counts changed:
   `python3 tools/ergo.py digest <pages-dir> --write <pages-dir>/INDEX.md`.
   If the project serves a bundle (a `site/…/ergo/` directory with
   `index.json`), republish it in the same change:
   `python3 tools/ergo.py publish <pages-dir> --dir <bundle-dir> --base-url <url>`
   — and re-run any generator that renders ergo panels into public pages.
   The served copy is a **public projection**: wrap internal-only sections
   (rebuild runbooks, our-surfaces methodology, loading inventories) in
   `<!-- ergo:internal -->` … `<!-- /ergo:internal -->`; `handled_by`,
   `evidence`, and `access.builders/raw/feeds` are stripped automatically;
   chase publish's internal-smell warnings to zero-or-deliberate. Write
   issue prose so the *what* of a workaround is public ("non-numeric →
   NULL") and only the *how-we-run-ours* sits inside internal markers.

Judgment calls:

- **Dataset's problem vs. our choice — both belong on the page, in different
  blocks.** The file mixing four budget bases is the dataset's `[issue]`;
  which base your chart uses is a `[practice]`. Two tests: *would it still be
  true if all our tooling were rebuilt from scratch?* (yes → issue), and
  *could a competent team look at the same data and rightly decide
  otherwise?* (yes → practice, and set `contested = true`). The second
  catches what the first misses — an inherited publisher rule has no code to
  delete and is still a practice, marked `authority = "publisher"`.
- **When one defect has two handlings, that is why practices are separate.**
  Conduit contributions are double-counted in FEC data (one issue), but a
  committee topline excludes the memo lines while a donor list does the
  opposite. Two practices, one issue, both `addresses` it.
- **Does the practice earn its block?** Only if `naive` is fillable — if
  there is no plausible wrong move it rules out, it is documentation, so put
  it in the narrative. The validator warns on a practice with no `naive`.
- **Prohibitions are practices.** "These counts cannot be turned into rates"
  is a `[practice]` whose `rule` is the prohibition and whose `naive` is the
  forbidden computation — not an issue. `implemented_by` stays empty.
- **`stops_at` vs `irreversible`.** Where *our* automation stops and a human
  takes over → `stops_at`. Where the *publisher* already decided and the
  input is gone for good → `irreversible`. A reader acts differently on each.
- **Record what you don't know.** Add to the manifest's `unknowns` whenever
  you notice an era, column, or release channel you did not examine. Cheapest
  honesty in the format, and the only thing that stops silence from reading
  as a clean bill of health.
- **Set `subject` on every new page.** One URL naming *what dataset this is*
  — usually the program or product landing page — not where you fetch bytes
  (that is `source_urls`). It is a best guess and it is how anyone else finds
  your page alongside theirs. A page without one is invisible to directories;
  the validator warns.
- **Effect picking.** Pipeline fails → `breaks`. Numbers silently wrong →
  `corrupts`. Numbers faithful but a natural reading is wrong → `misleads`.
  Not a defect, but background you must hold → `context`.
- **Core marking.** `core = true` only when exposure is universal or one
  misread poisons published work — well under a third of the registry, or
  the flag means nothing (the validator warns). When in doubt, supplemental.
- **misuse/instead pairs.** Write `misuse` as the fail example, `instead`
  as the pass. If a foreseeable over-correction exists ("don't drop capped
  subgroup values entirely"), name it in the prose.
- **Never delete a resolved issue** — set `status = "resolved"` and keep the
  block. Archives of old vintages keep old issues relevant.
- **New dataset** → scaffold with `python3 tools/ergo.py new <slug>`, fill
  the manifest before anything else, and write the `pitfall` last, once you
  know which lesson cost the most.
