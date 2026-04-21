# gmdiagram — Architecture Diagram Skill

A Claude Code and Codex skill that generates professional diagrams from natural language descriptions. Supports 5 diagram types, 9 visual styles, and 4 output formats.

Source repository: `https://github.com/ZeroZ-lab/gmdiagram`

## Features

- **5 diagram types**: Architecture, Flowchart, Mind Map, ER Diagram, Sequence Diagram
- **9 visual styles**: Dark Professional, Hand-Drawn Sketch, Light Corporate, Cyberpunk Neon, Blueprint, Warm Cozy, Minimalist, Terminal Retro, Pastel Dream
- **4 output formats**: HTML, SVG, Mermaid, PNG/PDF (via export script)
- **150+ icons**: Curated from Tabler Icons and Simple Icons for richer visual expression
- **Structured generation**: Two-step process (JSON schema → output) for reliable results
- **Self-contained output**: Single file, no JavaScript, no external dependencies

## Quick Start

### Install

#### Claude Code

Clone this repository, add it as a local Claude Code marketplace, then install the `gm-architecture` plugin from that marketplace:

```bash
/plugin marketplace add ZeroZ-lab/gmdiagram
/plugin install gm-architecture@gmdiagram-marketplace
```

#### Codex

Clone this repository locally and use the bundled Codex metadata:

- Plugin manifest: `gm-architecture/.codex-plugin/plugin.json`
- Marketplace entry: `.agents/plugins/marketplace.json`

The Claude and Codex variants share the same `skills/`, `assets/`, and `scripts/` directories, so the behavior stays aligned across both environments.

### Use

Just ask Claude to create a diagram:

```
> Draw an architecture diagram of Chrome's multi-process system

> Create a flowchart for a CI/CD pipeline with build, test, and deploy stages

> Generate a mind map for full-stack developer learning roadmap

> Design an ER diagram for an e-commerce database

> Draw a sequence diagram for user login authentication flow

> 画一个微服务架构图，包含 API Gateway、用户服务、订单服务
```

## Diagram Types

| Type | Trigger Keywords | Best For |
|------|-----------------|----------|
| **Architecture** | system, layered, infrastructure, 架构图 | System tiers, services, platforms |
| **Flowchart** | flow, decision, process, algorithm, 流程图 | Decision trees, process flows |
| **Mind Map** | brainstorm, hierarchy, feature tree, 思维导图 | Topic overview, roadmaps |
| **ER Diagram** | database, entity, table, schema, ER图 | Data models, database design |
| **Sequence** | API flow, message, interaction, 时序图 | Protocol flows, API calls |

## Examples

Each of the 9 visual styles applied to a different diagram type:

<table>
<tr>
<td width="50%" align="center">
<img src="assets/examples/images/chrome-architecture.png" alt="Chrome Architecture" width="100%"/><br/>
<b>Chrome Architecture</b><br/>
<sup>Architecture · <b>Dark Professional</b> · 4 layers · 8 modules</sup>
</td>
<td width="50%" align="center">
<img src="assets/examples/images/simple-webapp.png" alt="Simple Webapp" width="100%"/><br/>
<b>Simple Web Application</b><br/>
<sup>Architecture · <b>Hand-Drawn Sketch</b> · 3 tiers · 4 modules</sup>
</td>
</tr>
<tr>
<td width="50%" align="center">
<img src="assets/examples/images/flowchart-user-auth.png" alt="User Auth Flowchart" width="100%"/><br/>
<b>User Authentication Flow</b><br/>
<sup>Flowchart · <b>Light Corporate</b> · 8 nodes · 2 decisions</sup>
</td>
<td width="50%" align="center">
<img src="assets/examples/images/sequence-order.png" alt="Order Sequence" width="100%"/><br/>
<b>Order Processing</b><br/>
<sup>Sequence · <b>Cyberpunk Neon</b> · 5 actors · 9 messages · 1 loop</sup>
</td>
</tr>
<tr>
<td width="50%" align="center">
<img src="assets/examples/images/er-ecommerce.png" alt="ER Diagram" width="100%"/><br/>
<b>E-Commerce Database</b><br/>
<sup>ER Diagram · <b>Blueprint</b> · 6 entities · 6 relationships</sup>
</td>
<td width="50%" align="center">
<img src="assets/examples/images/mindmap-product.png" alt="Mind Map" width="100%"/><br/>
<b>Product Strategy</b><br/>
<sup>Mind Map · <b>Warm Cozy</b> · 3 levels · 15+ nodes</sup>
</td>
</tr>
<tr>
<td width="50%" align="center">
<img src="assets/examples/images/architecture-minimalist.png" alt="Minimalist" width="100%"/><br/>
<b>Clean API Architecture</b><br/>
<sup>Architecture · <b>Minimalist</b> · 4 layers · 9 modules</sup>
</td>
<td width="50%" align="center">
<img src="assets/examples/images/architecture-terminal.png" alt="Terminal Retro" width="100%"/><br/>
<b>Retro Terminal System</b><br/>
<sup>Architecture · <b>Terminal Retro</b> · 4 layers · CRT phosphor green</sup>
</td>
</tr>
<tr>
<td width="50%" align="center">
<img src="assets/examples/images/architecture-cyberpunk.png" alt="Cyberpunk" width="100%"/><br/>
<b>Hacker Toolkit</b><br/>
<sup>Architecture · <b>Cyberpunk Neon</b> · 4 layers · Catppuccin palette</sup>
</td>
<td width="50%" align="center">
<img src="assets/examples/images/architecture-pastel.png" alt="Pastel Dream" width="100%"/><br/>
<b>Cloud Native Ecosystem</b><br/>
<sup>Architecture · <b>Pastel Dream</b> · 5 layers · lavender pastels</sup>
</td>
</tr>
</table>

## Visual Styles

| Style | Background | Best For |
|-------|-----------|----------|
| **Dark Professional** | Deep dark (#020617) | Technical articles, docs |
| **Hand-Drawn Sketch** | Light beige (#faf8f5) | Teaching, brainstorming |
| **Light Corporate** | White (#f8fafc) | Business presentations |
| **Cyberpunk Neon** | Catppuccin dark (#11111b) | Developer tools, tech content |
| **Blueprint** | Nord dark (#2e3440) | Engineering specs, infra docs |
| **Warm Cozy** | Warm cream (#f9f5eb) | Tutorials, non-technical audiences |
| **Minimalist** | Pure white (#ffffff) | Technical docs, print |
| **Terminal Retro** | CRT black (#0a0a0a) | Developer blogs, fun |
| **Pastel Dream** | Lavender (#fef7ff) | Education, presentations |

## Output Formats

| Format | Description | Command |
|--------|-------------|---------|
| **HTML** | Single file with inline SVG (default) | Specify `format: "html"` or omit |
| **SVG** | Standalone SVG for vector editors | Specify `format: "svg"` |
| **Mermaid** | Text syntax for GitHub/Notion | Specify `format: "mermaid"` |
| **PNG/PDF** | Image export via script | `./scripts/export.sh diagram.html --format png` |

### PNG/PDF Export

```bash
# Requirements: Node.js (PNG) or rsvg-convert (PDF)
./scripts/export.sh diagram.html --format png
./scripts/export.sh diagram.html --format pdf
./scripts/export.sh diagram.svg --format png --output my-diagram.png
```

## Icons

Add icons to any component via the `"icon"` field:
```json
{ "id": "api-server", "label": "API Server", "type": "module", "icon": "tabler-server" }
```

150+ icons available in `references/icons-catalog.md`, organized by category:
- **Compute**: server, database, cloud, cpu, terminal, code
- **Networking**: globe, wifi, network, link, route
- **Security**: lock, shield, key, fingerprint
- **Users**: user, users, sitemap, hierarchy
- **Data**: table, file, folder, chart-bar, analytics
- **General**: settings, home, dashboard, search, rocket
- **Brands**: docker, kubernetes, react, aws, postgresql, github, nginx

## File Structure

```
gm-architecture/
├── .claude-plugin/
│   └── plugin.json                   # Claude plugin manifest
├── .codex-plugin/
│   └── plugin.json                   # Codex plugin manifest
├── README.md                         # Plugin overview
└── skills/
    └── gm-architecture/
        ├── SKILL.md                  # Core instructions + dispatcher
        ├── README.md                 # This file
        ├── references/
│   ├── design-system.md              # Colors, typography, spacing, icons
│   ├── diagram-type-registry.md      # All diagram types registry
│   ├── icons-catalog.md              # 150+ SVG icon paths
│   ├── output-svg.md                 # SVG output format rules
│   ├── output-mermaid.md             # Mermaid output format rules
│   ├── output-png-pdf.md             # PNG/PDF export instructions
│   │
│   │ # Architecture
│   ├── schema-architecture.md        # Architecture schema docs
│   ├── diagram-architecture.md       # Architecture workflow
│   ├── layout-rules.md               # Architecture coordinate rules
│   ├── component-templates.md        # Architecture SVG snippets
│   │
│   │ # Flowchart
│   ├── diagram-flowchart.md
│   ├── layout-flowchart.md
│   ├── components-flowchart.md
│   │
│   │ # Mind Map
│   ├── diagram-mindmap.md
│   ├── layout-mindmap.md
│   ├── components-mindmap.md
│   │
│   │ # ER Diagram
│   ├── diagram-er.md
│   ├── layout-er.md
│   ├── components-er.md
│   │
│   │ # Sequence Diagram
│   ├── diagram-sequence.md
│   ├── layout-sequence.md
│   ├── components-sequence.md
│   │
│   │ # Style guides (shared)
│   ├── style-dark-professional.md
│   ├── style-hand-drawn.md
│   ├── style-light-corporate.md
│   ├── style-cyberpunk-neon.md
│   ├── style-blueprint.md
│   ├── style-warm-cozy.md
│   ├── style-minimalist.md
│   ├── style-terminal-retro.md
│   └── style-pastel-dream.md
│
├── assets/
│   ├── schema-architecture.json      # Architecture JSON Schema
│   ├── schema-flowchart.json
│   ├── schema-mindmap.json
│   ├── schema-er.json
│   ├── schema-sequence.json
│   ├── template-dark.html
│   ├── template-sketch.html
│   ├── template-light-corporate.html
│   ├── template-cyberpunk-neon.html
│   ├── template-blueprint.html
│   ├── template-warm-cozy.html
│   ├── template-minimalist.html
│   ├── template-terminal-retro.html
│   ├── template-pastel-dream.html
│   └── examples/
│
└── scripts/
    ├── export.sh
    └── package.json
```

## How It Works

```
Natural Language → [LLM extracts] → JSON Schema → [Layout rules] → SVG → Output format
```

1. **Schema first**: Structure captured in JSON (layers/nodes/entities/actors + connections)
2. **Rendering second**: Layout rules compute coordinates, SVG components assembled
3. **Output**: Wrapped in HTML, or output as standalone SVG, Mermaid text, or PNG/PDF

## License

MIT
