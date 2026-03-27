---
name: build-harness-project
description: Use when creating or adding `harness/` and `.harness/` layers inside a project root, clarifying the boundary between harness, product code, and `.harness/resources`, or defining the minimal closed-loop structure and setup order.
argument-hint: "[目标项目，例如：为 skills manager 创建 harness]"
context: fork
disable-model-invocation: true
---

# build-harness-project

目标：在目标项目根目录内创建 `harness/` 与 `.harness/`，并与业务代码保持清晰边界。

## 核心模型

- `<project>/harness/` = AI 开发系统（执行引擎）
- `<project>/` = 被开发的业务项目根目录
- `<project>/.harness/` = 项目给 harness 的接口层（说明书）
- 第一版只追求最小闭环：`generator + evaluator + spec.md + project-rules.md + report + run_state.json`

### Quick Reference

| 内容类型 | 放哪里 | 第一版必须 |
|---------|--------|-----------|
| 调度、agent、tools、state、logs、configs | `harness/` | ✅ |
| 真实产品代码、测试、文档 | `<project>/`（业务目录） | — |
| spec、rules、report | `.harness/` | ✅ |
| contract（任务拆分） | `.harness/contracts/` | ❌（第二阶段） |
| 参考资料 | `.harness/resources/` | ❌（第二阶段） |
| 阶段总结 | `.harness/summary.md` | ❌（可选） |

## 常见错误

| 错误 | 为什么错 | 怎么修 |
|------|---------|--------|
| 把 harness 实现塞进 `src/`、`backend/` | harness 是开发工具，不是业务代码；混入会污染产品 repo | 单独建 `harness/` 目录，与业务代码并列 |
| 把 `.harness/` 当成 harness 本体 | `.harness/` 是接口层（说明书），harness 本体是执行引擎 | `.harness/` 只放项目侧说明、约束、报告和参考材料，不放 agent/tools 代码 |
| 把 `resources` 放进 `harness/` | resources 是项目侧材料，不是平台侧能力 | 统一放 `.harness/resources/`，让 agent 按路径读取 |
| 把运行状态、日志、工件混成一层 | 调试时无法区分"是跑坏了还是业务出错了" | state 在 `harness/state/`，报告在 `.harness/reports/`，日志在 `harness/logs/` |
| 第一版就设计成大平台 | 越复杂越难跑通第一轮 | 先用最小闭环（generator + evaluator + spec + project-rules + report + run_state），二期再扩展 |
| 默认套一层 `projects/<name>/` | 大多数场景是单项目，多套一层只增加路径复杂度 | 除非用户明确要做多项目平台，否则直接用项目根目录 |

## 工作流

### 第一步：先判边界

先把用户提到的内容归类到三层之一：

- `<project>/harness/`：调度、agent、tools、state、logs、configs
- `<project>/`：真实产品代码、测试、文档、配置
- `<project>/.harness/`：spec、rules、contract、report、summary、resources

如果一个内容属于“项目给 AI 的说明书或交接材料”，默认放进 `.harness/`，不是 `harness/`。

### 第二步：再给标准结构

第一版默认只输出这套最小结构：

```text
my-project/
├─ ... existing app dirs ...
├─ harness/
│  ├─ orchestrator/
│  ├─ agents/
│  ├─ tools/
│  ├─ state/
│  ├─ logs/
│  └─ configs/
└─ .harness/
   ├─ spec.md
   ├─ project-rules.md
   └─ reports/
```

如果目标项目已经存在，就保留现有源码目录，只新增 `harness/` 与 `.harness/`。

第二阶段再补这些可选内容：

- `<project>/.harness/contracts/`
- `<project>/.harness/summary.md`
- `<project>/.harness/resources/`

### 第三步：收束成最小闭环

第一版只要求这些交付物：

- `<project>/harness/orchestrator/`
- `<project>/harness/agents/generator/`
- `<project>/harness/agents/evaluator/`
- `<project>/harness/tools/registry.py`
- `<project>/harness/state/run_state.json`
- `<project>/.harness/spec.md`
- `<project>/.harness/project-rules.md`
- `<project>/.harness/reports/`

`contracts/`、`summary.md`、`resources/`、`planner`、`checkpoint / resume`、复杂平台能力都放到第二阶段再补。

### 第四步：给出创建顺序

按这个顺序落地：

1. 确认目标项目根目录
2. 在项目根目录下创建 `harness/`
3. 在项目根目录下创建 `.harness/`
4. 写 `.harness/spec.md`
5. 写 `.harness/project-rules.md`
6. 实现 `generator`
7. 实现 `evaluator`
8. 写 `harness/state/run_state.json`
9. 跑通一轮：生成 → 检查 → 报告 → 更新状态
10. 稳定后再补 `contracts/`、`summary.md`、`resources/`、`planner`
11. 最后再补 `checkpoint / resume`

## 验收标准

第一版跑通的标志：

```
生成 → 检查 → 报告 → 更新状态
```

即 generator 产出变更 → evaluator 读取并输出 pass/fail → report 落入 `.harness/reports/` → `run_state.json` 中 `status` 更新。没有这一轮跑通，不算完成。

## 判断规则

每次设计或收文件时，都先回答这 4 个问题：

1. 这是 harness 的职责，还是业务项目的职责？
2. 这是平台侧内容，还是项目侧内容？
3. 这是运行状态，还是项目工件？
4. 这一步该由 `generator` 做，还是 `evaluator` 做？

## resources 规则

- `resources` 统一放在 `<project>/.harness/resources/`
- `resources` 是允许 harness 参考的外部材料，不是运行状态
- 默认按产品、技术、UI、数据分层，不要混成一篇长文
- 信息优先级固定为：`spec > rules > contract > resources > summary/report`
- 第一版如果还没有 `contract` 或 `resources`，不阻塞落地；缺失时直接跳过，不要伪造占位内容

## 文件级模板

当用户明确要求“每个文件里该写什么”时，再读取 [references/file-templates.md](references/file-templates.md)。

## 默认输出

默认按这 4 段输出，避免写成教程：

1. `边界判断`
2. `目录结构`
3. `最小交付物`
4. `创建步骤`
