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

function buildEvaluatorPrompt(context, generatorResult) {
  const contractSection = context.contractText
    ? `Current contract (${context.contractPath}):\n${context.contractText}\n`
    : "Current contract: none\n";

  return [
    "You are the evaluator phase of a local project harness.",
    "Inspect the repository in read-only mode. Do not edit files.",
    "Use the spec, project rules, and current contract as the source of truth.",
    "Review the generator outcome, inspect the changed code, and run the smallest relevant read-only checks if useful.",
    "At the end, respond with a single JSON object in a ```json fenced block.",
    "The JSON schema is:",
    "{",
    '  "status": "pass | fail",',
    '  "issues": ["string"],',
    '  "required_fixes": ["string"],',
    '  "evidence": ["string"]',
    "}",
    "",
    `Spec (${context.specPath}):`,
    context.specText,
    "",
    `Project rules (${context.rulesPath}):`,
    context.rulesText,
    "",
    contractSection,
    "Generator output:",
    JSON.stringify(generatorResult.parsed, null, 2)
  ].join("\n");
}

async function runEvaluator({ client, context, generatorResult, runtimeConfig }) {
  const prompt = buildEvaluatorPrompt(context, generatorResult);
  const phaseResult = await client.runPrompt({
    phaseName: "evaluator",
    prompt,
    approvalPolicy: runtimeConfig.evaluator.approvalPolicy,
    sandbox: runtimeConfig.evaluator.sandbox
  });
  const parsed = extractJsonBlock(phaseResult.agentText) || {
    status: "fail",
    issues: ["Evaluator did not return a parseable JSON payload."],
    required_fixes: ["Inspect the raw evaluator output and tighten the evaluator prompt."],
    evidence: [phaseResult.agentText.slice(0, 2000)]
  };

  return {
    raw: phaseResult,
    parsed
  };
}

module.exports = {
  runEvaluator
};
