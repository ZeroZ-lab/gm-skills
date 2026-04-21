# Gantt Chart — Layout Rules

## Overall Structure

```
┌─────────────────────────────────────────────────┐
│  Title + Subtitle                                │
├──────┬──────────────────────────────────────────┤
│ Task │  Week 1  Week 2  Week 3  Week 4  Week 5 │
│ Name │  │   │    │   │   │   │   │   │   │   │  │
├──────┼──────────────────────────────────────────┤
│Task A│ ████████████                              │
│Task B│          ████████████████                 │
│Task C│               ◆                          │
│Task D│                    ██████████████         │
├──────┼──────────────────────────────────────────┤
│      │  │   │    │   │   │   │   │   │   │  │  │
└──────┴──────────────────────────────────────────┘
```

## Coordinate System

### Time Axis

- Position: top of chart area, horizontal
- Each unit (day/week/month) gets equal width
- Unit width: `UNIT_W = (CHART_WIDTH - LABEL_WIDTH) / num_units`
- Label width: `LABEL_WIDTH = 140px`
- Chart area starts at `x = LABEL_WIDTH`

### Task Rows

- Row height: `ROW_H = 36px` (normal density)
- Task label column: left side, `LABEL_WIDTH` wide
- Bar area: right of labels
- Row gap: `ROW_GAP = 4px`

### Bar Positioning

- Bar x = `LABEL_WIDTH + (start_offset * UNIT_W)`
- Bar width = `duration * UNIT_W`
- Bar y = `row_index * (ROW_H + ROW_GAP) + ROW_H/2 - BAR_H/2`
- Bar height: `BAR_H = 24px` (normal density)

### Milestones

- Diamond marker at exact time position
- Size: `12x12px`
- Center at `(x, row_center_y)`
- Rotated 45° square

### Group Headers

- Subtle background band spanning full width
- Label in bold, left-aligned
- Padding: `8px` vertical

### Today Line

- Vertical dashed line at current date/position
- Color: style-specific accent
- Stroke: `stroke-dasharray="4 4"`

### Dependencies

- Arrows from end of predecessor bar to start of successor bar
- SVG `<path>` with marker arrowhead
- Route: horizontal → vertical → horizontal (orthogonal)

## Density Multipliers

| Property | Compact | Normal | Spacious |
|----------|---------|--------|----------|
| ROW_H | 28px | 36px | 48px |
| BAR_H | 18px | 24px | 32px |
| ROW_GAP | 2px | 4px | 8px |
| Label width | 120px | 140px | 160px |
| Font size | 10px | 12px | 14px |

## ViewBox

- Width: `max(LABEL_WIDTH + num_units * UNIT_W + 40, 800)`
- Height: `HEADER_H + num_tasks * (ROW_H + ROW_GAP) + LEGEND_H + 40`
- `HEADER_H = 60px`, `LEGEND_H = 40px`
