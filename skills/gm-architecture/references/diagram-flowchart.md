# Flowchart Diagram — Complete Reference

## Overview

Flowchart diagrams show process flows as a sequence of connected nodes. Each node represents a step (process, decision, I/O, etc.) and connections show the flow direction with optional branch labels. Decision nodes create branching paths (yes/no) and can loop back to earlier steps.

## When to Use

- Algorithm or process with sequential steps
- Decision trees with branching logic (if/else)
- Approval workflows with yes/no gates
- CI/CD pipelines with pass/fail paths
- User journeys with conditional steps
- Troubleshooting guides with decision points
- Business process flows (BPMN-lite)

## JSON Schema

See `assets/schema-flowchart.json` for the formal JSON Schema (draft-07).

Key structure:
```json
{
  "diagramType": "flowchart",
  "title": "Process Name",
  "subtitle": "Optional description",
  "style": "dark-professional",
  "format": "html",
  "nodes": [
    { "id": "start", "label": "Start", "type": "start" },
    { "id": "step1", "label": "Do Something", "type": "process" },
    { "id": "check", "label": "Is Valid?", "type": "decision" },
    { "id": "end", "label": "End", "type": "end" }
  ],
  "connections": [
    { "from": "start", "to": "step1", "direction": "down" },
    { "from": "step1", "to": "check", "direction": "down" },
    { "from": "check", "to": "end", "label": "Yes", "branch": "yes", "direction": "down" },
    { "from": "check", "to": "step1", "label": "No", "branch": "no", "direction": "right" }
  ],
  "swimlanes": [],
  "legend": [],
  "metadata": {}
}
```

## Supported Flowchart Types

1. **Sequential flow**: Linear process from start to end (no decisions)
2. **Branching flow**: Decision points that split into yes/no paths
3. **Loop-back flow**: Failed branches that return to an earlier step
4. **Swimlane flow**: Process grouped by actor/responsibility (horizontal bands)
5. **Multi-branch flow**: Decisions with more than two outcomes (using `branch: "default"`)

## Node Types (7 shapes)

| Type | Shape | Use for |
|------|-------|---------|
| `start` | Rounded rect (stadium, rx=20) | Entry point of the flow |
| `end` | Rounded rect (stadium, rx=20) | Exit point(s) of the flow |
| `process` | Rectangle (rx=4) | Action step, computation |
| `decision` | Diamond (rotated square) | Yes/no or true/false branch |
| `io` | Parallelogram (skewed) | Data input or output |
| `subprocess` | Double-border rectangle | Nested process / sub-flow |
| `document` | Rectangle with wavy bottom | Output document / report |

## Connection Properties

| Property | Required | Values | Description |
|----------|----------|--------|-------------|
| `from` | Yes | node id | Source node |
| `to` | Yes | node id | Target node |
| `label` | No | string | Text on the arrow (e.g., "Yes", "No") |
| `direction` | No | `down`, `right`, `left`, `up` | Arrow direction for layout |
| `style` | No | `solid`, `dashed`, `dotted` | Line style |
| `branch` | No | `yes`, `no`, `default` | Decision branch label |

## Layout Rules

See `references/layout-flowchart.md` for complete coordinate calculation formulas.

Key constants:
- NODE_GAP_V = 60px (vertical gap between nodes)
- NODE_GAP_H = 40px (horizontal gap for branching)
- DIAMOND_W = 140px, DIAMOND_H = 90px
- TERMINAL_RX = 20 (start/end corner radius)
- SVG_W = 1000px

## Component Templates

See `references/components-flowchart.md` for SVG snippets per node type.

7 node shapes + connection arrows + loop-back bezier paths.

## Style Templates

All 6 styles apply to flowchart diagrams:

| Style | Template File | Reference File |
|-------|---------------|----------------|
| dark-professional | `assets/template-dark.html` | `references/style-dark-professional.md` |
| hand-drawn | `assets/template-sketch.html` | `references/style-hand-drawn.md` |
| light-corporate | `assets/template-light-corporate.html` | `references/style-light-corporate.md` |
| cyberpunk-neon | `assets/template-cyberpunk-neon.html` | `references/style-cyberpunk-neon.md` |
| blueprint | `assets/template-blueprint.html` | `references/style-blueprint.md` |
| warm-cozy | `assets/template-warm-cozy.html` | `references/style-warm-cozy.md` |

## Node Type Color Mapping

| Type | fill | stroke | Use for |
|------|------|--------|---------|
| `start` | `rgba(6, 78, 59, 0.4)` | `#34d399` (emerald) | Start terminals |
| `end` | `rgba(6, 78, 59, 0.4)` | `#34d399` (emerald) | End terminals |
| `process` | `rgba(6, 78, 59, 0.4)` | `#34d399` (emerald) | Action steps |
| `decision` | `rgba(120, 53, 15, 0.3)` | `#fbbf24` (amber) | Branch points |
| `io` | `rgba(8, 51, 68, 0.4)` | `#22d3ee` (cyan) | Data I/O |
| `subprocess` | `rgba(6, 78, 59, 0.4)` | `#34d399` (emerald) | Sub-flows |
| `document` | `rgba(76, 29, 149, 0.4)` | `#a78bfa` (violet) | Output docs |

## Examples

- `assets/examples/flowchart-ci-cd.json` — CI/CD pipeline (10 nodes, 2 decisions, 2 loop-backs, 3 swimlanes, dark-professional)
- `assets/examples/flowchart-user-auth.json` — User authentication with 2FA (12 nodes, 3 decisions, 2 loop-backs, light-corporate)

## Generation Workflow

1. Identify the process steps and their order from the user's description
2. Determine node types: start/end terminals, process actions, decision gates, I/O operations
3. Assign `type` to each node based on its semantic role
4. Define connections with direction and branch labels (yes/no) for decisions
5. Identify loop-back connections (fail/retry paths that return to earlier steps)
6. Optionally group nodes into swimlanes by actor/responsibility
7. Choose style based on context or user preference
8. Compute layout using `layout-flowchart.md` formulas
9. Build SVG using `components-flowchart.md` snippets
10. Wrap in HTML using the style's template file
