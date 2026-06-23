"""npx skills evidence adapter: lock proves Installation, list proves Exposure."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from adapters.common import UNKNOWN, load_json, run

AGENT_RUNTIME_NAMES = {
    "Codex": "codex",
    "Claude Code": "claude-code",
}


def collect_npx_evidence(
    home: Path,
    warnings: list[str],
    *,
    project: Path | None = None,
    use_native_commands: bool = True,
    list_payload: list[dict] | None = None,
    project_list_payload: list[dict] | None = None,
) -> list[dict]:
    rows = collect_scope(
        home / ".agents" / ".skill-lock.json",
        "global",
        UNKNOWN,
        warnings,
        use_native_commands=use_native_commands,
        list_payload=list_payload,
        command_cwd=None,
    )
    if project is not None:
        project = project.expanduser().resolve()
        rows.extend(
            collect_scope(
                project / "skills-lock.json",
                "project",
                str(project),
                warnings,
                use_native_commands=use_native_commands,
                list_payload=project_list_payload,
                command_cwd=project,
            )
        )
    return rows


def collect_scope(
    lock_path: Path,
    scope: str,
    project_path: str,
    warnings: list[str],
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
                warnings.append(f"npx skills {scope} list returned invalid JSON.")
        else:
            warnings.append(f"npx skills {scope} list failed; exposures may be unknown.")
    listed_by_name = {item.get("name"): item for item in listed if isinstance(item, dict)}
    rows = []
    for name, record in sorted(lock_skills.items()):
        if not isinstance(record, dict):
            continue
        remote, skill_path, revision = remote_fields(record)
        listing = listed_by_name.pop(name, None)
        runtimes = listed_runtimes(listing)
        if not runtimes:
            runtimes = [UNKNOWN]
        for runtime in runtimes:
            installed_path = (listing or {}).get("path") or record.get("canonicalPath") or UNKNOWN
            rows.append(
                evidence_row(
                    name=name,
                    runtime=runtime,
                    remote=remote,
                    skill_path=skill_path,
                    revision=revision,
                    install_path=installed_path,
                    installation_state="installed",
                    exposure_state="active" if runtime != UNKNOWN else "inactive",
                    installer_available=executable is not None,
                    managed=True,
                    scope=scope,
                    project_path=project_path,
                    installation_key=f"{scope}:{lock_path}:{name}",
                )
            )
    for name, listing in sorted(listed_by_name.items()):
        for runtime in listed_runtimes(listing) or [UNKNOWN]:
            rows.append(
                evidence_row(
                    name=name,
                    runtime=runtime,
                    remote=UNKNOWN,
                    skill_path=UNKNOWN,
                    revision=UNKNOWN,
                    install_path=listing.get("path") or UNKNOWN,
                    installation_state="broken",
                    exposure_state="active" if runtime != UNKNOWN else "unknown",
                    installer_available=executable is not None,
                    managed=False,
                    scope=scope,
                    project_path=project_path,
                    installation_key=f"unmanaged:{scope}:{listing.get('path') or name}",
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


def evidence_row(
    *,
    name: str,
    runtime: str,
    remote: str,
    skill_path: str,
    revision: str,
    install_path: str,
    installation_state: str,
    exposure_state: str,
    installer_available: bool,
    managed: bool,
    scope: str,
    project_path: str,
    installation_key: str,
) -> dict:
    package_path = str(Path(skill_path).parent) if skill_path != UNKNOWN else UNKNOWN
    return {
        "runtime": runtime,
        "package_format": "npx-skills",
        "installation_channel": "npx-skills",
        "scope": scope,
        "installation_state": installation_state,
        "exposure_state": exposure_state,
        "installer_available": installer_available,
        "installer_compatible": True if installer_available else UNKNOWN,
        "remote_source": remote,
        "package_path": package_path,
        "package_name": name,
        "revision": revision,
        "install_path": install_path,
        "project_path": project_path,
        "development_local": False,
        "capabilities": [{"name": name, "skill_path": skill_path, "aliases": []}],
        "verification": {
            "registry": "verified" if managed else "missing",
            "discovery": "verified" if exposure_state == "active" else "unknown",
        },
        "aliases": [],
        "notes": [] if managed else ["unmanaged-exposure"],
        "identity_gap": "npx-lock-missing-remote-evidence",
        "installation_key": installation_key,
    }
