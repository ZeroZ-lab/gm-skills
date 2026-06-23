"""Capability and package identity resolution.

Decisions: ADR-0001, ADR-0003, ADR-0004, ADR-0005.
"""

from __future__ import annotations

import posixpath
import re
from urllib.parse import urlsplit, urlunsplit

UNKNOWN = "unknown"


def normalize_remote(value: str | None) -> str:
    """Normalize equivalent Git SSH/HTTPS remotes without retaining credentials."""
    if not value or value == UNKNOWN:
        return UNKNOWN
    remote = value.strip()
    ssh = re.match(r"^git@([^:]+):(.+)$", remote)
    if ssh:
        remote = f"https://{ssh.group(1)}/{ssh.group(2)}"
    elif remote.startswith("ssh://git@"):
        parts = urlsplit(remote)
        remote = urlunsplit(("https", parts.hostname or "", parts.path, "", ""))
    elif "://" not in remote and re.match(r"^[\w.-]+/[\w.-]+$", remote):
        remote = f"https://github.com/{remote}"

    if "://" in remote:
        parts = urlsplit(remote)
        hostname = (parts.hostname or "").lower()
        path = re.sub(r"/+", "/", parts.path).rstrip("/")
        if path.endswith(".git"):
            path = path[:-4]
        return urlunsplit(("https", hostname, path, "", ""))
    return remote.rstrip("/").removesuffix(".git")


def canonical_path(value: str | None) -> str:
    if not value or value == UNKNOWN:
        return UNKNOWN
    normalized = posixpath.normpath(value.replace("\\", "/"))
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized if normalized not in ("", ".") else UNKNOWN


def resolve_capability(evidence: dict, candidate: dict) -> dict:
    """Return the only identity result callers may use for equality."""
    if evidence["package_format"] == "built-in":
        builtin_path = canonical_path(candidate.get("skill_path"))
        runtime = evidence.get("runtime", UNKNOWN)
        if runtime != UNKNOWN and builtin_path != UNKNOWN:
            return {
                "status": "resolved",
                "key": f"builtin:{runtime}:{builtin_path}",
                "remote_source": UNKNOWN,
                "skill_path": builtin_path,
                "reason": "runtime-and-built-in-path",
            }

    remote = normalize_remote(evidence.get("remote_source"))
    skill_path = canonical_path(candidate.get("skill_path"))
    if remote != UNKNOWN and skill_path != UNKNOWN and not evidence.get("development_local", False):
        return {
            "status": "resolved",
            "key": f"remote:{remote}:{skill_path}",
            "remote_source": remote,
            "skill_path": skill_path,
            "reason": "remote-and-canonical-skill-path",
        }
    return {
        "status": "unresolved",
        "key": UNKNOWN,
        "remote_source": remote,
        "skill_path": skill_path,
        "reason": evidence.get("identity_gap", "insufficient-evidence"),
    }


def resolve_package(evidence: dict) -> dict:
    if evidence["package_format"] == "built-in":
        return {
            "status": "resolved",
            "key": f"builtin-package:{evidence.get('runtime', UNKNOWN)}",
            "remote_source": UNKNOWN,
            "package_path": UNKNOWN,
        }
    remote = normalize_remote(evidence.get("remote_source"))
    package_path = canonical_path(evidence.get("package_path"))
    if remote != UNKNOWN and package_path != UNKNOWN and not evidence.get("development_local", False):
        return {
            "status": "resolved",
            "key": f"package:{remote}:{package_path}",
            "remote_source": remote,
            "package_path": package_path,
        }
    return {
        "status": "unresolved",
        "key": UNKNOWN,
        "remote_source": remote,
        "package_path": package_path,
    }


def revision_relation(revisions: list[str]) -> str:
    known = [value for value in revisions if value and value != UNKNOWN]
    if len(known) != len(revisions) or len(known) < 2:
        return "unknown"
    return "same" if len(set(known)) == 1 else "different"
