function extractJsonBlock(text) {
  const fencedMatch = text.match(/```json\s*([\s\S]*?)```/i);
  const candidate = fencedMatch ? fencedMatch[1] : text;
  const objectMatch = candidate.match(/\{[\s\S]*\}/);

  if (!objectMatch) {
    return null;
  }

  try {
    return JSON.parse(objectMatch[0]);
  } catch (error) {
    return null;
  }
}

function buildGeneratorPrompt(context) {
  const contractSection = context.contractText
    ? `Current contract (${context.contractPath}):\n${context.contractText}\n`
    : "Current contract: none\n";

  return [
    "You are the generator phase of a local project harness.",
    "Work in the current repository and implement the smallest complete set of changes that satisfy the spec, project rules, and current contract.",
    "Do not ask the user follow-up questions. If something is ambiguous, choose the smallest safe implementation and record the assumption in notes.",
    "Read the repository, edit files if needed, and run the smallest relevant verification commands.",
    "At the end, respond with a single JSON object in a ```json fenced block.",
    "The JSON schema is:",
    "{",
    '  "summary": "string",',
    '  "files_changed": ["relative/path"],',
    '  "commands_run": ["command"],',
    '  "notes": "string"',
    "}",
    "",
    `Spec (${context.specPath}):`,
    context.specText,
    "",
    `Project rules (${context.rulesPath}):`,
    context.rulesText,
    "",
    contractSection
  ].join("\n");
}

async function runGenerator({ client, context, runtimeConfig }) {
  const prompt = buildGeneratorPrompt(context);
  const phaseResult = await client.runPrompt({
    phaseName: "generator",
    prompt,
    approvalPolicy: runtimeConfig.generator.approvalPolicy,
    sandbox: runtimeConfig.generator.sandbox
  });
  const parsed = extractJsonBlock(phaseResult.agentText) || {
    summary: "Generator completed but did not return a parseable JSON payload.",
    files_changed: [...new Set(phaseResult.fileChanges.map((change) => change.path).filter(Boolean))],
    commands_run: [...new Set(phaseResult.commands.map((entry) => entry.command).filter(Boolean))],
    notes: phaseResult.agentText.slice(0, 2000)
  };

  return {
    raw: phaseResult,
    parsed
  };
}

module.exports = {
  runGenerator
};
