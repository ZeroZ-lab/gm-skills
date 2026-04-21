# SVG Component Templates

Copy and adapt these SVG+HTML snippets when generating diagram output. All component boxes use `<foreignObject>` with CSS flexbox for layout — **no manual coordinate math needed for text centering or module spacing**.

**CRITICAL**: Every `<foreignObject>` MUST include `xmlns="http://www.w3.org/1999/xhtml"` on the root HTML element. CSS classes are defined in each template's `<style>` block.

## 1. Layer Card with Modules (CSS Layout)

```svg
<!-- Layer: Browser Process at y=40, type=process -->
<!-- Only translate-y needs computing. Width is always 920 (SVG_W - 2*PAGE_MARGIN) -->
<!-- Layer height: 101 for simple modules, 116 for modules with tech badges -->
<g transform="translate(40, 40)">
  <!-- Masking rect: covers arrows behind this layer -->
  <rect width="920" height="101" rx="8" fill="#0f172a"/>
  <!-- foreignObject with CSS layout -->
  <foreignObject width="920" height="101">
    <div xmlns="http://www.w3.org/1999/xhtml" class="layer-card type-process">
      <div class="layer-label">Browser Process</div>
      <div class="modules">
        <div class="module type-module"><span class="module-label">UI / Tabs</span></div>
        <div class="module type-module"><span class="module-label">Network</span></div>
        <div class="module type-data"><span class="module-label">Storage</span></div>
      </div>
    </div>
  </foreignObject>
</g>
```

## 2. Layer Card with Modules + Tech Badges

```svg
<!-- Layer with tech badges — height=116 (taller to fit badge row) -->
<g transform="translate(40, 191)">
  <rect width="920" height="116" rx="8" fill="#0f172a"/>
  <foreignObject width="920" height="116">
    <div xmlns="http://www.w3.org/1999/xhtml" class="layer-card type-process">
      <div class="layer-label">Renderer Process</div>
      <div class="modules">
        <div class="module has-badges type-module">
          <span class="module-label">Blink</span>
          <span class="tech-badges"><span class="tech-badge">Render Engine</span></span>
        </div>
        <div class="module has-badges type-module">
          <span class="module-label">V8 Engine</span>
          <span class="tech-badges"><span class="tech-badge">JavaScript</span></span>
        </div>
        <div class="module type-module"><span class="module-label">DOM / CSS</span></div>
      </div>
    </div>
  </foreignObject>
</g>
```

## 3. Data Store Layer (Cylinder Hint)

```svg
<!-- Data store: PostgreSQL, type=data, height=101 -->
<g transform="translate(40, 350)">
  <rect width="920" height="101" rx="8" fill="#0f172a"/>
  <foreignObject width="920" height="101">
    <div xmlns="http://www.w3.org/1999/xhtml" class="layer-card type-data">
      <div class="layer-label">Database</div>
      <div class="modules">
        <div class="module type-data"><span class="module-label">PostgreSQL</span></div>
      </div>
    </div>
  </foreignObject>
</g>
```

## 4. Connection: Unidirectional Arrow (SVG only — no CSS)

Arrows remain pure SVG. Compute endpoints from layer y-positions:

```svg
<!-- Arrow from Layer 1 bottom-center to Layer 2 top-center -->
<!-- y1 = layer1_y + layer1_h, y2 = layer2_y -->
<line x1="500" y1="141" x2="500" y2="191"
      stroke="#fb923c" stroke-width="1.5"
      marker-end="url(#arrowhead-orange)"/>
<!-- Connection label at midpoint -->
<g transform="translate(500, 166)">
  <rect x="-18" y="-9" width="36" height="18" rx="3" fill="#020617" opacity="0.9"/>
  <text x="0" y="0" font-size="10" fill="#fb923c"
        font-family="JetBrains Mono, monospace"
        text-anchor="middle" dominant-baseline="central">IPC</text>
</g>
```

**Connection endpoint rules:**
- Vertical (down): `x = SVG_W/2 = 500`, `y1 = source_layer_y + source_layer_h`, `y2 = target_layer_y`
- Offset vertical: use source/target module center x (estimate: `SVG_W/2` if single module, offset if multiple)
- Diagonal: route with bend points to avoid crossing intermediate layers

## 5. Connection: Bidirectional Arrow

```svg
<line x1="500" y1="141" x2="500" y2="191"
      stroke="#fb923c" stroke-width="1.5"
      marker-start="url(#arrowhead-orange-rev)" marker-end="url(#arrowhead-orange)"/>
```

## 6. Connection: Dashed Line

```svg
<line x1="300" y1="141" x2="350" y2="357"
      stroke="#64748b" stroke-width="1.5" stroke-dasharray="6,4"
      marker-end="url(#arrowhead)"/>
```

## 7. Connection Routed Around Layers (Avoid Overlap)

When a connection must skip layers (e.g., Browser→GPU skipping Renderer), route the line along the LEFT or RIGHT edge:

```svg
<!-- Routed connection: goes along left edge to avoid crossing Layer 2 -->
<path d="M 60,141 L 20,141 L 20,357 L 60,357"
      fill="none" stroke="#64748b" stroke-width="1.5" stroke-dasharray="6,4"
      marker-end="url(#arrowhead)"/>
```

**Routing rules:**
- Left edge route: `x = PAGE_MARGIN - 20 = 20`
- Right edge route: `x = SVG_W - PAGE_MARGIN + 20 = 980`
- NEVER draw diagonal lines through intermediate layers

## 8. Security Group Boundary

```svg
<rect x="60" y="170" width="400" height="120" rx="8"
      fill="none" stroke="#fb7185" stroke-width="1.5" stroke-dasharray="6,4"/>
<text x="75" y="188" font-size="11" fill="#fb7185"
      font-family="JetBrains Mono, monospace"
      text-anchor="start" dominant-baseline="central">Security Group</text>
```

## 9. Region Boundary

```svg
<rect x="30" y="30" width="940" height="400" rx="12"
      fill="none" stroke="#fbbf24" stroke-width="1.5" stroke-dasharray="8,4"/>
<text x="48" y="50" font-size="11" fill="#fbbf24"
      font-family="JetBrains Mono, monospace"
      text-anchor="start" dominant-baseline="central">AWS Region: us-east-1</text>
```

## 10. Legend (CSS Layout)

```svg
<!-- Legend below all layers -->
<g transform="translate(40, 600)">
  <foreignObject width="920" height="40">
    <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: 'JetBrains Mono', monospace;">
      <div style="font-size:11px; font-weight:600; color:#cbd5e1; margin-bottom:8px;">Legend</div>
      <div class="legend-container">
        <div class="legend-item">
          <div class="legend-swatch type-process"></div>
          <span class="legend-text">Process</span>
        </div>
        <div class="legend-item">
          <div class="legend-swatch type-module"></div>
          <span class="legend-text">Module</span>
        </div>
        <div class="legend-item">
          <div class="legend-swatch type-data"></div>
          <span class="legend-text">Data</span>
        </div>
        <div class="legend-item">
          <div class="legend-swatch type-infra"></div>
          <span class="legend-text">Infra</span>
        </div>
        <div class="legend-item">
          <div class="legend-swatch type-channel"></div>
          <span class="legend-text">IPC Channel</span>
        </div>
      </div>
    </div>
  </foreignObject>
</g>
```

## 11. SVG Defs (Required at start of every SVG)

```svg
<defs>
  <!-- Grid pattern -->
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(51, 65, 85, 0.3)" stroke-width="0.5"/>
  </pattern>
  <!-- Forward arrowhead -->
  <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
    <polygon points="0 0, 8 3, 0 6" fill="#64748b"/>
  </marker>
  <!-- Reverse arrowhead (for bidirectional) -->
  <marker id="arrowhead-rev" markerWidth="8" markerHeight="6" refX="0" refY="3" orient="auto">
    <polygon points="8 0, 0 3, 8 6" fill="#64748b"/>
  </marker>
</defs>
```

## 12. Hand-Drawn Style Layer (using foreignObject)

Hand-drawn sketch style uses taller layer heights (110px/130px vs 101px/116px) due to bolder borders.

```svg
<!-- Layer: Browser Process at y=40, height=130px (has badges) -->
<g transform="translate(40, 40)">
  <foreignObject width="920" height="130">
    <div xmlns="http://www.w3.org/1999/xhtml" class="layer-card type-process">
      <div class="layer-header">
        <span class="layer-label">Browser Process</span>
        <span class="layer-description">Main process - controls UI and coordinates subprocesses</span>
      </div>
      <div class="modules">
        <div class="module type-module">
          <span class="module-label">UI Module</span>
          <span class="tech-badges">
            <span class="tech-badge">Address Bar</span>
            <span class="tech-badge">Tabs</span>
            <span class="tech-badge">Bookmarks</span>
          </span>
        </div>
        <div class="module type-channel">
          <span class="module-label">Network Service</span>
          <span class="tech-badges">
            <span class="tech-badge">HTTP/HTTPS</span>
            <span class="tech-badge">WebSocket</span>
            <span class="tech-badge">QUIC</span>
          </span>
        </div>
      </div>
    </div>
  </foreignObject>
</g>
```

**Key differences from dark-professional:**
- Layer height: **130px** (not 116px) when modules have badges
- Module styling: white background with 2px colored border
- Badges: white background with colored border (not translucent)
- Header: includes optional `.layer-description` for subtitles

## Style-Specific Module CSS

### Dark Professional (template-dark.html)
```css
.module { min-width: 100px; height: 50px; border-radius: 6px; padding: 0 16px; }
.module.has-badges { height: 65px; }
```

### Hand-Drawn Sketch (template-sketch.html)
```css
.module {
  min-width: 100px;
  min-height: 50px;  /* Use min-height, not height */
  border-radius: 6px;
  padding: 10px 16px;
  background: white;
}
/* Layer heights: 110px (simple), 130px (badges), 70px (empty) */
```

**Critical:** Hand-drawn uses `min-height` not fixed `height`, allowing modules to grow if needed. Always use the taller layer heights (110px/130px) for this style.

| Old (SVG absolute) | New (CSS + SVG hybrid) |
|---|---|
| LLM computes `module_x`, `module_w` | CSS `justify-content: center` + `gap: 20px` |
| LLM computes `text_x = w/2`, `text_y = h/2` | CSS `display:flex; align-items:center; justify-content:center` |
| Double rect for every module | Single `<div>` with CSS `background` + `border` |
| Manual spacing with `+20` gaps | CSS `gap: 20px` — guaranteed equal |
| Masking rect needed per module | One masking rect per layer covers all modules |
| Risk of text overflow / overlap | CSS auto-sizes from content |

## Component Type → CSS Class Mapping

| Type | CSS class | Colors (dark-professional) |
|------|-----------|---------------------------|
| `process` | `type-process` | bg: `rgba(8,51,68,0.4)` border: `#22d3ee` |
| `module` | `type-module` | bg: `rgba(6,78,59,0.4)` border: `#34d399` |
| `data` | `type-data` | bg: `rgba(76,29,149,0.4)` border: `#a78bfa` |
| `infra` | `type-infra` | bg: `rgba(120,53,15,0.3)` border: `#fbbf24` |
| `security` | `type-security` | bg: `rgba(136,19,55,0.4)` border: `#fb7185` (dashed) |
| `channel` | `type-channel` | bg: `rgba(251,146,60,0.3)` border: `#fb923c` |
| `external` | `type-external` | bg: `rgba(30,41,59,0.5)` border: `#94a3b8` |
