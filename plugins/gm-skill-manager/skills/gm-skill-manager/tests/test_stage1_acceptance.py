from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).parents[1] / "scripts"
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from doctor import doctor_report
from inventory import inventory
from inventory_model import REQUIRED_EVIDENCE_FIELDS


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(str(path.relative_to(root)).encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


class Stage1AcceptanceTests(unittest.TestCase):
    def test_inventory_and_doctor_are_read_only_and_zcode_is_unmanaged(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            (home / ".zcode").mkdir()
            lock = home / ".agents/.skill-lock.json"
            lock.parent.mkdir(parents=True)
            lock.write_text(json.dumps({"skills": {}}), encoding="utf-8")

            before = tree_hash(home)
            payload = inventory(home, use_native_commands=False)
            report = doctor_report(payload)
            after = tree_hash(home)

            self.assertEqual(before, after)
            self.assertEqual(payload["diagnostics"]["facts"], report["facts"])
            zcode = next(row for row in payload["evidence"] if row["runtime"] == "zcode")
            self.assertEqual("unknown", zcode["installation_state"])
            self.assertIn("unmanaged-runtime", zcode["notes"])
            self.assertTrue(any("unmanaged" in warning for warning in report["warnings"]))

    def test_evidence_contract_has_explicit_required_fields(self):
        with tempfile.TemporaryDirectory() as temp:
            payload = inventory(Path(temp), use_native_commands=False)
            for item in payload["evidence"]:
                self.assertTrue(REQUIRED_EVIDENCE_FIELDS.keys() <= item.keys())

    def test_action_contract_keeps_mutation_with_native_installers(self):
        skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        contract = (SKILL_DIR / "references/action-contract.md").read_text(encoding="utf-8")
        scenarios = (SKILL_DIR / "tests/action-scenarios.md").read_text(encoding="utf-8")
        combined = "\n".join((skill_text, contract, scenarios))

        for action in ("install", "uninstall", "enable", "disable", "repair"):
            self.assertIn(action, combined)
        for installer in ("codex plugin", "claude plugin", "npx skills"):
            self.assertIn(installer, combined)
        self.assertIn("不直接修改", combined)
        self.assertIn("doctor 只读", combined)
        self.assertIn("不自动回滚", combined)


if __name__ == "__main__":
    unittest.main()
