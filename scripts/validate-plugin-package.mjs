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

// External (upstream-maintained) plugins. Each entry opts into markets via `markets`
// (["claude"], ["codex"], or both); omitting `markets` defaults to ["claude"].
let externalPlugins = [];
try {
  externalPlugins = await readJson(".claude-plugin/external-plugins.json");
} catch {
  externalPlugins = [];
}

function inMarket(plugin, market) {
  const markets = Array.isArray(plugin.markets) ? plugin.markets : ["claude"];
  return markets.includes(market);
}

const claudeExternal = externalPlugins.filter((p) => inMarket(p, "claude"));
const codexExternal = externalPlugins.filter((p) => inMarket(p, "codex"));

assert(Array.isArray(claudeMarketplace.plugins), "Claude marketplace plugins must be an array");
assert(Array.isArray(codexMarketplace.plugins), "Codex marketplace plugins must be an array");
assert(Array.isArray(externalPlugins), "external-plugins.json must be an array");
assert(
  claudeMarketplace.plugins?.length === pluginNames.length + claudeExternal.length,
  "Claude marketplace plugin count matches local plugins + Claude external plugins"
);
assert(
  codexMarketplace.plugins?.length === pluginNames.length + codexExternal.length,
  "Codex marketplace plugin count matches local plugins + Codex external plugins"
);

function assertValidSource(source, label) {
  assert(
    typeof source === "object" && source !== null,
    `${label} source must be an object (github/url/git-subdir)`
  );
  assert(
    typeof source.source === "string" && source.source.length > 0,
    `${label} source.source must be a non-empty string`
  );
  // GitHub sources require an owner/repo string; url/git-subdir require a url.
  if (source.source === "github") {
    assert(
      typeof source.repo === "string" && /^[^/]+\/[^/]+$/.test(source.repo),
      `${label} github source.repo must be in owner/repo form`
    );
  } else if (source.source === "url" || source.source === "git-subdir") {
    assert(typeof source.url === "string", `${label} ${source.source} source.url is required`);
  } else {
    assert(false, `${label} source.source "${source.source}" is unsupported`);
  }
}

for (const external of externalPlugins) {
  const label = `External plugin ${external.name}`;
  assert(typeof external.name === "string" && external.name.length > 0, `${label} has a name`);
  assert(!pluginNames.includes(external.name), `${label} must not collide with a local plugin name`);
  assert(typeof external.description === "string", `${label} has a description`);
  assertValidSource(external.source, label);

  if (inMarket(external, "claude")) {
    const claudeEntry = claudeMarketplace.plugins?.find((plugin) => plugin.name === external.name);
    assert(Boolean(claudeEntry), `${label} exists in Claude marketplace`);
    assert(
      JSON.stringify(claudeEntry?.source) === JSON.stringify(external.source),
      `${label} Claude marketplace source matches external-plugins.json`
    );
  }
  if (inMarket(external, "codex")) {
    const codexEntry = codexMarketplace.plugins?.find((plugin) => plugin.name === external.name);
    assert(Boolean(codexEntry), `${label} exists in Codex marketplace`);
    assert(
      JSON.stringify(codexEntry?.source) === JSON.stringify(external.source),
      `${label} Codex marketplace source matches external-plugins.json`
    );
  }
}

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

console.log(
  `Plugin package validation passed for ${pluginNames.length} local + ${claudeExternal.length} Claude external + ${codexExternal.length} Codex external plugin(s).`
);
