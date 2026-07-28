window.__ERGO_META__ = {
  "generated": "2026-07-28T13:51:04+00:00",
  "tool_version": "0.4.0",
  "format_version": "0.4",
  "revision": "2d3dbb2",
  "spec_status": "draft v0.4 · 2026-07-26",
  "spec_lines": 1030,
  "spec_sections": 16,
  "tool_lines": 938,
  "checks": 44,
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
      "name": "new",
      "summary": "Scaffold a fresh page from the template.",
      "usage": "ergo.py new [-h] [--dir DIR] slug"
    }
  ],
  "issue_types": 15,
  "example": {
    "path": "examples/spr.md",
    "issues": 5,
    "practices": 2
  }
};
