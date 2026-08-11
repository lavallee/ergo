# Vision — ergo

**North star:** Nobody working with a dataset—human or agent—has to rediscover
a known trap, silently repeat a bad workaround, or misuse a number because its
caveat lived only in prose, in one person's memory, or inside somebody's parser.

**North-star metric:** live issue coverage — the share of known consequential
dataset issues that are stably identified, machine-scoped, typed, current,
linked to the handling code, and backed by a dated validation record where the
claim can be checked.

## The problem, as measured

Every dataset has quirks, decisions, mislabelings, errors. Publishers usually
write them down — **18 of 20** sampled ship guidance that changes what a reader
may honestly claim — but inconsistently, and almost always somewhere the
download never points: a fetcher following download links alone reaches it
**7 times in 20**. Open-source parsers carry more of it, earned the hard way
and baked into code and nowhere else.

Frontier models are good at finding datasets and good at working out what is
wrong with them. What they do not reliably do is look around first. Denied the
dataset's documentation entirely, agents building an ELT pipeline completed
**at most one task out of many** — a controlled ablation, and the cleanest
statement available that this knowledge is not already in the model. Handed the
specific thing to look at, an agent's rate of finding known dataset issues rises
from **10.86–29.86%** to **67.42–78.28%** across DCA-Bench's hint ladder.

So the knowledge is worth a great deal and everyone currently pays for it
separately.

*Evidence: `docs/publisher-guidance-survey.md`; DCA-Bench, ELT-Bench, BIRD,
SEED, BEAVER and eight other sources, captured and graded in the project's
research notebook.*

## Strategy bets

- **ergo is two forms of caching.** The publisher's own guidance, found and
  pointed at; and other people's earned wisdom, pre-baked so nobody repeats
  the traversal. A cache hit is cheaper and more accurate than recomputing —
  and *how much* cheaper is measurable, moving, and currently narrowing. This
  bet is held with a number attached rather than as an article of faith; see
  below.
- **The cache is a lead, never an answer.** You still check. What you are
  handed is where to look and what to look for. The expensive part was never
  the reading; it was not knowing to look.
- **The issue is the unit.** A stable ID, effect, type, status, scope, misuse,
  and handling link make each caveat findable and actionable.
- **Capture happens at the moment of learning.** Every prior documentation
  tradition failed because writing it down was a separate act, done later, by
  someone who had stopped being confused. An agent working alongside you is
  present at that moment and holds what the record needs — so the skill, not
  the format, is what people adopt.
- **Canonical where it can be corrected.** A page belongs wherever it can
  actually be patched. A public bundle served from a private repository is
  published but unpatchable, so most pages are canonical in a directory rather
  than in somebody's repo. Where a project can take pull requests, it keeps its
  own page and the directory indexes it.
- **Adoption must be cheap and safe.** A vendorable stdlib tool, progressive
  conformance, explicit internal/public projection, and agent entry points let
  real data projects adopt ergo without a platform migration.

## Models getting better is the good outcome

ergo is not a bet against model improvement, and its value should not be
argued from a capability deficit. The published record shows improvement moving
fast: DABstep's hard split went from **14.55%** (paper baseline, Q1 2025) to
**89.95%** (validated leaderboard, February 2026).

**The knowledge gain is narrowing too, and we should say so.** The one
independent re-measurement of BIRD's external-knowledge effect — SEED, by
authors with no stake in BIRD — puts the gap at **8.35 to 20.86 points** across
six systems, with only the oldest scaffold reaching the high end and every
modern one sitting at 8–13. The original 2023 figure was +20.01. So supplying
domain semantics is still worth a lot, and it is worth less than it was.

Which gaps close is therefore an empirical question this project tracks rather
than assumes, with dated forecasts in the notebook. If the delta keeps
narrowing toward zero, models have absorbed what a page would have told them,
the second cache matters much less, and ergo should say so plainly rather than
defend the claim.

There is also a ceiling worth stating in public: handed *every* subtask
annotation, agents still fail roughly seven times in ten against warehouses
they were not trained on (BEAVER — 10.8% unaided to 30.1% for the best model
with full annotation, and 25.9% for the best method averaged across models).
No documentation format buys more than documentation can buy.

## Non-goals

- A data catalog service, data warehouse, or hosted validation platform.
- Replacing source ledgers, reporter notebooks, schemas, or ingestion tests.
- Making every caveat executable before the prose and scope are useful.
- Treating metadata completeness as evidence that a dataset is safe to use.
- Encoding any one publication's house style. A page may record that a rate
  under one percent cannot be shown without its denominator; it may not record
  that your newsroom prints "<1%".

## Engine map

- The data-page specification defines manifests, issues, practices, evidence,
  and the canonical/derived boundary.
- `tools/ergo.py` scaffolds, checks, exports, digests, and publishes without
  external dependencies. It reads and validates; it never rewrites a page.
- Greppable code anchors close the round trip between documented caveat and
  implemented workaround.
- Skills and AGENTS/CLAUDE pointers put the right subset of the issue registry
  into an agent's working context, and carry the procedures — consuming a page,
  registering an issue, reading a page out of an existing implementation.
- `scan` plus the reading procedure open a dataset that has no documentation
  anywhere, which is nearly all of them.
- The directory is where a page lives when its author cannot accept
  corrections publicly, and an index when they can.
- njschooldata is the first production proving ground; served public bundles
  test the decentralized documentation path.

## What would falsify this

Held open deliberately, because a vision nobody can argue with is not one.

- **Nothing yet shows a page helps.** `ergo check` validates well-formed;
  nothing validates useful, and those are demonstrably not the same thing.
  ROADMAP Outcome 2 remains unrun.
- **Every adopter is inside this household** and wanted the format to work.
- **The format is thinnest where the literature is thickest.** Schema linking
  is the most-measured failure anywhere and ergo has no column-level structure.
- **The evidence base is almost entirely self-reported.** Nearly every figure
  about how models handle data comes from a benchmark's authors reporting on
  the benchmark they built, and one of them — BEAVER — is structurally
  uncorroborable because its warehouses are private. Exactly one independent
  re-measurement exists in the set. Claims built on this base carry their
  grade, and should be read as the best available rather than as settled.
