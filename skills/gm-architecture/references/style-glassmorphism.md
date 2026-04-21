# Glassmorphism Style Reference

## Design Philosophy

**Translucent depth.** Glassmorphism uses frosted glass effects, semi-transparent layers, and blur to create a sense of depth and modernity. A vibrant gradient background shines through translucent components.

## Prohibited (Do NOT)

- NO opaque solid backgrounds on components — must use translucent fills
- NO sharp corners — all elements use rounded corners
- NO flat, non-blurred surfaces — the frosted glass effect is essential
- NO dark, heavy borders — light, semi-transparent borders only
- NO JavaScript — static HTML/CSS/SVG only
- NO solid white or solid black fills — everything is translucent

This style produces modern, visually striking diagrams suitable for creative presentations, landing pages, and social media.

## Template File

Use `assets/template-glassmorphism.html` as the starting point. It contains:
- Complete HTML structure with embedded CSS (Inter font)
- Vibrant gradient background (`linear-gradient(135deg, #667eea, #764ba2, #f093fb)`)
- SVG with frosted glass container and example components
- Footer

## How to Use This Style

### 1. Copy the template structure

Take the HTML wrapper from the template. Replace the SVG content with your generated diagram. The body gradient background is critical — do not remove it.

### 2. Color mapping

| Type | Fill (glass tint) | Border | Text color |
|------|------------------|--------|------------|
| `process` | `rgba(59, 130, 246, 0.2)` | `rgba(59, 130, 246, 0.35)` | `#ffffff` |
| `module` | `rgba(34, 197, 94, 0.2)` | `rgba(34, 197, 94, 0.35)` | `#ffffff` |
| `data` | `rgba(168, 85, 247, 0.2)` | `rgba(168, 85, 247, 0.35)` | `#ffffff` |
| `infra` | `rgba(251, 191, 36, 0.2)` | `rgba(251, 191, 36, 0.35)` | `#ffffff` |
| `security` | `rgba(244, 63, 94, 0.2)` | `rgba(244, 63, 94, 0.35)` | `#ffffff` |
| `channel` | `rgba(251, 146, 60, 0.2)` | `rgba(251, 146, 60, 0.35)` | `#ffffff` |
| `external` | `rgba(148, 163, 184, 0.2)` | `rgba(148, 163, 184, 0.35)` | `#ffffff` |

### 3. Component styling

- Fill: `rgba(color, 0.15-0.2)` — translucent glass tint
- Border: `1px solid rgba(color, 0.25-0.35)` — light frosted edge
- Corner radius: `rx="10"` for modules, `rx="12"` for layers
- Box shadow: `0 4px 16px rgba(0,0,0,0.08)` — soft depth
- `backdrop-filter: blur(8px)` on module elements (CSS)

### 4. Connection styling

- Default arrow color: `rgba(255,255,255,0.4)`
- Connection labels: frosted pill background
- Arrowhead: triangular, `rgba(255,255,255,0.5)`

### 5. Page colors

| Element | Color |
|---------|-------|
| Page background | `linear-gradient(135deg, #667eea, #764ba2, #f093fb)` |
| Container | `rgba(255,255,255,0.12)` with `backdrop-filter: blur(20px)` |
| Container border | `rgba(255,255,255,0.2)` |
| Container shadow | `0 8px 32px rgba(0,0,0,0.12)` |
| Primary text | `#ffffff` |
| Secondary text | `rgba(255,255,255,0.8)` |
| Muted text | `rgba(255,255,255,0.6)` |

## Typography

| Element | Font | Size | Weight | Color |
|---------|------|------|--------|-------|
| Diagram title | Inter | 20px | 700 | `#ffffff` |
| Module labels | Inter | 12px | 500 | `#ffffff` |
| Layer headers | Inter | 13px | 600 | `#ffffff` |
| Connection labels | Inter | 10px | 400 | `rgba(255,255,255,0.8)` |
| Legend text | Inter | 11px | 400 | `rgba(255,255,255,0.8)` |

## Component Details

### Layer cards
- Fill: `rgba(255,255,255,0.08)` — very light frosted glass
- Border: `1px solid rgba(255,255,255,0.15)`
- Corner radius: `rx="12"`
- No heavy shadow — light and airy

### Module boxes
- Fill: type-specific translucent tint
- Border: type-specific light edge
- Corner radius: `rx="10"`
- Height: `50px`
- White text
- Soft shadow for depth

### Connections
- Stroke width: `1px`
- Color: `rgba(255,255,255,0.4)`
- Arrowheads: `rgba(255,255,255,0.5)`
- Labels: frosted pill background

### Legend
- Horizontal list with glass-tinted swatches
- Swatch uses type-specific translucent fill
- White border on swatch

## Layout Adjustments

| Property | Normal |
|----------|--------|
| SVG width | 900 |
| Layer padding | 60px |
| Module height | 50px |
| Module gap | 16px |
| Layer gap | 24px |

## Important Notes

- The gradient background is set on the `<body>` element, not inside SVG
- SVG elements should have no opaque backgrounds — let the body gradient show through
- `backdrop-filter: blur()` works in modern browsers; the diagram still renders acceptably without it (graceful degradation)
- Use `rgba()` exclusively — no `hsla()` or `#hex` for fills, to maintain the translucent aesthetic
