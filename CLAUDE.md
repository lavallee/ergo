# ergo

Format and tooling for **data pages** — per-dataset documentation carrying a
structured, code-linked registry of a dataset's known pitfalls. See
[README.md](README.md) for what it is and [SPEC.md](SPEC.md) for the format.

This repo *is* the format, so the conventions below are ergo's own rules applied
to ergo. Changing one of them is a spec change, not a preference.

## Working on the format

- **Spec changes update four things together** — `SPEC.md`, `templates/datapage.md`,
  `examples/spr.md`, and `tools/ergo.py`. The four must never disagree; see
  [CONTRIBUTING.md](CONTRIBUTING.md).
- **`tools/ergo.py` stays one stdlib-only file** (Python ≥ 3.11, `tomllib`).
  Vendorability is the point, not an accident.
- **The tool reads and checks; it never rewrites a page.** Pages are edited as
  text, so comments survive. A structured writer would silently delete them.
- **Before committing**: `python3 tests/run.py`, `python3 -m unittest discover tests`,
  `python3 tools/ergo.py check examples templates --strict`, and
  `python3 website/build.py` — the site is derived from the tool and the spec, so
  drift fails its build rather than shipping stale.
- **Plain language.** Real terms of art from data work where they are more precise,
  ordinary English otherwise, and nothing invented. No process vocabulary about
  gates, floors, or things being earned. This is why 0.4 renamed `bite` to `pitfall`.

## Data pages in this repo

`examples/spr.md` is the worked example and `templates/datapage.md` the scaffold;
both are checked in CI and must stay warning-free under `--strict`. There is no
production data-page corpus here — adopters carry those.

## Agent skills

### Issue tracker

Issues live on **`lavallee/ergo-private`**, not this repo's origin — planning
references private corpora, so it stays out of the public tracker. Every `gh`
command needs an explicit `--repo`. See `docs/agents/issue-tracker.md`.

### Triage labels

The five canonical roles, each label string equal to its name. See
`docs/agents/triage-labels.md`.

### Domain docs

Single-context — one `CONTEXT.md` and `docs/adr/` at the repo root, both created
lazily. See `docs/agents/domain.md`.
