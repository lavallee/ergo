# <Dataset title>

One-paragraph lede: what this dataset is, who publishes it, and why this
project uses it. Written for someone deciding whether to read on.

```toml ergo
[dataset]
ergo = "0.1"
slug = "my-dataset"              # kebab-case; unique within the project
title = "<Dataset title>"
publisher = "<agency / org, office if known>"
source_url = "https://…"         # the landing page you'd send a human to
bite = "One sentence: the single most likely way this data bites someone who touches it cold."
status = "acquiring"             # live | acquiring | dormant | archived
confidence = "?"                 # A authoritative primary · B official doc · C secondary · ? unjudged
updated = "YYYY-MM-DD"           # last substantive page edit

[dataset.coverage]
years = "1998-99 → 2025-26"      # in the source's own year labels
grain = "year × entity × …"      # what one row means
entities = "who is covered"

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
                                 # linkage | uncertainty | availability | measurement
status = "open"                  # open | mitigated | resolved | monitor
discovered = "YYYY-MM"
# handled_by = ["tools/build_….py#fn"]   # required once mitigated; anchor the code:
#                                        #   # ergo: my-dataset/first-issue
detection = "how you'd spot it"
misuse = "the wrong conclusion a reasonable reader would draw"   # expected for misleads/context

[issue.scope]
years = "all"                    # or a list; also: tables, columns, rows, entities, all = true
```

How it was found; a concrete example; the numbers that let the next person
verify it's still true (or notice it changed).

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
