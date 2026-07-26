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
check("error count == 19", n_err == 19, f"got {n_err}")
check("warning count == 9", n_warn == 9, f"got {n_warn}")
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
    # warnings
    "outside the recommended taxonomy",
    "names no naive alternative",
    "practices take no scope",
    "but names no misuse",
    "no subject — directories cluster pages by subject URL",
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
    check("recognition signatures emitted", bool(entry.get("recognizes")))
except (ValueError, KeyError, IndexError) as e:
    check("directory output is valid JSON with entries", False, str(e))

print()
if failures:
    print(f"{len(failures)} failure(s): {', '.join(failures)}")
    sys.exit(1)
print("all tests passed")
