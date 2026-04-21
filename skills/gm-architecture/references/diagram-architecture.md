# Architecture Diagram — Complete Reference

## Overview

Architecture diagrams show system structure as layered horizontal bands. Each layer contains modules, with connections showing data flow and dependencies between components.

## When to Use

- System with clear tiers (UI → API → Data)
- Multi-process/multi-service architecture
- Platform capability maps
- Microservices with infrastructure
- AI/ML pipelines with data flow

## JSON Schema

See `assets/schema-architecture.json` for the formal schema. See `references/schema-architecture.md` for human-readable documentation.

Key structure:
```json
{
  "title": "System Name",
  "subtitle": "Optional description",
  "style": "dark-professional",
  "format": "html",
  "diagramType": "architecture",
  "layers": [...],
  "connections": [...],
  "groups": [...],
  "legend": [...]
}
```

## Supported Architecture Types

1. **Layered architecture**: Horizontal bands representing system tiers (UI → API → Data)
2. **Multi-process system**: Independent processes with communication channels
3. **Platform capability map**: Feature/capability groups organized by layer
4. **Microservices**: Service mesh with data stores and gateways
5. **AI/ML pipeline**: Data flow from input through processing to output

## Layout Rules

See `references/layout-rules.md` for complete coordinate calculation formulas.

Key constants:
- PAGE_MARGIN = 40px
- LAYER_GAP = 50px
- MODULE_GAP = 20px
- MODULE_MIN_W = 100px
- SVG_W = 1000px

## Component Templates

See `references/component-templates.md` for SVG snippets per component type.

7 component types: `process`, `module`, `data`, `infra`, `security`, `channel`, `external`

Each type maps to a fill/stroke color pair that varies by style.

## Style Templates

All 6 styles apply to architecture diagrams:

| Style | Template File | Reference File |
|-------|---------------|----------------|
| dark-professional | `assets/template-dark.html` | `references/style-dark-professional.md` |
| hand-drawn | `assets/template-sketch.html` | `references/style-hand-drawn.md` |
| light-corporate | `assets/template-light-corporate.html` | `references/style-light-corporate.md` |
| cyberpunk-neon | `assets/template-cyberpunk-neon.html` | `references/style-cyberpunk-neon.md` |
| blueprint | `assets/template-blueprint.html` | `references/style-blueprint.md` |
| warm-cozy | `assets/template-warm-cozy.html` | `references/style-warm-cozy.md` |

## Examples

- `assets/examples/chrome-architecture.json` — Chrome multi-process (3 layers, 6+ modules, IPC)
- `assets/examples/ai-platform.json` — Enterprise AI platform (5 layers, 15 modules)
- `assets/examples/simple-webapp.json` — Simple 3-tier web app (2 layers, 4 modules)

## Generation Workflow

1. Extract layers and modules from the user's description
2. Assign `type` to each component (process, module, data, etc.)
3. Define connections between components
4. Choose style based on context or user preference
5. Compute layout using `layout-rules.md` formulas
6. Build SVG using `component-templates.md` snippets
7. Wrap in HTML using the style's template file
