# gm-skills

`gm-skills` is a multi-plugin marketplace monorepo. The root of the repo owns marketplace metadata only; each plugin owns its own skill source and support files.

## Layout

- Claude marketplace: `.claude-plugin/marketplace.json`
- Codex marketplace: `.agents/plugins/marketplace.json`
- External (upstream-maintained) plugin registry: `.claude-plugin/external-plugins.json`
- Plugin source of truth: `plugins/<plugin-name>/`
- Canonical skill entrypoint: `plugins/<plugin-name>/skills/<plugin-name>/SKILL.md`

## Common Commands

```bash
npm run plugin:sync
npm run plugin:validate
```

Use `npm run plugin:sync` after adding or renaming plugins. It updates every plugin manifest version and regenerates both marketplace catalogs.

Use `npm run plugin:validate` before commit. It verifies:

1. Every plugin has `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`
2. Every plugin has `skills/<plugin-name>/SKILL.md`
3. Claude marketplace lists every local plugin plus every external plugin; Codex marketplace lists every local plugin only
4. All plugin manifest versions match `package.json`
5. Referenced `references/`, `examples/`, `templates/`, and `assets/` stay inside each plugin
6. Every external plugin in `.claude-plugin/external-plugins.json` has a matching entry in the Claude marketplace with a valid object-form `source` (e.g. `{ "source": "github", "repo": "owner/repo" }`) and a name that does not collide with a local plugin

## Adding A Plugin

1. Create `plugins/<plugin-name>/`
2. Add `.claude-plugin/plugin.json`
3. Add `.codex-plugin/plugin.json`
4. Add `skills/<plugin-name>/SKILL.md`
5. Keep all plugin-specific support files in that same plugin
6. Run `npm run plugin:sync`
7. Run `npm run plugin:validate`

## Adding An External / Upstream Plugin

For a plugin whose code lives in a separate GitHub repo and is maintained upstream, do **not** copy the source into `plugins/`. Register a marketplace entry instead:

1. Append an entry to `.claude-plugin/external-plugins.json` with the shape:
   ```json
   {
     "name": "<upstream plugin name>",
     "description": "...",
     "homepage": "https://github.com/<owner>/<repo>",
     "source": { "source": "github", "repo": "<owner>/<repo>" }
   }
   ```
   - `name` must equal the upstream `.claude-plugin/plugin.json` `name`, so users can `/plugin install <name>@gm-skills`.
   - Optionally pin with `"ref": "<tag>"` or `"sha": "<40-char sha>"`.
2. Run `npm run plugin:sync`
3. Run `npm run plugin:validate`

Notes:
- External plugins are **Claude marketplace–only**. Codex is not supported because upstream repos typically ship no `.codex-plugin/plugin.json`.
- By default the entry tracks the upstream default branch. Pin a `ref`/`sha` to freeze a version.
- If the upstream author changes the plugin name or repo, update the entry here.

## Editing Rules

- Do not reintroduce a root `skills/` source tree
- Do not create a new aggregate plugin like `plugins/gm-skills/`
- Do not point manifests at paths outside their plugin directory
- If a skill uses `references/`, `examples/`, `templates/`, or `assets/`, keep those files inside the plugin package

## Complete Criteria

1. The target plugin is independently installable from the root marketplace
2. `npm run plugin:sync` is clean
3. `npm run plugin:validate` passes
4. README and marketplace descriptions match the new plugin or change
