# Codex app-server Node Harness Template

This directory is a copyable `harness/` starter built on `codex app-server`.

It is designed to be copied directly into a project root as:

```text
<project>/
├─ harness/
└─ .harness/
```

## What It Does

One run performs the full closed loop:

1. Read `.harness/spec.md`
2. Read `.harness/project-rules.md`
3. Read the latest `.harness/contracts/sprint-N.md` if present
4. Start `codex app-server`
5. Run a generator phase that can edit code
6. Run an evaluator phase that inspects the result in read-only mode
7. Write a report to `.harness/reports/`
8. Update `harness/state/run_state.json`

## Requirements

- Node.js 18+
- `codex` available in `PATH`
- Project root already contains:
  - `.harness/spec.md`
  - `.harness/project-rules.md`

## Run

默认会在终端里实时持续显示详细进度，包括：

- runId / model / log file
- 阶段切换
- `threadId`
- 审批请求与自动决策
- 命令执行结果
- agent 增量输出摘要
- report 路径和最终状态

From the copied `harness/` directory:

```bash
npm run harness:run
```

If you prefer running from the project root:

```bash
cd harness && npm run harness:run
```

Or run the harness directly from the project root:

```bash
node harness
```

## Key Files

- `orchestrator/main.js` - entrypoint
- `index.js` - root entrypoint for `node harness`
- `orchestrator/runner.js` - closed-loop runner
- `runtime/console-reporter.js` - real-time terminal display
- `runtime/app-server-client.js` - `codex app-server` client
- `runtime/approval-handler.js` - command and file approval responses
- `agents/generator.js` - implementation phase prompt
- `agents/evaluator.js` - evaluation phase prompt
- `tools/report-writer.js` - writes `.harness/reports/...`

## Notes

- The generator runs with workspace-write access.
- The evaluator runs in read-only mode.
- The template uses only Node built-in modules. No package install step is required.
