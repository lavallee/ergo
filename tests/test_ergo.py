from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location("ergo_tool", ROOT / "tools" / "ergo.py")
assert SPEC is not None and SPEC.loader is not None
ERGO = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ERGO)


class ErgoToolTests(unittest.TestCase):
    def test_require_manifest_exposes_unstructured_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tmp_path = Path(directory)
            (tmp_path / "structured.md").write_text(
                """# Structured

```toml ergo
[dataset]
ergo = "0.1"
slug = "structured"
title = "Structured"
publisher = "Publisher"
source_url = "https://example.test"
bite = "A bite."
status = "live"
```
""",
                encoding="utf-8",
            )
            (tmp_path / "narrative.md").write_text(
                "# Narrative only\n", encoding="utf-8"
            )
            (tmp_path / "INDEX.md").write_text("# Generated\n", encoding="utf-8")

            self.assertEqual(len(ERGO.collect_pages([tmp_path])), 1)
            parsed = ERGO.collect_pages([tmp_path], require_manifest=True)
            self.assertEqual(len(parsed), 2)
            narrative, lines = next(
                item for item in parsed if item[0].path.name == "narrative.md"
            )
            ERGO.check_page(narrative, lines)
            self.assertEqual(
                narrative.errors,
                [(1, "no ergo blocks found — not a data page (or all blocks unparseable)")],
            )

    def test_independently_observed_issue_types_are_recommended(self) -> None:
        self.assertLessEqual({"identity", "policy"}, ERGO.TYPES)


if __name__ == "__main__":
    unittest.main()
