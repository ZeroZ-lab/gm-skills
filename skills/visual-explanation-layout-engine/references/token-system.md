# Token System For SVG Visual Explanations

Use tokens to prevent visual drift and to make spacing rules auditable.

## Minimal Token Template

```js
const tokens = {
  canvas: { w: 1120, h: 770 },

  card: {
    radius: 18,
    border: 1
  },

  section: {
    x: 56,
    y: 150,
    w: 1008,
    h: 480,
    radius: 16,
    pad: 18,
    innerBottomPad: 52,
    noteGap: 28
  },

  node: {
    w: 198,
    h: 116,
    radius: 18,
    border: 1.5,

    padX: 22,
    padTop: 22,
    padBottom: 18,

    metaX: 22,
    metaY: 22,
    metaW: 54,
    metaH: 24,
    metaRadius: 12,
    metaTextY: 34,

    titleY: 68,
    descY: 94,
    titleTracking: 1.5
  },

  font: {
    title: 31,
    subtitle: 15,
    sectionLabel: 13,
    nodeTitle: 20,
    nodeDesc: 14,
    edgeLabel: 11,
    note: 13,
    meta: 12
  },

  line: {
    width: 3,
    baseWidth: 7,
    arrow: 5,
    labelH: 22,
    labelPadX: 12
  },

  spacing: {
    rowGap: 94,
    colGap: 60,
    laneGap: 18,
    labelRailGap: 34,
    sectionToNoteGap: 28
  },

  color: {
    paper: "#fff",
    ink: "#0f172a",
    muted: "#64748b",
    border: "#d8e0ea",
    faint: "#eef2f7",
    blue: "#2563eb",
    green: "#059669",
    orange: "#ea580c",
    red: "#dc2626",
    purple: "#7c3aed",
    gray: "#334155"
  }
};
```

## Geometry Rules

```text
nodeBottom + innerBottomPad <= sectionBottom
noteY >= sectionBottom + noteGap
mainRowNodeBottom + rowGap <= secondaryRowNodeTop
labelBox does not intersect nodeBox
labelBox does not cover arrowhead
```

## Text Alignment

Use:

```svg
dominant-baseline="middle"
text-anchor="middle"
```

Avoid aligning badge, title, and description by visual guesswork. Give each text role a stable Y slot.
