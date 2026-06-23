# Sync requires explicit Runtime targets

Coverage Sync has no implicit Runtime target set. When an Operator requests “sync” without naming target Runtimes, the Manager may show current coverage but must ask which Runtimes to include before executing Native Installer operations. It must not assume Codex plus Claude Code, every detected Runtime, or every agent supported by `npx skills`.
