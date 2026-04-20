# gm-skills

Agent skills 集合，`npx skills add ZeroZ-lab/gm-skills` 安装。Markdown + Shell，无构建步骤。

## 常用命令

```bash
npx skills add . --list                              # 验证所有 skill 可发现
grep -rn '^name:\|^description:' skills/*/SKILL.md   # 检查 frontmatter
git submodule update --remote skills/cc-design        # 拉取 cc-design 最新
```

## 写代码时

- 新 skill 放 `skills/<skill-name>/SKILL.md`，`name` 与目录名一致
- cc-design 是 submodule → 只在 ZeroZ-lab/cc-design 仓库修改
- 其余 skill 直接在本仓库维护

```yaml
# ✅
---
name: my-skill
description: 具体说明做什么、何时触发，包含关键词
---

# ❌
---
name: My Skill
description: A useful skill
---
```

可选字段：`argument-hint`、`context: fork`、`allowed-tools`、`disable-model-invocation: true`

## 完成标准

1. `npx skills add . --list` 输出包含新 skill 名称
2. README.md 的 Skills 表格、Install 命令、Structure 已同步更新
3. commit message: `type(scope): description`

## 卡住时

- submodule 异常 → `git submodule sync && git submodule update --init --recursive`
- npx skills 找不到 skill → 检查 SKILL.md frontmatter 是否有 `name` 和 `description`
- ✅ 必须做：改完 skill 后跑 `npx skills add . --list` 验证
- ⚠️ 先问：删除已有 skill、修改 .gitmodules
- 🚫 绝不：直接改 `skills/cc-design/` 内容、force push main、删 .gitmodules
