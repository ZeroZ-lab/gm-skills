import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(scriptDir, "..");
const pluginsDir = path.join(rootDir, "plugins");
const repoUrl = "https://github.com/ZeroZ-lab/gm-skills";

async function readJson(relativePath) {
  return JSON.parse(await fs.readFile(path.join(rootDir, relativePath), "utf8"));
}

async function writeJson(relativePath, value) {
  const filePath = path.join(rootDir, relativePath);
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, `${JSON.stringify(value, null, 2)}\n`);
}

async function listPluginNames() {
  const entries = await fs.readdir(pluginsDir, { withFileTypes: true });
  return entries
    .filter((entry) => entry.isDirectory() && !entry.name.startsWith("."))
    .map((entry) => entry.name)
    .sort();
}

// External (upstream-maintained) plugins are registered in a separate manifest.
// Each entry has an optional `markets` array ("claude" and/or "codex") controlling
// which marketplace lists it. Omitting `markets` defaults to ["claude"].
// `source` uses the official object form (e.g. { source: "github", repo: "owner/repo" }).
async function readExternalPlugins() {
  try {
    return await readJson(".claude-plugin/external-plugins.json");
  } catch {
    return [];
  }
}

function inMarket(plugin, market) {
  const markets = Array.isArray(plugin.markets) ? plugin.markets : ["claude"];
  return markets.includes(market);
}

function pluginHomepage(pluginName) {
  return `${repoUrl}/tree/main/plugins/${pluginName}`;
}

function codexCategory(manifest) {
  return manifest.interface?.category || "Productivity";
}

// Local plugins choose their marketplaces via an optional `markets` array in their
// Claude manifest (["claude"], ["codex"], or both). Omitting it defaults to
// ["claude"] — this repo publishes Claude Code plugins; a plugin only reaches the
// Codex marketplace by explicitly opting in with "codex" in `markets`.
function localMarkets(claudeManifest) {
  return Array.isArray(claudeManifest.markets) ? claudeManifest.markets : ["claude"];
}

const pkg = await readJson("package.json");
const pluginNames = await listPluginNames();
const externalPlugins = await readExternalPlugins();
const claudeLocalEntries = [];
const codexLocalEntries = [];

for (const pluginName of pluginNames) {
  const claudePath = `plugins/${pluginName}/.claude-plugin/plugin.json`;
  const codexPath = `plugins/${pluginName}/.codex-plugin/plugin.json`;
  const claudeManifest = await readJson(claudePath);
  const markets = localMarkets(claudeManifest);
  const inClaude = markets.includes("claude");
  const inCodex = markets.includes("codex");

  claudeManifest.name = pluginName;
  claudeManifest.version = pkg.version;
  await writeJson(claudePath, claudeManifest);

  let codexManifest = null;
  if (inCodex) {
    const codexManifestExists = await fs
      .access(path.join(rootDir, codexPath))
      .then(() => true)
      .catch(() => false);
    if (!codexManifestExists) {
      throw new Error(`${pluginName} lists "codex" in markets but ${codexPath} is missing`);
    }
    codexManifest = await readJson(codexPath);
    codexManifest.name = pluginName;
    codexManifest.version = pkg.version;
    await writeJson(codexPath, codexManifest);
  }

  if (inClaude) {
    claudeLocalEntries.push({
      name: pluginName,
      description: claudeManifest.description || codexManifest?.description || pluginName,
      homepage: claudeManifest.homepage || pluginHomepage(pluginName)
    });
  }
  if (inCodex) {
    codexLocalEntries.push({ name: pluginName, category: codexCategory(codexManifest) });
  }
}

// Local plugins first, then external (upstream-maintained) entries for each market.
const externalClaudeEntries = externalPlugins
  .filter((plugin) => inMarket(plugin, "claude"))
  .map((plugin) => ({
    name: plugin.name,
    description: plugin.description,
    homepage: plugin.homepage,
    source: plugin.source
  }));

// Codex external entries need a policy/category wrapper to match the local shape.
const externalCodexEntries = externalPlugins
  .filter((plugin) => inMarket(plugin, "codex"))
  .map((plugin) => ({
    name: plugin.name,
    source: plugin.source,
    policy: {
      installation: "AVAILABLE",
      authentication: "ON_INSTALL"
    },
    category: plugin.category || "Productivity"
  }));

await writeJson(".claude-plugin/marketplace.json", {
  name: "gm-skills",
  description: "ZeroZ-lab agent plugin marketplace for design, writing, agent workflow, and visual explanation tools.",
  owner: {
    name: "ZeroZ-lab"
  },
  homepage: repoUrl,
  plugins: [
    ...claudeLocalEntries.map((plugin) => ({
      name: plugin.name,
      description: plugin.description,
      homepage: plugin.homepage,
      source: `./plugins/${plugin.name}`
    })),
    ...externalClaudeEntries
  ]
});

await writeJson(".agents/plugins/marketplace.json", {
  name: "gm-skills",
  interface: {
    displayName: "gm-skills Marketplace"
  },
  plugins: [
    ...codexLocalEntries.map((plugin) => ({
      name: plugin.name,
      source: {
        source: "local",
        path: `./plugins/${plugin.name}`
      },
      policy: {
        installation: "AVAILABLE",
        authentication: "ON_INSTALL"
      },
      category: plugin.category
    })),
    ...externalCodexEntries
  ]
});

const claudeExternal = externalPlugins.filter((p) => inMarket(p, "claude")).length;
const codexExternal = externalPlugins.filter((p) => inMarket(p, "codex")).length;
console.log(
  `Synced ${claudeLocalEntries.length} Claude local, ${codexLocalEntries.length} Codex local, ${claudeExternal} Claude external, ${codexExternal} Codex external plugin(s) into marketplaces.`
);
