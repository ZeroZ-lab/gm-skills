# Flowchart SVG Component Templates

Copy and adapt these SVG snippets when generating flowchart diagram HTML. All coordinates are examples — replace with computed values from `layout-flowchart.md`.

## Architecture: CSS+SVG Hybrid

This template uses a **CSS+SVG hybrid approach**:
- **Rectangular nodes** (start, end, process, subprocess, document) use `<foreignObject>` + CSS classes for styling and text layout. CSS handles sizing, colors, text centering, and padding.
- **I/O nodes** use pure SVG `<polygon>` for both mask and visible shape. Do not mix a rectangular mask with CSS `clip-path`, because the hidden rectangular background will leak at the left/right edges and looks broken in browsers.
- **Diamond (decision) nodes** use pure SVG `<polygon>` because CSS cannot draw diamond shapes.
- **Arrows, connections, and labels** on connections use pure SVG elements.

## Required CSS Classes

Include these styles in the `<style>` block of the SVG or in the enclosing HTML:

```css
/* Base flowchart node */
.flow-node {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  padding: 4px 8px;
  font-family: "JetBrains Mono", monospace;
  color: white;
  text-align: center;
}

.flow-node .node-label {
  font-size: 12px;
  font-weight: 500;
  line-height: 1.3;
  word-wrap: break-word;
}

.flow-node .node-desc {
  display: block;
  font-size: 9px;
  color: #94a3b8;
  margin-top: 2px;
}

/* Type-specific styles */
.type-start {
  background: rgba(6, 78, 59, 0.4);
  border: 1.5px solid #34d399;
  border-radius: 20px;
}
.type-start .node-label {
  font-weight: 600;
}

.type-end {
  background: rgba(6, 78, 59, 0.4);
  border: 1.5px solid #34d399;
  border-radius: 20px;
}
.type-end .node-label {
  font-weight: 600;
}

.type-process {
  background: rgba(6, 78, 59, 0.4);
  border: 1.5px solid #34d399;
  border-radius: 4px;
}

.type-subprocess {
  background: rgba(6, 78, 59, 0.4);
  border: 1.5px solid #34d399;
  border-radius: 4px;
  /* Double-border effect via box-shadow (inset) */
  box-shadow: inset 3px 0 0 0 rgba(52, 211, 153, 0.6),
              inset -3px 0 0 0 rgba(52, 211, 153, 0.6);
}

.type-document {
  background: rgba(76, 29, 149, 0.4);
  border: 1.5px solid #a78bfa;
  border-radius: 4px 4px 0 0;
  border-bottom: none;
  /* Wavy bottom via clip-path */
  clip-path: polygon(
    0% 0%, 100% 0%, 100% 85%,
    75% 100%, 50% 85%, 25% 100%,
    0% 85%
  );
}
```

## Node Type Color Mapping (Quick Reference)

| Type | CSS class | background | border |
|------|-----------|-----------|--------|
| `start` | `.type-start` | `rgba(6, 78, 59, 0.4)` | `#34d399` (emerald) |
| `end` | `.type-end` | `rgba(6, 78, 59, 0.4)` | `#34d399` (emerald) |
| `process` | `.type-process` | `rgba(6, 78, 59, 0.4)` | `#34d399` (emerald) |
| `decision` | *(SVG only)* | `rgba(120, 53, 15, 0.3)` | `#fbbf24` (amber) |
| `io` | *(SVG polygon only)* | `rgba(8, 51, 68, 0.4)` | `#22d3ee` (cyan) |
| `subprocess` | `.type-subprocess` | `rgba(6, 78, 59, 0.4)` | `#34d399` (emerald) |
| `document` | `.type-document` | `rgba(76, 29, 149, 0.4)` | `#a78bfa` (violet) |

---

## 1. Start / End Terminal (foreignObject + CSS)

```svg
<!-- Start node: "Start" at position (450, 40), size 100x40 -->
<!-- Masking rect (draw FIRST, before arrows) -->
<rect x="450" y="40" width="100" height="40" rx="20" fill="#0f172a"/>
<!-- Node via foreignObject -->
<foreignObject x="450" y="40" width="100" height="40">
  <div xmlns="http://www.w3.org/1999/xhtml" class="flow-node type-start">
    <span class="node-label">Start</span>
  </div>
</foreignObject>
```

End nodes use the same pattern with `.type-end`:
```svg
<!-- End node: "End" at position (450, 1040), size 100x40 -->
<rect x="450" y="1040" width="100" height="40" rx="20" fill="#0f172a"/>
<foreignObject x="450" y="1040" width="100" height="40">
  <div xmlns="http://www.w3.org/1999/xhtml" class="flow-node type-end">
    <span class="node-label">End</span>
  </div>
</foreignObject>
```

## 2. Process Node (foreignObject + CSS)

```svg
<!-- Process node: "Build Application" at position (430, 240), size 140x40 -->
<!-- Masking rect -->
<rect x="430" y="240" width="140" height="40" rx="4" fill="#0f172a"/>
<!-- Node via foreignObject -->
<foreignObject x="430" y="240" width="140" height="40">
  <div xmlns="http://www.w3.org/1999/xhtml" class="flow-node type-process">
    <span class="node-label">Build Application</span>
  </div>
</foreignObject>
```

With optional description (increase height to accommodate):
```svg
<!-- Process node with description, size 140x52 -->
<rect x="430" y="240" width="140" height="52" rx="4" fill="#0f172a"/>
<foreignObject x="430" y="240" width="140" height="52">
  <div xmlns="http://www.w3.org/1999/xhtml" class="flow-node type-process">
    <span class="node-label">Build Application<span class="node-desc">Compile &amp; package</span></span>
  </div>
</foreignObject>
```

## 3. Decision Node (SVG Diamond — NOT foreignObject)

Decision diamonds remain pure SVG because CSS cannot render diamond shapes.

```svg
<!-- Decision node: "Tests Pass?" -->
<!-- Diamond polygon centered at (cx=500, cy=485) with w=140, h=90 -->
<!-- Masking polygon (same shape, opaque fill) -->
<polygon points="500,440 570,485 500,530 430,485" fill="#0f172a"/>
<!-- Styled diamond -->
<polygon points="500,440 570,485 500,530 430,485"
         fill="rgba(120, 53, 15, 0.3)" stroke="#fbbf24" stroke-width="1.5"/>
<!-- Label -->
<text x="500" y="482" font-size="11" font-weight="500" fill="white"
      font-family="JetBrains Mono, monospace" text-anchor="middle">Tests</text>
<text x="500" y="496" font-size="11" font-weight="500" fill="white"
      font-family="JetBrains Mono, monospace" text-anchor="middle">Pass?</text>
```

Diamond anchor points for connections:
```
top_vertex    = (cx, cy - h/2)       // (500, 440)
right_vertex  = (cx + w/2, cy)       // (570, 485)
bottom_vertex = (cx, cy + h/2)       // (500, 530)
left_vertex   = (cx - w/2, cy)       // (430, 485)
```

## 4. I/O Parallelogram (SVG Polygon Only)

I/O nodes should be rendered as pure SVG parallelograms. Use the same polygon geometry for both the opaque mask and the visible border/fill. Do **not** use a rectangular `<foreignObject>` plus CSS `clip-path` here; the mask and visible shape will diverge and produce ugly dark sidebars.

```svg
<!-- I/O node: "User Login" at position (430, 340), size 140x40 -->
<!-- Background mask -->
<polygon points="442,340 582,340 570,380 430,380" fill="#0f172a"/>
<!-- Styled parallelogram border -->
<polygon points="442,340 582,340 570,380 430,380"
         fill="rgba(8, 51, 68, 0.4)" stroke="#22d3ee" stroke-width="1.5"/>
<!-- Text -->
<text x="506" y="360" font-size="12" font-weight="500" fill="white"
      font-family="JetBrains Mono, monospace"
      text-anchor="middle" dominant-baseline="middle">User Login</text>
```

If the label needs two lines, split it into two `<text>` nodes or use `<tspan>` inside one `<text>`. Keep the text centered in the polygon, not in an invisible rectangle.

Parallelogram coordinate formula (for the polygon mask/border):
```
// Given x, y, w, h, skew=12
top_left     = (x + skew, y)
top_right    = (x + w + skew, y)
bottom_right = (x + w - skew, y + h)
bottom_left  = (x - skew, y + h)
```

## 5. Subprocess Node (foreignObject + CSS)

The double-border effect is handled by CSS `box-shadow: inset`.

```svg
<!-- Subprocess node: "Build" at position (430, 240), size 140x40 -->
<!-- Masking rect -->
<rect x="430" y="240" width="140" height="40" rx="4" fill="#0f172a"/>
<!-- Node via foreignObject (CSS .type-subprocess provides double border via box-shadow) -->
<foreignObject x="430" y="240" width="140" height="40">
  <div xmlns="http://www.w3.org/1999/xhtml" class="flow-node type-subprocess">
    <span class="node-label">Build</span>
  </div>
</foreignObject>
```

If CSS `box-shadow` inset is not sufficient, fall back to an inner SVG rect:
```svg
<!-- Fallback: explicit inner rect for double-border -->
<rect x="430" y="240" width="140" height="40" rx="4" fill="#0f172a"/>
<foreignObject x="430" y="240" width="140" height="40">
  <div xmlns="http://www.w3.org/1999/xhtml" class="flow-node type-process">
    <span class="node-label">Build</span>
  </div>
</foreignObject>
<!-- Inner rect overlay for double-border (drawn on top) -->
<rect x="436" y="240" width="128" height="40" rx="2"
      fill="none" stroke="#34d399" stroke-width="0.8"/>
```

## 6. Document Node (foreignObject + CSS)

The wavy bottom is handled by CSS `clip-path` on the `.type-document` class.

```svg
<!-- Document node: "Log Audit Entry" at position (430, 600), size 140x40 -->
<!-- Masking rect -->
<rect x="430" y="600" width="140" height="40" rx="4" fill="#0f172a"/>
<!-- Node via foreignObject (CSS .type-document provides wavy bottom via clip-path) -->
<foreignObject x="430" y="600" width="140" height="40">
  <div xmlns="http://www.w3.org/1999/xhtml" class="flow-node type-document">
    <span class="node-label">Log Audit Entry</span>
  </div>
</foreignObject>
```

If CSS `clip-path` is not available, use an SVG path mask instead:
```svg
<!-- Fallback: SVG path for document shape -->
<path d="M 430,600 L 570,600 L 570,635 Q 540,645 500,635 Q 460,625 430,635 Z"
      fill="#0f172a"/>
<path d="M 430,600 L 570,600 L 570,635 Q 540,645 500,635 Q 460,625 430,635 Z"
      fill="rgba(76, 29, 149, 0.4)" stroke="#a78bfa" stroke-width="1.5"/>
<foreignObject x="430" y="600" width="140" height="40">
  <div xmlns="http://www.w3.org/1999/xhtml" class="flow-node"
       style="background: transparent; border: none;">
    <span class="node-label">Log Audit Entry</span>
  </div>
</foreignObject>
```

Wavy bottom SVG path formula:
```
// Given x, y, w, h, wave_amplitude=5
path = "M {x},{y}                          // top-left
        L {x+w},{y}                         // top-right
        L {x+w},{y+h}                       // right side down
        Q {x+w*0.75},{y+h+wave_amp}         // wave curve 1
          {x+w*0.5},{y+h}                   // wave midpoint
        Q {x+w*0.25},{y+h-wave_amp}         // wave curve 2
          {x},{y+h}                          // wave end
        Z"                                   // close to top-left
```

## 7. Connection Arrow: Solid (Down)

```svg
<!-- Solid arrow from source bottom-center to target top-center -->
<line x1="500" y1="80" x2="500" y2="140"
      stroke="#64748b" stroke-width="1.5" marker-end="url(#arrowhead)"/>
```

## 8. Connection Arrow: Dashed

```svg
<!-- Dashed arrow (for fail/optional paths) -->
<line x1="500" y1="80" x2="500" y2="140"
      stroke="#64748b" stroke-width="1.5" stroke-dasharray="6,4"
      marker-end="url(#arrowhead)"/>
```

## 9. Connection Arrow: With Label

```svg
<!-- Arrow with label background and text -->
<line x1="500" y1="280" x2="500" y2="340"
      stroke="#64748b" stroke-width="1.5" marker-end="url(#arrowhead)"/>
<!-- Label background -->
<rect x="484" y="296" width="32" height="16" rx="3" fill="#0f172a" opacity="0.9"/>
<!-- Label text -->
<text x="500" y="308" font-size="10" fill="#94a3b8"
      font-family="JetBrains Mono, monospace" text-anchor="middle">Yes</text>
```

## 10. Loop-Back Arrow (Cubic Bezier)

```svg
<!-- Loop-back from decision "No" branch back to earlier node -->
<!-- Routes along the right side of the diagram -->
<path d="M 570,485 C 650,485 640,160 560,160"
      fill="none" stroke="#fb923c" stroke-width="1.5" stroke-dasharray="6,4"
      marker-end="url(#arrowhead-loop)"/>
<!-- Branch label -->
<rect x="622" y="300" width="40" height="16" rx="3" fill="#0f172a" opacity="0.9"/>
<text x="642" y="312" font-size="10" fill="#fb923c"
      font-family="JetBrains Mono, monospace" text-anchor="middle">No</text>
```

Loop-back arrows use orange (`#fb923c`) stroke to visually distinguish them from the main flow.

## 11. Decision Branch Labels ("Yes" / "No")

```svg
<!-- "Yes" label below decision diamond (on the down path) -->
<text x="500" y="545" font-size="10" font-weight="600" fill="#34d399"
      font-family="JetBrains Mono, monospace" text-anchor="middle">Yes</text>

<!-- "No" label to the right of decision diamond (on the right path) -->
<text x="582" y="482" font-size="10" font-weight="600" fill="#fb7185"
      font-family="JetBrains Mono, monospace" text-anchor="start">No</text>
```

Color coding for branch labels:
- **Yes** (positive path): `#34d399` (emerald/green)
- **No** (negative path): `#fb7185` (rose/red)
- **Default** (fallback): `#94a3b8` (slate/gray)

## 12. Swimlane Band

```svg
<!-- Swimlane: "Developer" -->
<rect x="40" y="20" width="920" height="160" rx="0"
      fill="none" stroke="rgba(148, 163, 184, 0.2)" stroke-width="1"/>
<!-- Swimlane label (rotated vertical text on left) -->
<text x="55" y="100" font-size="11" font-weight="600" fill="#cbd5e1"
      font-family="JetBrains Mono, monospace" text-anchor="middle"
      writing-mode="tb">Developer</text>
<!-- Separator line (right edge of label column) -->
<line x1="120" y1="20" x2="120" y2="180"
      stroke="rgba(148, 163, 184, 0.15)" stroke-width="1"/>
```

Swimlane band height includes top/bottom padding of 20px each:
```
band_h = max(node_h for nodes in lane) + 40
```

## 13. Swimlane Separator (Between Bands)

```svg
<!-- Separator between swimlanes -->
<line x1="40" y1="180" x2="960" y2="180"
      stroke="rgba(148, 163, 184, 0.15)" stroke-width="1"/>
```

## 14. Legend (Flowchart)

```svg
<!-- Legend, positioned below all diagram content -->
<g transform="translate(40, 1100)">
  <text x="0" y="0" font-size="11" font-weight="600" fill="#cbd5e1"
        font-family="JetBrains Mono, monospace">Legend</text>

  <!-- Legend item: Start/End -->
  <rect x="0" y="12" width="30" height="14" rx="7"
        fill="rgba(6, 78, 59, 0.4)" stroke="#34d399" stroke-width="1"/>
  <text x="36" y="23" font-size="11" fill="#cbd5e1"
        font-family="JetBrains Mono, monospace">Start / End</text>

  <!-- Legend item: Process -->
  <rect x="130" y="12" width="14" height="14" rx="2"
        fill="rgba(6, 78, 59, 0.4)" stroke="#34d399" stroke-width="1"/>
  <text x="150" y="23" font-size="11" fill="#cbd5e1"
        font-family="JetBrains Mono, monospace">Process</text>

  <!-- Legend item: Decision -->
  <polygon points="255,12 262,19 255,26 248,19"
           fill="rgba(120, 53, 15, 0.3)" stroke="#fbbf24" stroke-width="1"/>
  <text x="270" y="23" font-size="11" fill="#cbd5e1"
        font-family="JetBrains Mono, monospace">Decision</text>

  <!-- Legend item: I/O -->
  <polygon points="360,12 380,12 377,26 357,26"
           fill="rgba(8, 51, 68, 0.4)" stroke="#22d3ee" stroke-width="1"/>
  <text x="386" y="23" font-size="11" fill="#cbd5e1"
        font-family="JetBrains Mono, monospace">I/O</text>

  <!-- Legend item: Loop-back -->
  <path d="M 440,19 C 450,19 455,12 455,12"
        fill="none" stroke="#fb923c" stroke-width="1.5" stroke-dasharray="4,2"/>
  <text x="462" y="23" font-size="11" fill="#cbd5e1"
        font-family="JetBrains Mono, monospace">Loop-back</text>
</g>
```

## 15. SVG Defs (Required at start of every flowchart SVG)

```svg
<defs>
  <!-- Grid pattern -->
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(51, 65, 85, 0.3)" stroke-width="0.5"/>
  </pattern>
  <!-- Forward arrowhead (main flow) -->
  <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
    <polygon points="0 0, 8 3, 0 6" fill="#64748b"/>
  </marker>
  <!-- Loop-back arrowhead (orange) -->
  <marker id="arrowhead-loop" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
    <polygon points="0 0, 8 3, 0 6" fill="#fb923c"/>
  </marker>
  <!-- Reverse arrowhead (for bidirectional) -->
  <marker id="arrowhead-rev" markerWidth="8" markerHeight="6" refX="0" refY="3" orient="auto">
    <polygon points="8 0, 0 3, 8 6" fill="#64748b"/>
  </marker>
</defs>
```

## foreignObject Pattern Summary

For rectangular node types (start, end, process, subprocess, document), use this pattern:

```svg
<!-- 1. Masking rect (same position/size as node, opaque background color) -->
<rect x="X" y="Y" width="W" height="H" rx="RX" fill="#0f172a"/>
<!-- 2. foreignObject containing a styled HTML div -->
<foreignObject x="X" y="Y" width="W" height="H">
  <div xmlns="http://www.w3.org/1999/xhtml" class="flow-node type-TYPE">
    <span class="node-label">LABEL TEXT</span>
  </div>
</foreignObject>
```

Where:
- `X`, `Y` = top-left position from layout calculations
- `W`, `H` = node dimensions from layout calculations
- `RX` = corner radius (20 for start/end, 4 for process/subprocess/document)
- `type-TYPE` = one of `type-start`, `type-end`, `type-process`, `type-subprocess`, `type-document`
- CSS handles all visual styling (background, border, border-radius, text centering)

For **decision (diamond)** and **I/O parallelogram** nodes, continue using SVG geometry with SVG `<text>` labels.

## Rendering Order

When composing the final SVG, draw elements in this order:

1. Grid background (`<rect fill="url(#grid)" />`)
2. Swimlane bands and separators
3. All connection lines and arrows (behind nodes)
4. All node shapes (on top of arrows) — masking rects/polygons first, then foreignObject divs or SVG shapes
5. All labels (text on top of everything) — connection labels and decision diamond text
6. Legend

This order ensures arrows go behind nodes and text is always readable.
