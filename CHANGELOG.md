# Changelog

## 1.8.0 (2026-09-08)

- feat(3d-brief): add intent-based creative direction, production contracts, and explicitly authorized Blender production and review workflows through one entrypoint. Replace mandatory interview rounds with focused clarification and recorded defaults.
- feat(3d-brief): add product and environment branches, contract checks, fixed review instructions, budget-aware recovery, and frozen-scene render validation.
- docs(3d-brief): add desktop speaker and coffee bar briefs, installation instructions, and behavioral evaluation cases; replace the mixed-model MacBook example with an explicitly unresolved research draft.
- fix(3d-brief): unify asset counts and hard completion gates; preserve interface data under supported manifest metadata and remove the unverified minimum Claude version claim.
- validation: repository and strict Claude plugin checks pass, with static example and link checks; real Claude behavioral sessions and Blender production remain untested.

## 1.7.0 (2026-09-08)

- feat: add `3d-brief` plugin — turn a vague 3D project idea into a production-grade autonomous-build brief. The skill researches verifiable facts itself (official specs, public teardowns, surface finishes), grills the user only for intent and preferences (one theme per round, defaults offered), and emits a 00-07 mission brief with rubric, evidence-governed review loop, and cold-start validation. Ships with a full example brief (`MacBook Pro 14″` teardown). Claude Code marketplace only.
- feat: the repo now publishes Claude Code plugins only — the local-plugin default market is `["claude"]` (matching the external-plugins default), all 12 `.codex-plugin/` manifests are removed, and the Codex catalog is empty. A plugin can still opt into Codex explicitly via a `markets` array plus a `.codex-plugin/plugin.json`; `plugin:sync` and `plugin:validate` enforce membership in both directions.

## 1.4.0 (2026-07-06)

- feat: convert `cc-design` to an upstream plugin — remove local `plugins/cc-design/` (209 files) and register it from `github:ZeroZ-lab/cc-design` instead
- feat: external plugins now support a `markets` field (`["claude"]`/`["codex"]`) so a single entry can target one or both marketplaces
- feat: `plugin:sync` writes external entries into the Claude and/or Codex marketplace based on `markets`; `plugin:validate` checks counts per-market and verifies Codex external entries too
- breaking: `cc-design` is removed from the Codex marketplace (now Claude-only via upstream)

## 1.3.0 (2026-07-06)

- feat: support external/upstream plugins — register `mattpocock-skills` from `github:mattpocock/skills` in the Claude marketplace without copying source
- feat: add `.claude-plugin/external-plugins.json` registry; `plugin:sync` merges external entries into the Claude marketplace only (Codex stays local-only)
- feat: `plugin:validate` now recognizes external plugins and verifies their object-form `source` and name uniqueness
- docs: document external/upstream plugin workflow in README and CLAUDE.md

## 1.2.0 (2026-06-24)

- feat: implement the Observed Evidence deepening, Runtime Facts seam, schema 2.0, fail-visible validation, and non-synthetic ZCode detection
- feat: implement the gm-skill-manager Stage 1 Unified Inventory, runtime evidence adapters, derived views, diagnostics, redaction, and native-installer action contract
- docs: define the gm-skill-manager Stage 1 domain model, architecture decisions, execution plan, and P0 test skeleton

## 1.0.0 (2026-04-26)

- feat: Claude Code 插件支持 — 添加 `.claude-plugin/` 清单文件和 `package.json`
- feat: 新增 `gm-skill-quality` skill — 基于 unified + cc-design 实践标准的 6 轴技能质量审查
