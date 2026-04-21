# 坐标轴与网格规则 (Axis and Grid Rules for Charts)

本参考文档定义了图表坐标轴、网格线和刻度的渲染规则，适用于所有带坐标轴的图表类型（bar、line）。

---

## Nice Numbers 算法（Step 1 执行）

Nice Numbers 算法在 Step 1（JSON 提取阶段）执行，结果存入 `axis.y.ticks` 数组。Step 2 渲染时直接使用，无需重新计算。

### 步骤

```
1. 确定数据范围
   - values = 所有 series 中所有 data[].value
   - dataMin = min(values)
   - dataMax = max(values)
   - 如果所有值 >= 0：minValue 从 0 开始
   - 如果有负值：minValue = dataMin（后续向下取整到 nice step）

2. 计算粗略步长
   - range = dataMax - minValue
   - roughStep = range / 5（目标约 5 个刻度）

3. 选择 nice step
   - nice 序列：[1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, ...]
   - 对于小数：[0.1, 0.2, 0.5, 1, 2, 5, ...]
   - 找到最接近 roughStep 的 nice 值

4. 计算刻度范围
   - start = floor(minValue / niceStep) * niceStep
   - end = ceil(dataMax / niceStep) * niceStep

5. 生成 ticks 数组
   - ticks = [start, start + niceStep, start + 2*niceStep, ..., end]
   - 保留为整数（如果原始数据都是整数）
   - 否则保留与原始数据相同的小数位数
```

### Worked Examples

**Example 1：季度营收**

```
数据：[120, 150, 180, 200]
所有值 >= 0 → minValue = 0
range = 200 - 0 = 200
roughStep = 200 / 5 = 40
最接近 40 的 nice 值 → 50
start = floor(0 / 50) * 50 = 0
end = ceil(200 / 50) * 50 = 200
ticks = [0, 50, 100, 150, 200]
```

**Example 2：小数数据**

```
数据：[3.2, 5.7, 8.1]
所有值 >= 0 → minValue = 0
range = 8.1 - 0 = 8.1
roughStep = 8.1 / 5 = 1.62
最接近 1.62 的 nice 值 → 2
start = floor(0 / 2) * 2 = 0
end = ceil(8.1 / 2) * 2 = 10
ticks = [0, 2, 4, 6, 8, 10]
```

**Example 3：含负值**

```
数据：[-15, 10, 35]
有负值 → minValue = -15
range = 35 - (-15) = 50
roughStep = 50 / 5 = 10
最接近 10 的 nice 值 → 10
start = floor(-15 / 10) * 10 = -20
end = ceil(35 / 10) * 10 = 40
ticks = [-20, -10, 0, 10, 20, 30, 40]
```

**Example 4：全负值**

```
数据：[-80, -45, -30, -10]
全负值 → minValue = -80
range = -10 - (-80) = 70
roughStep = 70 / 5 = 14
最接近 14 的 nice 值 → 10
start = floor(-80 / 10) * 10 = -80
end = ceil(-10 / 10) * 10 = -10
ticks = [-80, -70, -60, -50, -40, -30, -20, -10]
（tick 数量偏多，可调整为 niceStep=20）
→ niceStep=20: ticks = [-80, -60, -40, -20, 0]
```

---

## 布局常量

| 名称 | 值 | 用途 |
|------|-----|------|
| `CHART_PADDING_TOP` | 60px | 标题 + 副标题区域 |
| `CHART_PADDING_RIGHT` | 40px | 右侧留白（或右侧图例空间） |
| `CHART_PADDING_BOTTOM` | 60px | X 轴标签 + 轴标题区域 |
| `CHART_PADDING_LEFT` | 70px | Y 轴刻度值 + 轴标题区域 |

### 绘图区域计算

```
plotWidth = totalWidth - CHART_PADDING_LEFT - CHART_PADDING_RIGHT
plotHeight = totalHeight - CHART_PADDING_TOP - CHART_PADDING_BOTTOM
plotX = CHART_PADDING_LEFT
plotY = CHART_PADDING_TOP
```

### 坐标映射公式

将数据值映射到像素 Y 坐标：

```
valueToY(value) = plotY + plotHeight - ((value - minTick) / tickRange) * plotHeight
```

其中 `tickRange = maxTick - minTick`。

对于水平方向（`direction: horizontal`），交换 X/Y：

```
valueToX(value) = plotX + ((value - minTick) / tickRange) * plotWidth
```

---

## 坐标轴渲染（Step 2）

### Y 轴

- **元素**：SVG `<line>`
- **位置**：从 `(plotX, plotY)` 到 `(plotX, plotY + plotHeight)`
- **CSS 类**：`.axis-line`
- **粗细**：由 CSS 定义（通常 1.5px）

### X 轴

- **元素**：SVG `<line>`
- **位置**：从 `(plotX, plotY + plotHeight)` 到 `(plotX + plotWidth, plotY + plotHeight)`
- **CSS 类**：`.axis-line`

### 基线（value = 0 的位置）

当数据包含负值时，需要在 Y 轴的 0 值位置画一条额外的基线：

```
baselineY = valueToY(0)
```

- **元素**：SVG `<line>`，从 `(plotX, baselineY)` 到 `(plotX + plotWidth, baselineY)`
- **样式**：比网格线稍粗，使用轴色

---

## 网格线规则

### 水平网格线（bar / line 默认方向）

- **元素**：SVG `<line>`
- **位置**：每个 tick 值（排除坐标轴本身）对应一条水平线
- **起止**：从 `plotX` 到 `plotX + plotWidth`
- **CSS 类**：`.grid-line`（CSS 定义虚线样式 `stroke-dasharray: 4,4`）

```
For each tick value (excluding minTick if it's on the axis line):
  y = valueToY(tick)
  <line x1="plotX" y1="y" x2="plotX + plotWidth" y2="y" class="grid-line" />
```

### 垂直网格线（可选，默认不显示）

如果 `axis.x.gridLines` 为 true，在每个 X 轴分组中心画垂直虚线。

---

## 刻度标签放置（foreignObject + CSS）

### Y 轴刻度值

- **容器**：foreignObject
- **位置**：每个 tick 的 Y 坐标左侧
- **布局**：

```svg
<foreignObject x="0" y="{tickY - 10}" width="{CHART_PADDING_LEFT - 10}" height="20">
  <div xmlns="http://www.w3.org/1999/xhtml" class="tick-label" style="text-align: right;">
    {tickValue}
  </div>
</foreignObject>
```

- 右对齐，字号 11px，使用 `.tick-label` CSS 类

### X 轴分组标签

- **容器**：foreignObject
- **位置**：每个分组中心正下方
- **布局**：

```svg
<foreignObject x="{groupCenterX - groupWidth/2}" y="{plotY + plotHeight + 8}" width="{groupWidth}" height="40">
  <div xmlns="http://www.w3.org/1999/xhtml" class="tick-label" style="text-align: center;">
    {label}
  </div>
</foreignObject>
```

- 居中对齐
- **长标签处理**：如果标签文本宽度超过 `groupWidth * 0.8`，添加 CSS `transform: rotate(-45deg); transform-origin: top center;` 并增加 foreignObject 高度到 60px

---

## 轴标题放置（foreignObject + CSS）

### Y 轴标题

- **容器**：foreignObject
- **位置**：Y 轴左侧，垂直居中
- **旋转**：-90 度

```svg
<foreignObject x="0" y="{plotY}" width="20" height="{plotHeight}">
  <div xmlns="http://www.w3.org/1999/xhtml" class="axis-title"
       style="transform: rotate(-90deg); transform-origin: center center; height: 100%; display: flex; align-items: center; justify-content: center;">
    {axis.y.label}
  </div>
</foreignObject>
```

### X 轴标题

- **容器**：foreignObject
- **位置**：X 轴标签下方，水平居中

```svg
<foreignObject x="{plotX}" y="{plotY + plotHeight + 40}" width="{plotWidth}" height="20">
  <div xmlns="http://www.w3.org/1999/xhtml" class="axis-title" style="text-align: center;">
    {axis.x.label}
  </div>
</foreignObject>
```

---

## X 轴 Nice Numbers（Scatter/Bubble）

Scatter 和 Bubble 图表的 X 轴也是数值轴（不是类别轴），需要对 X 轴数据运行同样的 Nice Numbers 算法。

### 步骤

与 Y 轴完全相同，只是数据来源换成所有 `series[].data[].x`：

```
1. 确定数据范围
   - values = 所有 series 中所有 data[].x
   - dataMin = min(values)
   - dataMax = max(values)
   - 如果所有值 >= 0：minValue 从 0 开始
   - 如果有负值：minValue = dataMin

2-5. 同 Y 轴步骤
```

结果存入 `axis.x.ticks`。

### 坐标映射公式

```
xMinTick = axis.x.ticks[0]
xMaxTick = axis.x.ticks[axis.x.ticks.length - 1]
xTickRange = xMaxTick - xMinTick

valueToX(val) = plotX + ((val - xMinTick) / xTickRange) * plotWidth
```

### X 轴渲染

X 轴刻度标签使用与 Y 轴相同的 foreignObject 模式，但水平排列在 X 轴下方：

```svg
<foreignObject x="{tickX - 25}" y="{plotY + plotHeight + 8}" width="50" height="20">
  <div xmlns="http://www.w3.org/1999/xhtml" class="tick-label" style="text-align: center;">
    {tickValue}
  </div>
</foreignObject>
```

其中 `tickX = valueToX(tickValue)`。

### 垂直网格线

当 `axis.x.gridLines = true` 时（scatter/bubble 默认为 true），对每个 X 轴 tick 画垂直虚线：

```svg
<line x1="{tickX}" y1="{plotY}" x2="{tickX}" y2="{plotY + plotHeight}" class="grid-line" />
```
