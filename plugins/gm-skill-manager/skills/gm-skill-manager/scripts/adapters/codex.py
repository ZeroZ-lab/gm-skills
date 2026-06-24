"""Codex Runtime Facts adapter."""

from __future__ import annotations

import shutil
from pathlib import Path

from adapters.common import InventoryContext, UNKNOWN, adapter_result, discover_skills, run

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None


def collect(context: InventoryContext) -> dict:
    findings = []
    config = load_config(context.home / ".codex" / "config.toml", findings)
    facts = []
    payload = context.fixtures.get("codex")
    executable = shutil.which("codex")
    native_allowed = context.use_native_commands and context.home == Path.home().resolve()
    if payload is None and executable and native_allowed:
        result = run([executable, "plugin", "list", "--json"])
        if result and result.returncode == 0:
            try:
                import json

                payload = json.loads(result.stdout)
            except ValueError:
                findings.append({"runtime": "codex", "code": "invalid-native-json", "source": "plugin-list"})
        else:
            findings.append({"runtime": "codex", "code": "native-command-failed", "source": "plugin-list"})
    if isinstance(payload, dict):
        native_facts, native_findings = from_native(payload, config, executable is not None)
        facts.extend(native_facts)
        findings.extend(native_findings)
    else:
        config_facts, config_findings = from_config(config, executable is not None)
        facts.extend(config_facts)
        findings.extend(config_findings)
    facts.extend(builtins(context.home, executable is not None))
    return adapter_result(facts, findings)


def load_config(path: Path, findings: list[dict]) -> dict:
    if not path.is_file() or tomllib is None:
        return {}
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        findings.append({"runtime": "codex", "code": "registry-parse-failed", "source": "config"})
        return {}


def from_native(payload: dict, config: dict, installer_available: bool) -> tuple[list[dict], list[dict]]:
    rows = []
    findings = []
    marketplaces = config.get("marketplaces", {})
    for item in payload.get("installed", []):
        if not isinstance(item, dict) or not (item.get("pluginId") or item.get("name")):
            findings.append({"runtime": "codex", "code": "unlocatable-native-record", "source": "plugin-list"})
            continue
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
        name = item.get("name") or UNKNOWN
        rows.append(
            {
                "fact_type": "codex-plugin",
                "runtime": "codex",
                "native_record_id": item.get("pluginId") or f"{name}@{marketplace_name}",
                "scope": "user",
                "enabled": item.get("enabled"),
                "installer_available": installer_available,
                "installer_compatible": True if installer_available else UNKNOWN,
                "remote_source": remote if not development_local else UNKNOWN,
                "package_path": package_path,
                "package_name": name,
                "revision": marketplace.get("last_revision") or item.get("version") or UNKNOWN,
                "install_path": str(plugin_root) if plugin_root else UNKNOWN,
                "install_exists": bool(plugin_root and plugin_root.exists()),
                "development_local": development_local,
                "capabilities": capabilities,
                "notes": [] if capabilities else ["capability-set-unresolved"],
                "provenance": {
                    "source_kind": "native-command",
                    "source_id": f"plugin:{name}@{marketplace_name}",
                    "collection": "success",
                },
            }
        )
    return rows, findings


def from_config(config: dict, installer_available: bool) -> tuple[list[dict], list[dict]]:
    rows = []
    findings = []
    marketplaces = config.get("marketplaces", {})
    for selector, settings in sorted(config.get("plugins", {}).items()):
        if not isinstance(settings, dict):
            rows.append(
                {
                    "fact_type": "codex-plugin",
                    "runtime": "codex",
                    "native_record_id": selector,
                    "scope": "user",
                    "malformed": True,
                    "provenance": {
                        "source_kind": "registry",
                        "source_id": f"config-plugin:{selector}",
                        "collection": "success",
                    },
                }
            )
            continue
        name, _, marketplace_name = selector.partition("@")
        marketplace = marketplaces.get(marketplace_name, {})
        source_type = marketplace.get("source_type", UNKNOWN)
        remote = marketplace.get("source", UNKNOWN)
        development_local = source_type == "local"
        rows.append(
            {
                "fact_type": "codex-plugin",
                "runtime": "codex",
                "native_record_id": selector,
                "scope": "user",
                "enabled": settings.get("enabled", True),
                "installer_available": installer_available,
                "installer_compatible": True if installer_available else UNKNOWN,
                "remote_source": remote if not development_local else UNKNOWN,
                "package_path": f"plugins/{name}" if not development_local else UNKNOWN,
                "package_name": name,
                "revision": marketplace.get("last_revision", UNKNOWN),
                "install_path": UNKNOWN,
                "install_exists": True,
                "development_local": development_local,
                "capabilities": [],
                "notes": ["config-fallback"],
                "provenance": {
                    "source_kind": "registry",
                    "source_id": f"config-plugin:{selector}",
                    "collection": "success",
                },
            }
        )
    return rows, findings


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
            {
                "fact_type": "codex-built-in",
                "runtime": "codex",
                "native_record_id": f"built-in:{child.name}",
                "scope": "system",
                "installer_available": installer_available,
                "installer_compatible": True if installer_available else UNKNOWN,
                "revision": version,
                "install_path": str(child),
                "capabilities": [capability] if capability else [],
                "provenance": {
                    "source_kind": "filesystem",
                    "source_id": f"built-in:{child.name}",
                    "collection": "success",
                },
            }
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
