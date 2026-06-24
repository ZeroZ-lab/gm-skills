---
name: gm-skill-manager
description: 统一盘点和协调 Codex Plugin、Claude Code Plugin 与 npx skills。Use when the operator asks to list or diagnose installed skills, inspect duplicate exposures or revision drift, install or remove a remote skill package, enable or disable an exposure, or repair native installation records without creating a fourth installer.
---

# GM Skill Manager

作为可执行协调者管理 Skills。Codex、Claude Code 与 `npx skills` 的 Native Installer 和原生记录始终权威；Manager 只生成当前 Unified Inventory、制定 Execution Plan、调用原生机制并验证结果。

## 不可违反的规则

1. 先 inventory，再 Action，Action 后重新 inventory。
2. Capability Identity 只由 normalized Remote Source + canonical `SKILL.md` path 决定；Revision、名称、Runtime 和 Package Format 不参与身份。
3. Runtime Adapter 只产 Runtime Facts；Observed Evidence module 负责标准化与验证；只有 Identity Resolution 可以裁决相同 Capability。
4. 不直接修改 plugin registry、cache、`skills-lock`、私有数据库或 Runtime links。
5. 不复制本地目录模拟安装；普通安装只接受 GitHub/Git Remote Source。
6. doctor 只读；repair 是独立 mutation Action。
7. Facts、Findings、Recommendations、Execution Plan 分开输出。
8. Stage 1 管理 Codex Plugin、Claude Code Plugin、`npx skills`；ZCode 仅报告 unmanaged。

## 生成 Unified Inventory

从本 skill 目录运行：

```bash
python3 scripts/inventory.py --json
```

可选视图：

```bash
python3 scripts/inventory.py --view capability
python3 scripts/inventory.py --view package
python3 scripts/inventory.py --view runtime
python3 scripts/inventory.py --redact --json
python3 scripts/inventory.py --project /explicit/project/root --json
```

默认使用 Capability View。机器可读输出当前使用 `schema_version: "2.0"`；required field 的未知值显式写 `unknown`。
Project scope 只在 Operator 通过 `--project` 明确给出根目录时读取；不得从当前工作目录推断。

Inventory 必须能够表达：

- Installation Package、Package Format、Installation、Capability、Exposure；
- Runtime Facts 经标准化后的 Observed Evidence；
- Evidence Subject、Validity、Provenance 与 Evidence Findings；
- Resolved / Unresolved Identity；
- Installation State 与 Exposure State；
- Revision Relation；
- Registry / Discovery Verification；
- Duplicate Exposure、Revision drift、broken Installation；
- ZCode unmanaged。

无效 evidence 必须保留并显示 finding，但不得产生 Installation、Capability、Exposure 或 Execution Plan。ZCode detection 只进入 Runtime View，不创建虚假的 Installation Package。

## Action 路由

执行任何 mutation 前读取 [references/action-contract.md](references/action-contract.md)。需要 runtime 路径和命令时读取 [references/runtime-map.md](references/runtime-map.md)。

### 只读 Action

- `list`：生成三种视图。
- `doctor`：报告 installer、identity、state、scope、manifest 与 exposure 问题。
- Remote catalog / Package Impact：读取已知 Remote Source，不搜索未知仓库猜来源。

### Mutation Action

- `install`
- `uninstall`
- `enable`
- `disable`
- `repair`

Mutation 必须：

1. 明确 Capability 或 Installation Package。
2. 明确目标 Runtime；不默认 Codex + Claude。
3. 多 scope 可选时让 Operator 明确选择。
4. 预览 Package Impact 和受影响 Capabilities。
5. 选择目标 Runtime 最原生的 Package Format；没有时才使用 `npx skills`。
6. 使用 Native Installer 或 Runtime 原生 Plugin UI。
7. 每步后立即做 Registry Verification 和 Discovery Verification。
8. 失败即停止，重新 inventory，报告 Partial Success；不自动回滚。

明确请求已包含 Action、目标、Runtime 和 scope 时可视为 Action Authorization。若预检发现额外 Capability、可执行扩展、数据删除、project/local scope 或批量影响，必须再次确认。

## Native Installer 选择

```text
Codex 有 codex-plugin format
  → codex plugin / Codex Plugin UI

Claude Code 有 claude-code-plugin format
  → claude plugin

目标 Runtime 无原生 Plugin format，但 npx skills 支持
  → npx skills

均不支持
  → blocked: unsupported-format
```

一个 Capability 在同一 Runtime 同时由 Plugin 与 `npx skills` 暴露时，不推断加载优先级：标记 `ambiguous`，推荐保留原生 Plugin，但不自动删除。

## 完成验证

Action 完成必须同时满足：

- Native Installer 返回成功；
- 原生 registry / lock 反映目标状态；
- Runtime 能可靠发现 Capability；
- 没有新增 Duplicate Exposure 或 broken Installation；
- 实际影响未超出已授权 Execution Plan。

无法完成 Discovery Verification 时，Exposure State 保持 `unknown`，不得声称 active。
安装目录中存在 `SKILL.md` 只证明文件/manifest evidence，不构成 Discovery Verification。

## 输出契约

```markdown
## Facts
- 当前 Native Installer evidence 和 Unified Inventory 状态

## Findings
- identity、revision、installation、exposure、scope 问题

## Recommendations
- 非执行建议

## Execution Plan
- 仅在 Operator 选择 Action 后生成

## Verification
- Registry / Discovery evidence

## Risks
- unknown、unmanaged、partial success、未验证内容
```
