# Anti-Overlap Checklist

## Node Internal

- Badge has its own row.
- Title has its own row.
- Description has its own row.
- Description is not near the bottom edge.
- Title does not collide with badge.

## Containers

- Nodes do not touch section boundaries.
- Bottom row has section bottom padding.
- Section does not touch note or caption.
- Caption has enough vertical gap.

## Edges

- Edges use anchors, not centers.
- Edges are drawn before nodes.
- Exception and callback routes have their own channels.
- Edge labels use `labelAt` or a label rail.

## Labels

- Labels have white background chips.
- Labels do not sit on arrows.
- Labels do not cover nodes.
- Labels do not follow crowded bends blindly.

## Typography

- Font sizes come from tokens.
- Same-level nodes have identical typography.
- SVG text uses `dominant-baseline` where appropriate.
