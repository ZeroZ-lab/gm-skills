# Version the Unified Inventory schema

Stage 1 may replace the current flat `entries[]` and `source.id` JSON with a model for Installation Packages, Package Formats, Installations, Capabilities, Exposures, Observed Evidence, and Identity Resolution. The command entrypoint `python3 scripts/inventory.py --json` remains stable, but the current JSON shape is not a compatibility contract. The replacement output includes an Inventory Schema Version, and SKILL instructions and behavior tests change with it.
