# Anti-Overlap Checklist

Use this as the final pre-delivery audit.

## Data And Topology

- The chosen topology matches the user's explanation goal.
- The main reading path is obvious before color or animation.
- `nodes[]` and `edges[]` still describe meaning, not only coordinates.

## Node Internals

- Badge or meta chip owns the meta row.
- Title owns the title row.
- Description owns the desc row.
- Title does not collide with the badge.
- Description does not sit near the bottom edge.

## Containers And Spacing

- Nodes do not touch section boundaries.
- Bottom row leaves `innerBottomPad`.
- Note or caption area leaves `sectionToNoteGap`.
- Main row and secondary row leave `rowGap`.

## Routes

- Routes start from anchors, not node centers.
- `right-left`, `bottom-top`, `left-down`, `outer-right`, and `side-channel` are used consistently.
- Exception and callback edges use their own channels.
- Paths do not cross node text or node interiors.

## Labels

- Labels use white chips.
- Labels sit on a rail or explicit `labelAt`.
- Labels do not cover nodes.
- Labels do not cover arrowheads.
- Labels do not cling to crowded bends.
- Relationship labels are specific enough to stand alone.

## Legend And Notation

- Legend or key exists when color, chip, or route meaning is not obvious.
- Legend does not compete with the primary reading path.
- Legend stays outside the densest node and edge area.

## Typography And Tokens

- Font sizes come from `tokens.font`.
- Edge labels use `tokens.font.edgeLabel`.
- Same-level nodes use consistent typography and spacing.
- SVG text uses `dominant-baseline="middle"` where appropriate.
