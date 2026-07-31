# Negative fixture — every error class the validator should catch

Not a real data page. `tests/run.py` asserts that checking this file
produces exactly the errors and warnings listed in `tests/expected.txt`.
When you add a check to `ergo.py`, add its trigger here.

```toml ergo
[dataset]
ergo = "0.2"
slug = "Bad_Slug"
title = "Negative fixture"
publisher = "Test"
source_urls = [""]
pitfall = "Every block below is wrong on purpose."
status = "sideways"
version = 3
unknowns = "not a list"

contribute = "send us a postcard"

[dataset.acquisition]
terms = "public-ish"
credentials = 42
whatever = "unknown key"

[dataset.missingness]
zero_is_missing = "yes"
source_tokens = [1, 2]
bogus_key = true
```

## Issues

### An issue that is wrong in several ways

```toml ergo
[issue]
id = "shared-id"
title = "Mitigated but unhandled, bad effect, bad status, unknown type"
effect = "explodes"
type = "vibes"
status = "mitigated"
about = "ours"

[issue.scope]
nonsense = "x"

[issue.detect]
regex = ['([unclosed']
whatever = 1
```

### A misleads issue with no misuse

```toml ergo
[issue]
id = "no-misuse"
title = "Misleads but names no misuse"
effect = "misleads"
type = "definitional"
status = "open"

[issue.scope]
all = true
```

## Practices

### A practice that is wrong in several ways

```toml ergo
[practice]
id = "shared-id"
authority = "vibes"
rule = 42
contested = "sure"
addresses = ["no-such-issue"]

[practice.scope]
all = true
```

## Prior work

### A reference nobody could check or trust

```toml ergo
[reference]
kind = "wrapper"
url = "github.com/someone/thing"
maintenance = "abandoned"
supports = "not-a-list"
```

### A reference into a moving repository

```toml ergo
[reference]
id = "shared-id"
kind = "implementation"
url = "https://github.com/someone/thing"
observed = "2026-01-01"
```

## Quotes

### A quote with nothing a reader could re-check

```toml ergo
[quote]
text = "Estimates are subject to sampling variability."
supports = ["no-such-id"]
```

### A quote whose source is not a URL, and which quotes far too much

```toml ergo
[quote]
text = "Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. Padding to exceed the length warning. "
source = "the agency website"
retrieved = "2026-01-01"
```

## Changelog

```toml ergo
[change]
date = "2030-01-01"
note = "Dated after the manifest has no updated field."
issues = ["ghost-id"]
```
