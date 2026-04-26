---
name: gm-skill-quality
description: 审查 agent skills 质量，对 SKILL.md 给出结构化审查报告和优化建议。使用 cuando 需要评估 skill 实现质量、编写新 skill 后质量把关、review PR 中的 skill 变更
argument-hint: "[目标 skill 路径，默认扫描所有本地非 submodule skill]"
---

# Skill Quality — 技能质量审查

基于 unified + cc-design 实践标准的结构化 skill 审查。

审查标准来源于对 unified（CANON.md + 44 技能通用模式）和 cc-design（P0-P3 原则、路由表、输出契约）的项目实践总结。

## 入口/出口

- **入口**: 一个或多个目标 skill 的 `SKILL.md`
- **出口**: 结构化审查报告（`review/<skill-name>-quality-report.md`）
- **指向**: 通过 → 通知用户可合并/发布；有问题 → 给出具体修复建议
- **假设已加载**: 无

## Iron Law

<HARD-GATE>
没有基于 6 轴的结构化审查证据就不能批准一个 skill。每轴至少检查 4 个验证点。缺轴、跳过、或仅检查"看上去不错"即视为审查不完整。
</HARD-GATE>

## 何时不使用

- 审查 submodule skill（如 cc-design）—— 它们有独立的版本和标准
- 审查非 SKILL.md 文件（README、引用文档、模板）
- 用户要求直接修改 skill 而非仅审查（此时应调用编辑流程，不是审查技能）

## 工作流

### Step 1：确定审查目标

- **有参数** → 审查指定 skill 路径（如 `skills/auto-skill-fit`）
- **无参数** → 扫描 `skills/` 下所有非 submodule skill
- 排除规则：检查目标目录是否为 `.git` submodule（检测 `.git` 文件而非子目录）

输出审查列表让用户确认。

### Step 2：读取目标

对每个目标 skill，读取 `{target}/SKILL.md`。如果文件不存在，报告并跳过。

### Step 3：逐轴执行 6 轴审查

每轴检查以下验证点。每个验证点标注：

| 标记 | 含义 |
|------|------|
| ✅ | 满足 |
| ❌ | 不满足 |
| ⚠️ | 部分满足 |
| - | 不适用（记录理由） |

#### 轴 1：Frontmatter & Discoverability

检查 skill 能否被 agent 系统正确发现和调用。

- [ ] `name` 与目录名一致（CC: `name: my-skill` → 目录 `my-skill/`）
- [ ] `description` 包含具体功能描述和触发关键词
- [ ] 有 `argument-hint`（如需参数）
- [ ] `allowed-tools` 精确列明所需工具（不多开，不少开）
- [ ] YAML 语法正确，无换行/对齐错误

常见问题：
- `description` 过于通用（"A useful skill"），缺少触发关键词
- `argument-hint` 缺失但工作流包含 `[用户输入]`
- `allowed-tools` 包含从未使用的工具

#### 轴 2：Structural Completeness

检查 skill 是否包含质量 skill 的必要结构要素。

- [ ] 入口/出口条件已定义
- [ ] Iron Law 或等效 HARD-GATE
- [ ] 结构化步骤式工作流（非散文段落）
- [ ] "常见说辞表"（针对性反驳用户常见合理化借口）
- [ ] "红旗"清单（STOP 条件）
- [ ] "验证清单"（完成证据要求）
- [ ] 失败模式处理表（常见失败场景 + 对应处理操作）

source: unified 44 技能的通用结构模式。

#### 轴 3：Behavioral Guardrails

检查 skill 能否防止常见的 AI 行为陷阱。

- [ ] Surface Assumptions 机制（关键步骤前要求 / 输出假设）
- [ ] 验证证据要求（"应该能过"≠ 证据；测试/截图/构建 = 证据）
- [ ] Push Back 机制（有明确规则拒绝 bad input / 范围外请求）
- [ ] "何时使用 / 何时不使用"边界（防止不当触发）
- [ ] 防止 AI 幻觉措施（禁止编数据、编案例、猜版本号、猜价格）
- [ ] Manage Confusion 机制（遇到矛盾 STOP → 命名困惑 → 权衡 → 等解决）

source: CANON.md 第 1、5、7、8 条。

#### 轴 4：Specificity & Actionability

检查 skill 能否被 agent 无歧义地执行。

- [ ] 步骤具体到可独立执行（不依赖 AI "猜"下一步）
- [ ] 包含代码 / 命令 / 格式示例
- [ ] 输出格式 / 契约已定义
- [ ] 成功标准可测量（有具体验证命令或检查项）
- [ ] 边界值 / 命名规范 / 路径等给出了具体说明

source: cc-design 的 Output Contracts + unified 的验证清单。

#### 轴 5：Edge Case & Failure Coverage

检查 skill 对异常情况的处理是否完备。

- [ ] 已知失败模式已列明
- [ ] 异常输入（空值、缺失依赖）有处理路径
- [ ] 资源不可用（API down、工具缺失、无权限）时有降级/替代方案
- [ ] 大规模 / 性能边界有考虑（如大文件、长循环）
- [ ] 版本兼容性 / API 变更风险已说明

#### 轴 6：Scope Discipline

检查 skill 是否聚焦、不越界。

- [ ] 职责聚焦（一个 skill 做一件事，不做多件事）
- [ ] 步骤中无隐藏的 scope creep（"顺便"添加的功能）
- [ ] 外部依赖明确声明（其他技能、系统工具、API key）
- [ ] 与已有技能的集成方式清晰（不重复造轮子）

source: CANON.md 第 2（Simple First）、3（Scope Discipline）条。

### Step 4：分类意见

每个验证点加上级别标签：

| 级别 | 含义 | 处理要求 |
|------|------|---------|
| **Critical** | 必须改 | 合入/发布前必须修复 |
| **Important** | 强烈建议改 | 不修复需在报告中说明理由 |
| **Suggestion** | 可选 | 风格偏好或锦上添花 |

### Step 5：生成审查报告

每个 skill 按以下模板输出：

```markdown
# Skill Quality Report: <skill-name>

## Overall Verdict

**<Strong / Acceptable / Needs Work / Incomplete>**

<1-2 句摘要>

## Scorecard

| Axis | Verdict | Critical | Important | Suggestion |
|------|---------|----------|-----------|------------|
| 1. Frontmatter | ✅ | 0 | 0 | 0 |
| 2. Structure | ⚠️ | 1 | 2 | 1 |
| 3. Guardrails | ✅ | 0 | 0 | 0 |
| 4. Specificity | ⚠️ | 1 | 1 | 0 |
| 5. Edge Case | ❌ | 2 | 1 | 0 |
| 6. Scope | ✅ | 0 | 0 | 0 |
| **Total** | | **4** | **4** | **1** |

## Details

### Axis 1: Frontmatter — ✅

- ✅ `name` matches directory name
- ✅ `description` has trigger keywords
- ❌ [Critical] `allowed-tools` 包含 `Bash` 但在工作流中从未使用任何 bash 命令

**Suggestions:**

### Axis 2: Structure — ⚠️

...

## Summary of Required Changes

1. [Critical] ... (axis 1)
2. [Critical] ... (axis 5)
3. [Important] ... (axis 2)
```

**Verdict 定义：**

| Verdict | 条件 |
|---------|------|
| **Strong** | 0 Critical, < 3 Important, 覆盖率 > 80% |
| **Acceptable** | 0 Critical, < 5 Important |
| **Needs Work** | 1-2 Critical 或 < 60% 覆盖率 |
| **Incomplete** | ≥ 3 Critical 或缺 ≥ 2 轴 |

### Step 6：多 skill 场景

- 审查多个 skill 时，每个技能独立输出报告
- 结束时给出汇总表：

```markdown
## Summary

| Skill | Verdict | Critical | Important |
|-------|---------|----------|-----------|
| gm-agent-docs | Strong | 0 | 1 |
| gm-topic-engine | Acceptable | 0 | 3 |
| auto-skill-fit | Needs Work | 1 | 2 |
```

## 常见说辞

| 说辞 | 现实 |
|------|------|
| "我的 skill 很小，不需要这么多结构" | 小 skill 更需要清晰边界——否则 agent 会误触发。5 行描述 + 当/不当使用就够。 |
| "unified 的标准太严格了" | 不需要照搬 unified 的所有 section。核心是：边界清晰 + 行为可预测 + 可验证。 |
| "描述已经够清楚了，不需要关键词" | agent 通过 description 的关键词触发 skill。无关键词 = 不会被代理系统发现。 |
| "这个 skill 没人用，不需要审查" | 一次审查发现多个问题的案例比"一次通过"多得多。越早发现成本越低。 |
| "以后再加 red flags" | 红旗下次永远不会加。开发的时候不写，review 的时候也不会补。审查就是加的时机。 |

## 红旗 — STOP

- 审查者没有读取完整的 SKILL.md 就开始评价
- 审查报告中缺少某个轴（跳过即视为审查不完整）
- 审查者被其他 SKILL.md 的格式/表达影响判断（"它像 unified 所以好"≠ 它好）
- 审查意见全是 Suggestion 但明显有结构缺失（不敢打 Critical）
- 对 submodule skill 执行了审查
- 审查报告没有给出 Verdict（推诿判断）

## 验证清单

- [ ] 每个目标 skill 的 SKILL.md 已完整读取
- [ ] submodule skill 已排除
- [ ] 6 轴全部检查（每轴 ≥ 4 验证点）
- [ ] 每个验证点有明确标记（✅/❌/⚠️/-）
- [ ] Critical 问题标记了处理要求
- [ ] 结果包含具体改进建议（不仅仅是判分）
- [ ] Verdict 已给出并附理由
- [ ] 报告已输出到 `review/<skill-name>-quality-report.md`

## 验证失败处理

| 失败场景 | 处理方式 |
|---------|---------|
| 目标 SKILL.md 不存在 | 报告并跳过。不在不存在的文件上浪费时间。 |
| 目标不是 skill 目录 | 提示用户指定正确的 skill 路径。 |
| 用户要求同时审查 submodule | 说明 submodule 的 review 不在本 skill 范围内，建议在对应仓库中审查。 |
| 6 轴中有不适用项 | 标注 `-` 并在括号中记录理由（如："无需失败模式表，技能仅 3 步"）。 |
| 大量 Critical 问题 | 按优先级修复轴 1-3，再修复 4-6，每轮修复后重审。 |
