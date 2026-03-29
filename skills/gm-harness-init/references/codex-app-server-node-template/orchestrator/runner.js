const fs = require("node:fs/promises");
const path = require("node:path");
const { randomUUID } = require("node:crypto");

const { AppServerClient } = require("../runtime/app-server-client");
const { assertTransition } = require("./state-machine");
const { runGenerator } = require("../agents/generator");
const { runEvaluator } = require("../agents/evaluator");
const { writeRunReport } = require("../tools/report-writer");

function emitStructuredEvent(emit, event) {
  if (typeof emit === "function") {
    emit(event);
  }
}

async function readJson(filePath) {
  const raw = await fs.readFile(filePath, "utf8");
  return JSON.parse(raw);
}

async function readJsonIfExists(filePath, fallback) {
  try {
    return await readJson(filePath);
  } catch (error) {
    if (error && error.code === "ENOENT") {
      return fallback;
    }
    throw error;
  }
}

async function writeJson(filePath, value) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

async function readRequiredText(filePath, label) {
  try {
    return await fs.readFile(filePath, "utf8");
  } catch (error) {
    if (error && error.code === "ENOENT") {
      throw new Error(`missing required ${label}: ${filePath}`);
    }
    throw error;
  }
}

async function findLatestContract(contractsDir) {
  let entries = [];

  try {
    entries = await fs.readdir(contractsDir, { withFileTypes: true });
  } catch (error) {
    if (error && error.code === "ENOENT") {
      return null;
    }
    throw error;
  }

  const candidates = entries
    .filter((entry) => entry.isFile())
    .map((entry) => {
      const match = entry.name.match(/^sprint-(\d+)\.md$/);
      return match ? { name: entry.name, number: Number(match[1]) } : null;
    })
    .filter(Boolean)
    .sort((a, b) => b.number - a.number);

  if (!candidates.length) {
    return null;
  }

  return path.join(contractsDir, candidates[0].name);
}

async function updateState(stateFile, patch) {
  const current = await readJsonIfExists(stateFile, {
    project_name: "",
    current_phase: "idle",
    current_sprint: null,
    status: "idle",
    last_checkpoint: null,
    next_action: "run_generator",
    last_report: null,
    last_error: null
  });

  if (
    patch.current_phase &&
    current.current_phase &&
    patch.current_phase !== current.current_phase
  ) {
    assertTransition(current.current_phase, patch.current_phase);
  }

  const nextState = {
    ...current,
    ...patch
  };

  await writeJson(stateFile, nextState);
  return {
    previousState: current,
    nextState
  };
}

async function runHarness(options = {}) {
  const emit = typeof options.onStructuredEvent === "function"
    ? options.onStructuredEvent
    : () => {};
  const harnessRoot = path.resolve(__dirname, "..");
  const projectRoot = path.resolve(harnessRoot, "..");
  const dotHarnessRoot = path.join(projectRoot, ".harness");
  const runtimeConfig = await readJson(path.join(harnessRoot, "config", "runtime.json"));
  const stateFile = path.join(harnessRoot, "state", "run_state.json");
  const reportDir = path.join(projectRoot, runtimeConfig.reportDir);
  const logsDir = path.join(projectRoot, runtimeConfig.logDir);
  const runId = new Date().toISOString().replace(/[:.]/g, "-") + `-${randomUUID().slice(0, 8)}`;
  const logFile = path.join(logsDir, `${runId}.jsonl`);

  await fs.mkdir(reportDir, { recursive: true });
  await fs.mkdir(logsDir, { recursive: true });

  emitStructuredEvent(emit, {
    type: "run_started",
    runId,
    projectRoot,
    model: runtimeConfig.model,
    logFile
  });

  const client = new AppServerClient({
    runtimeConfig,
    cwd: projectRoot,
    logFile,
    onStructuredEvent: emit
  });

  const specPath = path.join(dotHarnessRoot, "spec.md");
  const rulesPath = path.join(dotHarnessRoot, "project-rules.md");
  const contractsDir = path.join(dotHarnessRoot, "contracts");
  let generatorResult = null;
  let evaluatorResult = null;
  let reportPath = null;
  let context = null;

  const generatingState = await updateState(stateFile, {
    project_name: path.basename(projectRoot),
    current_phase: "generating",
    status: "running",
    next_action: "run_generator",
    last_error: null
  });
  emitStructuredEvent(emit, {
    type: "state_changed",
    from: generatingState.previousState.current_phase,
    to: "generating"
  });
  emitStructuredEvent(emit, {
    type: "phase_started",
    phase: "generator"
  });

  try {
    const specText = await readRequiredText(specPath, "spec");
    const rulesText = await readRequiredText(rulesPath, "project rules");
    const contractPath = await findLatestContract(contractsDir);
    const contractText = contractPath ? await fs.readFile(contractPath, "utf8") : null;

    context = {
      projectRoot,
      dotHarnessRoot,
      specPath,
      rulesPath,
      contractPath,
      specText,
      rulesText,
      contractText
    };

    await client.start();

    generatorResult = await runGenerator({
      client,
      context,
      runtimeConfig
    });
    emitStructuredEvent(emit, {
      type: "phase_completed",
      phase: "generator",
      status: generatorResult.raw.finalStatus || "unknown"
    });

    const evaluatingState = await updateState(stateFile, {
      current_phase: "evaluating",
      status: "running",
      next_action: "run_evaluator",
      last_error: null
    });
    emitStructuredEvent(emit, {
      type: "state_changed",
      from: evaluatingState.previousState.current_phase,
      to: "evaluating"
    });
    emitStructuredEvent(emit, {
      type: "phase_started",
      phase: "evaluator"
    });

    evaluatorResult = await runEvaluator({
      client,
      context,
      generatorResult,
      runtimeConfig
    });
    emitStructuredEvent(emit, {
      type: "phase_completed",
      phase: "evaluator",
      status: evaluatorResult.parsed.status
    });

    reportPath = await writeRunReport({
      reportDir,
      runId,
      generatorResult,
      evaluatorResult
    });
    emitStructuredEvent(emit, {
      type: "report_written",
      reportPath
    });

    if (String(evaluatorResult.parsed.status).toLowerCase() === "pass") {
      const doneState = await updateState(stateFile, {
        current_phase: "done",
        status: "done",
        next_action: null,
        last_report: reportPath,
        last_error: null
      });
      emitStructuredEvent(emit, {
        type: "state_changed",
        from: doneState.previousState.current_phase,
        to: "done"
      });
    } else {
      const failedEvaluationState = await updateState(stateFile, {
        current_phase: "generating",
        status: "failed",
        next_action: "run_generator",
        last_report: reportPath,
        last_error: "evaluation_failed"
      });
      emitStructuredEvent(emit, {
        type: "state_changed",
        from: failedEvaluationState.previousState.current_phase,
        to: "failed"
      });
    }

    emitStructuredEvent(emit, {
      type: "run_completed",
      status: String(evaluatorResult.parsed.status).toLowerCase() === "pass" ? "done" : "failed",
      reportPath,
      commandsCount: generatorResult.raw.commands.length + evaluatorResult.raw.commands.length,
      fileChangesCount: generatorResult.raw.fileChanges.length,
      nextAction: String(evaluatorResult.parsed.status).toLowerCase() === "pass" ? null : "run_generator"
    });

    return {
      reportPath,
      generatorResult,
      evaluatorResult
    };
  } catch (error) {
    reportPath = await writeRunReport({
      reportDir,
      runId,
      generatorResult,
      evaluatorResult,
      error
    });
    emitStructuredEvent(emit, {
      type: "report_written",
      reportPath
    });

    const failedState = await updateState(stateFile, {
      current_phase: "failed",
      status: "failed",
      next_action: "run_generator",
      last_report: reportPath,
      last_error: error.message
    });
    emitStructuredEvent(emit, {
      type: "state_changed",
      from: failedState.previousState.current_phase,
      to: "failed"
    });
    emitStructuredEvent(emit, {
      type: "run_failed",
      error: error.message
    });

    throw error;
  } finally {
    await client.close();
  }
}

module.exports = {
  runHarness
};
