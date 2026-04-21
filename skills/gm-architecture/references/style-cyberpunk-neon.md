# Cyberpunk Neon Style Reference

## Design Philosophy

**Futuristic, immersive, electric.** The output should feel like a holographic display from a sci-fi interface — glowing borders, neon traces, and an atmosphere of advanced technology. The diagram is not just information; it's an experience.

## Prohibited (Do NOT)

- NO light/white backgrounds — dark canvas only (#11111b)
- NO flat borders without glow — every border must have the glow filter
- NO pastel or muted colors — vivid neon palette only (Catppuccin Mocha brights)
- NO rounded corners wider than `rx="8"` — keep it sharp
- NO serif fonts — monospace only (JetBrains Mono)
- NO solid connection lines without glow — all traces must glow
- NO decorative elements that don't convey information — functional futurism
- NO JavaScript — static HTML/CSS/SVG only

Dark theme with neon glow effects, inspired by the Catppuccin Mocha terminal color scheme. Best for tech-forward content, developer tools, and futuristic aesthetics.

## Template File

Use `assets/template-cyberpunk-neon.html` as the starting point.

## Key Visual Properties

| Property | Value |
|----------|-------|
| Background | `#11111b` (Catppuccin Crust) |
| Card bg | `#1e1e2e` (Catppuccin Base) |
| Surface | `#181825` (Catppuccin Mantle) |
| Font | JetBrains Mono, monospace |
| Border width | 1.2px with glow filter |
| Glow filter | `feGaussianBlur stdDeviation="2"` + merge |

## Color Mapping (Catppuccin Mocha)

| Type | Fill | Stroke | Glow color |
|------|------|--------|------------|
| `process` | `rgba(137,180,250,0.08)` | `#89b4fa` (Blue) | Blue glow |
| `module` | `rgba(166,227,161,0.1)` | `#a6e3a1` (Green) | Green glow |
| `data` | `rgba(203,166,247,0.1)` | `#cba6f7` (Mauve) | Mauve glow |
| `infra` | `rgba(249,226,175,0.06)` | `#f9e2af` (Yellow) | Yellow glow |
| `security` | `rgba(243,139,168,0.1)` | `#f38ba8` (Red) | Red glow |
| `channel` | `rgba(250,179,135,0.1)` | `#fab387` (Peach) | Peach glow |
| `external` | `rgba(108,112,134,0.15)` | `#6c7086` (Overlay0) | No glow |

## Neon Glow Effect

Apply SVG filter to borders and connection lines:
```svg
<defs>
  <filter id="glow">
    <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
    <feMerge>
      <feMergeNode in="coloredBlur"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>
</defs>
```

Apply with `filter="url(#glow)"` on stroke elements.

## Typography

- Layer labels: 13px, `font-weight: 600`, `#cdd6f4` (Text)
- Module labels: 12px, `font-weight: 500`, `#cdd6f4`
- Annotations: 8px, `#a6adc8` (Subtext0)
- Connection labels: 9px, matches connection stroke color
- Primary text: `#cdd6f4`, Secondary: `#a6adc8`, Muted: `#6c7086`

## Component Details

### Double-rect masking (same as dark-professional)
```svg
<rect ... fill="#181825"/>
<rect ... fill="rgba(type-color,0.1)" stroke="type-color" stroke-width="1.2" filter="url(#glow)"/>
```

### Grid pattern
Same 40px grid as dark style, but using Catppuccin colors:
```svg
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
  <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#313244" stroke-width="0.5" opacity="0.4"/>
</pattern>
```

### Security components
Dashed borders: `stroke-dasharray="6,3"` with red glow.

### External components
Dashed borders: `stroke-dasharray="4,3"`, no glow, muted overlay color.

### Arrow markers
Multiple colored markers for different connection types:
```svg
<marker id="arrow-blue" ...>fill="#89b4fa"</marker>
<marker id="arrow-green" ...>fill="#a6e3a1"</marker>
<marker id="arrow-mauve" ...>fill="#cba6f7"</marker>
<marker id="arrow-peach" ...>fill="#fab387"</marker>
```

### Summary cards
- Dark background with `#1e1e2e`
- Dots have colored glow: `box-shadow: 0 0 6px rgba(color,0.5)`
- Optional hover effect: `box-shadow: 0 0 12px rgba(137,180,250,0.08)`

### Pulse animation (header)
Same as dark-professional but with Catppuccin Blue.

## Layout Adjustments

Same coordinate system as `references/layout-rules.md`:
- `LAYER_GAP`: 50px
- `MODULE_GAP`: 20px
- Borders: 1.2px (slightly thicker than dark-professional for glow visibility)
