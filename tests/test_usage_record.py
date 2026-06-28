from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "usage_record.py"
BUNDLED_SCRIPT = REPO_ROOT / "skills" / "using-agentmentor" / "scripts" / "usage_record.py"


class UsageRecordTests(unittest.TestCase):
    def make_repo(self) -> tempfile.TemporaryDirectory[str]:
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "config", "user.name", "TangHui-Best"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
        doc = root / "docs" / "features" / "F009-feature-recall-governance.md"
        doc.parent.mkdir(parents=True)
        doc.write_text("# F009\n", encoding="utf-8")
        return tmp

    def test_appends_minimal_usage_record_under_git_user_file(self) -> None:
        with self.make_repo() as tmp:
            root = Path(tmp)
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--root",
                    str(root),
                    "--doc",
                    "docs/features/F009-feature-recall-governance.md",
                    "--doc-type",
                    "feature",
                    "--task",
                    "optimize feature recall",
                    "--impact",
                    "changed_verification_gate",
                ],
                text=True,
                capture_output=True,
            )

            target = root / ".agentmentor" / "usage" / "events" / "tanghui-best.jsonl"
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(target.exists())
            event = json.loads(target.read_text(encoding="utf-8").strip())
            self.assertEqual(
                set(event),
                {"ts", "doc", "doc_type", "task", "impact"},
            )
            self.assertTrue(event["ts"].endswith("Z"))
            self.assertEqual(event["doc"], "docs/features/F009-feature-recall-governance.md")
            self.assertEqual(event["doc_type"], "feature")
            self.assertEqual(event["task"], "optimize feature recall")
            self.assertEqual(event["impact"], "changed_verification_gate")

    def test_rejects_invalid_impact(self) -> None:
        with self.make_repo() as tmp:
            root = Path(tmp)
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--root",
                    str(root),
                    "--doc",
                    "docs/features/F009-feature-recall-governance.md",
                    "--doc-type",
                    "feature",
                    "--task",
                    "optimize feature recall",
                    "--impact",
                    "opened_but_unused",
                ],
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((root / ".agentmentor" / "usage").exists())

    def test_root_and_bundled_scripts_stay_identical(self) -> None:
        self.assertEqual(
            SCRIPT.read_text(encoding="utf-8"),
            BUNDLED_SCRIPT.read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
