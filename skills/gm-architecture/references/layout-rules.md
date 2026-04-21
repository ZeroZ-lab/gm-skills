# Layout Rules Reference (CSS + SVG Hybrid)

These rules compute SVG coordinates for the hybrid CSS+SVG approach. CSS handles module positioning and text centering — you only need to compute **layer y-positions** and **arrow endpoints**.

## What CSS Handles (NO calculation needed)

- Module width: auto-sized from label text via `min-width: 100px; padding: 0 16px`
- Module horizontal centering: `justify-content: center` in `.modules` flexbox
- Text centering: `display: flex; align-items: center; justify-content: center`
- Module spacing: `gap: 20px` in `.modules` flexbox
- Tech badge layout: auto-flowed below module label

## What You Must Compute

Only two things need coordinate math:
1. **Layer y-positions** (vertical stacking)
2. **Arrow start/end points** (SVG lines between layers)

## Constants

| Name | Value | Purpose |
|------|-------|---------|
| `PAGE_MARGIN` | 40px | Space between SVG edge and first element |
| `LAYER_GAP` | 50px | Vertical gap between layer cards |
| `SVG_W` | 1000px | SVG viewBox width (fixed) |
| `LAYER_W` | 920px | Layer card width (= SVG_W - 2 * PAGE_MARGIN) |
| `LEGEND_OFFSET` | 50px | Space below last layer before legend |

### Style-Specific Layer Heights

**CRITICAL:** Layer heights vary by visual style due to different border widths and padding.

| Style | `LAYER_H_SIMPLE` | `LAYER_H_BADGE` | `LAYER_H_EMPTY` |
|-------|------------------|-----------------|-----------------|
| dark-professional | 101px | 116px | 60px |
| cyberpunk-neon | 101px | 116px | 60px |
| terminal-retro | 101px | 116px | 60px |
| light-corporate | 105px | 120px | 65px |
| minimalist | 95px | 110px | 55px |
| **hand-drawn** | **110px** | **130px** | **70px** |
| warm-cozy | 105px | 120px | 65px |
| blueprint | 101px | 116px | 60px |
| pastel-dream | 105px | 125px | 65px |

> **Why different heights?** Thicker borders and larger visual elements need more room. Hand-drawn style has 2.5px layer borders (vs 1px for dark), requiring ~15-20px extra height to prevent content overflow.

## Density Multipliers

Apply these multipliers to the constants above based on the `density` parameter (default: `normal`).

| Constant | compact | normal | spacious |
|----------|---------|--------|----------|
| PAGE_MARGIN | 24px | 40px | 60px |
| LAYER_GAP | 30px | 50px | 70px |
| MODULE_GAP | 12px | 20px | 28px |

## Step 1: Determine Layer Heights

> ⚠️ **CRITICAL RULE: ALWAYS use fixed heights. NEVER compute custom heights based on content.**
> The most common layout bug is using non-standard heights (e.g., 49px, 80px, 106px) for individual layers,
> which breaks the y-position chain and causes layers to overlap.

For each layer, choose a fixed height from the table below:

| Condition | Height | Constant |
|-----------|--------|----------|
| Any module in the layer has `tech` badges | **116px** | `LAYER_H_BADGE` |
| All modules have NO tech badges | **101px** | `LAYER_H_SIMPLE` |
| Layer has NO children (empty layer, label only) | **60px** | `LAYER_H_EMPTY` |

**Common mistakes to avoid:**
- ❌ Using 49px for a layer with 1 module → use 116px (if module has badges) or 101px
- ❌ Using 80px for a "thin" layer → use 116px or 101px
- ❌ Computing height from module count → always use the fixed values above
- ❌ Making Gateway/Infra layers shorter because they have fewer modules → still use fixed heights

## Step 2: Position Layers Vertically

```
layer_y[0] = PAGE_MARGIN (= 40)
layer_y[i] = layer_y[i-1] + layer_card_h[i-1] + LAYER_GAP
```

All layers use the same x and width:
```
layer_x = PAGE_MARGIN (= 40)
layer_w = LAYER_W (= 920)
```

## Step 3: Draw Layer Content (CSS Layout)

For each layer, output this pattern:

```svg
<g transform="translate(40, LAYER_Y)">
  <!-- Masking rect (hides arrows behind this layer) -->
  <rect width="920" height="LAYER_H" rx="8" fill="[background-color]"/>
  <!-- CSS-styled content -->
  <foreignObject width="920" height="LAYER_H">
    <div xmlns="http://www.w3.org/1999/xhtml" class="layer-card type-[LAYER_TYPE]">
      <div class="layer-label">[LAYER_LABEL]</div>
      <div class="modules">
        <div class="module [type-X] [has-badges?]">
          <span class="module-label">[MODULE_LABEL]</span>
          <span class="tech-badges">
            <span class="tech-badge">[BADGE_TEXT]</span>
          </span>
        </div>
        <!-- more modules... -->
      </div>
    </div>
  </foreignObject>
</g>
```

For `count: "multiple"` layers, add a stacked border:
```svg
<rect x="4" y="3" width="920" height="LAYER_H" rx="8"
      fill="none" stroke="[color]" stroke-width="0.5" opacity="0.3"/>
```

## Step 4: Compute Connection Paths

For each connection, compute SVG line endpoints from layer positions.

### Arrow Anchor Points

```
source_bottom_center = (SVG_W/2, source_layer_y + source_layer_h)
target_top_center    = (SVG_W/2, target_layer_y)
```

For connections between specific modules (not whole layers):
```
source_bottom = (estimated_module_center_x, source_layer_y + source_layer_h)
target_top    = (estimated_module_center_x, target_layer_y)
```

### Connection Routing Rules

1. **Adjacent layers** (directly above/below): straight vertical line
   ```
   <line x1="500" y1="source_bottom_y" x2="500" y2="target_top_y" .../>
   ```

2. **Skipping layers**: route along LEFT or RIGHT edge to avoid crossing intermediate layers
   ```
   <!-- Left edge route -->
   <path d="M 60,SRC_Y L 20,SRC_Y L 20,TGT_Y L 60,TGT_Y" fill="none" .../>
   <!-- Right edge route -->
   <path d="M 940,SRC_Y L 980,SRC_Y L 980,TGT_Y L 940,TGT_Y" fill="none" .../>
   ```

3. **Same-layer connections**: horizontal line at module level
   ```
   <line x1="SOURCE_RIGHT_X" y1="MODULE_Y+25" x2="TARGET_LEFT_X" y2="MODULE_Y+25" .../>
   ```

**CRITICAL**: NEVER draw diagonal lines through intermediate layer cards. Always route around them.

### Connection Label Position

```
label_y = (source_y + target_y) / 2
label_x = midpoint of the line segment (or SVG_W/2 for vertical lines)
```

Use SVG `<text>` with `text-anchor="middle" dominant-baseline="central"` for labels.

## Step 5: Compute ViewBox

```
viewBox_h = last_layer_y + last_layer_h + LEGEND_OFFSET + 50 + 30
viewBox = "0 0 1000 viewBox_h"
```

Default: `"0 0 1000 620"`. Adjust based on actual content.

## Step 5.5: VERIFY — Overlap Check (MANDATORY)

After computing all positions, verify NO layers overlap:

```
for each pair of adjacent layers (i, i+1):
  gap = layer_y[i+1] - (layer_y[i] + layer_h[i])
  assert gap == LAYER_GAP (50px), otherwise there is an overlap!
```

If ANY gap ≠ 50px, recompute the y-positions from the first incorrect layer downward.

**Quick sanity check**: tabulate all layers with their y, h, and gap-to-next. Example correct table:

| # | Label | y | h | End | Gap |
|---|-------|---|---|-----|-----|
| 0 | Gateway | 40 | 116 | 156 | 50 |
| 1 | Frontend | 206 | 116 | 322 | 50 |
| 2 | Backend | 372 | 116 | 488 | 50 |
| 3 | Core | 538 | 116 | 654 | 50 |
| 4 | Workers | 704 | 116 | 820 | 50 |
| 5 | Data | 870 | 116 | 986 | 50 |
| 6 | External | 1036 | 116 | 1152 | — |

## Step 6: Position Legend

```
legend_y = last_layer_y + last_layer_h + LEGEND_OFFSET
```

Use foreignObject + CSS flexbox for legend layout:

```svg
<g transform="translate(40, LEGEND_Y)">
  <foreignObject width="920" height="40">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <div style="font-size:11px; font-weight:600; color:[text-color]; margin-bottom:8px;">Legend</div>
      <div class="legend-container">
        <div class="legend-item">
          <div class="legend-swatch type-process"></div>
          <span class="legend-text">Process</span>
        </div>
        <!-- more items... -->
      </div>
    </div>
  </foreignObject>
</g>
```

## Worked Example: Chrome Architecture

### Layers
| # | Label | Type | Has Badges? | Height |
|---|-------|------|-------------|--------|
| 0 | Browser Process | process | no | 101 |
| 1 | Renderer Process | process | yes | 116 |
| 2 | GPU Process | infra | no | 101 |
| 3 | Utility Process | infra | no | 101 |

### Y Positions
```
layer_y[0] = 40
layer_y[1] = 40 + 101 + 50 = 191
layer_y[2] = 191 + 116 + 50 = 357
layer_y[3] = 357 + 101 + 50 = 508
```

### Connections
| From → To | Type | Routing |
|-----------|------|---------|
| L0 → L1 | bidirectional IPC | straight: (500, 141) → (500, 191) |
| L0 → L2 | dashed Command Buffer | left-edge route: skip L1 |
| L1 → L2 | solid GPU Commands | straight: (500, 307) → (500, 357) |
| L0 → L3 | bidirectional IPC | right-edge route: skip L1, L2 |

### ViewBox
```
h = 508 + 101 + 50 + 50 + 30 = 739 → "0 0 1000 740"
```

## Edge Cases

### Too many modules in one layer (>5)
- Add class `module-compact` which reduces padding to `0 10px`
- If still overflowing, split into two rows with a second `.modules` div

### No connections
- Skip Step 4 entirely, layout is just stacked layers

### Groups (security/region boundaries)
- Draw SVG `<rect>` around the layers that belong to the group
- Add 20px padding on each side
- Position SVG `<text>` label at top-left

### Layer with no children
- Set height to **60px** (just the label)
- Use `type-[layer_type]` for the border styling

### Layer with only 1 module (e.g., Gateway, Load Balancer)
- **Still use LAYER_H_BADGE (116px) or LAYER_H_SIMPLE (101px)** — do NOT shrink the height
- A single-module layer is NOT the same as a no-children layer
- Example: a Gateway layer with Nginx module + `:80/:443` badge → height = 116px

## LR Mode (Left-to-Right)

When `direction` is `"LR"`, layers become vertical columns arranged horizontally instead of horizontal rows stacked vertically.

### Layout Changes

- **Layers become vertical columns** arranged left-to-right
- **SVG_W** becomes computed from column count; **SVG_H** is fixed at 800px
- **Column width**: 180px; **Column gap**: 40px
- **Modules stack vertically** within each column (`flex-direction: column`)
- **Connections route horizontally** between columns

### Coordinate Formulas

```
col_x[0] = PAGE_MARGIN
col_x[i] = col_x[i-1] + col_w + 40
```

Where `col_w = 180` and the column gap is `40`.

### ViewBox Calculation

```
viewBox_w = col_x[last] + col_w + PAGE_MARGIN
viewBox_h = max(col_h) + PAGE_MARGIN * 2
viewBox = "0 0 viewBox_w viewBox_h"
```

### Connection Routing

- Adjacent columns: straight horizontal line from right edge of source column to left edge of target column
- Skipping columns: route along TOP or BOTTOM edge to avoid crossing intermediate columns
