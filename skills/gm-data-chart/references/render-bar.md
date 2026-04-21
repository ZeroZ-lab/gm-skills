# 柱状图渲染规则 (Bar Chart Rendering Rules)

本参考文档定义了 bar chart 的完整渲染流程，包含坐标公式和 worked example。LLM 在 Step 2 生成 SVG 输出时必须遵循这些规则。

---

## 渲染架构

Bar chart 采用 **混合渲染模式**：

| 层次 | 技术 | 元素 |
|------|------|------|
| 数据图形 | SVG 原生元素 | `<rect>`（柱子）、`<line>`（坐标轴、网格线） |
| 文字区域 | foreignObject + CSS | 标题、轴标签、轴标题、图例、数据标签 |

**为什么这样分**：柱子高度 = `value / maxTick * plotHeight`，这是简单比例运算，LLM 可以可靠计算。文字对齐、换行、旋转交给 CSS。

---

## 布局常量

| 名称 | 值 | 用途 |
|------|-----|------|
| `CHART_PADDING_TOP` | 60px | 标题区域 |
| `CHART_PADDING_RIGHT` | 40px | 右侧留白 |
| `CHART_PADDING_BOTTOM` | 60px | X 轴标签区域 |
| `CHART_PADDING_LEFT` | 70px | Y 轴标签区域 |
| `BAR_GAP_RATIO` | 0.3 | 同组柱子间距占比 |
| `BAR_GROUP_GAP_RATIO` | 0.5 | 分组间距占比 |

### 高度计算

```
基础高度 = max(300, 80 + numDataPoints * heightPerBar)

heightPerBar by density:
  compact  = 25px
  normal   = 35px
  spacious = 45px
```

### 宽度

```
totalWidth = clamp(CHART_MIN_WIDTH, max(500, numDataPoints * 100), CHART_MAX_WIDTH)
即 min=500, max=900, 默认按每组 100px 估算
```

### 绘图区域

```
plotWidth  = totalWidth - CHART_PADDING_LEFT - CHART_PADDING_RIGHT
plotHeight = totalHeight - CHART_PADDING_TOP - CHART_PADDING_BOTTOM
plotX = CHART_PADDING_LEFT
plotY = CHART_PADDING_TOP
```

---

## 逐步渲染流程

### Step A：读取数据

从 JSON 中读取：
- `series[].data[].label` — 类别标签
- `series[].data[].value` — 数值
- `axis.y.ticks` — Nice Numbers 预计算的刻度数组
- `direction` — vertical 或 horizontal
- `variant` — grouped 或 stacked

### Step B：计算柱子几何

```
numGroups = series[0].data.length    （数据点数量）
numSeries = series.length            （系列数量）
```

**Grouped 模式（默认）**：

```
groupWidth = plotWidth / numGroups
groupGap = groupWidth * BAR_GROUP_GAP_RATIO
usableGroupWidth = groupWidth - groupGap
barWidth = usableGroupWidth / numSeries
barGap = barWidth * BAR_GAP_RATIO
actualBarWidth = barWidth - barGap
```

**Stacked 模式**：

```
barWidth = (plotWidth / numGroups) * (1 - BAR_GAP_RATIO)
groupGap = (plotWidth / numGroups) * BAR_GAP_RATIO
```

### Step C：绘制网格线

参考 `axis-and-grid.md`。对每个 tick 值画水平虚线：

```svg
<line x1="{plotX}" y1="{tickY}" x2="{plotX + plotWidth}" y2="{tickY}" class="grid-line" />
```

其中 `tickY = valueToY(tickValue)`：

```
tickRange = maxTick - minTick
valueToY(value) = plotY + plotHeight - ((value - minTick) / tickRange) * plotHeight
```

### Step D：绘制坐标轴

```svg
<!-- Y 轴 -->
<line x1="{plotX}" y1="{plotY}" x2="{plotX}" y2="{plotY + plotHeight}" class="axis-line" />

<!-- X 轴 -->
<line x1="{plotX}" y1="{plotY + plotHeight}" x2="{plotX + plotWidth}" y2="{plotY + plotHeight}" class="axis-line" />
```

如果数据包含负值，额外画基线（value=0）：

```svg
<line x1="{plotX}" y1="{baselineY}" x2="{plotX + plotWidth}" y2="{baselineY}" class="axis-line" style="stroke-width: 1.5" />
```

### Step E：绘制柱子（SVG `<rect>`）

**Grouped 模式**：

```
For each group g (0..numGroups-1):
  For each series s (0..numSeries-1):
    value = series[s].data[g].value
    barPixelHeight = abs((value - minTick) / tickRange * plotHeight)

    If value >= 0:
      barY = valueToY(value)
    Else:
      barY = valueToY(0)   // 从 0 基线向下

    barX = plotX + g * groupWidth + groupGap/2 + s * barWidth + barGap/2

    <rect x="{barX}" y="{barY}" width="{actualBarWidth}" height="{barPixelHeight}"
          rx="2" fill="{paletteColor}" class="bar" />
```

**Stacked 模式**：

```
For each group g (0..numGroups-1):
  cumulativePositive = 0
  cumulativeNegative = 0

  For each series s (0..numSeries-1):
    value = series[s].data[g].value

    If value >= 0:
      barY = valueToY(cumulativePositive + value)
      barHeight = valueToY(cumulativePositive) - barY
      cumulativePositive += value
    Else:
      barY = valueToY(cumulativeNegative)
      barHeight = valueToY(cumulativeNegative + value) - barY
      cumulativeNegative += value

    barX = plotX + g * (plotWidth / numGroups) + groupGap/2

    <rect x="{barX}" y="{barY}" width="{barWidth}" height="{barHeight}"
          rx="2" fill="{paletteColor}" class="bar" />
```

**颜色**：`paletteColor` 通过 `color-palettes.md` 的规则确定。未指定时使用 `palette[s % 10]`。

### Step F：绘制轴标签（foreignObject + CSS）

**Y 轴刻度值**：

```svg
<foreignObject x="0" y="{tickY - 10}" width="{CHART_PADDING_LEFT - 10}" height="20">
  <div xmlns="http://www.w3.org/1999/xhtml" class="tick-label" style="text-align: right;">
    {tickValue}
  </div>
</foreignObject>
```

**X 轴分组标签**：

```svg
<foreignObject x="{groupCenterX - groupWidth/2}" y="{plotY + plotHeight + 8}"
               width="{groupWidth}" height="40">
  <div xmlns="http://www.w3.org/1999/xhtml" class="tick-label" style="text-align: center;">
    {label}
  </div>
</foreignObject>
```

长标签（宽度 > groupWidth * 0.8）时旋转 -45°：

```
style="text-align: center; transform: rotate(-45deg); transform-origin: top center;"
```

### Step G：绘制轴标题（foreignObject + CSS）

```svg
<!-- Y 轴标题（旋转） -->
<foreignObject x="0" y="{plotY}" width="20" height="{plotHeight}">
  <div xmlns="http://www.w3.org/1999/xhtml" class="axis-title"
       style="transform: rotate(-90deg); transform-origin: center; display: flex; align-items: center; justify-content: center; height: 100%;">
    {axis.y.label}
  </div>
</foreignObject>

<!-- X 轴标题 -->
<foreignObject x="{plotX}" y="{plotY + plotHeight + 40}" width="{plotWidth}" height="20">
  <div xmlns="http://www.w3.org/1999/xhtml" class="axis-title" style="text-align: center;">
    {axis.x.label}
  </div>
</foreignObject>
```

### Step H：绘制图例（foreignObject + CSS）

```svg
<foreignObject x="{plotX}" y="{plotY - 35}" width="{plotWidth}" height="30">
  <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: center; justify-content: center; gap: 16px;">
    <!-- 每个系列一个图例项 -->
    <div style="display: flex; align-items: center; gap: 6px;">
      <div style="width: 12px; height: 12px; background: {color}; border-radius: 2px;"></div>
      <span class="tick-label">{seriesName}</span>
    </div>
  </div>
</foreignObject>
```

### Step I：绘制标题和副标题

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

**输入**：季度营收 JSON

```json
{
  "series": [{ "name": "营收", "data": [
    {"label": "Q1", "value": 120}, {"label": "Q2", "value": 150},
    {"label": "Q3", "value": 180}, {"label": "Q4", "value": 200}
  ]}],
  "axis": { "y": { "ticks": [0, 50, 100, 150, 200] } }
}
```

**计算**：

```
numGroups = 4, numSeries = 1
totalHeight = max(300, 80 + 4 * 35) = 300
totalWidth = max(500, 4 * 100) = 500
plotWidth = 500 - 70 - 40 = 390
plotHeight = 300 - 60 - 60 = 180
plotX = 70, plotY = 60

groupWidth = 390 / 4 = 97.5
groupGap = 97.5 * 0.5 = 48.75
usableGroupWidth = 97.5 - 48.75 = 48.75
barWidth = 48.75 / 1 = 48.75
barGap = 48.75 * 0.3 = 14.625
actualBarWidth = 48.75 - 14.625 ≈ 34

minTick = 0, maxTick = 200, tickRange = 200

valueToY(0)   = 60 + 180 - (0/200)*180   = 240
valueToY(50)  = 60 + 180 - (50/200)*180  = 195
valueToY(100) = 60 + 180 - (100/200)*180 = 150
valueToY(150) = 60 + 180 - (150/200)*180 = 105
valueToY(200) = 60 + 180 - (200/200)*180 = 60
```

**柱子坐标**：

| 数据点 | value | barX | barY | barWidth | barHeight |
|--------|-------|------|------|----------|-----------|
| Q1 | 120 | 70 + 0*97.5 + 24.375 + 7.3 ≈ **101.7** | valueToY(120) = **132** | **34** | valueToY(0) - valueToY(120) = 240 - 132 = **108** |
| Q2 | 150 | 70 + 1*97.5 + 24.375 + 7.3 ≈ **199.2** | valueToY(150) = **105** | **34** | 240 - 105 = **135** |
| Q3 | 180 | 70 + 2*97.5 + 24.375 + 7.3 ≈ **296.7** | valueToY(180) = **78** | **34** | 240 - 78 = **162** |
| Q4 | 200 | 70 + 3*97.5 + 24.375 + 7.3 ≈ **394.2** | valueToY(200) = **60** | **34** | 240 - 60 = **180** |

**颜色**：dark-professional → Palette B → `palette[0]` = `#6366f1`

---

## 水平方向变体

当 `direction: "horizontal"` 时：

- 柱子从左向右生长（而非从下向上）
- X 轴变为数值轴，Y 轴变为类别轴
- 坐标映射交换 X/Y：

```
valueToX(value) = plotX + ((value - minTick) / tickRange) * plotWidth
barX = plotX（或从 0 基线开始）
barWidth = valueToX(value) - valueToX(0)
barY = plotY + g * groupHeight + groupGap/2 + s * barHeight
barHeight = actualBarHeight（类别轴上的高度）
```

- 标签交换：类别标签在 Y 轴（左），数值标签在 X 轴（下）

---

## 堆叠变体

当 `variant: "stacked"` 时：

- 同一组内的柱子垂直堆叠
- 正值从基线向上累加，负值从基线向下累加
- 颜色：每个系列使用自己的调色板颜色
- 图例必须显示所有系列名称

---

## 数据标签（可选）

如果用户要求在柱子顶部显示数值，使用 foreignObject：

```svg
<foreignObject x="{barX - 10}" y="{barY - 22}" width="{actualBarWidth + 20}" height="20">
  <div xmlns="http://www.w3.org/1999/xhtml" class="tick-label"
       style="text-align: center; font-size: 10px;">
    {value}
  </div>
</foreignObject>
```
