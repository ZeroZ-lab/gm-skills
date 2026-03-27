async function handleApprovalRequest({ transport, request, runtimeConfig, reducer }) {
  if (request.method === "item/commandExecution/requestApproval") {
    reducer.recordApproval(request);
    const decision = runtimeConfig.defaultCommandApprovalDecision || "accept";
    transport.emit("structuredEvent", {
      type: "approval_requested",
      phase: reducer.phaseName,
      requestType: "command"
    });
    await transport.respond(
      request.id,
      decision
    );
    transport.emit("structuredEvent", {
      type: "approval_resolved",
      requestType: "command",
      decision
    });
    return true;
  }

  if (request.method === "item/fileChange/requestApproval") {
    reducer.recordApproval(request);
    const decision = runtimeConfig.defaultFileApprovalDecision || "accept";
    transport.emit("structuredEvent", {
      type: "approval_requested",
      phase: reducer.phaseName,
      requestType: "file"
    });
    await transport.respond(
      request.id,
      decision
    );
    transport.emit("structuredEvent", {
      type: "approval_resolved",
      requestType: "file",
      decision
    });
    return true;
  }

  return false;
}

module.exports = {
  handleApprovalRequest
};
