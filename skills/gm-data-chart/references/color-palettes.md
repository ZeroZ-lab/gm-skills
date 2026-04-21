# 图表调色板 (Chart Color Palettes)

本参考文档定义了图表数据颜色的调色板系统。图表的颜色分为两个维度：

- **风格 (style)** 控制环境 — 背景、轴线、网格、文字颜色、字体
- **调色板 (palette)** 控制数据 — 柱子填充色、饼图扇区色、折线描边色

这与大多数图表库的设计一致，确保任何风格下的数据都能清晰区分。

---

## 设计原则

> Style controls the environment. Palette controls the data.

数据颜色不应受风格审美的单色限制。即使是 `minimalist`（极简灰）或 `terminal-retro`（绿色终端）风格，图表中的不同数据类别仍然需要通过多色调色板来区分。

---

## 调色板定义

### Palette A — Vivid（鲜艳）

适合浅色/中性背景，高饱和度确保清晰区分。

```
#3b82f6  #ef4444  #22c55e  #f59e0b  #8b5cf6  #ec4899  #06b6d4  #f97316  #14b8a6  #6366f1
```

| 索引 | 色值 | 颜色名 |
|------|------|--------|
| 0 | `#3b82f6` | Blue |
| 1 | `#ef4444` | Red |
| 2 | `#22c55e` | Green |
| 3 | `#f59e0b` | Amber |
| 4 | `#8b5cf6` | Violet |
| 5 | `#ec4899` | Pink |
| 6 | `#06b6d4` | Cyan |
| 7 | `#f97316` | Orange |
| 8 | `#14b8a6` | Teal |
| 9 | `#6366f1` | Indigo |

### Palette B — Muted（柔和）

适合深色背景，饱和度适中，与暗色环境和谐。

```
#6366f1  #f472b6  #34d399  #fbbf24  #a78bfa  #fb923c  #22d3ee  #f87171  #4ade80  #e879f9
```

| 索引 | 色值 | 颜色名 |
|------|------|--------|
| 0 | `#6366f1` | Indigo |
| 1 | `#f472b6` | Pink |
| 2 | `#34d399` | Emerald |
| 3 | `#fbbf24` | Amber |
| 4 | `#a78bfa` | Violet |
| 5 | `#fb923c` | Orange |
| 6 | `#22d3ee` | Cyan |
| 7 | `#f87171` | Red |
| 8 | `#4ade80` | Green |
| 9 | `#e879f9` | Fuchsia |

### Palette C — Warm（暖色）

适合暖色系风格，色彩偏暖但仍有足够区分度。

```
#e74c3c  #f39c12  #27ae60  #3498db  #9b59b6  #1abc9c  #e67e22  #2c3e50  #e91e63  #00bcd4
```

| 索引 | 色值 | 颜色名 |
|------|------|--------|
| 0 | `#e74c3c` | Alizarin |
| 1 | `#f39c12` | Sunflower |
| 2 | `#27ae60` | Nephritis |
| 3 | `#3498db` | Peter River |
| 4 | `#9b59b6` | Amethyst |
| 5 | `#1abc9c` | Turquoise |
| 6 | `#e67e22` | Carrot |
| 7 | `#2c3e50` | Midnight Blue |
| 8 | `#e91e63` | Pink |
| 9 | `#00bcd4` | Cyan |

---

## 风格 → 调色板映射

| 风格 | 调色板 | 理由 |
|------|--------|------|
| dark-professional | **B (Muted)** | 深色背景，柔和色更和谐 |
| cyberpunk-neon | **B (Muted)** | Catppuccin 深色背景 |
| terminal-retro | **B (Muted)** | CRT 深色背景 |
| light-corporate | **A (Vivid)** | 浅色商务背景需要鲜艳色 |
| minimalist | **A (Vivid)** | 白色背景需要高饱和色 |
| notion | **A (Vivid)** | Notion 风格中性背景 |
| material | **A (Vivid)** | Material Design 风格 |
| hand-drawn | **C (Warm)** | 手绘风暖色背景 |
| warm-cozy | **C (Warm)** | Gruvbox 暖色背景 |
| pastel-dream | **C (Warm)** | 柔和暖色背景 |
| blueprint | **A (Vivid)** | Nord 冷色背景用鲜艳色增加对比 |
| glassmorphism | **A (Vivid)** | 半透明风格需要鲜艳色穿透 |

---

## 颜色分配规则

### 优先级（从高到低）

1. **用户指定颜色**：如果 JSON 中 `series[].color` 或 `data[].color` 被设置，直接使用该颜色
2. **调色板颜色**：未指定的颜色按顺序从调色板取

### 分配逻辑

```
For each series (s = 0, 1, 2, ...):
  if series[s].color is set:
    use that color for ALL data points in this series
  else:
    use palette[s % 10]
```

对于饼图（无 series 层级）：

```
For each data point (d = 0, 1, 2, ...):
  if data[d].color is set:
    use that color
  else:
    use palette[d % 10]
```

### 循环规则

调色板有 10 种颜色。如果需要超过 10 种颜色（例如 12 个饼图扇区），使用取模循环：

```
color = palette[index % 10]
```

### 部分覆盖的交互

当部分数据点指定了颜色，部分未指定时：

- 已指定的位置使用用户颜色
- 未指定的位置从调色板按顺序填充，索引独立于覆盖位置

例如饼图 5 个扇区，第 0 个指定 `#ff0000`，其余未指定：
- 扇区 0：`#ff0000`（用户指定）
- 扇区 1：`palette[1]`
- 扇区 2：`palette[2]`
- 扇区 3：`palette[3]`
- 扇区 4：`palette[4]`

---

## 颜色格式规则（安全要求）

### 允许格式

仅允许 `#rrggbb`（6 位十六进制），例如 `#3b82f6`、`#ef4444`。

### 禁止格式

| 格式 | 示例 | 原因 |
|------|------|------|
| `rgb()` | `rgb(59, 130, 246)` | Schema 不允许 |
| `rgba()` | `rgba(59, 130, 246, 0.8)` | Schema 不允许 |
| 命名色 | `blue`, `red` | Schema 不允许 |
| `url()` 引用 | `url(#gradient1)` | 安全风险，可引用外部资源 |
| 3 位简写 | `#f00` | Schema 不允许 |
| `hsl()` | `hsl(217, 91%, 60%)` | Schema 不允许 |

### Schema 强制

所有颜色字段在 JSON Schema 中通过正则强制验证：

```json
{ "type": "string", "pattern": "^#[0-9a-fA-F]{6}$" }
```

不匹配此模式的颜色值会在 Step 1 验证时被拒绝。
