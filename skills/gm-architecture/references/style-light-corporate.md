# Light Corporate Style Reference

## Design Philosophy

**Clean, trustworthy, executive-ready.** The output should look like it belongs in a boardroom presentation — minimal decoration, generous whitespace, subtle accents, and a "less is more" restraint that signals professionalism.

## Prohibited (Do NOT)

- NO dark backgrounds — white/light canvas only
- NO heavy borders — 1px clean lines maximum
- NO glow, blur, or shadow effects on SVG elements — flat and clean
- NO monospace-only fonts — use system-ui/sans-serif for readability
- NO bright saturated colors — muted, professional tones only
- NO decorative elements or ornaments — pure information
- NO JavaScript — static HTML/CSS/SVG only
- NO gradient fills — solid colors only

Clean, professional business style with a white background and subtle color accents. Best for corporate presentations, documentation, and stakeholder-facing materials.

## Template File

Use `assets/template-light-corporate.html` as the starting point.

## Key Visual Properties

| Property | Value |
|----------|-------|
| Background | `#f8fafc` (cool gray) |
| Card bg | `white` |
| Font | system-ui, -apple-system, sans-serif |
| Border width | 1px, clean |
| Border color | `#e2e8f0` (light gray) |
| Shadow | Subtle `0 1px 3px rgba(0,0,0,0.04)` |
| Rounded corners | `rx="5"` (modules), `rx="6"` (layers) |

## Color Mapping

| Type | Layer bg | Layer stroke | Module fill | Module stroke |
|------|----------|-------------|-------------|---------------|
| `process` | `#eff6ff` | `#bfdbfe` | `#dbeafe` | `#1e40af` |
| `module` | `#ecfdf5` | `#a7f3d0` | `#d1fae5` | `#059669` |
| `data` | `#f5f3ff` | `#ddd6fe` | `#ede9fe` | `#7c3aed` |
| `infra` | `#fffbeb` | `#fde68a` | `#fef3c7` | `#d97706` |
| `security` | `#fef2f2` | `#fecaca` | `#fee2e2` | `#dc2626` |
| `channel` | `#fff7ed` | `#fed7aa` | `#ffedd5` | `#ea580c` |
| `external` | `#f8fafc` | `#e2e8f0` | `#f1f5f9` | `#475569` |

## Typography

- Layer labels: 13px, `font-weight: 600`, uppercase, color matches layer type stroke
- Module labels: 12px, `font-weight: 600`, `#0f172a` or type-specific color
- Annotations: 8px, type-specific color
- Connection labels: 9px, `#64748b`

## Component Details

### Header
- Uses a vertical gradient bar (4px wide) instead of a dot
- `linear-gradient(180deg, #1e40af, #059669)`

### Layer cards
- Clean 1px borders with pastel background
- Uppercase layer labels with letter-spacing

### Module boxes
- Solid colored fill matching component type
- 1px border in darker shade
- Tech badges: white bg, light colored border

### Connection lines
- 1px stroke, `#64748b`
- Solid for sync connections, dashed (`4,3`) for async
- Arrow markers: `#64748b`

### Summary cards
- White background with 1px `#e2e8f0` border
- Uses icon boxes (32x32 colored squares with text) instead of dots
- Subtle shadow: `0 1px 2px rgba(0,0,0,0.03)`

### Legend
- Compact row with colored rectangles and labels
- Includes connection type indicators (solid = Sync, dashed = Async)

## Layout Adjustments

Same coordinate system as `references/layout-rules.md`:
- `LAYER_GAP`: 50px
- `MODULE_GAP`: 20px
- All borders: 1px (thinnest of all themes)
