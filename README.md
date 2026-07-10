# ergo

Format and tooling for **data pages** — documentation of datasets as they
actually are, for the humans and agents who have to work with them.

Anyone who has worked with government data knows the real documentation
burden isn't the schema. It's the *issues*: the misspelled columns, the
suppression markers hiding in rate fields, the format that silently changed
in 2019, the category whose meaning narrowed in 2006, the boundary that
moved, the two published calculations with one name. Working through these
is the craft of data journalism — and every project that doesn't write them
down pays for the same discoveries twice.

A data page is one markdown file per dataset that a human reads as a
reporter's notebook and a program parses without guesswork: a manifest, a
narrative, and a **structured issue registry** where every known issue has a
stable ID, a type, an effect, a machine-readable scope (which years, which
columns), the foreseeable misuse it invites, and a link to the code that
works around it — with a greppable anchor in that code pointing back. Data +
documented caveats ⇒ justified use. Hence the name.

**[SPEC.md](SPEC.md)** has the full format: the page, the manifest, the
issue registry and its taxonomies, code linkage, validation records, the
index/digest, authoring discipline, tooling, and interop.

Why a new format? A survey of the landscape
([docs/survey.md](docs/survey.md)) — metadata standards, ML dataset cards,
validation tooling, newsroom practice, agency documentation, agent-readable
docs — found the same gap everywhere: **caveats live in prose.** No existing
format makes an issue scoped, typed, versioned, and code-linked at once. And
agents left to rediscover dataset issues unaided find roughly a third of
them; the rest must be handed over.

Design commitments (shared with ergo's sibling,
[flip](https://github.com/lavallee/flip)):

- **Plain files, no services.** Markdown with embedded TOML blocks. Readable
  with `less`, diffable with `git`, parseable with Python ≥ 3.11's stdlib.
- **One source of truth.** The page is canonical; JSON exports, index
  digests, public explainer pages, and catalog records (DCAT, Data Package,
  Croissant) are generated renders.
- **Vendorable tooling.** [`tools/ergo.py`](tools/ergo.py) — validator,
  digest, exporter, scaffold — is one dependency-free file you copy into
  your repo.

## Quick start

```bash
python3 tools/ergo.py new my-dataset --dir docs/data   # scaffold a page
# …fill it in (see templates/datapage.md and examples/)…
python3 tools/ergo.py check docs/data --repo .          # validate + code linkage
python3 tools/ergo.py digest docs/data --write docs/data/INDEX.md
```

Then plant a two-line pointer in your `CLAUDE.md`/`AGENTS.md` so agents find
the pages, and adopt the [skill](skills/ergo/SKILL.md) so they maintain them.

Status: spec draft v0.1, proven against
[njschooldata](https://github.com/lavallee/njschooldata)'s NJ DOE datasets.
Next: executable detection checks, catalog-format exporters, cross-project
issue sharing.

Contributions welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). Changes are
tracked in [CHANGELOG.md](CHANGELOG.md). [MIT licensed](LICENSE).
