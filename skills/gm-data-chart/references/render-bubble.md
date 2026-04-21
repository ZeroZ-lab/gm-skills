# 气泡图渲染规则 (Bubble Chart Rendering Rules)

本参考文档定义了 bubble chart 的完整渲染流程，包含坐标公式和 worked example。LLM 在 Step 2 生成 SVG 输出时必须遵循这些规则。

---

## 渲染架构

Bubble chart 采用 **混合渲染模式**：

| 层次 | 技术 | 元素 |
|------|------|------|
| 数据图形 | SVG 原生元素 | `<circle>`（气泡）、`<line>`（坐标轴、网格线） |
| 文字区域 | foreignObject + CSS | 标题、轴标签、轴标题、图例、数据点标签、size 图例 |

---

## 布局常量

| 名称 | 值 | 用途 |
|------|-----|------|
| `CHART_PADDING_TOP` | 60px | 标题区域 |
| `CHART_PADDING_RIGHT` | 40px | 右侧留白 |
| `CHART_PADDING_BOTTOM` | 60px | X 轴标签区域 |
| `CHART_PADDING_LEFT` | 70px | Y 轴标签区域 |

### 尺寸计算

```
totalWidth = totalHeight = 500（正方形 ViewBox，与 scatter 一致）
```

### 绘图区域

```
plotWidth  = totalWidth - CHART_PADDING_LEFT - CHART_PADDING_RIGHT  = 500 - 70 - 40 = 390
plotHeight = totalHeight - CHART_PADDING_TOP - CHART_PADDING_BOTTOM = 500 - 60 - 60 = 380
plotX = CHART_PADDING_LEFT  = 70
plotY = CHART_PADDING_TOP   = 60
```

---

## 逐步渲染流程

### Step A：读取数据

从 JSON 中读取：
- `series[].data[].x` — X 坐标值
- `series[].data[].y` — Y 坐标值
- `series[].data[].size` — 气泡大小值（映射为面积）
- `series[].data[].label` — 可选的气泡标签
- `axis.x.ticks` — Nice Numbers 预计算的 X 轴刻度数组
- `axis.y.ticks` — Nice Numbers 预计算的 Y 轴刻度数组
- `sizeRange.minRadius` — 最小气泡半径（默认 5px）
- `sizeRange.maxRadius` — 最大气泡半径（默认 35px）

### Step B：坐标映射（双轴线性映射）

与 scatter chart 相同，X 轴和 Y 轴都是数值轴：

```
// 从 ticks 数组派生（Step 1 预计算）
xMinTick = axis.x.ticks[0]
xMaxTick = axis.x.ticks[axis.x.ticks.length - 1]
yMinTick = axis.y.ticks[0]
yMaxTick = axis.y.ticks[axis.y.ticks.length - 1]
xTickRange = xMaxTick - xMinTick
yTickRange = yMaxTick - yMinTick

valueToX(val) = plotX + ((val - xMinTick) / xTickRange) * plotWidth
valueToY(val) = plotY + plotHeight - ((val - yMinTick) / yTickRange) * plotHeight
```

### Step C：计算气泡半径（面积映射）

`size` 值通过 **面积映射** 转换为半径（不是线性映射到半径），确保视觉面积比例正确：

```
minSize = min(all series[].data[].size)
maxSize = max(all series[].data[].size)
minR = sizeRange.minRadius   // default 5
maxR = sizeRange.maxRadius   // default 35

For each data point:
  if maxSize == minSize:
    r = (minR + maxR) / 2
  else:
    radiusSquared = minR² + (size - minSize) / (maxSize - minSize) * (maxR² - minR²)
    r = sqrt(radiusSquared)
```

**为什么用面积映射而非半径线性映射**：如果 radius 直接线性映射到 size，视觉面积会按 size² 增长，导致大泡看起来比小泡大太多。面积映射确保视觉面积与数据值成线性比例。

### Step D：绘制网格线

**X 轴和 Y 轴都默认显示网格线** (`scatterAxisConfig.gridLines` 默认 `true`)。

Y 轴网格线（水平虚线）：

```svg
<line x1="{plotX}" y1="{valueToY(tickValue)}" x2="{plotX + plotWidth}" y2="{valueToY(tickValue)}" class="grid-line" />
```

X 轴网格线（垂直虚线）：

```svg
<line x1="{valueToX(tickValue)}" y1="{plotY}" x2="{valueToX(tickValue)}" y2="{plotY + plotHeight}" class="grid-line" />
```

### Step E：绘制坐标轴

```svg
<!-- Y 轴 -->
<line x1="{plotX}" y1="{plotY}" x2="{plotX}" y2="{plotY + plotHeight}" class="axis-line" />

<!-- X 轴 -->
<line x1="{plotX}" y1="{plotY + plotHeight}" x2="{plotX + plotWidth}" y2="{plotY + plotHeight}" class="axis-line" />
```

### Step F：绘制气泡（SVG `<circle>`）

**渲染顺序**：按 size 升序绘制（小泡先画、大泡后画），确保大泡在上层、标签不被小泡遮挡。size 相同时按 series 索引升序，再按 data 索引升序。

```
// 排序算法
sortedPoints = []
for s = 0..numSeries-1:
  for d = 0..series[s].data.length-1:
    sortedPoints.append({series: s, data: d, size: series[s].data[d].size})

sortedPoints.sort((a, b) => {
  if (a.size != b.size) return a.size - b.size   // size 升序
  if (a.series != b.series) return a.series - b.series   // series 索引升序
  return a.data - b.data   // data 索引升序
})

// 按排序顺序依次绘制
```

每个气泡使用 `.bubble-point` CSS 类，半透明填充 + 实色描边：

```svg
<circle cx="{valueToX(d.x)}" cy="{valueToY(d.y)}" r="{r}"
        fill="{color}" fill-opacity="0.5"
        stroke="{color}" stroke-width="1.5" stroke-opacity="0.8"
        class="bubble-point" />
```

**颜色**：`color` 通过 `color-palettes.md` 的规则确定。未指定时使用 `palette[s % 10]`。

### Step G：绘制气泡标签（可选，foreignObject + CSS）

只有 `data[].label` 存在时才显示标签。标签放在气泡中心（优先）或上方：

```svg
<foreignObject x="{cx - 30}" y="{cy - 10}" width="60" height="20">
  <div xmlns="http://www.w3.org/1999/xhtml" class="tick-label"
       style="text-align: center; font-size: 10px;">
    {d.label}
  </div>
</foreignObject>
```

如果气泡太小（r < 15），标签放在气泡上方避免溢出：

```svg
<foreignObject x="{cx - 30}" y="{cy - r - 18}" width="60" height="16">
  <div xmlns="http://www.w3.org/1999/xhtml" class="tick-label"
       style="text-align: center; font-size: 10px;">
    {d.label}
  </div>
</foreignObject>
```

### Step H：绘制轴标签（foreignObject + CSS）

**Y 轴刻度值**：

```svg
<foreignObject x="0" y="{tickY - 10}" width="{CHART_PADDING_LEFT - 10}" height="20">
  <div xmlns="http://www.w3.org/1999/xhtml" class="tick-label" style="text-align: right;">
    {tickValue}
  </div>
</foreignObject>
```

**X 轴刻度值**：

```svg
<foreignObject x="{valueToX(tickValue) - 30}" y="{plotY + plotHeight + 8}" width="60" height="20">
  <div xmlns="http://www.w3.org/1999/xhtml" class="tick-label" style="text-align: center;">
    {tickValue}
  </div>
</foreignObject>
```

### Step I：绘制轴标题（foreignObject + CSS）

```svg
<!-- Y 轴标题（旋转） -->
<foreignObject x="0" y="{plotY}" width="20" height="{plotHeight}">
  <div xmlns="http://www.w3.org/1999/xhtml" class="axis-title"
       style="transform: rotate(-90deg); transform-origin: center; display: flex; align-items: center; justify-content: center; height: 100%;">
    {axis.y.label}
  </div>
</foreignObject>

<!-- X 轴标题 -->
<foreignObject x="{plotX}" y="{plotY + plotHeight + 35}" width="{plotWidth}" height="20">
  <div xmlns="http://www.w3.org/1999/xhtml" class="axis-title" style="text-align: center;">
    {axis.x.label}
  </div>
</foreignObject>
```

### Step J：绘制图例（foreignObject + CSS）

图例包含两部分：系列名称图例 + size 图例指示器。

**系列名称图例**：

```svg
<foreignObject x="{plotX}" y="{plotY - 35}" width="{plotWidth}" height="30">
  <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: center; justify-content: center; gap: 16px;">
    <!-- 每个系列一个图例项 -->
    <div style="display: flex; align-items: center; gap: 6px;">
      <div style="width: 12px; height: 12px; background: {color}; border-radius: 50%; opacity: 0.5;"></div>
      <span class="tick-label">{seriesName}</span>
    </div>
  </div>
</foreignObject>
```

**Size 图例指示器**（放在图表右下角或底部空白处）：

```svg
<foreignObject x="{plotX + plotWidth - 120}" y="{plotY + plotHeight + 40}" width="120" height="20">
  <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: center; gap: 6px; justify-content: flex-end;">
    <span class="tick-label" style="font-size: 10px;">Size:</span>
    <svg width="80" height="16" xmlns="http://www.w3.org/2000/svg">
      <circle cx="12" cy="10" r="{minR}" fill="#64748b" fill-opacity="0.3" stroke="#64748b" stroke-width="1" />
      <circle cx="40" cy="10" r="{(minR + maxR) / 2}" fill="#64748b" fill-opacity="0.3" stroke="#64748b" stroke-width="1" />
      <circle cx="68" cy="10" r="{maxR}" fill="#64748b" fill-opacity="0.3" stroke="#64748b" stroke-width="1" />
    </svg>
  </div>
</foreignObject>
```

### Step K：绘制标题和副标题

```svg
<!-- 标题 -->
<foreignObject x="{plotX}" y="10" width="{plotWidth}" height="28">
  <div xmlns="http://www.w3.org/1999/xhtml" class="axis-title"
       style="text-align: center; font-size: 18px; font-weight: 700;">
    {title}
  </div>
</foreignObject>

<!-- 副标题 -->
<foreignObject x="{plotX}" y="36" width="{plotWidth}" height="20">
  <div xmlns="http://www.w3.org/1999/xhtml" class="tick-label"
       style="text-align: center;">
    {subtitle}
  </div>
</foreignObject>
```

---

## Worked Example

**输入**：产品竞争力分析 JSON

```json
{
  "series": [
    {
      "name": "产品",
      "data": [
        {"x": 50, "y": 8.5, "size": 30, "label": "Product A"},
        {"x": 80, "y": 7.0, "size": 15, "label": "Product B"},
        {"x": 30, "y": 9.2, "size": 45, "label": "Product C"},
        {"x": 65, "y": 6.5, "size": 10, "label": "Product D"}
      ]
    }
  ],
  "axis": {
    "x": { "label": "价格", "ticks": [0, 20, 40, 60, 80, 100] },
    "y": { "label": "满意度", "ticks": [5, 6, 7, 8, 9, 10] }
  },
  "sizeRange": { "minRadius": 5, "maxRadius": 35 }
}
```

**计算**：

```
totalWidth = totalHeight = 500
plotWidth = 500 - 70 - 40 = 390
plotHeight = 500 - 60 - 60 = 380
plotX = 70, plotY = 60

xMinTick = 0, xMaxTick = 100, xTickRange = 100
yMinTick = 5, yMaxTick = 10, yTickRange = 5

valueToX(val) = 70 + (val / 100) * 390
valueToY(val) = 60 + 380 - ((val - 5) / 5) * 380

// Size → Radius (面积映射)
minSize = 10, maxSize = 45
minR = 5, maxR = 35
minR² = 25, maxR² = 1225

Product D: size=10
  radiusSquared = 25 + (10-10)/(45-10) * (1225-25) = 25 + 0 = 25
  r = sqrt(25) = 5

Product B: size=15
  radiusSquared = 25 + (15-10)/35 * 1200 = 25 + 171.4 = 196.4
  r = sqrt(196.4) ≈ 14.0

Product A: size=30
  radiusSquared = 25 + (30-10)/35 * 1200 = 25 + 685.7 = 710.7
  r = sqrt(710.7) ≈ 26.7

Product C: size=45
  radiusSquared = 25 + (45-10)/35 * 1200 = 25 + 1200 = 1225
  r = sqrt(1225) = 35
```

**渲染排序**（按 size 升序）：Product D (10) → Product B (15) → Product A (30) → Product C (45)

**气泡坐标**：

| 产品 | x | y | size | valueToX | valueToY | radius |
|------|---|---|------|----------|----------|--------|
| Product D | 65 | 6.5 | 10 | 70 + (65/100)*390 = 323.5 | 60 + 380 - (1.5/5)*380 = 326 | 5.0 |
| Product B | 80 | 7.0 | 15 | 70 + (80/100)*390 = 382 | 60 + 380 - (2/5)*380 = 288 | 14.0 |
| Product A | 50 | 8.5 | 30 | 70 + (50/100)*390 = 265 | 60 + 380 - (3.5/5)*380 = 174 | 26.7 |
| Product C | 30 | 9.2 | 45 | 70 + (30/100)*390 = 187 | 60 + 380 - (4.2/5)*380 = 120.8 | 35.0 |

**X 轴网格线**（对每个 tick）：

| tick | valueToX |
|------|----------|
| 0 | 70 |
| 20 | 148 |
| 40 | 226 |
| 60 | 304 |
| 80 | 382 |
| 100 | 460 |

**Y 轴网格线**（对每个 tick）：

| tick | valueToY |
|------|----------|
| 5 | 440 |
| 6 | 364 |
| 7 | 288 |
| 8 | 212 |
| 9 | 136 |
| 10 | 60 |

**颜色**：dark-professional → Palette B → `palette[0]` = `#6366f1`

---

## 与 Scatter 的关键差异

| 方面 | Scatter | Bubble |
|------|---------|--------|
| 数据维度 | 2D (x, y) | 3D (x, y, size) |
| 数据点大小 | 固定（pointSize） | 按数据值映射（面积映射） |
| 数据点形状 | 4 种可选（circle/square/diamond/triangle） | 仅 circle |
| 填充透明度 | 0.7 | 0.5（更透明以显示重叠） |
| CSS 类 | `.scatter-point` | `.bubble-point` |
| 渲染顺序 | 按数据顺序 | 按 size 升序（小泡先、大泡后） |
| 图例 | 仅系列名称 | 系列名称 + size 图例指示器 |
| Series 上限 | 8 | 5（气泡占用更多空间） |
| Mermaid | 不支持 | 不支持 |

---

## Mermaid 输出

Bubble chart 不支持 Mermaid 格式（Mermaid 无气泡图语法）。如果用户请求 Mermaid 格式，告知限制并建议 HTML 或 SVG 格式。
