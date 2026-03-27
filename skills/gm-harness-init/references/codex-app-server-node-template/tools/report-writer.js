const fs = require("node:fs/promises");
const path = require("node:path");

async function writeRunReport({ reportDir, runId, generatorResult, evaluatorResult, error }) {
  await fs.mkdir(reportDir, { recursive: true });

  const reportPath = path.join(reportDir, `${runId}-report.json`);
  const payload = {
    runId,
    createdAt: new Date().toISOString(),
    status: error
      ? "failed"
      : (evaluatorResult && evaluatorResult.parsed ? evaluatorResult.parsed.status : "unknown"),
    generator: generatorResult || null,
    evaluator: evaluatorResult || null,
    error: error
      ? {
          message: error.message,
          stack: error.stack
        }
      : null
  };

  await fs.writeFile(reportPath, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  return reportPath;
}

module.exports = {
  writeRunReport
};
