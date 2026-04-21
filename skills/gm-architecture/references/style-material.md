# Material Design Style Reference

## Design Philosophy

**Bold surfaces with elevation.** Google's Material Design language applied to diagrams — filled color blocks, subtle shadows, and clear hierarchy. Strong visual presence suitable for presentations and marketing materials.

## Prohibited (Do NOT)

- NO gradient fills on components — solid Material colors only
- NO grid background — clean white/gray surface
- NO thin borders — Material uses filled blocks, not outlines
- NO muted or washed-out colors — full Material palette saturation
- NO JavaScript — static HTML/CSS/SVG only
- NO text shadows on module labels — white on color is sufficient contrast

This style produces bold, presentation-ready diagrams suitable for slides, pitch decks, and marketing docs.

## Template File

Use `assets/template-material.html` as the starting point. It contains:
- Complete HTML structure with embedded CSS (Roboto font)
- SVG with arrowhead markers and example components
- Footer

## How to Use This Style

### 1. Copy the template structure

Take the HTML wrapper from the template. Replace the SVG content with your generated diagram.

### 2. Color mapping

| Type | Background | Text color |
|------|-----------|------------|
| `process` | `#1976d2` (Blue 700) | `#ffffff` |
| `module` | `#388e3c` (Green 700) | `#ffffff` |
| `data` | `#7b1fa2` (Purple 700) | `#ffffff` |
| `infra` | `#f57c00` (Orange 700) | `#ffffff` |
| `security` | `#d32f2f` (Red 700) | `#ffffff` |
| `channel` | `#0288d1` (Light Blue 700) | `#ffffff` |
| `external` | `#546e7a` (Blue Grey 600) | `#ffffff` |

### 3. Component styling

- NO border — solid filled blocks only
- Corner radius: `rx="6"` for modules, `rx="6"` for layers
- Box shadow on modules: `0 1px 3px rgba(0,0,0,0.1)`
- White text on colored backgrounds

### 4. Connection styling

- Default arrow color: `#bdbdbd`
- Connection labels: white background pill (`border-radius: 12px`), `font-size="10"`
- Arrowhead: simple triangular marker in `#757575`

### 5. Page colors

| Element | Color |
|---------|-------|
| Page background | `#fafafa` |
| Card/container bg | `#ffffff` |
| Card shadow | `0 2px 8px rgba(0,0,0,0.08)` |
| Primary text | `#212121` |
| Secondary text | `#757575` |
| Header accent | `#1976d2` |

## Typography

| Element | Font | Size | Weight | Color |
|---------|------|------|--------|-------|
| Diagram title | Roboto | 20px | 700 | `#212121` |
| Module labels | Roboto | 12px | 500 | `#ffffff` |
| Layer headers | Roboto | 13px | 700 | `#424242` |
| Connection labels | Roboto | 10px | 400 | `#757575` |
| Legend text | Roboto | 11px | 400 | `#757575` |

## Component Details

### Layer cards
- Border: none (or very thin `1px solid #e0e0e0`)
- Fill: `#ffffff` or very light gray
- Corner radius: `rx="6"`
- Subtle shadow

### Module boxes
- NO border — solid fill with Material palette color
- Corner radius: `rx="6"`
- Height: `50px`
- White text centered
- Subtle elevation shadow

### Connections
- Stroke width: `1px`
- Color: `#bdbdbd`
- Arrowheads: triangular, `#757575`

### Legend
- Horizontal list with colored swatches
- Swatch uses the full Material color (not alpha)

## Layout Adjustments

| Property | Normal |
|----------|--------|
| SVG width | 900 |
| Layer padding | 60px |
| Module height | 50px |
| Module gap | 16px |
| Layer gap | 24px |
