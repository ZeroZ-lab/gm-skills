from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from identity import normalize_remote
from inventory_model import build_inventory


def evidence(runtime, package_format, channel, remote, package_path, skill_path, revision, scope="user"):
    return {
        "runtime": runtime,
        "package_format": package_format,
        "installation_channel": channel,
        "scope": scope,
        "installation_state": "installed",
        "exposure_state": "active",
        "installer_available": True,
        "installer_compatible": True,
        "remote_source": remote,
        "package_path": package_path,
        "package_name": "gm-skill-manager",
        "revision": revision,
        "install_path": f"/cache/{runtime}/{channel}",
        "project_path": "unknown",
        "development_local": False,
        "capabilities": [
            {
                "name": "gm-skill-manager",
                "skill_path": skill_path,
                "aliases": [],
            }
        ],
        "verification": {"registry": "verified", "discovery": "verified"},
        "aliases": [],
        "notes": [],
    }


class IdentityInventoryTests(unittest.TestCase):
    def test_remote_normalization(self):
        expected = "https://github.com/ZeroZ-lab/gm-skills"
        self.assertEqual(expected, normalize_remote("git@github.com:ZeroZ-lab/gm-skills.git"))
        self.assertEqual(expected, normalize_remote("https://user:secret@github.com/ZeroZ-lab/gm-skills.git?token=x"))

    def test_three_formats_converge_but_revisions_remain_separate(self):
        remote = "https://github.com/ZeroZ-lab/gm-skills.git"
        skill = "plugins/gm-skill-manager/skills/gm-skill-manager/SKILL.md"
        rows = [
            evidence("codex", "codex-plugin", "codex-plugin", remote, "plugins/gm-skill-manager", skill, "aaa"),
            evidence(
                "claude-code",
                "claude-code-plugin",
                "claude-code-plugin",
                "git@github.com:ZeroZ-lab/gm-skills.git",
                "plugins/gm-skill-manager",
                skill,
                "bbb",
            ),
            evidence("codex", "npx-skills", "npx-skills", remote, str(Path(skill).parent), skill, "aaa"),
        ]
        payload = build_inventory(Path("/home/test"), rows, [])
        self.assertEqual("1.0", payload["schema_version"])
        self.assertEqual(1, len(payload["capabilities"]))
        self.assertEqual("different", payload["capabilities"][0]["revision_relation"])
        self.assertEqual(3, len(payload["installations"]))
        self.assertEqual(2, len(payload["packages"]))
        codex_exposures = [row for row in payload["capabilities"][0]["exposures"] if row["runtime"] == "codex"]
        self.assertTrue(all(row["state"] == "ambiguous" for row in codex_exposures))

    def test_npx_multi_runtime_exposures_share_one_installation(self):
        remote = "https://github.com/ZeroZ-lab/gm-skills.git"
        skill = "plugins/gm-skill-manager/skills/gm-skill-manager/SKILL.md"
        codex = evidence("codex", "npx-skills", "npx-skills", remote, str(Path(skill).parent), skill, "aaa")
        claude = evidence(
            "claude-code",
            "npx-skills",
            "npx-skills",
            remote,
            str(Path(skill).parent),
            skill,
            "aaa",
        )
        codex["installation_key"] = "global:lock:gm-skill-manager"
        claude["installation_key"] = codex["installation_key"]
        payload = build_inventory(Path("/home/test"), [codex, claude], [])
        self.assertEqual(1, len(payload["installations"]))
        self.assertEqual(["claude-code", "codex"], sorted(payload["installations"][0]["target_runtimes"]))
        self.assertEqual(2, len(payload["capabilities"][0]["exposures"]))
        self.assertEqual(
            2,
            len({row["exposure_id"] for row in payload["capabilities"][0]["exposures"]}),
        )

    def test_incomplete_evidence_does_not_match_by_name(self):
        rows = [
            evidence("codex", "codex-plugin", "codex-plugin", "unknown", "unknown", "unknown", "1"),
            evidence("claude-code", "claude-code-plugin", "claude-code-plugin", "unknown", "unknown", "unknown", "1"),
        ]
        payload = build_inventory(Path("/home/test"), rows, [])
        self.assertEqual(2, len(payload["capabilities"]))
        self.assertTrue(all(row["identity"]["status"] == "unresolved" for row in payload["capabilities"]))

    def test_builtin_identity_uses_runtime_and_path(self):
        row = evidence(
            "codex",
            "built-in",
            "built-in",
            "unknown",
            "unknown",
            ".system/skill-creator/SKILL.md",
            "codex 1.0",
            "system",
        )
        payload = build_inventory(Path("/home/test"), [row], [])
        self.assertEqual(
            "builtin:codex:.system/skill-creator/SKILL.md",
            payload["capabilities"][0]["identity"]["key"],
        )

    def test_separate_project_scopes_are_not_duplicate_exposures(self):
        remote = "https://github.com/ZeroZ-lab/gm-skills.git"
        skill = "plugins/gm-skill-manager/skills/gm-skill-manager/SKILL.md"
        first = evidence(
            "claude-code",
            "claude-code-plugin",
            "claude-code-plugin",
            remote,
            "plugins/gm-skill-manager",
            skill,
            "aaa",
            "project",
        )
        first["project_path"] = "/work/first"
        second = dict(first)
        second["install_path"] = "/cache/claude-code/second"
        second["project_path"] = "/work/second"
        payload = build_inventory(Path("/home/test"), [first, second], [])
        states = [row["state"] for row in payload["capabilities"][0]["exposures"]]
        self.assertEqual(["active", "active"], states)

    def test_global_and_project_exposures_are_ambiguous(self):
        remote = "https://github.com/ZeroZ-lab/gm-skills.git"
        skill = "plugins/gm-skill-manager/skills/gm-skill-manager/SKILL.md"
        global_row = evidence(
            "claude-code",
            "claude-code-plugin",
            "claude-code-plugin",
            remote,
            "plugins/gm-skill-manager",
            skill,
            "aaa",
            "user",
        )
        project_row = evidence(
            "claude-code",
            "claude-code-plugin",
            "claude-code-plugin",
            remote,
            "plugins/gm-skill-manager",
            skill,
            "aaa",
            "project",
        )
        project_row["project_path"] = "/work/project"
        payload = build_inventory(Path("/home/test"), [global_row, project_row], [])
        states = [row["state"] for row in payload["capabilities"][0]["exposures"]]
        self.assertEqual(["ambiguous", "ambiguous"], states)
        runtime_row = next(row for row in payload["views"]["runtime"] if row["runtime"] == "claude-code")
        self.assertEqual(["ambiguous"], runtime_row["states"])


if __name__ == "__main__":
    unittest.main()
