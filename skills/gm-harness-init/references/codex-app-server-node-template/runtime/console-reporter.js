function createConsoleReporter() {
  let currentPhase = "idle";
  const agentBuffers = new Map();

  function print(line = "") {
    process.stdout.write(`${line}\n`);
  }

  function stringifyPayload(payload) {
    try {
      return JSON.stringify(payload);
    } catch (error) {
      return String(payload);
    }
  }

  function onEvent(event) {
    switch (event.type) {
      case "run_started":
        print(`[run] started id=${event.runId}`);
        print(`[run] project=${event.projectRoot}`);
        print(`[run] model=${event.model}`);
        print(`[run] log=${event.logFile}`);
        break;

      case "state_changed":
        print(`[state] ${event.from} -> ${event.to}`);
        currentPhase = event.to;
        break;

      case "phase_started":
        print(`[phase] start ${event.phase}`);
        break;

      case "phase_completed":
        print(`[phase] complete ${event.phase} status=${event.status}`);
        break;

      case "app_server_started":
        print("[app-server] started");
        break;

      case "thread_started":
        print(`[thread] ${event.threadId}`);
        break;

      case "turn_started":
        print(`[turn] started phase=${event.phase}`);
        break;

      case "approval_requested":
        print(`[approval] requested type=${event.requestType} phase=${event.phase}`);
        break;

      case "approval_resolved":
        print(`[approval] resolved type=${event.requestType} decision=${event.decision}`);
        break;

      case "command_started":
        print(`[command] start ${event.command}`);
        break;

      case "command_finished":
        print(`[command] finish exit=${event.exitCode} status=${event.status} cmd=${event.command}`);
        break;

      case "file_change_completed":
        print(`[files] changed=${event.count}`);
        break;

      case "agent_text_delta": {
        const phase = event.phase || currentPhase;
        const nextBuffer = (agentBuffers.get(phase) || "") + (event.delta || "");
        const parts = nextBuffer.split("\n");
        const completeLines = parts.slice(0, -1);
        const remainder = parts[parts.length - 1];

        for (const line of completeLines) {
          if (line.trim()) {
            print(`${phase}> ${line}`);
          }
        }

        agentBuffers.set(phase, remainder);
        break;
      }

      case "agent_text_completed": {
        const phase = event.phase || currentPhase;
        const remainder = agentBuffers.get(phase);

        if (remainder && remainder.trim()) {
          print(`${phase}> ${remainder}`);
        }

        agentBuffers.delete(phase);
        break;
      }

      case "report_written":
        print(`[report] ${event.reportPath}`);
        break;

      case "run_failed":
        print(`[run] failed: ${event.error}`);
        break;

      case "run_completed":
        print(`[run] completed status=${event.status}`);
        print(`[run] report=${event.reportPath}`);
        print(`[run] commands=${event.commandsCount} file_changes=${event.fileChangesCount}`);
        if (event.nextAction !== undefined && event.nextAction !== null) {
          print(`[run] next_action=${event.nextAction}`);
        }
        break;

      case "transport_stderr":
        print(`[stderr] ${event.chunk}`.trimEnd());
        break;

      case "transport_parse_error":
        print(`[transport] parse error payload=${stringifyPayload(event.line)}`);
        break;

      default:
        break;
    }
  }

  return {
    onEvent
  };
}

module.exports = {
  createConsoleReporter
};
