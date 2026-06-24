"""Claude Code Runtime Facts adapter."""

from __future__ import annotations

import shutil
from pathlib import Path

from adapters.common import InventoryContext, UNKNOWN, adapter_result, discover_skills, load_json


def collect(context: InventoryContext) -> dict:
    home = context.home
    findings = []
    registry_path = home / ".claude" / "plugins" / "installed_plugins.json"
    marketplaces_path = home / ".claude" / "plugins" / "known_marketplaces.json"
    registry = load_json(registry_path)
    marketplaces = load_json(marketplaces_path)
    if registry_path.exists() and not isinstance(registry, dict):
        findings.append({"runtime": "claude-code", "code": "registry-parse-failed", "source": "installed-plugins"})
    if not isinstance(registry, dict):
        return adapter_result(findings=findings)
    marketplaces = marketplaces if isinstance(marketplaces, dict) else {}
    installer_available = shutil.which("claude") is not None
    rows = []
    for selector, installs in sorted(registry.get("plugins", {}).items()):
        name, _, marketplace_name = selector.partition("@")
        marketplace = marketplaces.get(marketplace_name, {})
        remote = marketplace_remote(marketplace.get("source"))
        package_path = catalog_package_path(marketplace, name)
        development_local = remote == UNKNOWN
        if not isinstance(installs, list):
            findings.append(
                {"runtime": "claude-code", "code": "unsupported-native-record-variant", "source": selector}
            )
            continue
        for install in installs:
            if not isinstance(install, dict):
                findings.append(
                    {"runtime": "claude-code", "code": "unlocatable-native-record", "source": selector}
                )
                continue
            install_path = install.get("installPath")
            install_root = Path(install_path) if install_path else None
            capabilities = discover_skills(install_root, package_path) if install_root else []
            scope = install.get("scope") or UNKNOWN
            rows.append(
                {
                    "fact_type": "claude-plugin",
                    "runtime": "claude-code",
                    "native_record_id": f"{selector}:{scope}:{install.get('projectPath') or ''}",
                    "scope": scope,
                    "installer_available": installer_available,
                    "installer_compatible": True if installer_available else UNKNOWN,
                    "remote_source": remote,
                    "package_path": package_path,
                    "package_name": name,
                    "revision": install.get("gitCommitSha") or install.get("version") or UNKNOWN,
                    "install_path": str(install_root) if install_root else UNKNOWN,
                    "install_exists": bool(install_root and install_root.exists()),
                    "project_path": install.get("projectPath") or UNKNOWN,
                    "development_local": development_local,
                    "capabilities": capabilities,
                    "aliases": [selector],
                    "notes": [] if capabilities else ["capability-set-unresolved"],
                    "provenance": {
                        "source_kind": "registry",
                        "source_id": f"installed-plugin:{selector}:{scope}",
                        "collection": "success",
                    },
                }
            )
    return adapter_result(rows, findings)


def marketplace_remote(value) -> str:
    if not isinstance(value, dict):
        return UNKNOWN
    if value.get("source") == "github" and value.get("repo"):
        return f"https://github.com/{value['repo']}.git"
    if value.get("source") == "git" and value.get("url"):
        return value["url"]
    return UNKNOWN


def catalog_package_path(marketplace: dict, plugin_name: str) -> str:
    root_value = marketplace.get("installLocation")
    if not root_value:
        return UNKNOWN
    root = Path(root_value)
    for candidate in (root / ".claude-plugin" / "marketplace.json", root / "marketplace.json"):
        payload = load_json(candidate)
        if not isinstance(payload, dict):
            continue
        for item in payload.get("plugins", []):
            if item.get("name") == plugin_name and isinstance(item.get("source"), str):
                return item["source"].removeprefix("./").rstrip("/")
    return UNKNOWN
