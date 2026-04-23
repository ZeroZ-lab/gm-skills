---
name: ui-fork
description: 从一张或多张 UI 截图中提炼产品级设计系统草案、组件规则、design tokens 和后续 AI 延续设计约束。Use when users want to analyze UI screenshots, fork an interface style, create reusable design guidelines from images, extract implementation-oriented design-system specs, or generate prompt contracts for future AI-generated pages.
argument-hint: "[UI 截图/产品背景/输出模式 brief|guide|system/是否保存为 DESIGN.md]"
---

# ui-fork

Convert one or more UI screenshots into a reusable, implementation-oriented design system specification.

This skill is a **UI Screenshot -> Design System Draft Engine**. It is not for aesthetic commentary. It should compress good UI into assets that another AI, designer, or frontend engineer can continue using.

## Core Contract

Always produce a structured design asset, not a loose visual review.

The output must extract the interface on five layers:

- Product Intent: page type, page goal, user task, reading path.
- Structural System: regions, hierarchy, grid, density, module grouping.
- Visual System: color, typography, spacing, radius, border, shadow, theme mapping.
- Component System: role, anatomy, reuse rule, variable parts, invariant parts.
- Continuation Contract: rules future AI-generated designs must follow.

Default output language is Chinese. Use another language only if the user asks for it.

Default mode is `guide`. If the user says "tokens", "落地", "实现", "设计系统", or "DESIGN.md", use `system` unless they explicitly request a lighter output.

Do not ask for language or file-save preferences before analysis. Ask only when a missing decision would change the result materially, or when writing/overwriting a file requires confirmation.

## Inputs

Accept any combination of:

- One or more UI screenshots.
- Product background, target users, business goal, brand constraints.
- Output mode: `brief`, `guide`, or `system`.
- Follow-up goal: create a design guide, extend this style, generate tokens, write `DESIGN.md`, or prepare constraints for another AI.

If product context is missing, infer the likely context from the screenshot and label it as inference in `Confidence Split`.

## Output Modes

### brief

Use for quick style capture across many screenshots. Output:

- 页面类型与目标
- 结构骨架
- 核心视觉特征
- 核心组件
- AI 延续约束
- 关键不确定项

### guide

Use `templates/output_template.md`. Output the full design specification:

- Design Brief
- Structural System
- Visual System
- Component System
- Interaction Assumptions
- Design Tokens Draft
- Prompt Contract
- Confidence Split

For tone and depth, use `examples/directory_ai_navigation_guide_output.md` as the reference quality bar: the output should read like a reusable design guide, not like a screenshot caption.

### system

Use `guide` plus stronger implementation detail:

- Full token draft using `templates/tokens_template.yaml`.
- Component anatomy for every major component.
- Semantic token suggestions.
- Reuse rules and failure modes.
- Implementation hints for design handoff.

Even in `system` mode, do not write frontend code unless the user explicitly asks for implementation.

## Workflow

### 1. Inspect before interpreting

Start with concrete observations from the screenshot:

- Visible page regions.
- Visible content hierarchy.
- Visible components.
- Visible theme, typography, spacing, surfaces, dividers, and interaction affordances.

Do not jump directly to style labels such as "clean", "modern", or "premium".

### 2. Classify the page type

Identify the primary page type before writing the guide:

- Marketing / 官网型
- Dashboard / 数据看板型
- Workspace / 工作台型
- Directory / 导航聚合型
- Content / 内容阅读型
- Tool / 工具型
- Form / 流程录入型
- Mobile App / 移动端界面
- AI Workbench / AI 工作台型

If the page is mixed, name the primary type and secondary type. Read `references/page_types.md` when the page type is ambiguous or when using `system` mode.

### 3. Separate observation, inference, and unknowns

Keep these categories distinct throughout the output:

- Direct observations: facts clearly visible in the screenshot.
- Likely inferences: judgments based on UI patterns and context.
- Unknowns: items the screenshot cannot confirm.

Never present an inferred font family, exact hex value, exact spacing value, hover state, or breakpoint as confirmed unless the screenshot or user explicitly provides it.

### 4. Extract structural logic

Convert the screenshot from a picture into a reusable layout system:

- Page-level regions and their order.
- Primary, secondary, navigation, action, and support zones.
- Grid, columns, container width, and responsive assumptions.
- Module grouping and repetition rules.
- Information density and scanning path.

### 5. Extract visual logic

Describe visual decisions as system rules:

- Background, surface, text, accent, state, and border relationships.
- Typography hierarchy across headings, body, labels, metadata, and numbers.
- Spacing rhythm at page, module, and component levels.
- Radius scale and where each radius level applies.
- Border, shadow, elevation, and surface strategy.
- Light/dark token mapping when multiple themes are visible.

Values may be approximate, but approximate values must be labeled as estimates.

### 6. Extract component logic

For each important visible component, output:

- 作用
- 结构
- 层级
- 复用规则
- 可变项
- 不可变项

Only analyze components that are visible or directly implied by the page type. Do not invent components to fill a template.

### 7. Infer interaction carefully

Interaction rules are usually inferred from static screenshots. Label them as assumptions:

- Hover, focus, active, selected, disabled states.
- Filter, tab, navigation, search, and theme-switch behavior.
- Motion duration, easing, and where animation is allowed.
- Loading, empty, error, and success states when relevant to the page type.

### 8. Produce tokens as draft assets

Use `templates/tokens_template.yaml` for token shape. Tokens are draft implementation hints, not final truth.

Rules:

- Prefer semantic tokens over one-off values.
- Use token references for component rules, such as `{color.brand.primary}`.
- Mark estimated values as estimated.
- Leave unconfirmable values blank or label them as unknown.
- Do not overfit tokens to one screenshot if multiple screenshots imply a broader system.

### 9. Write a strong Prompt Contract

Prompt Contract is a primary deliverable. Use `templates/prompt_contract_template.md` when writing `guide` or `system` output.

It must define:

- What future AI outputs must inherit.
- What may vary.
- What must not be broken.
- How new components should extend the system.
- Which decorative moves are forbidden unless explicitly present or requested.

### 10. Quality gate

Before finalizing, self-check against `templates/rubric.md`.

The output is acceptable only if it:

- Identifies page type and user intent.
- Extracts reusable structure, not just visible details.
- Explains component reuse and invariants.
- Provides implementation-oriented tokens or token placeholders.
- Contains a concrete Prompt Contract.
- Clearly separates observations, inferences, and unknowns.
- Could be reused as an AI design input document, frontend implementation seed, or design-system seed.

If the output would score below 32/40, revise it before responding. Do not expose a long scoring report unless the user asks.

## Optional DESIGN.md Output

Only write a `DESIGN.md` file when the user asks to save, generate, create, update, or persist the design guide.

When writing `DESIGN.md`:

1. Check whether `DESIGN.md` already exists.
2. If it does not exist, create it directly.
3. If it exists, do not overwrite silently. Ask whether to overwrite, append, or merge.
4. Use the same fixed Markdown structure as `templates/output_template.md`.
5. In `system` mode, include YAML front matter only if the user asks for machine-readable tokens or if the existing `DESIGN.md` already uses front matter.

## Prohibited Output

Read `references/anti_patterns.md` when output feels generic. Never:

- Write vague praise without system explanation.
- Stop at color and font summary.
- Confuse observation with inference.
- Invent exact hex, font, spacing, or breakpoint values.
- Flatten every page into the same template regardless of page type.
- Generate frontend code unless requested.
- Add glassmorphism, glow, noise, complex gradients, or 3D effects without evidence.
- Write a weak Prompt Contract such as "keep the style consistent".

## Final Response Style

Be structured, concise, and implementation-oriented.

Lead with the design system result, not with process commentary. Prefer rules, reusable patterns, and constraints over taste adjectives. The final result should be usable as:

- A design guide for humans.
- A token draft for frontend implementation.
- A prompt contract for future AI-generated pages.
- A reference spec for extending the same UI language.
