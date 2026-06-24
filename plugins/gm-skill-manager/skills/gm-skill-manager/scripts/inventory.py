#!/usr/bin/env python3
"""Generate a versioned, read-only inventory of agent skills and plugins."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from adapters import collect_runtime_facts
from adapters.common import InventoryContext
from inventory_model import build_inventory, render_table
from observed_evidence import normalize_runtime_facts
from views import redact_inventory


def inventory(
    home: Path,
    *,
    project: Path | None = None,
    use_native_commands: bool = True,
    fixtures: dict | None = None,
) -> dict:
    context = InventoryContext(
        home=home,
        project=project,
        use_native_commands=use_native_commands,
        fixtures=fixtures or {},
    )
    collected = collect_runtime_facts(context)
    evidence = normalize_runtime_facts(collected["facts"])
    return build_inventory(home, evidence, collected["findings"])


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
        for finding in payload["diagnostics"]["collection_findings"]:
            print(f"warning: {finding['runtime']} {finding['code']}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
