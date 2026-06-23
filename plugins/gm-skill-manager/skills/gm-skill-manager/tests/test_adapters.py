from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from adapters.claude import collect_claude_evidence
from adapters.codex import collect_codex_evidence
from adapters.npx_skills import collect_npx_evidence


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def write_skill(path: Path, name: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\nname: {name}\ndescription: test\n---\n", encoding="utf-8")


class AdapterTests(unittest.TestCase):
    def test_codex_native_and_builtins(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            marketplace = home / "market"
            plugin = marketplace / "plugins" / "demo"
            write_skill(plugin / "skills" / "demo" / "SKILL.md", "demo")
            write_skill(home / ".codex" / "skills" / ".system" / "creator" / "SKILL.md", "creator")
            config = f"""
[marketplaces.demo]
source_type = "git"
source = "https://github.com/acme/repo.git"
last_revision = "abc"
"""
            config_path = home / ".codex" / "config.toml"
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config_path.write_text(config, encoding="utf-8")
            payload = {
                "installed": [
                    {
                        "name": "demo",
                        "marketplaceName": "demo",
                        "version": "1.0.0",
                        "enabled": True,
                        "source": {"source": "local", "path": str(plugin)},
                        "marketplaceSource": {"sourceType": "git", "source": "https://github.com/acme/repo.git"},
                    }
                ]
            }
            rows = collect_codex_evidence(home, [], use_native_commands=False, native_payload=payload)
            plugin_row = next(row for row in rows if row["package_format"] == "codex-plugin")
            builtin_row = next(row for row in rows if row["package_format"] == "built-in")
            self.assertEqual("plugins/demo/skills/demo/SKILL.md", plugin_row["capabilities"][0]["skill_path"])
            self.assertEqual(".system/creator/SKILL.md", builtin_row["capabilities"][0]["skill_path"])
            self.assertEqual("unknown", plugin_row["exposure_state"])
            self.assertEqual("unknown", plugin_row["verification"]["discovery"])

    def test_claude_scopes_and_broken_installation(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            market = home / ".claude/plugins/marketplaces/acme"
            install = home / ".claude/plugins/cache/acme/demo/1"
            write_skill(install / "skills/demo/SKILL.md", "demo")
            write_json(
                market / ".claude-plugin/marketplace.json",
                {"plugins": [{"name": "demo", "source": "./plugins/demo"}]},
            )
            write_json(
                home / ".claude/plugins/known_marketplaces.json",
                {
                    "acme": {
                        "source": {"source": "github", "repo": "acme/repo"},
                        "installLocation": str(market),
                    }
                },
            )
            write_json(
                home / ".claude/plugins/installed_plugins.json",
                {
                    "plugins": {
                        "demo@acme": [
                            {"scope": "user", "installPath": str(install), "gitCommitSha": "a"},
                            {
                                "scope": "project",
                                "projectPath": "/project",
                                "installPath": str(home / "missing"),
                                "gitCommitSha": "b",
                            },
                        ]
                    }
                },
            )
            rows = collect_claude_evidence(home, [])
            self.assertEqual({"installed", "broken"}, {row["installation_state"] for row in rows})
            self.assertEqual({"user", "project"}, {row["scope"] for row in rows})
            self.assertTrue(all(row["exposure_state"] == "unknown" for row in rows))
            self.assertTrue(all(row["verification"]["discovery"] == "unknown" for row in rows))

    def test_npx_lock_and_exposure_are_separate(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            write_json(
                home / ".agents/.skill-lock.json",
                {
                    "skills": {
                        "demo": {
                            "sourceType": "github",
                            "sourceUrl": "https://github.com/acme/repo.git",
                            "skillPath": "skills/demo/SKILL.md",
                            "skillFolderHash": "abc",
                        },
                        "inactive": {
                            "sourceType": "github",
                            "sourceUrl": "https://github.com/acme/repo.git",
                            "skillPath": "skills/inactive/SKILL.md",
                            "skillFolderHash": "def",
                        },
                    }
                },
            )
            listed = [
                {
                    "name": "demo",
                    "path": str(home / ".agents/skills/demo"),
                    "agents": ["Codex", "Claude Code"],
                },
                {
                    "name": "orphan",
                    "path": str(home / ".agents/skills/orphan"),
                    "agents": ["Codex"],
                },
            ]
            rows = collect_npx_evidence(home, [], use_native_commands=False, list_payload=listed)
            demo = [row for row in rows if row["package_name"] == "demo"]
            inactive = next(row for row in rows if row["package_name"] == "inactive")
            orphan = next(row for row in rows if row["package_name"] == "orphan")
            self.assertEqual({"codex", "claude-code"}, {row["runtime"] for row in demo})
            self.assertEqual(1, len({row["installation_key"] for row in demo}))
            self.assertEqual("inactive", inactive["exposure_state"])
            self.assertEqual("broken", orphan["installation_state"])

    def test_npx_project_scope_requires_explicit_project(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp) / "home"
            project = Path(temp) / "project"
            write_json(
                project / "skills-lock.json",
                {
                    "skills": {
                        "demo": {
                            "sourceType": "github",
                            "sourceUrl": "https://github.com/acme/repo.git",
                            "skillPath": "skills/demo/SKILL.md",
                            "skillFolderHash": "abc",
                        }
                    }
                },
            )
            listed = [
                {
                    "name": "demo",
                    "path": str(project / ".agents/skills/demo"),
                    "agents": ["Codex"],
                }
            ]
            without_project = collect_npx_evidence(home, [], use_native_commands=False)
            with_project = collect_npx_evidence(
                home,
                [],
                project=project,
                use_native_commands=False,
                project_list_payload=listed,
            )
            self.assertEqual([], without_project)
            self.assertEqual("project", with_project[0]["scope"])
            self.assertEqual(str(project.resolve()), with_project[0]["project_path"])

    def test_missing_plugin_install_paths_do_not_scan_the_working_directory(self):
        codex_rows = collect_codex_evidence(
            Path("/missing-home"),
            [],
            use_native_commands=False,
            native_payload={
                "installed": [
                    {
                        "name": "missing",
                        "enabled": True,
                        "source": {},
                        "marketplaceSource": {
                            "sourceType": "git",
                            "source": "https://github.com/acme/repo.git",
                        },
                    }
                ]
            },
        )
        self.assertEqual("broken", codex_rows[0]["installation_state"])
        self.assertEqual("unknown", codex_rows[0]["capabilities"][0]["skill_path"])

        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            write_json(
                home / ".claude/plugins/installed_plugins.json",
                {"plugins": {"missing@acme": [{"scope": "user"}]}},
            )
            write_json(
                home / ".claude/plugins/known_marketplaces.json",
                {"acme": {"source": {"source": "github", "repo": "acme/repo"}}},
            )
            claude_rows = collect_claude_evidence(home, [])
            self.assertEqual("broken", claude_rows[0]["installation_state"])
            self.assertEqual("unknown", claude_rows[0]["capabilities"][0]["skill_path"])


if __name__ == "__main__":
    unittest.main()
