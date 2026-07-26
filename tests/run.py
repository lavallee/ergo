#!/usr/bin/env python3
"""Test suite for ergo.py. Stdlib only, no framework.

    python3 tests/run.py          # from the repo root

Asserts three things: the shipped positive fixtures are clean, the negative
fixture triggers every error class we claim to catch, and a 0.1-shaped page
still validates under the current tool.
"""
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
check("warning count == 8", n_warn == 8, f"got {n_warn}")
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
]:
    check(f"catches: {probe}", probe in out)

print("0.1 pages still validate (backward compatibility)")
legacy = ROOT / "tests" / "legacy-0.1.md"
src = (ROOT / "examples" / "spr.md").read_text(encoding="utf-8")
src = src.replace('ergo = "0.2"', 'ergo = "0.1"').replace(
    'source_urls = ["https://www.nj.gov/education/spr/"]',
    'source_url = "https://www.nj.gov/education/spr/"')
src = re.sub(r'version = .*\n', '', src, count=1)
src = re.sub(r'unknowns = \[.*?\n\]\n', '', src, flags=re.S)
src = re.sub(r'\[dataset\.missingness\]\n.*?\n\n', '', src, flags=re.S)
legacy.write_text(src, encoding="utf-8")
try:
    code, out = run("check", legacy, "--strict")
    check("0.1 manifest shape: 0 errors, 0 warnings", counts(out) == (0, 0), out.strip())
finally:
    legacy.unlink(missing_ok=True)

print("digest and export run")
for cmd in ("digest", "export"):
    code, out = run(cmd, ROOT / "examples")
    check(f"{cmd} exits 0", code == 0, out.strip()[:200])

print()
if failures:
    print(f"{len(failures)} failure(s): {', '.join(failures)}")
    sys.exit(1)
print("all tests passed")
