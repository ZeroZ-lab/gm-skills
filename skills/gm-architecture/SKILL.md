---
name: gm-architecture
description: >
  Generate professional architecture diagrams from system descriptions.
  Creates single-file HTML with inline SVG that can be opened in any browser.
  Use this skill whenever the user asks to create, draw, or generate:
  architecture diagrams, system diagrams, infrastructure diagrams, layered architecture,
  component diagrams, platform capability maps, process architecture, microservice architecture,
  system design diagrams, architecture visualization, tech stack diagrams,
  flowchart, flow chart, decision tree, process flow,
  mind map, mindmap, brainstorm, concept map,
  ER diagram, entity relationship, database schema, data model,
  sequence diagram, interaction diagram, message flow, API flow, protocol flow,
  social card, knowledge card, comparison card, quote card, ranked list card,
  知识卡片, 社交卡片, 分享图, 对比卡片, 引用卡片, 排行卡片,
  分层架构图, 系统架构图, 架构图, 流程图, 思维导图, ER图, 序列图, 时序图,
  or wants to visualize how a system works.
  Supports 9 diagram types and 12 visual styles: dark-professional, hand-drawn, light-corporate, cyberpunk-neon, blueprint, warm-cozy, minimalist, terminal-retro, pastel-dream, notion, material, glassmorphism.
  Supports 4 output formats: html, svg, mermaid, png/pdf (via export script).
---

# gmdiagram — GM Architecture Skill

## What This Skill Does

Generate publication-quality diagrams as standalone files. The output can be:
- **HTML**: Single `.html` file with inline SVG and embedded CSS (default, no JavaScript)
- **SVG**: Standalone `.svg` file
- **Mermaid**: Mermaid text syntax (paste into GitHub, Notion, etc.)
- **PNG/PDF**: Via the export script at `scripts/export.sh`

## Output Directory Structure

All example files must be output to the correct directory structure:

```
assets/examples/
├── {example-name}.json      # JSON schema file
├── {example-name}.html      # HTML rendered output (same name as JSON)
└── images/                  # For preview screenshots only
    └── {example-name}-preview.png
```

### Rules

**Correct approach**:
- HTML and JSON files go in the `examples/` root directory
- Preview images go in the `examples/images/` subdirectory
- Filenames must be consistent (only extensions differ)

**Prohibited approach**:
- Do NOT put HTML files in the `images/` directory
- Do NOT generate any non-image files in the `images/` directory
- Do NOT put JSON files in subdirectories (unless there's explicit categorization need)

### Example

For the `chrome-architecture` example:
- `assets/examples/chrome-architecture.json`
- `assets/examples/chrome-architecture.html`
- `assets/examples/images/chrome-architecture-preview.png`
- `assets/examples/images/chrome-architecture.html` (WRONG: HTML should not be in images/)

## Interactive Selection

When the user's request does NOT already specify all three choices (diagram type, style, output format), use the `AskUserQuestion` tool to let the user choose.

**Important**: `AskUserQuestion` supports at most **4 options per question** and **4 questions per call**. When there are more than 4 choices, split into two calls or use the auto-infer + confirm pattern below.

### Selection Strategy

For each dimension, follow this logic:

1. **Can the choice be inferred from the user's description?** → Skip asking, use the inferred value directly.
2. **Does the user explicitly state it?** → Skip asking, use the stated value.
3. **Still ambiguous?** → Ask via `AskUserQuestion`.

### Question 1 — Diagram Type (ask only if ambiguous)

The user's description usually makes the type obvious. Only ask when multiple types could fit.

```
question: "Which diagram type fits your needs?"
header: "Type"
multiSelect: false
options:
  - label: "Architecture"
    description: "System layers, services, infrastructure, platform maps"
  - label: "Flowchart"
    description: "Process flow, decision tree, branching logic"
  - label: "Mind Map"
    description: "Topic hierarchy, brainstorm, feature tree"
  - label: "Other"
    description: "ER Diagram, Sequence, Gantt, UML Class, Network, or Card"
```

If the user picks "Other", ask a follow-up:
```
question: "Which specific type?"
header: "Type"
multiSelect: false
options:
  - label: "ER Diagram"
    description: "Database tables, entities, relationships, data model"
  - label: "Sequence Diagram"
    description: "Message flow, API calls, protocol, interaction between actors"
  - label: "Gantt Chart"
    description: "Project timeline, milestones, task scheduling"
  - label: "Card"
    description: "Social sharing card — knowledge, comparison, quote, or ranked list"
  - label: "More"
    description: "UML Class Diagram or Network Topology"
```

If the user picks "More", ask a final follow-up:
```
question: "Which type?"
header: "Type"
multiSelect: false
options:
  - label: "UML Class Diagram"
    description: "OOP design, classes, inheritance, interfaces"
  - label: "Network Topology"
    description: "Servers, routers, subnets, network architecture"
```

### Question 2 — Visual Style (always ask unless user named a style)

Split into three style families. First call asks for family:

**First call:**
```
question: "Which style family?"
header: "Style"
multiSelect: false
options:
  - label: "Dark"
    description: "Dark Professional, Cyberpunk Neon, or Terminal Retro"
  - label: "Light / Clean"
    description: "Light Corporate, Minimalist, Warm Cozy, or Notion"
  - label: "Creative"
    description: "Hand-Drawn, Blueprint, Pastel Dream, Material, or Glassmorphism"
```

Then follow up based on the family:

**Dark follow-up:**
```
options:
  - label: "Dark Professional (Recommended)"
    description: "Neon accents, tech articles, docs, presentations"
  - label: "Cyberpunk Neon"
    description: "Catppuccin dark, vivid neon, developer tools"
  - label: "Terminal Retro"
    description: "CRT green-on-black, scanlines, developer blogs"
```

**Light follow-up:**
```
options:
  - label: "Light Corporate"
    description: "Clean white, muted palette, enterprise reviews"
  - label: "Minimalist"
    description: "Monochrome, ultra-thin borders, maximum whitespace"
  - label: "Warm Cozy"
    description: "Warm cream, soft tones, tutorials"
  - label: "Notion"
    description: "Notion-like document aesthetic, system fonts, subtle borders"
```

**Creative follow-up:**
```
options:
  - label: "Hand-Drawn Sketch"
    description: "Warm beige, sketchy borders, whiteboard feel"
  - label: "Blueprint"
    description: "Nord blue, grid lines, engineering specs"
  - label: "Pastel Dream"
    description: "Soft pastels, rounded corners, playful"
  - label: "More"
    description: "Material Design or Glassmorphism"
```

If user picks "More":
```
options:
  - label: "Material Design"
    description: "Google Material, bold fills, elevation shadows, Roboto font"
  - label: "Glassmorphism"
    description: "Frosted glass, translucent layers, gradient background"
```

### Question 3 — Output Format (always ask unless user named a format)

```
question: "Which output format?"
header: "Format"
multiSelect: false
options:
  - label: "HTML (Recommended)"
    description: "Single file with inline SVG, opens in any browser"
  - label: "SVG"
    description: "Standalone SVG for vector editors (Figma, Illustrator)"
  - label: "Mermaid"
    description: "Text syntax, paste into GitHub, Notion, or markdown"
  - label: "PNG / PDF"
    description: "Image export via script (requires Node.js or rsvg-convert)"
```

### How to Combine Questions

Minimize the number of `AskUserQuestion` calls:

- **User specified nothing**: First call asks Type + Style family + Format (3 questions). Then a follow-up call if they picked "Other" type or "Creative" style.
- **User specified type only**: Ask Style family + Format (2 questions). Follow-up if "Creative" style.
- **User specified type + style**: Ask Format only (1 question, 1 call).
- **User specified everything**: Skip all selection, proceed directly to generation.

### Rules

1. If the user already specified all three, skip selection entirely.
2. Only ask about dimensions the user hasn't specified.
3. Put `(Recommended)` on the default/first option for style and format.
4. After all selections are made, proceed to the Two-Step Generation Process below.

### Density (default: normal, never ask)

Density defaults to `"normal"`. Infer from the user's description — never ask via AskUserQuestion:
- "compact" / "dense" / "tight" / "紧凑" → `"compact"`
- "spacious" / "spread out" / "presentation" / "宽松" → `"spacious"`
- Otherwise → `"normal"`

When density differs from normal, read the "Density Multipliers" section in the corresponding layout reference file to get adjusted spacing constants.

### Direction (default: TB, never ask)

Direction defaults to `"TB"` (top-to-bottom). Only applies to `architecture` and `flowchart`. Infer from user description:
- "left to right" / "horizontal" / "LR" / "从左到右" → `"LR"`
- Otherwise → `"TB"`

When direction is `"LR"`, read the "LR Mode" section in the layout reference file for transformed coordinate rules. ER, sequence, and mindmap diagrams always use their inherent layout — ignore direction for these types.

### Font and Color Overrides (ask only if user requests)

After all selections, if the user mentions custom colors, fonts, or brand colors, apply overrides from the `font` and `colors` fields in the JSON schema.

**Font override:** When `font` is set, add a Google Fonts `<link>` in the HTML `<head>` and replace all `font-family` declarations with the user's font as primary.

**Color overrides:** When `colors` object is present:
- `colors.primary` replaces the style's primary accent/border color
- `colors.secondary` replaces subtle border and background colors
- `colors.accent` replaces highlight colors
- `colors.background` replaces the page background color
- `colors.text` replaces primary text color

Apply overrides LAST, after all style template values are resolved. Override colors replace corresponding values in type color mapping, connection lines, and legend swatches.

### Metadata Version Field

生成 JSON 时，metadata.version 必须遵循以下规则：

- **格式**: 必须符合 SemVer (Semantic Versioning) 格式: `major.minor.patch`
- **示例**: `"0.6.1"`, `"1.2.0"`, `"2.0.0"`
- **禁止的占位符版本**: `"0.0.0"`, `"1.0"`, `"1.0.0"`

**推荐的版本策略**:
建议使用与插件版本一致的值，但不做强制要求。重要的是保持格式规范。

**JSON 示例**:
```json
"metadata": {
  "author": "gmdiagram",
  "date": "2026-04-14",
  "version": "0.6.1"
}
```

**验证规则**:
- 必须包含 3 个数字段，用点号分隔
- 每段必须是纯数字
- 不允许前导零（如 `"01.02.03"` 无效）

## Two-Step Generation Process

ALWAYS follow these two steps in order. Never skip to output directly.

### Step 1: Generate JSON Schema

Read the user's description and extract structure into the JSON schema for the selected diagram type. Each type has its own schema file in `assets/`:

| Diagram Type | Schema File |
|---|---|
| `architecture` | `assets/schema-architecture.json` |
| `flowchart` | `assets/schema-flowchart.json` |
| `mindmap` | `assets/schema-mindmap.json` |
| `er` | `assets/schema-er.json` |
| `sequence` | `assets/schema-sequence.json` |
| `gantt` | `assets/schema-gantt.json` |
| `uml-class` | `assets/schema-uml-class.json` |
| `network` | `assets/schema-network.json` |

Key rules across all types:
- Every component gets a unique `id` (kebab-case)
- Use semantic `type` values as defined in each schema
- If the user doesn't specify a style, use `dark-professional`
- If the user doesn't specify a format, use `html`
- If the user doesn't specify a density, use `normal`
- If the user doesn't specify a direction, use `TB` (architecture/flowchart only)
- Components can reference icons via the `"icon"` field (see `references/icons-catalog.md`)

Output the JSON first, then proceed to Step 2.

### Step 2: Generate Output

Read the diagram-type reference file for generation instructions:

1. **Choose template**: Based on the `style` field, read the corresponding style reference and template:
   - `dark-professional` → `references/style-dark-professional.md` → `assets/template-dark.html`
   - `hand-drawn` → `references/style-hand-drawn.md` → `assets/template-sketch.html`
   - `light-corporate` → `references/style-light-corporate.md` → `assets/template-light-corporate.html`
   - `cyberpunk-neon` → `references/style-cyberpunk-neon.md` → `assets/template-cyberpunk-neon.html`
   - `blueprint` → `references/style-blueprint.md` → `assets/template-blueprint.html`
   - `warm-cozy` → `references/style-warm-cozy.md` → `assets/template-warm-cozy.html`
   - `minimalist` → `references/style-minimalist.md` → `assets/template-minimalist.html`
   - `terminal-retro` → `references/style-terminal-retro.md` → `assets/template-terminal-retro.html`
   - `pastel-dream` → `references/style-pastel-dream.md` → `assets/template-pastel-dream.html`
   - `notion` → `references/style-notion.md` → `assets/template-notion.html`
   - `material` → `references/style-material.md` → `assets/template-material.html`
   - `glassmorphism` → `references/style-glassmorphism.md` → `assets/template-glassmorphism.html`

2. **Compute layout**: Follow the coordinate calculation rules in the diagram-type-specific layout file.

3. **Build SVG**: Use the component SVG snippets from the diagram-type-specific components file.

4. **Wrap in HTML** (if format=html): Use the corresponding template file as the starting structure.

   **HTML Language Attribute**

   根据内容语言设置正确的 `<html lang="...">` 属性：

   | 内容语言 | lang 属性值 | 使用场景 |
   |----------|-------------|----------|
   | 英文 | `en` | 标题、标签、描述均为英文 |
   | 简体中文 | `zh-CN` | 标题、标签、描述包含简体中文 |
   | 繁体中文 | `zh-TW` | 标题、标签、描述包含繁体中文 |
   | 日文 | `ja` | 标题、标签、描述包含日文 |

   **自动检测规则**

   使用以下启发式规则判断内容语言：

   1. **检查 title 字段**: 如果包含中文字符（`\u4e00-\u9fff`），使用 `zh-CN`
   2. **检查 subtitle 字段**: 如果包含中文字符，使用 `zh-CN`
   3. **检查主要 labels**: 如果超过 50% 的标签包含中文，使用 `zh-CN`
   4. **默认**: 如果不确定或混合语言，使用 `en`

   **示例**

   *中文内容示例*:
   ```html
   <html lang="zh-CN">
   <head><title>系统架构图</title></head>
   ```

   *英文内容示例*:
   ```html
   <html lang="en">
   <head><title>Chrome Multi-Process Architecture</title></head>
   ```

   **重要性**

   正确的 `lang` 属性有助于：
   - 屏幕阅读器正确发音
   - 浏览器正确渲染字体
   - SEO 优化

For other formats:
- **SVG**: Follow `references/output-svg.md` — extract standalone SVG
- **Mermaid**: Follow `references/output-mermaid.md` — transform JSON to Mermaid text
- **PNG/PDF**: First generate HTML or SVG, then run `scripts/export.sh` (see `references/output-png-pdf.md`)

## Design Principles

1. **Diagrams should argue, not just display** — every element should contribute to understanding
2. **Structure first, aesthetics second** — correct relationships matter more than visual polish
3. **Label everything meaningful** — connections need labels, components need names
4. **Consistency over creativity** — use the defined color system, don't invent new colors
5. **No JavaScript** — the output must work without any scripting (HTML/SVG formats)
6. **Escape all user text** — HTML-entity-escape `<`, `>`, `&`, `"`, `'` in all labels, titles, and descriptions before inserting into SVG/HTML to prevent XSS

## Diagram Type Reference

When the diagram type is clear from context (or after the user selects it), use this mapping:

| Diagram Type | Reference File | Schema File |
|---|---|---|
| `architecture` | `references/diagram-architecture.md` | `assets/schema-architecture.json` |
| `flowchart` | `references/diagram-flowchart.md` | `assets/schema-flowchart.json` |
| `mindmap` | `references/diagram-mindmap.md` | `assets/schema-mindmap.json` |
| `er` | `references/diagram-er.md` | `assets/schema-er.json` |
| `sequence` | `references/diagram-sequence.md` | `assets/schema-sequence.json` |
| `gantt` | `references/diagram-gantt.md` | `assets/schema-gantt.json` |
| `uml-class` | `references/diagram-uml-class.md` | `assets/schema-uml-class.json` |
| `network` | `references/diagram-network.md` | `assets/schema-network.json` |
| `card` | `references/diagram-card.md` | `assets/schema-card.json` |

Read the diagram-type-registry at `references/diagram-type-registry.md` for detailed trigger keywords.

## Iteration Workflow

After generating the initial diagram, the user may request changes:
- Add/remove components → update JSON, recompute layout
- Change a connection → update JSON connections, recompute paths
- Change style → switch template, keep same JSON
- Change diagram type → re-extract JSON for new type, regenerate
- Change output format → regenerate from existing JSON

## File Naming Convention

示例文件名必须使用 **kebab-case**（短横线连接的小写字母）。

### 命名格式

```
{context}-{type}[-{variant}].{ext}
```

- **context**: 场景描述（如 chrome, saas, ecommerce, quarterly-revenue）
- **type**: 图表类型（可选，如 architecture, flowchart, bar-chart）
- **variant**: 变体标识（可选，如 cyberpunk, minimalist, dark）
- **ext**: 文件扩展名（json 或 html）

### 正确与错误示例

| 命名风格 | 示例 | 状态 |
|----------|------|------|
| **kebab-case** ✅ | `chrome-architecture.json` | 正确 |
| **kebab-case** ✅ | `quarterly-revenue.json` | 正确 |
| **kebab-case** ✅ | `team-skills-radar.json` | 正确 |
| camelCase ❌ | `chromeArchitecture.json` | 错误 |
| PascalCase ❌ | `QuarterlyRevenue.json` | 错误 |
| snake_case ❌ | `team_skills.json` | 错误 |
| 空格 ❌ | `chrome architecture.json` | 错误 |

### 规则

1. **全部小写**: 文件名中不包含大写字母
2. **单词分隔**: 使用连字符 `-` 分隔单词，不使用下划线或空格
3. **无特殊字符**: 仅使用字母、数字和连字符
4. **清晰语义**: 文件名应清晰表达示例内容

### 批量命名示例

对于同一系统的多个风格变体：
- `architecture-system.json` (默认风格)
- `architecture-system-cyberpunk.json`
- `architecture-system-minimalist.json`
- `architecture-system-terminal.json`

## Quality Checklist

Before delivering, verify:
- [ ] JSON validates against the diagram type's schema
- [ ] Every `<foreignObject>` has `xmlns="http://www.w3.org/1999/xhtml"` on the root HTML element
- [ ] Component boxes use CSS classes from the template (`.module`, `.type-X`, `.module-label`)
- [ ] Flowchart `io` nodes use matched SVG parallelogram mask + visible polygon geometry; never use rectangular masks behind clipped shapes
- [ ] SVG `<text>` (connection labels only) has `text-anchor="middle" dominant-baseline="central"`
- [ ] Connection lines route around intermediate layers (never cross through layer cards)
- [ ] Masking rects cover full layer area (hides arrows behind components)
- [ ] **Every layer height is exactly LAYER_H_BADGE (116) or LAYER_H_SIMPLE (101) — NEVER custom heights like 49, 80, or 106**
- [ ] **NO overlapping layers: gap between every pair of adjacent layers = exactly 50px**
- [ ] Layer y-positions are correctly stacked: `layer_y[i] = layer_y[i-1] + h + gap`
- [ ] ViewBox fits all content with no clipping and no more than 40px whitespace margin
- [ ] Legend matches the component types used
- [ ] Title and subtitle are accurate
- [ ] Icons (if used) are correctly colored and positioned
