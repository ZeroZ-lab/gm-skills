# Gantt Chart — Component Templates

## Task Bar

Uses foreignObject + CSS:

```svg
<g transform="translate(BAR_X, BAR_Y)">
  <foreignObject width="BAR_W" height="BAR_H">
    <div xmlns="http://www.w3.org/1999/xhtml" class="gantt-bar gantt-bar--TYPE" style="width: BAR_Wpx;">
      <span class="gantt-bar-label">Task Label</span>
    </div>
  </foreignObject>
</g>
```

CSS classes:
- `.gantt-bar`: Base bar styling (border-radius, padding, font)
- `.gantt-bar--default`: Default color
- `.gantt-bar--complete`: Completed bar (different opacity/fill)

## Progress Overlay

Partial fill within task bar:

```svg
<rect x="BAR_X" y="BAR_Y" width="PROGRESS_W" height="BAR_H"
      fill="rgba(255,255,255,0.2)" rx="4"/>
```

Where `PROGRESS_W = BAR_W * (progress / 100)`.

## Milestone Diamond

Pure SVG polygon (not foreignObject):

```svg
<g transform="translate(X, Y)">
  <polygon points="0,-7 7,0 0,7 -7,0" fill="ACCENT_COLOR" stroke="BORDER_COLOR" stroke-width="1.5"/>
  <text y="18" text-anchor="middle" font-size="10" fill="TEXT_COLOR">Milestone Label</text>
</g>
```

## Dependency Arrow

SVG path with arrowhead marker:

```svg
<path d="M FROM_X,FROM_Y L MID_X,FROM_Y L MID_X,TO_Y L TO_X,TO_Y"
      fill="none" stroke="ARROW_COLOR" stroke-width="1.5"
      marker-end="url(#arrowhead)"/>
```

Route: horizontal → vertical → horizontal (orthogonal routing).

## Group Header

foreignObject + CSS:

```svg
<g transform="translate(0, GROUP_Y)">
  <foreignObject width="FULL_WIDTH" height="GROUP_H">
    <div xmlns="http://www.w3.org/1999/xhtml" class="gantt-group" style="width: FULL_WIDTHpx;">
      <span class="gantt-group-label">Group Name</span>
    </div>
  </foreignObject>
</g>
```

## Time Axis Label

SVG text:

```svg
<text x="LABEL_X" y="AXIS_Y"
      font-size="10" fill="TEXT_COLOR"
      text-anchor="middle" dominant-baseline="central">
  Week 1
</text>
```

## Time Axis Grid Line

```svg
<line x1="X" y1="GRID_TOP" x2="X" y2="GRID_BOTTOM"
      stroke="GRID_COLOR" stroke-width="0.5" opacity="0.3"/>
```

## Today Marker

```svg
<line x1="TODAY_X" y1="GRID_TOP" x2="TODAY_X" y2="GRID_BOTTOM"
      stroke="ACCENT_COLOR" stroke-width="1.5"
      stroke-dasharray="4 4"/>
<text x="TODAY_X" y="GRID_TOP - 6"
      text-anchor="middle" font-size="9" fill="ACCENT_COLOR">
  Today
</text>
```

## Task Label (left column)

foreignObject + CSS:

```svg
<g transform="translate(0, ROW_Y)">
  <foreignObject width="LABEL_WIDTH" height="ROW_H">
    <div xmlns="http://www.w3.org/1999/xhtml" class="gantt-task-label">
      Task Name
    </div>
  </foreignObject>
</g>
```
