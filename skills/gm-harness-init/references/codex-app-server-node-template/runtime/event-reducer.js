function createTurnReducer(phaseName) {
  return {
    phaseName,
    agentText: "",
    commandOutputs: [],
    commands: [],
    fileChanges: [],
    approvals: [],
    errors: [],
    notifications: [],
    turnStatus: null,
    completed: false,

    apply(message) {
      this.notifications.push(message);

      switch (message.method) {
        case "item/agentMessage/delta": {
          const delta = message.params && typeof message.params.delta === "string"
            ? message.params.delta
            : "";
          this.agentText += delta;
          break;
        }

        case "item/commandExecution/outputDelta": {
          const output = message.params && typeof message.params.delta === "string"
            ? message.params.delta
            : "";
          const itemId = message.params ? message.params.itemId : null;
          this.commandOutputs.push({ itemId, output });
          break;
        }

        case "item/completed": {
          const item = message.params ? message.params.item : null;

          if (!item || typeof item !== "object") {
            break;
          }

          if (item.type === "agentMessage" && typeof item.text === "string") {
            this.agentText = item.text;
          }

          if (item.type === "commandExecution") {
            this.commands.push({
              command: item.command || "",
              cwd: item.cwd || "",
              exitCode: item.exitCode,
              status: item.status || null
            });
          }

          if (item.type === "fileChange" && Array.isArray(item.changes)) {
            this.fileChanges.push(...item.changes);
          }

          break;
        }

        case "error": {
          this.errors.push(message.params || {});
          break;
        }

        case "turn/completed": {
          const turn = message.params ? message.params.turn : null;
          this.turnStatus = turn && turn.status ? turn.status : "unknown";
          this.completed = true;
          break;
        }

        default:
          break;
      }
    },

    recordApproval(message) {
      this.approvals.push({
        method: message.method,
        params: message.params || {}
      });
    },

    result() {
      return {
        phaseName: this.phaseName,
        finalStatus: this.turnStatus,
        agentText: this.agentText,
        commandOutputs: this.commandOutputs,
        commands: this.commands,
        fileChanges: this.fileChanges,
        approvals: this.approvals,
        errors: this.errors,
        notifications: this.notifications
      };
    }
  };
}

module.exports = {
  createTurnReducer
};
