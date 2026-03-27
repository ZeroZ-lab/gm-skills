# File Templates

只有在用户明确要求文件级模板、字段定义或 `resources` 细化规则时，才读取本文件。

默认假设这些文件都创建在目标项目根目录内：

```text
<project>/
├─ harness/
└─ .harness/
```

## `harness/` 最小文件集

```text
harness/
├─ orchestrator/
│  ├─ main.py
│  ├─ runner.py
│  └─ state_machine.py
├─ agents/
│  ├─ generator/
│  │  ├─ prompt.md
│  │  ├─ schema.json
│  │  └─ agent.py
│  └─ evaluator/
│     ├─ prompt.md
│     ├─ schema.json
│     └─ agent.py
├─ tools/
│  ├─ registry.py
│  ├─ files.py
│  ├─ shell.py
│  ├─ tests.py
│  └─ browser.py
├─ state/
│  ├─ run_state.json
│  └─ checkpoints/
├─ logs/
│  ├─ events.jsonl
│  └─ tool_calls.jsonl
└─ configs/
   ├─ models.yaml
   └─ runtime.yaml
```

## `harness/orchestrator/`

### `main.py`

入口文件，只负责启动一轮流程：

- 读取项目路径
- 读取 `.harness/spec.md`
- 读取 `.harness/project-rules.md`
- 读取 `harness/state/run_state.json`
- 判断当前该调用谁
- 执行一轮
- 写回状态

### `runner.py`

真正跑流程的导演层，最少包括：

- `run_once(project_path)`
- `run_generator(project_path)`
- `run_evaluator(project_path)`
- `handle_pass(project_path)`
- `handle_fail(project_path)`

### `state_machine.py`

只放状态流转规则，不写 prompt、不写业务逻辑。

```python
ALLOWED_TRANSITIONS = {
    "idle": ["generating"],
    "generating": ["evaluating", "failed"],
    "evaluating": ["done", "generating", "failed"],
    "failed": ["generating"],
}
```

## `harness/agents/`

每个 agent 最少 3 个文件：

- `prompt.md`：角色、目标、禁止项
- `schema.json`：输出结构
- `agent.py`：组装上下文、调用模型、校验输出

### `generator/prompt.md`

必须明确：

- 当前 sprint 是什么
- 必须读取 `.harness/spec.md`
- 必须读取 `.harness/project-rules.md`
- 如果存在，再读取当前 contract / relevant resources
- 可以改文件、跑命令
- 不得无证据宣告完成

### `generator/schema.json`

第一版只要求：

```json
{
  "type": "object",
  "properties": {
    "summary": { "type": "string" },
    "files_changed": {
      "type": "array",
      "items": { "type": "string" }
    },
    "commands_run": {
      "type": "array",
      "items": { "type": "string" }
    },
    "notes": { "type": "string" }
  },
  "required": ["summary", "files_changed"]
}
```

### `evaluator/prompt.md`

必须明确：

- 你不是生成者
- 你要独立检查 `spec.md` 和 `project-rules.md`
- 如果当前有 contract，再检查当前 contract
- 你要检查 rules、测试证据和实际行为
- 不能因为“差不多”就判通过

### `evaluator/schema.json`

```json
{
  "type": "object",
  "properties": {
    "status": { "type": "string", "enum": ["pass", "fail"] },
    "issues": {
      "type": "array",
      "items": { "type": "string" }
    },
    "required_fixes": {
      "type": "array",
      "items": { "type": "string" }
    },
    "evidence": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "required": ["status", "issues"]
}
```

## `harness/tools/`

### `registry.py`

定义按角色分配的工具，不要把权限散落到各处。

```python
TOOLS_BY_ROLE = {
    "generator": ["read_file", "write_file", "run_shell", "run_tests"],
    "evaluator": ["read_file", "run_tests", "browser_check"],
}
```

### `files.py`

放文件工具：

- `read_file`
- `write_file`
- `list_files`
- `search_files`

### `shell.py`

控制命令执行边界：

- 允许命令范围
- 超时
- 输出长度
- destructive command 黑名单

### `tests.py`

复用测试入口：

- `run_unit_tests`
- `run_smoke_tests`
- `run_lint`

### `browser.py`

只在 UI 验收需要时提供：

- `open_local_app`
- `run_playwright_checks`
- `capture_screenshot`

## `harness/state/`

### `run_state.json`

运行状态，不是说明文档。第一版最少字段：

```json
{
  "project_name": "skills-manager",
  "current_phase": "generating",
  "current_sprint": 1,
  "status": "running",
  "last_checkpoint": null,
  "next_action": "run_generator",
  "last_report": null
}
```

### `checkpoints/`

checkpoint 文件最少记录：

- `checkpoint_id`
- `phase`
- `sprint`
- `summary_path`
- `report_path`
- `created_at`

## `.harness/` 最小文件集

### `spec.md`

定义当前项目要让 harness 完成什么，不写运行日志。第一版最少要写清：

- 项目目标
- 当前要交付的范围
- 验收标准
- 不做什么

### `project-rules.md`

定义该项目的长期约束。第一版最少要写清：

- 代码边界
- 可用命令
- 禁止操作
- 测试或验收要求

### `contracts/`

只有任务需要更细粒度拆分时再创建。没有 contract 时，不要为了凑结构而硬建空文件。

### `reports/`

存放 evaluator 的阶段性报告。至少保证每轮能落一份可读结果。

### `summary.md`

可选。用于阶段总结，不是必须输入。

### `resources/`

可选。放参考资料，不放运行状态。

## `harness/logs/`

### `events.jsonl`

记录流程事件：

```json
{"time":"2026-03-27T10:01:00Z","event":"generator_started"}
{"time":"2026-03-27T10:02:00Z","event":"generator_finished"}
```

### `tool_calls.jsonl`

记录工具调用：

```json
{"time":"2026-03-27T10:03:30Z","role":"generator","tool":"read_file","target":"src/App.tsx"}
```

## `harness/configs/`

### `models.yaml`

```yaml
generator:
  model: your-generator-model  # 替换为实际使用的模型
  temperature: 0.4

evaluator:
  model: your-evaluator-model  # 替换为实际使用的模型
  temperature: 0.1
```

### `runtime.yaml`

```yaml
max_retries: 3
auto_checkpoint: true
auto_advance_on_pass: true
```
