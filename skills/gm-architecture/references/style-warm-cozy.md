# Warm Cozy Style Reference

## Design Philosophy

**Friendly, inviting, human-centered.** The output should feel like a well-designed textbook illustration — warm colors, generous curves, approachable typography. The reader should feel comfortable, not intimidated. Education over impressiveness.

## Prohibited (Do NOT)

- NO dark backgrounds — warm cream/light canvas only
- NO sharp corners — use generous rounding (rx=8 minimum)
- NO neon or electric colors — earthy, natural tones only (Gruvbox palette)
- NO thin 1px borders — 2px warm strokes minimum
- NO monospace-only fonts — use serif (Georgia) for warmth
- NO glow or blur effects — solid, grounded aesthetic
- NO cold blue/gray tones — warm hues (amber, cream, muted green, soft purple)
- NO JavaScript — static HTML/CSS/SVG only
- NO cramped layouts — generous spacing and breathing room

Warm, friendly aesthetic with earthy tones, inspired by the Gruvbox terminal color scheme. Best for educational content, non-technical audiences, and approachable documentation.

## Template File

Use `assets/template-warm-cozy.html` as the starting point.

## Key Visual Properties

| Property | Value |
|----------|-------|
| Background | `#f9f5eb` (Gruvbox bg, warm cream) |
| Card bg | `#fffdf7` (warm white) |
| Border | `#d5c4a1` (Gruvbox bg3) |
| Font | Georgia, system-ui, serif |
| Border width | 2px, bold and warm |
| Rounded corners | `rx="10"` (layers), `rx="8"` (modules) |
| Shadow | `3px 3px 0px rgba(180,83,9,0.1)` (warm shadow) |

## Color Mapping (Gruvbox-inspired Tailwind shades)

| Type | Layer fill | Layer stroke | Module fill | Module stroke |
|------|-----------|-------------|-------------|---------------|
| `process` | `#fef3c7` (amber-100) | `#b45309` (amber-700) | `#fffdf7` | `#b45309` |
| `module` | `#dcfce7` (green-100) | `#15803d` (green-700) | `#fffdf7` | `#15803d` |
| `data` | `#f3e8ff` (purple-100) | `#7e22ce` (purple-700) | `#fffdf7` | `#7e22ce` |
| `infra` | `#fff7ed` (orange-100) | `#c2410c` (orange-700) | `#fffdf7` | `#c2410c` |
| `security` | `#fff1f2` (rose-100) | `#be123c` (rose-700) | `#fffdf7` | `#be123c` |
| `channel` | `#fefce8` (yellow-100) | `#a16207` (yellow-700) | `#fffdf7` | `#a16207` |
| `external` | `#f5f5f4` (stone-100) | `#57534e` (stone-600) | `#fffdf7` | `#57534e` |

## Typography

- Layer labels: 15px, `font-weight: 700`, `font-family: Georgia, serif`, type-specific stroke color
- Module labels: 13px, `font-weight: 600`, `#3c3836` (Gruvbox dark)
- Annotations: 8px, type-specific color, `font-family: system-ui`
- Connection labels: 9-10px, `font-weight: 600`, `#78716c` (stone-500)
- Primary text: `#3c3836`, Secondary: `#78716c`, Muted: `#bdae93`

## Component Details

### Decorative accents
Small decorative circles at SVG corners and midpoints:
```svg
<circle cx="30" cy="30" r="4" fill="#fef3c7" stroke="#d5c4a1" stroke-width="1"/>
```

### Layer accent dots
Small colored circle before layer label:
```svg
<circle cx="80" cy="68" r="4" fill="type-color" opacity="0.3"/>
```

### Module boxes
- White fill with colored 2px border
- `rx="8"` (very rounded)
- Drop shadow via SVG: `filter: drop-shadow(2px 2px 0px rgba(type-color,0.1))`

### Connection lines
- 2px stroke, `#78716c` (stone-500)
- `stroke-linecap="round"` and `stroke-linejoin="round"` for warm feel
- Dashed for feedback/optional: `stroke-dasharray="6,4"`

### Feedback label style
Connection labels use pill-shaped background:
```svg
<rect ... width="52" height="18" rx="9" fill="#fffdf7" stroke="#d5c4a1" stroke-width="1"/>
```

### Summary cards
- Warm white background with `#d5c4a1` border
- `rx="10"` (very rounded)
- Warm shadow: `3px 3px 0px rgba(180,83,9,0.1)`
- Card dot colors: amber, green, purple

### Header dot
Warm dot with glow:
```css
.warm-dot {
  width: 14px; height: 14px; border-radius: 50%;
  background: #b45309;
  box-shadow: 0 0 6px rgba(180, 83, 9, 0.25);
}
```

### Footer
Dashed border: `border-top: 2px dashed #d5c4a1`

## Layout Adjustments

Same coordinate system as `references/layout-rules.md`:
- `LAYER_GAP`: 50px
- `MODULE_GAP`: 20px
- Borders: 2px (thick and warm)
- Rounded corners: generous (10px for layers, 8px for modules)
