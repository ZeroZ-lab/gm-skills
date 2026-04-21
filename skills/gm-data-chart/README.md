# gmdiagram — GM Data Chart Skill

A Claude Code and Codex skill that generates professional data visualization charts from natural language descriptions. Supports 9 chart types, 12 visual styles, and 4 output formats.

Source repository: `https://github.com/ZeroZ-lab/gmdiagram`

## Features

- **9 chart types**: Bar, Pie/Donut, Line, Area, Scatter, Radar, Funnel, Bubble, Table
- **12 visual styles**: Dark Professional, Hand-Drawn Sketch, Light Corporate, Cyberpunk Neon, Blueprint, Warm Cozy, Minimalist, Terminal Retro, Pastel Dream, Notion, Material, Glassmorphism
- **4 output formats**: HTML, SVG, Mermaid, PNG/PDF (via export script)
- **Structured generation**: Two-step process (JSON schema → output) for reliable results
- **Self-contained output**: Single file, no JavaScript, no external dependencies

## Quick Start

### Install

#### Claude Code

Clone this repository, add it as a local Claude Code marketplace, then install the `gm-data-chart` plugin from that marketplace:

```bash
/plugin marketplace add ZeroZ-lab/gmdiagram
/plugin install gm-data-chart@gmdiagram-marketplace
```

#### Codex

Clone this repository locally and use the bundled Codex metadata:

- Plugin manifest: `gm-data-chart/.codex-plugin/plugin.json`
- Marketplace entry: `.agents/plugins/marketplace.json`

The Claude and Codex variants share the same `skills/`, `assets/`, and `scripts/` directories, so the behavior stays aligned across both environments.

### Use

Just ask Claude to create a chart:

```
> Draw a bar chart showing Q1-Q4 sales data

> Create a pie chart of market share by company

> Generate a line chart of website traffic over 12 months

> Make a scatter plot showing height vs weight correlation

> Design a radar chart comparing product features

> 画一个柱状图，显示各部门的年度预算
```

## Chart Types

| Type | Trigger Keywords | Best For |
|------|-----------------|----------|
| **Bar** | bar chart, column chart, 柱状图, 条形图 | Comparing categories, ranking |
| **Pie/Donut** | pie chart, donut chart, 饼图, 环形图 | Showing proportions, percentages |
| **Line** | line chart, trend, 折线图 | Time series, trends over time |
| **Area** | area chart, stacked area, 面积图 | Cumulative values, volume |
| **Scatter** | scatter plot, correlation, 散点图 | Relationships between variables |
| **Radar** | radar chart, spider chart, 雷达图 | Multi-dimensional comparison |
| **Funnel** | funnel chart, conversion, 漏斗图 | Pipeline stages, conversion rates |
| **Bubble** | bubble chart, 气泡图 | Three-dimensional data (x, y, size) |
| **Table** | data table, comparison table, 表格 | Precise values, detailed comparison |

## Visual Styles

| Style | Background | Best For |
|-------|-----------|----------|
| **Dark Professional** | Deep dark (#020617) | Technical articles, dashboards |
| **Hand-Drawn Sketch** | Light beige (#faf8f5) | Teaching, brainstorming |
| **Light Corporate** | White (#f8fafc) | Business presentations |
| **Cyberpunk Neon** | Catppuccin dark (#11111b) | Developer tools, tech content |
| **Blueprint** | Nord dark (#2e3440) | Engineering specs, reports |
| **Warm Cozy** | Warm cream (#f9f5eb) | Tutorials, non-technical audiences |
| **Minimalist** | Pure white (#ffffff) | Technical docs, print |
| **Terminal Retro** | CRT black (#0a0a0a) | Developer blogs, fun |
| **Pastel Dream** | Lavender (#fef7ff) | Education, presentations |
| **Notion** | Notion-style light | Documentation, wikis |
| **Material** | Material Design 3 | Google-style interfaces |
| **Glassmorphism** | Frosted glass effect | Modern UI, portfolios |

## Output Formats

| Format | Description | Command |
|--------|-------------|---------|
| **HTML** | Single file with inline SVG (default) | Specify `format: "html"` or omit |
| **SVG** | Standalone SVG for vector editors | Specify `format: "svg"` |
| **Mermaid** | Text syntax for GitHub/Notion | Specify `format: "mermaid"` (limited support) |
| **PNG/PDF** | Image export via script | `../gm-architecture/skills/gm-architecture/scripts/export.sh chart.html --format png` |

### PNG/PDF Export

The export script is shared with the gm-architecture plugin:

```bash
# Requirements: Node.js (PNG) or rsvg-convert (PDF)
../gm-architecture/skills/gm-architecture/scripts/export.sh chart.html --format png
../gm-architecture/skills/gm-architecture/scripts/export.sh chart.html --format pdf
../gm-architecture/skills/gm-architecture/scripts/export.sh chart.svg --format png --output my-chart.png
```

## File Structure

```
gm-data-chart/
├── .claude-plugin/
│   └── plugin.json                   # Claude plugin manifest
├── .codex-plugin/
│   └── plugin.json                   # Codex plugin manifest
├── README.md                         # Plugin overview
└── skills/
    └── gm-data-chart/
        ├── SKILL.md                  # Core instructions + dispatcher
        ├── README.md                 # This file
        ├── references/
        │   ├── design-system.md      # Colors, typography, spacing
        │   ├── chart-type-registry.md # All chart types registry
        │   ├── render-bar.md         # Bar chart render rules
        │   ├── render-pie.md         # Pie chart render rules
        │   ├── render-line.md        # Line chart render rules
        │   ├── render-area.md        # Area chart render rules
        │   ├── render-scatter.md     # Scatter chart render rules
        │   ├── render-radar.md       # Radar chart render rules
        │   ├── render-funnel.md      # Funnel chart render rules
        │   ├── render-bubble.md      # Bubble chart render rules
        │   ├── render-table.md       # Table render rules
        │   └── style-*.md            # Style guides (shared)
        │
        └── assets/
            ├── schema-bar.json       # Bar chart JSON Schema
            ├── schema-pie.json       # Pie chart JSON Schema
            ├── schema-line.json      # Line chart JSON Schema
            ├── schema-*.json         # Other chart schemas
            ├── template-*.html       # Style templates
            └── examples/
```

## How It Works

```
Natural Language → [LLM extracts] → JSON Schema → [Render rules] → SVG → Output format
```

1. **Schema first**: Structure captured in JSON (data series, labels, values, config)
2. **Rendering second**: Render rules compute coordinates, SVG components assembled
3. **Output**: Wrapped in HTML, or output as standalone SVG, Mermaid text, or PNG/PDF

## License

MIT
