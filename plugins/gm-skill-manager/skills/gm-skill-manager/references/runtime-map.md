# Runtime Map

本文件记录 manager 已验证的路径与操作边界。路径不存在时视为该 runtime 或 packing mechanism 未配置，不要主动创建 plugin 私有目录。

## Source of Truth

能力身份由 Source of Truth 决定：

- loose skill：解析完整符号链接链。目标位于 git repo 时使用 `repo + repo 内相对路径`；否则使用真实目录。
- plugin：使用 marketplace source、版本或 commit、plugin source path。
- built-in：身份属于 runtime 本身，不与任何外部同名 skill 合并。
- 无法解析或指向不存在路径：标记异常，不自动归组。

名称冲突不是重复。例如三个 runtime 中都叫 `skill-creator`，只要 Source of Truth 不同，就是三个 capability。

## Codex

### Loose skills

- 当前文档化的 user root：`~/.agents/skills`
- 仓库 root：`<repo>/.agents/skills`
- 本机兼容性扫描 root：`~/.codex/skills`
- built-ins：`~/.codex/skills/.system`

新建 user loose skill 优先使用 `~/.agents/skills`。扫描 `~/.codex/skills` 是为了发现旧安装和死链，不要默认向该 legacy root 新增安装。

### Plugins

使用原生命令：

```bash
codex plugin list --available --json
codex plugin marketplace list --json
codex plugin marketplace add <source> --json
codex plugin marketplace upgrade [marketplace] --json
codex plugin add <plugin>@<marketplace> --json
codex plugin remove <plugin>@<marketplace> --json
```

若 `plugin list` 因某个失效 marketplace 整体失败，inventory 会只读解析 `~/.codex/config.toml` 的 `marketplaces` 和 `plugins` 作为 fallback。先修复失效 marketplace，再做 plugin mutation；不要手改 plugin cache。

## Claude Code

### Loose skills

- user root：`~/.claude/skills`
- project root：`<project>/.claude/skills`

### Plugins

- registry：`~/.claude/plugins/installed_plugins.json`
- marketplace registry：`~/.claude/plugins/known_marketplaces.json`
- cache：`~/.claude/plugins/cache`

只读 inventory 可读取这些文件。写操作使用原生命令：

```bash
claude plugin list --available --json
claude plugin marketplace add <source>
claude plugin marketplace update <marketplace>
claude plugin install <plugin>@<marketplace> --scope user
claude plugin uninstall <plugin>@<marketplace> --scope user --keep-data
```

scope 可为 `user`、`project` 或 `local`。卸载时必须使用 inventory 中的原 scope。安装、启用或禁用后，在交互会话运行 `/reload-plugins`。

## ZCode

### Loose skills

- 本机验证 root：`~/.zcode/skills`

使用与其他 runtime 相同的符号链接安全规则。

### Plugins

本机观察到：

- marketplace/cache：`~/.zcode/cli/plugins/cache`
- plugin data：`~/.zcode/cli/plugins/data`
- official marketplace snapshot：`~/.zcode/cli/plugins/marketplaces`

这些是私有实现路径，不是稳定写 API。cache 目录存在只表示文件曾被下载；`data/<plugin>@<marketplace>` 只能作为安装活动的局部证据。inventory 因此使用 `cached-only` 或 `observed-installed`，不会宣称完整 registry 状态。

所有 ZCode plugin 安装和卸载都通过 ZCode UI。不要直接删除 cache、data、SQLite 或编辑 marketplace snapshot。

## Loose-skill target mapping

| Runtime | User target |
| --- | --- |
| Codex | `~/.agents/skills/<name>` |
| Claude Code | `~/.claude/skills/<name>` |
| ZCode | `~/.zcode/skills/<name>` |

安装前比较目标与源的真实路径。相同则幂等，不同则冲突。
