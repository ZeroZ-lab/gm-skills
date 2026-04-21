# 散点图渲染规则 (Scatter Chart Rendering Rules)

本参考文档定义了 scatter chart 的完整渲染流程，包含坐标公式和 worked example。LLM 在 Step 2 生成 SVG 输出时必须遵循这些规则。

---

## 渲染架构

Scatter chart 采用 **混合渲染模式**：

| 层次 | 技术 | 元素 |
|------|------|------|
| 数据图形 | SVG 原生元素 | `<circle>`, `<rect>`, `<polygon>`（数据点）、`<line>`（坐标轴、网格线） |
| 文字区域 | foreignObject + CSS | 标题、轴标签、轴标题、图例、数据点标签 |

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
totalWidth = totalHeight = 500（正方形，scatter 推荐等比例）
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
- `series[].data[].label` — 可选的数据点标签
- `series[].pointShape` — 数据点形状
- `series[].pointSize` — 数据点大小
- `axis.x.ticks` — Nice Numbers 预计算的 X 轴刻度数组
- `axis.y.ticks` — Nice Numbers 预计算的 Y 轴刻度数组

### Step B：坐标映射（双轴线性映射）

Scatter chart 的 X 轴和 Y 轴都是数值轴，使用线性映射：

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

### Step C：绘制网格线

**X 轴和 Y 轴都默认显示网格线** (`gridLines: true`)。

Y 轴网格线（水平虚线，对每个 Y tick）：

```svg
<line x1="{plotX}" y1="{valueToY(tickValue)}" x2="{plotX + plotWidth}" y2="{valueToY(tickValue)}" class="grid-line" />
```

X 轴网格线（垂直虚线，对每个 X tick）：

```svg
<line x1="{valueToX(tickValue)}" y1="{plotY}" x2="{valueToX(tickValue)}" y2="{plotY + plotHeight}" class="grid-line" />
```

### Step D：绘制坐标轴

```svg
<!-- Y 轴 -->
<line x1="{plotX}" y1="{plotY}" x2="{plotX}" y2="{plotY + plotHeight}" class="axis-line" />

<!-- X 轴 -->
<line x1="{plotX}" y1="{plotY + plotHeight}" x2="{plotX + plotWidth}" y2="{plotY + plotHeight}" class="axis-line" />
```

### Step E：绘制数据点（SVG 图形元素）

所有数据点使用 `.scatter-point` CSS 类和 `fill-opacity="0.7"`。

**circle（圆形）**：

```svg
<circle cx="{valueToX(d.x)}" cy="{valueToY(d.y)}" r="{pointSize}"
        fill="{color}" fill-opacity="0.7" class="scatter-point" />
```

**square（方形）**：

```svg
<!-- size = pointSize -->
<rect x="{cx - size}" y="{cy - size}" width="{size * 2}" height="{size * 2}"
      fill="{color}" fill-opacity="0.7" class="scatter-point" />
```

**diamond（菱形）**：

```svg
<polygon points="{cx},{cy - size} {cx + size},{cy} {cx},{cy + size} {cx - size},{cy}"
         fill="{color}" fill-opacity="0.7" class="scatter-point" />
```

**triangle（三角形，向上）**：

```svg
<polygon points="{cx},{cy - size} {cx - size},{cy + size} {cx + size},{cy + size}"
         fill="{color}" fill-opacity="0.7" class="scatter-point" />
```

**颜色**：`color` 通过 `color-palettes.md` 的规则确定。未指定时使用 `palette[s % 10]`。

### Step F：绘制数据点标签（可选，foreignObject + CSS）

只有 `data[].label` 存在时才显示标签（避免拥挤）。标签放在点的右上方：

```svg
<foreignObject x="{cx + 6}" y="{cy - 18}" width="80" height="16">
  <div xmlns="http://www.w3.org/1999/xhtml" class="tick-label" style="font-size: 10px;">
    {d.label}
  </div>
</foreignObject>
```

### Step G：绘制轴标签（foreignObject + CSS）

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
<foreignObject x="{plotX}" y="{plotY + plotHeight + 35}" width="{plotWidth}" height="20">
  <div xmlns="http://www.w3.org/1999/xhtml" class="axis-title" style="text-align: center;">
    {axis.x.label}
  </div>
</foreignObject>
```

### Step I：绘制图例（foreignObject + CSS）

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

### Step J：绘制标题和副标题

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

**输入**：学习时间与考试成绩 JSON

```json
{
  "series": [
    {
      "name": "A班", "pointShape": "circle", "pointSize": 5,
      "data": [
        {"x": 2, "y": 65}, {"x": 3, "y": 70}, {"x": 5, "y": 80},
        {"x": 7, "y": 88}, {"x": 8, "y": 92}
      ]
    },
    {
      "name": "B班", "pointShape": "diamond", "pointSize": 5,
      "data": [
        {"x": 1, "y": 55}, {"x": 4, "y": 68}, {"x": 6, "y": 75},
        {"x": 7, "y": 82}, {"x": 9, "y": 95}
      ]
    }
  ],
  "axis": {
    "x": { "label": "学习时间（小时/天）", "ticks": [0, 2, 4, 6, 8, 10], "gridLines": true },
    "y": { "label": "考试成绩", "ticks": [50, 60, 70, 80, 90, 100], "gridLines": true }
  }
}
```

**计算**：

```
totalWidth = totalHeight = 500
plotWidth = 500 - 70 - 40 = 390
plotHeight = 500 - 60 - 60 = 380
plotX = 70, plotY = 60

xMinTick = 0, xMaxTick = 10, xTickRange = 10
yMinTick = 50, yMaxTick = 100, yTickRange = 50

valueToX(val) = 70 + (val / 10) * 390
valueToY(val) = 60 + 380 - ((val - 50) / 50) * 380
```

**X 轴网格线位置**：

| tick | valueToX |
|------|----------|
| 0 | 70 |
| 2 | 148 |
| 4 | 226 |
| 6 | 304 |
| 8 | 382 |
| 10 | 460 |

**Y 轴网格线位置**：

| tick | valueToY |
|------|----------|
| 50 | 440 |
| 60 | 364 |
| 70 | 288 |
| 80 | 212 |
| 90 | 136 |
| 100 | 60 |

**A班 数据点坐标**：

| 数据点 | x | y | valueToX | valueToY |
|--------|---|---|----------|----------|
| (2, 65) | 2 | 65 | 70 + (2/10)*390 = 148 | 60 + 380 - (15/50)*380 = 326 |
| (3, 70) | 3 | 70 | 70 + (3/10)*390 = 187 | 60 + 380 - (20/50)*380 = 288 |
| (5, 80) | 5 | 80 | 70 + (5/10)*390 = 265 | 60 + 380 - (30/50)*380 = 212 |
| (7, 88) | 7 | 88 | 70 + (7/10)*390 = 343 | 60 + 380 - (38/50)*380 = 151.2 |
| (8, 92) | 8 | 92 | 70 + (8/10)*390 = 382 | 60 + 380 - (42/50)*380 = 120.8 |

**B班 数据点坐标**：

| 数据点 | x | y | valueToX | valueToY |
|--------|---|---|----------|----------|
| (1, 55) | 1 | 55 | 70 + (1/10)*390 = 109 | 60 + 380 - (5/50)*380 = 402 |
| (4, 68) | 4 | 68 | 70 + (4/10)*390 = 226 | 60 + 380 - (18/50)*380 = 303.2 |
| (6, 75) | 6 | 75 | 70 + (6/10)*390 = 304 | 60 + 380 - (25/50)*380 = 250 |
| (7, 82) | 7 | 82 | 70 + (7/10)*390 = 343 | 60 + 380 - (32/50)*380 = 196.8 |
| (9, 95) | 9 | 95 | 70 + (9/10)*390 = 421 | 60 + 380 - (45/50)*380 = 98 |

**颜色**：dark-professional → Palette B → `palette[0]` = `#6366f1`（A班），`palette[1]` = `#f472b6`（B班）

---

## 与 Bar/Line 的关键差异

| 方面 | Bar | Line | Scatter |
|------|-----|------|---------|
| X 轴类型 | 类别轴 | 类别轴（共享标签） | 数值轴 |
| ViewBox | 矩形 | 矩形 | 正方形 (500x500) |
| 坐标映射 | 仅 valueToY | 仅 valueToY | valueToX + valueToY |
| 网格线 | 仅 Y 轴（默认关） | 仅 Y 轴（默认开） | X + Y 轴（默认开） |
| 数据形状 | `<rect>` 柱子 | 折线 + 标记点 | 4 种独立形状 |
| 数据点标签 | 柱顶（可选） | 标记点旁（可选） | 右上方（可选，仅当 label 存在） |

---

## Mermaid 输出

Scatter chart 不支持 Mermaid 格式（Mermaid 无散点图语法）。如果用户请求 Mermaid 格式，告知限制并建议 HTML 或 SVG 格式。
