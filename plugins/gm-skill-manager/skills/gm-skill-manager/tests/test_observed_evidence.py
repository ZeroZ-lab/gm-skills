from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from inventory_model import build_inventory
from inventory import inventory
from observed_evidence import normalize_runtime_fact


def codex_fact(**overrides):
    fact = {
        "fact_type": "codex-plugin",
        "runtime": "codex",
        "native_record_id": "demo@gm",
        "scope": "user",
        "enabled": True,
        "installer_available": True,
        "installer_compatible": True,
        "remote_source": "https://github.com/acme/repo.git",
        "package_path": "plugins/demo",
        "package_name": "demo",
        "revision": "abc",
        "install_path": "/cache/demo",
        "install_exists": True,
        "development_local": False,
        "capabilities": [{"name": "demo", "skill_path": "plugins/demo/skills/demo/SKILL.md", "aliases": []}],
        "provenance": {"source_kind": "fixture", "source_id": "demo-record", "collection": "success"},
    }
    fact.update(overrides)
    return fact


class ObservedEvidenceTests(unittest.TestCase):
    def test_stable_identity_excludes_revision_and_state(self):
        first = normalize_runtime_fact(codex_fact(revision="a", enabled=True))
        second = normalize_runtime_fact(codex_fact(revision="b", enabled=False))
        self.assertEqual(first["evidence_id"], second["evidence_id"])
        self.assertEqual("unknown", first["exposure_facts"][0]["state"])
        self.assertEqual("inactive", second["exposure_facts"][0]["state"])

    def test_missing_identity_evidence_is_valid_but_unresolved(self):
        evidence = normalize_runtime_fact(
            codex_fact(remote_source="unknown", package_path="unknown", capabilities=[])
        )
        payload = build_inventory(Path("/home/test"), [evidence])
        self.assertEqual("valid", evidence["validity"])
        self.assertEqual("unresolved", payload["capabilities"][0]["identity"]["status"])

    def test_malformed_record_is_visible_but_creates_no_entities(self):
        fact = {
            "fact_type": "codex-plugin",
            "runtime": "codex",
            "native_record_id": "bad-record",
            "malformed": True,
            "provenance": {"source_kind": "fixture", "source_id": "bad", "collection": "success"},
        }
        payload = inventory(
            Path("/home/test"),
            use_native_commands=False,
            fixtures={"runtime-facts": [fact]},
        )
        evidence = payload["evidence"][0]
        self.assertEqual("invalid", evidence["validity"])
        self.assertEqual([], payload["packages"])
        self.assertEqual([], payload["installations"])
        self.assertEqual([], payload["capabilities"])
        self.assertTrue(any(row["code"] == "invalid-evidence" for row in payload["diagnostics"]["findings"]))

    def test_malformed_record_keeps_identity_when_repaired(self):
        malformed = codex_fact(malformed=True)
        invalid = normalize_runtime_fact(malformed)
        repaired = normalize_runtime_fact(codex_fact(revision="new"))
        self.assertEqual(invalid["evidence_id"], repaired["evidence_id"])
        self.assertEqual("invalid", invalid["validity"])
        self.assertEqual("valid", repaired["validity"])

    def test_runtime_detection_does_not_manufacture_package(self):
        evidence = normalize_runtime_fact(
            {
                "fact_type": "zcode-detection",
                "runtime": "zcode",
                "native_record_id": "runtime-detection",
                "install_path": "/home/.zcode",
                "provenance": {"source_kind": "filesystem", "source_id": ".zcode", "collection": "success"},
            }
        )
        payload = build_inventory(Path("/home/test"), [evidence])
        self.assertEqual([], payload["packages"])
        self.assertEqual("zcode", payload["views"]["runtime"][0]["runtime"])
        self.assertEqual(["unmanaged"], payload["views"]["runtime"][0]["states"])

    def test_unresolved_npx_record_remains_one_capability_with_multiple_exposures(self):
        evidence = normalize_runtime_fact(
            {
                "fact_type": "npx-skill",
                "runtime": "npx-skills",
                "native_record_id": "global:demo",
                "scope": "global",
                "package_name": "demo",
                "skill_path": "unknown",
                "managed": True,
                "runtimes": ["codex", "claude-code"],
                "provenance": {"source_kind": "fixture", "source_id": "global-lock", "collection": "success"},
            }
        )
        payload = build_inventory(Path("/home/test"), [evidence])
        self.assertEqual(1, len(payload["capabilities"]))
        self.assertEqual(2, len(payload["capabilities"][0]["exposures"]))
        self.assertEqual("unresolved", payload["capabilities"][0]["identity"]["status"])


if __name__ == "__main__":
    unittest.main()
