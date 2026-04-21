# Card Component Templates

## Architecture

Cards render as a **single SVG element** with no page wrapper. The SVG viewport is the entire output at fixed dimensions.

All text content uses `foreignObject` with HTML for CSS text handling (overflow, line-clamp). SVG `<text>` is only used for the icon emoji.

## 12-Style CSS Variable Lookup Table

> **How to use:** Read the row matching the JSON `style` field. Apply these CSS custom properties to the SVG root. Use them throughout all component templates.

| Variable | dark-professional | hand-drawn | light-corporate | cyberpunk-neon |
|----------|------------------|------------|-----------------|----------------|
| `--card-bg` | `#020617` | `#faf9f6` | `#f8fafc` | `#11111b` |
| `--card-text` | `#f1f5f9` | `#2c3e50` | `#0f172a` | `#cdd6f4` |
| `--card-title` | `#f1f5f9` | `#2c3e50` | `#0f172a` | `#cdd6f4` |
| `--card-muted` | `#94a3b8` | `#7f8c8d` | `#64748b` | `#a6adc8` |
| `--card-accent` | `#22d3ee` | `#3498db` | `#1e40af` | `#89b4fa` |
| `--card-border` | `rgba(255,255,255,0.06)` | `#27ae60` | `#e2e8f0` | `rgba(137,180,250,0.2)` |
| `--card-point-bg` | `rgba(255,255,255,0.04)` | `#f0ede8` | `#ffffff` | `rgba(137,180,250,0.06)` |
| `--card-tag-bg` | `rgba(255,255,255,0.08)` | `#e8e4de` | `#e2e8f0` | `rgba(137,180,250,0.12)` |
| `--card-radius` | `6` | `10` | `6` | `8` |
| `--card-font` | `JetBrains Mono, monospace` | `Segoe UI, system-ui, sans-serif` | `system-ui, -apple-system, sans-serif` | `JetBrains Mono, monospace` |

| Variable | blueprint | warm-cozy | minimalist | terminal-retro |
|----------|-----------|-----------|------------|----------------|
| `--card-bg` | `#2e3440` | `#f9f5eb` | `#ffffff` | `#0a0a0a` |
| `--card-text` | `#eceff4` | `#3c3836` | `#222222` | `#00ff41` |
| `--card-title` | `#eceff4` | `#3c3836` | `#222222` | `#00ff41` |
| `--card-muted` | `#d8dee9` | `#bdae93` | `#999999` | `#005a15` |
| `--card-accent` | `#88c0d0` | `#b45309` | `#222222` | `#00ff41` |
| `--card-border` | `#4c566a` | `#d5c4a1` | `rgba(0,0,0,0.08)` | `rgba(0,255,65,0.15)` |
| `--card-point-bg` | `rgba(136,192,208,0.08)` | `#f0ebe0` | `#fafafa` | `rgba(0,255,65,0.04)` |
| `--card-tag-bg` | `rgba(136,192,208,0.12)` | `#e8e0d0` | `#f0f0f0` | `rgba(0,255,65,0.08)` |
| `--card-radius` | `2` | `10` | `2` | `4` |
| `--card-font` | `JetBrains Mono, monospace` | `Georgia, system-ui, serif` | `Inter, Helvetica Neue, system-ui, sans-serif` | `Courier New, IBM Plex Mono, monospace` |

| Variable | pastel-dream | notion | material | glassmorphism |
|----------|-------------|--------|----------|---------------|
| `--card-bg` | `#fef7ff` | `#ffffff` | `#fafafa` | `linear-gradient(135deg, #667eea, #764ba2, #f093fb)` |
| `--card-text` | `#3d3250` | `#37352f` | `#212121` | `#ffffff` |
| `--card-title` | `#3d3250` | `#37352f` | `#212121` | `#ffffff` |
| `--card-muted` | `#a89bb5` | `#9b9a97` | `#757575` | `rgba(255,255,255,0.6)` |
| `--card-accent` | `#c084fc` | `#e8e8e5` | `#1976d2` | `rgba(59,130,246,0.5)` |
| `--card-border` | `rgba(0,0,0,0.06)` | `#e8e8e5` | `#e0e0e0` | `rgba(255,255,255,0.2)` |
| `--card-point-bg` | `rgba(192,132,252,0.08)` | `#f7f7f5` | `#f5f5f5` | `rgba(255,255,255,0.12)` |
| `--card-tag-bg` | `rgba(192,132,252,0.12)` | `#f0f0ec` | `#e3f2fd` | `rgba(255,255,255,0.18)` |
| `--card-radius` | `14` | `4` | `6` | `12` |
| `--card-font` | `Nunito, Quicksand, system-ui, sans-serif` | `system-ui, -apple-system, sans-serif` | `Roboto, system-ui, sans-serif` | `Inter, system-ui, sans-serif` |

## Emoji Font Stack

For the `icon` field rendered via SVG `<text>`:
```css
font-family: 'Apple Color Emoji', 'Segoe UI Emoji', 'Noto Color Emoji', sans-serif;
```

For PNG export via resvg-js: macOS renders emoji natively. Linux requires `fonts-noto-color-emoji` installed.

## SVG Root Template

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <style>
    /* Card variables — pick from lookup table above */
    :root {
      --card-bg: #020617;
      --card-text: #f1f5f9;
      --card-title: #f1f5f9;
      --card-muted: #94a3b8;
      --card-accent: #22d3ee;
      --card-border: rgba(255,255,255,0.06);
      --card-point-bg: rgba(255,255,255,0.04);
      --card-tag-bg: rgba(255,255,255,0.08);
      --card-radius: 6;
      --card-font: 'JetBrains Mono', monospace;
    }

    .card-bg { fill: var(--card-bg); }
    .card-title { color: var(--card-title); font-weight: 700; }
    .card-subtitle { color: var(--card-muted); font-weight: 400; }
    .card-point-label { color: var(--card-title); font-weight: 600; }
    .card-point-desc { color: var(--card-text); font-weight: 400; }
    .card-tag {
      color: var(--card-muted);
      background: var(--card-tag-bg);
      border-radius: 4px;
      padding: 4px 10px;
      font-size: 13px;
    }
    .card-footer-author { color: var(--card-muted); font-size: 12px; }
    .card-footer-brand { color: var(--card-muted); font-size: 12px; opacity: 0.6; }
    .card-icon { font-size: 36px; }

    /* Text overflow protection */
    .text-block {
      overflow: hidden;
      text-overflow: ellipsis;
      display: -webkit-box;
      -webkit-box-orient: vertical;
      -webkit-line-clamp: 2;
    }
  </style>

  <!-- Background -->
  <rect class="card-bg" width="{W}" height="{H}" rx="0" />

  <!-- Content via foreignObject -->
</svg>
```

## Component: Title Block

All card types share this header component.

```svg
<!-- Title block: icon + title + subtitle -->
<g transform="translate({PADDING_X}, {PADDING_Y})">
  <!-- Icon (if present) -->
  <text class="card-icon" x="0" y="0" dominant-baseline="hanging"
        font-family="'Apple Color Emoji','Segoe UI Emoji','Noto Color Emoji',sans-serif">
    {escaped-icon}
  </text>

  <!-- Title and subtitle via foreignObject for text wrapping -->
  <foreignObject x="{icon_offset}" y="0" width="{CONTENT_W - icon_offset}" height="80">
    <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: var(--card-font);">
      <div class="card-title" style="font-size: 32px; line-height: 1.2;">{escaped-title}</div>
      {subtitle ? '<div class="card-subtitle" style="font-size: 18px; margin-top: 8px;">{escaped-subtitle}</div>' : ''}
    </div>
  </foreignObject>
</g>
```

## Component: Info Point Grid

```svg
<!-- 2-column grid of point cards -->
<g transform="translate({PADDING_X}, {content_y})">
  <!-- Row 0, Col 0 -->
  <rect x="0" y="0" width="{card_w}" height="{card_h}" rx="{radius}"
        fill="var(--card-point-bg)" stroke="var(--card-border)" stroke-width="1" />
  <foreignObject x="{padding}" y="{padding}" width="{card_w - 2*padding}" height="{card_h - 2*padding}">
    <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: var(--card-font);">
      <div class="card-point-label text-block" style="font-size: 16px;">{escaped-label}</div>
      <div class="card-point-desc text-block" style="font-size: 14px; margin-top: 4px;">{escaped-description}</div>
    </div>
  </foreignObject>

  <!-- Row 0, Col 1 -->
  <rect x="{card_w + gap}" y="0" width="{card_w}" height="{card_h}" rx="{radius}"
        fill="var(--card-point-bg)" stroke="var(--card-border)" stroke-width="1" />
  <!-- ... same foreignObject pattern ... -->

  <!-- Row 1, Col 0 / Col 1 ... -->
</g>
```

## Component: Compare Sides

```svg
<!-- Left-right split with center divider -->
<g transform="translate({PADDING_X}, {content_y})">
  <!-- Left side -->
  <g transform="translate(0, 0)">
    <foreignObject x="0" y="0" width="{side_w}" height="{side_h}">
      <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: var(--card-font); text-align: center;">
        <span style="font-size: 24px;">{escaped-icon}</span>
        <div style="font-size: 20px; font-weight: 700; color: {side-color}; margin-top: 4px;">{escaped-label}</div>
        <!-- Comparison points -->
        <div style="text-align: left; margin-top: 12px;">
          <div style="margin-bottom: 8px;">
            <span style="font-size: 13px; font-weight: 600; color: var(--card-muted);">{escaped-point-label}</span>
            <div style="font-size: 14px; color: var(--card-text);">{escaped-point-value}</div>
          </div>
        </div>
      </div>
    </foreignObject>
  </g>

  <!-- Center divider -->
  <line x1="{side_w + gap/2}" y1="0" x2="{side_w + gap/2}" y2="{side_h}"
        stroke="var(--card-border)" stroke-width="1" stroke-dasharray="4 4" />

  <!-- Right side (same pattern, offset by side_w + gap) -->
</g>
```

## Component: Quote Block

```svg
<!-- Centered quote -->
<g transform="translate({PADDING_X}, {content_y})">
  <!-- Decorative quote mark -->
  <text x="0" y="-10" font-size="60" fill="var(--card-accent)" opacity="0.3"
        font-family="Georgia, serif">"</text>

  <!-- Quote text -->
  <foreignObject x="40" y="0" width="{CONTENT_W - 80}" height="{quote_h}">
    <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: var(--card-font);">
      <div style="font-size: 28px; font-style: italic; color: var(--card-title);
                  line-height: 1.4; text-align: center;" class="text-block">
        {escaped-quote}
      </div>
    </div>
  </foreignObject>

  <!-- Closing quote mark -->
  <text x="{CONTENT_W - 20}" y="{quote_h + 10}" font-size="60" fill="var(--card-accent)"
        opacity="0.3" font-family="Georgia, serif" text-anchor="end">"</text>
</g>
```

## Component: List Items

```svg
<!-- Vertical ranked list -->
<g transform="translate({PADDING_X}, {content_y})">
  <!-- Item 1 -->
  <g transform="translate(0, 0)">
    <text x="0" y="18" font-size="18" font-weight="700" fill="var(--card-accent)"
          font-family="var(--card-font)">01</text>
    <text x="40" y="18" font-size="20"
          font-family="'Apple Color Emoji','Segoe UI Emoji','Noto Color Emoji',sans-serif">{escaped-icon}</text>
    <text x="68" y="18" font-size="16" fill="var(--card-text)" font-family="var(--card-font)">{escaped-label}</text>
  </g>

  <!-- Item 2 (y offset = LIST_ITEM_HEIGHT + LIST_ITEM_GAP) -->
  <!-- ... repeat for each item ... -->
</g>
```

## Component: Tags Row

```svg
<!-- Tags at bottom of content area -->
<g transform="translate({PADDING_X}, {tags_y})">
  <foreignObject x="0" y="0" width="{CONTENT_W}" height="24">
    <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; gap: 8px; font-family: var(--card-font);">
      <span class="card-tag">#{escaped-tag1}</span>
      <span class="card-tag">#{escaped-tag2}</span>
      <span class="card-tag">#{escaped-tag3}</span>
    </div>
  </foreignObject>
</g>
```

## Component: Footer

```svg
<!-- Footer: author left, brand right -->
<g transform="translate({PADDING_X}, {footer_y})">
  <foreignObject x="0" y="0" width="{CONTENT_W}" height="20">
    <div xmlns="http://www.w3.org/1999/xhtml"
         style="display: flex; justify-content: space-between; font-family: var(--card-font);">
      <span class="card-footer-author">{escaped-author}</span>
      <span class="card-footer-brand">{escaped-brand}</span>
    </div>
  </foreignObject>
</g>
```

## Rendering Order

1. Background rect (full viewport)
2. Title block (icon + title + subtitle)
3. Content area (varies by cardType)
4. Tags row
5. Footer
