# Pastel Dream Style Reference

## Design Philosophy

**Friendly, approachable, and playful.** Soft pastel fills with generous rounding. Designed for educational content, presentations to non-technical audiences, and friendly documentation. Feels like a children's book illustration system.

## Prohibited (Do NOT)

- NO sharp corners — generous border radius on all elements
- NO dark or saturated colors — soft pastels only
- NO harsh contrasts — gentle, welcoming palette
- NO small or cramped text — readability and warmth over density
- NO decorative elements (circles, ornaments, ribbons) — pure function
- NO gradient fills on components — flat pastel fills only
- NO images or photo backgrounds — SVG only
- NO JavaScript — static HTML/CSS/SVG only

This style produces warm, friendly architecture diagrams suitable for educational materials, onboarding docs, presentations to non-technical stakeholders, and community-focused content.

## Template File

Use `assets/template-pastel-dream.html` as the starting point. It contains:
- Complete HTML structure with embedded CSS
- SVG with no grid background, arrowhead markers with rounded tips, and example components
- Summary cards section
- Footer

## How to Use This Style

### 1. Copy the template structure

Take the HTML wrapper (head, style, header, footer, cards) from the template. Replace the SVG content with your generated diagram.

### 2. Generate SVG content

Build the SVG in this order:
1. `<defs>` block (arrowhead markers) — copy from template, no grid needed
2. Connections (lines/arrows) — drawn FIRST so they appear behind components
3. Layer cards (outermost to innermost)
4. Modules inside each layer
5. Group boundaries (if any)
6. Legend

### 3. Color mapping

Look up each component's type in this table to get its colors:

| Type | Fill | Stroke | Text color |
|------|------|--------|------------|
| `process` | `rgba(134, 239, 172, 0.5)` | `#6ee7a0` | `#2d6a4f` |
| `module` | `rgba(147, 197, 253, 0.5)` | `#7db8f5` | `#1e40af` |
| `data` | `rgba(196, 181, 253, 0.5)` | `#b19cdc` | `#5b21b6` |
| `infra` | `rgba(253, 224, 71, 0.4)` | `#f0d44a` | `#854d0e` |
| `security` | `rgba(252, 165, 165, 0.5)` | `#f5a0a0` | `#9f1239` |
| `channel` | `rgba(253, 186, 116, 0.5)` | `#f5b97e` | `#9a3412` |
| `external` | `rgba(214, 188, 163, 0.5)` | `#c9a882` | `#78350f` |

### 4. Double-rect masking

Every component box uses two rects:
```svg
<rect x="..." y="..." width="..." height="..." rx="12" fill="#fef7ff"/>  <!-- opaque mask -->
<rect x="..." y="..." width="..." height="..." rx="12"                  <!-- styled box -->
      fill="rgba(...)" stroke="..." stroke-width="1.5"/>
```

The first rect (`#fef7ff`) hides connection lines behind the box and ensures the pastel fill renders cleanly over the light background.

### 5. Connection styling

- Default arrow color: `#d4b8e0` (soft lavender)
- IPC/channel connections: `#f5b97e` (soft orange)
- Auth/security connections: `#f5a0a0` (soft pink), dashed
- Arrowhead marker: `url(#arrowhead)` for forward, `url(#arrowhead-rev)` for reverse
- Connection labels: background rect in `#fef7ff` with 90% opacity and rounded corners, then text

### 6. Soft shadow on container

The main SVG container should have a subtle soft shadow applied via CSS:
```css
.diagram-container {
  filter: drop-shadow(4px 4px 8px rgba(0, 0, 0, 0.06));
}
```

### 7. "Multiple instances" effect

When a layer has `count: "multiple"`, add a second border rect offset by (+5, +4):
```svg
<rect x="45" y="184" width="500" height="120" rx="16"
      fill="none" stroke="#c9a882" stroke-width="1" opacity="0.4"/>
```

Use a softer stroke color and increased opacity for a gentle layered look.

### 8. Summary cards

Generate 3 summary cards that highlight:
1. Key structural insight (e.g., "4 Processes" for Chrome)
2. Component count or module breakdown
3. Key mechanism (e.g., "IPC Communication")

Card dot colors should match the primary component type color in its pastel form.

### 9. Page colors

| Element | Color |
|---------|-------|
| Page background | `#fef7ff` |
| Card/container bg | `#ffffff` |
| Border subtle | `rgba(0, 0, 0, 0.06)` |
| Primary text | `#3d3250` |
| Secondary text | `#6b5b7b` |
| Muted text | `#a89bb5` |
| Accent (header dot) | Match primary component type pastel color |

## Typography

| Element | Font | Size | Weight | Color |
|---------|------|------|--------|-------|
| Diagram title | Nunito, Quicksand, system-ui | 16px | 700 | `#3d3250` |
| Module labels | Nunito, Quicksand, system-ui | 13px | 600 | `#3d3250` |
| Annotations | Nunito, Quicksand, system-ui | 11px | 400 | `#6b5b7b` |
| Layer headers | Nunito, Quicksand, system-ui | 13px | 700 | `#3d3250` |
| Connection labels | Nunito, Quicksand, system-ui | 11px | 500 | `#6b5b7b` |
| Legend text | Nunito, Quicksand, system-ui | 11px | 400 | `#6b5b7b` |

## Component Details

### Layer cards
- Border: `1.5px` solid, pastel stroke color from type mapping
- Fill: semi-transparent pastel matching type
- Corner radius: `rx="16"` — generously rounded, friendly feel
- Padding between layers: extra generous for breathing room

### Module boxes
- Border: `1.5px` solid, pastel stroke
- Fill: semi-transparent pastel
- Corner radius: `rx="12"` — very rounded
- Height: `46px` — slightly taller for comfortable readability
- Text centered vertically and horizontally

### Connections
- Stroke width: `1.5px` default
- Color: soft lavender default, soft orange for channels, soft pink for security
- Arrowheads: slightly rounded, matching connection color
- Labels: pastel background rect with generous rounding

### Legend
- Horizontal or vertical list with friendly spacing
- Small rounded square swatch (`10x10`, `rx="3"`) with pastel fill
- Label in secondary text color

## Layout Adjustments

| Property | Normal | Wide |
|----------|--------|------|
| SVG width | 900 | 1200 |
| SVG height | auto (content-driven) | auto |
| Layer padding | 56px | 72px |
| Module height | 46px | 46px |
| Module gap | 14px | 20px |
| Layer gap | 28px | 40px |
| Connection label offset | 8px | 8px |
| Legend position | bottom-left | bottom-left |

All spacing should feel open and generous. The pastel dream style prioritizes comfort and approachability — every element should have room to breathe. Avoid cramming components together; the extra whitespace contributes to the friendly, readable aesthetic.
