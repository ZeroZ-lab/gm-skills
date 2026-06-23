"""Codex Plugin and built-in evidence adapter."""

from __future__ import annotations

import shutil
from pathlib import Path

from adapters.common import UNKNOWN, discover_skills, load_json, run

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None


def collect_codex_evidence(
    home: Path,
    warnings: list[str],
    *,
    use_native_commands: bool = True,
    native_payload: dict | None = None,
) -> list[dict]:
    config = load_config(home / ".codex" / "config.toml", warnings)
    evidence = []
    payload = native_payload
    executable = shutil.which("codex")
    native_allowed = use_native_commands and home == Path.home().resolve()
    if payload is None and executable and native_allowed:
        result = run([executable, "plugin", "list", "--json"])
        if result and result.returncode == 0:
            try:
                import json

                payload = json.loads(result.stdout)
            except ValueError:
                warnings.append("Codex plugin list returned invalid JSON.")
        else:
            warnings.append("Codex plugin list failed; using config fallback.")
    if isinstance(payload, dict):
        evidence.extend(from_native(payload, config, executable is not None))
    else:
        evidence.extend(from_config(config, executable is not None))
    evidence.extend(builtins(home, executable is not None))
    return evidence


def load_config(path: Path, warnings: list[str]) -> dict:
    if not path.is_file() or tomllib is None:
        return {}
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        warnings.append("Could not parse Codex config.toml.")
        return {}


def from_native(payload: dict, config: dict, installer_available: bool) -> list[dict]:
    rows = []
    marketplaces = config.get("marketplaces", {})
    for item in payload.get("installed", []):
        marketplace_name = item.get("marketplaceName") or UNKNOWN
        marketplace = marketplaces.get(marketplace_name, {})
        source_info = item.get("marketplaceSource") or {}
        source_type = source_info.get("sourceType") or marketplace.get("source_type") or UNKNOWN
        remote = source_info.get("source") or marketplace.get("source") or UNKNOWN
        install_path = (item.get("source") or {}).get("path")
        plugin_root = Path(install_path) if install_path else None
        package_path = relative_package_path(plugin_root, remote) if plugin_root else UNKNOWN
        development_local = source_type == "local"
        capabilities = discover_skills(plugin_root, package_path) if plugin_root else []
        rows.append(
            evidence_row(
                runtime="codex",
                package_format="codex-plugin",
                channel="codex-plugin",
                scope="user",
                installation_state="installed" if plugin_root and plugin_root.exists() else "broken",
                exposure_state="unknown" if item.get("enabled", False) else "inactive",
                installer_available=installer_available,
                remote_source=remote if not development_local else UNKNOWN,
                package_path=package_path,
                package_name=item.get("name") or UNKNOWN,
                revision=marketplace.get("last_revision") or item.get("version") or UNKNOWN,
                install_path=str(plugin_root) if plugin_root else UNKNOWN,
                development_local=development_local,
                capabilities=capabilities or unresolved_capability(item.get("name")),
                registry="verified",
                discovery="unknown",
                notes=[] if capabilities else ["capability-set-unresolved"],
            )
        )
    return rows


def from_config(config: dict, installer_available: bool) -> list[dict]:
    rows = []
    marketplaces = config.get("marketplaces", {})
    for selector, settings in sorted(config.get("plugins", {}).items()):
        name, _, marketplace_name = selector.partition("@")
        marketplace = marketplaces.get(marketplace_name, {})
        source_type = marketplace.get("source_type", UNKNOWN)
        remote = marketplace.get("source", UNKNOWN)
        development_local = source_type == "local"
        rows.append(
            evidence_row(
                runtime="codex",
                package_format="codex-plugin",
                channel="codex-plugin",
                scope="user",
                installation_state="installed",
                exposure_state="unknown" if settings.get("enabled", True) else "inactive",
                installer_available=installer_available,
                remote_source=remote if not development_local else UNKNOWN,
                package_path=f"plugins/{name}" if not development_local else UNKNOWN,
                package_name=name,
                revision=marketplace.get("last_revision", UNKNOWN),
                install_path=UNKNOWN,
                development_local=development_local,
                capabilities=unresolved_capability(name),
                registry="verified",
                discovery="unknown",
                notes=["config-fallback"],
            )
        )
    return rows


def builtins(home: Path, installer_available: bool) -> list[dict]:
    root = home / ".codex" / "skills" / ".system"
    rows = []
    if not root.is_dir():
        return rows
    version = UNKNOWN
    executable = shutil.which("codex")
    if executable and home == Path.home().resolve():
        result = run([executable, "--version"])
        if result and result.returncode == 0:
            version = result.stdout.strip()
    for child in sorted(root.iterdir()):
        skill_md = child / "SKILL.md"
        if not skill_md.is_file():
            continue
        capabilities = discover_skills(child, f".system/{child.name}")
        capability = capabilities[0] if capabilities else None
        rows.append(
            evidence_row(
                runtime="codex",
                package_format="built-in",
                channel="built-in",
                scope="system",
                installation_state="installed",
                exposure_state="unknown",
                installer_available=installer_available,
                remote_source=UNKNOWN,
                package_path=UNKNOWN,
                package_name="codex-built-ins",
                revision=version,
                install_path=str(child),
                development_local=False,
                capabilities=[capability] if capability else unresolved_capability(child.name),
                registry="verified",
                discovery="unknown",
                notes=[],
            )
        )
    return rows


def relative_package_path(plugin_root: Path, marketplace_source: str) -> str:
    try:
        source_path = Path(marketplace_source)
        return plugin_root.resolve().relative_to(source_path.resolve()).as_posix()
    except (ValueError, OSError):
        parts = plugin_root.parts
        if "plugins" in parts:
            index = len(parts) - 1 - list(reversed(parts)).index("plugins")
            return Path(*parts[index:]).as_posix()
        return UNKNOWN


def unresolved_capability(name: str | None) -> list[dict]:
    return [{"name": name or UNKNOWN, "skill_path": UNKNOWN, "aliases": []}]


def evidence_row(**values) -> dict:
    return {
        "runtime": values["runtime"],
        "package_format": values["package_format"],
        "installation_channel": values["channel"],
        "scope": values["scope"],
        "installation_state": values["installation_state"],
        "exposure_state": values["exposure_state"],
        "installer_available": values["installer_available"],
        "installer_compatible": True if values["installer_available"] else UNKNOWN,
        "remote_source": values["remote_source"],
        "package_path": values["package_path"],
        "package_name": values["package_name"],
        "revision": values["revision"],
        "install_path": values["install_path"],
        "project_path": UNKNOWN,
        "development_local": values["development_local"],
        "capabilities": values["capabilities"],
        "verification": {"registry": values["registry"], "discovery": values["discovery"]},
        "aliases": [],
        "notes": values["notes"],
        "identity_gap": "missing-remote-or-skill-path",
    }
