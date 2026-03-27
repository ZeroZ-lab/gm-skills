#!/bin/sh

set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
skill_file="$repo_root/skills/gm-topic-engine/SKILL.md"
de_ai_skill_file="$repo_root/skills/gm-de-ai-article/SKILL.md"
battle_init_skill_file="$repo_root/skills/gm-battle/SKILL.md"
pk_skill_file="$repo_root/skills/gm-pk/SKILL.md"
build_harness_skill_file="$repo_root/skills/build-harness-project/SKILL.md"
build_harness_reference_file="$repo_root/skills/build-harness-project/references/file-templates.md"

fail() {
  printf '%s\n' "$1" >&2
  exit 1
}

[ -f "$skill_file" ] || fail "missing skill file: $skill_file"

grep -F "name: gm-topic-engine" "$skill_file" >/dev/null || fail "skill frontmatter must declare name: gm-topic-engine"
grep -F "description:" "$skill_file" >/dev/null || fail "skill frontmatter must declare a description"
grep -F "argument-hint: \"[想法、笔记、评论、草稿]\"" "$skill_file" >/dev/null || fail "skill frontmatter must declare the expected argument hint"
grep -F "# gm-topic-engine" "$skill_file" >/dev/null || fail "skill body must include the skill heading"

[ -f "$de_ai_skill_file" ] || fail "missing skill file: $de_ai_skill_file"

grep -F "name: gm-de-ai-article" "$de_ai_skill_file" >/dev/null || fail "skill frontmatter must declare name: gm-de-ai-article"
grep -F "description:" "$de_ai_skill_file" >/dev/null || fail "skill frontmatter must declare a description"
grep -F "argument-hint: \"[文章草稿]\"" "$de_ai_skill_file" >/dev/null || fail "skill frontmatter must declare the expected argument hint"
grep -F "# gm-de-ai-article" "$de_ai_skill_file" >/dev/null || fail "skill body must include the skill heading"

[ -f "$battle_init_skill_file" ] || fail "missing skill file: $battle_init_skill_file"

grep -F "name: gm-battle" "$battle_init_skill_file" >/dev/null || fail "skill frontmatter must declare name: gm-battle"
grep -F "description: Use when starting a new battle session" "$battle_init_skill_file" >/dev/null || fail "gm-battle description should describe when to use the skill"
grep -F '`pk_id`' "$battle_init_skill_file" >/dev/null || fail "gm-battle must describe generating a pk_id"
grep -F '只允许讨论方案，不允许编写、修改或提交任何代码' "$battle_init_skill_file" >/dev/null || fail "gm-battle must explicitly prohibit code changes during battle"
grep -F "last_implement_output_version" "$battle_init_skill_file" >/dev/null || fail "gm-battle must initialize implement-output version metadata"
grep -F "last_judge_output" "$battle_init_skill_file" >/dev/null || fail "gm-battle must initialize last_judge_output"
grep -F 'battle/sessions/<pk_id>/state.json' "$battle_init_skill_file" >/dev/null || fail "gm-battle must write per-session state files"
grep -F 'battle/sessions/<pk_id>/issues.json' "$battle_init_skill_file" >/dev/null || fail "gm-battle must write per-session issues files"
grep -F 'battle/latest.json' "$battle_init_skill_file" >/dev/null || fail "gm-battle must update latest battle index"
grep -F '"current_stage": "implement"' "$battle_init_skill_file" >/dev/null || fail "gm-battle must initialize the implement stage"
grep -F "# gm-battle" "$battle_init_skill_file" >/dev/null || fail "skill body must include the skill heading"

[ -f "$pk_skill_file" ] || fail "missing skill file: $pk_skill_file"

grep -F "name: gm-pk" "$pk_skill_file" >/dev/null || fail "skill frontmatter must declare name: gm-pk"
grep -F "description: Use when an existing battle session already has state on disk" "$pk_skill_file" >/dev/null || fail "gm-pk description should describe when to use the skill"
grep -F "argument-hint: \"[pk_id] [stop]\"" "$pk_skill_file" >/dev/null || fail "gm-pk must accept an optional pk_id and stop flag"
grep -F 'battle/sessions/<pk_id>/state.json' "$pk_skill_file" >/dev/null || fail "gm-pk must read per-session state files"
grep -F 'battle/sessions/<pk_id>/issues.json' "$pk_skill_file" >/dev/null || fail "gm-pk must read per-session issues files"
grep -F 'battle/latest.json' "$pk_skill_file" >/dev/null || fail "gm-pk must describe latest-session resolution"
grep -F '整个 battle 是方案评审流程，不是编码流程。' "$pk_skill_file" >/dev/null || fail "gm-pk must define battle as plan review rather than coding"
grep -F '如果没有传 `pk_id`，优先读取 `battle/latest.json`' "$pk_skill_file" >/dev/null || fail "gm-pk must resolve the latest battle when pk_id is omitted"
grep -F 'last_implement_output_version' "$pk_skill_file" >/dev/null || fail "gm-pk must require implement-output version metadata"
grep -F 'implement-r{current_round}' "$pk_skill_file" >/dev/null || fail "gm-pk must gate the initial implement handoff with version metadata"
grep -F 'revise-r{current_round}' "$pk_skill_file" >/dev/null || fail "gm-pk must gate revised plan handoff with version metadata"
grep -F '如果 `battle/sessions/<pk_id>/state.json` 中还没有 `last_judge_output` 字段，应补上并设为空字符串' "$pk_skill_file" >/dev/null || fail "gm-pk must describe initializing last_judge_output when entering judge"
grep -F '> `last_judge_output` 为空。请先把裁判模型的输出写入 `battle/sessions/<pk_id>/state.json`，再运行 `/gm:gm-pk`。' "$pk_skill_file" >/dev/null || fail "gm-pk must block judge completion until last_judge_output exists"
grep -F -- '- 将 `current_actor` 更新为 `judge`' "$pk_skill_file" >/dev/null || fail "gm-pk must set current_actor to judge when stopping"
grep -F -- '- 将 `current_actor` 更新为 `none`' "$pk_skill_file" >/dev/null || fail "gm-pk must set current_actor to none when completed"
grep -F '只有 `last_judge_output` 已写入时，才能从 judge 进入 completed' "$pk_skill_file" >/dev/null || fail "gm-pk must document the judge completion gate"
grep -F '最新方案正文：' "$pk_skill_file" >/dev/null || fail "gm-pk judge prompt must include the latest proposal text"
grep -F '被判定为 rejected 的问题' "$pk_skill_file" >/dev/null || fail "gm-pk judge prompt must surface rejected issues"
grep -F '[RESOLVE ISSUE-001]' "$pk_skill_file" >/dev/null || fail "gm-pk revise prompt must require issue-id-based responses"
grep -F '[REJECT ISSUE-002]' "$pk_skill_file" >/dev/null || fail "gm-pk revise prompt must support explicit rejections by issue id"
grep -F '只有在相关时，再补充安全性、性能、合规性或表达质量问题' "$pk_skill_file" >/dev/null || fail "gm-pk challenge prompt should adapt review dimensions to the task"
grep -F '拿到裁判回复后，应将完整输出写入 `battle/sessions/<pk_id>/state.json` 的 `last_judge_output`，再运行一次 `/gm:gm-pk` 完成收尾。' "$pk_skill_file" >/dev/null || fail "gm-pk must explain the final judge handoff"
grep -F "# gm-pk" "$pk_skill_file" >/dev/null || fail "skill body must include the skill heading"

[ -f "$build_harness_skill_file" ] || fail "missing skill file: $build_harness_skill_file"

grep -F "name: build-harness-project" "$build_harness_skill_file" >/dev/null || fail "skill frontmatter must declare name: build-harness-project"
grep -F "description:" "$build_harness_skill_file" >/dev/null || fail "skill frontmatter must declare a description"
grep -F 'argument-hint: "[目标项目，例如：为 skills manager 创建 harness]"' "$build_harness_skill_file" >/dev/null || fail "build-harness-project must declare the expected argument hint"
grep -F '`harness/` = AI 开发系统' "$build_harness_skill_file" >/dev/null || fail "build-harness-project must define the harness boundary"
grep -F '`projects/<name>/.harness/` = 项目给 harness 的接口层' "$build_harness_skill_file" >/dev/null || fail "build-harness-project must define the .harness boundary"
grep -F '`spec > rules > contract > resources > summary/report`' "$build_harness_skill_file" >/dev/null || fail "build-harness-project must define information priority"
grep -F "# build-harness-project" "$build_harness_skill_file" >/dev/null || fail "skill body must include the skill heading"

[ -f "$build_harness_reference_file" ] || fail "missing reference file: $build_harness_reference_file"

grep -F 'harness/orchestrator/' "$build_harness_reference_file" >/dev/null || fail "build-harness-project reference must include orchestrator templates"
grep -F 'projects/my-project/.harness/' "$build_harness_reference_file" >/dev/null || fail "build-harness-project reference must include project-side templates"
grep -F '`spec > rules > contract > resources > summary/report`' "$build_harness_reference_file" >/dev/null || fail "build-harness-project reference must repeat information priority"
