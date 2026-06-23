# Multi-Runtime Actions are not transactional

Codex, Claude Code, and `npx skills` do not provide one shared transaction, so the Manager does not automatically roll back successful native operations when a later Runtime operation fails. It stops further execution, regenerates Unified Inventory, reports Partial Success, and offers explicit choices to retain successful Installations or invoke their Native Installers to restore the previous state. Automatic rollback would add another failure path and could remove a working Exposure without Operator consent.
