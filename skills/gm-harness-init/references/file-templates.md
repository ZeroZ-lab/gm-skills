# File Templates

只有在用户明确要求文件级模板、字段定义或 `resources` 细化规则时，才读取本文件。

默认 `harness/` 实现直接来自：

- `references/codex-app-server-node-template/`

默认假设这些文件都创建在目标项目根目录内：

```text
<project>/
├─ harness/
└─ .harness/
```

## `harness/` 默认文件集

关键目录：

- `harness/orchestrator/`
- `harness/runtime/`
- `harness/agents/`
- `harness/tools/`
- `harness/state/`
- `harness/logs/`
- `harness/config/`

```text
harness/
├─ package.json
├─ orchestrator/
│  ├─ main.js
│  ├─ runner.js
│  └─ state-machine.js
├─ runtime/
│  ├─ app-server-client.js
│  ├─ jsonrpc-transport.js
│  ├─ event-reducer.js
│  └─ approval-handler.js
├─ agents/
│  ├─ generator.js
│  └─ evaluator.js
├─ tools/
│  └─ report-writer.js
├─ state/
│  └─ run_state.json
├─ logs/
│  └─ .gitkeep
└─ config/
   └─ runtime.json
```

## `harness/` 关键职责

- `package.json`：只暴露 `npm run harness:run`
- `orchestrator/main.js`：单入口，触发一轮完整闭环
- `orchestrator/runner.js`：执行 generator -> evaluator -> report -> state update
- `runtime/app-server-client.js`：启动 `codex app-server`，完成 `initialize` / `initialized` / `thread/start` / `turn/start`
- `runtime/approval-handler.js`：处理命令审批和文件审批
- `agents/generator.js`：构造实现阶段 prompt，并解析 JSON 结果
- `agents/evaluator.js`：构造审核阶段 prompt，并解析 JSON 结果
- `tools/report-writer.js`：将结果写入 `.harness/reports/`
- `state/run_state.json`：记录当前阶段和最近一次 report

## 复制规则

- `harness/` 不存在时：先创建，再整目录复制模板
- `harness/` 已存在且非空时：不要覆盖，停下来提示人工决定
- `.harness/` 不存在时：自动创建
- `.harness/` 已存在时：只补缺失文件

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
