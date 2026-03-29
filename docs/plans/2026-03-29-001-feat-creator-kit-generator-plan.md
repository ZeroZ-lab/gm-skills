---
title: "gm-creator-kit: 内容创作者技能套件生成器"
type: feat
status: active
date: 2026-03-29
origin: docs/brainstorms/2026-03-29-creator-kit-requirements.md
---

# gm-creator-kit: 内容创作者技能套件生成器

## 概述

创建一个面向内容创作者的元技能，通过引导式对话，帮助非技术用户将自己的创作工作流转化为一套可复用的 AI skills。区别于技术型 skill 编写指南，本方案完全隐藏技术细节，用业务语言替代技术术语。

## 问题定义

内容创作者有成熟的工作流（选题→调研→写稿→改稿→标题→配图→发布），但：
- 不知道如何把个人经验转化为 AI skills
- 现有 skill 编写指南门槛过高（TDD、pressure testing）
- 业务型 skills 更注重创意输出，不需要严谨的工程测试

## 需求追溯

| 需求 | 本计划实现方式 |
|------|---------------|
| R1: 引导式 Skill 生成 | 对话式引导 + 填空模板 |
| R2: 创作者友好模板 | 内容创作专用模板库 |
| R3: 套件打包 | 自动生成套件结构和索引 |
| R4: 快速验证 | 样例输出验证替代压力测试 |

## 范围边界

**包含:**
- 元技能 gm-creator-kit 本身
- 6 个内容创作环节模板
- 套件打包和索引生成

**不包含:**
- 通用 skill 测试框架
- 技能分享平台
- 非创作类 skill 支持

## 技术决策

1. **完全隐藏技术细节**: 创作者只需描述「做什么」，不接触 skill 结构
2. **样例验证**: 用 3 组输入/输出样例验证 skill 效果，而非 pressure testing
3. **标准输出**: 生成标准 skill 结构确保 Claude Code 兼容性

## 实现单元

- [ ] **Unit 1: 元技能主体框架 (gm-creator-kit/SKILL.md)**

**目标:** 创建引导内容创作者生成 skills 的核心元技能

**需求:** R1

**依赖:** 无

**文件:**
- 创建: `skills/gm-creator-kit/SKILL.md`

**实现方式:**
- 设计对话流程：发现工作流 → 拆解环节 → 选择模板 → 填充内容 → 生成套件
- 隐藏 SKILL.md 技术细节，用「环节名称」「触发条件」「操作步骤」等业务术语
- 内置 6 个创作环节模板映射：选题/调研/写稿/改稿/标题/配图

**模板类型映射:**
| 创作环节 | Skill 类型 | 模板特征 |
|---------|-----------|---------|
| 选题 | Decision | 判断标准、筛选逻辑 |
| 调研 | Research | 信息源、整理框架 |
| 写初稿 | Generation | 结构模板、风格指令 |
| 改稿 | Transformation | 检查清单、改写规则 |
| 起标题 | Hook | 注意力机制、AB选项 |
| 配图 | Prompt | 视觉描述、风格约束 |

**验证:**
- 元技能能被正确加载
- 对话流程覆盖完整工作流

---

- [ ] **Unit 2: 内容创作模板库**

**目标:** 提供 6 个预置的创作环节模板

**需求:** R2

**依赖:** Unit 1

**文件:**
- 创建: `skills/gm-creator-kit/templates/选题决策.md`
- 创建: `skills/gm-creator-kit/templates/调研整理.md`
- 创建: `skills/gm-creator-kit/templates/初稿生成.md`
- 创建: `skills/gm-creator-kit/templates/改稿优化.md`
- 创建: `skills/gm-creator-kit/templates/标题撰写.md`
- 创建: `skills/gm-creator-kit/templates/配图提示.md`

**实现方式:**
- 每个模板包含：引导问题 → 填空区域 → 示例 → 输出预览
- 模板语言平实，无技术术语
- 提供基于 gm-x-hook-writer 和 gm-writing 的提炼示例

**验证:**
- 6 个模板完整可用
- 模板能被元技能正确引用

---

- [ ] **Unit 3: 套件生成器逻辑**

**目标:** 将多个 skills 打包成可协同工作的创作者套件

**需求:** R3

**依赖:** Unit 1, Unit 2

**文件:**
- 创建: `skills/gm-creator-kit/generator.js`
- 创建: `skills/gm-creator-kit/templates/套件索引.md`

**实现方式:**
- 生成器接收：套件名称 + 选择的环节 + 每个环节的填充内容
- 输出标准 skill 目录结构：
  ```
  skills/
    <套件名>-选题/
      SKILL.md
    <套件名>-调研/
      SKILL.md
    ...
    <套件名>-索引/
      SKILL.md  # 套件使用指南
  ```
- 套件索引说明各环节调用顺序和配合方式

**验证:**
- 生成器能输出标准 skill 结构
- 生成的 skills 能被 Claude Code 加载

---

- [ ] **Unit 4: 样例验证工具**

**目标:** 提供简化的 skill 验证方式

**需求:** R4

**依赖:** Unit 3

**文件:**
- 创建: `skills/gm-creator-kit/validator.js`
- 创建: `skills/gm-creator-kit/templates/验证工作表.md`

**实现方式:**
- 验证工作表包含：3组输入样例 → 预期输出特征 → 实际输出对比
- 通过对比判断 skill 是否符合预期
- 提供调整建议模板

**验证:**
- 验证流程能在 5 分钟内完成
- 提供明确的通过/调整信号

---

- [ ] **Unit 5: 示例创作者套件**

**目标:** 提供一个完整的示例套件作为参考

**需求:** R1-R4

**依赖:** Unit 1-4

**文件:**
- 创建: `skills/example-creator-kit/` 完整示例

**实现方式:**
- 基于「科技评论博主」人设创建示例套件
- 包含完整的 6 个环节 skills
- 展示套件索引和协同使用方式

**验证:**
- 示例套件能正常运行
- 作为创作者参考模板

---

- [ ] **Unit 6: 使用文档**

**目标:** 提供完整的使用指南

**需求:** R1-R4

**依赖:** Unit 1-5

**文件:**
- 创建: `skills/gm-creator-kit/README.md`
- 创建: `docs/creator-kit-guide.md`

**实现方式:**
- README: 快速开始（3 步创建第一个 skill）
- 指南：完整工作流说明、最佳实践、FAQ

**验证:**
- 新用户能在 30 分钟内创建第一个 skill

## 系统影响

- 新增 skills 目录，不影响现有代码
- 生成器输出到 skills/ 目录，遵循现有 skill 发现机制
- 无外部依赖或运行时影响

## 风险与应对

| 风险 | 可能性 | 影响 | 应对 |
|-----|-------|-----|-----|
| 生成的 skills 质量参差不齐 | 中 | 中 | 提供验证工作表 + 示例参考 |
| 创作者不理解 skill 概念 | 高 | 低 | 完全隐藏技术细节，用业务语言 |
| 模板不够通用 | 中 | 低 | 从现有 gm-* skills 提炼，保持迭代 |

## 测试场景

**Unit 1 (元技能):**
- 场景: 创作者描述自己的工作流 → 元技能正确拆解为环节
- 场景: 选择「写初稿」环节 → 提供正确的初稿生成模板

**Unit 3 (生成器):**
- 场景: 输入套件名+3个环节内容 → 输出标准 skill 目录结构
- 场景: 生成的 skill 能被 Claude Code 正确加载

**Unit 5 (示例套件):**
- 场景: 使用示例套件的「标题撰写」skill → 输出符合科技评论风格的标题

## 文档

- 使用指南: docs/creator-kit-guide.md
- 快速开始: skills/gm-creator-kit/README.md
- 示例参考: skills/example-creator-kit/

## 参考

- 需求文档: docs/brainstorms/2026-03-29-creator-kit-requirements.md
- 现有业务 skills: skills/gm-x-hook-writer/, skills/gm-writing/
- Skill 编写规范: superpowers/writing-skills
