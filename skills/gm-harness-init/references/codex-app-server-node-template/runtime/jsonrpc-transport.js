const { EventEmitter } = require("node:events");
const { spawn } = require("node:child_process");
const readline = require("node:readline");
const fs = require("node:fs/promises");

class JsonRpcTransport extends EventEmitter {
  constructor(options = {}) {
    super();
    this.command = options.command || "codex";
    this.args = Array.isArray(options.args) ? options.args : ["app-server"];
    this.cwd = options.cwd;
    this.logFile = options.logFile || null;
    this.proc = null;
    this.rl = null;
    this.nextId = 1;
    this.pending = new Map();
    this.onStructuredEvent = typeof options.onStructuredEvent === "function"
      ? options.onStructuredEvent
      : null;
  }

  async start() {
    if (this.proc) {
      return;
    }

    this.proc = spawn(this.command, this.args, {
      cwd: this.cwd,
      stdio: ["pipe", "pipe", "pipe"]
    });

    this.proc.on("error", (error) => {
      for (const { reject } of this.pending.values()) {
        reject(error);
      }

      this.pending.clear();
      this.#emitStructuredEvent({
        type: "run_failed",
        error: `failed to spawn codex app-server: ${error.message}`
      });
      this.emit("close", { code: null, signal: null, error });
    });

    this.proc.stdin.setDefaultEncoding("utf8");
    this.rl = readline.createInterface({ input: this.proc.stdout });

    this.rl.on("line", (line) => {
      void this.#handleLine(line);
    });

    this.proc.stderr.on("data", (chunk) => {
      const text = chunk.toString("utf8");
      this.#emitStructuredEvent({
        type: "transport_stderr",
        chunk: text
      });
      void this.#appendLog({
        direction: "stderr",
        chunk: text
      });
    });

    this.proc.on("close", (code, signal) => {
      const error = new Error(`codex app-server exited (code=${code}, signal=${signal})`);

      for (const { reject } of this.pending.values()) {
        reject(error);
      }

      this.pending.clear();
      this.emit("close", { code, signal });
    });
  }

  async stop() {
    if (!this.proc) {
      return;
    }

    this.rl.close();
    this.proc.kill();
    this.proc = null;
    this.rl = null;
  }

  async request(method, params = {}) {
    const id = this.nextId++;
    const payload = { method, id, params };

    const responsePromise = new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
    });

    await this.#send(payload);
    return responsePromise;
  }

  async notify(method, params = {}) {
    await this.#send({ method, params });
  }

  async respond(id, result) {
    await this.#send({ id, result });
  }

  async respondWithError(id, code, message) {
    await this.#send({
      id,
      error: { code, message }
    });
  }

  async #send(payload) {
    if (!this.proc) {
      throw new Error("transport not started");
    }

    const line = JSON.stringify(payload);
    this.proc.stdin.write(`${line}\n`);
    await this.#appendLog({ direction: "outbound", payload });
  }

  async #handleLine(line) {
    if (!line.trim()) {
      return;
    }

    let message;

    try {
      message = JSON.parse(line);
    } catch (error) {
      await this.#appendLog({
        direction: "parse-error",
        line,
        error: String(error)
      });
      this.#emitStructuredEvent({
        type: "transport_parse_error",
        line,
        error: String(error)
      });
      this.emit("transportError", error);
      return;
    }

    await this.#appendLog({ direction: "inbound", payload: message });

    if (message.id !== undefined && !message.method) {
      const pending = this.pending.get(message.id);

      if (!pending) {
        return;
      }

      this.pending.delete(message.id);

      if (message.error) {
        pending.reject(new Error(message.error.message || "json-rpc request failed"));
      } else {
        pending.resolve(message.result);
      }

      return;
    }

    if (message.method && message.id !== undefined) {
      this.emit("request", message);
      return;
    }

    if (message.method) {
      this.emit("notification", message);
    }
  }

  async #appendLog(entry) {
    if (!this.logFile) {
      return;
    }

    await fs.appendFile(this.logFile, `${JSON.stringify({
      timestamp: new Date().toISOString(),
      ...entry
    })}\n`);
  }

  #emitStructuredEvent(event) {
    if (this.onStructuredEvent) {
      this.onStructuredEvent(event);
    }
  }
}

module.exports = {
  JsonRpcTransport
};
