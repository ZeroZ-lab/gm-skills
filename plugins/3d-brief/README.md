# 3d-brief

把自然语言 3D 需求转为创意方向和可执行生产合同；用户明确要求成品后，继续指导 Agent 完成 Blender 建模、渲染评审与验收。一个入口，按阶段读取支持文件。

## 安装与调用

在 Claude Code 中从 gm-skills 市场安装：

```text
/plugin marketplace add ZeroZ-lab/gm-skills
/plugin install 3d-brief@gm-skills
/3d-brief:3d-brief 帮我设计一个温暖的小型咖啡吧，先交生产简报
```

本地 ZIP 解压后，用终端从插件目录的父目录启动：

```bash
claude --plugin-dir ./3d-brief
```

然后调用 `/3d-brief:3d-brief`。如只使用独立 Skill，把 `skills/3d-brief/` 整个目录复制到 `~/.claude/skills/3d-brief/` 或项目 `.claude/skills/3d-brief/`，调用 `/3d-brief`；不要只复制 SKILL.md。无需另装其他 Skill。

## 行为边界

| 用户意图 | 行为 |
|---|---|
| “做个 3D 酒吧”“帮我写生产提示词” | 默认交 brief 和检查结果，不启动制作 |
| “给我几个创意方向” | 提供有区别的方向，在用户要求的阶段结束 |
| “全推荐/你定” | 沿用已提出的默认，不继续强制问卷 |
| “按简报直接生成 .blend 和渲染” | 已授权制作；验证环境与资源预算后实际执行 |
| “继续上次制作” | 从状态与有效检查点恢复，延续原预算 |

支持最完整的路径是 Blender 产品资产与空间静态场景。动画、游戏运行时和网页交互可做简报，但需要额外的执行/验收设计。本包不自带 Blender、模型或渲染服务，也不自动购买资源。

## 输出结构

仅写简报时输出 `<slug>_brief.md` 与 `<slug>_brief_check.md`，不创建制作目录。授权制作后，采用聚合结构：

```text
<slug>/
  <slug>_brief.md
  <slug>_final.blend
  README.md
  renders/       # 最终图片、总览图和生成清单
  assets/        # 必要外部资源，按需创建
  _work/         # 合并工作记录、脚本、检查点、逐轮评审和验证证据
```

美术方向、资产清单、任务状态、规划与简报检查合并在 `_work/PROJECT.md`；每轮图片、评审及日志集中到 `_work/reviews/round_<n>/`。目录按需创建，质量门与证据要求保持不变。`_work/` 包含恢复和复现资料，应随完整工程保留。旧项目沿用已有路径，用户指定的布局优先。

## 八层生产契约

Goal 定义成果；Environment 声明能力与预算；Protocol 保存状态；Build Order 按阶段验证；Domain Spec 明确数量与功能；Review Loop 使用固定证据；Rubric 防止高分抵消缺项；Validation 检查真正保存的成果。

源头方法参考 [Skyline Restaurant and Cocktail Bar](https://restaurant-bar.space-z.ai/skyline_restaurant_bar_brief.html)。本包提炼并改写其方法，不附带原文或第三方图片。严格 Skyline 配置保留至少4轮和指定16机位；通用任务按范围配置，通常3–5轮，不继承原文的机器、超长预算或餐位数量。

## 内容导航

- [入口](skills/3d-brief/SKILL.md)
- [生产简报模板](skills/3d-brief/references/brief-template.md)
- [创意与事实研究](skills/3d-brief/references/creative-direction.md)
- [简报交接检查](skills/3d-brief/references/contract-check.md)
- [产品分支](skills/3d-brief/references/product.md) / [空间分支](skills/3d-brief/references/environment.md)
- [制作流程](skills/3d-brief/references/production.md) / [评审模板](skills/3d-brief/references/review-template.md)
- [原创音箱完整示例](skills/3d-brief/examples/desktop_speaker_brief.md)
- [咖啡吧完整示例](skills/3d-brief/examples/coffee_bar_brief.md)
- [真实产品研究草案](skills/3d-brief/examples/macbook_teardown_brief.md)
- [维护与回归案例](skills/3d-brief/references/evaluation-cases.md)

## 验证与发布

在 gm-skills 仓库运行 `npm run plugin:sync`、`npm run plugin:validate`；本地插件可运行 `claude plugin validate ./plugins/3d-brief`。本修订版本为 1.8.1；本仓库采用统一版本，发布时由根 package.json 同步全部插件清单。

核对规范日期：2026-09-08。[Claude Code Skills](https://code.claude.com/docs/en/skills) 和 [插件规范](https://code.claude.com/docs/en/plugins-reference) 是安装与格式依据。SKILL.md 使用 name/description，辅助内容留在插件内；没有 context: fork，用户交互留在主会话。

本地 Claude Code 2.1.261 的严格插件校验已通过；仓库校验、Skill frontmatter 校验、包内链接、两个完整示例的数量与评分计算均通过。

文档示例不是已生成作品。结构检查、语义走查、实际 Claude 会话测试、Blender 真实制作是不同级别的证据，发布说明应分别报告；本次未运行真实模型会话或 Blender 制作。

许可沿用本仓库声明的 MIT；不包含对外部参考内容的再许可。
