from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from inventory_model import build_inventory
from views import redact_inventory


class ViewsDoctorTests(unittest.TestCase):
    def test_views_are_derived_from_same_entities(self):
        payload = build_inventory(Path("/Users/test"), [], ["ZCode detected but unmanaged."])
        self.assertEqual(0, payload["diagnostics"]["facts"]["capability_count"])
        self.assertEqual([], payload["views"]["capability"])
        self.assertEqual([], payload["views"]["package"])
        self.assertEqual([], payload["views"]["runtime"])

    def test_nonempty_views_reference_the_same_inventory_entities(self):
        row = {
            "runtime": "codex",
            "package_format": "codex-plugin",
            "installation_channel": "codex-plugin",
            "scope": "user",
            "installation_state": "installed",
            "exposure_state": "unknown",
            "installer_available": True,
            "installer_compatible": True,
            "remote_source": "https://github.com/acme/repo.git",
            "package_path": "plugins/demo",
            "package_name": "demo",
            "revision": "abc",
            "install_path": "/cache/demo",
            "project_path": "unknown",
            "development_local": False,
            "capabilities": [{"name": "demo", "skill_path": "plugins/demo/skills/demo/SKILL.md", "aliases": []}],
            "verification": {"registry": "verified", "discovery": "unknown"},
            "aliases": [],
            "notes": [],
        }
        payload = build_inventory(Path("/Users/test"), [row], [])
        capability_id = payload["capabilities"][0]["capability_id"]
        package_id = payload["packages"][0]["package_id"]
        self.assertEqual(capability_id, payload["views"]["capability"][0]["capability_id"])
        self.assertEqual(package_id, payload["views"]["package"][0]["package_id"])
        self.assertEqual(1, payload["views"]["runtime"][0]["installation_count"])
        self.assertEqual(1, payload["views"]["runtime"][0]["capability_count"])
        self.assertEqual(["unknown"], payload["views"]["runtime"][0]["states"])

    def test_redaction_removes_home_credentials_and_query(self):
        payload = {
            "path": "/Users/test/private",
            "project_path": "/work/secret-project",
            "installation_key": "project:/work/secret-project:demo",
            "paths": {"project": "/another/private/project"},
            "remote": "https://user:secret@github.com/acme/repo.git?token=abc",
            "nested": ["password=hunter2"],
        }
        redacted = redact_inventory(payload, Path("/Users/test"))
        text = json.dumps(redacted)
        self.assertNotIn("/Users/test", text)
        self.assertNotIn("secret", text)
        self.assertNotIn("token=abc", text)
        self.assertNotIn("hunter2", text)
        self.assertNotIn("secret-project", text)
        self.assertNotIn("another/private", text)


if __name__ == "__main__":
    unittest.main()
