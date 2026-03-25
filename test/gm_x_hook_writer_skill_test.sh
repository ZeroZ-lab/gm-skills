#!/bin/sh

set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
skill_file="$repo_root/skills/gm-x-hook-writer/SKILL.md"

fail() {
  printf '%s\n' "$1" >&2
  exit 1
}

[ -f "$skill_file" ] || fail "missing skill file: $skill_file"

grep -F "name: gm-x-hook-writer" "$skill_file" >/dev/null || fail "skill frontmatter must declare name: gm-x-hook-writer"
grep -F "description:" "$skill_file" >/dev/null || fail "skill frontmatter must declare a description"
grep -F "# gm-x-hook-writer" "$skill_file" >/dev/null || fail "skill body must include the skill heading"
grep -F '`hook-only`' "$skill_file" >/dev/null || fail "skill must define hook-only classification"
grep -F '`hook + follow-up line`' "$skill_file" >/dev/null || fail "skill must define hook plus follow-up classification"
grep -F '完整推文请求' "$skill_file" >/dev/null || fail "skill must define full-post boundary handling"
grep -F '通过条件' "$skill_file" >/dev/null || fail "skill must define the core-sentence pass condition"
grep -F '保守模式' "$skill_file" >/dev/null || fail "skill must define conservative mode"
grep -F '`curiosity-gap`' "$skill_file" >/dev/null || fail "skill must document curiosity-gap handling"
grep -F '至少改变以下维度中的 2 个' "$skill_file" >/dev/null || fail "skill must define an executable hook difference test"
grep -F '简短服从信息' "$skill_file" >/dev/null || fail "skill must prioritize information over raw brevity"
grep -F '只改变最终输出格式，不改变内部 workflow' "$skill_file" >/dev/null || fail "skill must keep the workflow when users request no explanation"
grep -F '宁可少给，也不要凑数' "$skill_file" >/dev/null || fail "skill must refuse batch padding with near-duplicate hooks"
