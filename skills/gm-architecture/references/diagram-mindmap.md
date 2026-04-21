# Mind Map Diagram — Complete Reference

## Overview

Mind map diagrams show hierarchical information radiating from a central concept. A central node sits at the midpoint, with branches expanding outward to the left and right. Each branch can contain sub-branches, forming a tree structure ideal for brainstorming, feature breakdowns, and learning roadmaps.

## When to Use

- **Brainstorming sessions**: Capture ideas radiating from a central topic
- **Feature trees**: Break down a product into capabilities and sub-features
- **Learning roadmaps**: Organize skills and topics by domain
- **Project planning**: Map work streams, deliverables, and sub-tasks
- **Decision trees**: Show options and their consequences hierarchically
- **Knowledge maps**: Organize concepts by category and relationship

## JSON Schema

See `assets/schema-mindmap.json` for the formal JSON Schema (draft-07). Key structure:

```json
{
  "diagramType": "mindmap",
  "title": "Product Feature Map",
  "subtitle": "Core capabilities overview",
  "style": "dark-professional",
  "format": "html",
  "centralNode": {
    "id": "product",
    "label": "gmdiagram",
    "children": [
      {
        "id": "diagram-types",
        "label": "Diagram Types",
        "side": "auto",
        "children": [
          { "id": "architecture", "label": "Architecture" },
          { "id": "mindmap", "label": "Mind Map" },
          { "id": "flowchart", "label": "Flowchart" }
        ]
      },
      {
        "id": "styles",
        "label": "Visual Styles",
        "side": "auto",
        "children": [
          { "id": "dark", "label": "Dark Professional" },
          { "id": "hand", "label": "Hand-Drawn" }
        ]
      }
    ]
  },
  "legend": [],
  "metadata": {
    "author": "Mind Map Skill",
    "date": "2026-04-11",
    "version": "1.0"
  }
}
```

### Key Fields

| Field | Required | Description |
|-------|----------|-------------|
| `diagramType` | Yes | Must be `"mindmap"` |
| `title` | Yes | Diagram title (h1) |
| `subtitle` | No | Optional subtitle |
| `style` | Yes | Visual style preset |
| `format` | No | `"html"` (default) or `"svg"` |
| `centralNode` | Yes | Root node with recursive `children` |
| `legend` | No | Auto-generated from branch colors if omitted |
| `metadata` | No | Author, date, version |

### Branch Properties

| Property | Required | Default | Description |
|----------|----------|---------|-------------|
| `id` | Yes | — | Unique identifier |
| `label` | Yes | — | Display text |
| `side` | No | `"auto"` | `"left"`, `"right"`, or `"auto"` (balanced). Only for top-level branches. |
| `color` | No | Auto-assigned | Hex color override |
| `children` | No | `[]` | Sub-branches (recursive) |

### Depth Limits

- Practical maximum: **4 levels** (central -> branch -> sub-branch -> leaf)
- Beyond 4 levels the diagram becomes hard to read; split into multiple mind maps instead.

## Layout Rules

See `references/layout-mindmap.md` for complete coordinate calculation formulas.

Key constants:
- SVG_W = 1200px (wider than architecture to accommodate left/right branches)
- CENTER_NODE_R = 50px
- BRANCH_H_GAP = 120px (horizontal gap between levels)
- BRANCH_V_GAP = 30px (vertical gap between sibling branches)
- BRANCH_NODE_H = 32px (branch node height)

## Component Templates

See `references/components-mindmap.md` for SVG snippets for each mind map element.

Key components:
- **Central node**: Circle or rounded rect with prominent fill
- **Branch node**: Rounded rect (rx=12) or pill shape
- **Branch connection**: Cubic bezier path from parent to child
- **Color coding**: Top-level branches get distinct hues; children inherit lighter shades

## Style Templates

All 6 styles apply to mind map diagrams:

| Style | Template File | Reference File |
|-------|---------------|----------------|
| dark-professional | `assets/template-dark.html` | `references/style-dark-professional.md` |
| hand-drawn | `assets/template-sketch.html` | `references/style-hand-drawn.md` |
| light-corporate | `assets/template-light-corporate.html` | `references/style-light-corporate.md` |
| cyberpunk-neon | `assets/template-cyberpunk-neon.html` | `references/style-cyberpunk-neon.md` |
| blueprint | `assets/template-blueprint.html` | `references/style-blueprint.md` |
| warm-cozy | `assets/template-warm-cozy.html` | `references/style-warm-cozy.md` |

## Examples

- `assets/examples/mindmap-product.json` — Product feature map (4 branches, 18 nodes)
- `assets/examples/mindmap-learning.json` — Full-stack developer roadmap (4 branches, 14 nodes)

## Generation Workflow

1. **Extract structure**: Identify the central concept and its main categories from the user's description
2. **Build hierarchy**: Create `centralNode` with recursive `children` branches
3. **Assign sides**: For top-level branches, set `side` to `"auto"` (or explicit `"left"`/`"right"`)
4. **Assign colors**: Top-level branches get distinct palette colors; deeper levels get lighter shades
5. **Choose style**: Based on context or user preference
6. **Compute layout**: Use formulas from `layout-mindmap.md` to calculate coordinates
7. **Build SVG**: Use snippets from `components-mindmap.md` for each node and connection
8. **Wrap in HTML**: Use the chosen style's template file
