"""Read-only doctor helpers."""

from __future__ import annotations


def doctor_report(inventory: dict) -> dict:
    """Return facts, findings and recommendations without changing native state."""
    return {
        "facts": inventory["diagnostics"]["facts"],
        "findings": inventory["diagnostics"]["findings"],
        "recommendations": inventory["diagnostics"]["recommendations"],
        "warnings": inventory["diagnostics"]["warnings"],
    }
