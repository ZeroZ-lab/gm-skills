# 折线图渲染规则 (Line Chart Rendering Rules)

本参考文档定义了 line chart 的完整渲染流程，包含坐标公式和 worked example。LLM 在 Step 2 生成 SVG 输出时必须遵循这些规则。

---

## 渲染架构

Line chart 采用 **混合渲染模式**：

| 层次 | 技术 | 元素 |
|------|------|------|
| 数据图形 | SVG 原生元素 | `<polyline>` / `<path>`（折线/曲线）、`<circle>` / `<rect>` / `<polygon>`（数据点标记）、`<line>`（坐标轴、网格线） |
| 文字区域 | foreignObject + CSS | 标题、轴标签、轴标题、图例 |

**为什么这样分**：折线坐标 = `valueToY(value)` + `pointX(index)` 的简单运算，LLM 可以可靠计算。文字对齐、换行交给 CSS。

---

## 布局常量

| 名称 | 值 | 用途 |
|------|-----|------|
| `CHART_PADDING_TOP` | 60px | 标题区域 |
| `CHART_PADDING_RIGHT` | 40px | 右侧留白 |
| `CHART_PADDING_BOTTOM` | 60px | X 轴标签区域 |
| `CHART_PADDING_LEFT` | 70px | Y 轴标签区域 |

### 高度计算

```
totalHeight = max(300, 80 + numDataPoints * heightPerPoint)

heightPerPoint by density:
  compact  = 25px
  normal   = 35px
  spacious = 45px
```

### 宽度

```
totalWidth = clamp(CHART_MIN_WIDTH, max(500, numDataPoints * 100), CHART_MAX_WIDTH)
即 min=500, max=900, 默认按每点 100px 估算
```

### 绘图区域

```
plotWidth  = totalWidth - CHART_PADDING_LEFT - CHART_PADDING_RIGHT
plotHeight = totalHeight - CHART_PADDING_TOP - CHART_PADDING_BOTTOM
plotX = CHART_PADDING_LEFT
plotY = CHART_PADDING_TOP
```

---

## X 轴间距（EDGE-TO-EDGE，与 bar 不同）

**关键区别**：Line chart 使用 **edge-to-edge 分布**，数据点均匀分布在 plotWidth 的两端之间，首尾点贴近轴线。Bar chart 使用 **分组槽位分布**，每个柱子居中在自己的槽位内。

```
// Line/Area 使用 edge-to-edge 分布
pointX(g) = plotX + g * (plotWidth / (numDataPoints - 1))

// 对比 Bar 使用分组槽位分布
// groupCenterX = plotX + g * groupWidth + groupWidth / 2
```

**原因**：折线图需要展示趋势的连续性，首尾数据点应贴近绘图区域边界。

---

## 折线绘制

### 直线模式（`smooth: false`）

使用 SVG `<polyline>` 连接所有数据点：

```svg
<polyline points="{x0},{y0} {x1},{y1} ... {xn},{yn}"
          fill="none" stroke="{color}" stroke-width="{lineWidth}"
          stroke-linejoin="round" stroke-linecap="round"
          class="line-path" />
```

如果 `lineStyle: "dashed"`，添加 `stroke-dasharray="8,4"`。

### 曲线模式（`smooth: true`）

使用 Catmull-Rom → Bezier 控制点转换，生成 `<path>` 的 C（cubic Bezier）命令：

```
// 1. 创建虚拟端点（phantom points）用于边界处理
P[-1] = 2 * P[0] - P[1]      // 镜像首点
P[n]  = 2 * P[n-1] - P[n-2]  // 镜像尾点

// 2. 对每个线段 i (0..n-2) 计算控制点
For each segment i (0..n-2):
  cp1x = x[i] + (x[i+1] - x[i-1]) / 6
  cp1y = y[i] + (y[i+1] - y[i-1]) / 6
  cp2x = x[i+1] - (x[i+2] - x[i]) / 6
  cp2y = y[i+1] - (y[i+2] - y[i]) / 6

// 3. 生成 path
path = "M {x0},{y0}
        C {cp1x_0},{cp1y_0} {cp2x_0},{cp2y_0} {x1},{y1}
        C {cp1x_1},{cp1y_1} {cp2x_1},{cp2y_1} {x2},{y2}
        ..."
```

注意：`i-1` 在 `i=0` 时使用 phantom point `P[-1]`，`i+2` 在 `i=n-2` 时使用 phantom point `P[n]`。

```svg
<path d="{path}"
      fill="none" stroke="{color}" stroke-width="{lineWidth}"
      stroke-linejoin="round" stroke-linecap="round"
      class="line-path" />
```

---

## 数据点标记

根据 `dataPointShape` 属性绘制标记，使用 `.data-dot` CSS class：

```svg
<!-- circle (default) -->
<circle cx="{x}" cy="{y}" r="4" fill="{color}" stroke="white" stroke-width="1.5" class="data-dot" />

<!-- square -->
<rect x="{x - 3.5}" y="{y - 3.5}" width="7" height="7" fill="{color}" class="data-dot" />

<!-- diamond -->
<polygon points="{x},{y-5} {x+5},{y} {x},{y+5} {x-5},{y}" fill="{color}" class="data-dot" />

<!-- none: 不绘制标记 -->
```

---

## 网格线

**与 bar 的区别**：Line chart 默认 `axis.y.gridLines = true`（bar 默认 false）。

参考 `axis-and-grid.md`。对每个 tick 值（跳过 minTick，即最底部的刻度不画网格线，因为它与 X 轴重合）画水平虚线：

```svg
<line x1="{plotX}" y1="{tickY}" x2="{plotX + plotWidth}" y2="{tickY}" class="grid-line" />
```

其中 `tickY = valueToY(tickValue)`：

```
minTick = axis.y.ticks[0]
maxTick = axis.y.ticks[axis.y.ticks.length - 1]
tickRange = maxTick - minTick
valueToY(value) = plotY + plotHeight - ((value - minTick) / tickRange) * plotHeight
```

---

## 逐步渲染流程

### Step A：读取数据

从 JSON 中读取：
- `series[].data[].label` — 类别标签（所有系列的 label 必须一致）
- `series[].data[].value` — 数值
- `axis.y.ticks` — Nice Numbers 预计算的刻度数组
- `smooth` — 是否使用曲线模式
- `series[].lineWidth` — 线宽
- `series[].lineStyle` — 线型（solid / dashed）
- `series[].dataPointShape` — 数据点形状

### Step B：计算坐标

```
numDataPoints = series[0].data.length
numSeries = series.length

minTick = axis.y.ticks[0]
maxTick = axis.y.ticks[axis.y.ticks.length - 1]
tickRange = maxTick - minTick

// Edge-to-edge X 间距
step = plotWidth / (numDataPoints - 1)

For each series s:
  For each data point g:
    pointX[g] = plotX + g * step
    pointY[g] = valueToY(series[s].data[g].value)
```

### Step C：绘制网格线

对每个 Y 轴刻度值（跳过 minTick）画水平虚线：

```svg
<line x1="{plotX}" y1="{tickY}" x2="{plotX + plotWidth}" y2="{tickY}" class="grid-line" />
```

### Step D：绘制坐标轴

```svg
<!-- Y 轴 -->
<line x1="{plotX}" y1="{plotY}" x2="{plotX}" y2="{plotY + plotHeight}" class="axis-line" />

<!-- X 轴 -->
<line x1="{plotX}" y1="{plotY + plotHeight}" x2="{plotX + plotWidth}" y2="{plotY + plotHeight}" class="axis-line" />
```

### Step E：绘制折线

**直线模式**（`smooth: false`）：

```svg
<polyline points="{x0},{y0} {x1},{y1} ... {xn},{yn}"
          fill="none" stroke="{color}" stroke-width="{lineWidth}"
          stroke-linejoin="round" stroke-linecap="round"
          class="line-path" />
```

**曲线模式**（`smooth: true`）：

按 Catmull-Rom → Bezier 公式计算控制点，生成 `<path>`。

**颜色**：`paletteColor` 通过 `color-palettes.md` 的规则确定。未指定时使用 `palette[s % 10]`。

### Step F：绘制数据点标记

根据 `dataPointShape` 在每个数据点绘制标记。如果为 `"none"` 则跳过此步骤。

### Step G：绘制轴标签（foreignObject + CSS）

**Y 轴刻度值**：

```svg
<foreignObject x="0" y="{tickY - 10}" width="{CHART_PADDING_LEFT - 10}" height="20">
  <div xmlns="http://www.w3.org/1999/xhtml" class="tick-label" style="text-align: right;">
    {tickValue}
  </div>
</foreignObject>
```

**X 轴类别标签**：

使用 edge-to-edge 间距，每个标签居中在对应数据点下方：

```svg
<foreignObject x="{pointX - labelWidth/2}" y="{plotY + plotHeight + 8}"
               width="{labelWidth}" height="20">
  <div xmlns="http://www.w3.org/1999/xhtml" class="tick-label" style="text-align: center;">
    {label}
  </div>
</foreignObject>
```

其中 `labelWidth = step`（X 轴间距），且最小为 40px。

### Step H：绘制轴标题（foreignObject + CSS）

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

### Step I：绘制图例和标题

**图例**（foreignObject + CSS）：

```svg
<foreignObject x="{plotX}" y="{plotY - 35}" width="{plotWidth}" height="30">
  <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: center; justify-content: center; gap: 16px;">
    <!-- 每个系列一个图例项 -->
    <div style="display: flex; align-items: center; gap: 6px;">
      <div style="width: 20px; height: 3px; background: {color};"></div>
      <span class="tick-label">{seriesName}</span>
    </div>
  </div>
</foreignObject>
```

**标题和副标题**：

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

## Mermaid 输出

Line chart 使用 `xychart-beta` 语法：

```mermaid
xychart-beta
    title "{title}"
    x-axis [{label1}, {label2}, ...]
    y-axis "{axis.y.label}" {minTick} --> {maxTick}
    line [{value1}, {value2}, ...]
    line [{value1b}, {value2b}, ...]
```

**Mermaid 标签转义规则**：
- `"` 转义为 `#quot;`
- 标签中的换行符、`:` 字符需移除或替换为空格
- 插入 Mermaid 语法前验证 value 为有限数字

---

## Worked Example

**输入 JSON**：月度活跃用户

```json
{
  "diagramType": "line",
  "title": "月度活跃用户",
  "series": [
    { "name": "用户数", "data": [
      {"label": "1月", "value": 120},
      {"label": "2月", "value": 180},
      {"label": "3月", "value": 150},
      {"label": "4月", "value": 220}
    ]}
  ],
  "axis": {
    "y": { "ticks": [0, 50, 100, 150, 200, 250] }
  }
}
```

**计算**：

```
numDataPoints = 4, numSeries = 1
totalHeight = max(300, 80 + 4 * 35) = 300
totalWidth = max(500, 4 * 100) = 500
plotWidth = 500 - 70 - 40 = 390
plotHeight = 300 - 60 - 60 = 180
plotX = 70, plotY = 60

// Edge-to-edge X 间距（与 bar 的分组槽位不同）
step = 390 / (4 - 1) = 130
pointX(0) = 70 + 0 * 130 = 70
pointX(1) = 70 + 1 * 130 = 200
pointX(2) = 70 + 2 * 130 = 330
pointX(3) = 70 + 3 * 130 = 400

// Y 轴映射
minTick = 0, maxTick = 250, tickRange = 250
valueToY(0)   = 60 + 180 - (0/250)*180     = 240
valueToY(50)  = 60 + 180 - (50/250)*180    = 204
valueToY(100) = 60 + 180 - (100/250)*180   = 168
valueToY(120) = 60 + 180 - (120/250)*180   = 60 + 180 - 86.4 = 153.6
valueToY(150) = 60 + 180 - (150/250)*180   = 60 + 180 - 108  = 132
valueToY(180) = 60 + 180 - (180/250)*180   = 60 + 180 - 129.6 = 110.4
valueToY(200) = 60 + 180 - (200/250)*180   = 60 + 180 - 144  = 96
valueToY(220) = 60 + 180 - (220/250)*180   = 60 + 180 - 158.4 = 81.6
valueToY(250) = 60 + 180 - (250/250)*180   = 60

// 折线（直线模式）
points = "70,153.6 200,110.4 330,132 400,81.6"

// 数据点标记
circle at (70, 153.6), (200, 110.4), (330, 132), (400, 81.6)
```

**网格线坐标**（跳过 minTick=0，因为它与 X 轴重合）：

| tick | valueToY | 备注 |
|------|----------|------|
| 50   | 204      | 网格线 |
| 100  | 168      | 网格线 |
| 150  | 132      | 网格线 |
| 200  | 96       | 网格线 |
| 250  | 60       | 网格线（顶部边界） |

**Catmull-Rom 平滑模式**（如 `smooth: true`）：

```
Phantom points:
P[-1] = 2 * P[0] - P[1] = (2*70 - 200, 2*153.6 - 110.4) = (-60, 196.8)
P[4]  = 2 * P[3] - P[2] = (2*400 - 330, 2*81.6 - 132) = (470, 31.2)

// Segment 0 (P0→P1): i=0, use P[-1] for i-1
cp1x = 70 + (200 - (-60)) / 6 = 70 + 43.3 = 113.3
cp1y = 153.6 + (110.4 - 196.8) / 6 = 153.6 - 14.4 = 139.2
cp2x = 200 - (330 - 70) / 6 = 200 - 43.3 = 156.7
cp2y = 110.4 - (132 - 153.6) / 6 = 110.4 + 3.6 = 114.0

// Segment 1 (P1→P2): i=1
cp1x = 200 + (330 - 70) / 6 = 200 + 43.3 = 243.3
cp1y = 110.4 + (132 - 153.6) / 6 = 110.4 - 3.6 = 106.8
cp2x = 330 - (400 - 200) / 6 = 330 - 33.3 = 296.7
cp2y = 132 - (81.6 - 110.4) / 6 = 132 + 4.8 = 136.8

// Segment 2 (P2→P3): i=2, use P[4] for i+2
cp1x = 330 + (400 - 200) / 6 = 330 + 33.3 = 363.3
cp1y = 132 + (81.6 - 110.4) / 6 = 132 - 4.8 = 127.2
cp2x = 400 - (470 - 330) / 6 = 400 - 23.3 = 376.7
cp2y = 81.6 - (31.2 - 132) / 6 = 81.6 + 16.8 = 98.4

path = "M 70,153.6
        C 113.3,139.2 156.7,114.0 200,110.4
        C 243.3,106.8 296.7,136.8 330,132
        C 363.3,127.2 376.7,98.4 400,81.6"
```

**颜色**：dark-professional → Palette B → `palette[0]` = `#6366f1`
