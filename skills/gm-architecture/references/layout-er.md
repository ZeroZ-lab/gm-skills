# ER Diagram — Layout Rules

## Constants

| Constant | Value | Description |
|----------|-------|-------------|
| SVG_W | 1200 | Total SVG width |
| PAGE_MARGIN | 40 | Top/left margin |
| ENTITY_MIN_W | 160 | Minimum entity width |
| HEADER_H | 30 | Entity header row height |
| ROW_H | 22 | Attribute row height |
| ENTITY_GAP_H | 120 | Horizontal gap between entities |
| ENTITY_GAP_V | 80 | Vertical gap between entities |
| CARD_LABEL_PAD | 30 | Padding for cardinality label |

## Density Multipliers

Apply these multipliers to the constants above based on the `density` parameter (default: `normal`).

| Constant | compact | normal | spacious |
|----------|---------|--------|----------|
| PAGE_MARGIN | 24px | 40px | 60px |
| ENTITY_GAP_H | 80px | 120px | 160px |
| ENTITY_GAP_V | 50px | 80px | 110px |

## Entity Dimensions

### Width
```
entity_w = max(ENTITY_MIN_W, max(
  header_label_length * 9 + 24,
  max(attr: (attr_name_length + attr_type_length) * 7 + 50)
))
```

### Height
```
entity_h = HEADER_H + attributes.length * ROW_H
```

Height formula is `30 + 22 * num_attributes` because the HTML table header is 30px and each attribute row is 22px. This value is used for both the `<foreignObject height="...">` and for computing SVG relationship line endpoints.

## Entity Positioning

### Grid Layout
```
cols = min(3, entity_count)
rows = ceil(entity_count / cols)

col_x[c] = PAGE_MARGIN + c * (max_entity_w + ENTITY_GAP_H)
row_y[r] = PAGE_MARGIN + r * (max_entity_h_in_row + ENTITY_GAP_V)

entity[i].x = col_x[i % cols]
entity[i].y = row_y[floor(i / cols)]
```

### Centering
Center entities horizontally within each column:
```
entity[i].x = col_x[col] + (col_width - entity_w) / 2
```

Note: Text centering within entities is NOT needed here. HTML tables handle text layout naturally via CSS (left-aligned attribute names, left-aligned types, right-aligned badges). No manual `text-anchor` or position math is required for entity content.

## Relationship Lines

### Route Calculation
1. Find the center point of each entity: `(entity.x + entity_w/2, entity.y + entity_h/2)`
2. Determine which edges to connect based on relative positions:
   - If target is to the right: exit from right edge, enter left edge
   - If target is to the left: exit from left edge, enter right edge
   - If same column: exit bottom, enter top
3. For non-aligned entities, add one bend point:
```
path = M exit_x,exit_y L bend_x,exit_y L bend_x,enter_y L enter_x,enter_y
```
4. For horizontally aligned entities:
```
path = M exit_x,exit_y L enter_x,enter_y
```

### Edge Points
Use `entity_h` (= 30 + 22 * num_attributes) to compute edge midpoints:
- Right edge midpoint: `(entity.x + entity_w, entity.y + entity_h/2)`
- Left edge midpoint: `(entity.x, entity.y + entity_h/2)`
- Bottom edge midpoint: `(entity.x + entity_w/2, entity.y + entity_h)`
- Top edge midpoint: `(entity.x + entity_w/2, entity.y)`

### Cardinality Labels
```
fromCard text position: 15px from exit point, offset perpendicular to line
toCard text position: 15px from enter point, offset perpendicular to line
```

Cardinality labels remain SVG elements (not HTML) since they float near relationship lines.

## ViewBox Calculation

```
viewBox_w = max_entity_right_x + PAGE_MARGIN
viewBox_h = max_entity_bottom_y + LEGEND_H + PAGE_MARGIN
```

Where `LEGEND_H = 50` (if legend present).

## Worked Example: E-Commerce Database

6 entities: User, Product, Order, OrderItem, Category, Review

### Entity dimensions
| Entity | Attrs | Width | Height (= 30 + 22*N) |
|--------|-------|-------|----------------------|
| User | 4 (id, email, name, created_at) | 200 | 30+88=118 |
| Product | 5 (id, name, price, stock, category_id) | 220 | 30+110=140 |
| Order | 4 (id, user_id, total, created_at) | 180 | 30+88=118 |
| OrderItem | 4 (id, order_id, product_id, qty) | 200 | 30+88=118 |
| Category | 3 (id, name, description) | 200 | 30+66=96 |
| Review | 4 (id, user_id, product_id, rating) | 200 | 30+88=118 |

### Grid layout (3 cols, 2 rows)
```
Row 0: User(200x118)    Product(220x140)    Order(180x118)
Row 1: OrderItem(200x118) Category(200x96)  Review(200x118)

max_entity_w = 220
col_x = [40, 380, 720]
row_y = [40, 260]

User:      x=50,  y=40
Product:   x=380, y=40
Order:     x=730, y=40
OrderItem: x=50,  y=260
Category:  x=380, y=272  (centered: 260 + (140-96)/2 + 12)
Review:    x=740, y=260
```

### foreignObject dimensions
Each entity uses `<foreignObject width="entity_w" height="entity_h">` matching the calculated dimensions above. The HTML table inside naturally fills the space via CSS `width: 100%`.

### ViewBox
```
width = 940 + 40 = 980
height = 378 + 50 + 40 = 468
viewBox = "0 0 980 468"
```
