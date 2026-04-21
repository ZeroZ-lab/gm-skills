# Notion Style Reference

## Design Philosophy

**Content-first clarity.** Inspired by Notion's document aesthetic — clean white backgrounds, subtle borders, system fonts, and gentle color accents. Prioritizes readability and content over decoration.

## Prohibited (Do NOT)

- NO shadows or elevation effects — flat, border-only design
- NO gradient fills — solid colors only
- NO grid background patterns — white space is structure
- NO decorative elements — pure content focus
- NO JavaScript — static HTML/CSS/SVG only
- NO saturated or neon colors — muted, natural palette only

This style produces clean, Notion-like diagrams suitable for documentation, wikis, and internal tools.

## Template File

Use `assets/template-notion.html` as the starting point. It contains:
- Complete HTML structure with embedded CSS
- SVG with simple arrowhead markers and example components
- Footer

## How to Use This Style

### 1. Copy the template structure

Take the HTML wrapper (head, style, header, footer) from the template. Replace the SVG content with your generated diagram.

### 2. Generate SVG content

Build the SVG in this order:
1. `<defs>` block (arrowhead markers) — copy from template
2. Connections (lines/arrows) — drawn FIRST so they appear behind components
3. Layer cards
4. Modules inside each layer
5. Legend

### 3. Color mapping

| Type | Fill | Stroke | Text color |
|------|------|--------|------------|
| `process` | `rgba(35, 131, 226, 0.06)` | `rgba(35, 131, 226, 0.2)` | `#37352f` |
| `module` | `rgba(15, 157, 88, 0.06)` | `rgba(15, 157, 88, 0.2)` | `#37352f` |
| `data` | `rgba(154, 106, 255, 0.06)` | `rgba(154, 106, 255, 0.2)` | `#37352f` |
| `infra` | `rgba(234, 179, 8, 0.06)` | `rgba(234, 179, 8, 0.2)` | `#37352f` |
| `security` | `rgba(220, 38, 38, 0.06)` | `rgba(220, 38, 38, 0.2)` | `#37352f` |
| `channel` | `rgba(249, 115, 22, 0.06)` | `rgba(249, 115, 22, 0.2)` | `#37352f` |
| `external` | `rgba(107, 114, 128, 0.06)` | `rgba(107, 114, 128, 0.2)` | `#37352f` |

### 4. Component styling

- Border width: `1px`
- Corner radius: `rx="4"` for modules, `rx="4"` for layers
- Fill: semi-transparent with color-tinted alpha
- Stroke: color-matched at 20% opacity

### 5. Connection styling

- Default arrow color: `#9b9a97`
- IPC/channel: `#e8e8e5` background rect behind label
- Connection labels: `font-size="10"`, color `#9b9a97`
- Arrowhead: simple triangular marker in `#9b9a97`

### 6. Page colors

| Element | Color |
|---------|-------|
| Page background | `#ffffff` |
| Card/container bg | `#ffffff` |
| Border | `#e8e8e5` |
| Primary text | `#37352f` |
| Secondary text | `#9b9a97` |
| Header dot | `#e8e8e5` |

## Typography

| Element | Font | Size | Weight | Color |
|---------|------|------|--------|-------|
| Diagram title | System sans-serif | 20px | 600 | `#37352f` |
| Module labels | System sans-serif | 12px | 500 | `#37352f` |
| Layer headers | System sans-serif | 13px | 600 | `#37352f` |
| Connection labels | System sans-serif | 10px | 400 | `#9b9a97` |
| Legend text | System sans-serif | 11px | 400 | `#9b9a97` |

No external font loading — uses system fonts for fastest rendering.

## Component Details

### Layer cards
- Border: `1px` solid `#e8e8e5`
- Fill: white
- Corner radius: `rx="4"`
- No shadow, no glow

### Module boxes
- Border: `1px` with type-specific color at 20% alpha
- Fill: type-specific color at 6% alpha
- Corner radius: `rx="4"`
- Height: `48px`

### Connections
- Stroke width: `1px`
- Color: `#9b9a97`
- Arrowheads: simple triangles

### Legend
- Horizontal list
- Small square swatch with type fill color
- Label in `#9b9a97`

## Layout Adjustments

| Property | Normal |
|----------|--------|
| SVG width | 900 |
| Layer padding | 60px |
| Module height | 48px |
| Module gap | 16px |
| Layer gap | 24px |
