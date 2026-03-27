const { runHarness } = require("./runner");
const { createConsoleReporter } = require("../runtime/console-reporter");

async function runHarnessCli() {
  const reporter = createConsoleReporter();
  const result = await runHarness({
    onStructuredEvent: reporter.onEvent
  });
  const reportPath = result && result.reportPath ? result.reportPath : "(unknown report path)";
  process.stdout.write(`harness run completed: ${reportPath}\n`);
}

module.exports = {
  runHarnessCli
};
