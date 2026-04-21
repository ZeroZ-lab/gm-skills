# Sequence Diagram — Layout Rules (CSS+SVG Hybrid)

## Constants

| Constant | Value | Description |
|----------|-------|-------------|
| SVG_W | 1200 | Total SVG width |
| ACTOR_GAP | 150 | Horizontal gap between actors |
| ACTOR_START_X | 120 | Left margin for first actor |
| MSG_START_Y | 100 | First message y position |
| MSG_GAP | 40 | Vertical gap between messages |
| ACTIVATION_W | 12 | Activation box width |
| ACTOR_BOX_H | 36 | Actor box height (participant, boundary, controller) |
| ACTOR_FIGURE_H | 50 | Stick figure total height (head to legs) |
| ACTOR_LABEL_H | 14 | Text label below stick figure |
| ACTOR_TOTAL_H | 64 | Stick figure + label (ACTOR_FIGURE_H + ACTOR_LABEL_H) |
| FRAGMENT_PAD | 15 | Fragment box padding |
| ACTOR_BOX_MIN_W | 80 | Minimum width for actor boxes (CSS min-width) |
| ACTOR_BOX_PAD_X | 12 | Horizontal padding inside actor box (CSS padding) |

## Density Multipliers

Apply these multipliers to the constants above based on the `density` parameter (default: `normal`).

| Constant | compact | normal | spacious |
|----------|---------|--------|----------|
| PAGE_MARGIN | 24px | 40px | 60px |
| ACTOR_GAP | 100px | 150px | 200px |
| MSG_GAP | 28px | 40px | 55px |

## Actor Positioning

```
actor_x[i] = ACTOR_START_X + i * ACTOR_GAP
```

Each actor's horizontal center is `actor_x[i]`. The foreignObject for actor boxes is centered on this x:

```
foreignObject_x = actor_x[i] - (box_rendered_width / 2)
```

Since CSS auto-sizes the box (`min-width: 80px; padding: 0 12px`), the rendered width depends on text length. For layout purposes, assume a nominal width and use the centering approach:

```
foreignObject_y = 20   (for boxes: participant, boundary, controller)
foreignObject_y = 4    (for stick figures: top of head circle)
```

No manual text centering math — CSS `display: flex; align-items: center; justify-content: center` handles it.

## Actor Y Positioning by Type

| Type | Top Y | Total Height | Bottom Y |
|------|-------|-------------|----------|
| Box (participant, boundary, controller) | 20 | 36 | 56 |
| Stick figure (actor) | 4 | 64 | 68 |

Lifeline starts at `actor_bottom_y` (56 for boxes, 68 for stick figures).

## Lifeline Length

```
max_order = max(message.order)
last_message_y = MSG_START_Y + (max_order - 1) * MSG_GAP
lifeline_bottom = last_message_y + 40
```

Each actor gets a dashed vertical line:
```
from (actor_x[i], actor_bottom_y) to (actor_x[i], lifeline_bottom)
```

Where `actor_bottom_y` is 56 for box actors, 68 for stick figure actors.

## Message Y Position

```
message_y[order] = MSG_START_Y + (order - 1) * MSG_GAP
```

## Message Routing

For messages between different actors:
```
from_x = actor_x[from_index]
to_x = actor_x[to_index]
arrow_y = message_y[order]
```

For self-messages (from == to):
```
path = M x,y L x+30,y L x+30,y+20 L x,y+20
```

## Activation Boxes

Track which actors are active during which messages:
```
For each actor, find first and last order where activate=true or involved
activation_top = MSG_START_Y + (first_order - 1) * MSG_GAP
activation_bottom = MSG_START_Y + (last_order - 1) * MSG_GAP
activation_height = activation_bottom - activation_top
activation_x = actor_x[i] - ACTIVATION_W / 2
```

## Fragment Bounds

```
fragment_x = min(actor_x for involved actors) - FRAGMENT_PAD
fragment_y = MSG_START_Y + (min(children) - 1) * MSG_GAP - FRAGMENT_PAD
fragment_w = max(actor_x for involved actors) - fragment_x + FRAGMENT_PAD * 2
fragment_h = (max(children) - min(children) + 1) * MSG_GAP + FRAGMENT_PAD * 2
```

Fragment is rendered as a `<g>` with `transform="translate(fragment_x, fragment_y)"`. The foreignObject inside uses `width="fragment_w"` and `height="fragment_h"`.

For alt with else:
```
else_y = MSG_START_Y + (else_children[0] - 1) * MSG_GAP - 5
else_y_local = else_y - fragment_y   (relative to fragment group)
divider_line: from 0 to fragment_w at else_y_local (within the fragment group)
```

## foreignObject Sizing for Actor Boxes

The foreignObject width should accommodate the auto-sized CSS box. Use a generous fixed width:

```
fo_width = max(ACTOR_BOX_MIN_W + ACTOR_BOX_PAD_X * 2, estimated_label_width + ACTOR_BOX_PAD_X * 2)
fo_height = ACTOR_BOX_H   (always 36px)
```

The CSS `.seq-actor` class uses `min-width: 80px` and `padding: 0 12px`, so the box will auto-size. The foreignObject should be wide enough to contain the rendered box. A safe default:

```
fo_width = 120   (accommodates most labels)
```

Position the foreignObject centered on actor_x:
```
<g transform="translate(actor_x - fo_width/2, 20)">
  <foreignObject width="fo_width" height="36">
    ...
  </foreignObject>
</g>
```

## foreignObject Sizing for Fragments

```
fo_width = fragment_w
fo_height = fragment_h
```

Positioned via `<g transform="translate(fragment_x, fragment_y)">`.

## ViewBox

```
viewBox_w = max(actor_x) + ACTOR_START_X
viewBox_h = lifeline_bottom + 30
```

## Worked Example: Login Flow

4 actors: User (stick), Client (participant), AuthServer (participant), Database (participant)

```
actor_x = [120, 270, 420, 570]
actor_bottom_y = [68, 56, 56, 56]   (User is stick figure, rest are boxes)

max_order = 10
last_message_y = 100 + (10-1) * 40 = 460
lifeline_bottom = 460 + 40 = 500

Messages:
  1. User→Client (y=100)
  2. Client→AuthServer (y=140)
  3. AuthServer→Database (y=180)
  4. Database→AuthServer (y=220, return)
  5. AuthServer→Client (y=260) [alt: valid]
  6. Client→User (y=300) [alt: valid]
  7. AuthServer→Client (y=340) [alt: invalid]
  8. Client→User (y=380) [alt: invalid]

Fragment "alt":
  x = min(120, 270, 420, 570) - 15 = 105
  y = 260 - 15 = 245
  w = 570 - 120 + 30 = 480
  h = (8-5+1) * 40 + 30 = 190

  else_y = 340 - 5 = 335
  else_y_local = 335 - 245 = 90

  Rendered as:
  <g transform="translate(105, 245)">
    <foreignObject width="480" height="190">
      <div class="seq-fragment type-alt"></div>
    </foreignObject>
    <!-- SVG label tab -->
    <path d="M 0,0 L 0,20 L 50,20 L 60,10 L 60,0 Z" .../>
    <text x="8" y="15">alt</text>
    <!-- Else divider (relative coords) -->
    <line x1="0" y1="90" x2="480" y2="90" stroke-dasharray="6,4"/>
    <text x="8" y="104">[else: invalid]</text>
  </g>

Actor boxes rendered as foreignObject (example for Client):
  <g transform="translate(210, 20)">    <!-- 270 - 120/2 = 210 -->
    <foreignObject width="120" height="36">
      <div class="seq-actor type-participant">
        <span class="actor-label">Client</span>
      </div>
    </foreignObject>
  </g>

User (stick figure) rendered as pure SVG at x=120.
```

## Layout Responsibility Split

| Aspect | Handled By | Notes |
|--------|-----------|-------|
| Actor x-position | Layout math | `ACTOR_START_X + i * ACTOR_GAP` |
| Actor box width | CSS | `min-width: 80px; padding: 0 12px` auto-sizes |
| Actor box height | Fixed constant | Always 36px for box actors |
| Text centering in boxes | CSS | `display: flex; align-items: center; justify-content: center` |
| Message y-position | Layout math | `MSG_START_Y + (order-1) * MSG_GAP` |
| Fragment box sizing | Layout math | Calculated from involved actors and message orders |
| Fragment border | CSS | `.seq-fragment` border styling |
| Fragment label | SVG | Pentagon path + text at top-left |
| Lifeline length | Layout math | `last_message_y + 40` |
