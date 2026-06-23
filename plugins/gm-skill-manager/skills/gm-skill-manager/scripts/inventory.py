#!/usr/bin/env python3
"""Read-only inventory for skills and plugins across local coding runtimes."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.11+ is expected.
    tomllib = None


def run(command: list[str], timeout: int = 8) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def skill_name(skill_md: Path) -> str | None:
    try:
        head = skill_md.read_text(encoding="utf-8")[:4096]
    except OSError:
        return None
    match = re.search(r"(?m)^name:\s*[\"']?([^\"'\n]+)", head)
    return match.group(1).strip() if match else None


def git_source(path: Path) -> dict[str, str] | None:
    result = run(["git", "-C", str(path), "rev-parse", "--show-toplevel"])
    if not result or result.returncode != 0:
        return None
    root = Path(result.stdout.strip()).resolve()
    remote_result = run(["git", "-C", str(root), "config", "--get", "remote.origin.url"])
    remote = remote_result.stdout.strip() if remote_result and remote_result.returncode == 0 else ""
    repository = remote or str(root)
    try:
        relative = path.resolve().relative_to(root).as_posix()
    except ValueError:
        relative = "."
    return {
        "kind": "git",
        "repository": repository,
        "relative_path": relative,
        "id": f"git:{repository}:{relative}",
    }


def local_source(path: Path) -> dict[str, str]:
    git = git_source(path)
    if git:
        return git
    resolved = str(path.resolve())
    return {"kind": "directory", "path": resolved, "id": f"dir:{resolved}"}


def loose_entry(runtime: str, path: Path, packing: str = "loose-skill") -> dict[str, Any]:
    is_link = path.is_symlink()
    raw_target = os.readlink(path) if is_link else None
    if is_link and not path.exists():
        return {
            "runtime": runtime,
            "packing": packing,
            "name": path.name,
            "declared_name": None,
            "scope": "user",
            "status": "dead-link",
            "install_path": str(path),
            "link_target": raw_target,
            "source": {
                "kind": "unresolved",
                "id": f"dead-link:{path}:{raw_target}",
            },
        }

    resolved = path.resolve()
    declared = skill_name(resolved / "SKILL.md")
    status = "ok" if declared else "missing-skill-md"
    notes: list[str] = []
    if declared and declared != path.name:
        notes.append(f"directory-name={path.name}")
    return {
        "runtime": runtime,
        "packing": packing,
        "name": declared or path.name,
        "declared_name": declared,
        "scope": "system" if packing == "built-in-skill" else "user",
        "status": status,
        "install_path": str(path),
        "resolved_path": str(resolved),
        "link_target": raw_target,
        "source": local_source(resolved),
        "notes": notes,
    }


def scan_loose_skills(home: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    roots = [
        ("codex", home / ".agents" / "skills"),
        ("codex-legacy", home / ".codex" / "skills"),
        ("claude", home / ".claude" / "skills"),
        ("zcode", home / ".zcode" / "skills"),
    ]
    for runtime, root in roots:
        if not root.is_dir():
            continue
        for child in sorted(root.iterdir(), key=lambda item: item.name):
            if child.name.startswith("."):
                continue
            entries.append(loose_entry(runtime, child))

    builtins = home / ".codex" / "skills" / ".system"
    if builtins.is_dir():
        for child in sorted(builtins.iterdir(), key=lambda item: item.name):
            if child.is_dir() or child.is_symlink():
                entries.append(loose_entry("codex", child, "built-in-skill"))
    return entries


def marketplace_source(value: Any) -> str:
    if isinstance(value, str):
        return value
    if not isinstance(value, dict):
        return "unknown"
    source_type = value.get("source")
    if source_type == "github" and value.get("repo"):
        return f"https://github.com/{value['repo']}.git"
    if source_type == "git" and value.get("url"):
        return str(value["url"])
    return json.dumps(value, sort_keys=True, ensure_ascii=False)


def codex_plugins(home: Path, warnings: list[str]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    codex = shutil.which("codex")
    use_native_cli = home == Path.home().resolve()
    if codex and use_native_cli:
        result = run([codex, "plugin", "list", "--json"])
        if result and result.returncode == 0:
            try:
                payload = json.loads(result.stdout)
                installed = payload.get("installed", []) if isinstance(payload, dict) else []
                for item in installed:
                    marketplace = item.get("marketplaceName") or "unknown"
                    name = item.get("name") or item.get("pluginId") or "unknown"
                    source_value = marketplace_source(item.get("marketplaceSource") or item.get("source"))
                    entries.append(
                        {
                            "runtime": "codex",
                            "packing": "plugin",
                            "name": name,
                            "scope": "user",
                            "status": "enabled" if item.get("enabled", True) else "disabled",
                            "version": item.get("version"),
                            "marketplace": marketplace,
                            "install_path": item.get("installedPath"),
                            "source": {
                                "kind": "plugin",
                                "id": f"plugin:{source_value}:{name}",
                                "marketplace_source": source_value,
                            },
                        }
                    )
                return entries
            except json.JSONDecodeError:
                warnings.append("Codex plugin CLI returned invalid JSON; using config.toml fallback.")
        else:
            detail = result.stderr.strip().splitlines()[-1] if result and result.stderr.strip() else "unavailable"
            warnings.append(f"Codex plugin CLI failed ({detail}); using config.toml fallback.")
    elif use_native_cli:
        warnings.append("Codex executable not found; using config.toml fallback.")

    config_path = home / ".codex" / "config.toml"
    if not config_path.is_file() or tomllib is None:
        return entries
    try:
        config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        warnings.append("Could not parse ~/.codex/config.toml.")
        return entries

    marketplaces = config.get("marketplaces", {})
    for selector, settings in sorted(config.get("plugins", {}).items()):
        name, _, marketplace = selector.partition("@")
        market = marketplaces.get(marketplace, {}) if marketplace else {}
        source_value = str(market.get("source", marketplace or "unknown"))
        revision = str(market.get("last_revision", "unknown"))
        entries.append(
            {
                "runtime": "codex",
                "packing": "plugin",
                "name": name,
                "scope": "user",
                "status": "enabled" if settings.get("enabled", True) else "disabled",
                "version": None,
                "marketplace": marketplace or None,
                "install_path": None,
                "source": {
                    "kind": "plugin",
                    "id": f"plugin:{source_value}@{revision}:{name}",
                    "marketplace_source": source_value,
                    "revision": revision,
                },
                "notes": ["config-fallback"],
            }
        )
    return entries


def claude_catalog_path(marketplace: dict[str, Any], plugin_name: str) -> str:
    root_value = marketplace.get("installLocation")
    if not root_value:
        return plugin_name
    root = Path(root_value)
    for candidate in (root / ".claude-plugin" / "marketplace.json", root / "marketplace.json"):
        payload = load_json(candidate)
        if not isinstance(payload, dict):
            continue
        for item in payload.get("plugins", []):
            if item.get("name") != plugin_name:
                continue
            source = item.get("source")
            if isinstance(source, str):
                return source
            if isinstance(source, dict):
                return marketplace_source(source)
    return plugin_name


def claude_plugins(home: Path, warnings: list[str]) -> list[dict[str, Any]]:
    registry_path = home / ".claude" / "plugins" / "installed_plugins.json"
    market_path = home / ".claude" / "plugins" / "known_marketplaces.json"
    registry = load_json(registry_path)
    markets = load_json(market_path)
    if registry is None and registry_path.exists():
        warnings.append("Could not parse Claude installed_plugins.json.")
    if not isinstance(registry, dict):
        return []
    markets = markets if isinstance(markets, dict) else {}
    entries: list[dict[str, Any]] = []
    for selector, installs in sorted(registry.get("plugins", {}).items()):
        name, _, marketplace_name = selector.partition("@")
        market = markets.get(marketplace_name, {})
        market_source = marketplace_source(market.get("source"))
        relative = claude_catalog_path(market, name)
        for install in installs if isinstance(installs, list) else []:
            install_path = Path(install.get("installPath", "")) if install.get("installPath") else None
            sha = install.get("gitCommitSha") or install.get("version") or "unknown"
            status = "ok" if install_path and install_path.exists() else "missing-cache"
            entries.append(
                {
                    "runtime": "claude",
                    "packing": "plugin",
                    "name": name,
                    "scope": install.get("scope", "unknown"),
                    "status": status,
                    "version": install.get("version"),
                    "marketplace": marketplace_name or None,
                    "project_path": install.get("projectPath"),
                    "install_path": str(install_path) if install_path else None,
                    "source": {
                        "kind": "plugin",
                        "id": f"plugin:{market_source}@{sha}:{relative}",
                        "marketplace_source": market_source,
                        "revision": sha,
                        "relative_path": relative,
                    },
                }
            )
    return entries


def zcode_plugins(home: Path, warnings: list[str]) -> list[dict[str, Any]]:
    cache_root = home / ".zcode" / "cli" / "plugins" / "cache"
    data_root = home / ".zcode" / "cli" / "plugins" / "data"
    if not cache_root.is_dir():
        return []
    active = {item.name for item in data_root.iterdir()} if data_root.is_dir() else set()
    entries: list[dict[str, Any]] = []
    for marketplace_dir in sorted(cache_root.iterdir(), key=lambda item: item.name):
        if not marketplace_dir.is_dir():
            continue
        for plugin_dir in sorted(marketplace_dir.iterdir(), key=lambda item: item.name):
            if not plugin_dir.is_dir():
                continue
            versions = sorted(
                (item for item in plugin_dir.iterdir() if item.is_dir()),
                key=lambda item: item.stat().st_mtime,
                reverse=True,
            )
            if not versions:
                continue
            install_path = versions[0]
            manifest = load_json(install_path / ".zcode-plugin" / "plugin.json")
            manifest = manifest if isinstance(manifest, dict) else {}
            name = manifest.get("name") or plugin_dir.name
            selector = f"{name}@{marketplace_dir.name}"
            repository = manifest.get("repository") or f"runtime:zcode:{marketplace_dir.name}"
            entries.append(
                {
                    "runtime": "zcode",
                    "packing": "plugin",
                    "name": name,
                    "scope": "user",
                    "status": "observed-installed" if selector in active else "cached-only",
                    "version": manifest.get("version") or install_path.name,
                    "marketplace": marketplace_dir.name,
                    "install_path": str(install_path),
                    "source": {
                        "kind": "plugin",
                        "id": f"plugin:{repository}:{name}",
                        "marketplace_source": repository,
                    },
                    "notes": ["best-effort-private-layout"],
                }
            )
    warnings.append(
        "ZCode plugin status is best-effort: private cache/data paths are not an authoritative registry."
    )
    return entries


def inventory(home: Path) -> dict[str, Any]:
    warnings: list[str] = []
    entries = scan_loose_skills(home)
    entries.extend(codex_plugins(home, warnings))
    entries.extend(claude_plugins(home, warnings))
    entries.extend(zcode_plugins(home, warnings))
    entries.sort(key=lambda item: (item["runtime"], item["packing"], item["name"], item["install_path"] or ""))
    return {"home": str(home), "entries": entries, "warnings": warnings}


def print_table(payload: dict[str, Any]) -> None:
    rows = []
    for item in payload["entries"]:
        source_id = item.get("source", {}).get("id", "")
        rows.append(
            [
                item["runtime"],
                item["packing"],
                item["status"],
                item["name"],
                item.get("scope") or "-",
                source_id,
            ]
        )
    headers = ["runtime", "packing", "status", "name", "scope", "source"]
    widths = [len(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = min(max(widths[index], len(str(value))), 72)
    print("  ".join(header.ljust(widths[index]) for index, header in enumerate(headers)))
    print("  ".join("-" * width for width in widths))
    for row in rows:
        cells = []
        for index, value in enumerate(row):
            text = str(value)
            if len(text) > widths[index]:
                text = text[: widths[index] - 1] + "…"
            cells.append(text.ljust(widths[index]))
        print("  ".join(cells))
    if payload["warnings"]:
        print("\nWarnings:", file=sys.stderr)
        for warning in payload["warnings"]:
            print(f"- {warning}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit the full machine-readable inventory.")
    parser.add_argument(
        "--home",
        type=Path,
        default=Path.home(),
        help="Override the home directory for testing.",
    )
    args = parser.parse_args()
    payload = inventory(args.home.expanduser().resolve())
    if args.json:
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        print_table(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
