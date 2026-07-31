window.__ERGO_META__ = {
  "generated": "2026-07-31T13:52:01+00:00",
  "tool_version": "0.5.0",
  "format_version": "0.5",
  "revision": "4a258ce",
  "spec_status": "draft v0.5 · 2026-07-31",
  "spec_lines": 1516,
  "spec_sections": 16,
  "tool_lines": 1380,
  "checks": 90,
  "dependencies": [],
  "requires_python": "3.11",
  "license": "MIT",
  "cli": [
    {
      "name": "check",
      "summary": "Parse the pages and enforce the format. With --repo, cross-check the code round trip.",
      "usage": "ergo.py check [-h] [--repo ROOT] [--strict] [--require-manifest] [paths ...]"
    },
    {
      "name": "digest",
      "summary": "The INDEX.md table: one row per dataset, issue counts by effect, the pitfall.",
      "usage": "ergo.py digest [-h] [--long] [--write FILE] [paths ...]"
    },
    {
      "name": "export",
      "summary": "Everything machine-readable as one JSON document, for renders and interop.",
      "usage": "ergo.py export [-h] [--out FILE] [paths ...]"
    },
    {
      "name": "publish",
      "summary": "The servable bundle: index.json plus each page's public projection.",
      "usage": "ergo.py publish [-h] --dir OUT [--base-url URL] [paths ...]"
    },
    {
      "name": "directory",
      "summary": "This project's entries for a directory of bundles, with recognition signatures.",
      "usage": "ergo.py directory [-h] [--bundle URL] [--name NAME] [--entries-only] [--out FILE] [paths ...]"
    },
    {
      "name": "scan",
      "summary": "Read code that already works with a dataset and list what its author handled.",
      "usage": "ergo.py scan [-h] [--json] [--out FILE] [paths ...]"
    },
    {
      "name": "diverge",
      "summary": "Compare a forked page against its upstream: what moved, what they added, what you have that they don't.",
      "usage": "ergo.py diverge [-h] [--json] [--timeout SECONDS] [--out FILE] [paths ...]"
    },
    {
      "name": "new",
      "summary": "Scaffold a fresh page from the template.",
      "usage": "ergo.py new [-h] [--dir DIR] slug"
    }
  ],
  "issue_types": 16,
  "example": {
    "path": "examples/spr.md",
    "issues": 5,
    "practices": 2
  }
};
