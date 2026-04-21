# Design System Reference

## Color Palette (Dark Professional Theme)

### Background
- Page background: `#020617` (slate-950)
- Grid lines: `rgba(51, 65, 85, 0.3)` (slate-700, 30% opacity)
- Grid spacing: 40px
- Card background: `#0f172a` (slate-900)

### Component Colors (Fill + Stroke)

| Type | Fill (rgba) | Stroke | Use for |
|------|-------------|--------|---------|
| `process` | `rgba(8, 51, 68, 0.4)` | `#22d3ee` (cyan-400) | Processes, services |
| `module` | `rgba(6, 78, 59, 0.4)` | `#34d399` (emerald-400) | Sub-modules, libraries |
| `data` | `rgba(76, 29, 149, 0.4)` | `#a78bfa` (violet-400) | Databases, storage |
| `infra` | `rgba(120, 53, 15, 0.3)` | `#fbbf24` (amber-400) | Infrastructure, cloud |
| `security` | `rgba(136, 19, 55, 0.4)` | `#fb7185` (rose-400) | Auth, encryption |
| `channel` | `rgba(251, 146, 60, 0.3)` | `#fb923c` (orange-400) | Message buses, IPC |
| `external` | `rgba(30, 41, 59, 0.5)` | `#94a3b8` (slate-400) | External systems |

### Masking
All semi-transparent component boxes MUST have an opaque background rect underneath:
1. First draw: `<rect fill="#0f172a" .../>` (masks arrows behind the box)
2. Then draw: `<rect fill="rgba(...)" stroke="..." .../>` (the visible styled box)

## Typography

- Font: `JetBrains Mono, 'SF Mono', 'Fira Code', monospace`
- Layer label: 14px, font-weight 600, fill white
- Module label: 12px, font-weight 500, fill white
- Sub-label / annotation: 9px, fill #94a3b8 (slate-400)
- Tech badge: 8px, fill #64748b (slate-500)
- Connection label: 10px, fill #94a3b8 (slate-400)
- Legend text: 11px, fill #cbd5e1 (slate-300)

## CSS Layout in SVG (MANDATORY)

Use `<foreignObject>` with CSS flexbox for all component layout. This eliminates coordinate arithmetic errors.

### Why CSS Layout

LLMs cannot reliably compute pixel coordinates. CSS flexbox/grid handles:
- **Module width**: `min-width: 100px; padding: 0 16px` → browser auto-sizes from label text
- **Module centering**: `justify-content: center` → no `module_x` calculation needed
- **Text centering**: `display: flex; align-items: center; justify-content: center` → no `text-anchor`/`dominant-baseline` math
- **Equal spacing**: `gap: 20px` → guaranteed consistent gaps between modules
- **Tech badges**: `display: inline-flex; gap: 4px` → auto-flow badges below labels

### The foreignObject Pattern

Every component box (layer card, module, legend) MUST use this pattern:

```svg
<!-- Layer positioned via translate — only y-coordinate needs computing -->
<g transform="translate(40, 40)">
  <!-- Masking rect (required: hides arrows behind this layer) -->
  <rect width="920" height="120" rx="8" fill="#0f172a"/>
  <!-- foreignObject with HTML content -->
  <foreignObject width="920" height="120">
    <div xmlns="http://www.w3.org/1999/xhtml" class="layer-card type-process">
      <div class="layer-label">Browser Process</div>
      <div class="modules">
        <div class="module type-module"><span class="module-label">UI / Tabs</span></div>
        <div class="module type-module"><span class="module-label">Network</span></div>
        <div class="module type-data"><span class="module-label">Storage</span></div>
      </div>
    </div>
  </foreignObject>
</g>
```

**CRITICAL**: Every `<foreignObject>` MUST include `xmlns="http://www.w3.org/1999/xhtml"` on the root HTML element.

### What CSS Handles vs What SVG Handles

| Handled by CSS (no LLM math) | Handled by SVG (LLM computes) |
|-------------------------------|-------------------------------|
| Module width, height, padding | Arrow start/end x,y coordinates |
| Text centering (flex) | Arrowhead markers (`<marker>`) |
| Module spacing (flex gap) | Connection labels (SVG `<text>`) |
| Module centering in layer | Grid background pattern |
| Tech badge layout | Glow/filter effects |
| Legend item spacing | Non-rectangular shapes (diamonds, etc.) |

### CSS Classes (defined in each template's `<style>`)

Each template defines these classes with style-appropriate colors:

```css
.layer-card { width:100%; border-radius:8px; padding:8px 0 12px; box-sizing:border-box; }
.layer-label { font-size:14px; font-weight:600; padding:0 16px; }
.modules { display:flex; gap:20px; justify-content:center; padding:8px 16px 0; flex-wrap:wrap; }
.module { min-width:100px; height:50px; border-radius:6px; display:flex; align-items:center;
          justify-content:center; padding:0 16px; box-sizing:border-box; }
.module-label { font-size:12px; font-weight:500; text-align:center; white-space:nowrap; }
.tech-badges { display:flex; gap:4px; justify-content:center; padding-top:4px; }
.tech-badge { font-size:8px; padding:2px 6px; border-radius:4px; white-space:nowrap; }

/* Type-specific colors (dark-professional example) */
.type-process { background:rgba(8,51,68,0.4); border:1.5px solid #22d3ee; }
.type-module { background:rgba(6,78,59,0.4); border:1.5px solid #34d399; }
.type-data { background:rgba(76,29,149,0.4); border:1.5px solid #a78bfa; }
.type-infra { background:rgba(120,53,15,0.3); border:1.5px solid #fbbf24; }
.type-security { background:rgba(136,19,55,0.4); border:1.5px solid #fb7185; }
.type-channel { background:rgba(251,146,60,0.3); border:1.5px solid #fb923c; }
.type-external { background:rgba(30,41,59,0.5); border:1.5px solid #94a3b8; }
```

### When SVG `<text>` Is Still Needed

For elements that cannot use foreignObject (connection labels, arrow labels), use SVG `<text>` with:
```svg
text-anchor="middle" dominant-baseline="central"
```

## Spacing

- Layer vertical gap: 50px
- Module horizontal gap: 20px
- Module internal padding: 16px (horizontal), 12px (vertical)
- Module minimum width: 100px
- Module minimum height: 50px
- Layer card padding: 16px
- Legend offset from diagram: 30px below lowest element
- Page margin: 40px

## Borders & Shapes

- Component box: `rx="6"`, stroke-width 1.5px
- Security group: `rx="8"`, stroke-dasharray="6,4", stroke-width 1.5px, stroke rose
- Region boundary: `rx="12"`, stroke-dasharray="8,4", stroke-width 1.5px, stroke amber
- Layer card: `rx="8"`, stroke-width 1px

## Arrows & Connections

- Arrow marker: filled triangle, size 8x6, same color as stroke
- Default stroke: #64748b (slate-500), stroke-width 1.5px
- Bidirectional: arrowheads on both ends
- Dashed: stroke-dasharray="6,4"
- Dotted: stroke-dasharray="2,4"
- Connection labels: positioned at midpoint of the line, with small background rect

## Tech Badges

- Small pill shapes below module name
- Fill: rgba(255,255,255,0.08)
- Stroke: rgba(255,255,255,0.15)
- rx="4", height 16px
- Text: 8px, fill #94a3b8

## Page Structure

```
┌─────────────────────────────────────┐
│ Header: Title + Subtitle + Dot      │
├─────────────────────────────────────┤
│                                     │
│   SVG Diagram (in rounded card)     │
│   ┌───────────────────────────────┐ │
│   │  Grid background              │ │
│   │  Layer 1: [...]               │ │
│   │  Layer 2: [...]               │ │
│   │  Layer 3: [...]               │ │
│   │  Legend                        │ │
│   └───────────────────────────────┘ │
│                                     │
│ Footer                              │
└─────────────────────────────────────┘
```

## Icon System

Icons can be referenced in the JSON schema via the optional `"icon"` field:
```json
{ "id": "api-server", "label": "API Server", "type": "module", "icon": "tabler-server" }
```

### Sizing Rules
- Icon viewBox: 24×24
- Rendered size: 16×16 (inside modules), 20×20 (inside layer headers)
- Position: 8px left of the label text
- Module width calculation: add 24px (16px icon + 8px gap) when icon is present

### Color Rules
- Icon stroke/fill color inherits the component's stroke color
- In dark themes: use stroke with no fill (outline style)
- In light themes: use fill with no stroke (solid style)
- Icons must adapt to the current style's color system

### Embedding in SVG
```svg
<g transform="translate(x, y)">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="[path from catalog]"/>
  </svg>
</g>
```

### Icon Catalog
See `references/icons-catalog.md` for the full list of available icons with SVG paths.
