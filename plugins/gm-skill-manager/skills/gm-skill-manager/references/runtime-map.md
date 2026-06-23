# Runtime Map

本文件只记录 Stage 1 已验证的 Native Installer 和权威 evidence。命令和格式可能随 Runtime 更新，执行 mutation 前先读取本机 `--help`。

## Codex

### Evidence

- Plugin list：`codex plugin list --json`
- Marketplace list：`codex plugin marketplace list --json`
- 配置 fallback：`~/.codex/config.toml`
- Built-ins：`~/.codex/skills/.system`

### Native operations

```bash
codex plugin marketplace add <remote> --json
codex plugin marketplace upgrade <marketplace> --json
codex plugin add <plugin>@<marketplace> --json
codex plugin remove <plugin>@<marketplace> --json
```

Codex CLI 当前没有稳定的 plugin enable/disable 子命令。使用 Codex Plugin UI 执行；若 UI 不可操作，则阻止 Action，不直接编辑 `config.toml`。

Registry Verification 使用 `codex plugin list --json`。Discovery Verification 使用 Codex Plugin/Skill 列表重新读取结果。

## Claude Code

### Evidence

- Native list：`claude plugin list --json`
- Registry fallback：`~/.claude/plugins/installed_plugins.json`
- Marketplace registry：`~/.claude/plugins/known_marketplaces.json`
- Scope：`user`、`project`、`local`

### Native operations

```bash
claude plugin install <plugin>@<marketplace> --scope <scope>
claude plugin uninstall <plugin>@<marketplace> --scope <scope> --keep-data
claude plugin enable <plugin>@<marketplace> --scope <scope>
claude plugin disable <plugin>@<marketplace> --scope <scope>
claude plugin list --json
```

卸载默认使用 `--keep-data`。只有 Operator 明确授权 Data Removal 时才允许删除持久数据。变更后运行 `/reload-plugins` 或重启会话，再做 Discovery Verification。

## npx skills

### Evidence

- Managed Installation：global/project skill lock
- Global lock：`~/.agents/.skill-lock.json`
- Native list：`npx skills list -g --json`
- Project list：在 Operator 明确指定的 project root 中运行 `npx skills list --json`
- Exposure：Native list 中的 agent 集合及 Runtime link

```text
lock + exposure → installed + active
lock only       → installed + inactive
exposure only   → broken + unmanaged
neither         → absent
```

### Native operations

```bash
npx skills add <remote> --agent <runtime> --skill <skill> --global
npx skills remove --agent <runtime> --skill <skill> --global
npx skills update <skill> --global
npx skills list --global --json
```

`npx skills remove --agent` 表达目标 Runtime 的 disable/remove Exposure，不等于删除其他 Runtime Installation。
Project lock 仅在 inventory 收到显式 `--project <root>` 时读取；不得用当前目录隐式决定 scope。

## ZCode

Stage 1 只检测 `~/.zcode` 是否存在并报告 `unmanaged`。不读取私有 cache/data 作为权威状态，不执行 mutation。

## Sources

- Codex CLI plugin reference: https://developers.openai.com/codex/cli/reference
- Codex plugin behavior: https://developers.openai.com/codex/plugins
- Claude Code plugin reference: https://code.claude.com/docs/en/plugins-reference
