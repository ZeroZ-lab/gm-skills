---
name: gm-pk
description: 推进当前 battle session 到下一阶段。读取对应 pk_id 的状态文件，按 implement、challenge、revise、judge 的状态生成下一条 prompt，并更新回合信息。整个 battle 只审核方案不改代码。用 “gm-pk [pk_id] stop” 结束 battle 进入 judge。
argument-hint: "[pk_id] [stop]"
context: fork
disable-model-invocation: true
---

# gm-pk

把某一场 battle 从一个阶段推进到下一个阶段。

这个 skill 不负责替用户调用模型；它负责根据 `pk_id` 读取 battle 状态、判断当前所处阶段、更新该 session 的状态文件，并生成下一条应该发给哪个 Agent 的 prompt。

整个 battle 是方案评审流程，不是编码流程。

不允许要求任何 Agent：

- 编写代码
- 修改代码
- 提交 patch
- 输出大段可直接落地的代码实现

## 适用场景

当用户表达类似需求时使用这个 skill：

- “把这场 battle 推到下一轮。”
- “Agent A 已经给出方案了，下一步该给谁？”
- “结束 battle，进入裁判阶段。”
- “继续 challenge / revise 流程。”

适用于：

- implement -> challenge
- challenge -> revise
- revise -> 下一轮 challenge
- 任意非完成阶段 -> judge
- judge -> completed

不适用于：

- 还没初始化 battle
- 用户要新开一场 battle

如果用户要的是“开始一场新的 battle”，应改用 `/gm:gm-battle`。

## 输入

优先读取这些输入：

- `battle/sessions/<pk_id>/state.json`
- `battle/sessions/<pk_id>/issues.json`
- 如果没有传 `pk_id`，优先读取 `battle/latest.json`
- 用户调用时是否带了 `stop`

重点字段包括：

- `current_stage`
- `current_round`
- `task`
- `constraints`
- `last_implement_output`
- `last_judge_output`
- `status`
- `open`
- `resolved`
- `rejected`

如果用户没有给额外说明，也应继续工作，不要为了补字段而重新追问。

## 前置检查

先确认本次要操作哪一个 `pk_id`。

如果用户显式传了 `pk_id`，就使用它。

如果没有传 `pk_id`，优先读取 `battle/latest.json`。

如果 `battle/latest.json` 不存在，直接输出：

> 没有可继续的 battle。请先运行 `/gm:gm-battle` 初始化，或显式传入 `pk_id`。

然后停止。

拿到 `pk_id` 后，再检查 `battle/sessions/<pk_id>/state.json` 是否存在且可读。

如果不存在或为空，直接输出：

> `battle/sessions/<pk_id>/state.json` 不存在。请先确认 `pk_id` 是否正确，或重新运行 `/gm:gm-battle` 初始化 battle。

然后停止。

再检查是否能读取 `battle/sessions/<pk_id>/issues.json`。

如果缺失，也应明确提示 battle 状态不完整，并停止，而不是继续假设。

## 工作流

### 第一步：读取当前 battle 状态

从 `battle/sessions/<pk_id>/state.json` 读取当前阶段与轮次信息。

从 `battle/sessions/<pk_id>/issues.json` 读取问题列表。

同时判断这次调用是否带了 `stop` 参数。

### 第二步：按阶段推进

#### 情况 A：当前是 `implement`，且没有 `stop`

先检查 `last_implement_output` 是否为空。

如果为空，直接输出：

> `last_implement_output` 为空。请先把 Agent A 的方案输出写入 `battle/sessions/<pk_id>/state.json`，再运行 `/gm:gm-pk`。

然后停止。

如果不为空：

- 将 `current_stage` 更新为 `challenge`
- 将 `current_actor` 更新为 `agent_b`

然后生成发给 Agent B 的挑战 prompt。

这条 prompt 应要求 Agent B：

- 从正确性、安全性、性能、边界情况四个方向提问题
- 给每个问题标严重程度
- 使用统一的 `[ISSUE]` 格式输出
- 只审核方案，不给出代码实现

输出给用户的下一步动作时，还应明确要求：

1. 拿到 Agent B 的回复后，打开 `battle/sessions/<pk_id>/issues.json`
2. 将每条 `[ISSUE]` 解析后写入 `open` 数组，至少包含 `id`、`title`、`severity`、`description`、`raised_by`、`round`
3. 再运行 `/gm:gm-pk <pk_id>`；如果当前只有这一场未完成 battle，也可以直接运行 `/gm:gm-pk`

### 情况 B：当前是 `challenge`，且没有 `stop`

将 `battle/sessions/<pk_id>/issues.json` 中 `open` 数组整理成编号问题列表。

如果 `open` 数组为空，直接输出：

> `battle/sessions/<pk_id>/issues.json` 的 `open` 为空。请先把 Agent B 的 `[ISSUE]` 输出写入该文件，再运行 `/gm:gm-pk`。

然后停止。

然后：

- 将 `current_stage` 更新为 `revise`
- 将 `current_actor` 更新为 `agent_a`

接着生成发给 Agent A 的 revise prompt。

这条 prompt 应明确要求 Agent A：

- 对成立的问题给出方案修订
- 对不成立的问题明确说明拒绝理由
- 只更新方案，不输出代码修改

输出给用户的下一步动作时，还应明确要求：

1. 对已成立且在方案层面已处理的问题，将其从 `open` 移到 `resolved`
2. 对不成立的问题，将其从 `open` 移到 `rejected`
3. 把 Agent A 的完整修订回复写回 `battle/sessions/<pk_id>/state.json` 的 `last_implement_output`
4. 再运行 `/gm:gm-pk <pk_id>` 进入下一轮 challenge，或运行 `/gm:gm-pk <pk_id> stop` 提前进入 judge

### 情况 C：当前是 `revise`，且没有 `stop`

将 battle 推到下一轮 challenge：

- `current_round` 加 1
- `current_stage` 更新为 `challenge`
- `current_actor` 更新为 `agent_b`

然后基于新的轮次和当前 `last_implement_output`，生成下一轮 challenge prompt。

### 情况 D：用户带了 `stop` 参数，且当前不是 `judge` / `completed`

无论当前处于 implement、challenge 还是 revise，都可以结束 battle 并进入 judge。

这时应：

- 将 `current_stage` 更新为 `judge`
- 将 `status` 更新为 `judge`
- 将 `current_actor` 更新为 `judge`
- 如果 `battle/sessions/<pk_id>/state.json` 中还没有 `last_judge_output` 字段，应补上并设为空字符串

然后统计：

- `open` 中还有多少未解决问题
- `resolved` 中有多少已解决问题

基于这些内容生成一条发给裁判模型的 judge prompt。

这条 prompt 应要求裁判给出：

1. 方案是否可接受
2. 剩余风险
3. 建议的后续行动

### 情况 E：当前是 `judge`

先检查 `last_judge_output` 是否为空。

如果为空，直接输出：

> `last_judge_output` 为空。请先把裁判模型的输出写入 `battle/sessions/<pk_id>/state.json`，再运行 `/gm:gm-pk`。

然后停止。

如果不为空，说明裁判阶段已经完成收尾，可以把 battle 标记为结束：

- 将 `current_stage` 更新为 `completed`
- 将 `status` 更新为 `completed`
- 将 `current_actor` 更新为 `none`

然后输出 battle 已完成的提示。

### 情况 F：当前是 `completed`

直接输出：

> 这场 battle 已经完成，不需要继续推进。如需查看结果，请读取 `battle/sessions/<pk_id>/state.json`；如需新开一场，请运行 `/gm:gm-battle`。

然后停止。

## 输出格式

默认输出应包含两部分：

```md
# 阶段推进结果

- pk_id：
- 当前轮次：
- 新阶段：
- 当前执行方：

## 下一条 Prompt
<prompt 正文>

## 下一步
1. ...
2. ...
3. ...
```

如果当前阶段不该继续推进，或缺少关键输入，就直接输出阻塞原因和下一步动作，不要输出假的下一条 prompt。

## 关键判断

- 只有 `last_implement_output` 已写入时，才能从 implement 进入 challenge
- 只有 `issues.json` 的 `open` 已写入 Agent B 提出的 `[ISSUE]` 后，才能从 challenge 进入 revise
- 只有 battle 已初始化时，才能推进
- 每次调用只推进一个阶段，不跳步
- 如果没传 `pk_id`，默认读取 `battle/latest.json` 指向的 battle
- `stop` 的作用是提前进入 judge，不是直接标记 completed
- 只有 `last_judge_output` 已写入时，才能从 judge 进入 completed
- revise 之后发起下一轮 challenge 前，应先把 Agent A 的最新方案修订结果写回 `last_implement_output`
- judge 之后还需要在写入裁判输出后再运行一次 `/gm:gm-pk`，才会把状态标记为 completed

## 推荐 prompt 模板

### 发给 Agent B 的 Challenge Prompt

```md
你是 Agent B（挑战者）。

任务背景：{task}
约束：{constraints}
当前是第 {current_round} 轮。

Agent A 的方案：
{last_implement_output}

这是一场纯方案评审 battle。你只审核方案质量，不允许编写、修改或建议提交任何代码。

请从以下角度提出挑战：
1. 正确性问题
2. 安全性问题
3. 性能问题
4. 边界情况

对每个问题标注严重程度：high / medium / low
格式：[ISSUE] 严重程度: high/medium/low | 标题: xxx | 描述: xxx
```

拿到 Agent B 回复后，应将这些问题写入 `battle/sessions/<pk_id>/issues.json` 的 `open` 数组。建议每项至少保留：

```json
{
  "id": "ISSUE-001",
  "title": "xxx",
  "severity": "high",
  "description": "xxx",
  "raised_by": "agent_b",
  "round": 1
}
```

### 发给 Agent A 的 Revise Prompt

```md
你是 Agent A（方案提出者）。

任务背景：{task}
这是第 {current_round} 轮方案修订。

Agent B 提出的待解决问题：
{open_issues_numbered_list}

这是一场纯方案评审 battle。你只允许修订方案，不允许编写、修改或提交任何代码。

请针对每个问题：
1. 给出方案层面的修订（如果问题成立）
2. 或说明为何该问题不成立（rejected）
```

拿到 Agent A 回复后，应同步更新状态：

1. 已在方案层面处理的问题：从 `open` 移到 `resolved`
2. 不成立的问题：从 `open` 移到 `rejected`
3. 将 Agent A 的完整修订输出写入 `battle/sessions/<pk_id>/state.json` 的 `last_implement_output`

### 发给裁判的 Judge Prompt

```md
请作为裁判，综合以下信息给出最终评审：

任务：{task}
约束：{constraints}
共进行了 {current_round} 轮。

未解决的问题（{open_count} 个）：
{open_issues_list}

已解决的问题（{resolved_count} 个）：
{resolved_issues_list}

请给出：
1. 方案是否可接受
2. 剩余风险
3. 建议的后续行动
```

拿到裁判回复后，应将完整输出写入 `battle/sessions/<pk_id>/state.json` 的 `last_judge_output`，再运行一次 `/gm:gm-pk` 完成收尾。

## 约束

- 不要替用户发送 prompt 给任何模型
- 不要一次推进多个阶段
- 不要在 battle 未初始化时继续假设执行
- 不要忽略空的 `last_implement_output`
- 不要绕过 `battle/sessions/<pk_id>/issues.json` 直接编造问题列表
- 不要在 judge 之前提前标记 completed
- 不要让任何 Agent 在 battle 中编写或修改代码

## 默认风格

保持直接、清楚、偏操作手册式，但不要写成生硬脚本。

目标是让用户在每一步都明确知道：

- 当前操作的是哪一个 `pk_id`
- 现在 battle 处于哪个阶段
- 下一条 prompt 应该发给谁
- 状态文件应该怎么更新
- 什么时候该继续，什么时候该停
