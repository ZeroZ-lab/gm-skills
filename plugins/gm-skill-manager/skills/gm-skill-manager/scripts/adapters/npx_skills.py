"""npx skills Runtime Facts adapter."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from adapters.common import InventoryContext, UNKNOWN, adapter_result, load_json, run

AGENT_RUNTIME_NAMES = {
    "Codex": "codex",
    "Claude Code": "claude-code",
}


def collect(context: InventoryContext) -> dict:
    findings = []
    facts = collect_scope(
        context.home / ".agents" / ".skill-lock.json",
        "global",
        UNKNOWN,
        findings,
        use_native_commands=context.use_native_commands,
        list_payload=context.fixtures.get("npx-global"),
        command_cwd=None,
    )
    if context.project is not None:
        project = context.project.expanduser().resolve()
        facts.extend(
            collect_scope(
                project / "skills-lock.json",
                "project",
                str(project),
                findings,
                use_native_commands=context.use_native_commands,
                list_payload=context.fixtures.get("npx-project"),
                command_cwd=project,
            )
        )
    return adapter_result(facts, findings)


def collect_scope(
    lock_path: Path,
    scope: str,
    project_path: str,
    findings: list[dict],
    *,
    use_native_commands: bool,
    list_payload: list[dict] | None,
    command_cwd: Path | None,
) -> list[dict]:
    lock = load_json(lock_path)
    lock_skills = lock.get("skills", {}) if isinstance(lock, dict) else {}
    executable = shutil.which("npx")
    listed = list_payload or []
    native_allowed = scope == "project" or lock_path == Path.home().resolve() / ".agents" / ".skill-lock.json"
    if list_payload is None and executable and use_native_commands and native_allowed:
        command = [executable, "skills", "list"]
        if scope == "global":
            command.append("-g")
        command.append("--json")
        result = run(command, timeout=30, cwd=command_cwd)
        if result and result.returncode == 0:
            try:
                listed = json.loads(result.stdout)
            except ValueError:
                findings.append({"runtime": "npx-skills", "code": "invalid-native-json", "source": f"{scope}-list"})
        else:
            findings.append({"runtime": "npx-skills", "code": "native-command-failed", "source": f"{scope}-list"})
    elif list_payload is None and use_native_commands and not executable:
        findings.append({"runtime": "npx-skills", "code": "installer-unavailable", "source": f"{scope}-list"})
    listed_by_name = {item.get("name"): item for item in listed if isinstance(item, dict)}
    rows = []
    for name, record in sorted(lock_skills.items()):
        if not isinstance(record, dict):
            rows.append(
                {
                    "fact_type": "npx-skill",
                    "runtime": "npx-skills",
                    "native_record_id": f"{scope}:{name}",
                    "scope": scope,
                    "malformed": True,
                    "provenance": {
                        "source_kind": "lock",
                        "source_id": f"{scope}-skill:{name}",
                        "collection": "success",
                    },
                }
            )
            continue
        remote, skill_path, revision = remote_fields(record)
        listing = listed_by_name.pop(name, None)
        runtimes = listed_runtimes(listing)
        installed_path = (listing or {}).get("path") or record.get("canonicalPath") or UNKNOWN
        rows.append(
            fact_row(
                name=name,
                runtimes=runtimes,
                remote=remote,
                skill_path=skill_path,
                revision=revision,
                install_path=installed_path,
                installer_available=executable is not None,
                managed=True,
                scope=scope,
                project_path=project_path,
                native_record_id=f"{scope}:{name}",
            )
        )
    for name, listing in sorted(listed_by_name.items()):
        rows.append(
            fact_row(
                name=name,
                runtimes=listed_runtimes(listing),
                remote=UNKNOWN,
                skill_path=UNKNOWN,
                revision=UNKNOWN,
                install_path=listing.get("path") or UNKNOWN,
                installer_available=executable is not None,
                managed=False,
                scope=scope,
                project_path=project_path,
                native_record_id=f"unmanaged:{scope}:{listing.get('path') or name}",
            )
        )
    return rows


def remote_fields(record: dict) -> tuple[str, str, str]:
    if record.get("sourceType") == "github":
        return (
            record.get("sourceUrl") or record.get("source") or UNKNOWN,
            record.get("skillPath") or UNKNOWN,
            record.get("treeSha")
            or record.get("skillFolderHash")
            or record.get("computedHash")
            or record.get("version")
            or UNKNOWN,
        )
    source = record.get("source")
    if isinstance(source, dict) and source.get("type") in {"github", "git"}:
        return (
            source.get("url") or UNKNOWN,
            source.get("subpath") or record.get("skillPath") or UNKNOWN,
            source.get("ref")
            or record.get("treeSha")
            or record.get("contentHash")
            or record.get("computedHash")
            or UNKNOWN,
        )
    return UNKNOWN, UNKNOWN, record.get("contentHash") or record.get("computedHash") or UNKNOWN


def listed_runtimes(listing: dict | None) -> list[str]:
    if not listing:
        return []
    return sorted({AGENT_RUNTIME_NAMES[name] for name in listing.get("agents", []) if name in AGENT_RUNTIME_NAMES})


def fact_row(
    *,
    name: str,
    runtimes: list[str],
    remote: str,
    skill_path: str,
    revision: str,
    install_path: str,
    installer_available: bool,
    managed: bool,
    scope: str,
    project_path: str,
    native_record_id: str,
) -> dict:
    return {
        "fact_type": "npx-skill",
        "runtime": "npx-skills",
        "native_record_id": native_record_id,
        "scope": scope,
        "installer_available": installer_available,
        "installer_compatible": True if installer_available else UNKNOWN,
        "remote_source": remote,
        "package_name": name,
        "skill_path": skill_path,
        "revision": revision,
        "install_path": install_path,
        "project_path": project_path,
        "managed": managed,
        "runtimes": runtimes,
        "provenance": {
            "source_kind": "lock" if managed else "native-command",
            "source_id": f"{scope}-skill:{name}",
            "collection": "success",
        },
    }
