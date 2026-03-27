const { runHarnessCli } = require("./orchestrator/main");

if (require.main === module) {
  runHarnessCli().catch((error) => {
    process.stderr.write(`harness run failed: ${error.message}\n`);
    process.exitCode = 1;
  });
}

module.exports = {
  runHarnessCli
};
