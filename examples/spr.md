# NJ School Performance Reports

Worked example of an ergo data page, condensed from the real page in
[njschooldata](https://github.com/lavallee/njschooldata). New Jersey's
official annual "report card" for every public school and district —
assessments, graduation, absenteeism, growth — and the authoritative source
for academic-outcome reporting.

```toml ergo
[dataset]
ergo = "0.1"
slug = "spr"
title = "NJ School Performance Reports"
publisher = "NJ Dept. of Education, Office of Performance Reports"
source_url = "https://www.nj.gov/education/spr/"
bite = "NJ publishes two 4-year graduation rates; only the State calculation has a multi-year trend — plotting the Federal rate as a trend (it has one point) is the classic misread."
status = "live"
confidence = "A"
updated = "2026-07-10"
implementation = "https://github.com/lavallee/njschooldata"

[dataset.coverage]
years = "2015-16 → 2024-25 (trend tabs post-COVID only)"
grain = "school year × entity × student group"
entities = "every NJ public school, district, and the state"

[dataset.access]
keys = ["county_code", "district_code", "school_code", "school_year"]
raw = "data/raw/spr/"
builders = ["tools/build_spr_db.py"]
feeds = ["grad_rate", "assessment", "assessment_grade", "absenteeism", "growth"]
```

## What it is

ESSA-mandated accountability data: state assessments (NJSLA), student
growth percentiles, graduation and dropout, chronic absenteeism, and more,
disaggregated by student group. One monolithic workbook per year (~80 tabs,
330 MB at school level), with a companion layout workbook as the data
dictionary.

## Joins

Code columns are zero-padded TEXT in the data (county 2-wide, district
4-wide) despite the layout calling them "Numeric" — see
`spr/layout-types-lie`. `SchoolYear` is a `"2020-21"` string. Joins to the
enrollment warehouse are clean on `(district_code, school_code,
school_year)` with no coercion.

## Issues

### Landing page and file host are different paths

```toml ergo
[issue]
id = "url-host-split"
title = "Files live under /education/sprreports/, not the /education/spr/ landing path"
effect = "breaks"
type = "availability"
status = "mitigated"
discovered = "2026-06"
handled_by = ["tools/build_spr_db.py"]
detection = "404s when constructing file URLs from the landing-page path"

[issue.scope]
all = true
```

The landing page is a JS app whose `download.js` builds the real links:
`https://www.nj.gov/education/sprreports/download/DataFiles/<YEAR>/<file>`
with hyphenated years (`2024-2025`). Easy to fetch the wrong path.

### The layout workbook's "Numeric" typing is misleading

```toml ergo
[issue]
id = "layout-types-lie"
title = "Code columns typed 'Numeric' in the layout are zero-padded TEXT in the data"
effect = "corrupts"
type = "format"
status = "mitigated"
discovered = "2026-06"
handled_by = ["tools/build_spr_db.py"]
detection = "CountyCode='13', DistrictCode='4900' — string cells with leading zeros preserved"
misuse = "Coercing codes to integers strips leading zeros and silently breaks the warehouse join."

[issue.scope]
columns = ["CountyCode", "DistrictCode", "SchoolCode"]
all = true
```

Confirmed against the 2024-25 District/State file: the data cells match the
warehouse's TEXT keys verbatim, so the *correct* behavior is to trust the
data over the data dictionary.

### Rate cells are strings, with prose suppression and capped extremes mixed in

```toml ergo
[issue]
id = "rate-prose-suppression"
title = "Rate cells carry % signs, prose suppression sentences, and >90%/<10% privacy caps"
effect = "breaks"
type = "suppression"
status = "mitigated"
core = true
discovered = "2026-06"
handled_by = ["tools/build_spr_db.py#rate"]
detection = "value fails float() after stripping a trailing % — includes '>90%', '<10%', and sentences like 'Fewer than 10 students were in the graduation cohort.'"
misuse = "Treating suppression NULLs as zero. Capped extremes also go NULL — harmless for All Students, a real loss for small subgroups."
instead = "Leave suppressed values NULL, exclude them from denominators, and say so in captions for small subgroups."

[issue.scope]
tables = ["grad_rate", "assessment", "assessment_grade", "absenteeism"]
columns = ["*Rate*", "*Percent*"]
years = "all"

[issue.detect]
regex = ['^(>|<)\\d+(\\.\\d+)?%$', 'Fewer than 10 (students|valid scores)']
semantic = ["a rate column parses as numeric for some rows and prose for others"]
```

Parse rule: a value is a number iff it parses after stripping a trailing
`%`; everything else → NULL. Four distinct suppression sentences observed in
the 2024-25 files, plus the two extreme caps.

### Two graduation-rate calculations, one populated trend

```toml ergo
[issue]
id = "grad-state-vs-federal"
title = "State and Federal 4-yr graduation rates coexist; only State is populated across years"
effect = "misleads"
type = "measurement"
status = "mitigated"
discovered = "2026-06"
handled_by = ["tools/build_spr_db.py"]
detection = "4YrGraduationRateState_District non-empty in 27,115 of 27,201 trend rows; Federal in only 5,423 (≈ one year)"
misuse = "Drawing the Federal rate as a trend line (it has one point), or comparing a State figure against another state's federal ACGR — NJ's State calc runs higher (SOMSD 2024-25: State 93.2% vs Federal 89.4%)."
instead = "Plot the State rate as the trend; headline the latest-year Federal ACGR beside it and caption the difference."

[issue.scope]
tables = ["grad_rate"]
columns = ["4YrGraduationRate*", "5YrGraduationRate*"]
years = "all"
```

The trajectory uses the State calculation; the latest-year Federal ACGR is
headlined where present, with the difference noted in the caption.

### A school's headline proficiency reflects only its tested grades

```toml ergo
[issue]
id = "grade-mix-context"
title = "District/state context blends all tested grades; a school's value covers only its own"
effect = "context"
type = "definitional"
status = "open"
discovered = "2026-06"
misuse = "Reading a high school's math proficiency sitting below its district as a deficit — the district figure blends grades 3–8 with HS course tests over different populations."

[issue.scope]
tables = ["assessment"]
all = true
```

Real, not a bug: comparisons across aggregation levels compare different
grade mixes. Per-grade views (`assessment_grade`) are the honest grain.

## Validation

```toml ergo
[validation]
date = "2026-06-14"
method = "confirmed from real data — 2024-25 District/State file"
result = "codes are zero-padded TEXT; All-Students label is 'All Students'; suppression is prose sentences; SchoolYear format matches warehouse"
```

## Provenance

Latest published: 2024-25 (released May 2026); databases downloadable back
to 2011-12 (legacy years via a separate archive). Working copy fetched
2026-06; record re-pulls here.

## Changelog

```toml ergo
[change]
date = "2026-07-10"
note = "Page created in ergo format; 5 issues registered from the 2024-25 acquisition notes."
```
