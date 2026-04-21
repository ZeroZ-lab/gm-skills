# Terminal Retro Style Reference

## Design Philosophy

**CRT nostalgia meets modern diagrams.** Green phosphor on deep black, scanline overlay, glowing text. Like reading architecture docs on a vintage terminal. Fun for developer blogs and tech-forward content.

## Prohibited (Do NOT)

- NO light or pastel backgrounds — deep black only
- NO rounded corners wider than `rx="4"` — keep it blocky and terminal-like
- NO sans-serif fonts — monospace only
- NO drop shadows — use text-shadow glow instead
- NO decorative elements (circles, ornaments, ribbons) — pure function
- NO gradient fills on components — flat fills only (scanline overlay is on container, not components)
- NO images or photo backgrounds — SVG only
- NO JavaScript — static HTML/CSS/SVG only

This style produces retro-themed, terminal-inspired architecture diagrams suitable for developer blogs, tech-forward presentations, and creative technical content.

## Template File

Use `assets/template-terminal-retro.html` as the starting point. It contains:
- Complete HTML structure with embedded CSS
- SVG with faint green grid background, arrowhead markers, scanline overlay, and example components
- Summary cards section
- Footer

## How to Use This Style

### 1. Copy the template structure

Take the HTML wrapper (head, style, header, footer, cards) from the template. Replace the SVG content with your generated diagram.

### 2. Generate SVG content

Build the SVG in this order:
1. `<defs>` block (faint green grid pattern, arrowhead markers) — copy from template
2. Grid background `<rect>`
3. Connections (lines/arrows) — drawn FIRST so they appear behind components
4. Layer cards (outermost to innermost)
5. Modules inside each layer
6. Group boundaries (if any)
7. Legend
8. Scanline overlay `<rect>` on top of the entire SVG (semi-transparent)

### 3. Color mapping

Look up each component's type in this table to get its colors:

| Type | Fill | Stroke | Text color |
|------|------|--------|------------|
| `process` | `rgba(0, 255, 65, 0.08)` | `#00ff41` | `#00ff41` |
| `module` | `rgba(0, 255, 65, 0.12)` | `#00cc33` | `#00ff41` |
| `data` | `rgba(0, 200, 80, 0.1)` | `#00c850` | `#00e646` |
| `infra` | `rgba(255, 170, 0, 0.08)` | `#ffaa00` | `#ffaa00` |
| `security` | `rgba(255, 50, 50, 0.1)` | `#ff3232` | `#ff3232` |
| `channel` | `rgba(0, 220, 255, 0.08)` | `#00dcff` | `#00dcff` |
| `external` | `rgba(0, 255, 65, 0.04)` | `#007a20` | `#00aa2a` |

### 4. Double-rect masking

Every component box uses two rects:
```svg
<rect x="..." y="..." width="..." height="..." rx="3" fill="#0a0a0a"/>  <!-- opaque mask -->
<rect x="..." y="..." width="..." height="..." rx="3"                   <!-- styled box -->
      fill="rgba(...)" stroke="..." stroke-width="1"/>
```

The first rect (`#0a0a0a`) hides connection lines behind the box. Without it, arrows bleed through the semi-transparent fill.

### 5. Connection styling

- Default arrow color: `#005a15`
- IPC/channel connections: `#00dcff` (cyan)
- Auth/security connections: `#ff3232` (red), dashed
- Arrowhead marker: `url(#arrowhead)` for forward, `url(#arrowhead-rev)` for reverse
- Connection labels: background rect in `#0a0a0a` with 85% opacity, then text in phosphor green

### 6. Scanline overlay

After all SVG content, add a scanline effect rect covering the entire diagram:
```svg
<rect x="0" y="0" width="100%" height="100%"
      fill="url(#scanlines)" opacity="0.06" pointer-events="none"/>
```

Define the scanline pattern in `<defs>`:
```svg
<pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
  <rect width="4" height="2" fill="transparent"/>
  <rect y="2" width="4" height="2" fill="rgba(0,0,0,0.15)"/>
</pattern>
```

### 7. Text glow effect

All text labels should have a subtle phosphor glow via text-shadow (applied in CSS):
```css
text.label { text-shadow: 0 0 4px rgba(0, 255, 65, 0.4); }
```

### 8. "Multiple instances" effect

When a layer has `count: "multiple"`, add a second border rect offset by (+4, +3):
```svg
<rect x="44" y="183" width="500" height="120" rx="4"
      fill="none" stroke="#00ff41" stroke-width="0.5" opacity="0.3"/>
```

### 9. Summary cards

Generate 3 summary cards that highlight:
1. Key structural insight (e.g., "4 Processes" for Chrome)
2. Component count or module breakdown
3. Key mechanism (e.g., "IPC Communication")

Card dot colors should use the phosphor green accent or the primary component type color from the mapping.

### 10. Page colors

| Element | Color |
|---------|-------|
| Page background | `#0a0a0a` |
| Card/container bg | `#111111` |
| Border subtle | `rgba(0, 255, 65, 0.1)` |
| Primary text | `#00ff41` |
| Secondary text | `#00aa2a` |
| Muted text | `#005a15` |
| Accent (header dot) | `#00ff41` |

## Typography

| Element | Font | Size | Weight | Color |
|---------|------|------|--------|-------|
| Diagram title | Courier New, IBM Plex Mono, monospace | 16px | 700 | `#00ff41` |
| Module labels | Courier New, IBM Plex Mono, monospace | 13px | 500 | `#00ff41` |
| Annotations | Courier New, IBM Plex Mono, monospace | 11px | 400 | `#00aa2a` |
| Layer headers | Courier New, IBM Plex Mono, monospace | 13px | 700 | `#00ff41` |
| Connection labels | Courier New, IBM Plex Mono, monospace | 10px | 400 | `#00dcff` |
| Legend text | Courier New, IBM Plex Mono, monospace | 11px | 400 | `#00aa2a` |

All text should have the phosphor glow applied: `text-shadow: 0 0 4px rgba(0, 255, 65, 0.4)`.

## Component Details

### Layer cards
- Border: `1px` solid, phosphor green or typed color stroke
- Fill: near-transparent green/amber/cyan depending on type
- Corner radius: `rx="4"` — slightly rounded, blocky terminal feel
- Scanline overlay on top of everything

### Module boxes
- Border: `1px` solid, typed color stroke
- Fill: near-transparent, matching type color
- Corner radius: `rx="3"`
- Height: `44px` — slightly taller to accommodate monospace text
- Text centered vertically and horizontally
- All labels have subtle text glow

### Connections
- Stroke width: `1px` default
- Color: dark green default, cyan for channels, red for security
- Arrowheads: angular, matching connection color
- Labels: monospace text with dark background rect

### Legend
- Horizontal or vertical list with terminal-style formatting
- Small square swatch (`8x8`) with typed stroke color
- Label in phosphor green or secondary text color

## Layout Adjustments

| Property | Normal | Wide |
|----------|--------|------|
| SVG width | 900 | 1200 |
| SVG height | auto (content-driven) | auto |
| Grid spacing | 40px | 40px |
| Grid color | `rgba(0, 255, 65, 0.05)` | `rgba(0, 255, 65, 0.05)` |
| Layer padding | 40px | 56px |
| Module height | 44px | 44px |
| Module gap | 10px | 14px |
| Layer gap | 20px | 28px |
| Connection label offset | 6px | 6px |
| Legend position | bottom-left | bottom-left |

Module widths should be slightly wider than other styles to accommodate the wider character width of monospace fonts. Prioritize readability of the terminal-style text over compact layout.
