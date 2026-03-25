---
name: gm-battle
description: 初始化一个回合制 AI 方案评审 battle。用于在同一任务上让 Agent A 先给方案、Agent B 再挑战，只审核方案不改代码，写入 battle 状态文件并生成第一条可直接发送的方案 prompt。
argument-hint: "[任务描述]"
context: fork
disable-model-invocation: true
---

# gm-battle

开始一个新的 battle session，并把它整理成可继续推进的状态。

这个 skill 不负责替用户调用模型，只负责初始化 battle、生成 `pk_id`、写入该 session 的状态文件，并给出第一条应该发给 Agent A 的 prompt。

## 适用场景

当用户表达类似需求时使用这个 skill：

- “我想让两个模型对打评审同一个方案。”
- “先让一个模型出方案，再让另一个模型专门挑刺。”
- “帮我开一个 battle session。”
- “我要开始一轮 AI review arena。”

适用于：

- 方案评审
- 架构评审
- 实现思路对打
- 多轮 challenge / revise 式打磨

不适用于：

- 已经有 battle 状态，用户只是想推进到下一阶段
- 用户要你直接替他执行完整评审流程

如果用户要的是“继续下一轮”，应改用 `/gm:gm-pk`。

## 输入

优先从用户输入里提取这些信息：

- `task`：这场 battle 要解决什么任务
- `constraints`：约束、背景、限制条件

如果用户只给了任务，没有明确约束，默认使用 `无`。

如果用户没有提供足够信息，最多补问两类内容：

1. 具体任务是什么
2. 有哪些必须遵守的约束或背景

不要把初始化阶段问成长访谈。这个 skill 的目标是尽快开始 battle，而不是把需求讨论完整。

整个 battle 只允许讨论方案、结构、风险、边界和取舍。

不允许要求任何 Agent：

- 编写代码
- 修改代码
- 提交 patch
- 输出可直接应用的代码变更

## 工作流

### 第一步：确认 battle 输入

先确认至少拿到了 `task`。

如果没有任务描述，不要初始化，也不要写入文件。直接要求用户先给出任务。

如果有任务但没有约束：

- 将 `constraints` 设为 `无`

### 第二步：生成 `pk_id` 并写入 battle 文件

为这场 battle 生成一个唯一的 `pk_id`。

`pk_id` 应简短、可读、可复制，例如时间戳或短随机串，但必须能稳定对应这一次 battle。

写入 `battle/sessions/<pk_id>/state.json`，内容结构应为：

```json
{
  "pk_id": "<本次生成的 battle id>",
  "title": "<从任务中提炼的简短标题>",
  "task": "<用户提供的任务>",
  "constraints": "<用户提供的约束，或 '无'>",
  "current_round": 1,
  "current_stage": "implement",
  "current_actor": "agent_a",
  "status": "in_progress",
  "last_implement_output": "",
  "last_judge_output": ""
}
```

写入 `battle/sessions/<pk_id>/issues.json`，内容结构应为：

```json
{
  "open": [],
  "resolved": [],
  "rejected": []
}
```

同时写入 `battle/latest.json`，至少记录：

```json
{
  "pk_id": "<本次生成的 battle id>"
}
```

每次调用都视为“开启一场新的 battle”：

- 创建新的 `battle/sessions/<pk_id>/` 目录
- 写入当前 session 的 `state.json` 和 `issues.json`
- 更新 `battle/latest.json` 指向这次新建的 battle
- 不覆盖其他 `pk_id` 对应的历史 battle

### 第三步：生成第一条方案 prompt

初始化完成后，输出一条可直接发给 Agent A 的 prompt。

这条 prompt 应明确：

- Agent A 的角色是方案提出者
- 当前任务是什么
- 约束是什么
- 需要产出方案概述、关键决策、潜在风险
- 明确禁止输出代码或改代码

推荐格式：

```md
你是 Agent A（方案提出者）。

任务：{task}
约束：{constraints}

这是一场纯方案评审 battle，只允许讨论方案，不允许编写、修改或提交任何代码。

请提供你的方案，包括：
1. 方案概述
2. 关键设计决策
3. 潜在风险（如果有）
```

### 第四步：告诉用户下一步怎么继续

在输出 prompt 后，明确告诉用户下一步动作：

1. 记住这次 battle 的 `pk_id`
2. 把这条 prompt 发给 Agent A
3. 拿到 Agent A 的完整回复后，写入 `battle/sessions/<pk_id>/state.json` 的 `last_implement_output`
4. 再运行 `/gm:gm-pk <pk_id>` 推进到 challenge 阶段；如果当前只有这一场未完成 battle，也可以直接运行 `/gm:gm-pk`

## 输出格式

默认输出应包含三部分：

```md
# Battle 已初始化

- pk_id：
- 标题：
- 当前轮次：
- 当前阶段：
- 当前执行方：

## 发给 Agent A 的 Prompt
<prompt 正文>

## 下一步
1. ...
2. ...
3. ...
```

如果初始化失败，直接说明缺了什么，不要输出半成品 prompt。

## 约束

- 不要替用户发送 prompt 给任何模型
- 不要在没有任务描述的情况下初始化
- 不要保留旧 battle 的状态内容
- 不要跳过文件写入，只输出 prompt
- 不要把 battle 初始化和 battle 推进混在同一次调用里
- 不要让任何 Agent 在 battle 中编写或修改代码

## 默认风格

保持直接、清楚、偏流程编辑感。

目标不是把 battle 讲复杂，而是让用户立刻知道：

- battle 的 `pk_id` 是什么
- battle 已经怎样被初始化
- 第一条 prompt 应该发给谁
- 下一步应该做什么
