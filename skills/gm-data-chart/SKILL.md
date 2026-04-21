---
name: gm-data-chart
description: >
  Generate data visualization charts from natural language descriptions.
  Creates single-file HTML with inline SVG that can be opened in any browser.
  Use this skill whenever the user asks to create, draw, or generate:
  bar chart, column chart, 柱状图, 条形图, pie chart, donut chart, 饼图, 环形图,
  line chart, area chart, 折线图, 面积图, scatter chart, scatter plot, 散点图,
  radar chart, spider chart, 雷达图, 蜘蛛图, funnel chart, 漏斗图, conversion,
  bubble chart, 气泡图, data table, table chart, 表格, 数据表, data visualization,
  chart, 数据可视化, 图表, or wants to visualize data, compare values, show trends,
  show proportions, analyze correlation, multi-dimensional comparison.
  Supports 9 chart types and 12 visual styles.
  Supports 4 output formats: html, svg, mermaid, png/pdf (via export script).
---

# gmdiagram — GM Data Chart Skill

## What This Skill Does

Generate publication-quality data visualization charts as standalone files. The output can be:
- **HTML**: Single `.html` file with inline SVG and embedded CSS (default, no JavaScript)
- **SVG**: Standalone `.svg` file
- **Mermaid**: Text syntax (limited chart support, see Mermaid rules)
- **PNG/PDF**: Via the export script at `../gm-architecture/skills/gm-architecture/scripts/export.sh`

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

When the user's request does NOT already specify all three choices (chart type, style, output format), use the `AskUserQuestion` tool to let the user choose.

**Important**: `AskUserQuestion` supports at most **4 options per question** and **4 questions per call**.

### Selection Strategy

For each dimension, follow this logic:

1. **Can the choice be inferred from the user's description?** → Skip asking, use the inferred value directly.
2. **Does the user explicitly state it?** → Skip asking, use the stated value.
3. **Still ambiguous?** → Ask via `AskUserQuestion`.

### Question 1 — Chart Type (ask only if ambiguous)

The user's description usually makes the type obvious. Only ask when multiple types could fit. Since there are 9 chart types, split into groups:

**First ask which group:**

```
question: "Which chart category fits your needs?"
header: "Category"
options:
  - label: "Comparison"
    description: "Bar chart — compare categories with bars"
  - label: "Proportion"
    description: "Pie / Donut — show proportions of a whole"
  - label: "Trend / Distribution"
    description: "Line / Area / Scatter — show trends, area, or correlation"
  - label: "Special"
    description: "Radar / Funnel / Bubble / Table — multi-axis, pipeline, 3D data, or grid"
```

**Then drill down within the category:**

- **Comparison** → Bar Chart (no further question needed)
- **Proportion** → Ask: "Pie or Donut?" (2 options, simple)
- **Trend / Distribution** → Ask: "Line / Area / Scatter?"
- **Special** → Ask: "Radar / Funnel / Bubble / Table?"

### Question 2 — Visual Style

Use the same 3-family approach as architecture-diagram:

```
First ask:
  "Which style family?" → Dark / Light+Clean / Creative

Then drill down within the family.
```

Infer from context when possible: technical content → dark, business → light-corporate, creative → cyberpunk/pastel.

### Question 3 — Output Format

Default is HTML. Only ask if the user mentions a specific use case (GitHub → Mermaid, print → SVG/PDF).

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

ALL chart generation follows exactly two steps. Never skip to output directly.

### Step 1 — Extract to JSON Schema

Extract data from the user's natural language description into the typed JSON schema for the chosen chart type.

**Schema files:**
| Chart Type | Schema File |
|---|---|
| bar | `assets/schema-bar.json` |
| pie | `assets/schema-pie.json` |
| line | `assets/schema-line.json` |
| area | `assets/schema-area.json` |
| scatter | `assets/schema-scatter.json` |
| radar | `assets/schema-radar.json` |
| funnel | `assets/schema-funnel.json` |
| bubble | `assets/schema-bubble.json` |
| table | `assets/schema-table.json` |

**Shared schema definitions** are in `assets/schema-shared.json` (styleEnum, formatEnum, legendConfig, axisConfig, scatterAxisConfig, sanitizedString, etc.). Individual schemas reference shared definitions via `$ref`.

**Critical: Nice Numbers algorithm runs in this step.**

Read `references/axis-and-grid.md` for the full algorithm. Compute Y-axis ticks and store them in `axis.y.ticks`. For scatter and bubble charts, compute Nice Numbers for **both X and Y axes** and store in `axis.x.ticks` and `axis.y.ticks`. This avoids complex math in Step 2.

**Data extraction rules:**
- Extract numeric values and labels from user text
- Infer series names when multiple data sets are mentioned
- When user provides percentages, store as raw values (not pre-multiplied)
- When user says "compare X and Y", infer grouped bar chart with 2 series
- All string fields have maxLength constraints — truncate if necessary with a note to the user
- **Scatter/Bubble**: Extract x/y pairs from user data. Infer axis labels from context (e.g., "height vs weight" → x label "Height", y label "Weight"). For bubble, also extract size values.
- **Radar**: Extract dimension labels (axes) and values per series. Ensure all series have the same number of data points as axes.
- **Funnel**: Extract stage names and values. Note that values should be in descending order; if not, auto-sort will be applied during rendering.
- **Table**: Extract column headers and row data. Ensure each row has a value for every column.

**Validation:**
- Bar/Line/Area: `series` max 8, `data` per series max 30. If exceeded, **must** ask user to simplify.
- Scatter: `series` max 8, `data` per series max 50.
- Bubble: `series` max 5, `data` per series max 30.
- Radar: `axes` min 3 max 12, `series` max 6, `data` length must match `axes` length.
- Pie/Funnel: `data` max 12 (pie) / max 8 (funnel). If exceeded, suggest merging smallest items into "Others" (pie) or simplifying stages (funnel).
- Table: `columns` min 2 max 12, `rows` max 50. Each row must contain all column keys.
- All `value` fields must be finite numbers (no NaN, Infinity).
- All `color` fields must match `^#[0-9a-fA-F]{6}$`.
- Radar `axes[].maxValue`: either all specified or all omitted (all-or-nothing). Partial specification is rejected in Step 1 validation.

### Step 2 — Render Output

Read the corresponding render reference and template, then generate SVG wrapped in HTML.

**Render references:**
| Chart Type | Render Reference |
|---|---|
| bar | `references/render-bar.md` |
| pie | `references/render-pie.md` |
| line | `references/render-line.md` |
| area | `references/render-area.md` |
| scatter | `references/render-scatter.md` |
| radar | `references/render-radar.md` |
| funnel | `references/render-funnel.md` |
| bubble | `references/render-bubble.md` |
| table | `references/render-table.md` |

**Shared references** (read for all chart types):
- `references/axis-and-grid.md` — axis, grid, tick rendering
- `references/color-palettes.md` — palette selection and color assignment

**Template:** Use `../../assets/template-{style}.html` (shared templates with chart CSS classes already added).

**Rendering approach — Hybrid Mode:**
- Data marks (bars, arcs, lines, dots): pure SVG native elements (`<rect>`, `<path>`, `<circle>`, `<line>`)
- Text (labels, legend, axis titles): `foreignObject` + CSS layout
- All `foreignObject` root elements must include `xmlns="http://www.w3.org/1999/xhtml"`

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
<head><title>2025年各季度营收</title></head>
```

*英文内容示例*:
```html
<html lang="en">
<head><title>Q1-Q4 Revenue Comparison</title></head>
```

**重要性**

正确的 `lang` 属性有助于：
- 屏幕阅读器正确发音
- 浏览器正确渲染字体
- SEO 优化

## Chart Type Reference

| Type | Trigger Keywords | Status |
|------|-----------------|--------|
| **bar** | bar chart, column chart, 柱状图, 条形图, 对比 | Available |
| **pie** | pie chart, donut chart, 饼图, 环形图, 占比, 比例, proportion, percentage | Available |
| **line** | line chart, line graph, 折线图, 趋势, trend, time series, 时间序列 | Available |
| **area** | area chart, 面积图, stacked area, 堆叠面积 | Available |
| **scatter** | scatter chart, scatter plot, 散点图, 相关性, correlation, distribution | Available |
| **radar** | radar chart, spider chart, 雷达图, 蜘蛛图, 多维, multi-dimensional | Available |
| **funnel** | funnel chart, 漏斗图, 转化率, conversion, pipeline, 管道 | Available |
| **bubble** | bubble chart, 气泡图, 三维数据, three-dimensional data | Available |
| **table** | data table, table chart, 表格, 数据表 | Available |

**Mermaid output matrix:**

| Type | Mermaid Support | Syntax |
|------|----------------|--------|
| Bar | Yes | `xychart-beta` |
| Pie | Yes | `pie title` |
| Line | Yes | `xychart-beta` |
| Area | No | — |
| Scatter | No | — |
| Radar | No | — |
| Funnel | No | — |
| Bubble | No | — |
| Table | No | — |

For chart types without Mermaid support, inform the user of the limitation and suggest HTML or SVG instead.

## Data Extraction Rules

- Extract numbers and labels directly from the user's description
- Support formats like "Q1=120万, Q2=150万" or "Chrome 65%, Safari 19%"
- Remove units from values (store "120" not "120万"), put units in `axis.y.label` or `subtitle`
- When multiple series are mentioned, create separate series objects
- Handle percentage input: if all values sum to ~100, they're percentages; store as-is

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

Before finalizing any chart output, verify ALL of the following:

### Data & Schema
- [ ] JSON validates against the chart type's schema file
- [ ] `axis.y.ticks` uses nice numbers (no awkward decimals unless data has decimals)
- [ ] For scatter/bubble: `axis.x.ticks` also uses nice numbers
- [ ] All values are finite numbers (no NaN or Infinity)
- [ ] Array sizes within limits (series, data, axes, columns, rows as per type constraints)

### Visual
- [ ] Bar width and spacing visually balanced
- [ ] Text labels readable (>= 11px, contrast >= 3:1 against background)
- [ ] ViewBox fits content — no clipping, no more than 20% whitespace
- [ ] Legend matches actual data series/colors
- [ ] Grid lines don't overlap with axis line

### Technical
- [ ] All `foreignObject` root elements have `xmlns="http://www.w3.org/1999/xhtml"`
- [ ] All user text is HTML-entity-escaped (`<`, `>`, `&` in text content; additionally `"` and control chars in attribute values)
- [ ] No user text in element name or attribute name positions
- [ ] Colors in `#rrggbb` format only — no `rgb()`, `rgba()`, named colors, `url()`
- [ ] No JavaScript in output
- [ ] ViewBox width and height are integers (no decimals)
- [ ] CSS classes match template definitions (`.axis-line`, `.grid-line`, `.bar`, `.tick-label`, etc.)

### Security
- [ ] No `<script` tags in output
- [ ] No `onerror`, `onload`, `onclick` or other event handler attributes
- [ ] No `url()` in inline style attributes
- [ ] No `<iframe>`, `<object>`, `<embed>` tags
- [ ] No extra `<style>` tags beyond what the template provides

### Bar Chart Specific
- [ ] Bars are proportional to data values
- [ ] Y-axis ticks evenly spaced
- [ ] X-axis labels centered under each bar/group
- [ ] Negative values handled correctly (bars extend below baseline)

### Pie Chart Specific
- [ ] Slice angles are proportional to data values
- [ ] Arcs start from 12 o'clock position (-90 degree offset)
- [ ] Donut variant: inner arc path has correct annular sector (sweep-flag = 0 for inner arc)
- [ ] Percentages computed and displayed correctly: `(item.value / totalValue * 100).toFixed(1)`
- [ ] Slices < 5% have no external label (still shown in legend)

### Line Chart Specific
- [ ] Edge-to-edge X spacing used (NOT grouped slots like bar chart): `pointX(g) = plotX + g * (plotWidth / (numDataPoints - 1))`
- [ ] Catmull-Rom smooth mode: phantom points computed correctly for boundary segments (`P[-1] = 2*P[0] - P[1]`, `P[n] = 2*P[n-1] - P[n-2]`)
- [ ] Data point markers match the specified shape (circle, square, diamond, none)

### Area Chart Specific
- [ ] Stacked mode: cumulative values computed correctly, top-to-bottom render order
- [ ] Overlaid mode: opacity applied correctly to each series fill
- [ ] Nice Numbers applied to cumulative max (stacked) or individual max (overlaid)
- [ ] Each area path closed to the baseline correctly

### Scatter Chart Specific
- [ ] Dual-axis Nice Numbers computed (both X and Y axes have ticks)
- [ ] Both axes display tick labels
- [ ] Triangle point shape rendered correctly (upright equilateral triangle)
- [ ] Data point labels only shown when `data[].label` is present

### Radar Chart Specific
- [ ] Concentric polygon grid drawn (not circular grid)
- [ ] `axes[].maxValue` is all-or-nothing: either all specified or all auto-computed
- [ ] Polygon vertices computed correctly using polar coordinates from center
- [ ] Data polygon normalized against per-axis maxValue
- [ ] Axis labels positioned outside the outer polygon edge

### Funnel Chart Specific
- [ ] Data auto-sorted in descending order if not already sorted
- [ ] Last stage has flat bottom (not tapered to a point)
- [ ] Conversion rates displayed between adjacent stages (when `showConversionRate: true`)
- [ ] Stage widths proportional to values relative to the maximum value

### Bubble Chart Specific
- [ ] Size mapped via area (r-squared), not linear radius: `area = minR^2 + (size - minSize) / (maxSize - minSize) * (maxR^2 - minR^2)`
- [ ] Render order: ascending by size (small bubbles drawn first, large on top)
- [ ] Dual numeric axes with Nice Numbers on both X and Y
- [ ] Size legend included showing min/max bubble mapping

### Table Chart Specific
- [ ] No SVG graphic elements — pure foreignObject + HTML table
- [ ] `sanitizedString` enforced on all cell content (no `<>` characters)
- [ ] Highlight colors are fixed system values (Max: green, Min: red), not user-customizable
- [ ] `columns[].width` matches pattern `^(\d{1,4}px|auto)$` — no arbitrary CSS values
- [ ] Table width matches column widths appropriately

## Iteration Workflow

Follow-up requests to modify an existing chart:

1. **Modify existing JSON** — add/remove data points, change series
2. **Re-render** from modified JSON
3. **Style change** — re-render with different template (keep JSON unchanged)
4. **Format change** — re-export to different output format

Common modifications:
- "Add another series" → add to `series` array, re-render
- "Change to horizontal" → set `direction: "horizontal"`, re-render
- "Stack the bars" → set `variant: "stacked"`, re-render
- "Switch to hand-drawn style" → change `style`, re-render with different template
- "Convert pie to donut" → set `variant: "donut"`, configure `donut` object, re-render
- "Smooth the lines" → set `smooth: true`, re-render
- "Show as stacked area" → set `variant: "stacked"` on area chart, re-render
