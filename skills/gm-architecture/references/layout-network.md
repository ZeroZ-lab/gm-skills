# Network Topology — Layout Rules

## Overall Structure

```
┌──────────── Zone: DMZ ──────────────┐
│                                       │
│  [Firewall] ──── [Load Balancer]     │
│                                       │
└───────────┬──────────────┬───────────┘
            │              │
┌──── Zone: Production ────────────────┐
│         │              │             │
│    [Server 1]    [Server 2]         │
│         │              │             │
│         └──────┬───────┘             │
│                │                     │
│          [(Database)]               │
└─────────────────────────────────────┘
```

## Node Placement

### Grid Layout (default)

Arrange nodes in a logical grid:
- Start with top-tier nodes (firewall, router, load balancer)
- Middle tier: servers, switches
- Bottom tier: databases, storage
- Column spacing: `COL_W = 180px`
- Row spacing: `ROW_H = 120px`

### Zone-Based Layout

When `zones[]` is provided:
- Each zone gets a rounded rectangle background
- Zone padding: `20px`
- Zone gap: `30px`
- Nodes within a zone are arranged in a sub-grid
- Zone label at top-left corner

## Node Sizing

- Node width: `120px` (or wider based on label)
- Node height: `70px` (icon + label + optional IP)
- Minimum gap between nodes: `60px`

## Connection Routing

- Default: straight line from center of source to center of target
- For crossing connections: use slight curve (`<path>` with control points)
- Redundant connections: offset by `4px` in parallel

## Zone Backgrounds

```svg
<rect x="ZONE_X" y="ZONE_Y" width="ZONE_W" height="ZONE_H"
      rx="8" fill="ZONE_FILL" stroke="ZONE_STROKE" stroke-width="1" opacity="0.5"/>
<text x="ZONE_X + 12" y="ZONE_Y + 16" font-size="11" fill="ZONE_LABEL_COLOR">
  Zone Name
</text>
```

## Density Multipliers

| Property | Compact | Normal | Spacious |
|----------|---------|--------|----------|
| COL_W | 140px | 180px | 220px |
| ROW_H | 90px | 120px | 160px |
| Node width | 100px | 120px | 140px |
| Node height | 60px | 70px | 80px |
| Min gap | 40px | 60px | 80px |
| Zone padding | 14px | 20px | 28px |

## ViewBox

- Width: `max(node_x) + node_width + zone_padding + 40`
- Height: `max(node_y) + node_height + zone_padding + 40`
