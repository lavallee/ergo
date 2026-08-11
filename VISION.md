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
wrong with them. What they do not do is look around first. An agent that reads
the documentation *before* writing pipeline config succeeds **78.8%** of the
time against **9.6%** for one that reads it after — and agents choose the wrong
order in **73%** of tasks. So everyone pays separately for the same lesson and
nobody banks it.

*Evidence: `docs/publisher-guidance-survey.md`; ELT-Bench, DCA-Bench, BIRD,
BEAVER and nine other sources, surveyed in the project's research notebook.*

## Strategy bets

- **ergo is two forms of caching.** The publisher's own guidance, found and
  pointed at; and other people's earned wisdom, pre-baked so nobody repeats
  the traversal. **A cache hit beats recomputation however good the compute
  gets** — which is why this does not decay as models improve.
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
argued from a capability deficit. The published record already shows both
directions: DABstep's hard split went from **14.55%** to **89.95%** in
eighteen months, while BIRD's gain from supplying domain semantics held at
**+17 to +23 points** across three years of scale.

So the honest position is that improvement closes some gaps and not others,
and which is which is an empirical question the project tracks rather than
assumes. The forecasts that test it are dated and in the notebook. If the
external-knowledge delta collapses, models have absorbed what a page would
have told them, the second cache matters much less, and ergo should say so.

There is also a ceiling worth stating in public: handed *every* subtask
annotation, agents still fail seven times in ten against warehouses they were
not trained on (BEAVER, 11.4% → 30.1%). No documentation format buys more
than documentation can buy.

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
  is the most-measured failure anywhere and ergo has no column-level
  structure; mixed-grain tables cause a third of errors on exactly the
  government data ergo targets and have no manifest flag.
