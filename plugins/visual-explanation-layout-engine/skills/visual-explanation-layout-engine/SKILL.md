---
name: visual-explanation-layout-engine
description: Turn complex workflows, responsibilities, states, and system relationships into mobile-readable HTML + SVG diagrams. Use for flowcharts, swimlanes, state machines, layered architectures, and hub-and-spoke explainers that need disciplined layout, routing, and audit.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
---

# Visual Explanation Layout Engine

This skill is for knowledge diagrams, not generic SVG decoration.

Use it when the reader needs to understand structure faster:

- sequence
- responsibility handoff
- state transition
- system layering
- orchestration around a central coordinator

Do not use it for:

- posters or decorative hero art
- photorealistic images
- dense dashboards
- large freeform graphs
- statistical charts better handled by chart grammar

Check `references/non-goals.md` before you commit to the SVG workflow. If the request lands there, do not force this skill onto the task.

## Core Rule

```text
intent -> topology -> template -> data model -> tokens -> layout -> routes -> labels -> audit -> final HTML/SVG
```

Do not jump straight to raw coordinates. Rendering is the last step.

## Entry Decision

Before building, explicitly decide:

1. What the reader must understand faster.
2. Which topology fits that goal.
3. Which template matches that topology.
4. Which details are essential versus optional.
5. What the main reading path is.
6. What would confuse the reader if left unstructured.

Reference order:

1. `references/non-goals.md`
2. `references/template-vs-case-study.md`
3. `references/topology-examples.md`
4. `references/request-patterns.md` when the request is underspecified
5. `references/failure-patterns.md` if the first layout pass fails audit

Topology choices:

| Reader goal | Topology |
|---|---|
| Step-by-step sequence | Flowchart |
| Responsibility by actor over time | Swimlane |
| Allowed state changes | State machine |
| System responsibility layers | Layered architecture |
| Central coordinator and surrounding resources | Hub-and-spoke |

## Required Workflow

Use this order every time:

### 1. Choose topology

State the topology before drawing anything.

### 2. Choose a template

Choose the generic template that matches the topology first. Only map domain content onto the template after the template is fixed.

### 3. Define the semantic data model

Use a minimum data model like this:

```js
const nodes = [
  {
    id: "step_b",
    title: "STEP B",
    desc: "second main step",
    tone: "blue",
    lane: "actor_b",
    row: "main",
    col: 2
  }
];

const edges = [
  {
    from: "step_b",
    to: "step_c",
    tone: "green",
    route: "right-left",
    label: "advance state",
    labelAt: { x: 585, y: 225 }
  }
];
```

Minimum field expectations:

- `nodes[]`: `id`, `title`, `desc`, `tone`
- `edges[]`: `from`, `to`, `tone`, `route`
- optional placement fields: `lane`, `row`, `col`
- optional label fields: `label`, `labelAt`

Raw `x/y` coordinates may appear in template examples as static scaffolding, but the preferred workflow is semantic placement first, coordinates second.

### 4. Choose tokens

All layout values must come from tokens. Use `references/token-system.md` as the single token source.

Required groups:

```js
const tokens = {
  canvas: { w, h },
  section: { x, y, w, h, radius, pad, innerBottomPad, noteGap },
  node: {
    w, h, radius, border,
    padX, padTop, padBottom,
    metaX, metaY, metaW, metaH, metaRadius, metaTextY,
    titleY, descY
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
  spacing: { rowGap, colGap, laneGap, labelRailGap, sectionToNoteGap },
  color: { paper, ink, muted, border, faint, blue, green, orange, red, purple, gray }
};
```

### 5. Build slot-based nodes

Each node is a small typesetting component:

```text
meta row
title row
desc row
```

Rules:

- badge or meta chip owns the meta row
- title owns the title row
- description owns the desc row
- badge must not share baseline with title
- description must not sit on the bottom edge

Use:

```svg
text-anchor="middle"
dominant-baseline="middle"
```

### 6. Route edges through anchors

Every node exposes:

```js
function anchors(node) {
  return {
    top: { x: node.x + node.w / 2, y: node.y },
    bottom: { x: node.x + node.w / 2, y: node.y + node.h },
    left: { x: node.x, y: node.y + node.h / 2 },
    right: { x: node.x + node.w, y: node.y + node.h / 2 },
    center: { x: node.x + node.w / 2, y: node.y + node.h / 2 }
  };
}
```

Use a consistent route vocabulary:

- `right-left`: main horizontal flow
- `bottom-top`: main vertical flow
- `left-down`: exception branch dropping to a side row
- `outer-right`: callback or return path on the outer rail
- `side-channel`: exception or compensation channel

Prefer straight or orthogonal routes. Do not default to center-to-center lines.

### 7. Put labels on rails

Do not place labels at the geometric midpoint by default.

Use:

```js
edge.labelAt = { x, y };
```

Rails:

- main-flow labels sit above the main row
- exception labels sit between the main row and exception row
- callback labels sit on a dedicated outer rail
- notes stay outside the main node area

### 8. Audit before rendering final output

Before final output, explicitly check:

- topology is correct
- peer nodes are visually consistent
- labels do not cover nodes or arrowheads
- routes avoid node bodies
- reading path is obvious
- mobile width remains readable

Use the references this way:

- `references/non-goals.md`: reject or reroute tasks that do not fit
- `references/template-vs-case-study.md`: decide whether you are producing a generic template or a domain case study
- `references/topology-examples.md`: choose the right topology
- `references/request-patterns.md`: shape vague requests into reusable inputs
- `references/token-system.md`: define layout tokens
- `references/output-contract.md`: lock the required output decisions
- `references/anti-overlap-checklist.md`: run final collision audit
- `references/evaluation-rubric.md`: score quality before delivery
- `references/failure-patterns.md`: repair failed layouts without random nudging

## Output Contract

Always satisfy these requirements:

1. Output a complete single-file HTML document unless the user asks for a fragment.
2. Use SVG with `viewBox`.
3. Build from structured `nodes[]` and `edges[]`.
4. Decide and state:
   - chosen topology
   - chosen template
   - node and edge semantic structure
   - token scheme
   - label rail strategy
   - audit result
   - legend or key requirement
5. Keep margins, spacing, border widths, type sizes, arrow sizes, and radii tokenized.
6. Avoid shadows unless explicitly requested.
7. Keep arrows restrained.
8. Preserve mobile readability.
9. Include a title.
10. Include a legend or key whenever color, chip, or route meaning is not obvious from context.
11. When producing a template or method artifact, do not mix domain case-study content into the template skeleton.

## Example Usage

Template examples:

- `examples/linear-flow-template.html`
- `examples/swimlane-template.html`
- `examples/state-machine-template.html`
- `examples/layered-architecture-template.html`
- `examples/hub-spoke-template.html`

Case studies:

- `examples/case-studies/`

The template examples intentionally keep the layout logic lightweight. They show how to separate:

- semantic data
- layout decisions
- anchors and routes
- label rails
- audit checks

Coverage:

- state machine explains allowed transitions and exception rows
- swimlane explains responsibility handoff over time
- layered architecture explains abstraction boundaries
- linear flow explains a main sequence with a branch
- hub-and-spoke explains central coordination with grouped spokes

## Quality Bar

A passing diagram must satisfy all of these:

- main reading path is obvious
- topology matches the information
- badge, title, and description are separated into slots
- labels use rails or explicit `labelAt`
- routes avoid node bodies
- same-level nodes use consistent sizing and typography
- color meaning is consistent

If the diagram fails the audit, revise layout or spacing rules before touching random coordinates.
