"""Runtime Adapter orchestration.

Adapters emit Runtime Facts and collection findings, never Observed Evidence or
Capability Identity.
"""

from __future__ import annotations

from adapters import claude, codex, npx_skills, zcode
from adapters.common import InventoryContext


def collect_runtime_facts(context: InventoryContext) -> dict:
    fixture_facts = context.fixtures.get("runtime-facts")
    if fixture_facts is not None:
        return {
            "facts": fixture_facts,
            "findings": context.fixtures.get("collection-findings") or [],
        }
    facts = []
    findings = []
    for adapter in (codex, claude, npx_skills, zcode):
        result = adapter.collect(context)
        facts.extend(result["facts"])
        findings.extend(result["findings"])
    return {"facts": facts, "findings": findings}
