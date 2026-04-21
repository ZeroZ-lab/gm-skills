# Hand-Drawn Sketch Style Reference

## Design Philosophy

**Approachable, informal, human.** The output should look like someone drew it on a whiteboard during a brainstorming session — bold strokes, slightly imperfect, warm and inviting. Precision is less important than clarity and friendliness.

## Prohibited (Do NOT)

- NO thin 1px lines — all strokes must be bold (2px+)
- NO dark backgrounds — light/white canvas only
- NO pixel-perfect alignment — slight variation adds charm
- NO neon or overly saturated colors — soft pastels and muted tones only
- NO complex SVG paths with many points — keep shapes simple
- NO JavaScript — static HTML/CSS/SVG only
- NO glow or blur effects — solid, hand-drawn aesthetic

This style produces light-themed, sketch-like architecture diagrams with a casual, whiteboard feel.

## Template File

Use `assets/template-sketch.html` as the starting point.

## Key Visual Differences from Dark Style

| Property | Dark Professional | Hand-Drawn Sketch |
|----------|------------------|-------------------|
| Background | `#020617` (near-black) | `#faf9f6` (warm white) |
| Card bg | `#0f172a` (dark) | `white` |
| Font | JetBrains Mono (monospace) | Segoe UI (sans-serif) |
| Border width | 1-1.5px, precise | 2-2.5px, bold |
| Colors | Neon/glowing (cyan, emerald) | Pastel/muted (blue, green) |
| Connection lines | Thin, precise | Thick, rounded caps |
| Component fills | Semi-transparent dark | Pastel tints |
| Shadow | None | Box shadow (2-3px offset) |

## Color Mapping

| Type | Fill | Stroke | Layer bg |
|------|------|--------|----------|
| `process` | `white` | `#27ae60` | `#eafaf1` |
| `module` | `white` | `#3498db` | `#ebf5fb` |
| `data` | `white` | `#8e44ad` | `#f5eef8` |
| `infra` | `white` | `#f39c12` | `#fef9e7` |
| `security` | `white` | `#e74c3c` | `#fdedec` (dashed border) |
| `channel` | `white` | `#e67e22` | `#fdf2e9` |
| `external` | `white` | `#95a5a6` | `#f2f3f4` |

## Hand-Drawn Effect Techniques (No JavaScript)

### 1. Bold borders with rounded caps
```svg
stroke-width="2.5" stroke-linecap="round"
```

### 2. Security components use dashed borders
```svg
stroke-dasharray="6,3"
```
This gives a "rough sketch" feel to security boundaries.

### 3. Layer cards with pastel fill
```svg
<rect ... fill="#eafaf1" stroke="#27ae60" stroke-width="2.5"/>
```

### 4. Modules are white boxes inside colored layers
```svg
<rect ... fill="white" stroke="#27ae60" stroke-width="2"/>
```

### 5. Box shadow via CSS
The `.diagram-container` and `.card` elements use CSS box-shadow instead of SVG effects:
```css
box-shadow: 3px 3px 0px rgba(0,0,0,0.1);
```

### 6. Connection lines with thick strokes
```svg
<path d="..." stroke="#2c3e50" stroke-width="2.5" fill="none"
      marker-end="url(#arrowhead-sketch)" stroke-linecap="round"/>
```

### 7. Connection labels with white background
```svg
<rect x="..." y="..." width="..." height="18" rx="2" fill="white"/>
<text ... font-weight="600">REST</text>
```

## Arrow Markers

Use different marker IDs than the dark style (both can't coexist on one page):
```svg
<marker id="arrowhead-sketch" ...>
<marker id="arrowhead-sketch-rev" ...>
```

## Typography

- Labels: 13-15px, `font-weight: 600-700`, `#2c3e50`
- Annotations: 10px, `#7f8c8d`
- Tech badges: 8px, matching stroke color
- Connection labels: 10px, `font-weight: 600`, `#2c3e50`

## Layout Rules

Same coordinate calculation as `references/layout-rules.md`, with these **CRITICAL adjustments** for hand-drawn style:

| Constant | Dark Professional | Hand-Drawn Sketch |
|----------|------------------|-------------------|
| `LAYER_GAP` | 50px | 50px (same) |
| `MODULE_GAP` | 20px | 20px (same) |
| `LAYER_H_SIMPLE` | **101px** | **110px** |
| `LAYER_H_BADGE` | **116px** | **130px** |
| `LAYER_H_EMPTY` | **60px** | **70px** |
| Module border | 1.5px | 2px thick |
| Layer border | 1px | 2.5px thick |

**Why taller layers?** Hand-drawn style uses bolder borders (2-2.5px vs 1-1.5px) and requires more internal padding for the "whiteboard" aesthetic. The extra height prevents module content from touching layer boundaries.

### Height Selection Guide

| Condition | Use Height |
|-----------|------------|
| Layer has modules WITH `tech` badges (3+ badges) | **130px** (`LAYER_H_BADGE`) |
| Layer has modules with 1-2 badges | **130px** (badges need room) |
| Layer has modules WITHOUT badges | **110px** (`LAYER_H_SIMPLE`) |
| Layer has NO children (label only) | **70px** (`LAYER_H_EMPTY`) |

**Common mistake:** Using 101px/116px (dark style values) for hand-drawn causes badges to overflow. Always use the taller hand-drawn values.

## Summary Cards

- White background with 2px solid border
- Box shadow: `2px 2px 0px rgba(0,0,0,0.08)`
- Dot colors: blue, green, orange (not neon)
- Text: dark gray on white

## Page Structure

Same as dark style: Header → SVG Diagram → Summary Cards → Footer.

Differences:
- Header uses a solid dot instead of pulsing animation
- Footer border is dashed
- Card shadows are subtle
