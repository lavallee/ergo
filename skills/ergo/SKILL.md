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

## Consuming (before you touch the data)

1. **Read the digest** (`INDEX.md`): one line per dataset, with the `bite` —
   the single most likely way to get burned.
2. **Skim the page** for the dataset you're using: the manifest (keys,
   builders, coverage) and the issue titles.
3. **Read every `core = true` issue in full before touching the data** —
   core issues apply regardless of your slice. Then load supplemental
   issue sections whose scope intersects your task; scope fields (`years`,
   `tables`, `columns`, `rows`, `entities`) are structured for exactly this
   test. An issue with `effect = "breaks"` or `"corrupts"` constrains
   ingestion; `"misleads"` and `"context"` constrain analysis and prose.
   Under context pressure, drop supplemental issues to their titles first;
   core issues stay whole; the manifest and `bite` never leave.
4. **Honor `misuse` fields** when writing analysis, charts, or copy — they
   name the foreseeable misread, and `instead` names the sanctioned move.
   If your draft does the thing a `misuse` field warns about, that is a bug
   in the draft.
5. **Read the practices before computing anything.** They are indexed by
   `question` — find the one matching the task you are doing. `rule` is the
   sanctioned move and `naive` is the wrong move it replaces; if your plan
   is the `naive` one, stop. `authority = "publisher"` means the decision is
   upstream and you do not get to re-derive it — departing from it means
   departing from the published definition, and you must say so in the
   output. `authority = "project"` plus `contested = true` means a competent
   team could rightly differ; you may too, deliberately and in writing.
   Check `irreversible` before assuming you can recover an underlying value,
   and `residual` before describing a mitigated number as clean.
6. **Read `unknowns` in the manifest.** It names where the page's knowledge
   stops. Absence of an issue in an area listed there is not evidence of
   absence — treat it as unexamined and say so rather than implying it is
   clean. A page with no `unknowns` is claiming completeness; be sceptical.
7. **Treat anchors as links to authority.** A comment `ergo: <slug>/<id>`
   means the weird code below it is deliberate; read that issue before
   "fixing" the code.
8. **No page in this repo? Look outward before writing a loader.** Order,
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
9. **Forking a page you found?** Set `subject` to the same URL so it still
   clusters, and record `[[dataset.derived_from]]` with the upstream url and
   today's date. That is what later lets anyone see what the upstream has
   added since you forked, instead of drifting quietly out of date.
10. **Working outside the repo?** Projects that serve a bundle expose
   `<base>/index.json` (every dataset's facts + issue list) and
   `<base>/<slug>.md` (the full page) over HTTP — fetch those instead of
   spelunking the code host. Check `updated` and the page's Changelog
   against when you last read it; the changelog tells you what's new.

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
  the manifest before anything else, and write the `bite` last, once you
  know which lesson cost the most.
