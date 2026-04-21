# Mind Map SVG Component Templates (CSS+SVG Hybrid)

Copy and adapt these SVG snippets when generating mind map HTML. All node boxes use `<foreignObject>` + CSS for rendering; connections use pure SVG `<path>` elements. Replace coordinates with computed values from `layout-mindmap.md`.

## CSS Classes

Every mind map SVG must include these CSS rules (inline `<style>` block inside the SVG). Nodes are rendered via `<foreignObject>` so CSS handles all box styling, text centering, and padding.

### Required CSS

```css
/* ---- Mind Map Node Styles ---- */
.mindmap-node {
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
  font-family: JetBrains Mono, monospace;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.node-label {
  display: inline-block;
  line-height: 1.2;
}

/* Central node — prominent circle / pill */
.type-central {
  width: 120px;
  height: 50px;
  border-radius: 25px;
  background: rgba(8, 51, 68, 0.6);
  border: 2.5px solid #22d3ee;
  font-size: 13px;
  font-weight: 700;
  color: white;
  padding: 0 12px;
}
.type-central .node-label {
  font-size: 13px;
  font-weight: 700;
  color: white;
}
/* Optional subtitle inside central node */
.type-central .node-subtitle {
  display: block;
  font-size: 9px;
  font-weight: 400;
  color: #94a3b8;
  margin-top: 1px;
}

/* Branch node — Level 1 */
.type-branch {
  height: 32px;
  min-width: 60px;
  padding: 0 12px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  color: white;
}
.type-branch .node-label {
  font-size: 11px;
  font-weight: 600;
  color: white;
}

/* Leaf node — Level 2+ */
.type-leaf {
  height: 28px;
  min-width: 50px;
  padding: 0 10px;
  border-radius: 8px;
  font-size: 10px;
  font-weight: 400;
  color: #cbd5e1;
}
.type-leaf .node-label {
  font-size: 10px;
  font-weight: 400;
  color: #cbd5e1;
}

/* ---- Branch Color Variants ---- */
/* Level 1 (top-level) uses the main color; Level 2 uses lighter shade; Level 3 uses lightest. */
/* Apply ONE color-variant class per node in addition to .type-branch or .type-leaf. */

.color-emerald-l1 {
  background: rgba(6, 78, 59, 0.5);
  border: 1.8px solid #34d399;
}
.color-emerald-l2 {
  background: rgba(6, 78, 59, 0.3);
  border: 1.2px solid #6ee7b7;
}
.color-emerald-l3 {
  background: rgba(6, 78, 59, 0.15);
  border: 0.8px solid #a7f3d0;
}

.color-violet-l1 {
  background: rgba(76, 29, 149, 0.4);
  border: 1.8px solid #a78bfa;
}
.color-violet-l2 {
  background: rgba(76, 29, 149, 0.25);
  border: 1.2px solid #c4b5fd;
}
.color-violet-l3 {
  background: rgba(76, 29, 149, 0.12);
  border: 0.8px solid #ddd6fe;
}

.color-amber-l1 {
  background: rgba(120, 53, 15, 0.4);
  border: 1.8px solid #fbbf24;
}
.color-amber-l2 {
  background: rgba(120, 53, 15, 0.25);
  border: 1.2px solid #fcd34d;
}
.color-amber-l3 {
  background: rgba(120, 53, 15, 0.12);
  border: 0.8px solid #fde68a;
}

.color-rose-l1 {
  background: rgba(136, 19, 55, 0.4);
  border: 1.8px solid #fb7185;
}
.color-rose-l2 {
  background: rgba(136, 19, 55, 0.25);
  border: 1.2px solid #fda4af;
}
.color-rose-l3 {
  background: rgba(136, 19, 55, 0.12);
  border: 0.8px solid #fecdd3;
}

.color-sky-l1 {
  background: rgba(7, 89, 133, 0.4);
  border: 1.8px solid #38bdf8;
}
.color-sky-l2 {
  background: rgba(7, 89, 133, 0.25);
  border: 1.2px solid #7dd3fc;
}
.color-sky-l3 {
  background: rgba(7, 89, 133, 0.12);
  border: 0.8px solid #bae6fd;
}

.color-orange-l1 {
  background: rgba(124, 45, 18, 0.4);
  border: 1.8px solid #fb923c;
}
.color-orange-l2 {
  background: rgba(124, 45, 18, 0.25);
  border: 1.2px solid #fdba74;
}
.color-orange-l3 {
  background: rgba(124, 45, 18, 0.12);
  border: 0.8px solid #fed7aa;
}

.color-teal-l1 {
  background: rgba(17, 94, 89, 0.4);
  border: 1.8px solid #2dd4bf;
}
.color-teal-l2 {
  background: rgba(17, 94, 89, 0.25);
  border: 1.2px solid #5eead4;
}
.color-teal-l3 {
  background: rgba(17, 94, 89, 0.12);
  border: 0.8px solid #99f6e4;
}

.color-pink-l1 {
  background: rgba(131, 24, 67, 0.4);
  border: 1.8px solid #f472b6;
}
.color-pink-l2 {
  background: rgba(131, 24, 67, 0.25);
  border: 1.2px solid #f9a8d4;
}
.color-pink-l3 {
  background: rgba(131, 24, 67, 0.12);
  border: 0.8px solid #fbcfe8;
}
```

## Color Coding System

Each top-level branch gets a distinct hue from the design system palette. Children inherit a lighter shade of their parent's color.

### Level Color Rules

| Level | CSS Class Pattern | Example |
|-------|------------------|---------|
| 0 (central node) | `.type-central` | cyan accent `#22d3ee` border |
| 1 (top-level branch) | `.type-branch .color-{name}-l1` | Emerald: `.color-emerald-l1` |
| 2 (sub-branches) | `.type-leaf .color-{name}-l2` | Emerald light: `.color-emerald-l2` |
| 3+ (deeper leaves) | `.type-leaf .color-{name}-l3` | Emerald lightest: `.color-emerald-l3` |

### Branch Color Palette (Top-Level Assignment)

Assign colors in order to top-level branches:

| Branch Index | Color Name | CSS Class | Main Hex | Light Shade (L2) | Lightest (L3) |
|-------------|-----------|-----------|----------|-----------------|---------------|
| 0 | Emerald | `.color-emerald-*` | `#34d399` | `#6ee7b7` | `#a7f3d0` |
| 1 | Violet | `.color-violet-*` | `#a78bfa` | `#c4b5fd` | `#ddd6fe` |
| 2 | Amber | `.color-amber-*` | `#fbbf24` | `#fcd34d` | `#fde68a` |
| 3 | Rose | `.color-rose-*` | `#fb7185` | `#fda4af` | `#fecdd3` |
| 4 | Sky | `.color-sky-*` | `#38bdf8` | `#7dd3fc` | `#bae6fd` |
| 5 | Orange | `.color-orange-*` | `#fb923c` | `#fdba74` | `#fed7aa` |
| 6 | Teal | `.color-teal-*` | `#2dd4bf` | `#5eead4` | `#99f6e4` |
| 7 | Pink | `.color-pink-*` | `#f472b6` | `#f9a8d4` | `#fbcfe8` |

For styles other than dark-professional, adapt colors from the style's design system.

## 1. Central Node (foreignObject + CSS)

The central node uses a `<foreignObject>` with CSS pill/rounded styling. Position the `<g>` wrapper at `(x, y)` where `x = center_x - 60` and `y = center_y - 25` (half of 120x50).

```svg
<g transform="translate(540, 391)">
  <foreignObject width="120" height="50">
    <div xmlns="http://www.w3.org/1999/xhtml" class="mindmap-node type-central">
      <span class="node-label">gmdiagram</span>
    </div>
  </foreignObject>
</g>
```

With subtitle:

```svg
<g transform="translate(540, 391)">
  <foreignObject width="120" height="50">
    <div xmlns="http://www.w3.org/1999/xhtml" class="mindmap-node type-central">
      <span class="node-label">gmdiagram<br/><span class="node-subtitle">Skill Engine</span></span>
    </div>
  </foreignObject>
</g>
```

## 2. Branch Node — Level 1 (foreignObject + CSS)

Top-level branch. Use `.type-branch` plus the branch's color variant class. The `<foreignObject>` dimensions use fixed height (32px) and estimated width. The `translate(x, y)` is the top-left corner of the node box.

```svg
<!-- Branch node: "Diagram Types" (Level 1, right side, emerald) -->
<g transform="translate(770, 214)">
  <foreignObject width="120" height="32">
    <div xmlns="http://www.w3.org/1999/xhtml"
         class="mindmap-node type-branch color-emerald-l1">
      <span class="node-label">Diagram Types</span>
    </div>
  </foreignObject>
</g>
```

## 3. Leaf Node — Level 2 (foreignObject + CSS)

Sub-branch. Use `.type-leaf` plus the lighter color variant. Fixed height 28px.

```svg
<!-- Sub-branch: "Architecture" (Level 2, right side, light emerald) -->
<g transform="translate(910, 90)">
  <foreignObject width="100" height="28">
    <div xmlns="http://www.w3.org/1999/xhtml"
         class="mindmap-node type-leaf color-emerald-l2">
      <span class="node-label">Architecture</span>
    </div>
  </foreignObject>
</g>
```

## 4. Leaf Node — Level 3+ (foreignObject + CSS)

Deepest level. Use `.type-leaf` plus the lightest color variant. Fixed height 28px.

```svg
<!-- Leaf node: "REST API" (Level 3, right side, lightest emerald) -->
<g transform="translate(1050, 150)">
  <foreignObject width="80" height="28">
    <div xmlns="http://www.w3.org/1999/xhtml"
         class="mindmap-node type-leaf color-emerald-l3">
      <span class="node-label">REST API</span>
    </div>
  </foreignObject>
</g>
```

## 5. Branch Connection: Right Side (SVG Cubic Bezier)

Connections remain pure SVG `<path>`. No CSS needed for paths.

Connects parent's right edge to child's left edge, curving smoothly rightward.

```svg
<!-- Connection: central node -> Diagram Types (right side) -->
<path d="M 660,416 C 700,416 730,230 770,230"
      fill="none" stroke="#34d399" stroke-width="1.5" opacity="0.7"/>

<!-- Connection: Diagram Types -> Architecture (right side, level 2) -->
<path d="M 890,230 C 930,230 950,106 990,106"
      fill="none" stroke="#6ee7b7" stroke-width="1.2" opacity="0.6"/>
```

**Right-side path formula**:
```
M x1,y1 C (x1+40),y1 (x2-40),y2 x2,y2
```
Where:
- `(x1, y1)` = parent right edge center = `(parent_x + parent_w, parent_y + parent_h/2)`
- `(x2, y2)` = child left edge center = `(child_x, child_y + child_h/2)`

For central node: `x1 = center_x + 60` (half of central node width 120).

## 6. Branch Connection: Left Side (SVG Cubic Bezier)

Connects parent's left edge to child's right edge, curving smoothly leftward.

```svg
<!-- Connection: central node -> Output Formats (left side) -->
<path d="M 540,416 C 500,416 430,323 430,323"
      fill="none" stroke="#fbbf24" stroke-width="1.5" opacity="0.7"/>

<!-- Connection: Output Formats -> HTML (left side, level 2) -->
<path d="M 330,307 C 290,307 250,270 250,270"
      fill="none" stroke="#fcd34d" stroke-width="1.2" opacity="0.6"/>
```

**Left-side path formula**:
```
M x1,y1 C (x1-40),y1 (x2+40),y2 x2,y2
```
Where:
- `(x1, y1)` = parent left edge center = `(parent_x, parent_y + parent_h/2)`
- `(x2, y2)` = child right edge center = `(child_x + child_w, child_y + child_h/2)`

For central node: `x1 = center_x - 60` (half of central node width 120).

## 7. Branch Connection: From Central Node

Special case — connections originate from the central node pill edge rather than a branch node edge.

```svg
<!-- Right-side from central node -->
<!-- x1 = center_x + 60 (half central width), y1 = center_y -->
<path d="M 660,416 C 700,416 730,230 770,230"
      fill="none" stroke="#34d399" stroke-width="1.5" opacity="0.7"/>

<!-- Left-side from central node -->
<!-- x1 = center_x - 60, y1 = center_y -->
<path d="M 540,416 C 500,416 430,323 430,323"
      fill="none" stroke="#fbbf24" stroke-width="1.5" opacity="0.7"/>
```

## 8. Legend (foreignObject + CSS)

```svg
<g transform="translate(40, 860)">
  <foreignObject width="500" height="40">
    <div xmlns="http://www.w3.org/1999/xhtml" style="display:flex;align-items:center;gap:20px;font-family:JetBrains Mono,monospace;">
      <span style="font-size:11px;font-weight:600;color:#cbd5e1;">Legend</span>
      <div style="display:flex;align-items:center;gap:6px;">
        <span style="display:inline-block;width:14px;height:14px;border-radius:3px;background:rgba(6,78,59,0.5);border:1px solid #34d399;"></span>
        <span style="font-size:11px;color:#cbd5e1;">Diagram Types</span>
      </div>
      <div style="display:flex;align-items:center;gap:6px;">
        <span style="display:inline-block;width:14px;height:14px;border-radius:3px;background:rgba(76,29,149,0.4);border:1px solid #a78bfa;"></span>
        <span style="font-size:11px;color:#cbd5e1;">Visual Styles</span>
      </div>
    </div>
  </foreignObject>
</g>
```

## 9. SVG Defs and Style Block (Required at Start of Every Mind Map SVG)

Every mind map SVG must include the CSS `<style>` block and shared SVG `<defs>`.

```svg
<defs>
  <!-- Grid pattern (optional, for background) -->
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(51, 65, 85, 0.3)" stroke-width="0.5"/>
  </pattern>
  <!-- Glow filter for central node (optional) -->
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="4" result="blur"/>
    <feMerge>
      <feMergeNode in="blur"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>
</defs>
<style>
  /* Paste the full CSS from the "Required CSS" section above here */
  .mindmap-node { /* ... */ }
  .node-label   { /* ... */ }
  .type-central { /* ... */ }
  .type-branch  { /* ... */ }
  .type-leaf    { /* ... */ }
  /* ... color variants ... */
</style>
```

## 10. Full Node Pattern (Reference)

The universal pattern for any mind map node:

```svg
<g transform="translate(X, Y)">
  <foreignObject width="W" height="H">
    <div xmlns="http://www.w3.org/1999/xhtml" class="mindmap-node TYPE CLASS">
      <span class="node-label">Label Text</span>
    </div>
  </foreignObject>
</g>
```

| Placeholder | Values | Notes |
|------------|--------|-------|
| `X, Y` | Computed top-left corner | From layout algorithm |
| `W` | `120` for central, estimated for branch/leaf | CSS auto-sizes content |
| `H` | `50` for central, `32` for branch, `28` for leaf | Fixed heights |
| `TYPE` | `type-central` / `type-branch` / `type-leaf` | Controls sizing and font |
| `CLASS` | `color-{name}-l{1|2|3}` | Controls color scheme |
| `Label Text` | Node label string | CSS handles centering |

## Style-Specific Adaptations

### dark-professional
- Central node: CSS `.type-central` with `rgba(8, 51, 68, 0.6)` background, `#22d3ee` border
- Connections: colored stroke with `opacity="0.7"`
- Background: `#0f172a` with grid pattern

### hand-drawn
- Add `stroke-dasharray: 3,2` to `.type-branch` and `.type-leaf` CSS rules
- Use `stroke-width: 2` for branch nodes
- Connections: `stroke-dasharray="6,3"` on `<path>` elements

### light-corporate
- Central node: `background: #1e40af`, `border-color: #3b82f6`, white text
- Branches: white fill with colored left border (`border-left: 3px solid`)
- Connections: thin gray or colored lines

### cyberpunk-neon
- Central node: apply SVG `filter="url(#glow)"` on the `<g>` wrapper, bright neon border
- Connections: double-stroke neon lines (draw two `<path>` elements: thick translucent + thin bright)
- Branches: dark fill with neon border colors

### blueprint
- Central node: white background, blue border, `stroke-width: 2`
- Branches: light blue background, darker blue border
- Connections: dashed blue lines (`stroke-dasharray="8,4"`)

### warm-cozy
- Central node: warm orange/brown background, cream text
- Branches: soft pastel backgrounds with warm borders
- Connections: soft brown/orange curves
