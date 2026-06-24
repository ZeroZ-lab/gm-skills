"""Derived views and share-safe redaction for Unified Inventory."""

from __future__ import annotations

import copy
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


def build_views(payload: dict) -> dict[str, list[dict]]:
    capability_view = [
        {
            "capability_id": item["capability_id"],
            "name": item["name"],
            "identity_status": item["identity"]["status"],
            "remote_source": item["identity"]["remote_source"],
            "skill_path": item["identity"]["skill_path"],
            "revision_relation": item["revision_relation"],
            "exposure_count": len(item["exposures"]),
            "runtimes": sorted({row["runtime"] for row in item["exposures"]}),
        }
        for item in payload["capabilities"]
    ]
    package_view = [
        {
            "package_id": item["package_id"],
            "name": item["name"],
            "identity_status": item["identity"]["status"],
            "formats": sorted(item["formats"]),
            "capability_count": len(item["capability_ids"]),
        }
        for item in payload["packages"]
    ]
    runtime_rows = {}
    installation_ids_by_runtime = {}
    for evidence in payload["evidence"]:
        if evidence["subject"] == "runtime-detection":
            runtime_rows.setdefault(
                evidence["runtime"],
                {"runtime": evidence["runtime"], "installation_count": 0, "capability_ids": set(), "states": set()},
            )["states"].add("unmanaged")
    for installation in payload["installations"]:
        for runtime in installation.get("target_runtimes") or [installation["runtime"]]:
            row = runtime_rows.setdefault(
                runtime,
                {"runtime": runtime, "installation_count": 0, "capability_ids": set(), "states": set()},
            )
            installation_ids_by_runtime.setdefault(runtime, set()).add(installation["installation_id"])
            if not installation["capability_ids"]:
                row["states"].add(installation["exposure_state"])
    for capability in payload["capabilities"]:
        for exposure in capability["exposures"]:
            row = runtime_rows.setdefault(
                exposure["runtime"],
                {"runtime": exposure["runtime"], "installation_count": 0, "capability_ids": set(), "states": set()},
            )
            row["capability_ids"].add(capability["capability_id"])
            row["states"].add(exposure["state"])
            installation_ids_by_runtime.setdefault(exposure["runtime"], set()).add(exposure["installation_id"])
    runtime_view = [
        {
            "runtime": row["runtime"],
            "installation_count": len(installation_ids_by_runtime.get(row["runtime"], set())),
            "capability_count": len(row["capability_ids"]),
            "states": sorted(row["states"]),
        }
        for row in runtime_rows.values()
    ]
    return {
        "capability": sorted(capability_view, key=lambda row: (row["name"], row["capability_id"])),
        "package": sorted(package_view, key=lambda row: (row["name"], row["package_id"])),
        "runtime": sorted(runtime_view, key=lambda row: row["runtime"]),
    }


def redact_inventory(payload: dict, home: Path) -> dict:
    result = copy.deepcopy(payload)
    home_text = str(home)

    def redact(value, key=None):
        if isinstance(value, dict):
            return {child_key: redact(item, child_key) for child_key, item in value.items()}
        if isinstance(value, list):
            return [redact(item, key) for item in value]
        if not isinstance(value, str):
            return value
        if key in {
            "path",
            "install_path",
            "install",
            "project_path",
            "project",
            "generated_from",
            "installation_key",
        } and value not in {
            "",
            "unknown",
        }:
            return "[redacted-path]"
        text = value.replace(home_text, "~")
        if "://" in text or text.startswith("git@"):
            text = redact_url(text)
        text = re.sub(r"(?i)(token|password|secret|credential)=([^&\s]+)", r"\1=[redacted]", text)
        return text

    return redact(result)


def redact_url(value: str) -> str:
    if value.startswith("git@"):
        return value
    parts = urlsplit(value)
    hostname = parts.hostname or ""
    port = f":{parts.port}" if parts.port else ""
    return urlunsplit((parts.scheme, hostname + port, parts.path, "", ""))
