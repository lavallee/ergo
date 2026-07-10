# Contributing

ergo is a young spec (draft v0.1) being proven against real datasets.
Contributions most welcome right now:

- **Field reports.** You adopted the format for a dataset and something
  didn't fit — an issue that resists the taxonomy, a scope you couldn't
  express, ceremony that felt like padding. Open an issue describing the
  dataset and the friction; real cases move the spec, opinions less so.
- **Taxonomy proposals.** New `type` values need two or more independent
  real-world examples that existing types don't cover.
- **Tooling.** `tools/ergo.py` must stay a single stdlib-only file
  (Python ≥ 3.11) — that constraint is a feature (vendorability), not a
  budget. Bug fixes and check improvements welcome; new subcommands should
  be argued in an issue first.
- **Survey additions.** Know a documentation practice
  [docs/survey.md](docs/survey.md) missed — especially non-US government
  data cultures? PRs welcome with sources.

Ground rules:

- Spec changes update SPEC.md, the template, the example, and the validator
  together — the four must never disagree.
- Breaking format changes bump the version (§13) and get a CHANGELOG entry.
- Keep the voice: plain, concrete, quantified. No aspirational fields the
  reference implementation doesn't check.
