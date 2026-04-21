# Blueprint Technical Style Reference

## Design Philosophy

**Precise, objective, specification-grade.** The output should look like an engineering schematic — thin lines, fine grid, minimal decoration, maximum data density. Every pixel is intentional. This is a technical document, not a marketing page.

## Prohibited (Do NOT)

- NO glow, blur, or shadow effects — purely technical flat aesthetic
- NO rounded corners wider than `rx="2"` — sharp, engineering feel
- NO thick borders — 0.8-1px maximum (thinnest of all styles)
- NO saturated or vivid colors — muted Nord palette only
- NO decorative elements — no circles, ornaments, or embellishments
- NO gradient fills — flat colors only
- NO casual fonts — monospace only (JetBrains Mono)
- NO JavaScript — static HTML/CSS/SVG only
- NO wide spacing — compact, information-dense layout

Engineering blueprint aesthetic with thin precise lines, inspired by the Nord terminal color scheme. Best for technical documentation, engineering diagrams, and architectural drawings.

## Template File

Use `assets/template-blueprint.html` as the starting point.

## Key Visual Properties

| Property | Value |
|----------|-------|
| Background | `#2e3440` (Nord0, Polar Night) |
| Card bg | `#3b4252` (Nord1) |
| Surface | `#434c5e` (Nord2) |
| Font | JetBrains Mono, monospace |
| Border width | 0.8-1px (thinnest theme) |
| Rounded corners | `rx="2"` max (engineering feel) |
| No glow, no shadows | Purely technical aesthetic |

## Color Mapping (Nord)

| Type | Fill | Stroke |
|------|------|--------|
| `process` | `rgba(136,192,208,0.12)` | `#88c0d0` (Nord8, Frost) |
| `module` | `rgba(163,190,140,0.12)` | `#a3be8c` (Nord14, Aurora Green) |
| `data` | `rgba(180,142,173,0.12)` | `#b48ead` (Nord15, Aurora Purple) |
| `infra` | `rgba(235,203,139,0.12)` | `#ebcb8b` (Nord13, Aurora Yellow) |
| `security` | `rgba(191,97,106,0.12)` | `#bf616a` (Nord11, Aurora Red) |
| `channel` | `rgba(208,135,112,0.12)` | `#d08770` (Nord12, Aurora Orange) |
| `external` | `rgba(216,222,233,0.1)` | `#d8dee9` (Nord4, Snow) |

## Grid Pattern

Blueprint uses a finer 20px grid (instead of 40px) for graph-paper feel:
```svg
<pattern id="bp-grid" width="20" height="20" patternUnits="userSpaceOnUse">
  <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#4c566a" stroke-width="0.3"/>
</pattern>
```

## Typography

- Layer labels: 13px, `font-weight: 600`, colored per type, UPPERCASE optional
- Module labels: 11-12px, `font-weight: 500`, `#eceff4` (Nord6)
- Annotations: 7-8px, type-specific color
- Connection labels: 8px, `#81a1c1` (Nord9)
- Primary: `#eceff4`, Secondary: `#d8dee9`

## Component Details

### Layer cards
- Minimal rounded corners (`rx="2"`)
- Thin borders (0.8px)
- Layer header colored per type
- No background fill effects

### Module boxes
- Very thin borders (0.8px)
- Semi-transparent fills
- Compact layout (height 30px for simple modules)

### Connection lines
- Thin 1px stroke, `#81a1c1` (Nord9, Frost)
- Dashed for async: `stroke-dasharray="4,3"`
- Small precise arrowheads (7x5 marker)
- Connection labels use connection-specific colors

### Technical watermark
Add a faint watermark text at the bottom of the SVG:
```svg
<text ... font-size="9" fill="#434c5e" text-anchor="middle" letter-spacing="2">
  TECHNICAL DIAGRAM — NOT TO SCALE
</text>
```

### Summary cards
- Dark `#3b4252` background
- 1px `#4c566a` border
- `rx="2"` (minimal rounding)
- Dot colors: Frost, Aurora Green, Aurora Yellow

## Layout Adjustments

Same coordinate system as `references/layout-rules.md`:
- `LAYER_GAP`: 50px
- `MODULE_GAP`: 20px
- Borders: 0.8-1px (thinnest of all themes)
- Module height can be reduced to 30px for simple modules
- Layers can be shorter (60px vs 95px) due to compact style
