# gm-skills

Agent skills 仓库，通过 `npx skills add ZeroZ-lab/gm-skills` 安装。

## 常用命令

```bash
# 列出所有 skills
npx skills add . --list

# 更新 cc-design submodule
git submodule update --remote skills/cc-design

# 验证 SKILL.md frontmatter
grep -l '^name:' skills/*/SKILL.md
```

## 写代码时

- 新 skill 放 `skills/<skill-name>/SKILL.md`
- frontmatter 必须有 `name` 和 `description`，`name` 与目录名一致
- cc-design 是 submodule，不要直接修改其内容
- 其余 skill 直接在本仓库维护

## SKILL.md frontmatter

```yaml
---
name: skill-name
description: 一句话描述
---
```

可选字段：`argument-hint`、`context: fork`、`allowed-tools`、`disable-model-invocation: true`

## 完成标准

1. `npx skills add . --list` 能发现新增的 skill
2. README.md 的 Skills 表格和 Structure 已更新
3. commit message 用 conventional commits 格式

## 卡住时

- submodule 问题：`git submodule sync && git submodule update --init`
- 绝不：直接修改 `skills/cc-design/` 内的文件、force push main
