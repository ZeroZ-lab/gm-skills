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

function pluginHomepage(pluginName) {
  return `${repoUrl}/tree/main/plugins/${pluginName}`;
}

function codexCategory(manifest) {
  return manifest.interface?.category || "Productivity";
}

const pkg = await readJson("package.json");
const pluginNames = await listPluginNames();
const marketplaceEntries = [];

for (const pluginName of pluginNames) {
  const claudePath = `plugins/${pluginName}/.claude-plugin/plugin.json`;
  const codexPath = `plugins/${pluginName}/.codex-plugin/plugin.json`;
  const claudeManifest = await readJson(claudePath);
  const codexManifest = await readJson(codexPath);

  claudeManifest.name = pluginName;
  claudeManifest.version = pkg.version;
  codexManifest.name = pluginName;
  codexManifest.version = pkg.version;

  await writeJson(claudePath, claudeManifest);
  await writeJson(codexPath, codexManifest);

  marketplaceEntries.push({
    name: pluginName,
    description: claudeManifest.description || codexManifest.description || pluginName,
    homepage: claudeManifest.homepage || pluginHomepage(pluginName),
    category: codexCategory(codexManifest)
  });
}

await writeJson(".claude-plugin/marketplace.json", {
  name: "gm-skills",
  description: "ZeroZ-lab agent plugin marketplace for design, writing, agent workflow, and visual explanation tools.",
  owner: {
    name: "ZeroZ-lab"
  },
  homepage: repoUrl,
  plugins: marketplaceEntries.map((plugin) => ({
    name: plugin.name,
    description: plugin.description,
    homepage: plugin.homepage,
    source: `./plugins/${plugin.name}`
  }))
});

await writeJson(".agents/plugins/marketplace.json", {
  name: "gm-skills",
  interface: {
    displayName: "gm-skills Marketplace"
  },
  plugins: marketplaceEntries.map((plugin) => ({
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
  }))
});

console.log(`Synced ${pluginNames.length} plugin manifests and marketplaces.`);
