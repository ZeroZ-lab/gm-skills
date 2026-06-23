# Test the versioned inventory through synthetic fixtures

Stage 1 behavior tests use synthetic temporary homes and Native Installer outputs for Codex Plugin, Claude Code Plugin, and `npx skills`. Fixtures cover cross-format Capability convergence, differing and unknown Revisions, Unresolved Identity, managed and unmanaged Exposures, scope overlap, and Duplicate Exposure. The versioned Unified Inventory JSON is the primary test surface; private helpers are not the contract, and the real machine is used only for smoke testing.
