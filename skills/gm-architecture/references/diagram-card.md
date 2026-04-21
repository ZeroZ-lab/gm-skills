# Card Diagram — Social Sharing Cards

## Overview

Card diagrams generate **social sharing cards** — visually polished, fixed-dimension images optimized for sharing on X/Twitter, WeChat, Instagram, Slack, and similar platforms.

Unlike other diagram types that expand to fit content, cards have a **fixed viewport** (1200×630 or 1080×1080). Content must fit within these bounds.

## When to Use

- Share a technical concept or knowledge point as a social media image
- Create comparison cards (e.g., "Rust vs Go")
- Generate quote cards from famous sayings
- Create ranked lists or top-N charts
- Summarize key takeaways from an article or talk
- 制作知识卡片、对比卡片、引用卡片、排行卡片

## Card Types (4)

### `info` — Knowledge/Concept Card

Displays a title, subtitle, and a grid of key points (2-6 points in a 2-column layout).

**Required fields:** `points` (array of `{label, description}`)

**Layout:** 2-column grid of point cards below the title.

```json
{
  "diagramType": "card",
  "cardType": "info",
  "title": "React Server Components",
  "subtitle": "服务端渲染的新范式",
  "size": "twitter",
  "style": "dark-professional",
  "format": "html",
  "icon": "⚡",
  "points": [
    { "label": "零打包体积", "description": "服务端组件不会被打包到客户端" },
    { "label": "直接数据访问", "description": "无需 API 层，直接读写数据库" },
    { "label": "流式渲染", "description": "支持 Suspense + Streaming" },
    { "label": "自动代码分割", "description": "客户端组件自动按需加载" }
  ],
  "tags": ["React", "Server Components", "SSR"],
  "footer": { "author": "@zhengjianqiao", "brand": "GM Diagram" }
}
```

### `compare` — Side-by-Side Comparison

Displays two items side-by-side with their own colors, icons, and comparison points.

**Required fields:** `sides` (array of exactly 2 `{label, icon, color, points}`)

**Layout:** Left-right split, each side with accent color and 2-5 comparison dimensions.

**Known limitation:** V1 supports exactly 2 sides only (`minItems: 2, maxItems: 2`).

```json
{
  "diagramType": "card",
  "cardType": "compare",
  "title": "Rust vs Go",
  "subtitle": "系统编程语言对比",
  "size": "twitter",
  "style": "dark-professional",
  "format": "html",
  "sides": [
    {
      "label": "Rust",
      "icon": "🦀",
      "color": "#CE422B",
      "points": [
        { "label": "性能", "value": "极快，零成本抽象" },
        { "label": "内存", "value": "无 GC，所有权系统" }
      ]
    },
    {
      "label": "Go",
      "icon": "🐹",
      "color": "#00ADD8",
      "points": [
        { "label": "性能", "value": "快，GC 优化良好" },
        { "label": "内存", "value": "自动垃圾回收" }
      ]
    }
  ],
  "tags": ["Rust", "Go", "系统编程"]
}
```

> **Note:** Compare cards are exempt from the "no custom colors" rule. Each side needs a distinct identity color (`sides[].color`), constrained to hex pattern `^#[0-9a-fA-F]{6}$`.

### `quote` — Famous Quote Card

Displays a quote with attribution. Centered layout with large quote text.

**Required fields:** `quote` (string, max 140 chars)

```json
{
  "diagramType": "card",
  "cardType": "quote",
  "title": "Linus Torvalds",
  "subtitle": "Linux 创始人",
  "size": "instagram",
  "style": "dark-professional",
  "format": "html",
  "quote": "Talk is cheap. Show me the code.",
  "tags": ["Linux", "开源", "编程哲学"]
}
```

### `list` — Ranked List / Top-N Card

Displays a numbered list of items with optional emoji icons.

**Required fields:** `items` (array of 3-10 `{rank, label, icon}`)

**Layout:** Vertical list with rank numbers.

```json
{
  "diagramType": "card",
  "cardType": "list",
  "title": "2026 前端技术趋势",
  "subtitle": "Top 5 值得关注的方向",
  "size": "twitter",
  "style": "dark-professional",
  "format": "html",
  "items": [
    { "rank": 1, "label": "AI-native 开发工具", "icon": "🤖" },
    { "rank": 2, "label": "Server Components 成熟", "icon": "⚡" },
    { "rank": 3, "label": "WebAssembly 突破", "icon": "🔧" },
    { "rank": 4, "label": "Edge-First 架构", "icon": "🌐" },
    { "rank": 5, "label": "信号式状态管理", "icon": "📡" }
  ],
  "tags": ["前端", "2026", "技术趋势"]
}
```

## Size Presets

| Size | Dimensions (px) | Aspect Ratio | Target Platform |
|------|----------------|-------------|----------------|
| `twitter` | 1200 × 630 | ~1.91:1 | X/Twitter, Facebook |
| `instagram` | 1080 × 1080 | 1:1 | Instagram, WeChat Moments |

> `story` (1080×1920) is deferred to V2.

## Output Format

Cards support **only `html` and `svg`** formats. Mermaid is not supported (cards have no Mermaid representation).

PNG and PDF export via `scripts/export.sh`:
```bash
./scripts/export.sh card-output.html --format png
./scripts/export.sh card-output.html --format pdf
```

## Text Length Limits

All text fields have `maxLength` constraints to prevent overflow in the fixed viewport. These values are calibrated for CJK safety (Chinese characters ≈ 2× Latin width):

| Field | maxLength |
|-------|-----------|
| `title` | 35 |
| `subtitle` | 55 |
| `points[].label` | 15 |
| `points[].description` | 40 |
| `sides[].label` | 15 |
| `sides[].points[].label` | 12 |
| `sides[].points[].value` | 30 |
| `quote` | 140 |
| `items[].label` | 25 |
| `tags[]` | 20 |
| `footer.author` | 20 |

## Style Templates

Cards do NOT use the standard `template-*.html` files. Instead, they use a **style variable lookup table** defined in `references/components-card.md`. The table maps each of the 12 styles to CSS custom properties for card-specific rendering.

## Layout Rules

See `references/layout-card.md` for:
- Fixed viewport dimensions
- Font-size definitions per field
- Spacing constants (padding, gap, margin)
- Layout steps for each card type

## Component Templates

See `references/components-card.md` for:
- SVG component templates (background, title, content, tags, footer)
- 12-style CSS variable lookup table
- foreignObject CSS classes
- Emoji font-family fallback stack

## Examples

| Name | Type | File |
|------|------|------|
| React Server Components | info | `card-info-react.json` / `.html` |
| Rust vs Go | compare | `card-compare-rust-go.json` / `.html` |

## Generation Workflow

1. Identify card type from user description (info/compare/quote/list)
2. If type is ambiguous, ask via `AskUserQuestion`
3. Determine `size` from context (twitter default unless user specifies instagram)
4. Determine `style` (ask unless user specified one)
5. **Step 1:** Generate JSON following `schema-card.json`, respecting maxLength limits
6. Validate JSON against schema
7. **Step 2:** Read `references/layout-card.md` for layout constants
8. Read `references/components-card.md` for style variables and component templates
9. Compute layout coordinates based on card type, size, and content
10. Render SVG within the fixed viewport, wrapped in minimal HTML
11. Verify no text overflow, all tags visible, footer correctly placed
12. Deliver file and suggest PNG export if needed
