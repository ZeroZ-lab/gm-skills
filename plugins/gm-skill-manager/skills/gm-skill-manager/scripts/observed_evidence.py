"""Normalize Runtime Facts into the versioned Observed Evidence contract.

Decisions: ADR-0003, ADR-0015, ADR-0019.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

UNKNOWN = "unknown"

REQUIRED_FIELDS = {
    "subject": UNKNOWN,
    "validity": "invalid",
    "runtime": UNKNOWN,
    "package_format": UNKNOWN,
    "installation_channel": UNKNOWN,
    "scope": UNKNOWN,
    "installation_state": UNKNOWN,
    "installer_available": UNKNOWN,
    "installer_compatible": UNKNOWN,
    "remote_source": UNKNOWN,
    "package_path": UNKNOWN,
    "package_name": UNKNOWN,
    "revision": UNKNOWN,
    "install_path": UNKNOWN,
    "project_path": UNKNOWN,
    "development_local": False,
    "capabilities": [],
    "exposure_facts": [],
    "verification": {"registry": UNKNOWN, "discovery": UNKNOWN},
    "aliases": [],
    "notes": [],
    "findings": [],
    "provenance": {
        "source_kind": UNKNOWN,
        "source_id": UNKNOWN,
        "collection": UNKNOWN,
    },
}


def stable_id(prefix: str, *parts: Any) -> str:
    raw = "\0".join(str(part) for part in parts)
    return f"{prefix}-{hashlib.sha256(raw.encode()).hexdigest()[:16]}"


def normalize_runtime_facts(facts: list[dict]) -> list[dict]:
    return [normalize_runtime_fact(fact) for fact in facts]


def normalize_runtime_fact(fact: dict) -> dict:
    if fact.get("malformed"):
        return _invalid(fact, "malformed-native-record")
    fact_type = fact.get("fact_type")
    interpreters = {
        "codex-plugin": _codex_plugin,
        "codex-built-in": _codex_builtin,
        "claude-plugin": _claude_plugin,
        "npx-skill": _npx_skill,
        "zcode-detection": _zcode_detection,
    }
    interpreter = interpreters.get(fact_type)
    if interpreter is None:
        return _invalid(fact, "unsupported-native-record-variant")
    try:
        item = interpreter(fact)
    except (KeyError, TypeError, ValueError):
        return _invalid(fact, "malformed-native-record")
    return _finalize(item, fact)


def _base(fact: dict, *, subject: str, package_format: str, channel: str) -> dict:
    runtime = fact.get("runtime") or UNKNOWN
    scope = fact.get("scope") or UNKNOWN
    return {
        **REQUIRED_FIELDS,
        "subject": subject,
        "validity": "valid",
        "runtime": runtime,
        "package_format": package_format,
        "installation_channel": channel,
        "scope": scope,
        "installer_available": fact.get("installer_available", UNKNOWN),
        "installer_compatible": fact.get("installer_compatible", UNKNOWN),
        "provenance": _provenance(fact),
    }


def _codex_plugin(fact: dict) -> dict:
    item = _base(fact, subject="installation", package_format="codex-plugin", channel="codex-plugin")
    enabled = fact.get("enabled")
    item.update(
        {
            "installation_state": "installed" if fact.get("install_exists") else "broken",
            "remote_source": fact.get("remote_source") or UNKNOWN,
            "package_path": fact.get("package_path") or UNKNOWN,
            "package_name": fact.get("package_name") or UNKNOWN,
            "revision": fact.get("revision") or UNKNOWN,
            "install_path": fact.get("install_path") or UNKNOWN,
            "development_local": bool(fact.get("development_local", False)),
            "capabilities": _capabilities(fact),
            "exposure_facts": [
                {
                    "runtime": "codex",
                    "scope": fact.get("scope") or "user",
                    "project_path": UNKNOWN,
                    "state": "inactive" if enabled is False else UNKNOWN,
                }
            ],
            "verification": {"registry": "verified", "discovery": UNKNOWN},
            "aliases": fact.get("aliases") or [],
            "notes": fact.get("notes") or [],
        }
    )
    return item


def _codex_builtin(fact: dict) -> dict:
    item = _base(fact, subject="installation", package_format="built-in", channel="built-in")
    item.update(
        {
            "installation_state": "installed",
            "package_name": "codex-built-ins",
            "revision": fact.get("revision") or UNKNOWN,
            "install_path": fact.get("install_path") or UNKNOWN,
            "capabilities": _capabilities(fact),
            "exposure_facts": [
                {"runtime": "codex", "scope": "system", "project_path": UNKNOWN, "state": UNKNOWN}
            ],
            "verification": {"registry": "verified", "discovery": UNKNOWN},
        }
    )
    return item


def _claude_plugin(fact: dict) -> dict:
    item = _base(fact, subject="installation", package_format="claude-code-plugin", channel="claude-code-plugin")
    item.update(
        {
            "installation_state": "installed" if fact.get("install_exists") else "broken",
            "remote_source": fact.get("remote_source") or UNKNOWN,
            "package_path": fact.get("package_path") or UNKNOWN,
            "package_name": fact.get("package_name") or UNKNOWN,
            "revision": fact.get("revision") or UNKNOWN,
            "install_path": fact.get("install_path") or UNKNOWN,
            "project_path": fact.get("project_path") or UNKNOWN,
            "development_local": bool(fact.get("development_local", False)),
            "capabilities": _capabilities(fact),
            "exposure_facts": [
                {
                    "runtime": "claude-code",
                    "scope": fact.get("scope") or UNKNOWN,
                    "project_path": fact.get("project_path") or UNKNOWN,
                    "state": UNKNOWN,
                }
            ],
            "verification": {"registry": "verified", "discovery": UNKNOWN},
            "aliases": fact.get("aliases") or [],
            "notes": fact.get("notes") or [],
        }
    )
    return item


def _npx_skill(fact: dict) -> dict:
    item = _base(fact, subject="installation", package_format="npx-skills", channel="npx-skills")
    managed = bool(fact.get("managed"))
    skill_path = fact.get("skill_path") or UNKNOWN
    runtimes = fact.get("runtimes") or []
    state = "active" if managed else "unknown"
    exposure_facts = [
        {
            "runtime": runtime,
            "scope": fact.get("scope") or UNKNOWN,
            "project_path": fact.get("project_path") or UNKNOWN,
            "state": state,
        }
        for runtime in runtimes
    ]
    if not exposure_facts:
        exposure_facts = [
            {
                "runtime": UNKNOWN,
                "scope": fact.get("scope") or UNKNOWN,
                "project_path": fact.get("project_path") or UNKNOWN,
                "state": "inactive" if managed else UNKNOWN,
            }
        ]
    item.update(
        {
            "installation_state": "installed" if managed else "broken",
            "remote_source": fact.get("remote_source") or UNKNOWN,
            "package_path": str(Path(skill_path).parent) if skill_path != UNKNOWN else UNKNOWN,
            "package_name": fact.get("package_name") or UNKNOWN,
            "revision": fact.get("revision") or UNKNOWN,
            "install_path": fact.get("install_path") or UNKNOWN,
            "project_path": fact.get("project_path") or UNKNOWN,
            "capabilities": [
                {
                    "name": fact.get("package_name") or UNKNOWN,
                    "skill_path": skill_path,
                    "aliases": [],
                }
            ],
            "exposure_facts": exposure_facts,
            "verification": {
                "registry": "verified" if managed else "missing",
                "discovery": "verified" if runtimes else UNKNOWN,
            },
            "notes": [] if managed else ["unmanaged-exposure"],
        }
    )
    return item


def _zcode_detection(fact: dict) -> dict:
    item = _base(fact, subject="runtime-detection", package_format=UNKNOWN, channel=UNKNOWN)
    item.update(
        {
            "runtime": "zcode",
            "installation_state": UNKNOWN,
            "install_path": fact.get("install_path") or UNKNOWN,
            "notes": ["unmanaged-runtime"],
        }
    )
    return item


def _invalid(fact: dict, code: str) -> dict:
    item = {
        **REQUIRED_FIELDS,
        "subject": fact.get("subject") or "installation",
        "validity": "invalid",
        "runtime": fact.get("runtime") or UNKNOWN,
        "scope": fact.get("scope") or UNKNOWN,
        "provenance": _provenance(fact),
        "findings": [{"code": code}],
    }
    return _finalize(item, fact)


def _finalize(item: dict, fact: dict) -> dict:
    normalized = dict(REQUIRED_FIELDS)
    normalized.update(item)
    normalized["verification"] = {
        **REQUIRED_FIELDS["verification"],
        **(item.get("verification") or {}),
    }
    normalized["provenance"] = {
        **REQUIRED_FIELDS["provenance"],
        **(item.get("provenance") or {}),
    }
    normalized["capabilities"] = _normalize_capabilities(normalized.get("capabilities") or [])
    normalized["exposure_facts"] = [
        {
            "runtime": row.get("runtime") or UNKNOWN,
            "scope": row.get("scope") or UNKNOWN,
            "project_path": row.get("project_path") or UNKNOWN,
            "state": row.get("state") or UNKNOWN,
        }
        for row in normalized.get("exposure_facts") or []
    ]
    native_record_id = fact.get("native_record_id")
    if not native_record_id:
        normalized["validity"] = "invalid"
        normalized["findings"] = [*normalized["findings"], {"code": "missing-native-record-identity"}]
        native_record_id = UNKNOWN
    normalized["evidence_id"] = stable_id(
        "evidence",
        normalized["runtime"],
        normalized["subject"],
        normalized["provenance"]["source_kind"],
        normalized["provenance"]["source_id"],
        native_record_id,
        normalized["scope"],
    )
    return normalized


def _provenance(fact: dict) -> dict:
    provenance = fact.get("provenance") or {}
    return {
        "source_kind": provenance.get("source_kind") or UNKNOWN,
        "source_id": provenance.get("source_id") or UNKNOWN,
        "collection": provenance.get("collection") or "success",
    }


def _capabilities(fact: dict) -> list[dict]:
    capabilities = fact.get("capabilities") or []
    if capabilities:
        return capabilities
    name = fact.get("package_name") or UNKNOWN
    return [{"name": name, "skill_path": UNKNOWN, "aliases": fact.get("aliases") or []}]


def _normalize_capabilities(capabilities: list[dict]) -> list[dict]:
    return [
        {
            "name": row.get("name") or UNKNOWN,
            "skill_path": row.get("skill_path") or UNKNOWN,
            "aliases": row.get("aliases") or [],
        }
        for row in capabilities
    ]
