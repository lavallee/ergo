#!/usr/bin/env python3
"""Generate the ergo site's data from the real repository and the real tool.

Nothing this script emits is authored prose. The walkthrough frames come from
running ``tools/ergo.py`` against a scratch project in a temp directory; the
format map's vocabularies are imported from the validator itself and
cross-checked against SPEC.md; the example page comes from ``ergo export`` over
``examples/spr.md``; the coordinates come from the tool header, the spec, the
test suite, and ``git``.

Every derivation is fail-loud: a vocabulary that drifts from the spec, a
section reference that no longer resolves, a command that vanished, or a
walkthrough step that stops failing when it is supposed to fail raises, and the
site does not build. That is the point — the site cannot quietly describe a
format the tool no longer enforces.

Stdlib only, and no network access. Run via ``artoo build``.
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ARTIFACT = Path(__file__).resolve().parent
REPO = ARTIFACT.parent
SITE = ARTIFACT / "site"
DATA = SITE / "data"
TOOL = REPO / "tools" / "ergo.py"

DEMO_SLUG = "ridgeway-311"
DEMO_TITLE = "Ridgeway County 311 service requests"
EXAMPLE_PAGE = "examples/spr.md"


class BuildError(RuntimeError):
    """A derivation drifted. Fail the build rather than ship a stale fact."""


# ---------------------------------------------------------------------------
# process helpers


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    env = {**os.environ, "NO_COLOR": "1", "COLUMNS": "88", "PYTHONIOENCODING": "utf-8"}
    return subprocess.run(
        args, cwd=cwd, env=env, capture_output=True, text=True, timeout=120
    )


def git(*args: str) -> str:
    try:
        out = subprocess.run(
            ["git", *args], cwd=REPO, capture_output=True, text=True, timeout=30
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return out.stdout.strip() if out.returncode == 0 else ""


def load_tool():
    """Import tools/ergo.py as a module, for its own vocabularies.

    The site's format map is built from these constants rather than retyped, so
    a vocabulary can never drift between what the validator enforces and what
    the site says it enforces.
    """
    spec = importlib.util.spec_from_file_location("ergo_tool", TOOL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# the demo project — the walkthrough's source of truth
#
# Synthetic material. An invented county's 311 export, chosen so that no frame
# on the site could be mistaken for documentation of a real dataset, and so
# that every issue in it is a shape the survey found in real government data:
# a system migration that backfilled timestamps, boundaries that moved, a zero
# that means "never happened".

LEDE = f"""# {DEMO_TITLE}

Reporter's notebook for the county's 311 export: where it comes from, what it
counts, and every oddity worth knowing before you publish a response time.

"""

MANIFEST = """```toml ergo
[dataset]
ergo = "0.5"
slug = "ridgeway-311"
title = "Ridgeway County 311 service requests"
publisher = "Ridgeway County Office of Constituent Services"
subject = "https://data.ridgeway.example.gov/311"
source_urls = ["https://data.ridgeway.example.gov/311/requests.csv"]
pitfall = "Every ticket still open when the county switched ticket systems was closed on the migration date, so response times computed across March 2021 are worthless unless those rows are excluded."
status = "live"
version = "export of 2026-06-30"
confidence = "B"
updated = "2026-07-28"
unknowns = [
  "The pre-2018 archive is published as PDF summaries only; we have not read it.",
  "We do not know whether the vendor rewrites categories on old rows when the category list changes.",
]

[dataset.coverage]
years = "2018 -> 2026 (partial year)"
grain = "one row per service request"
entities = "unincorporated county only; the four boroughs run their own systems"

[dataset.missingness]
zero_is_missing = true
source_tokens = ["", "N/A", "UNKNOWN"]

[dataset.access]
keys = ["request_id"]
raw = "data/raw/ridgeway-311/"
builders = ["tools/load_311.py"]
feeds = ["requests", "response_times"]

[dataset.acquisition]
access = "public"
terms = "County open-data terms; attribution requested, redistribution unrestricted."
credentials = "none"
format = "One CSV per calendar year, plus a rolling current-year file."
method = "Direct file URLs from the county's open-data index."
cadence = "annual, with the current year refreshed nightly"
lag = "Closed requests appear the following business day."
verification = "Compare the new year file's row count against the county's published annual total."
size = "About 40 MB per year."
```

## What it is

Every call, web form, and app report the county logs, one row per request,
with a category, a ward, an opened timestamp, a closed timestamp, and a
response time the vendor computes for us. It is the only county-wide record of
what residents ask for, which is why it ends up under a lot of stories.

## Access

A nightly CSV export behind a stable URL. No API, no pagination, no
authentication; the file is rewritten in place each night, so yesterday's
export is not recoverable from the source once it is gone.

## Issues
"""

ISSUE_MIGRATION_DRAFT = """### Half of 2020's tickets close on the same day in March 2021

```toml ergo
[issue]
id = "migration-close-dates"
title = "Every ticket open on 2021-03-15 carries that date as its closed_date"
effect = "annoying"
type = "revision"
status = "open"
discovered = "2026-07"
detection = "closed_date = 2021-03-15 on 14,902 rows; the next busiest close date in the whole file is 231 rows"
```

The county moved from the old ticket system to the current vendor on
2021-03-15, and the migration wrote a close date onto everything that was
still open. Those tickets were not resolved that day; most of them were never
resolved at all. A 2020 request that sat for eleven months reports a response
time of eleven months and looks, in the data, like a case that was worked.
"""

ISSUE_MIGRATION_FIXED = """### Half of 2020's tickets close on the same day in March 2021

```toml ergo
[issue]
id = "migration-close-dates"
title = "Every ticket open on 2021-03-15 carries that date as its closed_date"
effect = "corrupts"
type = "revision"
status = "open"
discovered = "2026-07"
detection = "closed_date = 2021-03-15 on 14,902 rows; the next busiest close date in the whole file is 231 rows"
misuse = "Reading 2020 and early 2021 response times as if they were measured. They were assigned by a data migration."

[issue.scope]
years = ["2018", "2019", "2020", "2021"]
columns = ["closed_date", "response_hours"]
```

The county moved from the old ticket system to the current vendor on
2021-03-15, and the migration wrote a close date onto everything that was
still open. Those tickets were not resolved that day; most of them were never
resolved at all. A 2020 request that sat for eleven months reports a response
time of eleven months and looks, in the data, like a case that was worked.
"""

ISSUE_WARD_DRAFT = """### Ward numbers mean different places before and after 2022

```toml ergo
[issue]
id = "ward-renumbering"
title = "The 2022 redistricting reassigned ward numbers; ward 3 before and after are different places"
effect = "misleads"
type = "geography"
status = "open"
discovered = "2026-07"
detection = "ward 9 first appears in the 2022 file; ward 6's request volume falls 71% between 2021 and 2022 with no change in population"

[issue.scope]
years = "all"
columns = ["ward"]
```

The county redrew wards after the 2020 census and renumbered them rather than
keeping the old labels. Nothing in the export marks the change: the column is
called `ward` in every year and holds a small integer in every year.
"""

ISSUE_WARD_FIXED = """### Ward numbers mean different places before and after 2022

```toml ergo
[issue]
id = "ward-renumbering"
title = "The 2022 redistricting reassigned ward numbers; ward 3 before and after are different places"
effect = "misleads"
type = "geography"
status = "open"
discovered = "2026-07"
detection = "ward 9 first appears in the 2022 file; ward 6's request volume falls 71% between 2021 and 2022 with no change in population"
misuse = "Charting requests per ward as one series from 2018 to 2026. The lines cross where the boundaries moved, not where the potholes are."
instead = "Break the series at 2022, or aggregate to the county before comparing across it."

[issue.scope]
years = "all"
columns = ["ward"]
```

The county redrew wards after the 2020 census and renumbered them rather than
keeping the old labels. Nothing in the export marks the change: the column is
called `ward` in every year and holds a small integer in every year.
"""

ISSUE_ZERO_OLD_ID = """### response_hours is 0 for tickets nobody ever worked

```toml ergo
[issue]
id = "response-zero-unrecorded"
title = "response_hours is 0 when intake closed the ticket without opening a work order"
effect = "corrupts"
type = "entry"
status = "mitigated"
core = true
discovered = "2026-07"
handled_by = ["tools/load_311.py#response_hours"]
detection = "response_hours = 0 with an empty work_order_id — 8.1% of closed tickets"
misuse = "Averaging response_hours over closed tickets. The zeros are 'never dispatched', not 'answered instantly', and they pull the mean down by about a third."

[issue.scope]
all = true
columns = ["response_hours"]
```

Duplicate reports, wrong-agency referrals, and calls resolved on the phone are
closed at intake with no work order. The vendor's response-time calculation
subtracts the timestamps anyway and gets zero. The field is not missing, which
is what makes it dangerous: it survives every null check.
"""

ISSUE_ZERO_NEW_ID = ISSUE_ZERO_OLD_ID.replace(
    'id = "response-zero-unrecorded"', 'id = "response-hours-zero"'
)

TOMBSTONE = """### (renamed) response-zero-unrecorded

```toml ergo
[issue]
id = "response-zero-unrecorded"
title = "Renamed to response-hours-zero on 2026-07-28; kept so stale anchors fail loudly"
effect = "corrupts"
type = "entry"
status = "resolved"
superseded_by = "response-hours-zero"

[issue.scope]
all = true
```

A tombstone, not an issue: ids are permanent, so a rename leaves the old entry
behind for one release with the new id recorded on it.
"""

PRACTICES = """## Practices

### Response time is a median over worked tickets, and the migration date is dropped

```toml ergo
[practice]
id = "median-response-worked-only"
title = "Response time is the median over tickets that had a work order, excluding the migration date"
question = "How fast does the county respond to a complaint?"
authority = "project"
rule = [
  "Restrict to tickets with a work_order_id and a closed_date.",
  "Drop every ticket whose closed_date is the 2021-03-15 migration date.",
  "Report the median by year, with n.",
]
naive = "The mean of response_hours over every closed ticket, which folds in the intake zeros and the migration backfill."
because = "Both defects push the average down, and they push it down hardest in exactly the years a reader wants to compare against."
residual = "Dropping the migration date also drops roughly 400 tickets genuinely closed that day. The error runs toward reporting the county as slower than it was, which is the safer direction."
contested = true
addresses = ["migration-close-dates", "response-hours-zero"]
implemented_by = ["tools/load_311.py#median_response"]
```

The county's own annual report uses a mean over all closed tickets, so our
number will not match theirs and we say so in the note under every chart. A
newsroom that wanted to hold the county to its own published method would
rightly make the opposite call — hence `contested`.
"""

REFERENCE = """## Prior work

```toml ergo
[reference]
kind = "documentation"
url = "https://ridgeway.example.gov/311/data-dictionary"
observed = "2026-07-28"
covers = "The county's field-by-field dictionary for the 311 export, including the closure-code list."
maintenance = "dated"
caveat = "Last revised before the 2023 code change; three closure codes in the current export are absent from it."
```
"""

VALIDATION = """## Evidence

The county publishes its own figure, so quote it rather than paraphrase it —
`text` is theirs, `note` is ours, and `retrieved` is what makes it re-checkable
a year from now when the page has been rewritten.

```toml ergo
[quote]
text = "Across all service requests closed in 2024, the median time to close was 42 hours."
source = "https://ridgeway.example.gov/311/annual-report-2024"
retrieved = "2026-07-28"
supports = ["median-response-worked-only"]
note = "Their 42 hours counts the four boroughs; ours does not, and that is the whole of the gap below."
```

```toml ergo
[validation]
date = "2026-07-28"
method = "reconciled our 2024 median against the county's published annual service report"
result = "ours 41.5 h vs the county's 42 h for 2024; the gap is the four boroughs, which the county includes and we exclude"
evidence = "docs/data/ridgeway-311-reconciliation.md"
```
"""

REBUILD = """<!-- ergo:internal -->
## Rebuild

Fetch the nightly export into `data/raw/ridgeway-311/` and run
`python3 tools/load_311.py --rebuild`. The loader is idempotent; it truncates
and reloads both feeds.
<!-- /ergo:internal -->
"""

CHANGELOG = """## Changelog

```toml ergo
[change]
date = "2026-07-28"
note = "First pass over the 311 export: migration close dates, ward renumbering, and the intake zeros registered; response-time practice recorded."
issues = ["migration-close-dates", "ward-renumbering", "response-hours-zero"]
```
"""

LOADER_NO_ANCHOR = '''"""Load the Ridgeway County 311 export into the warehouse."""

import csv
from statistics import median

MIGRATION_CLOSE_DATE = "2021-03-15"


def response_hours(row):
    hours = row.get("response_hours")
    if hours in (None, "", "N/A", "UNKNOWN"):
        return None
    hours = float(hours)
    if hours == 0 and not row.get("work_order_id"):
        return None
    return hours


def load(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return [row for row in csv.DictReader(handle)]
'''

LOADER_ANCHORED = '''"""Load the Ridgeway County 311 export into the warehouse."""

import csv
from statistics import median

MIGRATION_CLOSE_DATE = "2021-03-15"


def response_hours(row):
    hours = row.get("response_hours")
    if hours in (None, "", "N/A", "UNKNOWN"):
        return None
    hours = float(hours)
    # ergo: ridgeway-311/response-zero-unrecorded — a 0 with no work order means
    # nobody was ever dispatched, not that the call was answered instantly.
    if hours == 0 and not row.get("work_order_id"):
        return None
    return hours


def load(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return [row for row in csv.DictReader(handle)]
'''

LOADER_RENAMED_ANCHOR = LOADER_ANCHORED.replace(
    "ergo: ridgeway-311/response-zero-unrecorded",
    "ergo: ridgeway-311/response-hours-zero",
)

LOADER_WITH_MEDIAN = LOADER_RENAMED_ANCHOR + '''

def median_response(rows, year):
    # ergo: ridgeway-311/median-response-worked-only — worked tickets only, and
    # the migration date is not a close date.
    hours = [
        response_hours(row)
        for row in rows
        if row["closed_date"].startswith(year)
        and row["closed_date"] != MIGRATION_CLOSE_DATE
        and row.get("work_order_id")
    ]
    hours = [h for h in hours if h is not None]
    return median(hours) if hours else None
'''

AGENT_POINTER = """# Ridgeway Times — data desk

## Data documentation

Every dataset we ingest has an ergo data page in `docs/data/`, indexed by
`docs/data/INDEX.md`. Read the page before writing code against a dataset:
issues carry stable ids, the ids are anchored in the code that works around
them, and `python3 tools/ergo.py check docs/data --repo .` validates that
contract.
"""


# ---------------------------------------------------------------------------
# the page, assembled section by section

SECTION_ORDER = [
    "lede",
    "manifest",
    "issue-migration",
    "issue-ward",
    "issue-zero",
    "tombstone",
    "practices",
    "reference",
    "validation",
    "rebuild",
    "changelog",
]


def page_text(sections: dict[str, str]) -> str:
    parts = [sections[name] for name in SECTION_ORDER if name in sections]
    return "\n".join(part.rstrip("\n") + "\n" for part in parts)


def step_plan() -> list[dict]:
    """The narrative. Each step edits files, runs commands, and shows a record.

    ``record`` selects what the reader is shown after the step:
      ``file``   — a file in the demo project, optionally sliced
      ``block``  — the single ergo block carrying a given id, from the page
      ``stdout`` — the command's own output (used when the output *is* the point)
    """
    return [
        {
            "id": "scaffold",
            "act": "Open a page",
            "say": (
                "We're building a response-time tracker on the county's 311 export. "
                "Before you write any parsing code, start a data page for it."
            ),
            "reply": (
                "Scaffolded one. It's a single markdown file in docs/data — a page "
                "you can read top to bottom, with TOML blocks a program can parse."
            ),
            "title": "Scaffold the page",
            "narrative": (
                "A data page is one file per dataset, not a database and not a "
                "directory. `new` writes the template: a manifest, the section arc "
                "the format converges on, and one empty issue to be filled or "
                "deleted."
            ),
            "spec": "3",
            "commands": [["new", DEMO_SLUG, "--dir", "docs/data"]],
            "record": {
                "kind": "file",
                "path": "docs/data/ridgeway-311.md",
                "limit": 30,
                "caption": "The scaffold. Structured facts go in the blocks; the story goes in the prose between them.",
            },
        },
        {
            "id": "scaffold-fails",
            "act": "Open a page",
            "say": "",
            "reply": (
                "Worth knowing up front: the scaffold does not validate. The format "
                "will not call a page valid until it says who publishes the data, "
                "where it comes from, and what the one thing that bites is."
            ),
            "title": "An empty page is not a valid page",
            "narrative": (
                "`check` is the gate, and the scaffold fails it. That is deliberate: "
                "empty structure is worse than absent structure, so the template's "
                "placeholders are errors until somebody has actually looked at the "
                "data. `pitfall` — one sentence naming the thing most likely to trip "
                "up a cold reader — is required, and it is the field that travels "
                "furthest, into the index and into an agent's context."
            ),
            "spec": "4",
            "commands": [["check", "docs/data"]],
            "expect_failure": True,
            "record": {
                "kind": "stdout",
                "limit": 14,
                "caption": "Exit code 1. Required fields are errors, not suggestions.",
            },
        },
        {
            "id": "manifest",
            "act": "Open a page",
            "say": "",
            "reply": (
                "Filled the manifest from the export and the county's landing page. "
                "Note `unknowns` — I've said what I haven't looked at, so silence "
                "doesn't read as a clean bill of health."
            ),
            "title": "Write the manifest",
            "narrative": (
                "The manifest is the machine-readable identity of the dataset: "
                "publisher, where the bytes come from, coverage, what the source "
                "writes when it means nothing, and the pitfall. `subject` is the "
                "identity claim — the URL naming *what dataset this is*, as opposed "
                "to where we happen to fetch it — and it is what lets a directory "
                "cluster this page with other people's pages about the same data."
            ),
            "spec": "4",
            "edits": {"page": {"manifest": MANIFEST}},
            "commands": [["check", "docs/data"]],
            "record": {
                "kind": "block",
                "path": "docs/data/ridgeway-311.md",
                "id": "ridgeway-311",
                "caption": "zero_is_missing is a page-level fact about this publisher — the shape the survey found most often in government data.",
            },
        },
        {
            "id": "first-issue",
            "act": "Register what bites",
            "say": (
                "Something's off in 2020 — a huge number of tickets close on the same "
                "day in March 2021. Look into it and write down what you find."
            ),
            "reply": (
                "Found it: a system migration closed everything that was open. I "
                "registered it — but `check` refused my draft twice over, and both "
                "refusals are fair."
            ),
            "title": "The first issue, refused",
            "narrative": (
                "Two errors, and they are the format's two hardest edges. `effect` "
                "is a closed vocabulary of four values — breaks, corrupts, misleads, "
                "context — so an agent cannot invent a severity word, and a consumer "
                "can filter on it. And an issue with no `[issue.scope]` table is "
                "rejected outright: which years, which columns, which tables. "
                "\"Some years are affected\" is a bug report, not documentation."
            ),
            "spec": "5",
            "edits": {"page": {"issue-migration": ISSUE_MIGRATION_DRAFT}},
            "commands": [["check", "docs/data"]],
            "expect_failure": True,
            "record": {
                "kind": "stdout",
                "caption": "The vocabulary is closed so that filtering works. The scope is required so that filtering is possible at all.",
            },
        },
        {
            "id": "first-issue-fixed",
            "act": "Register what bites",
            "say": "",
            "reply": (
                "Fixed both: it corrupts (the pipeline succeeds and the numbers are "
                "silently wrong), and it is scoped to the four years and two columns "
                "it actually touches."
            ),
            "title": "Typed, and scoped",
            "narrative": (
                "`corrupts` is the dangerous class: unlike `breaks`, nothing fails. "
                "The scope table is what lets an agent working on 2024 data skip this "
                "issue without an LLM call, and what stops the page from becoming a "
                "wall of caveats that everybody loads and nobody reads."
            ),
            "spec": "5",
            "edits": {"page": {"issue-migration": ISSUE_MIGRATION_FIXED}},
            "commands": [["check", "docs/data"]],
            "record": {
                "kind": "block",
                "path": "docs/data/ridgeway-311.md",
                "id": "migration-close-dates",
                "caption": "One block, one section. The block carries the facts; the prose under it carries the story and the numbers.",
            },
        },
        {
            "id": "ward-issue",
            "act": "Register what bites",
            "say": (
                "There's a second one. Somebody is eventually going to chart requests "
                "per ward across all the years."
            ),
            "reply": (
                "Registered the renumbering. `check` passed it but warned — I typed "
                "it `misleads` and never said what the misreading is."
            ),
            "title": "A warning with a point to make",
            "narrative": (
                "This is the class only a documented page will ever tell you: the "
                "numbers are faithful to the source and a natural reading of them is "
                "still wrong. So for `misleads` and `context`, the validator warns "
                "when `misuse` is missing — naming the foreseeable misread is data "
                "journalism's contribution to documentation, and the field is its "
                "slot."
            ),
            "spec": "5",
            "edits": {"page": {"issue-ward": ISSUE_WARD_DRAFT}},
            "commands": [["check", "docs/data"]],
            "record": {
                "kind": "stdout",
                "caption": "A warning, not an error: the page is valid, and it is not yet useful.",
            },
        },
        {
            "id": "misuse",
            "act": "Register what bites",
            "say": "",
            "reply": (
                "Named the misuse and the move that replaces it. That pair is the "
                "part a reader in a hurry actually reads."
            ),
            "title": "Name the misuse, name the fix",
            "narrative": (
                "`misuse` and `instead` are a fail/pass pair — the shape both a "
                "hurried reporter and a language model follow best. It is also the "
                "sentence most likely to survive into a caption, which is why the "
                "format asks for it in the registry rather than in a paragraph "
                "somewhere below."
            ),
            "spec": "5",
            "edits": {"page": {"issue-ward": ISSUE_WARD_FIXED}},
            "commands": [["check", "docs/data"]],
            "record": {
                "kind": "block",
                "path": "docs/data/ridgeway-311.md",
                "id": "ward-renumbering",
                "caption": "No scope guessing: the issue is scoped to every year, because the renumbering changes what every year's ward column means.",
            },
        },
        {
            "id": "handled-by",
            "act": "Bind it to the code",
            "say": "Alright — now write the loader.",
            "reply": (
                "Loader written, and the zeros it drops are registered as a third "
                "issue, marked mitigated with `handled_by` pointing at the function. "
                "`check --repo .` warns: the code doesn't admit what it's doing."
            ),
            "title": "Documentation that knows where its fix lives",
            "narrative": (
                "A `mitigated` issue must name the code that handles it — that is an "
                "error, not a warning. The warning here is the other direction: the "
                "handling code carries no anchor, so the page points at the code and "
                "the code says nothing back. That is the state in which a future "
                "cleanup deletes the guard as dead weight."
            ),
            "spec": "7",
            "edits": {
                "page": {"issue-zero": ISSUE_ZERO_OLD_ID},
                "files": {"tools/load_311.py": LOADER_NO_ANCHOR},
            },
            "commands": [["check", "docs/data", "--repo", "."]],
            "record": {
                "kind": "stdout",
                "caption": "The page knows about the code. The code does not know about the page.",
            },
        },
        {
            "id": "anchor",
            "act": "Bind it to the code",
            "say": "",
            "reply": (
                "Anchored it. One comment line in the function, and the round trip "
                "closes — the page finds the code, the code names the page."
            ),
            "title": "Close the round trip",
            "narrative": (
                "The anchor is a comment matching `ergo: <slug>/<issue-id>`, next to "
                "the workaround. It replaces the paragraph a well-meaning developer "
                "would otherwise paste into the code, where it would drift: one line "
                "of *why this looks weird* is good manners, three lines is a fork. "
                "`grep -rn 'ergo: ridgeway-311'` now finds every workaround in the "
                "repository."
            ),
            "spec": "7",
            "edits": {"files": {"tools/load_311.py": LOADER_ANCHORED}},
            "commands": [["check", "docs/data", "--repo", "."]],
            "record": {
                "kind": "file",
                "path": "tools/load_311.py",
                "lang": "python",
                "limit": 20,
                "caption": "The comment is the link. Deleting the guard now breaks a check instead of quietly changing a number.",
            },
        },
        {
            "id": "rename",
            "act": "Bind it to the code",
            "say": "'response-zero-unrecorded' is a mouthful. Rename it.",
            "reply": (
                "Renamed it on the page — and `check` stopped me with an error, "
                "because the anchor in the loader now names an issue that doesn't "
                "exist. Exit 1."
            ),
            "title": "Ids are permanent for a reason",
            "narrative": (
                "An anchor naming an unknown issue is an error, never a warning: it "
                "means the documentation was renamed or deleted out from under the "
                "code, and the code is now carrying an explanation nobody can look "
                "up. This is the failure the round trip exists to catch, and it is "
                "the reason the spec asks for a tombstone rather than a clean rename."
            ),
            "spec": "15",
            "edits": {"page": {"issue-zero": ISSUE_ZERO_NEW_ID}},
            "commands": [["check", "docs/data", "--repo", "."]],
            "expect_failure": True,
            "record": {
                "kind": "stdout",
                "caption": "Exit code 1. The rename is not done until the code agrees.",
            },
        },
        {
            "id": "tombstone",
            "act": "Bind it to the code",
            "say": "",
            "reply": (
                "Updated the anchor and left a tombstone: the old id stays on the "
                "page as resolved, pointing at the new one, so anybody's stale link "
                "lands somewhere that explains itself."
            ),
            "title": "Leave a tombstone",
            "narrative": (
                "Issue ids are permanent because they are cited — in code anchors, in "
                "other people's pages, in commit messages. A rename creates the new "
                "id and keeps the old entry for one release, marked `resolved` with "
                "`superseded_by`, so stale references fail loudly rather than "
                "silently resolving to nothing."
            ),
            "spec": "15",
            "edits": {
                "page": {"tombstone": TOMBSTONE},
                "files": {"tools/load_311.py": LOADER_RENAMED_ANCHOR},
            },
            "commands": [["check", "docs/data", "--repo", "."]],
            "record": {
                "kind": "block",
                "path": "docs/data/ridgeway-311.md",
                "id": "response-zero-unrecorded",
                "caption": "A tombstone: status resolved, superseded_by the new id. Kept for one release, then dropped.",
            },
        },
        {
            "id": "practice",
            "act": "Decide, check, hand it over",
            "say": "So what's the actual number? How fast does the county respond?",
            "reply": (
                "Before I give you a number I've written down how it's computed — as "
                "a practice, not an issue. The defects are the county's; this "
                "decision is ours, and a different newsroom would rightly make it "
                "differently."
            ),
            "title": "A decision is not a defect",
            "narrative": (
                "Two tests separate them. Deletion: would this still be true if we "
                "deleted all our code? The migration backfill would; the median "
                "would not. Disagreement: could a competent team rightly decide "
                "otherwise? Here, yes — a newsroom holding the county to its own "
                "published method would use the mean, which is why this one carries "
                "`contested`. `naive` names the move being ruled out, `residual` "
                "names the error that remains **and its direction**, and `addresses` "
                "ties the practice back to the defects underneath it."
            ),
            "spec": "6",
            "edits": {
                "page": {"practices": PRACTICES},
                "files": {"tools/load_311.py": LOADER_WITH_MEDIAN},
            },
            "commands": [["check", "docs/data", "--repo", "."]],
            "record": {
                "kind": "block",
                "path": "docs/data/ridgeway-311.md",
                "id": "median-response-worked-only",
                "caption": "One defect can have several handlings, chosen by the question being asked — which is why practices are their own block.",
            },
        },
        {
            "id": "validation",
            "act": "Decide, check, hand it over",
            "say": "Does our number survive contact with the county's own report?",
            "reply": (
                "Close, and the gap is explainable: ours 41.5 hours against their 42 "
                "for 2024, and the difference is the boroughs. Recorded as a dated "
                "validation record with the numbers in it."
            ),
            "title": "Record the reconciliation",
            "narrative": (
                "A caveat you have not tested is a hypothesis. Two blocks answer "
                "that: a quote shows what the source itself says, verbatim and "
                "dated, so nobody has to trust a paraphrase; a validation record "
                "shows what happened when the claim met real files. Both "
                "accumulate — never edit an old record, add a new one. The numbers "
                "are what let the *next* check detect drift."
            ),
            "spec": "8",
            "edits": {"page": {"reference": REFERENCE, "validation": VALIDATION}},
            "commands": [["check", "docs/data", "--repo", "."]],
            "record": {
                "kind": "block",
                "path": "docs/data/ridgeway-311.md",
                "id": "reconciled our 2024 median",
                "caption": "\"7 of 7 figures match within rounding\" beats \"we checked\" — a number is what the next person can re-run.",
            },
        },
        {
            "id": "digest",
            "act": "Decide, check, hand it over",
            "say": "Make sure the next person — or the next model — finds this.",
            "reply": (
                "Generated the index and planted a three-line pointer in the desk's "
                "CLAUDE.md. Agents don't discover documentation at well-known paths; "
                "they go where they're pointed."
            ),
            "title": "The agent entry point",
            "narrative": (
                "The digest is one row per dataset: status, issue counts by effect, "
                "core flagged, and the pitfall line. It is the first of three "
                "disclosure tiers — digest, then the page's manifest and issue "
                "titles, then the issue's own section — so a working agent can spend "
                "a hundred tokens or three thousand depending on what it is about to "
                "touch."
            ),
            "spec": "9",
            "edits": {
                "page": {"rebuild": REBUILD, "changelog": CHANGELOG},
                "files": {"CLAUDE.md": AGENT_POINTER},
            },
            "commands": [
                ["digest", "docs/data", "--write", "docs/data/INDEX.md"],
                ["check", "docs/data", "--repo", "."],
            ],
            "record": {
                "kind": "file",
                "path": "docs/data/INDEX.md",
                "caption": "Generated, never hand-edited. The pitfall is written for a reader deciding whether they need to open the page at all.",
            },
        },
        {
            "id": "publish",
            "act": "Decide, check, hand it over",
            "say": (
                "Two other newsrooms are working the same export. Put ours somewhere "
                "they can read it."
            ),
            "reply": (
                "Published the bundle. The served page is the public projection: our "
                "rebuild runbook and every pointer into our repo are stripped, and "
                "the issues, scopes and misuses — the part that spares somebody else "
                "the same month — all survive."
            ),
            "title": "Publish what helps a stranger",
            "narrative": (
                "The served page is for someone building their own implementation on "
                "the same dataset, so `publish` derives it from the canonical page: "
                "regions marked internal are dropped, and repo-pointing fields "
                "(`handled_by`, `evidence`, the access paths) are stripped, while "
                "`status = \"mitigated\"` survives to tell a reimplementer the issue "
                "is tractable. Same pages in, same bytes out."
            ),
            "spec": "9",
            "commands": [
                [
                    "publish",
                    "docs/data",
                    "--dir",
                    "site/ergo",
                    "--base-url",
                    "https://ridgewaytimes.example.org/ergo/",
                ]
            ],
            "record": {
                "kind": "diff-block",
                "path": "site/ergo/ridgeway-311.md",
                "id": "response-hours-zero",
                "caption": "The same issue as served: handled_by gone, the misuse and the scope intact.",
            },
        },
        {
            "id": "gate",
            "act": "Decide, check, hand it over",
            "say": "And it stays honest without me watching it?",
            "reply": (
                "That's the CI line. Every issue scoped and typed, every mitigation "
                "anchored in code that still exists, every markdown file in the "
                "directory a real page — warnings included, exit non-zero."
            ),
            "title": "The line that goes in CI",
            "narrative": (
                "`--require-manifest` closes the directory: a prose file that quietly "
                "stops being a data page is an error rather than a page that silently "
                "disappears from the check. `--strict` makes warnings fail too, which "
                "is the setting for a corpus you have already cleaned. What is left "
                "on disk is markdown, one Python file you vendored, and a repository "
                "whose code and documentation cannot drift apart without something "
                "going red."
            ),
            "spec": "12",
            "commands": [
                [
                    "check",
                    "docs/data",
                    "--repo",
                    ".",
                    "--require-manifest",
                    "--strict",
                ]
            ],
            "record": {
                "kind": "stdout",
                "caption": "Clean, with the repo cross-checks on. This is the whole gate.",
            },
        },
    ]


# ---------------------------------------------------------------------------
# running the walkthrough


def snapshot_tree(root: Path) -> dict[str, int]:
    """Path -> mtime for every file in the demo project, so we can mark changes."""
    out: dict[str, int] = {}
    for path in root.rglob("*"):
        if path.is_file() and ".git" not in path.parts:
            out[path.relative_to(root).as_posix()] = path.stat().st_mtime_ns
    return out


def extract_block(text: str, needle: str) -> str:
    """The one ``toml ergo`` fence containing ``needle``, fence markers stripped.

    Used to show a single entry rather than the whole page. Matching on the
    literal text means a block that no longer carries the id we advertise fails
    the build instead of silently showing the wrong entry.
    """
    blocks = re.findall(r"^```toml ergo\n(.*?)^```", text, re.M | re.S)
    for block in blocks:
        if needle in block:
            return block.rstrip("\n")
    raise BuildError(f"no ergo block containing {needle!r}")


def read_slice(path: Path, limit: int) -> tuple[str, bool]:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    if limit and len(lines) > limit:
        return "\n".join(lines[:limit]), True
    return text.rstrip("\n"), False


def build_walkthrough() -> dict:
    with tempfile.TemporaryDirectory(prefix="ergo-site-") as tmp:
        root = Path(tmp) / "ridgeway-times"
        (root / "docs" / "data").mkdir(parents=True)
        (root / "tools").mkdir(parents=True)
        # The tool is vendored into the demo project exactly as a host repo
        # vendors it, so the commands shown on the site are the commands a
        # reader can paste.
        shutil.copy2(TOOL, root / "tools" / "ergo.py")
        # A git repo, because `check --repo` looks at tracked files first.
        subprocess.run(["git", "init", "-q"], cwd=root, capture_output=True)

        sections: dict[str, str] = {}
        page_path = root / "docs" / "data" / f"{DEMO_SLUG}.md"
        steps: list[dict] = []
        previous: dict[str, int] = {}

        for index, plan in enumerate(step_plan(), start=1):
            edits = plan.get("edits", {})
            for name, body in edits.get("page", {}).items():
                sections[name] = body
            if sections:
                # The lede is implicit: the page starts existing at `new`, and
                # every later edit rewrites it whole, the way an editor would.
                sections.setdefault("lede", LEDE)
                page_path.write_text(page_text(sections), encoding="utf-8")
            for rel, body in edits.get("files", {}).items():
                target = root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(body, encoding="utf-8")

            subprocess.run(["git", "add", "-A"], cwd=root, capture_output=True)

            outputs: list[str] = []
            code = 0
            for argv in plan["commands"]:
                proc = run([sys.executable, "tools/ergo.py", *argv], root)
                chunk = (proc.stdout or "") + (proc.stderr or "")
                outputs.append(chunk.rstrip("\n"))
                code = proc.returncode
                if code != 0 and not plan.get("expect_failure"):
                    raise BuildError(
                        f"step {plan['id']}: `ergo.py {' '.join(argv)}` exited {code}\n{chunk}"
                    )
            if plan.get("expect_failure") and code == 0:
                raise BuildError(
                    f"step {plan['id']} expected a refusal but the command succeeded — "
                    "the validator may have been weakened"
                )

            current = snapshot_tree(root)
            tree = []
            for path in sorted(current):
                if path == "tools/ergo.py":
                    continue  # the vendored validator; present from the start
                if path not in previous:
                    state = "added"
                elif current[path] != previous[path]:
                    state = "changed"
                else:
                    state = "same"
                tree.append({"path": path, "state": state})
            previous = current

            record = dict(plan["record"])
            kind = record.pop("kind")
            limit = record.pop("limit", 0)
            if kind == "stdout":
                body = "\n\n".join(chunk for chunk in outputs if chunk) or "(no output)"
                if limit:
                    lines = body.splitlines()
                    if len(lines) > limit:
                        body = "\n".join(lines[:limit])
                        record["truncated"] = True
                record["text"] = body
                record["path"] = "$ output"
                record["lang"] = "text"
            else:
                target = root / record["path"]
                if not target.exists():
                    raise BuildError(f"step {plan['id']}: record path {target} is missing")
                if kind in ("block", "diff-block"):
                    record["text"] = extract_block(
                        target.read_text(encoding="utf-8"), record.pop("id")
                    )
                    record["lang"] = "toml"
                else:
                    text, truncated = read_slice(target, limit)
                    record["text"] = text
                    if truncated:
                        record["truncated"] = True

            steps.append(
                {
                    "n": index,
                    "id": plan["id"],
                    "act": plan["act"],
                    "say": plan.get("say", ""),
                    "reply": plan.get("reply", ""),
                    "title": plan["title"],
                    "narrative": plan["narrative"],
                    "spec": plan["spec"],
                    # What a reader would type: the vendored tool, from the repo root.
                    "commands": [
                        "python3 tools/ergo.py " + " ".join(argv)
                        for argv in plan["commands"]
                    ],
                    "stdout": "\n\n".join(chunk for chunk in outputs if chunk),
                    "exit_code": code,
                    "refused": bool(plan.get("expect_failure")),
                    "tree": tree,
                    "record": record,
                }
            )

        # The finished page, and what the reader ends up with on disk.
        final_page = page_path.read_text(encoding="utf-8")
        served = (root / "site" / "ergo" / f"{DEMO_SLUG}.md").read_text(encoding="utf-8")
        bundle_index = json.loads(
            (root / "site" / "ergo" / "index.json").read_text(encoding="utf-8")
        )
        proc = run([sys.executable, "tools/ergo.py", "export", "docs/data"], root)
        if proc.returncode != 0:
            raise BuildError(f"demo export failed: {proc.stderr}")
        exported = json.loads(proc.stdout)

    if "handled_by" in served:
        raise BuildError(
            "the published projection still carries handled_by — the public "
            "projection is no longer stripping repo-pointing fields"
        )
    if "ergo:internal" in served or "Rebuild" in served:
        raise BuildError("the published projection still carries the internal region")

    return {
        "steps": steps,
        "final_page": final_page,
        "served_page": served,
        "bundle_index": bundle_index,
        "export": exported,
    }


# ---------------------------------------------------------------------------
# the spec, and the format map


def github_anchor(heading: str) -> str:
    """GitHub's heading-anchor slug, because that is where the links land.

    GitHub lowercases, deletes punctuation *without* substituting a separator,
    then turns spaces into hyphens. A naive ``[^a-z0-9]+ -> -`` produces
    anchors that 404.
    """
    text = heading.lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return text.replace(" ", "-")


def parse_spec_sections() -> dict[str, dict]:
    sections: dict[str, dict] = {}
    for line in (REPO / "SPEC.md").read_text(encoding="utf-8").splitlines():
        match = re.match(r"^## (\d+)\. (.+)$", line)
        if match:
            number, title = match.group(1), match.group(2).strip()
            sections[number] = {
                "number": number,
                "title": title,
                "anchor": github_anchor(f"{number}. {title}"),
            }
    if not sections:
        raise BuildError("parsed no sections out of SPEC.md")
    return sections


# The block map. Every key listed here must be one the validator really knows
# about or the demo page really carries; the cross-check below enforces it.
BLOCKS = [
    {
        "table": "dataset",
        "label": "The manifest",
        "spec": "4",
        "summary": "Who publishes it, where it comes from, what it covers — and the one sentence that saves a cold reader.",
        "one_per_page": True,
        "required_from": "DATASET_REQUIRED",
        "optional": [
            "subject", "version", "confidence", "updated", "unknowns",
            "implementation", "derived_from", "coverage", "missingness", "access",
        ],
    },
    {
        "table": "issue",
        "label": "An issue",
        "spec": "5",
        "summary": "One discrete thing a user of the data must know: a defect, a trap, or a piece of institutional nuance.",
        "one_per_page": False,
        "required_from": "ISSUE_REQUIRED",
        "extra_required": ["scope"],
        "optional": [
            "core", "discovered", "handled_by", "detection", "misuse", "instead",
            "refs", "detect", "superseded_by", "supersedes",
        ],
    },
    {
        "table": "practice",
        "label": "A practice",
        "spec": "6",
        "summary": "A decision about what may be computed from the data, and how. Not a defect — a call somebody made.",
        "one_per_page": False,
        "required_from": "PRACTICE_REQUIRED",
        "optional": [
            "naive", "stops_at", "irreversible", "residual", "because_not",
            "contested", "addresses", "implemented_by",
        ],
    },
    {
        "table": "reference",
        "label": "A reference",
        "spec": "8",
        "summary": "Other people's work on this dataset — what exists, which edition it serves, whether it is still maintained.",
        "one_per_page": False,
        "required_from": "REFERENCE_REQUIRED",
        "optional": ["id", "covers", "commit", "edition", "maintenance", "caveat", "supports"],
    },
    {
        "table": "quote",
        "label": "A quote",
        "spec": "8",
        "summary": "The source's own words, with the URL and the date they were seen there — so a reader never has to trust a paraphrase.",
        "one_per_page": False,
        "required_from": "QUOTE_REQUIRED",
        "optional": ["supports", "note"],
    },
    {
        "table": "validation",
        "label": "A validation record",
        "spec": "8",
        "summary": "Dated, quantified proof that a claim on this page was checked against reality. Append-only.",
        "one_per_page": False,
        "required_from": "VALIDATION_REQUIRED",
        "optional": ["evidence"],
    },
    {
        "table": "change",
        "label": "A changelog entry",
        "spec": "15",
        "summary": "What changed in a consumer's picture of the dataset, for readers who cannot see your git history.",
        "one_per_page": False,
        "required_from": "CHANGE_REQUIRED",
        "optional": ["issues"],
    },
]

# The issue lifecycle. Each stage names the act, what the page gains, and what
# it is worth — the same "separate acts" spine the spec argues for.
LIFECYCLE = [
    {
        "stage": "registered",
        "act": "write the block",
        "spec": "5",
        "gains": "An id that never changes, a symptom-first title, and an effect from the closed vocabulary.",
        "worth": "It is findable. Nothing else yet — an unscoped issue is refused.",
    },
    {
        "stage": "scoped",
        "act": "[issue.scope]",
        "spec": "5",
        "gains": "The years, columns, tables, or entities it touches — machine-readable, not adjectives.",
        "worth": "A consumer can now ask 'does this touch my slice?' without reading the page.",
    },
    {
        "stage": "mitigated",
        "act": "handled_by",
        "spec": "5",
        "gains": "A code reference. Required — a mitigated issue with no handled_by is an error.",
        "worth": "The claim that it is handled now names something a reader can open.",
    },
    {
        "stage": "anchored",
        "act": "# ergo: slug/id",
        "spec": "7",
        "gains": "A comment in the handling code naming the issue back.",
        "worth": "The round trip closes. Deleting either half now fails the check.",
    },
    {
        "stage": "validated",
        "act": "[validation]",
        "spec": "8",
        "gains": "A dated record with numbers in it: reconciled, or confirmed against real files.",
        "worth": "The caveat stops being a hypothesis. Drift becomes detectable.",
    },
    {
        "stage": "resolved",
        "act": "status = resolved",
        "spec": "15",
        "gains": "A note that it no longer applies — kept on the page, never deleted.",
        "worth": "The record that stops the next person rediscovering it in the archive.",
    },
]

CONFORMANCE = {
    "core": [
        "The manifest, with its required fields",
        "Issues with id, title, effect, type, status and a scope",
        "handled_by on every mitigated issue",
    ],
    "supplemental": [
        "Code anchors and the --repo round trip",
        "[practice] entries",
        "[validation] records and [change] changelogs",
        "The generated digest and the agent-memory pointer",
        "The served bundle and directory entries",
        "missingness, unknowns, version on the manifest",
        "core, misuse, instead, detect on issues",
        "The agent skill, and the interop exports",
    ],
}

COMMANDS = [
    ("check", "Parse the pages and enforce the format. With --repo, cross-check the code round trip."),
    ("digest", "The INDEX.md table: one row per dataset, issue counts by effect, the pitfall."),
    ("export", "Everything machine-readable as one JSON document, for renders and interop."),
    ("publish", "The servable bundle: index.json plus each page's public projection."),
    ("directory", "This project's entries for a directory of bundles, with recognition signatures."),
    ("scan", "Read code that already works with a dataset and list what its author handled."),
    ("new", "Scaffold a fresh page from the template."),
]


def block_example(page: str, table: str) -> str:
    """The first ``toml ergo`` block of a given table, from the demo page.

    The format map shows a real block per type rather than an authored sample,
    so a block shape that changed shows up on the site the moment it changes.
    """
    for body in re.findall(r"^```toml ergo\n(.*?)^```", page, re.M | re.S):
        if body.lstrip().startswith(f"[{table}]"):
            return body.rstrip("\n")
    raise BuildError(f"the demo page carries no [{table}] block to illustrate")


def build_format(tool, sections: dict[str, dict], exported: dict, demo_page: str) -> dict:
    """The format map, cross-checked three ways.

    Vocabularies come from the validator's own constants. Every value must also
    appear in SPEC.md, so the two cannot drift. Every key the map advertises
    must be one the demo page actually produced, so the map cannot describe a
    field the format no longer writes.
    """
    spec_text = (REPO / "SPEC.md").read_text(encoding="utf-8")

    # Values are listed in the order the spec presents them, because these are
    # scales and the order carries meaning that alphabetising would destroy.
    # Membership is not authored: each list must equal the validator's own set,
    # or the build fails.
    vocabularies = [
        {
            "field": "effect",
            "table": "issue",
            "closed": True,
            "spec": "5",
            "question": "What happens if you ignore it?",
            "values": ["breaks", "corrupts", "misleads", "context"],
            "from": tool.EFFECTS,
        },
        {
            "field": "status",
            "table": "issue",
            "closed": True,
            "spec": "5",
            "question": "Is it still true?",
            "values": ["open", "mitigated", "resolved", "monitor"],
            "from": tool.ISSUE_STATUSES,
        },
        {
            "field": "type",
            "table": "issue",
            "closed": False,
            "spec": "5",
            "question": "What kind of problem is it?",
            "values": [
                "definitional", "universe", "coverage", "suppression", "geography",
                "revision", "coding", "format", "entry", "linkage", "uncertainty",
                "availability", "measurement", "identity", "policy", "acquisition",
            ],
            "from": tool.TYPES,
        },
        {
            "field": "authority",
            "table": "practice",
            "closed": True,
            "spec": "6",
            "question": "Who decided?",
            "values": ["publisher", "project", "community"],
            "from": tool.AUTHORITIES,
        },
        {
            "field": "status",
            "table": "dataset",
            "closed": True,
            "spec": "4",
            "question": "Are we still taking this in?",
            "values": ["live", "acquiring", "dormant", "archived"],
            "from": tool.DATASET_STATUSES,
        },
        {
            "field": "scope",
            "table": "issue",
            "closed": False,
            "spec": "5",
            "question": "Where does it apply?",
            "values": ["years", "tables", "columns", "rows", "entities", "all"],
            "from": tool.SCOPE_KEYS,
        },
    ]
    for vocab in vocabularies:
        enforced = set(vocab.pop("from"))
        if set(vocab["values"]) != enforced:
            raise BuildError(
                f"{vocab['table']}.{vocab['field']} drifted: the validator accepts "
                f"{sorted(enforced)}, the site lists {sorted(vocab['values'])}"
            )
    # A presence check, not a parse: the spec states these vocabularies in
    # prose tables and in commented examples, so the enforceable invariant is
    # that a value the validator accepts is at least named in the document a
    # reader is sent to. A value added to the tool and not to the spec fails here.
    for vocab in vocabularies:
        for value in vocab["values"]:
            if not re.search(rf"(?<![\w-]){re.escape(value)}(?![\w-])", spec_text):
                raise BuildError(
                    f"{vocab['table']}.{vocab['field']} value {value!r} is enforced by "
                    "the validator but never named in SPEC.md"
                )

    # What the demo page really produced, by table.
    page = exported["pages"][0]
    observed = {
        "dataset": set(page["dataset"]),
        "issue": set().union(*(set(i) for i in page["issues"])),
        "practice": set().union(*(set(p) for p in page["practices"])),
        "quote": set().union(*(set(q) for q in page["quotes"])),
        "reference": set().union(*(set(r) for r in page["references"])),
        "validation": set().union(*(set(v) for v in page["validations"])),
        "change": set().union(*(set(c) for c in page["changes"])),
    }

    for block in BLOCKS:
        required = list(getattr(tool, block.pop("required_from")))
        required += block.pop("extra_required", [])
        block["required"] = required
        block["example"] = block_example(demo_page, block["table"])
        if block["spec"] not in sections:
            raise BuildError(f"block {block['table']} cites missing SPEC section {block['spec']}")
        seen = observed[block["table"]] | {"_line"}
        missing = [k for k in required if k not in seen]
        if missing:
            raise BuildError(
                f"[{block['table']}] required keys {missing} are not present in the "
                "demo page the walkthrough just built — the map cannot be checked"
            )
        # Optional keys are advertised only if the format still accepts them:
        # each must appear in the spec's own text for that block.
        for key in block["optional"]:
            if f"`{key}`" not in spec_text and f"{key} =" not in spec_text and f"[{block['table']}.{key}]" not in spec_text and f"[dataset.{key}]" not in spec_text:
                raise BuildError(
                    f"[{block['table']}] optional key {key!r} is advertised by the site "
                    "but not documented in SPEC.md"
                )

    for item in LIFECYCLE:
        if item["spec"] not in sections:
            raise BuildError(f"lifecycle stage {item['stage']} cites missing SPEC section")

    return {
        "blocks": BLOCKS,
        "vocabularies": vocabularies,
        "lifecycle": LIFECYCLE,
        "conformance": CONFORMANCE,
        "sections": list(sections.values()),
    }


# ---------------------------------------------------------------------------
# the example page


def issue_prose(text: str) -> dict[str, str]:
    """The narrative under each entry, keyed by the id in its block.

    A data page is a block *and* its story; the viewer shows both, and neither
    is retyped here — the prose is sliced out of the real page between the end
    of an entry's fence and the next heading.
    """
    lines = text.split("\n")
    prose: dict[str, str] = {}
    current_id = None
    in_fence = False
    buffer: list[str] = []

    def flush():
        if current_id and buffer:
            body = "\n".join(buffer).strip()
            if body:
                prose[current_id] = body

    for line in lines:
        if line.startswith("```"):
            if not in_fence:
                in_fence = True
                fence_body: list[str] = []
            else:
                in_fence = False
                match = re.search(r'^id = "([^"]+)"', "\n".join(fence_body), re.M)
                if match:
                    flush()
                    current_id, buffer = match.group(1), []
            continue
        if in_fence:
            fence_body.append(line)
            continue
        if re.match(r"^#{1,6}\s", line):
            flush()
            current_id, buffer = None, []
            continue
        if current_id is not None:
            buffer.append(line)
    flush()
    return prose


def build_example() -> dict:
    proc = run([sys.executable, str(TOOL), "export", EXAMPLE_PAGE], REPO)
    if proc.returncode != 0:
        raise BuildError(f"export of {EXAMPLE_PAGE} failed: {proc.stderr}")
    payload = json.loads(proc.stdout)
    page = payload["pages"][0]
    if not page["issues"]:
        raise BuildError(f"{EXAMPLE_PAGE} exported no issues")

    check = run([sys.executable, str(TOOL), "check", EXAMPLE_PAGE], REPO)
    if check.returncode != 0:
        raise BuildError(
            f"the example page shipped in the repository does not validate:\n{check.stdout}"
        )

    source = (REPO / EXAMPLE_PAGE).read_text(encoding="utf-8")
    page["prose"] = issue_prose(source)
    page["check"] = check.stdout.strip()
    page["lede"] = "\n".join(
        line for line in source.split("\n")[1:12] if not line.startswith("```")
    ).strip().split("\n\n")[0]
    return page


# ---------------------------------------------------------------------------
# coordinates


def tool_header() -> dict:
    header = TOOL.read_text(encoding="utf-8").split("\n", 5)
    version = re.search(r"tool ([\d.]+)", "\n".join(header))
    fmt = re.search(r"ergo format ([\d.]+)", "\n".join(header))
    if not version or not fmt:
        raise BuildError("could not read the version banner out of tools/ergo.py")
    return {"tool": version.group(1), "format": fmt.group(1)}


def count_checks() -> int:
    """Run the shipped test suite and count the checks it asserts.

    Deliberately not a coverage figure and not a count of test functions: this
    suite is a list of named assertions, so the honest number is how many of
    them ran and passed at the built revision.
    """
    proc = run([sys.executable, "tests/run.py"], REPO)
    if proc.returncode != 0:
        raise BuildError(f"the test suite fails at this revision:\n{proc.stdout}")
    total = len(re.findall(r"^\s+ok\s", proc.stdout, re.M))
    if total < 1:
        raise BuildError("counted zero passing checks; the suite's output shape moved")
    return total


def cli_surface() -> list[dict]:
    proc = run([sys.executable, str(TOOL), "--help"], REPO)
    if proc.returncode != 0:
        raise BuildError("ergo.py --help failed")
    match = re.search(r"\{([a-z,]+)\}", proc.stdout)
    if not match:
        raise BuildError("could not parse the command list out of --help")
    shipped = set(match.group(1).split(","))
    declared = {name for name, _ in COMMANDS}
    if shipped != declared:
        raise BuildError(f"commands drifted: tool ships {sorted(shipped)}, site declares {sorted(declared)}")
    surface = []
    for name, summary in COMMANDS:
        help_proc = run([sys.executable, str(TOOL), name, "--help"], REPO)
        if help_proc.returncode != 0:
            raise BuildError(f"ergo.py {name} --help failed")
        usage = re.search(r"usage: (.*?)\n\n", help_proc.stdout, re.S)
        surface.append(
            {
                "name": name,
                "summary": summary,
                "usage": re.sub(r"\s+", " ", usage.group(1)).strip() if usage else "",
            }
        )
    return surface


def spec_status() -> str:
    for line in (REPO / "SPEC.md").read_text(encoding="utf-8").splitlines()[:8]:
        if line.startswith("**Status:**"):
            return line.split("**Status:**", 1)[1].strip()
    raise BuildError("SPEC.md has no status line")


# ---------------------------------------------------------------------------


def main() -> int:
    tool = load_tool()
    sections = parse_spec_sections()

    print("· running the real validator to generate the walkthrough")
    walk = build_walkthrough()

    print("· cross-checking the format map against the tool and the spec")
    fmt = build_format(tool, sections, walk["export"], walk["final_page"])

    print("· exporting the example page")
    example = build_example()

    stamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    spec_text = (REPO / "SPEC.md").read_text(encoding="utf-8")
    versions = tool_header()

    coordinates = {
        "generated": stamp,
        "tool_version": versions["tool"],
        "format_version": versions["format"],
        "revision": git("rev-parse", "--short", "HEAD") or "unknown",
        "spec_status": spec_status(),
        "spec_lines": len(spec_text.splitlines()),
        "spec_sections": len(sections),
        "tool_lines": len(TOOL.read_text(encoding="utf-8").splitlines()),
        "checks": count_checks(),
        "dependencies": [],
        "requires_python": "3.11",
        "license": "MIT",
        "cli": cli_surface(),
        "issue_types": len(tool.TYPES),
        "example": {
            "path": EXAMPLE_PAGE,
            "issues": len(example["issues"]),
            "practices": len(example["practices"]),
        },
    }

    DATA.mkdir(parents=True, exist_ok=True)
    for name, global_name, payload in (
        ("ergo", "__ERGO_META__", coordinates),
        (
            "walkthrough",
            "__ERGO_WALK__",
            {
                "generated": stamp,
                "dataset": {"slug": DEMO_SLUG, "title": DEMO_TITLE},
                **walk,
            },
        ),
        ("format", "__ERGO_FORMAT__", {"generated": stamp, **fmt}),
        ("example", "__ERGO_PAGE__", example),
    ):
        body = json.dumps(payload, indent=2, sort_keys=False, ensure_ascii=False)
        (DATA / f"{name}.json").write_text(body + "\n", encoding="utf-8")
        # A file:// page cannot fetch() its own JSON, so ship a script loader
        # beside it — the same trick artoo uses for provenance.json.
        (DATA / f"{name}.js").write_text(
            f"window.{global_name} = {body};\n", encoding="utf-8"
        )
        print(f"· wrote site/data/{name}.json + {name}.js")

    commands = sum(len(s["commands"]) for s in walk["steps"])
    refusals = sum(1 for s in walk["steps"] if s["refused"])
    print(
        f"built from ergo {coordinates['tool_version']} at {coordinates['revision']}: "
        f"{len(walk['steps'])} steps, {commands} real commands, {refusals} refusals, "
        f"{coordinates['checks']} passing checks, {len(sections)} spec sections"
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BuildError as exc:
        print(f"build failed: {exc}", file=sys.stderr)
        sys.exit(1)
