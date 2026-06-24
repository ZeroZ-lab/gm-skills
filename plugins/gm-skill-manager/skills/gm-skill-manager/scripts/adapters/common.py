from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

UNKNOWN = "unknown"


@dataclass(frozen=True)
class InventoryContext:
    home: Path
    project: Path | None = None
    use_native_commands: bool = True
    fixtures: dict[str, Any] = field(default_factory=dict)


def adapter_result(facts: list[dict] | None = None, findings: list[dict] | None = None) -> dict:
    return {"facts": facts or [], "findings": findings or []}


def run(command: list[str], timeout: int = 15, cwd: Path | None = None) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False, cwd=cwd)
    except (OSError, subprocess.TimeoutExpired):
        return None


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def skill_name(skill_md: Path) -> str:
    try:
        head = skill_md.read_text(encoding="utf-8")[:4096]
    except OSError:
        return UNKNOWN
    match = re.search(r"(?m)^name:\s*[\"']?([^\"'\n]+)", head)
    return match.group(1).strip() if match else UNKNOWN


def discover_skills(root: Path, remote_prefix: str = "") -> list[dict]:
    if not root.is_dir():
        return []
    results = []
    for skill_md in sorted(root.rglob("SKILL.md")):
        relative = skill_md.relative_to(root).as_posix()
        path = "/".join(part for part in (remote_prefix.strip("/"), relative) if part)
        results.append({"name": skill_name(skill_md), "skill_path": path or relative, "aliases": []})
    return results
