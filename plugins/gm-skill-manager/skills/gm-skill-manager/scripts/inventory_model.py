"""Deep module for the versioned Unified Inventory contract."""

from __future__ import annotations

import hashlib
from collections import defaultdict
from pathlib import Path
from typing import Any

from identity import UNKNOWN, resolve_capability, resolve_package, revision_relation

SCHEMA_VERSION = "2.0"


def stable_id(prefix: str, *parts: Any) -> str:
    raw = "\0".join(str(part) for part in parts)
    return f"{prefix}-{hashlib.sha256(raw.encode()).hexdigest()[:16]}"


def build_inventory(
    home: Path,
    evidence: list[dict],
    collection_findings: list[dict] | None = None,
) -> dict:
    collection_findings = collection_findings or []
    packages: dict[str, dict] = {}
    installations: dict[str, dict] = {}
    capability_groups: dict[str, list[dict]] = defaultdict(list)
    unresolved_capabilities: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    runtime_detections: list[dict] = []

    for item in evidence:
        if item["subject"] == "runtime-detection":
            runtime_detections.append(item)
            continue
        if item["validity"] != "valid":
            continue
        package_identity = resolve_package(item)
        package_key = package_identity["key"]
        if package_key == UNKNOWN:
            package_key = stable_id("unresolved-package", item["evidence_id"])
        package_id = stable_id("package", package_key)
        package = packages.setdefault(
            package_id,
            {
                "package_id": package_id,
                "identity": package_identity,
                "name": item["package_name"],
                "formats": [],
                "capability_ids": [],
            },
        )
        if item["package_format"] not in package["formats"]:
            package["formats"].append(item["package_format"])

        installation_id = stable_id(
            "installation",
            item["runtime"],
            item["package_format"],
            item["scope"],
            item["evidence_id"],
        )
        exposure_facts = item.get("exposure_facts") or []
        installation = installations.setdefault(
            installation_id,
            {
                "installation_id": installation_id,
                "package_id": package_id,
                "runtime": item["runtime"],
                "target_runtimes": sorted({row["runtime"] for row in exposure_facts}),
                "package_format": item["package_format"],
                "installation_channel": item["installation_channel"],
                "scope": item["scope"],
                "installation_state": item["installation_state"],
                "exposure_state": _installation_exposure_state(exposure_facts),
                "installer": {
                    "available": item["installer_available"],
                    "compatible": item["installer_compatible"],
                },
                "revision": item["revision"],
                "paths": {
                    "install": item["install_path"],
                    "project": item["project_path"],
                },
                "verification": item["verification"],
                "development_local": item["development_local"],
                "evidence_ids": [],
                "capability_ids": [],
            },
        )
        if item["evidence_id"] not in installation["evidence_ids"]:
            installation["evidence_ids"].append(item["evidence_id"])

        for candidate in item["capabilities"]:
            identity = resolve_capability(item, candidate)
            for exposure_fact in exposure_facts or [
                {
                    "runtime": item["runtime"],
                    "scope": item["scope"],
                    "project_path": item["project_path"],
                    "state": UNKNOWN,
                }
            ]:
                record = {
                    "identity": identity,
                    "candidate": candidate,
                    "installation_id": installation_id,
                    "package_id": package_id,
                    "runtime": exposure_fact["runtime"],
                    "scope": exposure_fact["scope"],
                    "project_path": exposure_fact["project_path"],
                    "revision": item["revision"],
                    "exposure_state": exposure_fact["state"],
                }
                if identity["status"] == "resolved":
                    capability_groups[identity["key"]].append(record)
                else:
                    unresolved_capabilities[
                        (
                            installation_id,
                            candidate["skill_path"],
                            candidate["name"],
                        )
                    ].append(record)

    capabilities: list[dict] = []
    for identity_key, records in sorted(capability_groups.items()):
        capability_id = stable_id("capability", identity_key)
        names = [record["candidate"]["name"] for record in records if record["candidate"]["name"] != UNKNOWN]
        name = names[0] if names else Path(records[0]["identity"]["skill_path"]).parent.name
        exposures = []
        for record in records:
            exposure_id = stable_id(
                "exposure",
                capability_id,
                record["installation_id"],
                record["runtime"],
                record["scope"],
                record["project_path"],
            )
            exposures.append(
                {
                    "exposure_id": exposure_id,
                    "installation_id": record["installation_id"],
                    "runtime": record["runtime"],
                    "scope": record["scope"],
                    "project_path": record["project_path"],
                    "state": record["exposure_state"],
                    "revision": record["revision"],
                }
            )
            _attach_capability(installations, packages, record, capability_id)
        _mark_duplicate_exposures(exposures)
        capabilities.append(
            {
                "capability_id": capability_id,
                "identity": records[0]["identity"],
                "name": name,
                "aliases": sorted(set(names) - {name}),
                "revision_relation": revision_relation([record["revision"] for record in records]),
                "exposures": exposures,
            }
        )

    for unresolved_key, records in sorted(unresolved_capabilities.items()):
        record = records[0]
        capability_id = stable_id("unresolved-capability", *unresolved_key)
        exposures = [
            {
                "exposure_id": stable_id(
                    "exposure",
                    capability_id,
                    row["installation_id"],
                    row["runtime"],
                    row["scope"],
                    row["project_path"],
                ),
                "installation_id": row["installation_id"],
                "runtime": row["runtime"],
                "scope": row["scope"],
                "project_path": row["project_path"],
                "state": row["exposure_state"],
                "revision": row["revision"],
            }
            for row in records
        ]
        _mark_duplicate_exposures(exposures)
        capabilities.append(
            {
                "capability_id": capability_id,
                "identity": record["identity"],
                "name": record["candidate"]["name"],
                "aliases": record["candidate"]["aliases"],
                "revision_relation": "unknown",
                "exposures": exposures,
            }
        )
        for row in records:
            _attach_capability(installations, packages, row, capability_id)

    installation_rows = list(installations.values())
    for installation in installation_rows:
        installation["target_runtimes"].sort()
        installation["evidence_ids"].sort()
        installation["capability_ids"].sort()
    for package in packages.values():
        package["formats"].sort()
        package["capability_ids"].sort()
    findings = derive_findings(capabilities, installation_rows, evidence, runtime_detections)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_from": str(home),
        "capabilities": sorted(capabilities, key=lambda row: (row["name"], row["capability_id"])),
        "packages": sorted(packages.values(), key=lambda row: (row["name"], row["package_id"])),
        "installations": sorted(
            installation_rows,
            key=lambda row: (row["runtime"], row["scope"], row["package_format"], row["installation_id"]),
        ),
        "evidence": sorted(evidence, key=lambda row: row["evidence_id"]),
        "views": {},
        "diagnostics": {
            "facts": {
                "capability_count": len(capabilities),
                "package_count": len(packages),
                "installation_count": len(installations),
            },
            "findings": findings,
            "recommendations": recommendations_for(findings),
            "collection_findings": collection_findings,
        },
    }
    from views import build_views

    payload["views"] = build_views(payload)
    return payload


def _installation_exposure_state(exposure_facts: list[dict]) -> str:
    states = {row["state"] for row in exposure_facts}
    if len(states) == 1:
        return next(iter(states))
    return UNKNOWN


def _attach_capability(
    installations: dict[str, dict], packages: dict[str, dict], record: dict, capability_id: str
) -> None:
    installation = installations[record["installation_id"]]
    if capability_id not in installation["capability_ids"]:
        installation["capability_ids"].append(capability_id)
    package = packages[record["package_id"]]
    if capability_id not in package["capability_ids"]:
        package["capability_ids"].append(capability_id)


def _mark_duplicate_exposures(exposures: list[dict]) -> None:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for exposure in exposures:
        grouped[exposure["runtime"]].append(exposure)
    for rows in grouped.values():
        global_rows = [row for row in rows if row["scope"] in {"user", "global", "system"}]
        scoped_rows: dict[tuple[str, str], list[dict]] = defaultdict(list)
        for row in rows:
            if row not in global_rows:
                scoped_rows[(row["scope"], row["project_path"])].append(row)

        ambiguous_ids = set()
        if len(global_rows) > 1:
            ambiguous_ids.update(row["exposure_id"] for row in global_rows)
        if global_rows and scoped_rows:
            ambiguous_ids.update(row["exposure_id"] for row in rows)
        for scoped_group in scoped_rows.values():
            if len(scoped_group) > 1:
                ambiguous_ids.update(row["exposure_id"] for row in scoped_group)

        for row in rows:
            if row["exposure_id"] in ambiguous_ids:
                row["state"] = "ambiguous"


def derive_findings(
    capabilities: list[dict],
    installations: list[dict],
    evidence: list[dict],
    runtime_detections: list[dict],
) -> list[dict]:
    findings = []
    for item in evidence:
        if item["validity"] == "invalid":
            findings.append({"code": "invalid-evidence", "evidence_id": item["evidence_id"]})
        for finding in item.get("findings") or []:
            findings.append(
                {
                    "code": "evidence-finding",
                    "evidence_id": item["evidence_id"],
                    "detail": finding["code"],
                }
            )
    for item in runtime_detections:
        findings.append(
            {
                "code": "unmanaged-runtime",
                "runtime": item["runtime"],
                "evidence_id": item["evidence_id"],
            }
        )
    for capability in capabilities:
        if capability["identity"]["status"] == "unresolved":
            findings.append({"code": "unresolved-identity", "capability_id": capability["capability_id"]})
        if capability["revision_relation"] == "different":
            findings.append({"code": "revision-drift", "capability_id": capability["capability_id"]})
        if any(exposure["state"] == "ambiguous" for exposure in capability["exposures"]):
            findings.append({"code": "duplicate-exposure", "capability_id": capability["capability_id"]})
    for installation in installations:
        if installation["installation_state"] == "broken":
            findings.append({"code": "broken-installation", "installation_id": installation["installation_id"]})
    return findings


def recommendations_for(findings: list[dict]) -> list[dict]:
    messages = {
        "unresolved-identity": "Provide a Remote Source or reinstall through a Native Installer.",
        "revision-drift": "Compare explicit revisions before requesting Revision Sync.",
        "duplicate-exposure": "Keep the runtime-native Plugin exposure unless the Operator chooses otherwise.",
        "broken-installation": "Run doctor, then authorize a Native Installer repair.",
        "invalid-evidence": "Inspect the native record and repair it through its Native Installer.",
        "evidence-finding": "Inspect the evidence provenance and native record.",
        "unmanaged-runtime": "No Stage 1 mutation adapter is available for this Runtime.",
    }
    return [{"finding": finding["code"], "message": messages[finding["code"]]} for finding in findings]


def render_table(payload: dict, view: str) -> str:
    rows = payload["views"][view]
    if not rows:
        return f"{view}: no records"
    return json_like_table(rows)


def json_like_table(rows: list[dict]) -> str:
    lines = []
    for row in rows:
        label = row.get("name") or row.get("runtime") or row.get("package_id")
        summary = ", ".join(f"{key}={value}" for key, value in row.items() if key not in {"name", "runtime"} and not isinstance(value, (list, dict)))
        lines.append(f"- {label}: {summary}".rstrip(": "))
    return "\n".join(lines)
