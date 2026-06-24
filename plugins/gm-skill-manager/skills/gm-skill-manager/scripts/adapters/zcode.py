"""Unmanaged ZCode runtime detection adapter."""

from __future__ import annotations

from adapters.common import InventoryContext, adapter_result


def collect(context: InventoryContext) -> dict:
    root = context.home / ".zcode"
    if not root.exists():
        return adapter_result()
    return adapter_result(
        [
            {
                "fact_type": "zcode-detection",
                "runtime": "zcode",
                "native_record_id": "runtime-detection",
                "install_path": str(root),
                "provenance": {
                    "source_kind": "filesystem",
                    "source_id": ".zcode",
                    "collection": "success",
                },
            }
        ]
    )
