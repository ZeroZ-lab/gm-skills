---
name: visual-explanation-layout-engine
description: Turn complex ideas, workflows, systems, states, responsibilities, and causal structures into mobile-readable HTML + SVG visual explanations. Use for flowcharts, swimlanes, state machines, architecture diagrams, data-flow diagrams, value-flow diagrams, decision models, Web Component based visual artifacts, and GIF-ready lightweight animated diagrams.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
---

# Visual Explanation Layout Engine

This skill is not merely an SVG drawing skill. It is a method for translating complex knowledge structures into readable visual systems.

SVG, HTML, CSS, and Web Components are the rendering substrate. The real work is:

```text
problem
  -> information intent
  -> topology
  -> visual grammar
  -> layout system
  -> component slots
  -> routing channels
  -> annotation rails
  -> rendering
  -> quality audit
```

Core principle:

```text
Do not draw shapes first.
Compile meaning into spatial structure.
```

## When To Use

Use this skill for:

- Flowcharts and process diagrams
- Swimlane diagrams
- State machine diagrams
- System architecture diagrams
- Agent workflow diagrams
- Payment, order, transaction, and callback diagrams
- Data-flow and value-flow diagrams
- Decision models and fault paths
- Multi-layer technical explainers
- Web Component + SVG reusable visual artifacts
- Lightweight animated diagrams that may be exported as GIFs

Do not use it for:

- Photorealistic images
- Decorative posters without structural meaning
- Dense dashboards
- Large graph exploration with hundreds or thousands of nodes
- Statistical charts better handled by chart grammar

## Workflow

### 1. Determine Intent

Ask what the reader must understand faster:

```text
What is the primary relationship?
What must be compared, sequenced, grouped, or judged?
What can be omitted without losing the point?
What is the main reading path?
Where can the reader get confused?
```

Intent maps to visual form:

| Intent | Best visual form |
|---|---|
| Understand sequence | Flowchart |
| Understand responsibility | Swimlane |
| Understand state transition | State machine |
| Understand system layers | Layered architecture |
| Understand orchestration | Hub-and-spoke |
| Understand compounding loop | Flywheel |
| Understand business transfer | Value-flow |
| Understand choices | Decision tree or matrix |
| Understand risk | Fault path or exception map |

Rule:

```text
Intent determines topology.
Topology determines layout.
Layout determines geometry.
Geometry determines SVG.
```

### 2. Choose Topology

Common topologies:

- Linear flow: `A -> B -> C`
- Swimlane: rows are responsible actors, columns are time
- State machine: states plus allowed transitions
- Layered architecture: vertical levels represent abstraction or responsibility
- Hub-and-spoke: one core system coordinates surrounding resources
- Flywheel or loop: feedback improves the next cycle
- Value flow: money, data, power, risk, or bargaining position moves between parties

Never begin with visual style. Begin with topology.

### 3. Define Visual Grammar

Every visual element needs semantic duty.

| Visual element | Meaning |
|---|---|
| Node | Entity, state, step, actor, module |
| Edge | Relationship, transition, call, dependency |
| Lane | Responsibility boundary |
| Layer | Abstraction boundary |
| Section | Conceptual group |
| Label chip | Edge meaning or transition condition |
| Color | Semantic category |
| Thickness | Strength, volume, or importance |
| Position | Order, level, responsibility, priority |
| Animation | Direction or current focus |

Color semantics:

```text
Blue = main flow or data flow
Green = success, callback, feedback
Orange = channel, compensation, refund
Red = failure, exception, risk
Purple = fulfillment or high-level completion
Gray = neutral, initial, baseline, infrastructure
```

If the same color appears twice, it must mean the same thing.

### 4. Build A Layout System

A diagram must be a small layout engine, not a collection of guessed coordinates.

```text
Data
  -> topology
  -> placement
  -> anchors
  -> routes
  -> label rails
  -> rendering order
  -> audit
```

Prefer structured data:

```js
const nodes = [
  {
    id: "pending",
    title: "PENDING",
    desc: "等待支付",
    tone: "blue",
    lane: "backend",
    row: "main",
    col: 2
  }
];

const edges = [
  {
    from: "pending",
    to: "paid",
    type: "success",
    route: "right-left",
    label: "回调确认",
    labelAt: { x: 585, y: 225 }
  }
];
```

Do not encode meaning only in raw SVG coordinates.

### 5. Centralize Tokens

All visual values must come from tokens. Use [token-system.md](references/token-system.md) as the working template.

Required token groups:

```js
const tokens = {
  canvas: { w, h },
  card: { radius, border },
  section: { x, y, w, h, radius, pad, innerBottomPad, noteGap },
  node: {
    w, h,
    radius,
    border,
    padX,
    padTop,
    padBottom,
    metaX,
    metaY,
    metaW,
    metaH,
    metaRadius,
    metaTextY,
    titleY,
    descY
  },
  font: {
    title,
    subtitle,
    sectionLabel,
    nodeTitle,
    nodeDesc,
    edgeLabel,
    note,
    meta
  },
  line: { width, baseWidth, arrow, labelH, labelPadX },
  spacing: { rowGap, colGap, laneGap, labelRailGap, sectionToNoteGap }
};
```

Do not patch font size, padding, stroke width, or label size one element at a time.

### 6. Slot Components

A node is a small typesetting component, not just a rectangle with text.

Bad model:

```text
[badge] TITLE
desc
```

Good model:

```text
┌────────────────────┐
│ badge/meta          │
│                    │
│       TITLE         │
│       description   │
└────────────────────┘
```

Rules:

```text
Badge owns the meta row.
Title owns the title row.
Description owns the desc row.
Badge must not share baseline with title.
Text must not be positioned by guesswork.
```

Use:

```svg
text-anchor="middle"
dominant-baseline="middle"
```

### 7. Route Edges Through Anchors

Every node exposes anchors:

```js
function anchors(node) {
  return {
    top: { x: node.x + node.w / 2, y: node.y },
    bottom: { x: node.x + node.w / 2, y: node.y + node.h },
    left: { x: node.x, y: node.y + node.h / 2 },
    right: { x: node.x + node.w, y: node.y + node.h / 2 }
  };
}
```

Route types:

```text
right-left = horizontal flow
bottom-top = vertical flow
left-down = exception branch
outer-right = return or callback path
side-channel = compensation or error path
```

Prefer straight lines and orthogonal polylines. Avoid center-to-center routes, routes through node bodies, labels at crowded path midpoints, and Bezier curves for ordinary process diagrams.

### 8. Put Labels On Rails

Labels need their own spatial system. In complex diagrams, do not place edge labels at the path midpoint by default.

Use:

```js
edge.labelAt = { x, y };
```

Label rails:

```text
Main-flow labels: above the main node row.
Exception labels: between the main row and exception row.
Callback labels: in the callback rail.
Notes: outside sections, not inside node lanes.
```

Label chip:

```svg
<rect fill="#fff" stroke="#e2e8f0" rx="11" />
<text text-anchor="middle" dominant-baseline="middle">...</text>
```

### 9. Enforce Spacing Invariants

These checks must hold:

```text
nodeRight <= sectionRight - sectionPad
nodeLeft >= sectionLeft + sectionPad
bottomNodeY + nodeHeight + innerBottomPad <= sectionBottom
noteY >= sectionBottom + sectionToNoteGap
mainRowNodeBottom + rowGap <= secondaryRowNodeTop
label box must not intersect any node box
label box must not cover arrowhead
```

If any invariant fails, revise the layout system rather than nudging one coordinate.

### 10. Render In Stable Order

SVG later elements cover earlier elements. Render in this order:

```text
1. background
2. section / lanes
3. guide lines
4. edge base lines
5. edge main lines
6. labels
7. nodes
8. notes / captions
```

If an edge might pass through a node area, draw nodes last.

## Diagram Patterns

State machine:

```text
Main states stay on the main row.
Exception, terminal, and compensation states move to a secondary row.
Terminal states should not casually return to active states.
Refund is compensation; it does not erase a paid state.
```

Swimlane:

```text
Row = responsible actor.
Column = time.
Arrow = interaction.
Color = route semantics.
```

Layered architecture:

```text
Layer = responsibility boundary.
Vertical position = abstraction level.
Dependencies should move down or across, not randomly upward.
```

Vertical mobile flow:

```text
Main flow travels down the center axis.
Exception branches use side channels.
Node widths stay uniform.
Arrows stay restrained.
```

## Animation Rules

Motion serves direction, not spectacle.

Allowed:

```text
stroke-dashoffset for flow
small dots moving along a path
subtle highlight on active node or edge
```

Avoid:

```text
complex rotation
large flashing regions
many paths animating strongly at once
overused glow filters
motion that blocks text
```

For GIF export:

```text
Frames: 36-60
Duration: 70-100ms
Keep motion focused on primary path flow.
```

## Output Contract

When generating an HTML + SVG visual explanation:

```text
1. Produce a complete single-file HTML document unless the user asks otherwise.
2. Use no external dependencies unless explicitly allowed.
3. If using Web Components, encapsulate tokens, data, layout, and render logic.
4. Use SVG viewBox.
5. Generate nodes, edges, and labels from structured data.
6. Control margins, padding, borders, and font sizes through tokens.
7. Avoid shadows unless explicitly requested.
8. Keep arrow sizes restrained.
9. Ensure nodes do not overlap and labels do not cover nodes.
10. Preserve mobile readability.
```

## Quality Audit

Before final output, use:

- [anti-overlap-checklist.md](references/anti-overlap-checklist.md)
- [evaluation-rubric.md](references/evaluation-rubric.md)
- [topology-examples.md](references/topology-examples.md)

Minimum passing bar:

```text
The main reading path is obvious.
Peer nodes have consistent sizes.
Badge, title, and description use separate slots.
Routes avoid node bodies.
Labels use rails or explicit labelAt positions.
The diagram is readable at mobile width.
```
