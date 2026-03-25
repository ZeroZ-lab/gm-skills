# Battle Arena Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create two Claude Code skills (`gm-battle` and `gm-pk`) that implement a stateful round-based AI review arena where two different models debate a design/implementation.

**Architecture:** Pure SKILL.md files with no CLI or model API. State is persisted in `battle/state.json` and `battle/issues.json`. `gm-battle` initializes a session; `gm-pk` reads state and advances the round, generating the next prompt for the appropriate agent.

**Tech Stack:** Markdown SKILL.md files, JSON state files, Claude Code plugin system (`/gm:<skill>` invocation).

---

## File Map

| File | Action | Responsibility |
|------|--------|----------------|
| `skills/gm-battle/SKILL.md` | Create | Initialize battle session, write state files, output first implement prompt |
| `skills/gm-pk/SKILL.md` | Create | Read state, advance stage, generate next-step prompt, update state |
| `battle/state.json` | Create | Placeholder state file (overwritten by gm-battle at runtime) |
| `battle/issues.json` | Create | Placeholder issues file (overwritten by gm-battle at runtime) |

---

### Task 1: Create placeholder state files

**Files:**
- Create: `battle/state.json`
- Create: `battle/issues.json`

- [ ] **Step 1: Create `battle/state.json` placeholder**

```json
{
  "title": "",
  "task": "",
  "constraints": "",
  "current_round": 1,
  "current_stage": "implement",
  "current_actor": "agent_a",
  "status": "in_progress",
  "last_implement_output": ""
}
```

- [ ] **Step 2: Create `battle/issues.json` placeholder**

```json
{
  "open": [],
  "resolved": [],
  "rejected": []
}
```

- [ ] **Step 3: Commit**

```bash
git add battle/state.json battle/issues.json
git commit -m "feat: add battle state file placeholders"
```

---

### Task 2: Create `gm-battle` skill

**Files:**
- Create: `skills/gm-battle/SKILL.md`

- [ ] **Step 1: Create `skills/gm-battle/SKILL.md`**

```markdown
---
name: gm-battle
description: Initialize a new AI review battle session between two models. Creates state files and outputs the first implement prompt for Agent A.
argument-hint: "[task description]"
---

# gm-battle

You are initializing a new AI review battle (arena) session.

## Step 1: Collect inputs

Ask the user for the following (one at a time if not already provided):

1. **Task** — What should Agent A implement or design? (required)
2. **Constraints** — Any constraints, requirements, or context Agent A must follow? (optional, default: "none")

## Step 2: Write state files

Write `battle/state.json` with this exact content (substitute values):

```json
{
  "title": "<short title derived from task>",
  "task": "<task from user>",
  "constraints": "<constraints from user, or 'none'>",
  "current_round": 1,
  "current_stage": "implement",
  "current_actor": "agent_a",
  "status": "in_progress",
  "last_implement_output": ""
}
```

Write `battle/issues.json` with this exact content:

```json
{
  "open": [],
  "resolved": [],
  "rejected": []
}
```

## Step 3: Output the implement prompt

Tell the user:

---

**Battle initialized. Send this prompt to Agent A (your chosen model):**

---

你是 Agent A（实现者）。

任务：<task>
约束：<constraints>

请提供你的实现方案，包括：
1. 方案概述
2. 关键设计决策
3. 潜在风险（如果有）

---

**After Agent A responds:**

1. Copy Agent A's full output
2. Open `battle/state.json` and paste the output into the `last_implement_output` field (as a JSON string — escape any quotes)
3. Run `/gm:gm-pk` to advance to the challenge stage
```

- [ ] **Step 2: Verify the file was created correctly**

Check that `skills/gm-battle/SKILL.md` exists and has the correct frontmatter (`name: gm-battle`).

- [ ] **Step 3: Commit**

```bash
git add skills/gm-battle/SKILL.md
git commit -m "feat: add gm-battle skill"
```

---

### Task 3: Create `gm-pk` skill

**Files:**
- Create: `skills/gm-pk/SKILL.md`

- [ ] **Step 1: Create `skills/gm-pk/SKILL.md` — frontmatter and guard**

```markdown
---
name: gm-pk
description: Advance the current battle session to the next stage. Reads battle/state.json and generates the next prompt for the appropriate agent. Use "gm-pk stop" to trigger the judge phase.
argument-hint: "[stop]"
---

# gm-pk

You are advancing the current AI review battle session.

## Step 0: Guard — check state file exists

Read `battle/state.json`. If the file does not exist or is empty, output:

> `battle/state.json` not found. Please run `/gm:gm-battle` first to initialize a battle.

Then stop.

## Step 1: Read current state

Read `battle/state.json` and `battle/issues.json`.

Note the values of:
- `current_stage`
- `current_round`
- `current_actor`
- `task`
- `constraints`
- `last_implement_output`
- `status`

Also note whether the user invoked this skill with the argument `stop`.
```

- [ ] **Step 2: Append stage logic — implement → challenge**

Append to `skills/gm-pk/SKILL.md`:

```markdown
## Step 2: Advance based on current stage

### If `current_stage` is `"implement"` (and no `stop` argument)

Check `last_implement_output`. If it is empty or blank, output:

> `last_implement_output` in `battle/state.json` is empty. Please paste Agent A's output into that field before running `/gm:gm-pk`.

Then stop.

Update `battle/state.json`:
- `current_stage` → `"challenge"`
- `current_actor` → `"agent_b"`

Output:

---

**Stage advanced to: CHALLENGE (Round <current_round>)**

Send this prompt to Agent B (a different model than Agent A):

---

你是 Agent B（挑战者）。

任务背景：<task>
约束：<constraints>
当前是第 <current_round> 轮。

Agent A 的方案：
<last_implement_output>

请从以下角度提出挑战：
1. 正确性问题
2. 安全性问题
3. 性能问题
4. 边界情况

对每个问题标注严重程度：high / medium / low
格式：[ISSUE] 严重程度: high/medium/low | 标题: xxx | 描述: xxx

---

**After Agent B responds:**

1. Open `battle/issues.json`
2. Add each `[ISSUE]` Agent B raised to the `open` array in this format:
   ```json
   { "id": "ISSUE-00N", "title": "...", "severity": "high/medium/low", "raised_by": "agent_b", "round": <current_round> }
   ```
3. Run `/gm:gm-pk` to advance to the revise stage
```

- [ ] **Step 3: Append stage logic — challenge → revise**

Append to `skills/gm-pk/SKILL.md`:

```markdown
### If `current_stage` is `"challenge"` (and no `stop` argument)

Read the `open` array from `battle/issues.json`. Format it as a numbered list:
```
1. [ISSUE-001] (high) Title: xxx — Description: xxx
2. [ISSUE-002] (medium) Title: xxx — Description: xxx
...
```

Update `battle/state.json`:
- `current_stage` → `"revise"`
- `current_actor` → `"agent_a"`

Output:

---

**Stage advanced to: REVISE (Round <current_round>)**

Send this prompt to Agent A:

---

你是 Agent A（实现者）。

任务背景：<task>
这是第 <current_round> 轮修正。

Agent B 提出的待解决问题：
<numbered issues list>

请针对每个问题：
1. 给出修正方案（如果问题成立）
2. 或说明为何该问题不成立（rejected）

---

**After Agent A responds:**

1. For each issue Agent A resolved: move it from `open` to `resolved` in `battle/issues.json`
2. For each issue Agent A rejected: move it from `open` to `rejected`
3. Paste Agent A's full revised output into `battle/state.json` → `last_implement_output`
4. Run `/gm:gm-pk` to start the next challenge round, or `/gm:gm-pk stop` to end the battle
```

- [ ] **Step 4: Append stage logic — revise → next challenge, and stop → judge**

Append to `skills/gm-pk/SKILL.md`:

```markdown
### If `current_stage` is `"revise"` (and no `stop` argument)

Update `battle/state.json`:
- `current_round` → `current_round + 1`
- `current_stage` → `"challenge"`
- `current_actor` → `"agent_b"`

Then generate the challenge prompt exactly as in the `implement → challenge` branch above (using the updated round number and current `last_implement_output`).

---

### If `stop` argument is present (any stage except `judge`/`completed`)

Update `battle/state.json`:
- `current_stage` → `"judge"`
- `status` → `"judge"`

Read `battle/issues.json`. Count open and resolved issues.

Output:

---

**Battle stopped. Send this judge prompt to any model:**

---

请作为裁判，综合以下信息给出最终评审：

任务：<task>
约束：<constraints>
共进行了 <current_round> 轮。

未解决的问题（<open_count> 个）：
<open issues list>

已解决的问题（<resolved_count> 个）：
<resolved issues list>

请给出：
1. 方案是否可接受
2. 剩余风险
3. 建议的后续行动

---

After receiving the judge's verdict, run `/gm:gm-pk` one more time to mark the battle as completed.

---

### If `current_stage` is `"judge"`

Update `battle/state.json`:
- `current_stage` → `"completed"`
- `status` → `"completed"`

Output:

> Battle completed. The session has been marked as finished.
```

- [ ] **Step 5: Verify the file**

Read `skills/gm-pk/SKILL.md` and confirm:
- Frontmatter has `name: gm-pk`
- All 5 stage branches are present: implement→challenge, challenge→revise, revise→challenge, stop→judge, judge→completed
- Guard clause for missing state.json is present

- [ ] **Step 6: Commit**

```bash
git add skills/gm-pk/SKILL.md
git commit -m "feat: add gm-pk skill for battle round advancement"
```

---

### Task 4: End-to-end verification

- [ ] **Step 1: Verify plugin loads both skills**

Run `/gm:gm-battle` in Claude Code. Confirm the skill activates and asks for task input.

- [ ] **Step 2: Initialize a test battle**

Provide a simple task (e.g., "设计一个用户登录 API"). Confirm:
- `battle/state.json` is written with `current_stage: "implement"`
- `battle/issues.json` is written with empty arrays
- An implement prompt is displayed

- [ ] **Step 3: Simulate Agent A output**

Manually edit `battle/state.json` → set `last_implement_output` to a short fake plan string.

- [ ] **Step 4: Run `/gm:gm-pk` — implement → challenge**

Confirm:
- `state.json` updated: `current_stage: "challenge"`, `current_actor: "agent_b"`
- Challenge prompt is displayed with the fake implement output embedded

- [ ] **Step 5: Simulate Agent B issues**

Manually edit `battle/issues.json` → add one fake issue to `open`.

- [ ] **Step 6: Run `/gm:gm-pk` — challenge → revise**

Confirm:
- `state.json` updated: `current_stage: "revise"`, `current_actor: "agent_a"`
- Revise prompt shows the issue from issues.json

- [ ] **Step 7: Simulate Agent A revision**

Update `last_implement_output` with a revised fake plan. Move the issue from `open` to `resolved` in issues.json.

- [ ] **Step 8: Run `/gm:gm-pk` — revise → challenge round 2**

Confirm:
- `current_round` incremented to 2
- `current_stage: "challenge"`

- [ ] **Step 9: Run `/gm:gm-pk stop`**

Confirm:
- `status: "judge"`
- Judge prompt is displayed with issue counts

- [ ] **Step 10: Run `/gm:gm-pk` — judge → completed**

Confirm:
- `status: "completed"`
- Completion message displayed

- [ ] **Step 11: Re-init test**

Run `/gm:gm-battle` again with a new task. Confirm state.json and issues.json are fully overwritten.

- [ ] **Step 12: Missing state guard test**

Delete `battle/state.json`. Run `/gm:gm-pk`. Confirm error message is shown.
