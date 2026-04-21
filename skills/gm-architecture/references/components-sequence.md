# Sequence Diagram — SVG Component Templates (CSS+SVG Hybrid)

## Actor Box (Participant / Boundary / Controller)

Uses `<foreignObject>` + CSS for styled boxes. Position via `transform="translate(X, Y)"` on the parent `<g>`.

```svg
<g transform="translate(X, Y)">
  <foreignObject width="W" height="36">
    <div xmlns="http://www.w3.org/1999/xhtml" class="seq-actor type-participant">
      <span class="actor-label">API Gateway</span>
    </div>
  </foreignObject>
</g>
```

For boundary type:
```svg
<g transform="translate(X, Y)">
  <foreignObject width="W" height="36">
    <div xmlns="http://www.w3.org/1999/xhtml" class="seq-actor type-boundary">
      <span class="actor-label">:Boundary</span>
    </div>
  </foreignObject>
</g>
```

For controller type:
```svg
<g transform="translate(X, Y)">
  <foreignObject width="W" height="36">
    <div xmlns="http://www.w3.org/1999/xhtml" class="seq-actor type-controller">
      <span class="actor-label">:Controller</span>
    </div>
  </foreignObject>
</g>
```

### CSS Classes for Actor Boxes

```css
.seq-actor {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 80px;
  height: 36px;
  padding: 0 12px;
  background: #0f172a;
  border: 1.5px solid #22d3ee;
  border-radius: 4px;
  box-sizing: border-box;
  color: white;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
}

.seq-actor .actor-label {
  text-align: center;
}

.type-participant {
  border-radius: 4px;
}

.type-boundary {
  border-radius: 4px;
  border-left: 3px solid #22d3ee;
}

.type-controller {
  border-radius: 4px;
  background: #1e293b;
}
```

## Actor Stick Figure

Remains pure SVG (drawn with lines/circle).

```svg
<!-- type-actor: stick figure -->
<g class="type-actor">
  <!-- Head -->
  <circle cx="X" cy="12" r="6" fill="none" stroke="#22d3ee" stroke-width="1.5"/>
  <!-- Body -->
  <line x1="X" y1="18" x2="X" y2="32" stroke="#22d3ee" stroke-width="1.5"/>
  <!-- Arms -->
  <line x1="X-8" y1="24" x2="X+8" y2="24" stroke="#22d3ee" stroke-width="1.5"/>
  <!-- Legs -->
  <line x1="X" y1="32" x2="X-6" y2="42" stroke="#22d3ee" stroke-width="1.5"/>
  <line x1="X" y1="32" x2="X+6" y2="42" stroke="#22d3ee" stroke-width="1.5"/>
  <!-- Label below figure -->
  <text x="X" y="54" font-size="11" font-weight="500" fill="white" text-anchor="middle">User</text>
</g>
```

## Lifeline

Pure SVG dashed vertical line.

```svg
<line x1="X" y1="TOP" x2="X" y2="BOTTOM" stroke="#64748b" stroke-width="1" stroke-dasharray="6,4"/>
```

## Sync Message (solid arrow)

Pure SVG `<line>` with marker.

```svg
<defs>
  <marker id="seq-arrow-solid" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
    <polygon points="0 0, 8 3, 0 6" fill="#e2e8f0"/>
  </marker>
</defs>
<line x1="FROM_X" y1="Y" x2="TO_X" y2="Y" stroke="#e2e8f0" stroke-width="1.5" marker-end="url(#seq-arrow-solid)"/>
<text x="(FROM_X+TO_X)/2" y="Y-6" font-size="10" fill="#94a3b8" text-anchor="middle">Message Label</text>
```

## Async Message (open arrow)

Pure SVG `<line>` with open arrowhead marker.

```svg
<defs>
  <marker id="seq-arrow-open" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
    <polyline points="0 0, 8 3, 0 6" fill="none" stroke="#e2e8f0" stroke-width="1"/>
  </marker>
</defs>
<line x1="FROM_X" y1="Y" x2="TO_X" y2="Y" stroke="#e2e8f0" stroke-width="1.5" marker-end="url(#seq-arrow-open)"/>
```

## Return Message (dashed arrow)

Pure SVG dashed line with open arrowhead.

```svg
<line x1="FROM_X" y1="Y" x2="TO_X" y2="Y" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="6,4" marker-end="url(#seq-arrow-open)"/>
```

## Self-Message (recursive call)

Pure SVG path.

```svg
<path d="M X,Y L X+30,Y L X+30,Y+20 L X,Y+20" fill="none" stroke="#e2e8f0" stroke-width="1.5" marker-end="url(#seq-arrow-solid)"/>
```

## Activation Box

Pure SVG colored rectangle on lifeline.

```svg
<rect x="X-6" y="TOP_Y" width="12" height="HEIGHT" rx="2" fill="rgba(34,211,238,0.15)" stroke="#22d3ee" stroke-width="1"/>
```

## Fragment Frame (alt, loop, opt, par)

Uses `<foreignObject>` + CSS for the frame box, with SVG label at top-left corner.

```svg
<g transform="translate(X, Y)">
  <!-- Frame box via foreignObject + CSS -->
  <foreignObject width="W" height="H">
    <div xmlns="http://www.w3.org/1999/xhtml" class="seq-fragment type-alt">
      <!-- Fragment body is transparent, border only -->
    </div>
  </foreignObject>
  <!-- Label tab at top-left corner (SVG) -->
  <path d="M 0,0 L 0,20 L 50,20 L 60,10 L 60,0 Z" fill="rgba(100,116,139,0.2)" stroke="#64748b" stroke-width="1"/>
  <text x="8" y="15" font-size="10" font-weight="600" fill="#cbd5e1">alt</text>
</g>
```

For loop, opt, par — change the label text and CSS class:
```svg
<g transform="translate(X, Y)">
  <foreignObject width="W" height="H">
    <div xmlns="http://www.w3.org/1999/xhtml" class="seq-fragment type-loop">
    </div>
  </foreignObject>
  <path d="M 0,0 L 0,20 L 50,20 L 60,10 L 60,0 Z" fill="rgba(100,116,139,0.2)" stroke="#64748b" stroke-width="1"/>
  <text x="8" y="15" font-size="10" font-weight="600" fill="#cbd5e1">loop</text>
</g>
```

### CSS Classes for Fragments

```css
.seq-fragment {
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  border: 1px solid #64748b;
  border-radius: 4px;
  background: transparent;
}

.type-alt { /* no extra styling, inherits fragment base */ }
.type-loop { border-color: #64748b; }
.type-opt { border-color: #64748b; }
.type-par { border-color: #64748b; }
```

### Condition/Guard Text Inside Fragment

```svg
<text x="X+12" y="Y+34" font-size="9" fill="#94a3b8">[valid credentials]</text>
```

## Alt Else Divider

Pure SVG dashed line inside the fragment.

```svg
<line x1="X" y1="ELSE_Y" x2="X+W" y2="ELSE_Y" stroke="#64748b" stroke-width="1" stroke-dasharray="6,4"/>
<text x="X+8" y="ELSE_Y+14" font-size="9" fill="#94a3b8">[else: invalid]</text>
```

## Note Box

Pure SVG (small inline element, no foreignObject needed).

```svg
<rect x="X" y="Y" width="W" height="24" rx="3" fill="rgba(251,191,36,0.1)" stroke="#fbbf24" stroke-width="0.8"/>
<text x="X+W/2" y="Y+16" font-size="9" fill="#fbbf24" text-anchor="middle">Note text</text>
```

## CSS Class Summary

| Class | Applied To | Description |
|-------|-----------|-------------|
| `.seq-actor` | `<div>` in foreignObject | Base style for actor boxes |
| `.actor-label` | `<span>` inside `.seq-actor` | Text label inside actor box |
| `.type-actor` | `<g>` | Stick figure actor (SVG only) |
| `.type-participant` | `<div>` in foreignObject | Participant box |
| `.type-boundary` | `<div>` in foreignObject | Boundary box (left border emphasis) |
| `.type-controller` | `<div>` in foreignObject | Controller box (darker bg) |
| `.seq-fragment` | `<div>` in foreignObject | Fragment frame box |
| `.type-alt` | `<div>` in fragment | Alt fragment variant |
| `.type-loop` | `<div>` in fragment | Loop fragment variant |
| `.type-opt` | `<div>` in fragment | Opt fragment variant |
| `.type-par` | `<div>` in fragment | Par fragment variant |

## Rendering Approach Summary

| Element | Approach | Rationale |
|---------|----------|-----------|
| Actor boxes (participant, boundary, controller) | foreignObject + CSS | Auto-sizing text, easy styling, no manual text centering |
| Stick figure actors | Pure SVG | Geometric shapes (circle, lines) — no text wrapping needed |
| Lifelines | Pure SVG | Simple dashed vertical line |
| Message arrows | Pure SVG | Lines with markers — no CSS benefit |
| Self-messages | Pure SVG | Path-based geometry |
| Activation boxes | Pure SVG | Simple colored rectangles |
| Fragment frames (alt, loop, opt, par) | foreignObject + CSS | Box rendered by CSS, label tab as SVG overlay |
| Else dividers | Pure SVG | Simple dashed line with text |
| Note boxes | Pure SVG | Small fixed-size box |
| Condition/guard text | Pure SVG `<text>` | Short inline text — no wrapping needed |

## Color Mapping per Style

| Element | Dark | Blueprint | Warm |
|---------|------|-----------|------|
| Actor box stroke | #22d3ee | #88c0d0 | #b45309 |
| Actor box background | #0f172a | #2e3440 | #f5f0e8 |
| Lifeline | #64748b | #4c566a | #a89984 |
| Sync arrow | #e2e8f0 | #eceff4 | #3c3836 |
| Return arrow | #94a3b8 | #81a1c1 | #78716c |
| Fragment border | #64748b | #4c566a | #d5c4a1 |
| Activation fill | rgba(34,211,238,0.15) | rgba(136,192,208,0.15) | rgba(180,83,9,0.1) |
