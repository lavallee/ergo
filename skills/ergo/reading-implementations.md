# Reading an implementation into a data page

A procedure for recovering what a codebase's author learned about a dataset,
when no page for that dataset exists anywhere. Load this when bootstrapping
from code — your own repository, or an open-source parser someone else wrote.

`ergo scan` is the cheap pre-pass. It matches eleven regexes and finds
*places to look*: sentinel comparisons, year-keyed branches, rename maps,
header offsets. It cannot tell you whether a workaround was right, cannot see
that four scattered branches are one problem, and cannot read the paragraph
above the function explaining why. Use it to orient, then do the reading
below. A page built from scan output alone is a list of code smells wearing
the costume of documentation.

## Before anything: what dataset is this about?

A page documents a **dataset**, not a repository, and one repository usually
handles many. Split the work by dataset first or everything downstream is
wrong.

For each one, find the `subject` — the URL naming what the dataset *is*
(§4). Look in URL constants, the README, function documentation, test fixture
filenames, and any `data-raw/` script. **If you cannot identify the published
dataset a code path reads, stop and say so.** A page with no subject cannot
be clustered or found by anyone (§10), and guessing the identity is worse
than leaving it open.

## Read in this order — highest yield first

The parsing code is not the best source. It is where the workaround lives,
but the *reason* usually lives somewhere cheaper to read. Check which of these
a repository actually has before following the order ritually — a package with
four test files and a 700-line `NEWS.md` inverts the first two.

1. **Tests and fixtures.** The richest seam by a wide margin. A fixture is a
   captured sample of real-world data — often the only surviving evidence of
   what a bad file looked like. A test name is frequently a finished issue
   title: `test_handles_missing_header_2019`, `expect_error_on_ungraded_rows`.
   Read the fixture's contents, not just its name.
2. **NEWS / CHANGELOG.** Dated, in the author's words, and usually says what
   the data did: "fixed enrollment parsing for 2020 files, which moved the
   header to row 5." Quotable and citable.
3. **Long comments next to odd code.** A one-line comment is a label; a
   three-line comment is someone explaining a data problem they lost time to.
4. **README, vignettes, package documentation.** Where authors warn people in
   prose — the closest thing to an existing ergo page, and directly quotable.
   **Read the rendered example output, not just the prose.** A README code
   block that shows the function's real console output is a fixture in
   disguise: the warnings in it are what the data actually did on the author's
   machine. A discarded datum, a coercion notice, a row count that does not
   match the text above it — these are captured symptoms, and they are
   frequently the only evidence of a defect anywhere in the repository.
5. **The issue tracker**, if you can reach it. Bug reports are other people
   hitting the same dataset.
6. **The parsing code**, guided by scan output.
7. **Version control.** `git log -S'<constant>' -- <file>` finds the commit
   that introduced a workaround; `git log --grep='fix\|workaround\|broken'`
   finds the ones the author narrated. The message says what the data did and
   the diff shows it.

### Two things that get missed

**Open the file named after the concept.** If a topic has its own file —
`moe.R`, `suppression.py`, `geo.R` — read it. Grepping the big entry-point
file for the topic's keyword finds the call sites and misses the reasoning,
which lives in the dedicated file's documentation. This is the most common way
a read stops early with something plausible in hand.

**Follow the integration seams.** Where a library joins two sources — survey
attributes to boundary geometry, records to a crosswalk — look at what happens
when the two do not line up. A substitution like *"if the requested year has
no boundary file, use 2010"* produces a row with two different vintages in it
and no field saying so. These issues belong to neither source's page alone,
they are easy to read past because the code looks like ordinary
defaulting, and they are among the most damaging findings available.

## Cluster before you classify

Four `if year < 2009` branches in four functions are **one** issue about a
schema era, not four issues. A rename map with thirty entries is usually one
or two issues (a typo era, a subgroup relabelling), not thirty.

This is the main thing you can do that the regex pass cannot. Merge
aggressively, then check each cluster still has a single coherent scope — if
the scope is "everything", you merged too far.

## Sort every candidate three ways

**First: what kind of thing is it?**

| the finding is about | where it goes |
|---|---|
| the data itself — it would be true if this repo did not exist | `[issue]` |
| a decision about what may legitimately be computed | `[practice]` |
| this implementation's own behavior — its cache, its API, its bug | **not a page fact** |

The third row is the one that fills pages with noise. "The adapter caches for
30 days" is a fact about the library. It becomes a page fact only when it
changes what a *consumer of the data* must know — a stale cache that outlives
a replaced official workbook is a real trap, and that is the version to write.

Two implementation facts are worth carrying separately every time, because
they decide whether anyone should use the thing at all: **what edition of the
source it actually serves**, and **whether it is still maintained**. A wrapper
around a 2019 snapshot that has not been touched since 2021 is fine for
reproducing an old analysis and wrong for current work, and neither fact is
visible from its documentation.

**Second: who is it true for?** Everyone who touches this dataset, or only
this project? Only the first belongs in a page meant to be shared.

**Third: is it a defect, or is it the data?** A publisher's deliberate
suppression rule is not a bug. `effect = "context"` exists for things that are
correct and still mislead.

## Evidence rules

The failure here is a fluent draft that reads like documentation and was never
checked. These are not optional.

- **Every issue cites something.** A `file:line`, a commit SHA, a test name, a
  fixture path. No citation, no issue — delete it rather than soften it.
- **Prefer the author's own words.** A comment, a NEWS entry, a commit
  message, a vignette paragraph. Put it in a `[quote]` with the permalink and
  the date you read it, and let it carry the claim instead of your paraphrase.
- **Never infer the publisher's behavior from the parser's alone.** A
  `fillna(0)` shows what the author did. It does not show that the publisher
  writes nulls meaning zero — they may have been wrong, or solving a different
  problem, or papering over a bug of their own. Write what the code proves,
  then say what remains unverified.
- **Never invent scope.** If the branch says `year < 2009`, the scope is those
  years. If you cannot tell which columns are affected, say so in the issue's
  prose and leave the scope narrow. `all = true` on a guess is a lie that
  survives.
- **Mark inference as inference.** Where a claim rests only on the shape of
  the code, say that in the prose. A reader deciding whether to trust the page
  needs to know which parts were read off a file and which were reasoned.

## What the draft page looks like

Honest about its own provenance:

- `confidence = "?"` — the source has not been judged, only its parser read.
- `unknowns` carries an entry naming exactly this: *"Built by reading
  <repo>@<sha>; no file from the publisher has been examined."*
- `status = "mitigated"` and `handled_by` are true by construction where the
  workaround exists — this is the part mining gets right.
- `discovered` from the blame of the workaround, not guessed.
- Every issue's prose ends with what would confirm it.

Then hand back two things: the draft page, and a short list of what to check
against real files. The first `[validation]` record is what turns the draft
into documentation.

## Calibration

A dataset with a mature parser usually yields **3–8 issues** worth writing.
If you have produced thirty for one dataset you are reporting code smells; if
you have produced one for a parser with year-branching and a rename map, you
stopped too early. Where a repo handles many datasets, expect the count to
vary a lot between them — a stable annual CSV genuinely has less to say than a
twenty-year workbook series.

## Reading someone else's library

The output is a page about **the dataset**, not about the library.

- Cite their code by permalink at a pinned commit; never copy it into the
  page.
- Judgments about the implementation itself ("this wrapper drops the margin of
  error") are claims about a maintained project. Keep them out of the issue
  registry, keep them attributable, and tell the maintainers — they are best
  placed to tell you that you are wrong.
- Their license governs their code, not the facts about a public dataset that
  you learned by reading it.
