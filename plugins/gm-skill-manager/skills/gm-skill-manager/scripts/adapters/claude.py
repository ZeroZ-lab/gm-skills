"""Claude Code Plugin evidence adapter."""

from __future__ import annotations

import shutil
from pathlib import Path

from adapters.common import UNKNOWN, discover_skills, load_json


def collect_claude_evidence(home: Path, warnings: list[str]) -> list[dict]:
    registry_path = home / ".claude" / "plugins" / "installed_plugins.json"
    marketplaces_path = home / ".claude" / "plugins" / "known_marketplaces.json"
    registry = load_json(registry_path)
    marketplaces = load_json(marketplaces_path)
    if registry_path.exists() and not isinstance(registry, dict):
        warnings.append("Could not parse Claude installed_plugins.json.")
    if not isinstance(registry, dict):
        return []
    marketplaces = marketplaces if isinstance(marketplaces, dict) else {}
    installer_available = shutil.which("claude") is not None
    rows = []
    for selector, installs in sorted(registry.get("plugins", {}).items()):
        name, _, marketplace_name = selector.partition("@")
        marketplace = marketplaces.get(marketplace_name, {})
        remote = marketplace_remote(marketplace.get("source"))
        package_path = catalog_package_path(marketplace, name)
        development_local = remote == UNKNOWN
        for install in installs if isinstance(installs, list) else []:
            install_path = install.get("installPath")
            install_root = Path(install_path) if install_path else None
            capabilities = discover_skills(install_root, package_path) if install_root else []
            rows.append(
                {
                    "runtime": "claude-code",
                    "package_format": "claude-code-plugin",
                    "installation_channel": "claude-code-plugin",
                    "scope": install.get("scope") or UNKNOWN,
                    "installation_state": "installed" if install_root and install_root.exists() else "broken",
                    "exposure_state": "unknown",
                    "installer_available": installer_available,
                    "installer_compatible": True if installer_available else UNKNOWN,
                    "remote_source": remote,
                    "package_path": package_path,
                    "package_name": name,
                    "revision": install.get("gitCommitSha") or install.get("version") or UNKNOWN,
                    "install_path": str(install_root) if install_root else UNKNOWN,
                    "project_path": install.get("projectPath") or UNKNOWN,
                    "development_local": development_local,
                    "capabilities": capabilities
                    or [{"name": name, "skill_path": UNKNOWN, "aliases": [selector]}],
                    "verification": {
                        "registry": "verified",
                        "discovery": "unknown",
                    },
                    "aliases": [selector],
                    "notes": [] if capabilities else ["capability-set-unresolved"],
                    "identity_gap": "missing-remote-or-skill-path",
                }
            )
    return rows


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
