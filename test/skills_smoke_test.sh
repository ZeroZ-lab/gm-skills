#!/bin/sh

set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
skill_file="$repo_root/skills/gm-topic-engine/SKILL.md"
de_ai_skill_file="$repo_root/skills/gm-de-ai-article/SKILL.md"
battle_init_skill_file="$repo_root/skills/gm-battle/SKILL.md"
pk_skill_file="$repo_root/skills/gm-pk/SKILL.md"

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
grep -F '`pk_id`' "$battle_init_skill_file" >/dev/null || fail "gm-battle must describe generating a pk_id"
grep -F '只允许讨论方案，不允许编写、修改或提交任何代码' "$battle_init_skill_file" >/dev/null || fail "gm-battle must explicitly prohibit code changes during battle"
grep -F "last_judge_output" "$battle_init_skill_file" >/dev/null || fail "gm-battle must initialize last_judge_output"
grep -F 'battle/sessions/<pk_id>/state.json' "$battle_init_skill_file" >/dev/null || fail "gm-battle must write per-session state files"
grep -F 'battle/sessions/<pk_id>/issues.json' "$battle_init_skill_file" >/dev/null || fail "gm-battle must write per-session issues files"
grep -F 'battle/latest.json' "$battle_init_skill_file" >/dev/null || fail "gm-battle must update latest battle index"
grep -F '"current_stage": "implement"' "$battle_init_skill_file" >/dev/null || fail "gm-battle must initialize the implement stage"
grep -F "# gm-battle" "$battle_init_skill_file" >/dev/null || fail "skill body must include the skill heading"

[ -f "$pk_skill_file" ] || fail "missing skill file: $pk_skill_file"

grep -F "name: gm-pk" "$pk_skill_file" >/dev/null || fail "skill frontmatter must declare name: gm-pk"
grep -F "argument-hint: \"[pk_id] [stop]\"" "$pk_skill_file" >/dev/null || fail "gm-pk must accept an optional pk_id and stop flag"
grep -F 'battle/sessions/<pk_id>/state.json' "$pk_skill_file" >/dev/null || fail "gm-pk must read per-session state files"
grep -F 'battle/sessions/<pk_id>/issues.json' "$pk_skill_file" >/dev/null || fail "gm-pk must read per-session issues files"
grep -F 'battle/latest.json' "$pk_skill_file" >/dev/null || fail "gm-pk must describe latest-session resolution"
grep -F '整个 battle 是方案评审流程，不是编码流程。' "$pk_skill_file" >/dev/null || fail "gm-pk must define battle as plan review rather than coding"
grep -F '如果没有传 `pk_id`，优先读取 `battle/latest.json`' "$pk_skill_file" >/dev/null || fail "gm-pk must resolve the latest battle when pk_id is omitted"
grep -F '如果 `battle/sessions/<pk_id>/state.json` 中还没有 `last_judge_output` 字段，应补上并设为空字符串' "$pk_skill_file" >/dev/null || fail "gm-pk must describe initializing last_judge_output when entering judge"
grep -F '> `last_judge_output` 为空。请先把裁判模型的输出写入 `battle/sessions/<pk_id>/state.json`，再运行 `/gm:gm-pk`。' "$pk_skill_file" >/dev/null || fail "gm-pk must block judge completion until last_judge_output exists"
grep -F -- '- 将 `current_actor` 更新为 `judge`' "$pk_skill_file" >/dev/null || fail "gm-pk must set current_actor to judge when stopping"
grep -F -- '- 将 `current_actor` 更新为 `none`' "$pk_skill_file" >/dev/null || fail "gm-pk must set current_actor to none when completed"
grep -F '只有 `last_judge_output` 已写入时，才能从 judge 进入 completed' "$pk_skill_file" >/dev/null || fail "gm-pk must document the judge completion gate"
grep -F '拿到裁判回复后，应将完整输出写入 `battle/sessions/<pk_id>/state.json` 的 `last_judge_output`，再运行一次 `/gm:gm-pk` 完成收尾。' "$pk_skill_file" >/dev/null || fail "gm-pk must explain the final judge handoff"
grep -F "# gm-pk" "$pk_skill_file" >/dev/null || fail "skill body must include the skill heading"
