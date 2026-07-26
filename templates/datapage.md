# <Dataset title>

One-paragraph lede: what this dataset is, who publishes it, and why this
project uses it. Written for someone deciding whether to read on.

```toml ergo
[dataset]
ergo = "0.3"
slug = "my-dataset"              # kebab-case; unique within the project
title = "<Dataset title>"
publisher = "<agency / org, office if known>"
subject = "https://…"            # WHAT this documents — one URL; how directories cluster pages (§10)
source_urls = ["https://…"]      # where YOU get the bytes; a dataset can have several faces
bite = "One sentence: the single most likely way this data bites someone who touches it cold."
status = "acquiring"             # live | acquiring | dormant | archived
version = ""                     # the SOURCE's own edition/version label, if it has one — not the page's
confidence = "?"                 # A authoritative primary · B official doc · C secondary · ? unjudged
updated = "YYYY-MM-DD"           # last substantive page edit
unknowns = [                     # where your knowledge stops — silence reads as a clean bill of health
  "<what you have not examined: an era, a column, a release channel>",
]
# implementation = "https://…"   # public URL of your code — the one repo pointer the served projection keeps

# Forked someone else's page? Record it — it is what lets you see what the
# upstream has added since, instead of drifting quietly out of date.
# [[dataset.derived_from]]
# url = "https://example.org/ergo/their-page.md"
# retrieved = "YYYY-MM-DD"
# note = "Why you forked, and what you changed."

[dataset.coverage]
years = "1998-99 → 2025-26"      # in the source's own year labels
grain = "year × entity × …"      # what one row means
entities = "who is covered"

[dataset.missingness]
zero_is_missing = false          # true when the source writes 0 to mean "no value" (commoner than you'd think)
source_tokens = []               # literals meaning "not a number": "*", "N/A", "Fewer than 10 valid scores"

[dataset.access]
keys = ["…"]                     # join keys, in warehouse terms
raw = "data/raw/…"               # local cache of source files
builders = ["tools/build_….py"]  # ingestion code
feeds = ["…"]                    # tables / pages this source produces
```

## What it is

Orientation prose. What the dataset measures, the publisher's purpose for
it, what this project builds from it.

## Access

Where the files actually live (including any landing-page-vs-file-host
weirdness — register real quirks as issues and reference them here), formats
by year, sizes, fetch method.

## Structure

The shape of the data as normalized here: identity columns, metric columns,
format eras in summary. Drift itself belongs in the registry (`type =
"format"`); this section reads as the current understanding.

## Joins

Keys, quantified match rates ("~95% of districts match; unmatched keep NA"),
and join caveats by issue reference.

## Issues

One `###` section per issue: heading, block, then the story. Facts go in
the block; evidence, examples, and quantities go in the prose. Symptom-first
titles — name what you'd notice, not the diagnosis.

### <Symptom-first title of the first issue>

```toml ergo
[issue]
id = "first-issue"               # permanent kebab id, unique in this page
title = "<same one-liner as the heading, or sharper>"
effect = "corrupts"              # breaks | corrupts | misleads | context
type = "format"                  # definitional | universe | coverage | suppression |
                                 # geography | revision | coding | format | entry |
                                 # linkage | uncertainty | availability | measurement |
                                 # identity | policy
status = "open"                  # open | mitigated | resolved | monitor
# core = true                    # load before ANY contact with the dataset; mark sparingly (SPEC §5)
discovered = "YYYY-MM"
# handled_by = ["tools/build_….py#fn"]   # required once mitigated; anchor the code:
#                                        #   # ergo: my-dataset/first-issue
detection = "how you'd spot it"
misuse = "the wrong conclusion a reasonable reader would draw"   # expected for misleads/context
# instead = "the sanctioned move that replaces the misuse"       # misuse+instead = fail/pass pair

[issue.scope]
years = "all"                    # or a list; also: tables, columns, rows, entities, all = true

# [issue.detect]                 # optional structured detection (SPEC §5)
# regex = ['pattern the symptom matches']
# query = ["SELECT … sketch"]
# semantic = ["condition an agent can evaluate"]
```

How it was found; a concrete example; the numbers that let the next person
verify it's still true (or notice it changed).

## Practices

What may be computed from this data, and how. An issue is a defect that
would exist without you; a practice is a decision you (or the publisher)
made. One `###` section each, same discipline as issues.

### <The rule, stated as its conclusion>

```toml ergo
[practice]
id = "first-practice"            # permanent kebab id — one namespace with issues
title = "<the rule as a conclusion, not a topic>"
question = "<the task someone is doing when they need this>"
authority = "project"            # publisher (don't re-litigate) | project (our call) | community
rule = "<the sanctioned move>"   # or a list of strings for an ordered procedure
naive = "<the plausible wrong move this replaces>"   # no naive → it's documentation, not a practice
because = "<why; what a future reader would need to overrule this honestly>"
# addresses = ["first-issue"]    # issue ids on this page that this practice answers
# implemented_by = ["etl/….py#fn"]   # anchor it: # ergo: my-dataset/first-practice
# contested = true               # reasonable teams differ — independent of authority
# stops_at = "where OUR automation stops and a human takes over"
# irreversible = "what the publisher already decided, and which input is gone for good"
# residual = "the error we accept, AND its direction"
# because_not = "the road not taken, and what it cost when we tried it"
```

Why this call and not another; what it costs; who would disagree.

## Validation

How the work was checked. Reconciliations against independently published
figures, and dated confirmations from real files. Append records; never
edit old ones.

```toml ergo
[validation]
date = "YYYY-MM-DD"
method = "reconciled extract against <independent publication>"
result = "n/n spot figures match within rounding"
evidence = "path-or-ref"
```

## Provenance

Latest vintage in hand, fetch dates, the publisher's revision/errata
behavior, re-pull procedure.

<!-- ergo:internal -->
## Rebuild

Internal runbook — script names, commands, local paths. Everything between
the internal markers is dropped from the served public projection.
<!-- /ergo:internal -->

## Changelog

Append-only, newest last. One record per change that alters a consumer's
picture of the dataset (new issue, status change, coverage extension) —
and bump the manifest `updated` in the same edit (the validator checks).

```toml ergo
[change]
date = "YYYY-MM-DD"
note = "Page created."
# issues = ["ids-touched"]
```
