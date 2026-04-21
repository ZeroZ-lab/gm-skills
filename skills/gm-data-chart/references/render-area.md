# 面积图渲染规则 (Area Chart Rendering Rules)

本参考文档定义了 area chart 的完整渲染流程，包含坐标公式和 worked example。LLM 在 Step 2 生成 SVG 输出时必须遵循这些规则。

---

## 渲染架构

Area chart 采用 **混合渲染模式**：

| 层次 | 技术 | 元素 |
|------|------|------|
| 数据图形 | SVG 原生元素 | `<path>`（面积区域）、`<line>`（坐标轴、网格线） |
| 文字区域 | foreignObject + CSS | 标题、轴标签、轴标题、图例 |

**为什么这样分**：面积坐标 = `valueToY(value)` 配合 X 轴等间距分布，这是简单比例运算，LLM 可以可靠计算。文字对齐、换行交给 CSS。

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
基础高度 = max(300, 80 + numDataPoints * heightPerPoint)

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

## 逐步渲染流程

### Step A：读取数据

从 JSON 中读取：
- `series[].data[].label` — 类别标签
- `series[].data[].value` — 数值
- `axis.y.ticks` — Nice Numbers 预计算的刻度数组
- `variant` — overlaid 或 stacked
- `opacity` — 面积填充透明度（默认 0.3）
- `smooth` — 是否使用贝塞尔曲线（默认 false）

### Step B：计算坐标

```
numDataPoints = series[0].data.length    （数据点数量）
numSeries = series.length                （系列数量）
```

**X 轴间距（edge-to-edge，与 line chart 相同）**：

```
pointX(g) = plotX + g * (plotWidth / (numDataPoints - 1))
```

注意：与 bar chart 的分组槽位不同，area chart 首尾数据点紧贴绘图区域边缘。

**Y 轴映射**：

```
minTick = axis.y.ticks[0]
maxTick = axis.y.ticks[axis.y.ticks.length - 1]
tickRange = maxTick - minTick

valueToY(value) = plotY + plotHeight - ((value - minTick) / tickRange) * plotHeight
```

### Step C：绘制网格线

参考 `axis-and-grid.md`。对每个 tick 值画水平虚线：

```svg
<line x1="{plotX}" y1="{tickY}" x2="{plotX + plotWidth}" y2="{tickY}" class="grid-line" />
```

其中 `tickY = valueToY(tickValue)`。

### Step D：绘制坐标轴

```svg
<!-- Y 轴 -->
<line x1="{plotX}" y1="{plotY}" x2="{plotX}" y2="{plotY + plotHeight}" class="axis-line" />

<!-- X 轴 -->
<line x1="{plotX}" y1="{plotY + plotHeight}" x2="{plotX + plotWidth}" y2="{plotY + plotHeight}" class="axis-line" />
```

### Step E：绘制面积区域（SVG `<path>`）

#### Overlaid 模式（默认）

每个系列画一个从基线到数据点的闭合区域：

```
baselineY = valueToY(minTick)

For each series s (0..numSeries-1):
  For each data point p (0..numDataPoints-1):
    x[p] = pointX(p)
    y[p] = valueToY(series[s].data[p].value)

  path = "M {x0},{baselineY}
          L {x0},{y0} L {x1},{y1} ... L {xn},{yn}
          L {xn},{baselineY}
          Z"

  <path d="{path}" fill="{color}" fill-opacity="{opacity}"
        stroke="{color}" stroke-width="2" class="area-fill" />
```

**颜色**：`color` 通过 `color-palettes.md` 的规则确定。未指定时使用 `palette[s % 10]`。

#### Stacked 模式

**Step 1 特殊处理**：Nice Numbers 算法应用于累计最大值：

```
cumulativeMax = max over all s,p of sum(series[0..s].data[p].value)
```

Nice Numbers 运行在 `cumulativeMax` 上，将结果 ticks 存入 `axis.y.ticks`。

**累计值计算**：

```
For each series s (0..numSeries-1):
  for each point p (0..numDataPoints-1):
    cumulativeY[s][p] = sum(series[0..s].data[p].value)
```

**渲染顺序**：从上往下绘制（series N-1 先画，series 0 最后画）：

```
Draw order: s = numSeries-1 down to 0

For series s:
  topEdge[p]    = valueToY(cumulativeY[s][p])
  bottomEdge[p] = valueToY(cumulativeY[s-1][p])   // s=0 时 bottomEdge[p] = baselineY

  path = "M {x0},{bottomEdge[0]}
          L {x0},{topEdge[0]} L {x1},{topEdge[1]} ... L {xn},{topEdge[n]}
          L {xn},{bottomEdge[n]} ... L {x0},{bottomEdge[0]}
          Z"

  <path d="{path}" fill="{color}" fill-opacity="{opacity}"
        stroke="{color}" stroke-width="2" class="area-fill" />
```

#### Catmull-Rom Smooth 模式

当 `smooth: true` 时，面积顶边使用 Catmull-Rom → Bezier 控制点转换（与 line chart 相同的公式）：

```
// 创建虚拟端点（phantom points）用于边界处理
P[-1] = 2 * P[0] - P[1]      // 镜像首点
P[n] = 2 * P[n-1] - P[n-2]   // 镜像尾点

For each segment i (0..n-2):
  cp1x = x[i] + (x[i+1] - x[i-1]) / 6
  cp1y = y[i] + (y[i+1] - y[i-1]) / 6
  cp2x = x[i+1] - (x[i+2] - x[i]) / 6
  cp2y = y[i+1] - (y[i+2] - y[i]) / 6
```

注意：`i-1` 在 `i=0` 时使用 phantom point `P[-1]`，`i+2` 在 `i=n-2` 时使用 phantom point `P[n]`。

**Overlaid smooth path**：

```
path = "M {x0},{baselineY}
        L {x0},{y0}
        C {cp1x_0},{cp1y_0} {cp2x_0},{cp2y_0} {x1},{y1}
        C {cp1x_1},{cp1y_1} {cp2x_1},{cp2y_1} {x2},{y2}
        ...
        L {xn},{baselineY}
        Z"
```

**Stacked smooth path**：对 topEdge 和 bottomEdge 分别用 Catmull-Rom 生成 Bezier 曲线段，连接方式与直线版类似，但使用 C 命令替代 L 命令。

### Step F：绘制轴标签（foreignObject + CSS）

**Y 轴刻度值**：

```svg
<foreignObject x="0" y="{tickY - 10}" width="{CHART_PADDING_LEFT - 10}" height="20">
  <div xmlns="http://www.w3.org/1999/xhtml" class="tick-label" style="text-align: right;">
    {tickValue}
  </div>
</foreignObject>
```

**X 轴标签（edge-to-edge 分布）**：

```svg
<foreignObject x="{pointX(g) - 40}" y="{plotY + plotHeight + 8}" width="80" height="40">
  <div xmlns="http://www.w3.org/1999/xhtml" class="tick-label" style="text-align: center;">
    {label}
  </div>
</foreignObject>
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

**输入**：网站流量 JSON（overlaid 模式）

```json
{
  "series": [
    { "name": "直接访问", "data": [
      {"label": "1月", "value": 200}, {"label": "2月", "value": 220},
      {"label": "3月", "value": 250}, {"label": "4月", "value": 230},
      {"label": "5月", "value": 260}, {"label": "6月", "value": 280}
    ]},
    { "name": "社交媒体", "data": [
      {"label": "1月", "value": 80}, {"label": "2月", "value": 100},
      {"label": "3月", "value": 120}, {"label": "4月", "value": 110},
      {"label": "5月", "value": 130}, {"label": "6月", "value": 150}
    ]}
  ],
  "axis": { "y": { "ticks": [0, 50, 100, 150, 200, 250, 300] } },
  "variant": "overlaid",
  "opacity": 0.3
}
```

**计算**：

```
numDataPoints = 6, numSeries = 2
totalHeight = max(300, 80 + 6 * 35) = 300
totalWidth = max(500, 6 * 100) = 600 → clamped to 500
plotWidth = 500 - 70 - 40 = 390
plotHeight = 300 - 60 - 60 = 180
plotX = 70, plotY = 60

minTick = 0, maxTick = 300, tickRange = 300

// X 轴间距（edge-to-edge）
pointX(0) = 70 + 0 * (390 / 5) = 70
pointX(1) = 70 + 1 * 78 = 148
pointX(2) = 70 + 2 * 78 = 226
pointX(3) = 70 + 3 * 78 = 304
pointX(4) = 70 + 4 * 78 = 382
pointX(5) = 70 + 5 * 78 = 460

// Y 轴映射
valueToY(0)   = 60 + 180 - (0/300)*180   = 240  (baselineY)
valueToY(50)  = 60 + 180 - (50/300)*180  = 210
valueToY(100) = 60 + 180 - (100/300)*180 = 180
valueToY(150) = 60 + 180 - (150/300)*180 = 150
valueToY(200) = 60 + 180 - (200/300)*180 = 120
valueToY(250) = 60 + 180 - (250/300)*180 = 90
valueToY(300) = 60 + 180 - (300/300)*180 = 60
```

**Series 1（直接访问）Y 坐标**：

| 数据点 | value | pointX | valueToY |
|--------|-------|--------|----------|
| 1月 | 200 | 70 | 120 |
| 2月 | 220 | 148 | 108 |
| 3月 | 250 | 226 | 90 |
| 4月 | 230 | 304 | 102 |
| 5月 | 260 | 382 | 84 |
| 6月 | 280 | 460 | 72 |

**Area path（Series 1）**：

```
baselineY = 240
path = "M 70,240 L 70,120 L 148,108 L 226,90 L 304,102 L 382,84 L 460,72 L 460,240 Z"
```

**Series 2（社交媒体）Y 坐标**：

| 数据点 | value | pointX | valueToY |
|--------|-------|--------|----------|
| 1月 | 80 | 70 | 192 |
| 2月 | 100 | 148 | 180 |
| 3月 | 120 | 226 | 168 |
| 4月 | 110 | 304 | 174 |
| 5月 | 130 | 382 | 162 |
| 6月 | 150 | 460 | 150 |

**Area path（Series 2）**：

```
baselineY = 240
path = "M 70,240 L 70,192 L 148,180 L 226,168 L 304,174 L 382,162 L 460,150 L 460,240 Z"
```

**颜色**：dark-professional → Palette B → `palette[0]` = `#6366f1`, `palette[1]` = `#f472b6`

**SVG 输出**：

```svg
<!-- Series 1: 直接访问 -->
<path d="M 70,240 L 70,120 L 148,108 L 226,90 L 304,102 L 382,84 L 460,72 L 460,240 Z"
      fill="#6366f1" fill-opacity="0.3" stroke="#6366f1" stroke-width="2" class="area-fill" />

<!-- Series 2: 社交媒体 -->
<path d="M 70,240 L 70,192 L 148,180 L 226,168 L 304,174 L 382,162 L 460,150 L 460,240 Z"
      fill="#f472b6" fill-opacity="0.3" stroke="#f472b6" stroke-width="2" class="area-fill" />
```

---

## CSS 类

| 类名 | 用途 | 默认样式 |
|------|------|----------|
| `.area-fill` | 面积填充路径 | `opacity` 由 `fill-opacity` 属性控制，不使用 CSS opacity |
| `.axis-line` | 坐标轴线 | `stroke: #64748b; stroke-width: 1.5` |
| `.grid-line` | 网格线 | `stroke: rgba(255,255,255,0.06); stroke-dasharray: 4,4` |
| `.tick-label` | 刻度标签 | `fill: #94a3b8; font-size: 11px` |
| `.axis-title` | 轴标题 | `fill: #f1f5f9; font-size: 13px; font-weight: 600` |

以上为 dark-professional 风格的默认样式，其他风格由对应模板定义。
