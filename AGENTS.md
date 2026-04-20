# gm-skills

Agent skills 仓库，通过 `npx skills add ZeroZ-lab/gm-skills` 安装。

## 项目结构

- `skills/<name>/SKILL.md` — 每个 skill 的定义文件
- `skills/cc-design/` — git submodule，独立仓库维护
- 其余 skill 直接在本仓库维护

## 添加新 Skill

1. 创建 `skills/<skill-name>/SKILL.md`
2. frontmatter 必须包含 `name` 和 `description`
3. `name` 与目录名保持一致
4. 更新 `README.md` 的 Skills 表格和 Structure

## SKILL.md frontmatter 规范

```yaml
---
name: skill-name
description: 一句话描述，用于自动匹配触发
---
```

可选字段：`argument-hint`、`context: fork`、`allowed-tools`、`disable-model-invocation: true`

## 注意

- cc-design 是 submodule，不要直接修改，更新用 `git submodule update --remote skills/cc-design`
- commit message 用 conventional commits 格式
