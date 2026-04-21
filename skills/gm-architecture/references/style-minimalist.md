# Minimalist Style Reference

## Design Philosophy

**Less is more.** Ultra-clean, print-ready, maximum readability. No decoration, no color fills — structure communicates through borders and whitespace alone. Inspired by Swiss design and Dieter Rams.

## Prohibited (Do NOT)

- NO color fills on components — transparent or near-transparent fills only
- NO shadows, glow effects, or text-shadow — pure flat rendering
- NO grid background — white space is the structure
- NO gradient fills — flat and clean only
- NO decorative elements (circles, ornaments, ribbons) — pure function
- NO images or photo backgrounds — SVG only
- NO JavaScript — static HTML/CSS/SVG only
- NO bold or saturated colors — monochrome palette only

This style produces clean, print-ready architecture diagrams suitable for documentation, whitepapers, and environments where clarity and restraint are paramount.

## Template File

Use `assets/template-minimalist.html` as the starting point. It contains:
- Complete HTML structure with embedded CSS
- SVG with no grid background, simple arrowhead markers, and example components
- Summary cards section
- Footer

## How to Use This Style

### 1. Copy the template structure

Take the HTML wrapper (head, style, header, footer, cards) from the template. Replace the SVG content with your generated diagram.

### 2. Generate SVG content

Build the SVG in this order:
1. `<defs>` block (arrowhead markers) — copy from template, no grid pattern needed
2. Connections (lines/arrows) — drawn FIRST so they appear behind components
3. Layer cards (outermost to innermost)
4. Modules inside each layer
5. Group boundaries (if any)
6. Legend

### 3. Color mapping

Look up each component's type in this table to get its colors:

| Type | Fill | Stroke | Text color |
|------|------|--------|------------|
| `process` | `rgba(0, 0, 0, 0.02)` | `#4a4a4a` | `#333333` |
| `module` | `rgba(0, 0, 0, 0.03)` | `#555555` | `#333333` |
| `data` | `rgba(0, 0, 0, 0.04)` | `#666666` | `#333333` |
| `infra` | `rgba(0, 0, 0, 0.02)` | `#888888` | `#555555` |
| `security` | `rgba(0, 0, 0, 0.03)` | `#999999` | `#555555` |
| `channel` | `rgba(0, 0, 0, 0.02)` | `#aaaaaa` | `#666666` |
| `external` | `rgba(0, 0, 0, 0.01)` | `#bbbbbb` | `#777777` |

### 4. Single-rect component

Every component box uses a single rect — no masking rect needed since fills are near-transparent and connections behind are intentionally visible:
```svg
<rect x="..." y="..." width="..." height="..." rx="2"
      fill="rgba(0, 0, 0, 0.02)" stroke="#4a4a4a" stroke-width="0.5"/>
```

Keep `stroke-width` at `0.5` for the ultra-thin, precise aesthetic.

### 5. Connection styling

- Default arrow color: `#cccccc`
- IPC/channel connections: `#aaaaaa`, slightly thicker (`stroke-width="1"`)
- Auth/security connections: `#999999`, dashed (`stroke-dasharray="6 3"`)
- Arrowhead marker: `url(#arrowhead)` for forward, `url(#arrowhead-rev)` for reverse
- Connection labels: no background rect — just text in `#666666`, `font-size="10"`

### 6. "Multiple instances" effect

When a layer has `count: "multiple"`, add a second border rect offset by (+3, +2):
```svg
<rect x="43" y="182" width="500" height="120" rx="2"
      fill="none" stroke="#cccccc" stroke-width="0.3" opacity="0.5"/>
```

### 7. Summary cards

Generate 3 summary cards that highlight:
1. Key structural insight (e.g., "4 Processes" for Chrome)
2. Component count or module breakdown
3. Key mechanism (e.g., "IPC Communication")

Card styling uses light gray dots and thin borders — no color accents.

### 8. Page colors

| Element | Color |
|---------|-------|
| Page background | `#ffffff` |
| Card/container bg | `#fafafa` |
| Border subtle | `rgba(0, 0, 0, 0.08)` |
| Primary text | `#222222` |
| Secondary text | `#555555` |
| Muted text | `#999999` |
| Accent (header dot) | `#cccccc` |

## Typography

| Element | Font | Size | Weight | Color |
|---------|------|------|--------|-------|
| Diagram title | Inter, Helvetica Neue, system-ui | 14px | 600 | `#222222` |
| Module labels | Inter, Helvetica Neue, system-ui | 12px | 500 | `#333333` |
| Annotations | Inter, Helvetica Neue, system-ui | 10px | 400 | `#999999` |
| Layer headers | Inter, Helvetica Neue, system-ui | 12px | 600 | `#555555` |
| Connection labels | Inter, Helvetica Neue, system-ui | 10px | 400 | `#666666` |
| Legend text | Inter, Helvetica Neue, system-ui | 10px | 400 | `#777777` |

## Component Details

### Layer cards
- Border: `0.5px` solid, monochrome stroke color from type mapping
- Fill: near-transparent (`rgba(0, 0, 0, 0.01)` to `0.04`)
- Corner radius: `rx="2"` — barely rounded, nearly sharp
- Padding between layers: generous whitespace, no visual crowding

### Module boxes
- Border: `0.5px` solid, monochrome stroke
- Fill: near-transparent, same approach as layers
- Corner radius: `rx="1"` — essentially square
- Height: `40px` — compact
- Text centered vertically and horizontally

### Connections
- Stroke width: `0.75px` default, `1px` for emphasized connections
- Color: light gray to medium gray
- Arrowheads: small, simple triangular markers in matching gray
- Labels: plain text, no background box

### Legend
- Simple horizontal or vertical list
- Small square swatch (`8x8`) with the type's stroke color
- Label in secondary text color

## Layout Adjustments

| Property | Normal | Wide |
|----------|--------|------|
| SVG width | 900 | 1200 |
| SVG height | auto (content-driven) | auto |
| Layer padding | 60px | 80px |
| Module height | 40px | 40px |
| Module gap | 12px | 16px |
| Layer gap | 24px | 32px |
| Connection label offset | 4px | 4px |
| Legend position | bottom-left | bottom-left |

All spacing should feel generous — the hallmark of minimalist design is breathing room between elements. Prioritize whitespace over compactness.
