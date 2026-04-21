# Mind Map Layout Rules

These rules compute SVG coordinates from the JSON schema. Follow them to position all elements deterministically -- do NOT guess coordinates.

Node boxes use `<foreignObject>` + CSS (see `components-mindmap.md`), so text centering and box styling are handled by CSS. This file focuses on x/y positions and Bezier curve paths.

## Constants

| Name | Value | Purpose |
|------|-------|---------|
| `SVG_W` | 1200px | SVG viewBox width (fixed) |
| `SVG_H` | 800px | SVG viewBox height (starting value, auto-adjusted) |
| `CENTRAL_W` | 120px | Central node width (fixed, CSS pill) |
| `CENTRAL_H` | 50px | Central node height (fixed, CSS pill) |
| `BRANCH_NODE_H` | 32px | Branch node height (fixed, CSS handles layout) |
| `LEAF_NODE_H` | 28px | Leaf node height (fixed, CSS handles layout) |
| `BRANCH_H_GAP` | 120px | Horizontal distance between branch levels |
| `BRANCH_V_GAP` | 30px | Vertical gap between sibling branches |
| `CHAR_W` | 8px | Approximate character width for estimating node width |
| `NODE_PAD` | 24px | Total horizontal padding inside nodes (12px each side) |
| `PAGE_MARGIN` | 40px | Minimum space between content and SVG edge |

## Density Multipliers

Apply these multipliers to the constants above based on the `density` parameter (default: `normal`).

| Constant | compact | normal | spacious |
|----------|---------|--------|----------|
| PAGE_MARGIN | 24px | 40px | 60px |
| BRANCH_H_GAP | 80px | 120px | 160px |
| BRANCH_V_GAP | 20px | 30px | 40px |

## Step 1: Determine Central Node Position

```
center_x = SVG_W / 2   // = 600
center_y = SVG_H / 2   // = 400 (initial; adjusted after Step 3)
```

The central node `<foreignObject>` is placed at:
```
central_translate_x = center_x - CENTRAL_W / 2   // = 540
central_translate_y = center_y - CENTRAL_H / 2   // = 375
```

## Step 2: Assign Sides to Top-Level Branches

For each top-level branch (direct child of `centralNode`):

1. If `side` is `"left"` or `"right"` -- use that value.
2. If `side` is `"auto"` or not set -- distribute evenly:
   - Split branches into two groups: first half goes right, second half goes left.
   - If odd number: the extra branch goes to the side with less total subtree height (computed in Step 3).

All descendants of a top-level branch inherit their ancestor's side.

## Step 3: Compute Subtree Heights (Recursive)

For each branch, calculate the total vertical space its subtree occupies. Use the node height constant based on level: `BRANCH_NODE_H` (32) for level-1 branches, `LEAF_NODE_H` (28) for level 2+.

```
function subtreeHeight(branch, level):
    node_h = BRANCH_NODE_H if level == 1 else LEAF_NODE_H
    if branch has no children:
        return node_h
    children_total = sum(subtreeHeight(child, level+1) for each child)
                      + BRANCH_V_GAP * (num_children - 1)
    return max(node_h, children_total)
```

The total height of the mind map (both sides combined):

```
right_height = sum(subtreeHeight(b, 1) for right-side branches) + BRANCH_V_GAP * (num_right - 1)
left_height  = sum(subtreeHeight(b, 1) for left-side branches)  + BRANCH_V_GAP * (num_left - 1)
total_height = max(right_height, left_height) + CENTRAL_H + PAGE_MARGIN * 2
```

Adjust `center_y` and `SVG_H`:

```
SVG_H = total_height
center_y = SVG_H / 2
```

## Step 4: Estimate Node Widths

Node widths are estimates used for positioning. CSS auto-sizes the actual rendered box inside the `<foreignObject>`.

```
function nodeWidth(branch, level):
    if level == 0:
        return CENTRAL_W        // 120px fixed
    label_length = length of branch.label in characters
    min_w = 60 if level == 1 else 50
    return max(min_w, label_length * CHAR_W + NODE_PAD)
```

Cap width at 200px; if label exceeds that, CSS `text-overflow: ellipsis` will truncate.

## Step 5: Compute Branch X Positions

For each level of depth (1-indexed, where level 1 = top-level branches):

```
// Right-side branches
branch_x = center_x + CENTRAL_W / 2 + BRANCH_H_GAP * level

// Left-side branches
branch_x = center_x - CENTRAL_W / 2 - BRANCH_H_GAP * level - node_width
```

Where `node_width` is the estimated width from Step 4.

## Step 6: Compute Branch Y Positions (Vertical Centering)

For each group of sibling branches, center them vertically relative to their parent:

```
function layoutChildren(children, parent_y, parent_subtree_h, level):
    node_h = BRANCH_NODE_H if level == 1 else LEAF_NODE_H
    total_h = sum(subtreeHeight(child, level)) + BRANCH_V_GAP * (num_children - 1)
    start_y = parent_y + (parent_subtree_h - total_h) / 2

    current_y = start_y
    for each child:
        child_y = current_y + (subtreeHeight(child, level) - node_h) / 2
        // child_y is the top of the foreignObject box
        layoutChildren(child.children, current_y, subtreeHeight(child), level+1)
        current_y += subtreeHeight(child, level) + BRANCH_V_GAP
```

For top-level branches, the parent is the central node at `center_y`:

```
// Right side
layoutChildren(right_branches, center_y - subtree_h/2, total_right_subtree_h, 1)

// Left side
layoutChildren(left_branches, center_y - subtree_h/2, total_left_subtree_h, 1)
```

## Step 7: Compute Connection Paths (Cubic Bezier)

For each parent-child pair, draw a cubic bezier `<path>` from the parent's edge to the child's edge. Connections are pure SVG -- no CSS classes needed.

### Node edge helpers

```
// Right edge center of a node
function rightEdgeCX(node_x, node_w, node_y, node_h):
    return (node_x + node_w, node_y + node_h / 2)

// Left edge center of a node
function leftEdgeCX(node_x, node_w, node_y, node_h):
    return (node_x, node_y + node_h / 2)
```

For the central node specifically:
```
central_right = (center_x + CENTRAL_W / 2, center_y)   // (660, center_y)
central_left  = (center_x - CENTRAL_W / 2, center_y)   // (540, center_y)
```

### Right-side connections

Parent is to the left of the child:
```
x1, y1 = rightEdgeCX of parent     // (parent_x + parent_w, parent_y + parent_h/2)
x2, y2 = leftEdgeCX of child       // (child_x, child_y + child_h/2)

path = "M x1,y1 C (x1+40),y1 (x2-40),y2 x2,y2"
```

### Left-side connections

Parent is to the right of the child:
```
x1, y1 = leftEdgeCX of parent      // (parent_x, parent_y + parent_h/2)
x2, y2 = rightEdgeCX of child      // (child_x + child_w, child_y + child_h/2)

path = "M x1,y1 C (x1-40),y1 (x2+40),y2 x2,y2"
```

The control point offset of 40px creates a smooth S-curve. Adjust proportionally if `BRANCH_H_GAP` differs from default.

## Step 8: Compute ViewBox

Auto-calculate the viewBox to fit all branches with margin:

```
// Find extremes
min_x = min of all node left edges - PAGE_MARGIN
max_x = max of all node right edges + PAGE_MARGIN
min_y = min of all node top edges - PAGE_MARGIN
max_y = max of all node bottom edges + PAGE_MARGIN

// Include central node
min_x = min(min_x, center_x - CENTRAL_W/2 - PAGE_MARGIN)
max_x = max(max_x, center_x + CENTRAL_W/2 + PAGE_MARGIN)

viewBox = "min_x min_y (max_x - min_x) (max_y - min_y)"
```

If all content fits within `SVG_W x SVG_H`, use the simpler default:
```
viewBox = "0 0 SVG_W SVG_H"
```

## Step 9: Assemble SVG

Nodes and connections are emitted in this order:

1. **`<defs>`** -- grid pattern, glow filter
2. **`<style>`** -- all CSS classes from `components-mindmap.md`
3. **Background** -- `<rect>` fill + optional grid `<rect fill="url(#grid)"/>`
4. **Connections** -- all `<path>` elements (drawn first so nodes appear on top)
5. **Central node** -- `<g transform="translate(...)"><foreignObject>...</foreignObject></g>`
6. **Branch/leaf nodes** -- `<g transform="translate(...)"><foreignObject>...</foreignObject></g>` for each
7. **Legend** (optional) -- `<foreignObject>` legend

## Worked Example: Product Feature Map

### Input

- Central node: "gmdiagram" (id: "root")
- 4 top-level branches (all `side: "auto"`):
  - **Diagram Types** (5 children): Architecture, Mind Map, Flowchart, Sequence, ER Diagram
  - **Visual Styles** (6 children): Dark Pro, Hand-Drawn, Light Corp, Cyberpunk, Blueprint, Warm Cozy
  - **Output Formats** (4 children): HTML, SVG, PNG, PDF
  - **Icon System** (3 children): DevIcons, Simple Icons, Custom SVG

### Side Assignment (auto-balanced)

4 branches, split evenly:
- **Right side**: Diagram Types, Visual Styles (first 2)
- **Left side**: Output Formats, Icon System (last 2)

### Node Width Estimates

```
CENTRAL_W = 120 (fixed)

// Level 1 branches
"Diagram Types"  -> max(60, 13*8 + 24) = 128
"Visual Styles"  -> max(60, 12*8 + 24) = 120
"Output Formats" -> max(60, 13*8 + 24) = 128
"Icon System"    -> max(60, 11*8 + 24) = 112

// Level 2 leaves (min 50)
"Architecture" -> max(50, 12*8 + 24) = 120
"Mind Map"     -> max(50, 8*8 + 24)  = 88
"Flowchart"    -> max(50, 9*8 + 24)  = 96
"Sequence"     -> max(50, 8*8 + 24)  = 88
"ER Diagram"   -> max(50, 10*8 + 24) = 104
... etc
```

### Subtree Height Calculation

```
// Leaf nodes: height = LEAF_NODE_H = 28

// Diagram Types: 5 children (level 2)
subtreeHeight("diagram-types", 1) = 28*5 + 30*4 = 140 + 120 = 260

// Visual Styles: 6 children
subtreeHeight("visual-styles", 1) = 28*6 + 30*5 = 168 + 150 = 318

// Output Formats: 4 children
subtreeHeight("output-formats", 1) = 28*4 + 30*3 = 112 + 90 = 202

// Icon System: 3 children
subtreeHeight("icon-system", 1) = 28*3 + 30*2 = 84 + 60 = 144
```

### Total Side Heights

```
right_total = 260 + 318 + 30 = 608
left_total  = 202 + 144 + 30 = 376
total_height = max(608, 376) + 50 + 40*2 = 608 + 130 = 738
```

### SVG Dimensions

```
SVG_H = 738
center_x = 600
center_y = 369
```

### Central Node Placement

```
translate_x = 600 - 120/2 = 540
translate_y = 369 - 50/2 = 344
// <g transform="translate(540, 344)">
```

### Right-Side Branch X Positions (Level 1)

```
branch_x = 600 + 60 + 120 * 1 = 780
```

### Right-Side Branch Y Positions

```
// Right side total height = 608
start_y = 369 - 608/2 = 65

// Diagram Types: subtree=260, starts at y=65
diagram_types_y = 65 + (260 - 32) / 2 = 65 + 114 = 179
// Center: 179 + 16 = 195

// Visual Styles: subtree=318, starts at y=65+260+30=355
visual_styles_y = 355 + (318 - 32) / 2 = 355 + 143 = 498
// Center: 498 + 16 = 514
```

### Right-Side Children Y (Diagram Types, 5 children, level 2)

```
start_y = 65  // parent subtree start
children_total = 28*5 + 30*4 = 260

child[0] "Architecture": y = 65 + (260 - 260)/2 + (28-28)/2 = 65, center = 79
child[1] "Mind Map":     y = 65 + 28 + 30 = 123, center = 137
child[2] "Flowchart":    y = 123 + 28 + 30 = 181, center = 195
child[3] "Sequence":     y = 181 + 28 + 30 = 239, center = 253
child[4] "ER Diagram":   y = 239 + 28 + 30 = 297, center = 311
```

### Left-Side Branch X Positions (Level 1)

```
branch_x = 600 - 60 - 120 * 1 - node_w
// Output Formats (w=128): x = 600 - 60 - 120 - 128 = 292
// Icon System (w=112): x = 600 - 60 - 120 - 112 = 308
```

### Left-Side Branch Y Positions

```
start_y = 369 - 376/2 = 181

// Output Formats: subtree=202, starts at y=181
output_formats_y = 181 + (202 - 32) / 2 = 181 + 85 = 266
// Center: 266 + 16 = 282

// Icon System: subtree=144, starts at y=181+202+30=413
icon_system_y = 413 + (144 - 32) / 2 = 413 + 56 = 469
// Center: 469 + 16 = 485
```

### Connection Paths (Examples)

```
// Central node -> Diagram Types (right side)
// Central right edge: (660, 369); Diagram Types left edge: (780, 195)
M 660,369 C 700,369 740,195 780,195

// Central node -> Output Formats (left side)
// Central left edge: (540, 369); Output Formats right edge: (292+128, 282) = (420, 282)
M 540,369 C 500,369 460,282 420,282

// Diagram Types -> Architecture (right side, level 2)
// Diagram Types right edge: (780+128, 195) = (908, 195); Architecture left edge: (900, 79)
M 908,195 C 948,195 860,79 900,79
```

### ViewBox

```
// Rightmost edge: level-2 branch right edge ~ 900 + 120 = 1020
// Leftmost edge: level-1 branch left edge ~ 292
// Width needed: 1020 - 292 + 80 (margin) = 808, fits in 1200

min_x = 0
min_y = 0
viewBox = "0 0 1200 738"
```

## Edge Cases

### Single branch on one side
- The single branch is vertically centered on `center_y`
- No siblings to distribute, so subtree_h = parent allocation

### Very deep nesting (level 4+)
- Branches may extend beyond SVG bounds
- Increase `SVG_W` by `BRANCH_H_GAP` for each additional level
- Or reduce `BRANCH_H_GAP` to 80px for levels 3+

### Uneven sides
- If one side is much taller, `center_y` shifts toward that side's center
- The shorter side's branches are vertically centered within the total height

### Long labels
- `<foreignObject>` width is estimated; CSS `overflow: hidden` + `text-overflow: ellipsis` handles overflow
- Cap estimated width at 200px

### Too many top-level branches (>8)
- Consider regrouping into fewer branches with deeper nesting
- Or increase `BRANCH_V_GAP` and `SVG_H` proportionally
