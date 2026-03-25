#!/bin/sh

set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
skill_file="$repo_root/skills/gm-writing/SKILL.md"

fail() {
  printf '%s\n' "$1" >&2
  exit 1
}

[ -f "$skill_file" ] || fail "missing skill file: $skill_file"

grep -F "name: gm-writing" "$skill_file" >/dev/null || fail "skill frontmatter must declare name: gm-writing"
grep -F "description:" "$skill_file" >/dev/null || fail "skill frontmatter must declare a description"
grep -F 'argument-hint: "[文章草稿 / 主题]"' "$skill_file" >/dev/null || fail "skill frontmatter must declare the expected argument hint"
grep -F "# gm-writing" "$skill_file" >/dev/null || fail "skill body must include the skill heading"
grep -F '`draft-rewrite`' "$skill_file" >/dev/null || fail "skill must document the default draft-rewrite mode"
grep -F '`from-scratch`' "$skill_file" >/dev/null || fail "skill must document the explicit from-scratch mode"
grep -F '专业知识版' "$skill_file" >/dev/null || fail "skill must document the professional knowledge template"
grep -F '思想随笔版' "$skill_file" >/dev/null || fail "skill must document the thought essay template"
grep -F '战略分析版' "$skill_file" >/dev/null || fail "skill must document the strategic analysis template"
grep -F '创造实践版' "$skill_file" >/dev/null || fail "skill must document the creative practice template"
grep -F '矛盾切入' "$skill_file" >/dev/null || fail "skill must require contradiction-led openings"
grep -F '系统结构' "$skill_file" >/dev/null || fail "skill must require system structure strengthening"
grep -F '机制剖析' "$skill_file" >/dev/null || fail "skill must require mechanism analysis"
grep -F '实践路径' "$skill_file" >/dev/null || fail "skill must require a practical path"
grep -F 'gm-de-ai-article' "$skill_file" >/dev/null || fail "skill must define its boundary against gm-de-ai-article"
