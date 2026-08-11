# Design brief

Private working document. Artoo keeps this file outside `site/`; it is not deployed.

## Reader decision

Someone about to build a data pipeline with model help — a data journalist, a
civic analyst, a data engineer — deciding **what to delegate and what to check
themselves**. They have read that models are now good at this, and they have
also watched one confidently produce a wrong number. Both are true and they
want to know which applies where.

They are not deciding whether to adopt ergo. This piece does not ask them to.

## Headline claim

**Model capability at data work is improving fast, and so is the payoff from
handing a model documentation it could have found on the web. What is not
improving is access to the knowledge that was never on the web in a form
anything trains on.**

Every benchmark that measures the value of supplying knowledge supplies
*published* knowledge, about a *public* dataset, in a corpus a model has
probably seen. That gain narrowing is expected and is what SEED measures. It
says nothing about the notes tab in a state agency's workbook, the footnote
attached to a municipal portal record, or the comment in somebody's parser —
because no benchmark has tested those, which is itself a finding.

The distinction the piece draws is therefore not capability-versus-knowledge.
It is **published knowledge, which models are absorbing, versus local knowledge,
which nothing has measured and nothing is absorbing.**

## Supported claims

- Capability gaps close fast. DABstep's hard split: **14.55%** (paper baseline,
  Q1 2025) → **89.95%** (validated leaderboard, 2026-02-22).
- Knowledge gaps close more slowly, and are closing. BIRD's gain from supplying
  external knowledge was **+20.01 points** in 2023; the one independent
  re-measurement (SEED, no overlap with BIRD's authors) puts it at
  **8.35–20.86 points** across six systems in 2026, with every modern scaffold
  at **8–13**. Still large, and smaller than it was.
- Documentation is not already in the model. ELT-Bench's controlled ablation:
  denied the dataset documentation, Claude-3.5 completed **1** task and GPT-4o
  **0**. This is the ablation; the widely quoted 9.6%-vs-78.8% ordering figure
  is a figure caption for one agent-model pair in one stage, with the reading
  order self-selected rather than assigned, and does not support an ordering
  claim.
- Handing over the specific thing to look at has a large dose-response.
  DCA-Bench: **10.86–29.86%** unaided → **67.42–78.28%** at the top of the hint
  ladder.
- There is a ceiling. BEAVER: **10.8%** unaided → **30.1%** for the best model
  with every subtask annotation supplied (**25.9%** for the best method averaged
  across models). Roughly seven failures in ten survive perfect documentation.
- The knowledge usually exists. Of 20 widely used open datasets, **19** ship
  non-data guidance and **18** ship guidance that changes what a reader may
  honestly claim — but only **7** put it where a program holding the download
  URL would find it.

## Unsupported claims and counter-reading

**What the evidence cannot establish.**

- That any documentation format improves real outcomes. Nobody has measured it.
  ScienceAgentBench found a documentation intervention that *lowered* execution
  validity (+1.9 points on one axis, worse on another) — so "more documentation"
  and "better result" are demonstrably not the same claim.
- That benchmark performance transfers to real pipelines. Benchmarks measure
  benchmark tasks, on data the benchmark chose, scored the way its authors
  scored it.
- That the numbers are stable. Several benchmarks' ground truth is contested by
  their own communities; figures cited here are dated for that reason.

**Strongest counter-reading.** The distinction may be a timing argument
wearing a category's clothes. If a 2029 model has absorbed enough of the web to
know the NJDOE notes tab, local knowledge just becomes published knowledge on a
lag, and the piece's central line dissolves. Nothing here rules that out. What
can be said is that the tab in question is inside an `.xlsx` behind a
JavaScript-rendered index, which is not obviously in anyone's crawl — and that
this is an argument about crawlability, not about intelligence.

**Second counter-reading.** Survivorship. Benchmarks that persist are the ones
that stay hard; the ones models solved got retired and stopped being cited. A
sample of live benchmarks over-represents unsolved problems by construction.

## Data vintages and denominators

Every figure carries its benchmark, split, and date, because these move fast
enough that an undated number is wrong within a year.

- DCA-Bench — hint levels h₀–h₃, 2024, success rate over curated dataset issues.
- BIRD — dev set execution accuracy, with/without external knowledge. 2023
  original (+20.01); 2026 independent re-measurement by SEED across six systems
  (8.35–20.86); a separate 2026 vendor-authored measurement, flagged in place
  and not load-bearing. ~7% of BIRD's own evidence annotations are themselves
  flawed by SEED's audit, so the 2023 figure is not a fixed point either.
- Spider 2.0, BEAVER — execution accuracy, enterprise/private-warehouse splits.
- DABstep — **hard split**, paper baseline vs validated leaderboard tier. These
  are different denominators and the mistake this piece exists partly to fix.
- ELT-Bench — end-to-end pipeline construction success.
- Publisher guidance — n=20 datasets, sampled 2026-08, our own survey.

## Licit comparisons

**Valid:** the same benchmark, same split, over time. A within-benchmark
ablation (with vs without supplied knowledge). Direction of movement across
several benchmarks, stated as direction and not as magnitude.

**Invalid, and named as such in the piece:**

- A benchmark's authors reporting on their own benchmark, read as independent
  corroboration. Almost every figure here is self-reported by construction —
  which is a fact about the evidence base, not a reason to discard it, and the
  piece should say so once, plainly.

- Across benchmarks — different tasks, different scoring, different data.
- Paper baseline against leaderboard top. This is the DABstep trap: 14.55% and
  89.95% are both real and comparing them as "the number" is wrong. The honest
  comparison is baseline-to-baseline or leaderboard-to-leaderboard.
- Any figure without its date.
- Our own 20-dataset survey against a benchmark. Different kind of evidence,
  different n, our own sampling.

## Selected forms

- **One time-series table** — benchmark × date × score, with the split named in
  the row. Serves the past/present axis directly and makes the undated-number
  problem visible on the page.
- **A paired-bar or slope comparison for ablations** — with-knowledge vs
  without, per benchmark. Serves the central claim.
- **No composite index.** Averaging across benchmarks would be exactly the
  invalid comparison the brief rules out.

## Closest DES reference

- The publisher-guidance survey (`docs/publisher-guidance-survey.md`) — same
  discipline: a tally table, per-item evidence, quoted primary text, and gaps
  recorded rather than filled.

## Anti-reference

- The AI-benchmark blog post that puts six benchmarks on one axis and draws a
  rising line. Fails on comparability, on dates, and on survivorship.
- Our own README before 2026-08, which cited a single benchmark number undated
  and used it to argue a capability deficit.

## Proof required

- **Factual proof:** every figure traced to a primary source captured with
  custody in the flip notebook, graded, and cited by claim id. Where a claim
  rests only on our own synthesis, say so on the page. This is not
  hypothetical: auditing our own synthesis against the primaries found thirteen
  discrepancies, including a figure caption read as an ablation and an error
  category read as a structural property. No figure enters this piece that has
  not been read at its source.
- **Counter-reading proof:** the two counter-readings above appear in the piece,
  not only in this brief.
- **Date proof:** no figure ships without its date and split.
