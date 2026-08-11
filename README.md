# ergo

**ergo helps you and your agents work around data pitfalls, and share what
you've learned.**

Anyone who has worked with government data knows the real burden isn't the
schema. It's the pitfalls: the misspelled columns, the suppression markers
hiding in rate fields, the format that silently changed in 2019, the category
whose meaning narrowed in 2006, the boundary that moved, the two published
calculations with one name. Working through these is the craft. Every project
that doesn't write them down pays for the same discoveries twice — and agents
left to rediscover dataset issues unaided find roughly a third of them.

## The loop

| | |
|---|---|
| **Before you fetch anything** | Find out what's already known about this dataset — in your repo, from the publisher, from a directory, or by reading a parser someone else wrote |
| **While you build** | Work around the known issues, and leave a greppable anchor in the code pointing at the one you're handling |
| **When something bites** | Record it where the next person will find it, at the moment you learned it |
| **Later, deliberately** | Offer the shareable part upstream — usually to a directory, since a private repo's page is published but unpatchable. Never automatically, and never for a dataset that isn't public |

Most of that runs through the [skill](skills/ergo/SKILL.md): the agent already
in your session is the one that just helped you work around a jam value, and
it is holding everything the record needs. That's the difference from every
documentation tradition that came before — the moment of learning and the
moment of writing it down can be the same moment.

## Starting from nothing

Most datasets have no documentation anywhere, and most publishers will never
write any. But if code exists that reads the data, that code is a record of
what its author learned, in the only notation they were willing to maintain.

```bash
python3 tools/ergo.py scan src/          # places where someone already handled something
```

`scan` is a cheap pre-pass — eleven regexes that find *where to look*. The
reading is in
[skills/ergo/reading-implementations.md](skills/ergo/reading-implementations.md),
which puts tests, fixtures, NEWS files and commit history ahead of the parsing
code, because that's where the reasons are. Run against three open-source
packages it recovered most of a hand-built reference catalog's findings and
added more; the runs and their limits are in
[docs/distribution.md](docs/distribution.md).

The governing rule: **code proves a workaround exists, not that the reading
behind it was right.** A draft built this way says so about itself.

## What gets written down

One markdown file per dataset — a **data page** — that a program parses
without guesswork and an agent reads with nothing in between:

- a **manifest**: what this is, where the bytes come from, what it covers, and
  the one sentence that saves a cold reader;
- an **issue registry**, where every known problem has a stable ID, a type, an
  effect, a machine-readable scope (which years, which columns), the
  foreseeable misuse it invites, and a link to the code that works around it —
  with an anchor in that code pointing back;
- a **practice registry**: the decisions about what may legitimately be
  computed. An issue is a defect that would exist without you; a practice is a
  call someone made, sometimes yours, sometimes the publisher's;
- **what backs the page**: `[quote]` for the source's own words with a URL and
  a date, `[reference]` for what other people have already built, and
  `[validation]` for what happened when a claim met real files.

Data + documented caveats ⇒ justified use. Hence the name.

The pages are plain files in your repo. That matters more than readability:
they sit next to the code they describe, they diff legibly in a pull request,
and nothing sits between an agent and the text.

## Install

The skill is the product, so the shortest path is the plugin:

```
/plugin marketplace add lyra-forge/marketplace
/plugin install ergo@lyra-forge
```

Start a new session. Your agent now knows to look for what is already known
about a dataset before touching it, and how to write down what it learns.

The validator installs separately, and deliberately not as a package — it is a
single dependency-free file you copy into the repository that holds the pages,
so a project can still be checked in five years:

```bash
curl -sSLo tools/ergo.py https://raw.githubusercontent.com/lavallee/ergo/main/tools/ergo.py
```

Then:

```bash
python3 tools/ergo.py new my-dataset --dir docs/data   # scaffold a page
python3 tools/ergo.py check docs/data --repo .          # gate the corpus
python3 tools/ergo.py digest docs/data --write docs/data/INDEX.md
```

Not using Claude Code? Copy [`skills/ergo/`](skills/ergo/) into whatever your
agent reads, and plant a two-line pointer in `AGENTS.md` so it finds the pages.

## Reading further

**[SPEC.md](SPEC.md)** has the full format: the page, the manifest, the issue
and practice registries and their taxonomies, code linkage, what backs a page,
the index/digest, directories, authoring discipline, tooling, and interop.

**[The site](https://lavallee.github.io/ergo/)** is the illustrated version: a
[walkthrough](https://lavallee.github.io/ergo/walkthrough.html) of one page
being built by real commands (including the three times the validator
refuses), the [format map](https://lavallee.github.io/ergo/format.html), the
[example page](https://lavallee.github.io/ergo/page.html) rendered from its own
export, and a [start guide](https://lavallee.github.io/ergo/start.html). Built
from this repository by `website/build.py`, so it cannot describe a format the
tool no longer enforces.

**[docs/survey.md](docs/survey.md)** is why this exists rather than an existing
standard. Metadata standards, ML dataset cards, validation tooling, newsroom
practice, agency documentation, agent-readable docs — the same gap everywhere:
**caveats live in prose.** No existing format makes an issue scoped, typed,
versioned, and code-linked at once.

**[Models and data](https://lavallee.github.io/ergo/review/)** is the background:
what the benchmark record actually shows about models doing data work — which
parts have improved, which have not, what supplying documentation is measurably
worth, and which stages of a data project nobody is measuring at all. It makes
no case for ergo; it is the problem space ergo exists inside.

**[docs/distribution.md](docs/distribution.md)** is the open design question:
how pages get found and contributed when the dataset's publisher will never
write one, which is nearly always.

## Design commitments

Shared with ergo's sibling, [flip](https://github.com/lavallee/flip):

- **Plain files, no services.** Markdown with embedded TOML blocks. Readable
  with `less`, diffable with `git`, parseable with Python ≥ 3.11's stdlib.
- **One source of truth.** The page is canonical; JSON exports, index digests,
  public explainer pages, and catalog records (DCAT, Data Package, Croissant)
  are generated renders.
- **Vendorable tooling.** [`tools/ergo.py`](tools/ergo.py) is one
  dependency-free file you copy into your repo. It reads and checks; it never
  rewrites your pages.
- **Plain language.** Real terms of art from data work where they're more
  precise, ordinary English otherwise, and nothing invented.

Status: spec draft v0.5, proven against
[njschooldata](https://github.com/lavallee/njschooldata)'s NJ DOE datasets and
a second adopting project's multi-publisher source-contract corpus. Run the
tests with `python3 tests/run.py` and `python3 -m unittest discover tests`.
Next: executable detection checks, catalog-format exporters, and a directory of
served bundles that publishes its own observed vocabulary.

Contributions welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). Changes are
tracked in [CHANGELOG.md](CHANGELOG.md). [MIT licensed](LICENSE).
