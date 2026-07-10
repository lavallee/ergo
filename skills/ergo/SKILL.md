---
name: ergo
description: >
  Work with ergo data pages — the per-dataset documentation format with a
  structured, code-linked known-issues registry. Use when starting work with
  a documented dataset (read the digest and relevant issues first), when
  hitting an unexplained oddity in data (check the registry before
  diagnosing), when working around a data problem in code (register the
  issue and anchor the fix), or when authoring/revising a data page. Spec:
  https://github.com/lavallee/ergo
---

# Working with ergo data pages

A data page is one markdown file per dataset carrying fenced `toml ergo`
blocks: a `[dataset]` manifest, `[issue]` entries, `[validation]` records.
Pages live together (conventionally `docs/data/` or `docs/data-sources/`)
next to a generated `INDEX.md` digest. The project's CLAUDE.md/AGENTS.md
says where. Issue IDs are `<dataset-slug>/<issue-id>` and appear in code as
anchor comments: `# ergo: spr/rate-prose-suppression`.

## Consuming (before you touch the data)

1. **Read the digest** (`INDEX.md`): one line per dataset, with the `bite` —
   the single most likely way to get burned.
2. **Skim the page** for the dataset you're using: the manifest (keys,
   builders, coverage) and the issue titles.
3. **Load the issue sections whose scope intersects your task.** Scope
   fields (`years`, `tables`, `columns`, `rows`, `entities`) are structured
   for exactly this test. An issue with `effect = "breaks"` or `"corrupts"`
   constrains ingestion; `"misleads"` and `"context"` constrain analysis
   and prose.
4. **Honor `misuse` fields** when writing analysis, charts, or copy — they
   name the foreseeable misread. If your draft does the thing a `misuse`
   field warns about, that is a bug in the draft.
5. **Treat anchors as links to authority.** A comment `ergo: <slug>/<id>`
   means the weird code below it is deliberate; read that issue before
   "fixing" the code.

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
4. **Validate**: `python3 tools/ergo.py check <pages-dir> --repo .` must
   pass. Regenerate the digest if titles/counts changed:
   `python3 tools/ergo.py digest <pages-dir> --write <pages-dir>/INDEX.md`.

Judgment calls:

- **Dataset's problem vs. our choice.** The file mixing four budget bases is
  the dataset's issue (register it); which base your chart uses is your
  methodology (narrative section or the consuming app's docs). Test: would
  it still be true if all our tooling were rebuilt from scratch?
- **Effect picking.** Pipeline fails → `breaks`. Numbers silently wrong →
  `corrupts`. Numbers faithful but a natural reading is wrong → `misleads`.
  Not a defect, but background you must hold → `context`.
- **Never delete a resolved issue** — set `status = "resolved"` and keep the
  block. Archives of old vintages keep old issues relevant.
- **New dataset** → scaffold with `python3 tools/ergo.py new <slug>`, fill
  the manifest before anything else, and write the `bite` last, once you
  know which lesson cost the most.
