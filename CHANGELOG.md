# Changelog

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
