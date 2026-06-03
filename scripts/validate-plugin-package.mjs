import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(scriptDir, "..");
const pluginsDir = path.join(rootDir, "plugins");

const checks = [];

async function exists(relativePath) {
  try {
    await fs.access(path.join(rootDir, relativePath));
    return true;
  } catch {
    return false;
  }
}

async function readJson(relativePath) {
  return JSON.parse(await fs.readFile(path.join(rootDir, relativePath), "utf8"));
}

async function readText(relativePath) {
  return fs.readFile(path.join(rootDir, relativePath), "utf8");
}

async function listPluginNames() {
  const entries = await fs.readdir(pluginsDir, { withFileTypes: true });
  return entries
    .filter((entry) => entry.isDirectory() && !entry.name.startsWith("."))
    .map((entry) => entry.name)
    .sort();
}

function assert(condition, message) {
  checks.push({ ok: condition, message });
}

function assertAllSkillsUsePrefix(skills, prefix, label) {
  assert(Array.isArray(skills), `${label} must be an array`);
  if (!Array.isArray(skills)) {
    return;
  }
  for (const skillPath of skills) {
    assert(
      typeof skillPath === "string" && skillPath.startsWith(prefix) && !skillPath.includes(".."),
      `${label} entries must stay inside the plugin: ${skillPath}`
    );
  }
}

function hasPathReference(skillText, directoryName) {
  return skillText.includes(`${directoryName}/`);
}

const requiredFiles = [
  ".agents/plugins/marketplace.json",
  ".claude-plugin/marketplace.json",
  "package.json",
  "plugins"
];

for (const relativePath of requiredFiles) {
  assert(await exists(relativePath), `${relativePath} exists`);
}

const pkg = await readJson("package.json");
const claudeMarketplace = await readJson(".claude-plugin/marketplace.json");
const codexMarketplace = await readJson(".agents/plugins/marketplace.json");
const pluginNames = await listPluginNames();

assert(Array.isArray(claudeMarketplace.plugins), "Claude marketplace plugins must be an array");
assert(Array.isArray(codexMarketplace.plugins), "Codex marketplace plugins must be an array");
assert(
  claudeMarketplace.plugins?.length === pluginNames.length,
  "Claude marketplace plugin count matches plugins directory"
);
assert(
  codexMarketplace.plugins?.length === pluginNames.length,
  "Codex marketplace plugin count matches plugins directory"
);

for (const pluginName of pluginNames) {
  const pluginDir = `plugins/${pluginName}`;
  const claudeManifestPath = `${pluginDir}/.claude-plugin/plugin.json`;
  const codexManifestPath = `${pluginDir}/.codex-plugin/plugin.json`;
  const skillDir = `${pluginDir}/skills/${pluginName}`;
  const skillPath = `${skillDir}/SKILL.md`;

  assert(await exists(claudeManifestPath), `${claudeManifestPath} exists`);
  assert(await exists(codexManifestPath), `${codexManifestPath} exists`);
  assert(await exists(skillPath), `${skillPath} exists`);

  const claudeManifest = await readJson(claudeManifestPath);
  const codexManifest = await readJson(codexManifestPath);
  const skillText = await readText(skillPath);

  assert(claudeManifest.name === pluginName, `${pluginName} Claude manifest name matches directory`);
  assert(codexManifest.name === pluginName, `${pluginName} Codex manifest name matches directory`);
  assert(claudeManifest.version === pkg.version, `${pluginName} Claude manifest version matches package.json`);
  assert(codexManifest.version === pkg.version, `${pluginName} Codex manifest version matches package.json`);
  assertAllSkillsUsePrefix(claudeManifest.skills, "./skills/", `${pluginName} Claude manifest skills`);
  assert(
    JSON.stringify(claudeManifest.skills) === JSON.stringify([`./skills/${pluginName}`]),
    `${pluginName} Claude manifest must point to ./skills/${pluginName}`
  );
  assert(codexManifest.skills === "./skills/", `${pluginName} Codex manifest skills must equal "./skills/"`);

  const claudeEntry = claudeMarketplace.plugins?.find((plugin) => plugin.name === pluginName);
  const codexEntry = codexMarketplace.plugins?.find((plugin) => plugin.name === pluginName);

  assert(Boolean(claudeEntry), `${pluginName} exists in Claude marketplace`);
  assert(Boolean(codexEntry), `${pluginName} exists in Codex marketplace`);
  assert(
    claudeEntry?.source === `./plugins/${pluginName}`,
    `${pluginName} Claude marketplace source points at ./plugins/${pluginName}`
  );
  assert(
    codexEntry?.source?.path === `./plugins/${pluginName}`,
    `${pluginName} Codex marketplace source.path points at ./plugins/${pluginName}`
  );

  for (const directoryName of ["references", "examples", "templates"]) {
    if (hasPathReference(skillText, directoryName)) {
      assert(
        (await exists(`${skillDir}/${directoryName}`)) || (await exists(`${pluginDir}/${directoryName}`)),
        `${pluginName} keeps ${directoryName}/ inside the plugin package`
      );
    }
  }
}

const failures = checks.filter((check) => !check.ok);
if (failures.length > 0) {
  console.error("Plugin package validation failed:");
  for (const failure of failures) {
    console.error(`- ${failure.message}`);
  }
  process.exit(1);
}

console.log(`Plugin package validation passed for ${pluginNames.length} plugins.`);
