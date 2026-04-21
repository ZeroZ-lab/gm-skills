# Dark Professional Style Reference

## Design Philosophy

**Dramatic, high-contrast, presentation-ready.** The output should look like a premium tech keynote slide — dark canvas with vivid neon accents, precise geometry, and clear information hierarchy. Every element should command attention.

## Prohibited (Do NOT)

- NO rounded corners wider than `rx="8"` — keep it sharp and technical
- NO pastel or muted colors — colors must be vivid and saturated
- NO drop shadows on SVG elements — use opacity and glow borders only
- NO decorative elements (circles, ornaments, ribbons) — pure function
- NO gradient fills — flat semi-transparent fills only
- NO images or photo backgrounds — SVG only
- NO JavaScript — static HTML/CSS/SVG only

This style produces dark-themed, professional architecture diagrams suitable for technical articles, documentation, and presentations.

## Template File

Use `assets/template-dark.html` as the starting point. It contains:
- Complete HTML structure with embedded CSS
- SVG with grid background, arrowhead markers, and example components
- Summary cards section
- Footer

## How to Use This Style

### 1. Copy the template structure

Take the HTML wrapper (head, style, header, footer, cards) from the template. Replace the SVG content with your generated diagram.

### 2. Generate SVG content

Build the SVG in this order:
1. `<defs>` block (grid pattern, arrowhead markers) — copy from template
2. Grid background `<rect>`
3. Connections (lines/arrows) — drawn FIRST so they appear behind components
4. Layer cards (outermost to innermost)
5. Modules inside each layer
6. Group boundaries (if any)
7. Legend

### 3. Color mapping

Look up each component's type in this table to get its colors:

| Type | Fill | Stroke | Text color |
|------|------|--------|------------|
| `process` | `rgba(8, 51, 68, 0.4)` | `#22d3ee` | `#22d3ee` |
| `module` | `rgba(6, 78, 59, 0.4)` | `#34d399` | `#34d399` |
| `data` | `rgba(76, 29, 149, 0.4)` | `#a78bfa` | `#a78bfa` |
| `infra` | `rgba(120, 53, 15, 0.3)` | `#fbbf24` | `#fbbf24` |
| `security` | `rgba(136, 19, 55, 0.4)` | `#fb7185` | `#fb7185` |
| `channel` | `rgba(251, 146, 60, 0.3)` | `#fb923c` | `#fb923c` |
| `external` | `rgba(30, 41, 59, 0.5)` | `#94a3b8` | `#94a3b8` |

### 4. Double-rect masking

Every component box uses two rects:
```svg
<rect x="..." y="..." width="..." height="..." rx="6" fill="#0f172a"/>  <!-- opaque mask -->
<rect x="..." y="..." width="..." height="..." rx="6"                   <!-- styled box -->
      fill="rgba(...)" stroke="..." stroke-width="1.5"/>
```

The first rect (`#0f172a`) hides connection lines behind the box. Without it, arrows bleed through the semi-transparent fill.

### 5. Connection styling

- Default arrow color: `#64748b`
- IPC/channel connections: `#fb923c` (orange)
- Auth/security connections: `#fb7185` (rose), dashed
- Arrowhead marker: `url(#arrowhead)` for forward, `url(#arrowhead-rev)` for reverse
- Connection labels: background rect in `#020617` with 90% opacity, then text

### 6. "Multiple instances" effect

When a layer has `count: "multiple"`, add a second border rect offset by (+4, +3):
```svg
<rect x="44" y="183" width="500" height="120" rx="8"
      fill="none" stroke="#22d3ee" stroke-width="0.5" opacity="0.3"/>
```

### 7. Summary cards

Generate 3 summary cards that highlight:
1. Key structural insight (e.g., "4 Processes" for Chrome)
2. Component count or module breakdown
3. Key mechanism (e.g., "IPC Communication")

Card dot colors should match the primary component type used.

### 8. Page colors

| Element | Color |
|---------|-------|
| Page background | `#020617` |
| Card/container bg | `#0f172a` |
| Border subtle | `rgba(255,255,255,0.06)` |
| Primary text | `#f1f5f9` |
| Secondary text | `#94a3b8` |
| Muted text | `#64748b` |
| Accent (header dot) | Match primary component type color |
