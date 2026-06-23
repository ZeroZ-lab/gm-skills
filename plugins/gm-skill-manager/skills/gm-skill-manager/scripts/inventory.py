#!/usr/bin/env python3
"""Generate a versioned, read-only inventory of agent skills and plugins."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from adapters.claude import collect_claude_evidence
from adapters.codex import collect_codex_evidence
from adapters.npx_skills import collect_npx_evidence
from inventory_model import build_inventory, render_table
from views import redact_inventory


def inventory(home: Path, *, project: Path | None = None, use_native_commands: bool = True) -> dict:
    evidence = []
    warnings: list[str] = []
    evidence.extend(collect_codex_evidence(home, warnings, use_native_commands=use_native_commands))
    evidence.extend(collect_claude_evidence(home, warnings))
    evidence.extend(
        collect_npx_evidence(home, warnings, project=project, use_native_commands=use_native_commands)
    )
    if (home / ".zcode").exists():
        evidence.append(
            {
                "runtime": "zcode",
                "package_format": "unknown",
                "installation_channel": "unknown",
                "scope": "unknown",
                "installation_state": "unknown",
                "exposure_state": "unknown",
                "installer_available": "unknown",
                "installer_compatible": "unknown",
                "remote_source": "unknown",
                "package_path": "unknown",
                "package_name": "zcode-unmanaged",
                "revision": "unknown",
                "install_path": str(home / ".zcode"),
                "project_path": "unknown",
                "development_local": False,
                "capabilities": [],
                "verification": {"registry": "unknown", "discovery": "unknown"},
                "aliases": [],
                "notes": ["unmanaged-runtime"],
                "identity_gap": "runtime-not-managed-in-stage-1",
            }
        )
        warnings.append("ZCode detected but is unmanaged in Stage 1.")
    return build_inventory(home, evidence, warnings)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit the machine-readable inventory.")
    parser.add_argument("--redact", action="store_true", help="Redact paths and URL secrets for sharing.")
    parser.add_argument("--view", choices=("capability", "package", "runtime"), default="capability")
    parser.add_argument("--home", type=Path, default=Path.home(), help="Override home for fixtures.")
    parser.add_argument(
        "--project",
        type=Path,
        help="Explicit project root whose npx skills project lock/exposures should be included.",
    )
    parser.add_argument(
        "--no-native-commands",
        action="store_true",
        help="Read registries and files only; useful for deterministic fixtures.",
    )
    args = parser.parse_args()

    home = args.home.expanduser().resolve()
    payload = inventory(
        home,
        project=args.project,
        use_native_commands=not args.no_native_commands,
    )
    if args.redact:
        payload = redact_inventory(payload, home)
    if args.json:
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        print(render_table(payload, args.view))
        for warning in payload["diagnostics"]["warnings"]:
            print(f"warning: {warning}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
