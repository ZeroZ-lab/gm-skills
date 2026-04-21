# Card Layout Rules

## Architecture

Cards use a **fixed-viewport SVG** approach. The SVG viewport is the entire output — no page wrapper, no scrolling.

```
┌─────────────────────────────────────────┐
│  PADDING_TOP                            │
│  ┌─────────────────────────────────────┐│
│  │  ICON + TITLE                       ││
│  │  SUBTITLE                            ││
│  │                                      ││
│  │  CONTENT AREA (varies by cardType)   ││
│  │                                      ││
│  │  TAGS                                ││
│  │  FOOTER                    BRAND     ││
│  └─────────────────────────────────────┘│
│  PADDING_BOTTOM                         │
└─────────────────────────────────────────┘
```

## Size Constants

| Constant | twitter (1200×630) | instagram (1080×1080) |
|----------|-------------------|----------------------|
| `VIEWPORT_W` | 1200 | 1080 |
| `VIEWPORT_H` | 630 | 1080 |
| `PADDING_X` | 60 | 50 |
| `PADDING_Y` | 40 | 60 |
| `CONTENT_W` | 1080 (=1200-2×60) | 980 (=1080-2×50) |

## Font Sizes

| Element | Font Size (px) | Font Weight | Color Variable |
|---------|---------------|-------------|----------------|
| `icon` | 36 | 400 | --card-accent |
| `title` | 32 | 700 (bold) | --card-title |
| `subtitle` | 18 | 400 | --card-muted |
| `points[].label` | 16 | 600 (semibold) | --card-title |
| `points[].description` | 14 | 400 | --card-text |
| `sides[].label` | 20 | 700 | --card-title |
| `sides[].points[].label` | 13 | 600 | --card-muted |
| `sides[].points[].value` | 14 | 400 | --card-text |
| `quote` | 28 | 400 italic | --card-title |
| `items[].rank` | 18 | 700 | --card-accent |
| `items[].label` | 16 | 400 | --card-text |
| `tags[]` | 13 | 400 | --card-muted |
| `footer.author` | 12 | 400 | --card-muted |
| `footer.brand` | 12 | 400 | --card-muted |

## Spacing Constants

| Constant | Value (px) | Description |
|----------|-----------|-------------|
| `ICON_TITLE_GAP` | 12 | Space between icon and title text |
| `TITLE_SUBTITLE_GAP` | 8 | Space between title and subtitle |
| `SUBTITLE_CONTENT_GAP` | 24 | Space between subtitle and content area |
| `POINT_CARD_GAP` | 16 | Gap between point cards (horizontal and vertical) |
| `POINT_CARD_PADDING` | 16 | Internal padding of point cards |
| `POINT_CARD_RADIUS` | 8 | Border radius of point cards |
| `COMPARE_DIVIDER_GAP` | 32 | Gap for the center divider between sides |
| `COMPARE_POINT_GAP` | 12 | Gap between comparison points vertically |
| `LIST_ITEM_GAP` | 8 | Gap between list items vertically |
| `RANK_LABEL_GAP` | 12 | Gap between rank number and label text |
| `TAGS_CONTENT_GAP` | 20 | Space between content area and tags row |
| `TAG_GAP` | 8 | Gap between individual tags |
| `FOOTER_TAGS_GAP` | 16 | Space between tags row and footer |
| `TAG_PADDING_X` | 10 | Horizontal padding inside each tag |
| `TAG_PADDING_Y` | 4 | Vertical padding inside each tag |
| `TAG_RADIUS` | 4 | Border radius of tag badges |

## Layout: info Card

```
Available height = VIEWPORT_H - 2*PADDING_Y = twitter: 550, instagram: 960

Section heights (twitter / instagram):
  Title block (icon+title+subtitle): ~90 / ~100
  Content area (2-column grid):      ~280 / ~560
  Tags row:                           ~30 / ~30
  Footer:                             ~20 / ~20
  Gaps:                               ~52 / ~52
  Total:                              ~472 / ~762  ← fits within available

Point card layout:
  Columns: 2
  Cards per row: 2 (or 3 if 6 points)
  Card width: (CONTENT_W - POINT_CARD_GAP) / 2
  Card min-height: 80px

  twitter card width: (1080 - 16) / 2 = 532px
  instagram card width: (980 - 16) / 2 = 482px
```

## Layout: compare Card

```
Available height = same as info

Left-right split:
  Divider at center: x = VIEWPORT_W / 2
  Side width: (VIEWPORT_W - 2*PADDING_X - COMPARE_DIVIDER_GAP) / 2

  twitter side width: (1200 - 120 - 32) / 2 = 524px
  instagram side width: (1080 - 100 - 32) / 2 = 474px

Each side contains:
  Side icon + label (centered)
  Comparison points (label: value rows)
```

## Layout: quote Card

```
Centered layout:
  Quote text: centered horizontally and vertically
  Quote marks: decorative " " at larger font size
  Max width for quote text: CONTENT_W * 0.85

  twitter: 1080 * 0.85 = 918px max
  instagram: 980 * 0.85 = 833px max
```

## Layout: list Card

```
Vertical list:
  Each item: rank number + icon + label text
  Item height: ~36px (including LIST_ITEM_GAP)
  Rank numbers right-aligned or left-aligned in a fixed-width column

  twitter (height 550 available after title/footer):
    Max items at 36px each: ~12 (but schema limits to 10)

  instagram (height 960 available):
    Max items at 36px each: ~20 (but schema limits to 10)
```

## Text Overflow Handling

**Primary defense: schema `maxLength`** — limits input text length.

**Secondary defense: CSS overflow** — text blocks use foreignObject with:
```css
overflow: hidden;
text-overflow: ellipsis;
-webkit-line-clamp: 2;
display: -webkit-box;
-webkit-box-orient: vertical;
```

**Important:** resvg-js (PNG export) does NOT support CSS overflow properties. The schema maxLength is the primary defense for PNG export correctness.

## HTML Structure

Cards use a minimal HTML wrapper — no standard template:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escaped-title}</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { display: flex; justify-content: center; align-items: center;
           min-height: 100vh; background: #111; }
    svg { max-width: 100%; height: auto; }
  </style>
</head>
<body>
  <svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"
       viewBox="0 0 {W} {H}">
    <!-- Card content -->
  </svg>
</body>
</html>
```

## What Layout Does NOT Compute

- Text wrapping within foreignObject (handled by CSS)
- Emoji rendering (depends on system fonts)
- Exact pixel widths of text (font-dependent)
