---
name: gm-skill-manager
description: 统一盘点、安装、卸载和整理一台电脑上的 Codex、Claude Code、ZCode skills 与 plugins。Use when the operator asks to list local skills, diagnose duplicate names or dead links, install one capability into multiple runtimes, remove an installation safely, or clean up a disorganized multi-runtime skill setup.
---

# GM Skill Manager

管理本机多个 coding-agent runtime 的 skills 和 plugins。以 Source of Truth 判断能力身份；名称只用于展示，不能用于去重或删除决策。

## 核心规则

1. 先盘点，后修改。任何 install 或 uninstall 前都运行只读 inventory。
2. 按 Source of Truth 分组。同名但来源不同的条目保持分离。
3. 优先使用 runtime 原生命令或 UI。不要直接修改 plugin registry、cache、SQLite 或 runtime 私有状态。
4. loose skill 使用符号链接，不复制源目录，不覆盖已有路径。
5. built-in skill 只报告，不安装、不卸载。
6. 不执行 `rm -rf`。卸载 loose skill 时只删除已确认的符号链接，不删除链接目标。
7. 对“整理一下”这类宽泛请求，只输出清理计划并等待确认；明确指定目标、runtime 和动作的安装请求可在预检后执行。

## 工作流

### 1. 明确动作

将请求归类为：

- `list`：只读盘点、去重、找死链或冲突。
- `install`：把一个已确认来源的 loose skill 或 plugin 安装到目标 runtime。
- `uninstall`：移除指定 runtime 中的一个安装。

若用户只给出名称但存在多个 Source of Truth，停止并展示候选来源，不猜。

### 2. 运行 inventory

从本 skill 目录运行：

```bash
python3 scripts/inventory.py --json
```

使用返回的 `entries` 和 `warnings`：

- 以 `source.id` 聚合 capability。
- 单独标出 `dead-link`、`missing-skill-md`、`missing-cache` 和 `cached-only`。
- 不把 `cached-only` 当成已安装 plugin。
- runtime 私有命令失败时保留 warning，并使用脚本提供的只读 fallback 结果。

需要理解路径、scope、原生命令或 ZCode 限制时，读取 [references/runtime-map.md](references/runtime-map.md)。

### 3. 生成变更计划

在写操作前列出：

- capability 的 Source of Truth；
- 目标 runtime 和 packing mechanism；
- 将创建、删除或由原生命令维护的路径；
- 冲突、scope 和数据保留行为；
- 验证命令。

如果是批量整理、卸载、死链清理、跨多个 runtime 的同步，先获得 Operator 对这份精确计划的确认。

### 4. 执行动作

#### 安装 loose skill

1. 确认源目录存在且包含 `SKILL.md`。
2. 解析源目录真实路径和 git Source of Truth。
3. 选择 runtime 的 loose-skill 根目录。
4. 若目标不存在，创建父目录后建立绝对符号链接。
5. 若目标已存在：
   - 解析到同一 Source of Truth：报告 `already-installed`；
   - 解析到其他来源：报告冲突并停止；
   - 是普通目录：不要覆盖或移动。

#### 安装 plugin

- Codex：使用 `codex plugin marketplace ...` 和 `codex plugin add ... --json`。
- Claude Code：使用 `claude plugin marketplace ...` 和 `claude plugin install ... --scope ...`；安装后提示 `/reload-plugins`。
- ZCode：只使用 ZCode 的 plugin UI。没有可用 UI 自动化能力时，给出精确人工步骤并停止；不要写 `~/.zcode/cli/plugins`。

#### 卸载 loose skill

1. 再次确认 install path、链接目标和 Source of Truth。
2. 目标是符号链接时，只删除该链接。
3. 目标是死链时，仅在计划中明确列出后删除。
4. 目标是普通目录时停止，除非 Operator 明确说明该目录本身就是要删除的 Source of Truth；这超出默认 MVP。

#### 卸载 plugin

- Codex：使用 `codex plugin remove <plugin>@<marketplace> --json`。
- Claude Code：使用 `claude plugin uninstall <plugin>@<marketplace> --scope <scope> --keep-data`。只有 Operator 明确要求清除数据时才省略 `--keep-data`。
- ZCode：只通过 ZCode plugin UI 卸载。

### 5. 验证

修改后重新运行：

```bash
python3 scripts/inventory.py --json
```

验证：

- 目标 runtime 中安装状态符合请求；
- 没有新增 dead link；
- 同名不同 Source of Truth 未被误合并；
- plugin 原生命令成功，或 UI 状态已重新读取；
- 未触碰未列入计划的 scope、目录或 runtime。

## 输出契约

默认返回：

```markdown
## Inventory
- runtime、packing、name、scope、status、Source of Truth

## Findings
- dead links、名称冲突、重复安装、无法解析来源

## Changes
- 已执行的精确动作；list 请求写“无修改”

## Verification
- 运行的命令和结果

## Risks
- fallback 结果、未验证 UI、未知 registry 版本或保留数据
```

明确区分事实、推断和建议。不要把 cache 存在推断为 plugin 已安装。
