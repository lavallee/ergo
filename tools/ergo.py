#!/usr/bin/env python3
# ergo.py — validator, digest, and exporter for ergo data pages.
# Format: https://github.com/lavallee/ergo (SPEC.md) · ergo format 0.5 · tool 0.5.0
# Stdlib only, Python >= 3.11 (tomllib). Vendor this file freely; it has no deps.
"""
Usage:
  python3 ergo.py check   [PATHS...] [--repo ROOT] [--strict] [--require-manifest]
  python3 ergo.py digest  [PATHS...] [--long] [--write FILE]
  python3 ergo.py export  [PATHS...] [--out FILE]
  python3 ergo.py publish [PATHS...] --dir OUT [--base-url URL]
  python3 ergo.py directory [PATHS...] [--bundle URL] [--name NAME] [--entries-only]
  python3 ergo.py scan    [PATHS...] [--json] [--out FILE]
  python3 ergo.py new     SLUG [--dir DIR]

PATHS are data-page markdown files or directories containing them
(default: current directory). INDEX.md files are skipped automatically.
"""

import argparse
import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path

FORMAT_VERSIONS = {"0.1", "0.2", "0.3", "0.4", "0.5"}
BLOCK_TYPES = {"dataset", "issue", "practice", "reference", "quote", "validation",
               "change"}
EFFECTS = ["breaks", "corrupts", "misleads", "context"]
ISSUE_STATUSES = {"open", "mitigated", "resolved", "monitor"}
DATASET_STATUSES = {"live", "acquiring", "dormant", "archived"}
AUTHORITIES = {"publisher", "project", "community"}
# An issue is a defect in the data (SPEC §2). `handling` is the escape hatch
# for a fact about this project's own handling that is not worth a page of
# its own — deliberately narrow, and reported by `publish`.
ISSUE_ABOUT = {"data", "handling"}
TYPES = {
    "definitional", "universe", "coverage", "suppression", "geography",
    "revision", "coding", "format", "entry", "linkage", "uncertainty",
    "availability", "measurement", "identity", "policy", "acquisition",
}
SCOPE_KEYS = {"years", "tables", "columns", "rows", "entities", "all"}
MISSINGNESS_KEYS = {"zero_is_missing", "source_tokens"}
ACQUISITION_KEYS = {"access", "terms", "credentials", "format", "method", "via",
                    "cadence", "lag", "verification", "size"}
# Closed: this is the field a tool branches on when deciding whether a lesson
# about this dataset could be shared at all.
ACCESS_LEVELS = {"public", "conditional", "restricted"}
# source_url(s) handled separately: either form satisfies the requirement.
DATASET_REQUIRED = ("ergo", "slug", "title", "publisher", "pitfall", "status")
ISSUE_REQUIRED = ("id", "title", "effect", "type", "status")
PRACTICE_REQUIRED = ("id", "title", "question", "authority", "rule", "because")
QUOTE_REQUIRED = ("text", "source", "retrieved")
REFERENCE_REQUIRED = ("kind", "url", "observed")
# Recommended, not closed: one real corpus of 94 sources used 13 distinct
# words for this, so closing it now would close it wrong (cf. issue `type`).
REFERENCE_KINDS = {
    "implementation", "documentation", "article", "schema", "discussion",
    "dataset", "notebook",
}
# Closed: a consumer's behaviour branches on it — whether to use the thing.
MAINTENANCE = {"active", "dated", "archived", "unknown"}
VALIDATION_REQUIRED = ("date", "method", "result")
CHANGE_REQUIRED = ("date", "note")

KEBAB = re.compile(r"^[a-z0-9][a-z0-9-]*$")
ANCHOR = re.compile(r"ergo:\s*([a-z0-9][a-z0-9-]*)/([a-z0-9][a-z0-9-]*)")
FENCE = re.compile(r"^(`{3,})(.*)$")
HEADING = re.compile(r"^#{1,6}\s")

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "renders"}
BINARY_HINT = re.compile(rb"\x00")


# ---------- parsing ----------

class Block:
    def __init__(self, kind, data, line):
        self.kind, self.data, self.line = kind, data, line


class Page:
    def __init__(self, path):
        self.path = Path(path)
        self.blocks = []
        self.errors = []      # (line, message)
        self.warnings = []    # (line, message)

    @property
    def dataset(self):
        for b in self.blocks:
            if b.kind == "dataset":
                return b.data.get("dataset", {})
        return None

    def issues(self):
        return [b for b in self.blocks if b.kind == "issue"]

    def practices(self):
        return [b for b in self.blocks if b.kind == "practice"]

    def references(self):
        return [b for b in self.blocks if b.kind == "reference"]

    def quotes(self):
        return [b for b in self.blocks if b.kind == "quote"]

    def validations(self):
        return [b for b in self.blocks if b.kind == "validation"]

    def changes(self):
        return [b for b in self.blocks if b.kind == "change"]

    def updated(self):
        """The manifest updated field, as an ISO string ('' if absent)."""
        d = self.dataset or {}
        return str(d.get("updated") or "")


def parse_page(path):
    page = Page(path)
    text = Path(path).read_text(encoding="utf-8")
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        m = FENCE.match(lines[i])
        if not m:
            i += 1
            continue
        ticks, info = m.group(1), m.group(2).strip()
        start = i
        i += 1
        body = []
        while i < len(lines):
            close = FENCE.match(lines[i])
            if close and len(close.group(1)) >= len(ticks) and not close.group(2).strip():
                break
            body.append(lines[i])
            i += 1
        i += 1  # past the closing fence (or EOF)
        words = info.split()
        is_marked = len(words) >= 2 and words[0] == "toml" and words[1] == "ergo"
        is_plain_toml = words == ["toml"]
        if not (is_marked or is_plain_toml):
            continue
        try:
            data = tomllib.loads("\n".join(body))
        except tomllib.TOMLDecodeError as e:
            if is_marked:
                page.errors.append((start + 1, f"unparseable ergo block: {e}"))
            continue
        tops = set(data.keys())
        if is_marked:
            if len(tops) != 1 or not tops <= BLOCK_TYPES:
                page.errors.append((start + 1,
                    f"ergo block must contain exactly one of {sorted(BLOCK_TYPES)}, got: {sorted(tops) or 'nothing'}"))
                continue
        elif not (len(tops) == 1 and tops <= BLOCK_TYPES):
            continue  # plain toml block that isn't an ergo table — not ours
        kind = tops.pop()
        if is_plain_toml:
            page.warnings.append((start + 1, f"[{kind}] block fenced as plain `toml` — mark it `toml ergo`"))
        page.blocks.append(Block(kind, data, start + 1))
    return page, lines


# ---------- validation ----------

def check_page(page, lines):
    err, warn = page.errors, page.warnings
    if not page.blocks:
        err.append((1, "no ergo blocks found — not a data page (or all blocks unparseable)"))
        return
    datasets = [b for b in page.blocks if b.kind == "dataset"]
    if not datasets:
        err.append((1, "missing [dataset] manifest block"))
    else:
        if page.blocks[0].kind != "dataset":
            err.append((page.blocks[0].line, "first ergo block must be the [dataset] manifest"))
        if len(datasets) > 1:
            err.append((datasets[1].line, "more than one [dataset] block"))
        d = datasets[0].data["dataset"]
        dl = datasets[0].line
        for f in DATASET_REQUIRED:
            if not d.get(f):
                if f == "pitfall" and d.get("bite"):
                    err.append((dl, "`bite` was renamed to `pitfall` in ergo 0.4 — rename the field "
                                    "(same meaning, same one-sentence rule)"))
                else:
                    err.append((dl, f"[dataset] missing required field: {f}"))
        if d.get("ergo") and str(d["ergo"]) not in FORMAT_VERSIONS:
            warn.append((dl, f"unknown format version ergo = {d['ergo']!r} (this tool knows {sorted(FORMAT_VERSIONS)})"))
        if d.get("slug") and not KEBAB.match(str(d["slug"])):
            err.append((dl, f"slug must be kebab-case: {d['slug']!r}"))
        if d.get("status") and d["status"] not in DATASET_STATUSES:
            err.append((dl, f"[dataset] status must be one of {sorted(DATASET_STATUSES)}, got {d['status']!r}"))
        if d.get("pitfall") and len(str(d["pitfall"])) > 300:
            warn.append((dl, "pitfall is over 300 characters — it should be one sentence"))
        # source_url (string, 0.1) or source_urls (list, 0.2) — either satisfies it
        urls = d.get("source_urls")
        if urls is not None and not isinstance(urls, list):
            err.append((dl, f"source_urls must be a list, got {type(urls).__name__} — use source_url for a single string"))
            urls = None
        produced = d.get("produced_from")
        if produced is not None and not (isinstance(produced, list)
                                         and all(isinstance(x, str) and x.strip() for x in produced)):
            err.append((dl, "produced_from must be a list of page slugs or upstream URLs"))
            produced = None
        if not [u for u in (urls or []) if str(u).strip()] and not str(d.get("source_url") or "").strip():
            if not produced:
                err.append((dl, "[dataset] missing required field: source_urls "
                                "(a dataset this project produces rather than fetches "
                                "declares `produced_from` instead)"))
        for f in ("version", "implementation", "subject"):
            if f in d and not isinstance(d[f], str):
                err.append((dl, f"{f} must be a string, got {d[f]!r}"))
        if isinstance(d.get("subject"), str) and d["subject"].strip():
            if not re.match(r"^https?://\S+$", d["subject"].strip()):
                err.append((dl, f"subject must be a single http(s) URL, got {d['subject']!r}"))
        elif "subject" not in d and not d.get("produced_from"):
            warn.append((dl, "no subject — directories cluster pages by subject URL, so a page without one cannot be found alongside others documenting the same dataset (§10)"))
        derived = d.get("derived_from")
        if derived is not None:
            if not (isinstance(derived, list) and all(isinstance(x, dict) for x in derived)):
                err.append((dl, "derived_from must be an array of tables ([[dataset.derived_from]])"))
            else:
                for i, src in enumerate(derived):
                    for f in ("url", "retrieved"):
                        if not str(src.get(f) or "").strip():
                            err.append((dl, f"derived_from[{i}] missing required field: {f}"))
                    for k in set(src) - {"url", "retrieved", "note"}:
                        warn.append((dl, f"derived_from[{i}] key {k!r} is outside the recommended set ['note', 'retrieved', 'url']"))
        unknowns = d.get("unknowns")
        if unknowns is not None and not (isinstance(unknowns, list)
                                         and all(isinstance(u, str) for u in unknowns)):
            err.append((dl, "unknowns must be a list of strings"))
        acq = d.get("acquisition")
        if acq is not None:
            if not isinstance(acq, dict):
                err.append((dl, "[dataset.acquisition] must be a table"))
            else:
                for k in set(acq) - ACQUISITION_KEYS:
                    warn.append((dl, f"acquisition key {k!r} is outside the recommended set {sorted(ACQUISITION_KEYS)}"))
                level = acq.get("access")
                if not level:
                    err.append((dl, "[dataset.acquisition] needs `access` — one of "
                                    f"{sorted(ACCESS_LEVELS)}. Prose terms cannot be read by a tool "
                                    "deciding whether anything about this dataset may be shared"))
                elif level not in ACCESS_LEVELS:
                    err.append((dl, f"acquisition.access must be one of {sorted(ACCESS_LEVELS)}, got {level!r}"))
                for k in ACQUISITION_KEYS - {"access"}:
                    if k in acq and not isinstance(acq[k], str):
                        err.append((dl, f"acquisition.{k} must be a string, got {acq[k]!r}"))

        miss = d.get("missingness")
        if miss is not None:
            if not isinstance(miss, dict):
                err.append((dl, "[dataset.missingness] must be a table"))
            else:
                for k in set(miss) - MISSINGNESS_KEYS:
                    warn.append((dl, f"missingness key {k!r} is outside the recommended set {sorted(MISSINGNESS_KEYS)}"))
                if "zero_is_missing" in miss and not isinstance(miss["zero_is_missing"], bool):
                    err.append((dl, f"missingness.zero_is_missing must be a boolean, got {miss['zero_is_missing']!r}"))
                toks = miss.get("source_tokens")
                if toks is not None and not (isinstance(toks, list)
                                             and all(isinstance(t, str) for t in toks)):
                    err.append((dl, "missingness.source_tokens must be a list of strings"))

    seen_ids = {}
    prev_issue_line = None
    for b in page.issues():
        iss, il = b.data["issue"], b.line
        for f in ISSUE_REQUIRED:
            if not iss.get(f):
                err.append((il, f"[issue] missing required field: {f}"))
        iid = iss.get("id", "")
        if iid:
            if not KEBAB.match(str(iid)):
                err.append((il, f"issue id must be kebab-case: {iid!r}"))
            if iid in seen_ids:
                err.append((il, f"duplicate issue id {iid!r} (first at line {seen_ids[iid]})"))
            seen_ids[iid] = il
        if iss.get("effect") and iss["effect"] not in EFFECTS:
            err.append((il, f"effect must be one of {EFFECTS}, got {iss['effect']!r}"))
        if iss.get("status") and iss["status"] not in ISSUE_STATUSES:
            err.append((il, f"issue status must be one of {sorted(ISSUE_STATUSES)}, got {iss['status']!r}"))
        if iss.get("type") and iss["type"] not in TYPES:
            warn.append((il, f"type {iss['type']!r} is outside the recommended taxonomy"))
        scope = iss.get("scope", {})
        if not isinstance(scope, dict) or not scope:
            err.append((il, "issue needs a [issue.scope] table with at least one key (or all = true)"))
        else:
            for k in set(scope) - SCOPE_KEYS:
                warn.append((il, f"scope key {k!r} is outside the recommended set {sorted(SCOPE_KEYS)}"))
        if iss.get("status") == "mitigated" and not iss.get("handled_by"):
            err.append((il, f"issue {iid or '?'} is mitigated but has no handled_by"))
        if iss.get("effect") in ("misleads", "context") and not iss.get("misuse"):
            warn.append((il, f"issue {iid or '?'} is {iss.get('effect')} but names no misuse"))
        if iss.get("about") and iss["about"] not in ISSUE_ABOUT:
            err.append((il, f"issue about must be one of {sorted(ISSUE_ABOUT)}, got {iss['about']!r}"))
        if "core" in iss and not isinstance(iss["core"], bool):
            err.append((il, f"core must be a boolean, got {iss['core']!r}"))
        detect = iss.get("detect", {})
        if detect:
            if not isinstance(detect, dict):
                err.append((il, "[issue.detect] must be a table"))
            else:
                for k in set(detect) - {"regex", "query", "semantic"}:
                    warn.append((il, f"detect key {k!r} is outside the recommended set ['query', 'regex', 'semantic']"))
                for pat in detect.get("regex", []) if isinstance(detect.get("regex", []), list) else []:
                    try:
                        re.compile(pat)
                    except re.error as e:
                        err.append((il, f"detect.regex does not compile: {pat!r} ({e})"))
        # placement: expect a heading between consecutive issue blocks
        if prev_issue_line is not None:
            between = lines[prev_issue_line:il - 1]
            if not any(HEADING.match(l) for l in between):
                warn.append((il, "issue block shares a section with the previous issue — give each issue its own heading"))
        prev_issue_line = il

    # practices share the page's id namespace with issues (anchors stay kind-free)
    issue_ids = set(seen_ids)
    for b in page.practices():
        pr, pl = b.data["practice"], b.line
        for f in PRACTICE_REQUIRED:
            if not pr.get(f):
                err.append((pl, f"[practice] missing required field: {f}"))
        pid = pr.get("id", "")
        if pid:
            if not KEBAB.match(str(pid)):
                err.append((pl, f"practice id must be kebab-case: {pid!r}"))
            if pid in seen_ids:
                err.append((pl, f"duplicate id {pid!r} (first at line {seen_ids[pid]}) — issues and practices share one namespace"))
            seen_ids[pid] = pl
        if pr.get("authority") and pr["authority"] not in AUTHORITIES:
            err.append((pl, f"authority must be one of {sorted(AUTHORITIES)}, got {pr['authority']!r}"))
        rule = pr.get("rule")
        if rule is not None and not (isinstance(rule, str)
                                     or (isinstance(rule, list) and all(isinstance(s, str) for s in rule))):
            err.append((pl, "rule must be a string or a list of strings (ordered steps)"))
        if "contested" in pr and not isinstance(pr["contested"], bool):
            err.append((pl, f"contested must be a boolean, got {pr['contested']!r}"))
        if not pr.get("naive"):
            warn.append((pl, f"practice {pid or '?'} names no naive alternative — if nothing plausible is being ruled out, this is documentation, not a practice"))
        if "scope" in pr:
            warn.append((pl, "practices take no scope — they are reached through `question`; put any narrowing in `rule`"))
        for ref in pr.get("addresses", []) if isinstance(pr.get("addresses", []), list) else []:
            if ref not in issue_ids:
                err.append((pl, f"[practice] addresses unknown issue id {ref!r}"))

    issues = page.issues()
    n_handling = sum(1 for b in issues if b.data["issue"].get("about") == "handling")
    if issues and n_handling > max(1, len(issues) // 3):
        warn.append((issues[0].line,
            f"{n_handling} of {len(issues)} issues are about this project's own handling "
            "rather than the data — that is a page about your pipeline, not about the "
            "dataset; give the derived dataset its own page (`produced_from`, §4)"))
    n_core = sum(1 for b in issues if b.data["issue"].get("core") is True)
    if issues and n_core > max(1, len(issues) // 3):
        warn.append((issues[0].line,
            f"{n_core} of {len(issues)} issues are core — a page where a third of the registry is core has no core"))

    # references point at other people's work about this dataset
    for b in page.references():
        r, rl = b.data["reference"], b.line
        for f in REFERENCE_REQUIRED:
            if not r.get(f):
                err.append((rl, f"[reference] missing required field: {f}"))
        rid = r.get("id", "")
        if rid:
            if not KEBAB.match(str(rid)):
                err.append((rl, f"reference id must be kebab-case: {rid!r}"))
            if rid in seen_ids:
                err.append((rl, f"duplicate id {rid!r} (first at line {seen_ids[rid]}) "
                                "— issues, practices and references share one namespace"))
            seen_ids[rid] = rl
        url = str(r.get("url") or "").strip()
        if url and not re.match(r"^https?://\S+$", url):
            err.append((rl, f"reference url must be a single http(s) URL, got {r.get('url')!r}"))
        if r.get("kind") and r["kind"] not in REFERENCE_KINDS:
            warn.append((rl, f"reference kind {r['kind']!r} is outside the recommended set "
                             f"{sorted(REFERENCE_KINDS)}"))
        if r.get("maintenance") and r["maintenance"] not in MAINTENANCE:
            err.append((rl, f"maintenance must be one of {sorted(MAINTENANCE)}, "
                            f"got {r['maintenance']!r}"))
        if r.get("kind") == "implementation" and not str(r.get("commit") or "").strip():
            warn.append((rl, f"reference {rid or url or '?'} points at code with no commit — "
                             "a reference into a moving repository rots; pin the revision"))
        sup = r.get("supports")
        if sup is not None and not (isinstance(sup, list) and all(isinstance(s, str) for s in sup)):
            err.append((rl, "reference supports must be a list of issue or practice ids"))

    # quotes carry the publisher's own words; ids they support must exist here
    for b in page.quotes():
        q, ql = b.data["quote"], b.line
        for f in QUOTE_REQUIRED:
            if not q.get(f):
                err.append((ql, f"[quote] missing required field: {f}"))
        text = q.get("text")
        if text is not None and not isinstance(text, str):
            err.append((ql, "quote text must be a string — the source's words, verbatim"))
        elif isinstance(text, str) and len(text) > 1200:
            warn.append((ql, "quote is over 1200 characters — quote the sentence that carries "
                             "the point, not the page it came from"))
        src = str(q.get("source") or "").strip()
        if src and not re.match(r"^https?://\S+$", src):
            err.append((ql, f"quote source must be a single http(s) URL, got {q.get('source')!r}"))
        sup = q.get("supports")
        if sup is not None and not (isinstance(sup, list) and all(isinstance(s, str) for s in sup)):
            err.append((ql, "quote supports must be a list of issue or practice ids"))
        else:
            for ref in sup or []:
                if ref not in seen_ids:
                    err.append((ql, f"[quote] supports unknown issue or practice id {ref!r}"))

    for b in page.validations():
        v, vl = b.data["validation"], b.line
        for f in VALIDATION_REQUIRED:
            if not v.get(f):
                err.append((vl, f"[validation] missing required field: {f}"))

    latest_change = ""
    for b in page.changes():
        c, cl = b.data["change"], b.line
        for f in CHANGE_REQUIRED:
            if not c.get(f):
                err.append((cl, f"[change] missing required field: {f}"))
        for iid in c.get("issues", []) if isinstance(c.get("issues", []), list) else []:
            if iid not in seen_ids:
                err.append((cl, f"[change] references unknown issue or practice id {iid!r}"))
        latest_change = max(latest_change, str(c.get("date") or ""))
    if latest_change:
        upd = page.updated()
        if not upd:
            warn.append((page.blocks[0].line, "page has [change] records but no [dataset] updated field"))
        elif upd < latest_change:
            err.append((page.blocks[0].line,
                f"[dataset] updated ({upd}) is older than the newest [change] date ({latest_change})"))


# ---------- scanning code for undocumented dataset handling ----------

# Each signal is a shape that working code takes when its author has already
# learned something about a dataset. A hit is a *candidate*, never a finding:
# the code proves a workaround exists, not that the reading behind it is right
# (SPEC §5). The suggested type is a starting guess for whoever writes it up.
SCAN_SIGNALS = [
    ("sentinel-comparison", "suppression",
     re.compile(r"""(?:==|!=|\.eq\(|%in%|\bisin\()\s*[\[(]?\s*['"](?:\*{1,3}|N/?A|n/a|NULL|--?|\?|\.|N|X|Z)['"]"""
                r"""|[=!]=\s*-9{2,}\b|\b-9{3,}\b""")),
    ("null-filling", "suppression",
     re.compile(r"""\.fillna\(|\bfillna\(|\breplace_na\(|\bcoalesce\(|\bna\.omit\(|is\.na\([^)]*\)\s*<-""")),
    ("era-branch", "format",
     re.compile(r"""\b(?:year|yr|school_year|end_year|fy)\b\s*[<>]=?\s*['"]?(?:19|20)\d{2}"""
                r"""|['"]?(?:19|20)\d{2}['"]?\s*[<>]=?\s*\b(?:year|yr|school_year|end_year)\b""")),
    ("column-rename", "coding",
     re.compile(r"""\.rename\(\s*columns|\brename\(|\bcolnames\(|\bnames\([A-Za-z_.]+\)\s*<-"""
                r"""|\b(?:COLUMN_MAP|COL_MAP|RENAMES?|HEADER_MAP)\b""")),
    ("workbook-layout", "format",
     re.compile(r"""\bskiprows\s*=|\bskip\s*=\s*\d|\bsheet_name\s*=|\bsheet\s*=\s*['"\d]"""
                r"""|\bheader\s*=\s*\d|\bread_excel\(|\bread\.xlsx\(|\busecols\s*=""")),
    ("fixed-width", "format",
     re.compile(r"""\bread_fwf\(|\bread\.fwf\(|\bcolspecs\s*=|\bwidths\s*=\s*\[""")),
    ("identifier-padding", "identity",
     re.compile(r"""\.zfill\(|\bstr_pad\(|\bsprintf\(\s*['"]%0\d|\bformat\(\s*\w+\s*,\s*['"]0\d"""
                r"""|\bastype\(\s*str\s*\)|\bas\.character\(""")),
    ("encoding-fallback", "entry",
     re.compile(r"""\bencoding\s*=\s*['"](?:latin-?1|iso-8859|cp1252|windows-1252|mac_roman)""")),
    ("parse-guard", "availability",
     re.compile(r"""\bexcept\s+(?:Exception|ValueError|KeyError|IndexError|TypeError)\b|\bexcept\s*:"""
                r"""|\btryCatch\(|\bsuppressWarnings\(""")),
    ("hardcoded-source-url", "availability",
     re.compile(r"""['"]https?://[^\s'"]{12,}['"]""")),
    ("flagged-comment", "",
     re.compile(r"""(?:^|\s)(?:#|//|--|\*)\s*(?:HACK|XXX|FIXME|WORKAROUND|GOTCHA|WEIRD|UGLY|WTF|BUG)\b""",
                re.I)),
]
SCAN_EXT = {".py", ".r", ".rmd", ".sql", ".js", ".ts", ".jl", ".rb", ".go",
            ".scala", ".java", ".sh", ".pl", ".m", ".do", ".sas"}
SCAN_MAX_BYTES = 2_000_000


def scan_files(paths, anchor_window=3):
    """Find places where code already handles something about a dataset.

    Returns (candidates, stats). A candidate is a dict with file, line, signal,
    suggested type, and the source line. Lines already carrying an `ergo:`
    anchor — or sitting just under one — are skipped: they are documented.
    """
    targets = []
    for raw in paths or ["."]:
        p = Path(raw)
        if p.is_file():
            targets.append(p)
        elif p.is_dir():
            targets.extend(repo_files(p))
    candidates, scanned, anchored = [], 0, 0
    for path in sorted(set(targets)):
        if path.suffix.lower() not in SCAN_EXT:
            continue
        try:
            if path.stat().st_size > SCAN_MAX_BYTES:
                continue
            blob = path.read_bytes()
        except OSError:
            continue
        if BINARY_HINT.search(blob[:4096]):
            continue
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            continue
        lines = text.split("\n")
        scanned += 1
        anchor_lines = {n for n, l in enumerate(lines) if ANCHOR.search(l)}
        for n, line in enumerate(lines):
            if len(line) > 400:
                continue
            near_anchor = any((n - k) in anchor_lines for k in range(0, anchor_window + 1))
            hits = [(name, typ) for name, typ, rx in SCAN_SIGNALS if rx.search(line)]
            if not hits:
                continue
            if near_anchor:
                anchored += len(hits)
                continue
            for name, typ in hits:
                candidates.append({
                    "file": str(path), "line": n + 1, "signal": name,
                    "suggests": typ, "source": line.strip()[:160],
                })
    return candidates, {"files_scanned": scanned, "already_anchored": anchored}


def render_scan(candidates, stats):
    out = []
    by_file = {}
    for c in candidates:
        by_file.setdefault(c["file"], []).append(c)
    for path in sorted(by_file):
        out.append(path)
        for c in by_file[path]:
            suffix = f" → {c['suggests']}" if c["suggests"] else ""
            out.append(f"  {c['line']:>5}  {c['signal']}{suffix}")
            out.append(f"         {c['source']}")
        out.append("")
    signals = len({c["signal"] for c in candidates})
    out.append(f"{len(candidates)} candidate(s) across {len(by_file)} file(s) "
               f"of {stats['files_scanned']} scanned, {signals} signal(s); "
               f"{stats['already_anchored']} hit(s) skipped as already anchored")
    out.append("")
    out.append("Candidates are evidence that someone handled something — not that "
               "the reading behind it was right. Confirm each against real files "
               "before it becomes an [issue]; until then the page's confidence is "
               "'?' and its unknowns say the data has not been examined.")
    return "\n".join(out) + "\n"


def repo_files(root):
    root = Path(root)
    try:
        out = subprocess.run(["git", "-C", str(root), "ls-files"],
                             capture_output=True, text=True, check=True)
        return [root / p for p in out.stdout.splitlines() if p]
    except (subprocess.CalledProcessError, FileNotFoundError):
        files = []
        for p in root.rglob("*"):
            if p.is_file() and not (set(p.parts) & SKIP_DIRS):
                files.append(p)
        return files


def check_repo(pages, root):
    """Cross-checks needing the host repo: handled_by paths/symbols, anchor round trip."""
    root = Path(root)
    known = {}   # (slug, issue_id) -> page
    for page in pages:
        d = page.dataset or {}
        slug = d.get("slug")
        if not slug:
            continue
        for b in page.issues() + page.practices():
            iid = b.data[b.kind].get("id")
            if iid:
                known[(slug, iid)] = (page, b)

    page_paths = {p.path.resolve() for p in pages}
    anchors = {}  # (slug, id) -> [(path, line)]
    for f in repo_files(root):
        if f.resolve() in page_paths or f.name == "INDEX.md":
            continue
        try:
            raw = f.read_bytes()
        except OSError:
            continue
        if not raw or BINARY_HINT.search(raw[:4096]):
            continue
        text = raw.decode("utf-8", errors="replace")
        if "ergo:" not in text:
            continue
        for n, line in enumerate(text.split("\n"), 1):
            for m in ANCHOR.finditer(line):
                anchors.setdefault((m.group(1), m.group(2)), []).append((f, n))

    problems_err, problems_warn = [], []
    known_slugs = {slug for slug, _ in known}
    for key, sites in sorted(anchors.items()):
        if key in known:
            continue
        for f, n in sites:
            if key[0] in known_slugs:
                problems_err.append(f"{f.relative_to(root)}:{n}: anchor 'ergo: {key[0]}/{key[1]}' names an unknown issue")
            else:
                problems_warn.append(
                    f"{f.relative_to(root)}:{n}: anchor 'ergo: {key[0]}/{key[1]}' names a dataset not among the checked pages — run check on the full pages directory to verify it")

    for page in pages:
        d = page.dataset or {}
        slug = d.get("slug", "?")
        for b in page.issues() + page.practices():
            iss, il = b.data[b.kind], b.line
            iid = iss.get("id", "?")
            # issues point at code with handled_by; practices with implemented_by
            handled = iss.get("handled_by" if b.kind == "issue" else "implemented_by") or []
            if isinstance(handled, str):
                handled = [handled]
            anchored_files = {f.resolve() for f, _ in anchors.get((slug, iid), [])}
            for ref in handled:
                path, _, symbol = str(ref).partition("#")
                target = root / path
                if not target.is_file():
                    problems_err.append(f"{page.path}:{il}: handled_by path not found: {path}")
                    continue
                if symbol:
                    body = target.read_text(encoding="utf-8", errors="replace")
                    if not re.search(rf"\b{re.escape(symbol)}\b", body):
                        problems_warn.append(f"{page.path}:{il}: symbol {symbol!r} not found in {path}")
            # a mitigated issue, or any practice naming code, should carry an anchor
            expects_anchor = (iss.get("status") == "mitigated") if b.kind == "issue" else True
            if expects_anchor and handled:
                targets = {(root / str(r).partition('#')[0]).resolve() for r in handled}
                if not (anchored_files & targets):
                    field = "handled_by" if b.kind == "issue" else "implemented_by"
                    label = f"mitigated issue" if b.kind == "issue" else "practice"
                    problems_warn.append(
                        f"{page.path}:{il}: {label} {slug}/{iid} has no 'ergo: {slug}/{iid}' anchor in its {field} files")
    return problems_err, problems_warn


# ---------- outputs ----------

def effect_counts(page):
    counts = {e: 0 for e in EFFECTS}
    for b in page.issues():
        e = b.data["issue"].get("effect")
        if e in counts:
            counts[e] += 1
    return counts


def core_count(page):
    return sum(1 for b in page.issues() if b.data["issue"].get("core") is True)


def digest(pages, long=False):
    out = ["# Data pages", "",
           "<!-- generated by ergo.py digest — do not hand-edit -->", "",
           "| dataset | status | updated | issues | practices | the pitfall |",
           "|---|---|---|---|---|---|"]
    for page in sorted(pages, key=lambda p: (p.dataset or {}).get("slug", "")):
        d = page.dataset or {}
        counts = effect_counts(page)
        total = sum(counts.values())
        parts = " · ".join(f"{v} {k}" for k, v in counts.items() if v)
        n_core = core_count(page)
        if n_core:
            parts += f" · {n_core} core"
        issues = f"{total}" + (f" ({parts})" if parts else "")
        prs = page.practices()
        n_contested = sum(1 for b in prs if b.data["practice"].get("contested") is True)
        practices = f"{len(prs)}" + (f" ({n_contested} contested)" if n_contested else "")
        out.append(f"| [{d.get('title', page.path.stem)}]({page.path.name}) "
                   f"| {d.get('status', '?')} | {page.updated() or '?'} | {issues} | {practices} | {d.get('pitfall', '')} |")
    if long:
        for page in sorted(pages, key=lambda p: (p.dataset or {}).get("slug", "")):
            d = page.dataset or {}
            slug = d.get("slug", "?")
            out += ["", f"## {d.get('title', page.path.stem)} (`{slug}`)", "",
                    "| issue | effect | status | title |", "|---|---|---|---|"]
            for b in page.issues():
                iss = b.data["issue"]
                star = " ★core" if iss.get("core") is True else ""
                out.append(f"| `{slug}/{iss.get('id', '?')}`{star} | {iss.get('effect', '?')} "
                           f"| {iss.get('status', '?')} | {iss.get('title', '')} |")
            if page.practices():
                out += ["", "| practice | authority | question | title |", "|---|---|---|---|"]
                for b in page.practices():
                    pr = b.data["practice"]
                    mark = " ⚑contested" if pr.get("contested") is True else ""
                    out.append(f"| `{slug}/{pr.get('id', '?')}`{mark} | {pr.get('authority', '?')} "
                               f"| {pr.get('question', '')} | {pr.get('title', '')} |")
            for u in d.get("unknowns", []) or []:
                out.append(f"\n> **Not known:** {u}")
    return "\n".join(out) + "\n"


def export(pages):
    doc = {"ergo": "0.5", "pages": []}
    for page in pages:
        entry = {"path": str(page.path), "dataset": page.dataset,
                 "issues": [], "practices": [], "references": [],
                 "quotes": [], "validations": []}
        for b in page.issues():
            rec = dict(b.data["issue"])
            rec["_line"] = b.line
            entry["issues"].append(rec)
        for b in page.practices():
            rec = dict(b.data["practice"])
            rec["_line"] = b.line
            entry["practices"].append(rec)
        for b in page.references():
            rec = dict(b.data["reference"])
            rec["_line"] = b.line
            entry["references"].append(rec)
        for b in page.quotes():
            rec = dict(b.data["quote"])
            rec["_line"] = b.line
            entry["quotes"].append(rec)
        for b in page.validations():
            rec = dict(b.data["validation"])
            rec["_line"] = b.line
            entry["validations"].append(rec)
        entry["changes"] = [dict(b.data["change"], _line=b.line) for b in page.changes()]
        doc["pages"].append(entry)
    return json.dumps(doc, indent=2, default=str, ensure_ascii=False) + "\n"


INTERNAL_BEGIN, INTERNAL_END = "<!-- ergo:internal -->", "<!-- /ergo:internal -->"
# Fields that point into the host repo — stripped from the public projection.
INTERNAL_FIELDS = {"issue": {"handled_by"}, "practice": {"implemented_by"},
                   "validation": {"evidence"},
                   "dataset.access": {"builders", "raw", "feeds"}}
INTERNAL_SMELLS = re.compile(r"\btools/|\bpython3\b|\bdata/raw\b")


def project_public(text, name="page"):
    """The public projection of a page: internal regions and repo-pointing
    fields removed. Returns (text, warnings)."""
    out, warnings = [], []
    depth = 0
    in_block = table = None
    skip_until_balanced = 0
    for n, line in enumerate(text.split("\n"), 1):
        s = line.strip()
        if s == INTERNAL_BEGIN:
            depth += 1
            continue
        if s == INTERNAL_END:
            depth = max(0, depth - 1)
            continue
        if depth:
            continue
        m = FENCE.match(line)
        if m and in_block is None and "toml" in m.group(2):
            in_block, table = True, None
        elif m and in_block:
            in_block, table = None, None
        elif in_block:
            if skip_until_balanced > 0:
                skip_until_balanced += line.count("[") + line.count("{")
                skip_until_balanced -= line.count("]") + line.count("}")
                continue
            t = re.match(r"\[([a-z.]+)\]", s)
            if t:
                table = t.group(1)
            key = re.match(r"([A-Za-z_]+)\s*=", s)
            if key and table and key.group(1) in INTERNAL_FIELDS.get(table, ()):
                opens = line.count("[") + line.count("{")
                closes = line.count("]") + line.count("}")
                if opens > closes:
                    skip_until_balanced = opens - closes
                continue
        out.append(line)
    projected = re.sub(r"\n{3,}", "\n\n", "\n".join(out))
    for n, line in enumerate(projected.split("\n"), 1):
        if INTERNAL_SMELLS.search(line):
            warnings.append(f"{name}:{n}: published text still looks internal: {line.strip()[:90]}")
    return projected, warnings


def check_internal_markers(text):
    """Return an error string if internal markers are unbalanced, else None."""
    depth = 0
    for n, line in enumerate(text.split("\n"), 1):
        s = line.strip()
        if s == INTERNAL_BEGIN:
            depth += 1
        elif s == INTERNAL_END:
            depth -= 1
            if depth < 0:
                return f"line {n}: {INTERNAL_END} without a matching {INTERNAL_BEGIN}"
    if depth:
        return f"unclosed {INTERNAL_BEGIN}"
    return None


def publish(pages, out_dir, base_url=None):
    """Write the servable bundle: index.json + the public projection of each
    page as <slug>.md."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    base = (base_url.rstrip("/") + "/") if base_url else None
    datasets = []
    all_warnings = []
    for page in sorted(pages, key=lambda p: (p.dataset or {}).get("slug", "")):
        d = page.dataset or {}
        slug = d.get("slug") or page.path.stem
        for b in page.issues():
            if b.data["issue"].get("about") == "handling":
                all_warnings.append(
                    f"{page.path}:{b.line}: issue {b.data['issue'].get('id', '?')!r} is about "
                    "your own handling, not the data, and is being published — move it to the "
                    "derived dataset's page, or wrap its section in ergo:internal markers")
        dest = out / f"{slug}.md"
        src = page.path.read_text(encoding="utf-8")
        marker_err = check_internal_markers(src)
        if marker_err:
            sys.exit(f"{page.path}: {marker_err}")
        projected, warns = project_public(src, name=str(dest))
        all_warnings += warns
        dest.write_text(projected, encoding="utf-8")
        counts = effect_counts(page)
        changes = [b.data["change"] for b in page.changes()]
        latest = max((str(c.get("date") or "") for c in changes), default="")
        rec = {
            "slug": slug,
            "title": d.get("title", ""),
            "publisher": d.get("publisher", ""),
            "status": d.get("status", ""),
            "confidence": d.get("confidence", ""),
            "updated": page.updated(),
            "subject": d.get("subject", ""),
            "derived_from": d.get("derived_from", []),
            "version": d.get("version", ""),
            "implementation": d.get("implementation", ""),
            "pitfall": d.get("pitfall", ""),
            "coverage": d.get("coverage", {}),
            "missingness": d.get("missingness", {}),
            "unknowns": d.get("unknowns", []),
            "source_urls": (d.get("source_urls")
                            or ([d["source_url"]] if d.get("source_url") else [])),
            "counts": {"issues": sum(counts.values()), "core": core_count(page),
                       "practices": len(page.practices()),
                       "effects": {k: v for k, v in counts.items() if v}},
            "issues": [{
                "id": b.data["issue"].get("id", ""),
                "title": b.data["issue"].get("title", ""),
                "effect": b.data["issue"].get("effect", ""),
                "type": b.data["issue"].get("type", ""),
                "status": b.data["issue"].get("status", ""),
                "core": b.data["issue"].get("core", False) is True,
            } for b in page.issues()],
            # practices are more public than issues, not less: rule/naive/because
            # are exactly what a reader needs. Only implemented_by points inward.
            "practices": [{k: v for k, v in b.data["practice"].items()
                           if k != "implemented_by"} for b in page.practices()],
            "latest_change": latest,
            "page": f"{slug}.md",
        }
        if base:
            rec["page_url"] = base + f"{slug}.md"
        datasets.append(rec)
    index = {"ergo": "0.5", "datasets": datasets}
    if base:
        index["base_url"] = base
    (out / "index.json").write_text(
        json.dumps(index, indent=2, default=str, ensure_ascii=False) + "\n", encoding="utf-8")
    return len(datasets), all_warnings


def normalize_subject(url):
    """Canonical form of a subject URL, for directory clustering (§10).

    Fold the scheme to https, lowercase the host, drop a leading 'www.', a
    trailing slash, and a trailing index/default page of any common extension,
    drop the fragment.
    The query string is KEPT — for some publishers it carries the dataset
    identity, and dropping it would fuse distinct sources.
    """
    s = str(url or "").strip()
    if not s:
        return ""
    m = re.match(r"^(https?)://([^/?#]+)([^?#]*)(\?[^#]*)?", s, re.I)
    if not m:
        return s.rstrip("/")
    # scheme folds to https: nobody means a different dataset by http vs https
    scheme, host, path, query = "https", m.group(2).lower(), m.group(3) or "", m.group(4) or ""
    host = host[4:] if host.startswith("www.") else host
    path = re.sub(r"/(index|default)\.(html?|shtml|php|aspx?|jsp)$", "/", path, flags=re.I)
    path = path.rstrip("/")
    return f"{scheme}://{host}{path}{query}"


def directory_entries(pages, bundle_url=None):
    """Directory entries (§10) for these pages — what a publisher contributes."""
    base = (bundle_url.rstrip("/") + "/") if bundle_url else ""
    out = []
    for page in sorted(pages, key=lambda p: (p.dataset or {}).get("slug", "")):
        d = page.dataset or {}
        if d.get("produced_from") and not d.get("subject"):
            continue   # a dataset this project makes; nobody else publishes it to cluster with
        subject = d.get("subject", "")
        entry = {
            "subject": subject,
            "subject_normalized": normalize_subject(subject),
            "bundle": base,
            "slug": d.get("slug", ""),
            "title": d.get("title", ""),
            "publisher": d.get("publisher", ""),
            "updated": page.updated(),
        }
        cov = d.get("coverage") or {}
        recognizes = {}
        hosts = []
        for u in (d.get("source_urls") or ([d["source_url"]] if d.get("source_url") else [])):
            m = re.match(r"^https?://([^/?#]+)", str(u), re.I)
            if m:
                h = m.group(1).lower()
                hosts.append(h[4:] if h.startswith("www.") else h)
        if hosts:
            recognizes["domains"] = sorted(set(hosts))
        keys = (d.get("access") or {}).get("keys")
        if keys:
            recognizes["columns"] = list(keys)
        if recognizes:
            entry["recognizes"] = recognizes
        if cov.get("years"):
            entry["years"] = cov["years"]
        out.append(entry)
    return out


TEMPLATE = '''# {title}

One-paragraph lede: what this dataset is and why the project uses it.

```toml ergo
[dataset]
ergo = "0.5"
slug = "{slug}"
title = "{title}"
publisher = ""
subject = ""            # the URL of the dataset this documents — how directories cluster pages (§10)
source_urls = [""]
pitfall = ""
status = "acquiring"
version = ""
confidence = "?"
updated = ""
unknowns = ["What have you not looked at? Say so — silence reads as a clean bill of health."]

[dataset.coverage]
years = ""
grain = ""

[dataset.missingness]
zero_is_missing = false
source_tokens = []

[dataset.access]
keys = []
builders = []
```

## What it is

## Access

## Structure

## Joins

## Issues

### <symptom-first title of the first issue>

```toml ergo
[issue]
id = ""
title = ""
effect = "corrupts"
type = "format"
status = "open"

[issue.scope]
all = true
```

The story: how it was found, examples, quantities.

## Practices

### <the rule, stated as its conclusion>

```toml ergo
[practice]
id = ""
title = ""
question = "<the task a reader is doing when they need this>"
authority = "project"           # publisher | project | community
rule = ""
naive = "<the plausible wrong move this replaces — if there is none, delete this block>"
because = ""
```

Why this call and not another; what it costs.

## Validation

```toml ergo
[validation]
date = ""
method = ""
result = ""
```

## Provenance

## Changelog

```toml ergo
[change]
date = ""
note = "Page created."
```
'''


# ---------- CLI ----------

def collect_pages(paths, require_manifest=False):
    files = []
    for p in map(Path, paths or ["."]):
        if p.is_dir():
            files += sorted(f for f in p.glob("*.md") if f.name != "INDEX.md")
        else:
            files.append(p)
    parsed = []
    for f in files:
        page, lines = parse_page(f)
        if page.blocks or require_manifest or not f.is_file():
            parsed.append((page, lines))
    return parsed


def main(argv=None):
    ap = argparse.ArgumentParser(prog="ergo.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_check = sub.add_parser("check")
    p_check.add_argument("paths", nargs="*")
    p_check.add_argument("--repo", metavar="ROOT")
    p_check.add_argument("--strict", action="store_true")
    p_check.add_argument(
        "--require-manifest",
        action="store_true",
        help="require every Markdown file in a checked directory to be an Ergo page",
    )
    p_dig = sub.add_parser("digest")
    p_dig.add_argument("paths", nargs="*")
    p_dig.add_argument("--long", action="store_true")
    p_dig.add_argument("--write", metavar="FILE")
    p_exp = sub.add_parser("export")
    p_exp.add_argument("paths", nargs="*")
    p_exp.add_argument("--out", metavar="FILE")
    p_pub = sub.add_parser("publish")
    p_pub.add_argument("paths", nargs="*")
    p_pub.add_argument("--dir", required=True, metavar="OUT")
    p_pub.add_argument("--base-url", metavar="URL")
    p_dir = sub.add_parser("directory")
    p_dir.add_argument("paths", nargs="*")
    p_dir.add_argument("--bundle", metavar="URL", help="public URL of your served bundle")
    p_dir.add_argument("--name", default="", metavar="NAME", help="directory name, when emitting a whole file")
    p_dir.add_argument("--entries-only", action="store_true",
                       help="emit just the entries array, to paste into an existing directory")
    p_dir.add_argument("--out", metavar="FILE")
    p_scan = sub.add_parser("scan", help="find code that already handles something about a dataset")
    p_scan.add_argument("paths", nargs="*")
    p_scan.add_argument("--json", action="store_true", dest="as_json")
    p_scan.add_argument("--out", metavar="FILE")
    p_new = sub.add_parser("new")
    p_new.add_argument("slug")
    p_new.add_argument("--dir", default=".")
    args = ap.parse_args(argv)

    if args.cmd == "scan":
        candidates, stats = scan_files(args.paths)
        if args.as_json:
            text = json.dumps({"ergo_scan": "1", "stats": stats,
                               "candidates": candidates},
                              indent=2, ensure_ascii=False) + "\n"
        else:
            text = render_scan(candidates, stats)
        if args.out:
            Path(args.out).write_text(text, encoding="utf-8")
            print(f"wrote {args.out}")
        else:
            sys.stdout.write(text)
        return 0

    if args.cmd == "new":
        if not KEBAB.match(args.slug):
            sys.exit(f"slug must be kebab-case: {args.slug!r}")
        dest = Path(args.dir) / f"{args.slug}.md"
        if dest.exists():
            sys.exit(f"{dest} already exists")
        title = args.slug.replace("-", " ").title()
        dest.write_text(TEMPLATE.format(slug=args.slug, title=title), encoding="utf-8")
        print(f"scaffolded {dest}")
        return 0

    parsed = collect_pages(
        args.paths,
        require_manifest=(args.cmd == "check" and args.require_manifest),
    )
    if not parsed:
        sys.exit("no data pages found")
    pages = [p for p, _ in parsed]

    if args.cmd == "digest":
        text = digest(pages, long=args.long)
        if args.write:
            Path(args.write).write_text(text, encoding="utf-8")
            print(f"wrote {args.write}")
        else:
            sys.stdout.write(text)
        return 0

    if args.cmd == "export":
        text = export(pages)
        if args.out:
            Path(args.out).write_text(text, encoding="utf-8")
            print(f"wrote {args.out}")
        else:
            sys.stdout.write(text)
        return 0

    if args.cmd == "directory":
        entries = directory_entries(pages, bundle_url=args.bundle)
        missing = [e["slug"] for e in entries if not e["subject"]]
        doc = entries if args.entries_only else {
            "ergo_directory": "1", "name": args.name or "", "entries": entries}
        text = json.dumps(doc, indent=2, default=str, ensure_ascii=False) + "\n"
        if args.out:
            Path(args.out).write_text(text, encoding="utf-8")
            print(f"wrote {args.out} ({len(entries)} entr{'y' if len(entries) == 1 else 'ies'})")
        else:
            sys.stdout.write(text)
        if missing:
            print(f"warning: no subject on: {', '.join(missing)} — these cannot be clustered (§10)",
                  file=sys.stderr)
        if not args.bundle:
            print("warning: no --bundle URL given; entries have an empty bundle field",
                  file=sys.stderr)
        return 0

    if args.cmd == "publish":
        n, warns = publish(pages, args.dir, base_url=args.base_url)
        for w in warns:
            print(f"warning: {w}")
        print(f"published {n} page(s) + index.json -> {args.dir}"
              + (f" ({len(warns)} internal-smell warning(s))" if warns else ""))
        return 0

    # check
    n_err = n_warn = 0
    for page, lines in parsed:
        check_page(page, lines)
        marker_err = check_internal_markers("\n".join(lines))
        if marker_err:
            page.errors.append((1, f"internal markers unbalanced: {marker_err}"))
        for line, msg in sorted(page.errors):
            print(f"{page.path}:{line}: error: {msg}")
        for line, msg in sorted(page.warnings):
            print(f"{page.path}:{line}: warning: {msg}")
        n_err += len(page.errors)
        n_warn += len(page.warnings)
    if args.repo:
        errs, warns = check_repo(pages, args.repo)
        for m in errs:
            print(f"error: {m}")
        for m in warns:
            print(f"warning: {m}")
        n_err += len(errs)
        n_warn += len(warns)
    total_issues = sum(len(p.issues()) for p in pages)
    total_practices = sum(len(p.practices()) for p in pages)
    print(f"{len(pages)} page(s), {total_issues} issue(s), {total_practices} practice(s): "
          f"{n_err} error(s), {n_warn} warning(s)")
    return 1 if n_err or (args.strict and n_warn) else 0


if __name__ == "__main__":
    sys.exit(main())
