# Manager keeps no persistent state

The Manager generates only the current Unified Inventory from Codex, Claude Code, and `npx skills` authoritative records. It does not retain inventory snapshots, an Action Log, or a cross-runtime registry. Every plan and verification rereads native state; if historical auditing is needed later, it must come from the Native Installers or a separately approved system rather than silently expanding the Manager's ownership.
