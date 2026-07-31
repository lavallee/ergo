#!/usr/bin/env python3
"""Test suite for ergo.py. Stdlib only, no framework.

    python3 tests/run.py          # from the repo root

Asserts three things: the shipped positive fixtures are clean, the negative
fixture triggers every error class we claim to catch, and a 0.1-shaped page
still validates under the current tool.
"""
import json
import re
import subprocess
import tempfile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ERGO = ROOT / "tools" / "ergo.py"
failures = []


def run(*args):
    p = subprocess.run([sys.executable, str(ERGO), *map(str, args)],
                       capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def check(name, cond, detail=""):
    if cond:
        print(f"  ok   {name}")
    else:
        print(f"  FAIL {name}{(' — ' + detail) if detail else ''}")
        failures.append(name)


def counts(out):
    m = re.search(r"(\d+) error\(s\), (\d+) warning\(s\)", out)
    return (int(m.group(1)), int(m.group(2))) if m else (-1, -1)


print("positive fixtures are clean")
code, out = run("check", ROOT / "examples", ROOT / "templates", "--strict")
check("examples + templates: 0 errors, 0 warnings", counts(out) == (0, 0), out.strip())
check("exit 0 under --strict", code == 0)
check("practices are parsed", "practice(s)" in out and " 0 practice(s)" not in out, out.strip())

print("negative fixture triggers every class")
code, out = run("check", ROOT / "tests" / "negative.md")
n_err, n_warn = counts(out)
check("exit 1", code == 1)
check("error count == 32", n_err == 32, f"got {n_err}")
check("warning count == 13", n_warn == 13, f"got {n_warn}")
# Each string below is a check we must never silently lose in a refactor.
for probe in [
    "missing required field: source_urls",
    "status must be one of",
    "slug must be kebab-case",
    "version must be a string",
    "unknowns must be a list of strings",
    "missingness.zero_is_missing must be a boolean",
    "missingness.source_tokens must be a list of strings",
    "effect must be one of",
    "is mitigated but has no handled_by",
    "detect.regex does not compile",
    "[practice] missing required field: question",
    "authority must be one of",
    "rule must be a string or a list of strings",
    "contested must be a boolean",
    "addresses unknown issue id",
    "issues and practices share one namespace",
    "references unknown issue or practice id",
    "[quote] missing required field: source",
    "[quote] missing required field: retrieved",
    "[quote] supports unknown issue or practice id",
    "quote source must be a single http(s) URL",
    "[reference] missing required field: observed",
    "reference url must be a single http(s) URL",
    "maintenance must be one of",
    "reference supports must be a list of issue or practice ids",
    "issues, practices and references share one namespace",
    "[dataset.acquisition] needs `access`",
    "acquisition.credentials must be a string",
    "issue about must be one of",
    "contribute must be a single http(s) URL",
    # warnings
    "outside the recommended taxonomy",
    "names no naive alternative",
    "practices take no scope",
    "but names no misuse",
    "no subject — directories cluster pages by subject URL",
    "quote is over 1200 characters",
    "is outside the recommended set",
    "points at code with no commit",
    "acquisition key 'whatever' is outside the recommended set",
]:
    check(f"catches: {probe}", probe in out)

print("0.1 pages still validate (backward compatibility)")
legacy = ROOT / "tests" / "legacy-0.1.md"
src = (ROOT / "examples" / "spr.md").read_text(encoding="utf-8")
src, n = re.subn(r'^ergo = "0\.\d+"$', 'ergo = "0.1"', src, count=1, flags=re.M)
assert n == 1, "compat fixture: could not downgrade the ergo version"
src = src.replace(
    'source_urls = ["https://www.nj.gov/education/spr/"]',
    'source_url = "https://www.nj.gov/education/spr/"')
src = re.sub(r'^subject = .*\n', '', src, count=1, flags=re.M)
src = re.sub(r'version = .*\n', '', src, count=1)
src = re.sub(r'unknowns = \[.*?\n\]\n', '', src, flags=re.S)
src = re.sub(r'\[dataset\.missingness\]\n.*?\n\n', '', src, flags=re.S)
legacy.write_text(src, encoding="utf-8")
try:
    code, out = run("check", legacy, "--strict")
    check("0.1 manifest shape parses with no errors", counts(out)[0] == 0, out.strip())
    check("0.1 page warns only about the missing subject", counts(out)[1] == 1, out.strip())
finally:
    legacy.unlink(missing_ok=True)

print("digest and export run")
for cmd in ("digest", "export"):
    code, out = run(cmd, ROOT / "examples")
    check(f"{cmd} exits 0", code == 0, out.strip()[:200])

print("bite -> pitfall migration (0.4)")
legacy = ROOT / "tests" / "legacy-bite.md"
legacy.write_text(
    '# T\n\n```toml ergo\n[dataset]\nergo = "0.3"\nslug = "t"\ntitle = "T"\n'
    'publisher = "P"\nsubject = "https://x.org/d"\nsource_urls = ["https://x.org/d"]\n'
    'bite = "old field name"\nstatus = "live"\n```\n', encoding="utf-8")
try:
    code, out = run("check", legacy)
    check("a page still using `bite` fails", code == 1)
    check("and is told exactly what to rename",
          "`bite` was renamed to `pitfall`" in out, out.strip())
finally:
    legacy.unlink(missing_ok=True)

print("a produced dataset needs no source_urls and no subject (§4)")
produced = ROOT / "tests" / "produced.md"
produced.write_text(
    '# P\n\n```toml ergo\n[dataset]\nergo = "0.4"\nslug = "p"\ntitle = "P"\n'
    'publisher = "This project"\nproduced_from = ["spr"]\n'
    'pitfall = "Period labels are ours, not any publisher\'s."\nstatus = "live"\n```\n',
    encoding="utf-8")
try:
    code, out = run("check", produced, "--strict")
    check("produced page validates with no source_urls", counts(out) == (0, 0), out.strip())
    code, out = run("directory", produced, "--bundle", "https://x.org/ergo/")
    check("and is left out of directory entries", '"slug": "p"' not in out, out.strip()[:200])
    bad = ROOT / "tests" / "no-source.md"
    bad.write_text(
        '# B\n\n```toml ergo\n[dataset]\nergo = "0.4"\nslug = "b"\ntitle = "B"\n'
        'publisher = "P"\npitfall = "x"\nstatus = "live"\n```\n', encoding="utf-8")
    try:
        code, out = run("check", bad)
        check("a page with neither still errors", "missing required field: source_urls" in out, out.strip())
    finally:
        bad.unlink(missing_ok=True)
finally:
    produced.unlink(missing_ok=True)

print("diverge compares a fork against its upstream (§10)")
with tempfile.TemporaryDirectory(prefix="ergo-div-") as _d:
    dd = Path(_d)
    MAN = ('```toml ergo\n[dataset]\nergo = "0.5"\nslug = "{slug}"\ntitle = "{slug}"\n'
           'publisher = "P"\nsubject = "https://x.org/d"\n'
           'source_urls = ["https://x.org/d"]\npitfall = "One sentence."\n'
           'status = "live"\nupdated = "2026-07-20"\n{extra}```\n')
    ISS = ('\n### {id}\n\n```toml ergo\n[issue]\nid = "{id}"\ntitle = "{id}"\n'
           'effect = "corrupts"\ntype = "format"\nstatus = "open"\n'
           '[issue.scope]\nall = true\n```\n')
    up = dd / "upstream.md"
    up.write_text("# U\n\n" + MAN.format(slug="up", extra="") + ISS.format(id="shared")
                  + ISS.format(id="added-later")
                  + '\n## Changelog\n\n```toml ergo\n[change]\ndate = "2026-07-20"\n'
                    'note = "Registered a coverage gap."\nissues = ["added-later"]\n```\n',
                  encoding="utf-8")
    stale = "sha256:" + "0" * 64
    fork = dd / "fork.md"
    fork.write_text(
        "# F\n\n" + MAN.format(slug="fork", extra=(
            "\n[[dataset.derived_from]]\n"
            f'url = "file://{up}"\nretrieved = "2026-07-10"\nhash = "{stale}"\n'))
        + ISS.format(id="shared") + ISS.format(id="ours-alone"), encoding="utf-8")

    code, out = run("diverge", fork, "--json")
    check("diverge exits 0 when the upstream reads", code == 0, out.strip()[:200])
    rep = json.loads(out)["upstreams"][0]
    check("a stale hash reports the upstream as moved", rep["unchanged"] is False, str(rep)[:200])
    check("the current hash is reported so it can be pasted back",
          rep["current_hash"].startswith("sha256:"), str(rep["current_hash"]))
    check("upstream [change] records after `retrieved` are surfaced",
          [c["date"] for c in rep["upstream_changes_since"]] == ["2026-07-20"],
          str(rep["upstream_changes_since"]))
    check("ids only upstream has are listed",
          [e["id"] for e in rep["only_upstream"]] == ["added-later"], str(rep["only_upstream"]))
    check("ids only the fork has are listed (the offer-back queue)",
          [e["id"] for e in rep["only_here"]] == ["ours-alone"], str(rep["only_here"]))

    good = fork.read_text(encoding="utf-8").replace(stale, rep["current_hash"])
    fork.write_text(good, encoding="utf-8")
    code, out = run("diverge", fork, "--json")
    rep = json.loads(out)["upstreams"][0]
    check("a matching hash reports the upstream unmoved", rep["unchanged"] is True, str(rep)[:160])
    check("and a hash that disagrees with the changelog is called out",
          rep["inconsistent"] is True, str(rep)[:160])

    missing = dd / "gone.md"
    missing.write_text("# G\n\n" + MAN.format(slug="gone", extra=(
        "\n[[dataset.derived_from]]\n"
        f'url = "file://{dd}/not-there.md"\nretrieved = "2026-07-10"\n'
        f'hash = "{stale}"\n')), encoding="utf-8")
    code, out = run("diverge", missing)
    check("an unreadable upstream exits 1 rather than reporting no difference",
          code == 1 and "could not read the upstream" in out, out.strip()[:200])

print("scan finds handled-but-undocumented sites (§12)")
# Outside the repo on purpose: `scan` walks git-tracked files when it can, so
# an in-repo fixture would have to be staged to be seen at all.
with tempfile.TemporaryDirectory(prefix="ergo-scan-") as _tmp:
    scan_dir = Path(_tmp)
    (scan_dir / "loader.py").write_text(
        'SRC = "https://example.gov/data/2024/enr.xlsx"\n'
        'COLUMN_MAP = {"Cnty Code": "county_code"}\n'
        'def load(year):\n'
        '    if year < 2009:\n'
        '        df = read_fwf(SRC, colspecs=[(0, 2)])\n'
        '    df = read_excel(SRC, sheet_name="Enr", skiprows=3)\n'
        '    df = df.rename(columns=COLUMN_MAP)\n'
        '    df["cc"] = df["cc"].astype(str).str.zfill(2)\n'
        '    df.loc[df["rate"] == "*", "rate"] = None\n'
        '    df["rate"] = df["rate"].fillna(0)\n'
        '    # HACK: some files are latin-1\n'
        '    try:\n'
        '        notes = read_csv("n.csv", encoding="latin-1")\n'
        '    except ValueError:\n'
        '        notes = None\n'
        '    return df\n'
        'def documented(df):\n'
        '    # ergo: enr/prose-suppression\n'
        '    df.loc[df["rate"] == "*", "rate"] = None\n'
        '    return df\n', encoding="utf-8")
    (scan_dir / "notes.md").write_text("# not scanned - wrong extension\n", encoding="utf-8")

    code, out = run("scan", scan_dir, "--json")
    check("scan exits 0", code == 0, out.strip()[:200])
    payload = json.loads(out)
    signals = {c["signal"] for c in payload["candidates"]}
    for probe in ["sentinel-comparison", "null-filling", "era-branch",
                  "column-rename", "workbook-layout", "fixed-width",
                  "identifier-padding", "encoding-fallback", "parse-guard",
                  "hardcoded-source-url", "flagged-comment"]:
        check(f"scan signal: {probe}", probe in signals, str(sorted(signals)))
    check("anchored lines are skipped, not reported",
          payload["stats"]["already_anchored"] >= 1, str(payload["stats"]))
    check("the anchored duplicate is not a candidate",
          sum(1 for c in payload["candidates"] if c["signal"] == "sentinel-comparison") == 1,
          str([c["line"] for c in payload["candidates"] if c["signal"] == "sentinel-comparison"]))
    check("only source files are scanned",
          payload["stats"]["files_scanned"] == 1, str(payload["stats"]))
    code, out = run("scan", scan_dir)
    check("scan says a hit is a workaround, not a defect",
          "not that the reading behind it was right" in out, out.strip()[:200])

print("subject normalization clusters correctly (§10)")
import importlib.util
_spec = importlib.util.spec_from_file_location("ergo_tool_rt", ERGO)
_ergo = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ergo)
norm = _ergo.normalize_subject
acs = [
    "https://WWW.Census.GOV/programs-surveys/acs/",
    "http://census.gov/programs-surveys/acs",
    "https://www.census.gov/programs-surveys/acs/index.html",
    "https://census.gov/programs-surveys/acs#notes",
]
check("scheme/host/www/slash/index.html/fragment all fold together",
      len({norm(u) for u in acs}) == 1, str({norm(u) for u in acs}))
check("query string is preserved as identity",
      norm("https://x.org/d?dataset=foo") != norm("https://x.org/d?dataset=bar"))
check("distinct datasets stay distinct",
      norm("https://census.gov/acs") != norm("https://census.gov/cps"))
check("empty subject normalizes to empty", norm("") == "" and norm(None) == "")
check("non-URL passes through without crashing", norm("not a url") == "not a url")
ufb = ["https://www.nj.gov/education/budget/ufb/index.shtml",
       "https://nj.gov/education/budget/ufb/",
       "http://WWW.NJ.gov/education/budget/ufb/index.shtml"]
check("index pages fold across extensions (.shtml, not just .html)",
      len({norm(u) for u in ufb}) == 1, str({norm(u) for u in ufb}))

print("directory emit (§10)")
code, out = run("directory", ROOT / "examples", "--bundle", "https://example.org/ergo/")
check("directory exits 0", code == 0, out.strip()[:200])
try:
    doc = json.loads(out[:out.rindex("}") + 1])
    entry = doc["entries"][0]
    check("entry carries subject + normalized form",
          entry["subject"] and entry["subject_normalized"] == norm(entry["subject"]))
    check("entry points at the bundle, not page content",
          entry["bundle"] == "https://example.org/ergo/" and "issues" not in entry)
    check("contribute travels into the entry (§10 one home)",
          entry.get("contribute") == "https://github.com/lavallee/ergo/issues",
          str(entry.get("contribute")))
    check("recognition signatures emitted", bool(entry.get("recognizes")))
except (ValueError, KeyError, IndexError) as e:
    check("directory output is valid JSON with entries", False, str(e))

print()
if failures:
    print(f"{len(failures)} failure(s): {', '.join(failures)}")
    sys.exit(1)
print("all tests passed")
