# Action Scenarios

| Scenario | Expected Native mechanism | Guard |
|---|---|---|
| Install Codex plugin | `codex plugin add` | Remote/package/runtime explicit |
| Install Claude plugin | `claude plugin install --scope` | Scope explicit |
| Install standalone skill | `npx skills add --agent --skill` | No native plugin format |
| Disable Claude plugin | `claude plugin disable --scope` | Dependency failure preserved |
| Disable Codex plugin | Codex Plugin UI | Never edit config directly |
| Disable npx exposure | `npx skills remove --agent --skill` | Other runtimes preserved |
| Uninstall Claude plugin | `claude plugin uninstall --keep-data` | Data retained by default |
| Repair broken npx install | `npx skills add/remove` | Never edit lock or link |
| Unsupported runtime | none | Action blocked |
| Multi-runtime partial failure | stop and inventory | No automatic rollback |
