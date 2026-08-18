window.__ERGO_WALK__ = {
  "generated": "2026-08-18T02:10:57+00:00",
  "dataset": {
    "slug": "ridgeway-311",
    "title": "Ridgeway County 311 service requests"
  },
  "steps": [
    {
      "n": 1,
      "id": "scaffold",
      "act": "Open a page",
      "say": "We're building a response-time tracker on the county's 311 export. Before you write any parsing code, start a data page for it.",
      "reply": "Scaffolded one. It's a single markdown file in docs/data — a page you can read top to bottom, with TOML blocks a program can parse.",
      "title": "Scaffold the page",
      "narrative": "A data page is one file per dataset, not a database and not a directory. `new` writes the template: a manifest, the section arc the format converges on, and one empty issue to be filled or deleted.",
      "spec": "3",
      "commands": [
        "python3 tools/ergo.py new ridgeway-311 --dir docs/data"
      ],
      "stdout": "scaffolded docs/data/ridgeway-311.md",
      "exit_code": 0,
      "refused": false,
      "tree": [
        {
          "path": "docs/data/ridgeway-311.md",
          "state": "added"
        }
      ],
      "record": {
        "path": "docs/data/ridgeway-311.md",
        "caption": "The scaffold. Structured facts go in the blocks; the story goes in the prose between them.",
        "text": "# Ridgeway 311\n\nOne-paragraph lede: what this dataset is and why the project uses it.\n\n```toml ergo\n[dataset]\nergo = \"0.5\"\nslug = \"ridgeway-311\"\ntitle = \"Ridgeway 311\"\npublisher = \"\"\nsubject = \"\"            # the URL of the dataset this documents — how directories cluster pages (§10)\nsource_urls = [\"\"]\npitfall = \"\"\nstatus = \"acquiring\"\nversion = \"\"\nconfidence = \"?\"\nupdated = \"\"\nunknowns = [\"What have you not looked at? Say so — silence reads as a clean bill of health.\"]\n\n[dataset.coverage]\nyears = \"\"\ngrain = \"\"\n\n[dataset.missingness]\nzero_is_missing = false\nsource_tokens = []\n\n[dataset.access]\nkeys = []\nbuilders = []",
        "truncated": true
      }
    },
    {
      "n": 2,
      "id": "scaffold-fails",
      "act": "Open a page",
      "say": "",
      "reply": "Worth knowing up front: the scaffold does not validate. The format will not call a page valid until it says who publishes the data, where it comes from, and what the one thing that bites is.",
      "title": "An empty page is not a valid page",
      "narrative": "`check` is the gate, and the scaffold fails it. That is deliberate: empty structure is worse than absent structure, so the template's placeholders are errors until somebody has actually looked at the data. `pitfall` — one sentence naming the thing most likely to trip up a cold reader — is required, and it is the field that travels furthest, into the index and into an agent's context.",
      "spec": "4",
      "commands": [
        "python3 tools/ergo.py check docs/data"
      ],
      "stdout": "docs/data/ridgeway-311.md:5: error: [dataset] missing required field: pitfall\ndocs/data/ridgeway-311.md:5: error: [dataset] missing required field: publisher\ndocs/data/ridgeway-311.md:5: error: [dataset] missing required field: source_urls (a dataset this project produces rather than fetches declares `produced_from` instead)\ndocs/data/ridgeway-311.md:45: error: [issue] missing required field: id\ndocs/data/ridgeway-311.md:45: error: [issue] missing required field: title\ndocs/data/ridgeway-311.md:63: error: [practice] missing required field: because\ndocs/data/ridgeway-311.md:63: error: [practice] missing required field: id\ndocs/data/ridgeway-311.md:63: error: [practice] missing required field: rule\ndocs/data/ridgeway-311.md:63: error: [practice] missing required field: title\ndocs/data/ridgeway-311.md:78: error: [validation] missing required field: date\ndocs/data/ridgeway-311.md:78: error: [validation] missing required field: method\ndocs/data/ridgeway-311.md:78: error: [validation] missing required field: result\ndocs/data/ridgeway-311.md:89: error: [change] missing required field: date\n1 page(s), 1 issue(s), 1 practice(s): 13 error(s), 0 warning(s)",
      "exit_code": 1,
      "refused": true,
      "tree": [
        {
          "path": "docs/data/ridgeway-311.md",
          "state": "same"
        }
      ],
      "record": {
        "caption": "Exit code 1. Required fields are errors, not suggestions.",
        "text": "docs/data/ridgeway-311.md:5: error: [dataset] missing required field: pitfall\ndocs/data/ridgeway-311.md:5: error: [dataset] missing required field: publisher\ndocs/data/ridgeway-311.md:5: error: [dataset] missing required field: source_urls (a dataset this project produces rather than fetches declares `produced_from` instead)\ndocs/data/ridgeway-311.md:45: error: [issue] missing required field: id\ndocs/data/ridgeway-311.md:45: error: [issue] missing required field: title\ndocs/data/ridgeway-311.md:63: error: [practice] missing required field: because\ndocs/data/ridgeway-311.md:63: error: [practice] missing required field: id\ndocs/data/ridgeway-311.md:63: error: [practice] missing required field: rule\ndocs/data/ridgeway-311.md:63: error: [practice] missing required field: title\ndocs/data/ridgeway-311.md:78: error: [validation] missing required field: date\ndocs/data/ridgeway-311.md:78: error: [validation] missing required field: method\ndocs/data/ridgeway-311.md:78: error: [validation] missing required field: result\ndocs/data/ridgeway-311.md:89: error: [change] missing required field: date\n1 page(s), 1 issue(s), 1 practice(s): 13 error(s), 0 warning(s)",
        "path": "$ output",
        "lang": "text"
      }
    },
    {
      "n": 3,
      "id": "manifest",
      "act": "Open a page",
      "say": "",
      "reply": "Filled the manifest from the export and the county's landing page. Note `unknowns` — I've said what I haven't looked at, so silence doesn't read as a clean bill of health.",
      "title": "Write the manifest",
      "narrative": "The manifest is the machine-readable identity of the dataset: publisher, where the bytes come from, coverage, what the source writes when it means nothing, and the pitfall. `subject` is the identity claim — the URL naming *what dataset this is*, as opposed to where we happen to fetch it — and it is what lets a directory cluster this page with other people's pages about the same data.",
      "spec": "4",
      "commands": [
        "python3 tools/ergo.py check docs/data"
      ],
      "stdout": "1 page(s), 0 issue(s), 0 practice(s): 0 error(s), 0 warning(s)",
      "exit_code": 0,
      "refused": false,
      "tree": [
        {
          "path": "docs/data/ridgeway-311.md",
          "state": "changed"
        }
      ],
      "record": {
        "path": "docs/data/ridgeway-311.md",
        "caption": "zero_is_missing is a page-level fact about this publisher — the shape the survey found most often in government data.",
        "text": "[dataset]\nergo = \"0.5\"\nslug = \"ridgeway-311\"\ntitle = \"Ridgeway County 311 service requests\"\npublisher = \"Ridgeway County Office of Constituent Services\"\nsubject = \"https://data.ridgeway.example.gov/311\"\ncontribute = \"https://github.com/ridgeway-times/data/issues\"\nsource_urls = [\"https://data.ridgeway.example.gov/311/requests.csv\"]\npitfall = \"Every ticket still open when the county switched ticket systems was closed on the migration date, so response times computed across March 2021 are worthless unless those rows are excluded.\"\nstatus = \"live\"\nversion = \"export of 2026-06-30\"\nconfidence = \"B\"\nupdated = \"2026-07-28\"\nunknowns = [\n  \"The pre-2018 archive is published as PDF summaries only; we have not read it.\",\n  \"We do not know whether the vendor rewrites categories on old rows when the category list changes.\",\n]\n\n[dataset.coverage]\nyears = \"2018 -> 2026 (partial year)\"\ngrain = \"one row per service request\"\nentities = \"unincorporated county only; the four boroughs run their own systems\"\n\n[dataset.missingness]\nzero_is_missing = true\nsource_tokens = [\"\", \"N/A\", \"UNKNOWN\"]\n\n[dataset.access]\nkeys = [\"request_id\"]\nraw = \"data/raw/ridgeway-311/\"\nbuilders = [\"tools/load_311.py\"]\nfeeds = [\"requests\", \"response_times\"]\n\n[dataset.acquisition]\naccess = \"public\"\nterms = \"County open-data terms; attribution requested, redistribution unrestricted.\"\ncredentials = \"none\"\nformat = \"One CSV per calendar year, plus a rolling current-year file.\"\nmethod = \"Direct file URLs from the county's open-data index.\"\ncadence = \"annual, with the current year refreshed nightly\"\nlag = \"Closed requests appear the following business day.\"\nverification = \"Compare the new year file's row count against the county's published annual total.\"\nsize = \"About 40 MB per year.\"",
        "lang": "toml"
      }
    },
    {
      "n": 4,
      "id": "first-issue",
      "act": "Register what bites",
      "say": "Something's off in 2020 — a huge number of tickets close on the same day in March 2021. Look into it and write down what you find.",
      "reply": "Found it: a system migration closed everything that was open. I registered it — but `check` refused my draft twice over, and both refusals are fair.",
      "title": "The first issue, refused",
      "narrative": "Two errors, and they are the format's two hardest edges. `effect` is a closed vocabulary of four values — breaks, corrupts, misleads, context — so an agent cannot invent a severity word, and a consumer can filter on it. And an issue with no `[issue.scope]` table is rejected outright: which years, which columns, which tables. \"Some years are affected\" is a bug report, not documentation.",
      "spec": "5",
      "commands": [
        "python3 tools/ergo.py check docs/data"
      ],
      "stdout": "docs/data/ridgeway-311.md:69: error: effect must be one of ['breaks', 'corrupts', 'misleads', 'context'], got 'annoying'\ndocs/data/ridgeway-311.md:69: error: issue needs a [issue.scope] table with at least one key (or all = true)\n1 page(s), 1 issue(s), 0 practice(s): 2 error(s), 0 warning(s)",
      "exit_code": 1,
      "refused": true,
      "tree": [
        {
          "path": "docs/data/ridgeway-311.md",
          "state": "changed"
        }
      ],
      "record": {
        "caption": "The vocabulary is closed so that filtering works. The scope is required so that filtering is possible at all.",
        "text": "docs/data/ridgeway-311.md:69: error: effect must be one of ['breaks', 'corrupts', 'misleads', 'context'], got 'annoying'\ndocs/data/ridgeway-311.md:69: error: issue needs a [issue.scope] table with at least one key (or all = true)\n1 page(s), 1 issue(s), 0 practice(s): 2 error(s), 0 warning(s)",
        "path": "$ output",
        "lang": "text"
      }
    },
    {
      "n": 5,
      "id": "first-issue-fixed",
      "act": "Register what bites",
      "say": "",
      "reply": "Fixed both: it corrupts (the pipeline succeeds and the numbers are silently wrong), and it is scoped to the four years and two columns it actually touches.",
      "title": "Typed, and scoped",
      "narrative": "`corrupts` is the dangerous class: unlike `breaks`, nothing fails. The scope table is what lets an agent working on 2024 data skip this issue without an LLM call, and what stops the page from becoming a wall of caveats that everybody loads and nobody reads.",
      "spec": "5",
      "commands": [
        "python3 tools/ergo.py check docs/data"
      ],
      "stdout": "1 page(s), 1 issue(s), 0 practice(s): 0 error(s), 0 warning(s)",
      "exit_code": 0,
      "refused": false,
      "tree": [
        {
          "path": "docs/data/ridgeway-311.md",
          "state": "changed"
        }
      ],
      "record": {
        "path": "docs/data/ridgeway-311.md",
        "caption": "One block, one section. The block carries the facts; the prose under it carries the story and the numbers.",
        "text": "[issue]\nid = \"migration-close-dates\"\ntitle = \"Every ticket open on 2021-03-15 carries that date as its closed_date\"\neffect = \"corrupts\"\ntype = \"revision\"\nstatus = \"open\"\ndiscovered = \"2026-07\"\ndetection = \"closed_date = 2021-03-15 on 14,902 rows; the next busiest close date in the whole file is 231 rows\"\nmisuse = \"Reading 2020 and early 2021 response times as if they were measured. They were assigned by a data migration.\"\n\n[issue.scope]\nyears = [\"2018\", \"2019\", \"2020\", \"2021\"]\ncolumns = [\"closed_date\", \"response_hours\"]",
        "lang": "toml"
      }
    },
    {
      "n": 6,
      "id": "ward-issue",
      "act": "Register what bites",
      "say": "There's a second one. Somebody is eventually going to chart requests per ward across all the years.",
      "reply": "Registered the renumbering. `check` passed it but warned — I typed it `misleads` and never said what the misreading is.",
      "title": "A warning with a point to make",
      "narrative": "This is the class only a documented page will ever tell you: the numbers are faithful to the source and a natural reading of them is still wrong. So for `misleads` and `context`, the validator warns when `misuse` is missing — naming the foreseeable misread is data journalism's contribution to documentation, and the field is its slot.",
      "spec": "5",
      "commands": [
        "python3 tools/ergo.py check docs/data"
      ],
      "stdout": "docs/data/ridgeway-311.md:93: warning: issue ward-renumbering is misleads but names no misuse\n1 page(s), 2 issue(s), 0 practice(s): 0 error(s), 1 warning(s)",
      "exit_code": 0,
      "refused": false,
      "tree": [
        {
          "path": "docs/data/ridgeway-311.md",
          "state": "changed"
        }
      ],
      "record": {
        "caption": "A warning, not an error: the page is valid, and it is not yet useful.",
        "text": "docs/data/ridgeway-311.md:93: warning: issue ward-renumbering is misleads but names no misuse\n1 page(s), 2 issue(s), 0 practice(s): 0 error(s), 1 warning(s)",
        "path": "$ output",
        "lang": "text"
      }
    },
    {
      "n": 7,
      "id": "misuse",
      "act": "Register what bites",
      "say": "",
      "reply": "Named the misuse and the move that replaces it. That pair is the part a reader in a hurry actually reads.",
      "title": "Name the misuse, name the fix",
      "narrative": "`misuse` and `instead` are a fail/pass pair — the shape both a hurried reporter and a language model follow best. It is also the sentence most likely to survive into a caption, which is why the format asks for it in the registry rather than in a paragraph somewhere below.",
      "spec": "5",
      "commands": [
        "python3 tools/ergo.py check docs/data"
      ],
      "stdout": "1 page(s), 2 issue(s), 0 practice(s): 0 error(s), 0 warning(s)",
      "exit_code": 0,
      "refused": false,
      "tree": [
        {
          "path": "docs/data/ridgeway-311.md",
          "state": "changed"
        }
      ],
      "record": {
        "path": "docs/data/ridgeway-311.md",
        "caption": "No scope guessing: the issue is scoped to every year, because the renumbering changes what every year's ward column means.",
        "text": "[issue]\nid = \"ward-renumbering\"\ntitle = \"The 2022 redistricting reassigned ward numbers; ward 3 before and after are different places\"\neffect = \"misleads\"\ntype = \"geography\"\nstatus = \"open\"\ndiscovered = \"2026-07\"\ndetection = \"ward 9 first appears in the 2022 file; ward 6's request volume falls 71% between 2021 and 2022 with no change in population\"\nmisuse = \"Charting requests per ward as one series from 2018 to 2026. The lines cross where the boundaries moved, not where the potholes are.\"\ninstead = \"Break the series at 2022, or aggregate to the county before comparing across it.\"\n\n[issue.scope]\nyears = \"all\"\ncolumns = [\"ward\"]",
        "lang": "toml"
      }
    },
    {
      "n": 8,
      "id": "handled-by",
      "act": "Bind it to the code",
      "say": "Alright — now write the loader.",
      "reply": "Loader written, and the zeros it drops are registered as a third issue, marked mitigated with `handled_by` pointing at the function. `check --repo .` warns: the code doesn't admit what it's doing.",
      "title": "Documentation that knows where its fix lives",
      "narrative": "A `mitigated` issue must name the code that handles it — that is an error, not a warning. The warning here is the other direction: the handling code carries no anchor, so the page points at the code and the code says nothing back. That is the state in which a future cleanup deletes the guard as dead weight.",
      "spec": "7",
      "commands": [
        "python3 tools/ergo.py check docs/data --repo ."
      ],
      "stdout": "warning: docs/data/ridgeway-311.md:116: mitigated issue ridgeway-311/response-zero-unrecorded has no 'ergo: ridgeway-311/response-zero-unrecorded' anchor in its handled_by files\n1 page(s), 3 issue(s), 0 practice(s): 0 error(s), 1 warning(s)",
      "exit_code": 0,
      "refused": false,
      "tree": [
        {
          "path": "docs/data/ridgeway-311.md",
          "state": "changed"
        },
        {
          "path": "tools/load_311.py",
          "state": "added"
        }
      ],
      "record": {
        "caption": "The page knows about the code. The code does not know about the page.",
        "text": "warning: docs/data/ridgeway-311.md:116: mitigated issue ridgeway-311/response-zero-unrecorded has no 'ergo: ridgeway-311/response-zero-unrecorded' anchor in its handled_by files\n1 page(s), 3 issue(s), 0 practice(s): 0 error(s), 1 warning(s)",
        "path": "$ output",
        "lang": "text"
      }
    },
    {
      "n": 9,
      "id": "anchor",
      "act": "Bind it to the code",
      "say": "",
      "reply": "Anchored it. One comment line in the function, and the round trip closes — the page finds the code, the code names the page.",
      "title": "Close the round trip",
      "narrative": "The anchor is a comment matching `ergo: <slug>/<issue-id>`, next to the workaround. It replaces the paragraph a well-meaning developer would otherwise paste into the code, where it would drift: one line of *why this looks weird* is good manners, three lines is a fork. `grep -rn 'ergo: ridgeway-311'` now finds every workaround in the repository.",
      "spec": "7",
      "commands": [
        "python3 tools/ergo.py check docs/data --repo ."
      ],
      "stdout": "1 page(s), 3 issue(s), 0 practice(s): 0 error(s), 0 warning(s)",
      "exit_code": 0,
      "refused": false,
      "tree": [
        {
          "path": "docs/data/ridgeway-311.md",
          "state": "changed"
        },
        {
          "path": "tools/load_311.py",
          "state": "changed"
        }
      ],
      "record": {
        "path": "tools/load_311.py",
        "lang": "python",
        "caption": "The comment is the link. Deleting the guard now breaks a check instead of quietly changing a number.",
        "text": "\"\"\"Load the Ridgeway County 311 export into the warehouse.\"\"\"\n\nimport csv\nfrom statistics import median\n\nMIGRATION_CLOSE_DATE = \"2021-03-15\"\n\n\ndef response_hours(row):\n    hours = row.get(\"response_hours\")\n    if hours in (None, \"\", \"N/A\", \"UNKNOWN\"):\n        return None\n    hours = float(hours)\n    # ergo: ridgeway-311/response-zero-unrecorded — a 0 with no work order means\n    # nobody was ever dispatched, not that the call was answered instantly.\n    if hours == 0 and not row.get(\"work_order_id\"):\n        return None\n    return hours\n\n",
        "truncated": true
      }
    },
    {
      "n": 10,
      "id": "rename",
      "act": "Bind it to the code",
      "say": "'response-zero-unrecorded' is a mouthful. Rename it.",
      "reply": "Renamed it on the page — and `check` stopped me with an error, because the anchor in the loader now names an issue that doesn't exist. Exit 1.",
      "title": "Ids are permanent for a reason",
      "narrative": "An anchor naming an unknown issue is an error, never a warning: it means the documentation was renamed or deleted out from under the code, and the code is now carrying an explanation nobody can look up. This is the failure the round trip exists to catch, and it is the reason the spec asks for a tombstone rather than a clean rename.",
      "spec": "15",
      "commands": [
        "python3 tools/ergo.py check docs/data --repo ."
      ],
      "stdout": "error: tools/load_311.py:14: anchor 'ergo: ridgeway-311/response-zero-unrecorded' names an unknown issue\nwarning: docs/data/ridgeway-311.md:116: mitigated issue ridgeway-311/response-hours-zero has no 'ergo: ridgeway-311/response-hours-zero' anchor in its handled_by files\n1 page(s), 3 issue(s), 0 practice(s): 1 error(s), 1 warning(s)",
      "exit_code": 1,
      "refused": true,
      "tree": [
        {
          "path": "docs/data/ridgeway-311.md",
          "state": "changed"
        },
        {
          "path": "tools/load_311.py",
          "state": "same"
        }
      ],
      "record": {
        "caption": "Exit code 1. The rename is not done until the code agrees.",
        "text": "error: tools/load_311.py:14: anchor 'ergo: ridgeway-311/response-zero-unrecorded' names an unknown issue\nwarning: docs/data/ridgeway-311.md:116: mitigated issue ridgeway-311/response-hours-zero has no 'ergo: ridgeway-311/response-hours-zero' anchor in its handled_by files\n1 page(s), 3 issue(s), 0 practice(s): 1 error(s), 1 warning(s)",
        "path": "$ output",
        "lang": "text"
      }
    },
    {
      "n": 11,
      "id": "tombstone",
      "act": "Bind it to the code",
      "say": "",
      "reply": "Updated the anchor and left a tombstone: the old id stays on the page as resolved, pointing at the new one, so anybody's stale link lands somewhere that explains itself.",
      "title": "Leave a tombstone",
      "narrative": "Issue ids are permanent because they are cited — in code anchors, in other people's pages, in commit messages. A rename creates the new id and keeps the old entry for one release, marked `resolved` with `superseded_by`, so stale references fail loudly rather than silently resolving to nothing.",
      "spec": "15",
      "commands": [
        "python3 tools/ergo.py check docs/data --repo ."
      ],
      "stdout": "1 page(s), 4 issue(s), 0 practice(s): 0 error(s), 0 warning(s)",
      "exit_code": 0,
      "refused": false,
      "tree": [
        {
          "path": "docs/data/ridgeway-311.md",
          "state": "changed"
        },
        {
          "path": "tools/load_311.py",
          "state": "changed"
        }
      ],
      "record": {
        "path": "docs/data/ridgeway-311.md",
        "caption": "A tombstone: status resolved, superseded_by the new id. Kept for one release, then dropped.",
        "text": "[issue]\nid = \"response-zero-unrecorded\"\ntitle = \"Renamed to response-hours-zero on 2026-07-28; kept so stale anchors fail loudly\"\neffect = \"corrupts\"\ntype = \"entry\"\nstatus = \"resolved\"\nsuperseded_by = \"response-hours-zero\"\n\n[issue.scope]\nall = true",
        "lang": "toml"
      }
    },
    {
      "n": 12,
      "id": "practice",
      "act": "Decide, check, hand it over",
      "say": "So what's the actual number? How fast does the county respond?",
      "reply": "Before I give you a number I've written down how it's computed — as a practice, not an issue. The defects are the county's; this decision is ours, and a different newsroom would rightly make it differently.",
      "title": "A decision is not a defect",
      "narrative": "Two tests separate them. Deletion: would this still be true if we deleted all our code? The migration backfill would; the median would not. Disagreement: could a competent team rightly decide otherwise? Here, yes — a newsroom holding the county to its own published method would use the mean, which is why this one carries `contested`. `naive` names the move being ruled out, `residual` names the error that remains **and its direction**, and `addresses` ties the practice back to the defects underneath it.",
      "spec": "6",
      "commands": [
        "python3 tools/ergo.py check docs/data --repo ."
      ],
      "stdout": "1 page(s), 4 issue(s), 1 practice(s): 0 error(s), 0 warning(s)",
      "exit_code": 0,
      "refused": false,
      "tree": [
        {
          "path": "docs/data/ridgeway-311.md",
          "state": "changed"
        },
        {
          "path": "tools/load_311.py",
          "state": "changed"
        }
      ],
      "record": {
        "path": "docs/data/ridgeway-311.md",
        "caption": "One defect can have several handlings, chosen by the question being asked — which is why practices are their own block.",
        "text": "[practice]\nid = \"median-response-worked-only\"\ntitle = \"Response time is the median over tickets that had a work order, excluding the migration date\"\nquestion = \"How fast does the county respond to a complaint?\"\nauthority = \"project\"\nrule = [\n  \"Restrict to tickets with a work_order_id and a closed_date.\",\n  \"Drop every ticket whose closed_date is the 2021-03-15 migration date.\",\n  \"Report the median by year, with n.\",\n]\nnaive = \"The mean of response_hours over every closed ticket, which folds in the intake zeros and the migration backfill.\"\nbecause = \"Both defects push the average down, and they push it down hardest in exactly the years a reader wants to compare against.\"\nresidual = \"Dropping the migration date also drops roughly 400 tickets genuinely closed that day. The error runs toward reporting the county as slower than it was, which is the safer direction.\"\ncontested = true\naddresses = [\"migration-close-dates\", \"response-hours-zero\"]\nimplemented_by = [\"tools/load_311.py#median_response\"]",
        "lang": "toml"
      }
    },
    {
      "n": 13,
      "id": "validation",
      "act": "Decide, check, hand it over",
      "say": "Does our number survive contact with the county's own report?",
      "reply": "Close, and the gap is explainable: ours 41.5 hours against their 42 for 2024, and the difference is the boroughs. Recorded as a dated validation record with the numbers in it.",
      "title": "Record the reconciliation",
      "narrative": "A caveat you have not tested is a hypothesis. Two blocks answer that: a quote shows what the source itself says, verbatim and dated, so nobody has to trust a paraphrase; a validation record shows what happened when the claim met real files. Both accumulate — never edit an old record, add a new one. The numbers are what let the *next* check detect drift.",
      "spec": "8",
      "commands": [
        "python3 tools/ergo.py check docs/data --repo ."
      ],
      "stdout": "1 page(s), 4 issue(s), 1 practice(s): 0 error(s), 0 warning(s)",
      "exit_code": 0,
      "refused": false,
      "tree": [
        {
          "path": "docs/data/ridgeway-311.md",
          "state": "changed"
        },
        {
          "path": "tools/load_311.py",
          "state": "same"
        }
      ],
      "record": {
        "path": "docs/data/ridgeway-311.md",
        "caption": "\"7 of 7 figures match within rounding\" beats \"we checked\" — a number is what the next person can re-run.",
        "text": "[validation]\ndate = \"2026-07-28\"\nmethod = \"reconciled our 2024 median against the county's published annual service report\"\nresult = \"ours 41.5 h vs the county's 42 h for 2024; the gap is the four boroughs, which the county includes and we exclude\"\nevidence = \"docs/data/ridgeway-311-reconciliation.md\"",
        "lang": "toml"
      }
    },
    {
      "n": 14,
      "id": "digest",
      "act": "Decide, check, hand it over",
      "say": "Make sure the next person — or the next model — finds this.",
      "reply": "Generated the index and planted a three-line pointer in the desk's CLAUDE.md. Agents don't discover documentation at well-known paths; they go where they're pointed.",
      "title": "The agent entry point",
      "narrative": "The digest is one row per dataset: status, issue counts by effect, core flagged, and the pitfall line. It is the first of three disclosure tiers — digest, then the page's manifest and issue titles, then the issue's own section — so a working agent can spend a hundred tokens or three thousand depending on what it is about to touch.",
      "spec": "9",
      "commands": [
        "python3 tools/ergo.py digest docs/data --write docs/data/INDEX.md",
        "python3 tools/ergo.py check docs/data --repo ."
      ],
      "stdout": "wrote docs/data/INDEX.md\n\n1 page(s), 4 issue(s), 1 practice(s): 0 error(s), 0 warning(s)",
      "exit_code": 0,
      "refused": false,
      "tree": [
        {
          "path": "CLAUDE.md",
          "state": "added"
        },
        {
          "path": "docs/data/INDEX.md",
          "state": "added"
        },
        {
          "path": "docs/data/ridgeway-311.md",
          "state": "changed"
        },
        {
          "path": "tools/load_311.py",
          "state": "same"
        }
      ],
      "record": {
        "path": "docs/data/INDEX.md",
        "caption": "Generated, never hand-edited. The pitfall is written for a reader deciding whether they need to open the page at all.",
        "text": "# Data pages\n\n<!-- generated by ergo.py digest — do not hand-edit -->\n\n| dataset | status | updated | issues | practices | the pitfall |\n|---|---|---|---|---|---|\n| [Ridgeway County 311 service requests](ridgeway-311.md) | live | 2026-07-28 | 4 (3 corrupts · 1 misleads · 1 core) | 1 (1 contested) | Every ticket still open when the county switched ticket systems was closed on the migration date, so response times computed across March 2021 are worthless unless those rows are excluded. |"
      }
    },
    {
      "n": 15,
      "id": "publish",
      "act": "Decide, check, hand it over",
      "say": "Two other newsrooms are working the same export. Put ours somewhere they can read it.",
      "reply": "Published the bundle. The served page is the public projection: our rebuild runbook and every pointer into our repo are stripped, and the issues, scopes and misuses — the part that spares somebody else the same month — all survive.",
      "title": "Publish what helps a stranger",
      "narrative": "The served page is for someone building their own implementation on the same dataset, so `publish` derives it from the canonical page: regions marked internal are dropped, and repo-pointing fields (`handled_by`, `evidence`, the access paths) are stripped, while `status = \"mitigated\"` survives to tell a reimplementer the issue is tractable. Same pages in, same bytes out.",
      "spec": "9",
      "commands": [
        "python3 tools/ergo.py publish docs/data --dir site/ergo --base-url https://ridgewaytimes.example.org/ergo/"
      ],
      "stdout": "published 1 page(s) + index.json -> site/ergo",
      "exit_code": 0,
      "refused": false,
      "tree": [
        {
          "path": "CLAUDE.md",
          "state": "same"
        },
        {
          "path": "docs/data/INDEX.md",
          "state": "same"
        },
        {
          "path": "docs/data/ridgeway-311.md",
          "state": "changed"
        },
        {
          "path": "site/ergo/index.json",
          "state": "added"
        },
        {
          "path": "site/ergo/ridgeway-311.md",
          "state": "added"
        },
        {
          "path": "tools/load_311.py",
          "state": "same"
        }
      ],
      "record": {
        "path": "site/ergo/ridgeway-311.md",
        "caption": "The same issue as served: handled_by gone, the misuse and the scope intact.",
        "text": "[issue]\nid = \"response-hours-zero\"\ntitle = \"response_hours is 0 when intake closed the ticket without opening a work order\"\neffect = \"corrupts\"\ntype = \"entry\"\nstatus = \"mitigated\"\ncore = true\ndiscovered = \"2026-07\"\ndetection = \"response_hours = 0 with an empty work_order_id — 8.1% of closed tickets\"\nmisuse = \"Averaging response_hours over closed tickets. The zeros are 'never dispatched', not 'answered instantly', and they pull the mean down by about a third.\"\n\n[issue.scope]\nall = true\ncolumns = [\"response_hours\"]",
        "lang": "toml"
      }
    },
    {
      "n": 16,
      "id": "gate",
      "act": "Decide, check, hand it over",
      "say": "And it stays honest without me watching it?",
      "reply": "That's the CI line. Every issue scoped and typed, every mitigation anchored in code that still exists, every markdown file in the directory a real page — warnings included, exit non-zero.",
      "title": "The line that goes in CI",
      "narrative": "`--require-manifest` closes the directory: a prose file that quietly stops being a data page is an error rather than a page that silently disappears from the check. `--strict` makes warnings fail too, which is the setting for a corpus you have already cleaned. What is left on disk is markdown, one Python file you vendored, and a repository whose code and documentation cannot drift apart without something going red.",
      "spec": "12",
      "commands": [
        "python3 tools/ergo.py check docs/data --repo . --require-manifest --strict"
      ],
      "stdout": "1 page(s), 4 issue(s), 1 practice(s): 0 error(s), 0 warning(s)",
      "exit_code": 0,
      "refused": false,
      "tree": [
        {
          "path": "CLAUDE.md",
          "state": "same"
        },
        {
          "path": "docs/data/INDEX.md",
          "state": "same"
        },
        {
          "path": "docs/data/ridgeway-311.md",
          "state": "changed"
        },
        {
          "path": "site/ergo/index.json",
          "state": "same"
        },
        {
          "path": "site/ergo/ridgeway-311.md",
          "state": "same"
        },
        {
          "path": "tools/load_311.py",
          "state": "same"
        }
      ],
      "record": {
        "caption": "Clean, with the repo cross-checks on. This is the whole gate.",
        "text": "1 page(s), 4 issue(s), 1 practice(s): 0 error(s), 0 warning(s)",
        "path": "$ output",
        "lang": "text"
      }
    }
  ],
  "final_page": "# Ridgeway County 311 service requests\n\nReporter's notebook for the county's 311 export: where it comes from, what it\ncounts, and every oddity worth knowing before you publish a response time.\n\n```toml ergo\n[dataset]\nergo = \"0.5\"\nslug = \"ridgeway-311\"\ntitle = \"Ridgeway County 311 service requests\"\npublisher = \"Ridgeway County Office of Constituent Services\"\nsubject = \"https://data.ridgeway.example.gov/311\"\ncontribute = \"https://github.com/ridgeway-times/data/issues\"\nsource_urls = [\"https://data.ridgeway.example.gov/311/requests.csv\"]\npitfall = \"Every ticket still open when the county switched ticket systems was closed on the migration date, so response times computed across March 2021 are worthless unless those rows are excluded.\"\nstatus = \"live\"\nversion = \"export of 2026-06-30\"\nconfidence = \"B\"\nupdated = \"2026-07-28\"\nunknowns = [\n  \"The pre-2018 archive is published as PDF summaries only; we have not read it.\",\n  \"We do not know whether the vendor rewrites categories on old rows when the category list changes.\",\n]\n\n[dataset.coverage]\nyears = \"2018 -> 2026 (partial year)\"\ngrain = \"one row per service request\"\nentities = \"unincorporated county only; the four boroughs run their own systems\"\n\n[dataset.missingness]\nzero_is_missing = true\nsource_tokens = [\"\", \"N/A\", \"UNKNOWN\"]\n\n[dataset.access]\nkeys = [\"request_id\"]\nraw = \"data/raw/ridgeway-311/\"\nbuilders = [\"tools/load_311.py\"]\nfeeds = [\"requests\", \"response_times\"]\n\n[dataset.acquisition]\naccess = \"public\"\nterms = \"County open-data terms; attribution requested, redistribution unrestricted.\"\ncredentials = \"none\"\nformat = \"One CSV per calendar year, plus a rolling current-year file.\"\nmethod = \"Direct file URLs from the county's open-data index.\"\ncadence = \"annual, with the current year refreshed nightly\"\nlag = \"Closed requests appear the following business day.\"\nverification = \"Compare the new year file's row count against the county's published annual total.\"\nsize = \"About 40 MB per year.\"\n```\n\n## What it is\n\nEvery call, web form, and app report the county logs, one row per request,\nwith a category, a ward, an opened timestamp, a closed timestamp, and a\nresponse time the vendor computes for us. It is the only county-wide record of\nwhat residents ask for, which is why it ends up under a lot of stories.\n\n## Access\n\nA nightly CSV export behind a stable URL. No API, no pagination, no\nauthentication; the file is rewritten in place each night, so yesterday's\nexport is not recoverable from the source once it is gone.\n\n## Issues\n\n### Half of 2020's tickets close on the same day in March 2021\n\n```toml ergo\n[issue]\nid = \"migration-close-dates\"\ntitle = \"Every ticket open on 2021-03-15 carries that date as its closed_date\"\neffect = \"corrupts\"\ntype = \"revision\"\nstatus = \"open\"\ndiscovered = \"2026-07\"\ndetection = \"closed_date = 2021-03-15 on 14,902 rows; the next busiest close date in the whole file is 231 rows\"\nmisuse = \"Reading 2020 and early 2021 response times as if they were measured. They were assigned by a data migration.\"\n\n[issue.scope]\nyears = [\"2018\", \"2019\", \"2020\", \"2021\"]\ncolumns = [\"closed_date\", \"response_hours\"]\n```\n\nThe county moved from the old ticket system to the current vendor on\n2021-03-15, and the migration wrote a close date onto everything that was\nstill open. Those tickets were not resolved that day; most of them were never\nresolved at all. A 2020 request that sat for eleven months reports a response\ntime of eleven months and looks, in the data, like a case that was worked.\n\n### Ward numbers mean different places before and after 2022\n\n```toml ergo\n[issue]\nid = \"ward-renumbering\"\ntitle = \"The 2022 redistricting reassigned ward numbers; ward 3 before and after are different places\"\neffect = \"misleads\"\ntype = \"geography\"\nstatus = \"open\"\ndiscovered = \"2026-07\"\ndetection = \"ward 9 first appears in the 2022 file; ward 6's request volume falls 71% between 2021 and 2022 with no change in population\"\nmisuse = \"Charting requests per ward as one series from 2018 to 2026. The lines cross where the boundaries moved, not where the potholes are.\"\ninstead = \"Break the series at 2022, or aggregate to the county before comparing across it.\"\n\n[issue.scope]\nyears = \"all\"\ncolumns = [\"ward\"]\n```\n\nThe county redrew wards after the 2020 census and renumbered them rather than\nkeeping the old labels. Nothing in the export marks the change: the column is\ncalled `ward` in every year and holds a small integer in every year.\n\n### response_hours is 0 for tickets nobody ever worked\n\n```toml ergo\n[issue]\nid = \"response-hours-zero\"\ntitle = \"response_hours is 0 when intake closed the ticket without opening a work order\"\neffect = \"corrupts\"\ntype = \"entry\"\nstatus = \"mitigated\"\ncore = true\ndiscovered = \"2026-07\"\nhandled_by = [\"tools/load_311.py#response_hours\"]\ndetection = \"response_hours = 0 with an empty work_order_id — 8.1% of closed tickets\"\nmisuse = \"Averaging response_hours over closed tickets. The zeros are 'never dispatched', not 'answered instantly', and they pull the mean down by about a third.\"\n\n[issue.scope]\nall = true\ncolumns = [\"response_hours\"]\n```\n\nDuplicate reports, wrong-agency referrals, and calls resolved on the phone are\nclosed at intake with no work order. The vendor's response-time calculation\nsubtracts the timestamps anyway and gets zero. The field is not missing, which\nis what makes it dangerous: it survives every null check.\n\n### (renamed) response-zero-unrecorded\n\n```toml ergo\n[issue]\nid = \"response-zero-unrecorded\"\ntitle = \"Renamed to response-hours-zero on 2026-07-28; kept so stale anchors fail loudly\"\neffect = \"corrupts\"\ntype = \"entry\"\nstatus = \"resolved\"\nsuperseded_by = \"response-hours-zero\"\n\n[issue.scope]\nall = true\n```\n\nA tombstone, not an issue: ids are permanent, so a rename leaves the old entry\nbehind for one release with the new id recorded on it.\n\n## Practices\n\n### Response time is a median over worked tickets, and the migration date is dropped\n\n```toml ergo\n[practice]\nid = \"median-response-worked-only\"\ntitle = \"Response time is the median over tickets that had a work order, excluding the migration date\"\nquestion = \"How fast does the county respond to a complaint?\"\nauthority = \"project\"\nrule = [\n  \"Restrict to tickets with a work_order_id and a closed_date.\",\n  \"Drop every ticket whose closed_date is the 2021-03-15 migration date.\",\n  \"Report the median by year, with n.\",\n]\nnaive = \"The mean of response_hours over every closed ticket, which folds in the intake zeros and the migration backfill.\"\nbecause = \"Both defects push the average down, and they push it down hardest in exactly the years a reader wants to compare against.\"\nresidual = \"Dropping the migration date also drops roughly 400 tickets genuinely closed that day. The error runs toward reporting the county as slower than it was, which is the safer direction.\"\ncontested = true\naddresses = [\"migration-close-dates\", \"response-hours-zero\"]\nimplemented_by = [\"tools/load_311.py#median_response\"]\n```\n\nThe county's own annual report uses a mean over all closed tickets, so our\nnumber will not match theirs and we say so in the note under every chart. A\nnewsroom that wanted to hold the county to its own published method would\nrightly make the opposite call — hence `contested`.\n\n## Prior work\n\n```toml ergo\n[reference]\nkind = \"documentation\"\nurl = \"https://ridgeway.example.gov/311/data-dictionary\"\nobserved = \"2026-07-28\"\ncovers = \"The county's field-by-field dictionary for the 311 export, including the closure-code list.\"\nmaintenance = \"dated\"\ncaveat = \"Last revised before the 2023 code change; three closure codes in the current export are absent from it.\"\n```\n\n## Evidence\n\nThe county publishes its own figure, so quote it rather than paraphrase it —\n`text` is theirs, `note` is ours, and `retrieved` is what makes it re-checkable\na year from now when the page has been rewritten.\n\n```toml ergo\n[quote]\ntext = \"Across all service requests closed in 2024, the median time to close was 42 hours.\"\nsource = \"https://ridgeway.example.gov/311/annual-report-2024\"\nretrieved = \"2026-07-28\"\nsupports = [\"median-response-worked-only\"]\nnote = \"Their 42 hours counts the four boroughs; ours does not, and that is the whole of the gap below.\"\n```\n\n```toml ergo\n[validation]\ndate = \"2026-07-28\"\nmethod = \"reconciled our 2024 median against the county's published annual service report\"\nresult = \"ours 41.5 h vs the county's 42 h for 2024; the gap is the four boroughs, which the county includes and we exclude\"\nevidence = \"docs/data/ridgeway-311-reconciliation.md\"\n```\n\n<!-- ergo:internal -->\n## Rebuild\n\nFetch the nightly export into `data/raw/ridgeway-311/` and run\n`python3 tools/load_311.py --rebuild`. The loader is idempotent; it truncates\nand reloads both feeds.\n<!-- /ergo:internal -->\n\n## Changelog\n\n```toml ergo\n[change]\ndate = \"2026-07-28\"\nnote = \"First pass over the 311 export: migration close dates, ward renumbering, and the intake zeros registered; response-time practice recorded.\"\nissues = [\"migration-close-dates\", \"ward-renumbering\", \"response-hours-zero\"]\n```\n",
  "served_page": "# Ridgeway County 311 service requests\n\nReporter's notebook for the county's 311 export: where it comes from, what it\ncounts, and every oddity worth knowing before you publish a response time.\n\n```toml ergo\n[dataset]\nergo = \"0.5\"\nslug = \"ridgeway-311\"\ntitle = \"Ridgeway County 311 service requests\"\npublisher = \"Ridgeway County Office of Constituent Services\"\nsubject = \"https://data.ridgeway.example.gov/311\"\ncontribute = \"https://github.com/ridgeway-times/data/issues\"\nsource_urls = [\"https://data.ridgeway.example.gov/311/requests.csv\"]\npitfall = \"Every ticket still open when the county switched ticket systems was closed on the migration date, so response times computed across March 2021 are worthless unless those rows are excluded.\"\nstatus = \"live\"\nversion = \"export of 2026-06-30\"\nconfidence = \"B\"\nupdated = \"2026-07-28\"\nunknowns = [\n  \"The pre-2018 archive is published as PDF summaries only; we have not read it.\",\n  \"We do not know whether the vendor rewrites categories on old rows when the category list changes.\",\n]\n\n[dataset.coverage]\nyears = \"2018 -> 2026 (partial year)\"\ngrain = \"one row per service request\"\nentities = \"unincorporated county only; the four boroughs run their own systems\"\n\n[dataset.missingness]\nzero_is_missing = true\nsource_tokens = [\"\", \"N/A\", \"UNKNOWN\"]\n\n[dataset.access]\nkeys = [\"request_id\"]\n\n[dataset.acquisition]\naccess = \"public\"\nterms = \"County open-data terms; attribution requested, redistribution unrestricted.\"\ncredentials = \"none\"\nformat = \"One CSV per calendar year, plus a rolling current-year file.\"\nmethod = \"Direct file URLs from the county's open-data index.\"\ncadence = \"annual, with the current year refreshed nightly\"\nlag = \"Closed requests appear the following business day.\"\nverification = \"Compare the new year file's row count against the county's published annual total.\"\nsize = \"About 40 MB per year.\"\n```\n\n## What it is\n\nEvery call, web form, and app report the county logs, one row per request,\nwith a category, a ward, an opened timestamp, a closed timestamp, and a\nresponse time the vendor computes for us. It is the only county-wide record of\nwhat residents ask for, which is why it ends up under a lot of stories.\n\n## Access\n\nA nightly CSV export behind a stable URL. No API, no pagination, no\nauthentication; the file is rewritten in place each night, so yesterday's\nexport is not recoverable from the source once it is gone.\n\n## Issues\n\n### Half of 2020's tickets close on the same day in March 2021\n\n```toml ergo\n[issue]\nid = \"migration-close-dates\"\ntitle = \"Every ticket open on 2021-03-15 carries that date as its closed_date\"\neffect = \"corrupts\"\ntype = \"revision\"\nstatus = \"open\"\ndiscovered = \"2026-07\"\ndetection = \"closed_date = 2021-03-15 on 14,902 rows; the next busiest close date in the whole file is 231 rows\"\nmisuse = \"Reading 2020 and early 2021 response times as if they were measured. They were assigned by a data migration.\"\n\n[issue.scope]\nyears = [\"2018\", \"2019\", \"2020\", \"2021\"]\ncolumns = [\"closed_date\", \"response_hours\"]\n```\n\nThe county moved from the old ticket system to the current vendor on\n2021-03-15, and the migration wrote a close date onto everything that was\nstill open. Those tickets were not resolved that day; most of them were never\nresolved at all. A 2020 request that sat for eleven months reports a response\ntime of eleven months and looks, in the data, like a case that was worked.\n\n### Ward numbers mean different places before and after 2022\n\n```toml ergo\n[issue]\nid = \"ward-renumbering\"\ntitle = \"The 2022 redistricting reassigned ward numbers; ward 3 before and after are different places\"\neffect = \"misleads\"\ntype = \"geography\"\nstatus = \"open\"\ndiscovered = \"2026-07\"\ndetection = \"ward 9 first appears in the 2022 file; ward 6's request volume falls 71% between 2021 and 2022 with no change in population\"\nmisuse = \"Charting requests per ward as one series from 2018 to 2026. The lines cross where the boundaries moved, not where the potholes are.\"\ninstead = \"Break the series at 2022, or aggregate to the county before comparing across it.\"\n\n[issue.scope]\nyears = \"all\"\ncolumns = [\"ward\"]\n```\n\nThe county redrew wards after the 2020 census and renumbered them rather than\nkeeping the old labels. Nothing in the export marks the change: the column is\ncalled `ward` in every year and holds a small integer in every year.\n\n### response_hours is 0 for tickets nobody ever worked\n\n```toml ergo\n[issue]\nid = \"response-hours-zero\"\ntitle = \"response_hours is 0 when intake closed the ticket without opening a work order\"\neffect = \"corrupts\"\ntype = \"entry\"\nstatus = \"mitigated\"\ncore = true\ndiscovered = \"2026-07\"\ndetection = \"response_hours = 0 with an empty work_order_id — 8.1% of closed tickets\"\nmisuse = \"Averaging response_hours over closed tickets. The zeros are 'never dispatched', not 'answered instantly', and they pull the mean down by about a third.\"\n\n[issue.scope]\nall = true\ncolumns = [\"response_hours\"]\n```\n\nDuplicate reports, wrong-agency referrals, and calls resolved on the phone are\nclosed at intake with no work order. The vendor's response-time calculation\nsubtracts the timestamps anyway and gets zero. The field is not missing, which\nis what makes it dangerous: it survives every null check.\n\n### (renamed) response-zero-unrecorded\n\n```toml ergo\n[issue]\nid = \"response-zero-unrecorded\"\ntitle = \"Renamed to response-hours-zero on 2026-07-28; kept so stale anchors fail loudly\"\neffect = \"corrupts\"\ntype = \"entry\"\nstatus = \"resolved\"\nsuperseded_by = \"response-hours-zero\"\n\n[issue.scope]\nall = true\n```\n\nA tombstone, not an issue: ids are permanent, so a rename leaves the old entry\nbehind for one release with the new id recorded on it.\n\n## Practices\n\n### Response time is a median over worked tickets, and the migration date is dropped\n\n```toml ergo\n[practice]\nid = \"median-response-worked-only\"\ntitle = \"Response time is the median over tickets that had a work order, excluding the migration date\"\nquestion = \"How fast does the county respond to a complaint?\"\nauthority = \"project\"\nrule = [\n  \"Restrict to tickets with a work_order_id and a closed_date.\",\n  \"Drop every ticket whose closed_date is the 2021-03-15 migration date.\",\n  \"Report the median by year, with n.\",\n]\nnaive = \"The mean of response_hours over every closed ticket, which folds in the intake zeros and the migration backfill.\"\nbecause = \"Both defects push the average down, and they push it down hardest in exactly the years a reader wants to compare against.\"\nresidual = \"Dropping the migration date also drops roughly 400 tickets genuinely closed that day. The error runs toward reporting the county as slower than it was, which is the safer direction.\"\ncontested = true\naddresses = [\"migration-close-dates\", \"response-hours-zero\"]\n```\n\nThe county's own annual report uses a mean over all closed tickets, so our\nnumber will not match theirs and we say so in the note under every chart. A\nnewsroom that wanted to hold the county to its own published method would\nrightly make the opposite call — hence `contested`.\n\n## Prior work\n\n```toml ergo\n[reference]\nkind = \"documentation\"\nurl = \"https://ridgeway.example.gov/311/data-dictionary\"\nobserved = \"2026-07-28\"\ncovers = \"The county's field-by-field dictionary for the 311 export, including the closure-code list.\"\nmaintenance = \"dated\"\ncaveat = \"Last revised before the 2023 code change; three closure codes in the current export are absent from it.\"\n```\n\n## Evidence\n\nThe county publishes its own figure, so quote it rather than paraphrase it —\n`text` is theirs, `note` is ours, and `retrieved` is what makes it re-checkable\na year from now when the page has been rewritten.\n\n```toml ergo\n[quote]\ntext = \"Across all service requests closed in 2024, the median time to close was 42 hours.\"\nsource = \"https://ridgeway.example.gov/311/annual-report-2024\"\nretrieved = \"2026-07-28\"\nsupports = [\"median-response-worked-only\"]\nnote = \"Their 42 hours counts the four boroughs; ours does not, and that is the whole of the gap below.\"\n```\n\n```toml ergo\n[validation]\ndate = \"2026-07-28\"\nmethod = \"reconciled our 2024 median against the county's published annual service report\"\nresult = \"ours 41.5 h vs the county's 42 h for 2024; the gap is the four boroughs, which the county includes and we exclude\"\n```\n\n## Changelog\n\n```toml ergo\n[change]\ndate = \"2026-07-28\"\nnote = \"First pass over the 311 export: migration close dates, ward renumbering, and the intake zeros registered; response-time practice recorded.\"\nissues = [\"migration-close-dates\", \"ward-renumbering\", \"response-hours-zero\"]\n```\n",
  "bundle_index": {
    "ergo": "0.5",
    "datasets": [
      {
        "slug": "ridgeway-311",
        "title": "Ridgeway County 311 service requests",
        "publisher": "Ridgeway County Office of Constituent Services",
        "status": "live",
        "confidence": "B",
        "updated": "2026-07-28",
        "subject": "https://data.ridgeway.example.gov/311",
        "derived_from": [],
        "version": "export of 2026-06-30",
        "implementation": "",
        "pitfall": "Every ticket still open when the county switched ticket systems was closed on the migration date, so response times computed across March 2021 are worthless unless those rows are excluded.",
        "coverage": {
          "years": "2018 -> 2026 (partial year)",
          "grain": "one row per service request",
          "entities": "unincorporated county only; the four boroughs run their own systems"
        },
        "missingness": {
          "zero_is_missing": true,
          "source_tokens": [
            "",
            "N/A",
            "UNKNOWN"
          ]
        },
        "unknowns": [
          "The pre-2018 archive is published as PDF summaries only; we have not read it.",
          "We do not know whether the vendor rewrites categories on old rows when the category list changes."
        ],
        "source_urls": [
          "https://data.ridgeway.example.gov/311/requests.csv"
        ],
        "counts": {
          "issues": 4,
          "core": 1,
          "practices": 1,
          "effects": {
            "corrupts": 3,
            "misleads": 1
          }
        },
        "issues": [
          {
            "id": "migration-close-dates",
            "title": "Every ticket open on 2021-03-15 carries that date as its closed_date",
            "effect": "corrupts",
            "type": "revision",
            "status": "open",
            "core": false
          },
          {
            "id": "ward-renumbering",
            "title": "The 2022 redistricting reassigned ward numbers; ward 3 before and after are different places",
            "effect": "misleads",
            "type": "geography",
            "status": "open",
            "core": false
          },
          {
            "id": "response-hours-zero",
            "title": "response_hours is 0 when intake closed the ticket without opening a work order",
            "effect": "corrupts",
            "type": "entry",
            "status": "mitigated",
            "core": true
          },
          {
            "id": "response-zero-unrecorded",
            "title": "Renamed to response-hours-zero on 2026-07-28; kept so stale anchors fail loudly",
            "effect": "corrupts",
            "type": "entry",
            "status": "resolved",
            "core": false
          }
        ],
        "practices": [
          {
            "id": "median-response-worked-only",
            "title": "Response time is the median over tickets that had a work order, excluding the migration date",
            "question": "How fast does the county respond to a complaint?",
            "authority": "project",
            "rule": [
              "Restrict to tickets with a work_order_id and a closed_date.",
              "Drop every ticket whose closed_date is the 2021-03-15 migration date.",
              "Report the median by year, with n."
            ],
            "naive": "The mean of response_hours over every closed ticket, which folds in the intake zeros and the migration backfill.",
            "because": "Both defects push the average down, and they push it down hardest in exactly the years a reader wants to compare against.",
            "residual": "Dropping the migration date also drops roughly 400 tickets genuinely closed that day. The error runs toward reporting the county as slower than it was, which is the safer direction.",
            "contested": true,
            "addresses": [
              "migration-close-dates",
              "response-hours-zero"
            ]
          }
        ],
        "latest_change": "2026-07-28",
        "page": "ridgeway-311.md",
        "page_url": "https://ridgewaytimes.example.org/ergo/ridgeway-311.md"
      }
    ],
    "base_url": "https://ridgewaytimes.example.org/ergo/"
  },
  "export": {
    "ergo": "0.5",
    "pages": [
      {
        "path": "docs/data/ridgeway-311.md",
        "dataset": {
          "ergo": "0.5",
          "slug": "ridgeway-311",
          "title": "Ridgeway County 311 service requests",
          "publisher": "Ridgeway County Office of Constituent Services",
          "subject": "https://data.ridgeway.example.gov/311",
          "contribute": "https://github.com/ridgeway-times/data/issues",
          "source_urls": [
            "https://data.ridgeway.example.gov/311/requests.csv"
          ],
          "pitfall": "Every ticket still open when the county switched ticket systems was closed on the migration date, so response times computed across March 2021 are worthless unless those rows are excluded.",
          "status": "live",
          "version": "export of 2026-06-30",
          "confidence": "B",
          "updated": "2026-07-28",
          "unknowns": [
            "The pre-2018 archive is published as PDF summaries only; we have not read it.",
            "We do not know whether the vendor rewrites categories on old rows when the category list changes."
          ],
          "coverage": {
            "years": "2018 -> 2026 (partial year)",
            "grain": "one row per service request",
            "entities": "unincorporated county only; the four boroughs run their own systems"
          },
          "missingness": {
            "zero_is_missing": true,
            "source_tokens": [
              "",
              "N/A",
              "UNKNOWN"
            ]
          },
          "access": {
            "keys": [
              "request_id"
            ],
            "raw": "data/raw/ridgeway-311/",
            "builders": [
              "tools/load_311.py"
            ],
            "feeds": [
              "requests",
              "response_times"
            ]
          },
          "acquisition": {
            "access": "public",
            "terms": "County open-data terms; attribution requested, redistribution unrestricted.",
            "credentials": "none",
            "format": "One CSV per calendar year, plus a rolling current-year file.",
            "method": "Direct file URLs from the county's open-data index.",
            "cadence": "annual, with the current year refreshed nightly",
            "lag": "Closed requests appear the following business day.",
            "verification": "Compare the new year file's row count against the county's published annual total.",
            "size": "About 40 MB per year."
          }
        },
        "issues": [
          {
            "id": "migration-close-dates",
            "title": "Every ticket open on 2021-03-15 carries that date as its closed_date",
            "effect": "corrupts",
            "type": "revision",
            "status": "open",
            "discovered": "2026-07",
            "detection": "closed_date = 2021-03-15 on 14,902 rows; the next busiest close date in the whole file is 231 rows",
            "misuse": "Reading 2020 and early 2021 response times as if they were measured. They were assigned by a data migration.",
            "scope": {
              "years": [
                "2018",
                "2019",
                "2020",
                "2021"
              ],
              "columns": [
                "closed_date",
                "response_hours"
              ]
            },
            "_line": 69
          },
          {
            "id": "ward-renumbering",
            "title": "The 2022 redistricting reassigned ward numbers; ward 3 before and after are different places",
            "effect": "misleads",
            "type": "geography",
            "status": "open",
            "discovered": "2026-07",
            "detection": "ward 9 first appears in the 2022 file; ward 6's request volume falls 71% between 2021 and 2022 with no change in population",
            "misuse": "Charting requests per ward as one series from 2018 to 2026. The lines cross where the boundaries moved, not where the potholes are.",
            "instead": "Break the series at 2022, or aggregate to the county before comparing across it.",
            "scope": {
              "years": "all",
              "columns": [
                "ward"
              ]
            },
            "_line": 93
          },
          {
            "id": "response-hours-zero",
            "title": "response_hours is 0 when intake closed the ticket without opening a work order",
            "effect": "corrupts",
            "type": "entry",
            "status": "mitigated",
            "core": true,
            "discovered": "2026-07",
            "handled_by": [
              "tools/load_311.py#response_hours"
            ],
            "detection": "response_hours = 0 with an empty work_order_id — 8.1% of closed tickets",
            "misuse": "Averaging response_hours over closed tickets. The zeros are 'never dispatched', not 'answered instantly', and they pull the mean down by about a third.",
            "scope": {
              "all": true,
              "columns": [
                "response_hours"
              ]
            },
            "_line": 116
          },
          {
            "id": "response-zero-unrecorded",
            "title": "Renamed to response-hours-zero on 2026-07-28; kept so stale anchors fail loudly",
            "effect": "corrupts",
            "type": "entry",
            "status": "resolved",
            "superseded_by": "response-hours-zero",
            "scope": {
              "all": true
            },
            "_line": 141
          }
        ],
        "practices": [
          {
            "id": "median-response-worked-only",
            "title": "Response time is the median over tickets that had a work order, excluding the migration date",
            "question": "How fast does the county respond to a complaint?",
            "authority": "project",
            "rule": [
              "Restrict to tickets with a work_order_id and a closed_date.",
              "Drop every ticket whose closed_date is the 2021-03-15 migration date.",
              "Report the median by year, with n."
            ],
            "naive": "The mean of response_hours over every closed ticket, which folds in the intake zeros and the migration backfill.",
            "because": "Both defects push the average down, and they push it down hardest in exactly the years a reader wants to compare against.",
            "residual": "Dropping the migration date also drops roughly 400 tickets genuinely closed that day. The error runs toward reporting the county as slower than it was, which is the safer direction.",
            "contested": true,
            "addresses": [
              "migration-close-dates",
              "response-hours-zero"
            ],
            "implemented_by": [
              "tools/load_311.py#median_response"
            ],
            "_line": 161
          }
        ],
        "references": [
          {
            "kind": "documentation",
            "url": "https://ridgeway.example.gov/311/data-dictionary",
            "observed": "2026-07-28",
            "covers": "The county's field-by-field dictionary for the 311 export, including the closure-code list.",
            "maintenance": "dated",
            "caveat": "Last revised before the 2023 code change; three closure codes in the current export are absent from it.",
            "_line": 187
          }
        ],
        "quotes": [
          {
            "text": "Across all service requests closed in 2024, the median time to close was 42 hours.",
            "source": "https://ridgeway.example.gov/311/annual-report-2024",
            "retrieved": "2026-07-28",
            "supports": [
              "median-response-worked-only"
            ],
            "note": "Their 42 hours counts the four boroughs; ours does not, and that is the whole of the gap below.",
            "_line": 203
          }
        ],
        "validations": [
          {
            "date": "2026-07-28",
            "method": "reconciled our 2024 median against the county's published annual service report",
            "result": "ours 41.5 h vs the county's 42 h for 2024; the gap is the four boroughs, which the county includes and we exclude",
            "evidence": "docs/data/ridgeway-311-reconciliation.md",
            "_line": 212
          }
        ],
        "changes": [
          {
            "date": "2026-07-28",
            "note": "First pass over the 311 export: migration close dates, ward renumbering, and the intake zeros registered; response-time practice recorded.",
            "issues": [
              "migration-close-dates",
              "ward-renumbering",
              "response-hours-zero"
            ],
            "_line": 230
          }
        ]
      }
    ]
  }
};
