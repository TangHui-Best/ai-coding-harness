from __future__ import annotations

import json
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS = REPO_ROOT / "skills"


def read_skill(name: str) -> str:
    return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")


class SkillProgressiveDisclosureTests(unittest.TestCase):
    def test_harness_entrypoint_uses_progressive_disclosure(self) -> None:
        content = read_skill("using-harness")

        self.assertIn("Reference Map", content)
        self.assertIn("Use references only when their trigger applies", content)

    def test_knowledge_capture_uses_progressive_disclosure(self) -> None:
        content = read_skill("harness-knowledge-capture")

        self.assertIn("Reference Map", content)
        self.assertIn("references/completion-closeout-contract.md", content)
        self.assertIn("references/artifact-decision-matrix.md", content)
        self.assertIn("references/bugfix-attribution-and-patch-churn.md", content)

    def test_high_frequency_gates_use_progressive_disclosure(self) -> None:
        expected_refs = {
            "harness-start-gate": [
                "references/start-gate-decision-rules.md",
                "references/bug-intake-and-patch-churn.md",
            ],
            "harness-knowledge-retrieval": [
                "references/retrieval-order.md",
                "references/bug-retrieval-mode.md",
            ],
            "harness-readiness-dashboard": [
                "references/readiness-checks.md",
            ],
        }

        for skill, refs in expected_refs.items():
            content = read_skill(skill)
            self.assertIn("Reference Map", content)
            self.assertIn("Use references only when their trigger applies", content)
            for ref in refs:
                self.assertIn(ref, content)

    def test_script_resources_are_global_execute_first_contract(self) -> None:
        using_harness = read_skill("using-harness")
        capture = read_skill("harness-knowledge-capture")

        for content in [using_harness, capture]:
            self.assertIn("Execute bundled scripts; do not read script source", content)
            self.assertIn("unless debugging or editing that script", content)

    def test_verification_resources_are_run_first_contract(self) -> None:
        using_harness = read_skill("using-harness")
        capture = read_skill("harness-knowledge-capture")

        for content in [using_harness, capture]:
            self.assertIn("Run verification commands before reading verification source", content)
            self.assertIn("Do not read test files, validator scripts, or workflow files merely to verify", content)
            self.assertIn("Read them only when debugging a failure, editing them, reviewing them, or explaining their behavior", content)

    def test_referenced_harness_material_exists(self) -> None:
        expected = [
            SKILLS / "using-harness" / "references" / "routing.md",
            SKILLS / "using-harness" / "references" / "task-routing-fixtures.md",
            SKILLS
            / "harness-knowledge-capture"
            / "references"
            / "completion-closeout-contract.md",
            SKILLS
            / "harness-knowledge-capture"
            / "references"
            / "artifact-decision-matrix.md",
            SKILLS
            / "harness-knowledge-capture"
            / "references"
            / "bugfix-attribution-and-patch-churn.md",
            SKILLS
            / "harness-start-gate"
            / "references"
            / "start-gate-decision-rules.md",
            SKILLS
            / "harness-start-gate"
            / "references"
            / "bug-intake-and-patch-churn.md",
            SKILLS
            / "harness-knowledge-retrieval"
            / "references"
            / "retrieval-order.md",
            SKILLS
            / "harness-knowledge-retrieval"
            / "references"
            / "bug-retrieval-mode.md",
            SKILLS
            / "harness-readiness-dashboard"
            / "references"
            / "readiness-checks.md",
            SKILLS
            / "using-harness"
            / "assets"
            / "templates"
            / "CLOSEOUT_COMPACT.md",
        ]

        for path in expected:
            self.assertTrue(path.exists(), f"missing referenced file: {path}")

    def test_task_routing_fixtures_cover_common_workflows(self) -> None:
        content = (
            SKILLS
            / "using-harness"
            / "references"
            / "task-routing-fixtures.md"
        ).read_text(encoding="utf-8")

        for scenario in [
            "tiny bugfix",
            "non-tiny bugfix",
            "commit-only",
            "PR description",
            "skill edit",
            "artifact updated",
            "no artifact needed",
        ]:
            self.assertIn(scenario, content)

    def test_closeout_template_and_install_sync_are_discoverable(self) -> None:
        using_harness = read_skill("using-harness")
        capture = read_skill("harness-knowledge-capture")

        self.assertIn("assets/templates/CLOSEOUT_COMPACT.md", using_harness)
        self.assertIn("assets/templates/CLOSEOUT_COMPACT.md", capture)
        self.assertTrue((REPO_ROOT / "scripts" / "install.ps1").exists())
        self.assertTrue((REPO_ROOT / "scripts" / "install.sh").exists())

    def test_optional_hook_runtime_resources_are_discoverable(self) -> None:
        using_harness = read_skill("using-harness")
        install = (REPO_ROOT / "INSTALL.md").read_text(encoding="utf-8")

        for path in [
            REPO_ROOT / "hooks.json",
            REPO_ROOT / "hooks" / "hooks.json",
            REPO_ROOT / "hooks" / "run-harness-hook.cmd",
            SKILLS / "using-harness" / "hooks" / "harness_hook.py",
            SKILLS / "using-harness" / "scripts" / "hook_diagnostics.py",
            SKILLS / "using-harness" / "hooks" / "codex-hooks.example.json",
            SKILLS / "using-harness" / "hooks" / "claude-settings.example.json",
            SKILLS / "using-harness" / "hooks" / "opencode-plugin.example.ts",
        ]:
            self.assertTrue(path.exists(), f"missing optional hook resource: {path}")

        self.assertIn("Optional Hook Runtime", using_harness)
        self.assertIn("Skills-only install remains valid", using_harness)
        self.assertIn("Default examples install only `stop`, `session-start`, and `pre-compact`", using_harness)
        self.assertIn("hook_diagnostics.py", using_harness)
        self.assertIn("Basic install: Skills only", install)
        self.assertIn("Enhanced install: Skills + optional Hooks", install)
        self.assertIn("Hook installation failure must not roll back Skills", install)
        self.assertIn("Default hook examples enable Stop plus session recovery hooks", install)
        self.assertIn("hook_diagnostics.py", install)

    def test_default_hook_examples_do_not_wire_post_tool_use(self) -> None:
        examples = {
            "codex": SKILLS
            / "using-harness"
            / "hooks"
            / "codex-hooks.example.json",
            "claude": SKILLS
            / "using-harness"
            / "hooks"
            / "claude-settings.example.json",
            "opencode": SKILLS
            / "using-harness"
            / "hooks"
            / "opencode-plugin.example.ts",
        }

        forbidden = ["postToolUse", "PostToolUse", "tool.execute.after"]
        for name, path in examples.items():
            content = path.read_text(encoding="utf-8")
            for phrase in forbidden:
                self.assertNotIn(phrase, content, f"{name} wires {phrase} by default")

    def test_default_hook_examples_wire_session_recovery_hooks(self) -> None:
        examples = {
            "codex": SKILLS
            / "using-harness"
            / "hooks"
            / "codex-hooks.example.json",
            "claude": SKILLS
            / "using-harness"
            / "hooks"
            / "claude-settings.example.json",
            "opencode": SKILLS
            / "using-harness"
            / "hooks"
            / "opencode-plugin.example.ts",
        }

        for name, path in examples.items():
            content = path.read_text(encoding="utf-8")
            self.assertTrue(
                "--event" in content or "run-harness-hook.cmd" in content,
                f"{name} does not invoke the hook runner",
            )
            self.assertIn("session-start", content, f"{name} does not wire session-start")
            self.assertIn("pre-compact", content, f"{name} does not wire pre-compact")

    def test_opencode_hook_example_uses_compaction_context_output(self) -> None:
        path = SKILLS / "using-harness" / "hooks" / "opencode-plugin.example.ts"
        content = path.read_text(encoding="utf-8")

        self.assertIn('"experimental.session.compacting": async (input, output)', content)
        self.assertIn("output.context.push", content)
        self.assertIn("sessionID", content)
        self.assertNotIn('"session.created"', content)

    def test_codex_hook_example_uses_codex_schema(self) -> None:
        path = SKILLS / "using-harness" / "hooks" / "codex-hooks.example.json"
        config = json.loads(path.read_text(encoding="utf-8"))
        self.assertIn("hooks", config)
        for event in ["SessionStart", "PreCompact", "Stop"]:
            self.assertIn(event, config["hooks"])
        self.assertEqual(config["hooks"]["SessionStart"][0]["matcher"], "compact")
        self.assertEqual(config["hooks"]["PreCompact"][0]["matcher"], "")

    def test_codex_hook_example_uses_plugin_root_wrapper_commands(self) -> None:
        path = SKILLS / "using-harness" / "hooks" / "codex-hooks.example.json"
        config = json.loads(path.read_text(encoding="utf-8"))
        root_config = json.loads((REPO_ROOT / "hooks.json").read_text(encoding="utf-8"))
        nested_config = json.loads((REPO_ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8"))
        serialized = json.dumps(config)

        self.assertNotIn("HARNESS_SKILL_ROOT", serialized)
        self.assertNotIn("python ./skills", serialized)
        self.assertIn("CLAUDE_PLUGIN_ROOT", serialized)
        self.assertIn("PLUGIN_ROOT", serialized)
        self.assertEqual(root_config, config)
        self.assertEqual(nested_config, config)
        for event, normalized in [
            ("SessionStart", "session-start"),
            ("PreCompact", "pre-compact"),
            ("Stop", "stop"),
        ]:
            command = config["hooks"][event][0]["hooks"][0]["command"]
            command_windows = config["hooks"][event][0]["hooks"][0]["commandWindows"]
            self.assertEqual(
                command,
                f"\"${{CLAUDE_PLUGIN_ROOT}}/hooks/run-harness-hook.cmd\" {normalized}",
            )
            self.assertEqual(
                command_windows,
                f"\"%PLUGIN_ROOT%\\hooks\\run-harness-hook.cmd\" {normalized}",
            )

    def test_hot_path_constraints_remain_in_primary_skill_text(self) -> None:
        using_harness = read_skill("using-harness")
        capture = read_skill("harness-knowledge-capture")
        start_gate = read_skill("harness-start-gate")

        for phrase in [
            "Entry And Exit Gates",
            "Core Rule",
            "Superpowers specs and plans are linked material",
        ]:
            self.assertIn(phrase, using_harness)

        for phrase in [
            "Artifact Placement",
            "Templates",
            "Stable IDs",
            "docs/features/Fxxx-slug.md",
        ]:
            self.assertIn(phrase, capture)

        for phrase in [
            "Task Classes",
            "Risk Triggers",
            "Patch Churn Check",
        ]:
            self.assertIn(phrase, start_gate)


if __name__ == "__main__":
    unittest.main()
