---
name: gm-harness-plan-task
description: Use when a user wants to add a feature, fix a bug, or define a new task for an existing harness project.
argument-hint: "[需求描述，例如：给 skills manager 加登录功能]"
---

# gm-harness-plan-task

目标：把用户的需求转化为 `.harness/` 里的正确文档更新，并给出可直接运行的命令。

**前提**：项目已有 `harness/` 与 `.harness/` 目录。如果还没有，先用 `gm-harness-init` 搭结构。

## 工作流

### 第一步：读取现状

依次读取：

1. `.harness/spec.md` — 项目当前目标和验收标准
2. `.harness/project-rules.md` — 约束和禁止项
3. `harness/state/run_state.json` — 当前 sprint 编号和状态

没有这三个文件就停下来，提示用户先运行 `gm-harness-init`。

### 第二步：分类请求

| 请求类型 | 判断标准 | 操作 |
|---------|---------|------|
| 新功能 / 新任务 | 在现有目标内的具体实现工作 | 新建 `contracts/sprint-N.md` |
| 目标 / 范围变更 | 影响整个项目方向或验收标准 | 更新 `spec.md` |
| 约束变更 | 技术栈、命令范围、禁止项有变化 | 更新 `project-rules.md` |

**分类不确定时，默认建 contract，不改 spec。**

### 第三步：写入文档

**新建 contract**（最常见）：

N = 扫描 `.harness/contracts/` 目录，取已有 `sprint-*.md` 文件的最大编号 + 1。目录为空时 N = 1。**不要用 `run_state.json` 的 `current_sprint` 字段推算，避免 running 状态下重复编号。**

```markdown
# Sprint N — <任务名>

## 目标
<一句话说清楚要做什么>

## 验收标准
- [ ] <可检验的标准，有具体行为或输出>
- [ ] <可检验的标准>

## 不做什么
- <明确排除的内容>
```

如果 `.harness/contracts/` 目录不存在，先创建它。

**更新 spec.md**：追加新范围或修改验收标准，不删历史内容，用 `## 更新 <日期>` 标注变更。

**更新 project-rules.md**：在对应章节追加，加更新日期注释。

### 第四步：更新 run_state.json（仅限新建 contract）

**只有"新建 contract"时**才改 `run_state.json`，改这几个字段（`current_sprint` 用第三步算出的 N），其余保留原值：

```json
{
  "current_sprint": <N>,
  "status": "idle",
  "next_action": "run_generator",
  "last_checkpoint": null,
  "last_report": null
}
```

**更新 spec.md 或 project-rules.md 时，不动 `run_state.json`。**

如果当前 `status` 是 `running` 或 `evaluating`，照常更新文档，跳过 `run_state.json` 修改，并在输出中注明"已写入文档，等当前 run 结束后再执行"。

### 第五步：给出运行命令

```bash
# 从项目根目录运行
python harness/orchestrator/main.py
```

如果 harness 支持 `--project` 参数：

```bash
python harness/orchestrator/main.py --project <project_path>
```

## 判断规则

- contract 里的验收标准必须**可检验**（有具体行为或输出），不能写"代码质量好"
- sprint 编号从扫描 `contracts/` 目录取最大值 +1，不要用 `run_state.json` 的 `current_sprint` 推算
- 没读完 `spec.md` 不能判定"这是范围变更"
- 不要在 contract 里重复 spec.md 和 project-rules.md 的内容
- 如果 `run_state.json` 的 `status` 是 `running` 或 `evaluating`，文档照常更新，不改 run_state.json，输出中注明等当前 run 结束

## 默认输出

按这 4 段输出，不要写成教程：

1. `需求分类` — 判断类型 + 一句话理由
2. `文档变更` — 列出新增/修改的文件，粘贴关键内容
3. `状态更新` — 仅新建 contract 时输出 run_state.json 的新值；其他类型写"无状态变更"
4. `运行命令` — 仅新建 contract 时输出可直接复制的命令；其他类型写"无需运行"
