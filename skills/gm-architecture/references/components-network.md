# Network Topology — Component Templates

## Node Component

foreignObject + CSS (icon + label + optional IP):

```svg
<g transform="translate(NODE_X, NODE_Y)">
  <!-- Icon area -->
  <foreignObject width="NODE_W" height="NODE_H">
    <div xmlns="http://www.w3.org/1999/xhtml" class="net-node net-node--TYPE">
      <div class="net-icon"><!-- SVG icon --></div>
      <div class="net-label">Server Name</div>
      <div class="net-ip">10.0.0.1</div>
    </div>
  </foreignObject>
</g>
```

CSS classes:
- `.net-node`: Base node styling (center-aligned, border-radius, padding)
- `.net-node--server`, `.net-node--router`, etc.: Type-specific colors
- `.net-icon`: Icon container, centered
- `.net-label`: Bold, centered
- `.net-ip`: Smaller font, muted color, centered

Node type color mapping (dark style example):
| Type | Fill | Border |
|------|------|--------|
| server | `rgba(8,51,68,0.4)` | `#22d3ee` |
| router | `rgba(120,53,15,0.3)` | `#fbbf24` |
| switch | `rgba(6,78,59,0.4)` | `#34d399` |
| firewall | `rgba(136,19,55,0.4)` | `#fb7185` |
| load-balancer | `rgba(76,29,149,0.4)` | `#a78bfa` |
| database | `rgba(76,29,149,0.4)` | `#a78bfa` |
| cloud | `rgba(30,41,59,0.5)` | `#94a3b8` |
| client | `rgba(30,41,59,0.3)` | `#64748b` |

## Zone Background

SVG rect:

```svg
<rect x="ZONE_X" y="ZONE_Y" width="ZONE_W" height="ZONE_H"
      rx="8" fill="rgba(255,255,255,0.03)"
      stroke="rgba(255,255,255,0.08)" stroke-width="1" stroke-dasharray="6 3"/>
<text x="ZONE_X + 12" y="ZONE_Y + 16"
      font-size="11" fill="MUTED_COLOR" font-weight="600">
  Zone Label
</text>
```

## Connection Line

SVG line or path, type-specific styling:

```svg
<line x1="FROM_X" y1="FROM_Y" x2="TO_X" y2="TO_Y"
      stroke="LINE_COLOR" stroke-width="LINE_WIDTH"
      STYLE_ATTRIBUTE/>
```

### Connection type styles

| Type | Stroke style | Width |
|------|-------------|-------|
| ethernet | solid | `1.5px` |
| fiber | solid | `2px` |
| wireless | `stroke-dasharray="6 4"` | `1.5px` |
| vpn | `stroke-dasharray="4 4"` | `1.5px` |
| tunnel | `stroke-dasharray="2 4"` | `1.5px` |
| wan | solid | `2.5px` |
| lan | solid | `1px` |

## Bandwidth Label

Small text at midpoint of connection:

```svg
<rect x="MID_X - LABEL_W/2" y="MID_Y - 8" width="LABEL_W" height="16" rx="3"
      fill="BG_COLOR" opacity="0.9"/>
<text x="MID_X" y="MID_Y"
      font-size="9" fill="MUTED_COLOR"
      text-anchor="middle" dominant-baseline="central">
  1Gbps
</text>
```

## Redundant Connection

Two parallel lines offset by ±3px:

```svg
<line x1="FROM_X" y1="FROM_Y - 3" x2="TO_X" y2="TO_Y - 3" .../>
<line x1="FROM_X" y1="FROM_Y + 3" x2="TO_X" y2="TO_Y + 3" .../>
```
