# ER Diagram — CSS+SVG Hybrid Component Templates

## CSS Styles

Include these styles inside the SVG's `<style>` block:

```css
.er-entity {
  border-collapse: collapse;
  width: 100%;
  font-family: system-ui, -apple-system, sans-serif;
  background: var(--entity-bg);
  border: 1.5px solid var(--entity-color);
  border-radius: 6px;
  overflow: hidden;
}
.er-entity .entity-header th {
  background: var(--entity-color);
  color: white;
  font-size: 12px;
  font-weight: 600;
  padding: 6px 12px;
  text-align: left;
  border: none;
}
.er-entity td {
  font-size: 11px;
  padding: 3px 12px;
  border-top: 0.5px solid rgba(255,255,255,0.1);
  vertical-align: middle;
  height: 22px;
}
.er-entity .attr-name {
  color: var(--text-color);
  text-align: left;
  white-space: nowrap;
}
.er-entity .attr-name.pk {
  color: var(--accent-color);
  text-decoration: underline;
  font-weight: 600;
}
.er-entity .attr-name.fk {
  color: var(--text-color);
  font-style: italic;
}
.er-entity .attr-type {
  color: var(--muted-color);
  font-size: 10px;
  text-align: left;
  white-space: nowrap;
}
.er-entity .attr-badge,
.er-entity .attr-constraint {
  font-size: 9px;
  text-align: right;
  white-space: nowrap;
}
.er-entity .pk-badge {
  display: inline-block;
  background: rgba(251,191,36,0.2);
  color: #fbbf24;
  border: 0.5px solid #fbbf24;
  border-radius: 2px;
  padding: 1px 4px;
  font-size: 7px;
  font-weight: 600;
  line-height: 1;
}
.er-entity .fk-badge {
  display: inline-block;
  background: rgba(167,139,250,0.2);
  color: #a78bfa;
  border: 0.5px solid #a78bfa;
  border-radius: 2px;
  padding: 1px 4px;
  font-size: 7px;
  font-weight: 600;
  line-height: 1;
}
```

## Entity Table (foreignObject + HTML)

Each entity renders as an HTML table inside `<foreignObject>`, wrapped in an SVG `<g>` for positioning:

```svg
<g transform="translate(X, Y)">
  <foreignObject width="W" height="H">
    <table xmlns="http://www.w3.org/1999/xhtml" class="er-entity" style="--entity-bg:#0f172a; --entity-color:[entity-color]; --text-color:#e2e8f0; --muted-color:#64748b; --accent-color:#fbbf24;">
      <tr class="entity-header"><th colspan="3">Entity Name</th></tr>
      <!-- attribute rows go here -->
    </table>
  </foreignObject>
</g>
```

### Attribute Rows

Normal attribute:
```html
<tr><td class="attr-name">email</td><td class="attr-type">string</td><td class="attr-constraint">NN</td></tr>
```

Primary Key attribute:
```html
<tr><td class="attr-name pk">id</td><td class="attr-type">int</td><td class="attr-badge"><span class="pk-badge">PK</span></td></tr>
```

Foreign Key attribute:
```html
<tr><td class="attr-name fk">user_id</td><td class="attr-type">int</td><td class="attr-badge"><span class="fk-badge">FK</span></td></tr>
```

### Full Entity Example

```svg
<g transform="translate(X, Y)">
  <foreignObject width="200" height="118">
    <table xmlns="http://www.w3.org/1999/xhtml" class="er-entity" style="--entity-bg:#0f172a; --entity-color:#3b82f6; --text-color:#e2e8f0; --muted-color:#64748b; --accent-color:#fbbf24;">
      <tr class="entity-header"><th colspan="3">User</th></tr>
      <tr><td class="attr-name pk">id</td><td class="attr-type">int</td><td class="attr-badge"><span class="pk-badge">PK</span></td></tr>
      <tr><td class="attr-name">email</td><td class="attr-type">string</td><td class="attr-constraint">NN</td></tr>
      <tr><td class="attr-name">name</td><td class="attr-type">string</td><td class="attr-constraint"></td></tr>
      <tr><td class="attr-name">created_at</td><td class="attr-type">datetime</td><td class="attr-constraint"></td></tr>
    </table>
  </foreignObject>
</g>
```

## Relationship Lines (SVG only)

Relationship lines remain pure SVG elements placed in the same SVG canvas, rendered **after** all entity groups so they appear on top.

### Solid (identifying relationship)

```svg
<line x1="fromX" y1="fromY" x2="toX" y2="toY" stroke="#64748b" stroke-width="1.5" marker-end="url(#er-arrow)"/>
```

### Dashed (non-identifying relationship)

```svg
<line x1="fromX" y1="fromY" x2="toX" y2="toY" stroke="#64748b" stroke-width="1.5" stroke-dasharray="6,4" marker-end="url(#er-arrow)"/>
```

### With bend point

```svg
<path d="M fromX,fromY L bendX,fromY L bendX,toY L toX,toY" fill="none" stroke="#64748b" stroke-width="1.5" marker-end="url(#er-arrow)"/>
```

## Cardinality Labels (SVG)

```svg
<!-- From cardinality (near source) -->
<rect x="fromLabelX-12" y="fromLabelY-8" width="24" height="16" rx="3" fill="[bg-color]" opacity="0.9"/>
<text x="fromLabelX" y="fromLabelY+4" font-size="10" fill="[accent-color]" text-anchor="middle" font-weight="600">1</text>

<!-- To cardinality (near target) -->
<rect x="toLabelX-12" y="toLabelY-8" width="24" height="16" rx="3" fill="[bg-color]" opacity="0.9"/>
<text x="toLabelX" y="toLabelY+4" font-size="10" fill="[accent-color]" text-anchor="middle" font-weight="600">N</text>
```

## Relationship Label (optional, SVG)

```svg
<rect x="midX-labelLen*3" y="midY-8" width="labelLen*6" height="16" rx="3" fill="[bg-color]" opacity="0.9"/>
<text x="midX" y="midY+4" font-size="9" fill="#94a3b8" text-anchor="middle">has many</text>
```

## Color Mapping

| Component | CSS Var / Dark Value | Light Value |
|-----------|---------------------|-------------|
| Entity background | `--entity-bg: #0f172a` | `#ffffff` |
| Entity border | `--entity-color: [type-color]` | `[type-color]` |
| Entity header bg | `--entity-color` (same) | `[type-color]` |
| Text color | `--text-color: #e2e8f0` | `#1e293b` |
| Muted color | `--muted-color: #64748b` | `#94a3b8` |
| Accent color (PK) | `--accent-color: #fbbf24` | `#b45309` |
| PK badge bg | `rgba(251,191,36,0.2)` | `rgba(180,83,9,0.1)` |
| PK badge stroke/text | `#fbbf24` | `#b45309` |
| FK badge bg | `rgba(167,139,250,0.2)` | `rgba(126,34,206,0.1)` |
| FK badge stroke/text | `#a78bfa` | `#7e22ce` |
| Relationship line | `#64748b` | `#94a3b8` |
| Cardinality text | `#94a3b8` | `#475569` |

## Arrow Markers

```svg
<defs>
  <marker id="er-arrow" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
    <polygon points="0 0, 8 3, 0 6" fill="#64748b"/>
  </marker>
</defs>
```
