const { JsonRpcTransport } = require("./jsonrpc-transport");
const { createTurnReducer } = require("./event-reducer");
const { handleApprovalRequest } = require("./approval-handler");

class AppServerClient {
  constructor(options) {
    this.runtimeConfig = options.runtimeConfig;
    this.cwd = options.cwd;
    this.onStructuredEvent = typeof options.onStructuredEvent === "function"
      ? options.onStructuredEvent
      : () => {};
    this.transport = new JsonRpcTransport({
      command: "codex",
      args: ["app-server"],
      cwd: options.cwd,
      logFile: options.logFile,
      onStructuredEvent: this.onStructuredEvent
    });

    this.transport.on("structuredEvent", (event) => {
      this.onStructuredEvent(event);
    });
  }

  async start() {
    await this.transport.start();
    await this.transport.request("initialize", {
      clientInfo: {
        name: "gm_harness_template",
        title: "GM Harness Template",
        version: "0.1.0"
      }
    });
    await this.transport.notify("initialized", {});
    this.onStructuredEvent({ type: "app_server_started" });
  }

  async close() {
    await this.transport.stop();
  }

  async runPrompt({ phaseName, prompt, approvalPolicy, sandbox }) {
    const reducer = createTurnReducer(phaseName);
    const notificationHandler = (message) => {
      reducer.apply(message);

      if (message.method === "item/agentMessage/delta") {
        this.onStructuredEvent({
          type: "agent_text_delta",
          phase: phaseName,
          delta: message.params && typeof message.params.delta === "string"
            ? message.params.delta
            : ""
        });
      }

      if (message.method === "item/completed") {
        const item = message.params ? message.params.item : null;

        if (item && item.type === "commandExecution") {
          this.onStructuredEvent({
            type: "command_finished",
            command: item.command || "",
            exitCode: item.exitCode,
            status: item.status || null
          });
        }

        if (item && item.type === "fileChange") {
          this.onStructuredEvent({
            type: "file_change_completed",
            count: Array.isArray(item.changes) ? item.changes.length : 0
          });
        }

        if (item && item.type === "agentMessage") {
          this.onStructuredEvent({
            type: "agent_text_completed",
            phase: phaseName
          });
        }
      }
    };
    const requestHandler = async (message) => {
      const handled = await handleApprovalRequest({
        transport: this.transport,
        request: message,
        runtimeConfig: this.runtimeConfig,
        reducer
      });

      if (!handled) {
        await this.transport.respondWithError(
          message.id,
          -32601,
          `unsupported server request: ${message.method}`
        );
      }
    };

    this.transport.on("notification", notificationHandler);
    this.transport.on("request", requestHandler);

    try {
      const threadResult = await this.transport.request("thread/start", {
        model: this.runtimeConfig.model,
        cwd: this.cwd,
        approvalPolicy,
        sandbox,
        serviceName: this.runtimeConfig.serviceName
      });
      const threadId = threadResult && threadResult.thread ? threadResult.thread.id : null;

      if (!threadId) {
        throw new Error("thread/start did not return a thread id");
      }

      this.onStructuredEvent({
        type: "thread_started",
        threadId
      });

      const turnCompletion = new Promise((resolve, reject) => {
        const doneHandler = (message) => {
          if (message.method === "turn/completed") {
            cleanup();
            resolve(reducer.result());
          }
        };

        const closeHandler = (event) => {
          cleanup();
          reject(new Error(`transport closed before turn completion: ${JSON.stringify(event)}`));
        };

        const cleanup = () => {
          this.transport.off("notification", doneHandler);
          this.transport.off("close", closeHandler);
        };

        this.transport.on("notification", doneHandler);
        this.transport.on("close", closeHandler);
      });

      await this.transport.request("turn/start", {
        threadId,
        input: [{ type: "text", text: prompt }]
      });

      this.onStructuredEvent({
        type: "turn_started",
        phase: phaseName
      });

      return await turnCompletion;
    } finally {
      this.transport.off("notification", notificationHandler);
      this.transport.off("request", requestHandler);
    }
  }
}

module.exports = {
  AppServerClient
};
