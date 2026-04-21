# 饼图/环形图渲染规则 (Pie/Donut Chart Rendering Rules)

本参考文档定义了 pie/donut chart 的完整渲染流程，包含坐标公式和 worked example。LLM 在 Step 2 生成 SVG 输出时必须遵循这些规则。

---

## 渲染架构

Pie chart 采用 **混合渲染模式**：

| 层次 | 技术 | 元素 |
|------|------|------|
| 数据图形 | SVG 原生元素 | `<path>`（扇区弧形） |
| 文字区域 | foreignObject + CSS | 标题、副标题、标签、图例、中心文字 |

**为什么这样分**：弧形路径需要精确的角度和坐标计算，LLM 可以可靠完成。文字对齐和布局交给 CSS。

---

## 布局常量

| 名称 | 值 | 用途 |
|------|-----|------|
| `PIE_CENTER_X` | totalWidth * 0.42 | 饼图中心 X（偏左，为右侧图例留空间） |
| `PIE_CENTER_Y` | totalHeight / 2 | 饼图中心 Y |
| `PIE_RADIUS` | min(totalWidth * 0.35, totalHeight * 0.40) | 外半径 |
| `PIE_LABEL_RADIUS` | PIE_RADIUS + 25 | 外部标签位置 |
| `START_OFFSET` | -90 | 角度偏移（从 12 点钟方向开始） |

### 尺寸计算

```
totalWidth = 600（固定）
totalHeight = max(400, 60 + numItems * 30)
```

### 中心坐标和半径

```
centerX = totalWidth * 0.42
centerY = totalHeight / 2
PIE_RADIUS = min(totalWidth * 0.35, totalHeight * 0.40)
```

---

## 逐步渲染流程

### Step A：读取数据

从 JSON 中读取：
- `data[].label` — 类别标签
- `data[].value` — 数值（必须 > 0）
- `variant` — pie 或 donut
- `donut.innerRadiusRatio` — 内半径比例（仅 donut）
- `legend.visible`、`legend.position` — 图例配置

### Step B：计算角度

```
totalValue = sum of all data[].value
For each data item:
  angle = (item.value / totalValue) * 360°
  startAngle = cumulative angle
  endAngle = startAngle + angle
```

### Step C：SVG 弧形绘制（Pie 模式）

使用 `<path>` 的 `A`（arc）命令。所有角度从 12 点钟方向开始（START_OFFSET = -90）：

```
// 角度转弧度（含 START_OFFSET 偏移）
startRad = (startAngle + START_OFFSET) * π / 180
endRad = (endAngle + START_OFFSET) * π / 180

// 弧形起点（外圆）
x1 = centerX + radius * cos(startRad)
y1 = centerY + radius * sin(startRad)

// 弧形终点（外圆）
x2 = centerX + radius * cos(endRad)
y2 = centerY + radius * sin(endRad)

sliceAngle = endAngle - startAngle  // 单个扇区角度
largeArcFlag = (sliceAngle > 180) ? 1 : 0

path = "M {centerX} {centerY}
        L {x1} {y1}
        A {radius} {radius} 0 {largeArcFlag} 1 {x2} {y2}
        Z"
```

**要点**：
- 外弧 sweep-flag = 1（顺时针）
- largeArcFlag: 扇区 > 180° 时为 1，否则为 0
- 路径从中心出发，画直线到弧起点，画弧到弧终点，闭合回中心

### Step D：Donut 变体

使用完整环形扇区路径（annular sector）：

```
innerRadius = PIE_RADIUS * donut.innerRadiusRatio

// 内圆弧端点
ix1 = centerX + innerRadius * cos(startRad)
iy1 = centerY + innerRadius * sin(startRad)
ix2 = centerX + innerRadius * cos(endRad)
iy2 = centerY + innerRadius * sin(endRad)

// 完整环形扇区：外弧起点 → 外弧终点 → 内弧终点（逆时针）→ 内弧起点 → 闭合
path = "M {x1} {y1}
        A {radius} {radius} 0 {largeArcFlag} 1 {x2} {y2}
        L {ix2} {iy2}
        A {innerRadius} {innerRadius} 0 {largeArcFlag} 0 {ix1} {iy1}
        Z"
```

**注意**：
- 外弧 sweep-flag = 1（顺时针）
- 内弧 sweep-flag = 0（逆时针，与外弧相反）
- 路径不从中心出发，而是在内外圆之间画环形扇区
- `donut.innerRadiusRatio` 默认 0.6

### Step E：中心文字（Donut 模式）

当 `variant: "donut"` 且 `donut.centerText` 或 `donut.centerValue` 存在时：

```svg
<foreignObject x="{centerX - 50}" y="{centerY - 20}" width="100" height="40">
  <div xmlns="http://www.w3.org/1999/xhtml" style="text-align: center;">
    <div class="axis-title" style="font-size: 12px;">{donut.centerText}</div>
    <div style="font-size: 20px; font-weight: 700;">{donut.centerValue}</div>
  </div>
</foreignObject>
```

### Step F：绘制扇区标签

- 百分比计算：`percentage = (item.value / totalValue * 100).toFixed(1)`
- 计算扇区中点角度：`midAngle = (startAngle + endAngle) / 2`
- 计算中点弧度：`midRad = (midAngle + START_OFFSET) * π / 180`

**标签放置规则**（根据扇区占比）：

| 占比 | 标签策略 |
|------|---------|
| < 5% | 不显示扇区标签（仅图例中显示） |
| 5%-15% | 内部标签，位于 `radius * 0.75` 处（靠近外边缘） |
| > 15% | 内部标签，位于 `radius * 0.55` 处（扇区中心） |

```svg
<foreignObject x="{labelX - 30}" y="{labelY - 10}" width="60" height="20">
  <div xmlns="http://www.w3.org/1999/xhtml" class="tick-label"
       style="text-align: center; font-size: 11px;">
    {percentage}%
  </div>
</foreignObject>
```

### Step G：绘制图例（legend position = "right"）

```svg
<foreignObject x="{centerX + PIE_RADIUS + 40}" y="{centerY - numItems * 14}"
               width="{totalWidth - centerX - PIE_RADIUS - 60}" height="{numItems * 28}">
  <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; flex-direction: column; gap: 8px;">
    <!-- 每项：色块 + 名称 + 百分比 -->
    <div style="display: flex; align-items: center; gap: 8px;">
      <div style="width: 12px; height: 12px; background: {color}; border-radius: 2px; flex-shrink: 0;"></div>
      <span class="tick-label" style="flex: 1;">{label}</span>
      <span class="tick-label">{percentage}%</span>
    </div>
  </div>
</foreignObject>
```

**图例位置计算**：
- `x = centerX + PIE_RADIUS + 40`（饼图右侧留 40px 间距）
- `y = centerY - numItems * 14`（垂直居中）
- `width = totalWidth - centerX - PIE_RADIUS - 60`
- `height = numItems * 28`

### Step H：绘制标题和副标题

```svg
<!-- 标题 -->
<foreignObject x="0" y="10" width="{totalWidth}" height="28">
  <div xmlns="http://www.w3.org/1999/xhtml" class="axis-title"
       style="text-align: center; font-size: 18px; font-weight: 700;">
    {title}
  </div>
</foreignObject>

<!-- 副标题 -->
<foreignObject x="0" y="36" width="{totalWidth}" height="20">
  <div xmlns="http://www.w3.org/1999/xhtml" class="tick-label"
       style="text-align: center;">
    {subtitle}
  </div>
</foreignObject>
```

---

## Mermaid 输出

```mermaid
pie title {title}
    "{label1}" : {value1}
    "{label2}" : {value2}
```

**Mermaid 标签转义规则**：
- `"` 转义为 `#quot;`
- 标签中的换行符、`:` 字符需移除或替换为空格
- 插入 Mermaid 语法前验证 value 为有限数字

---

## Worked Example

**输入**：浏览器市场份额 JSON

```json
{
  "diagramType": "pie",
  "title": "浏览器市场份额",
  "variant": "pie",
  "data": [
    { "label": "Chrome", "value": 65 },
    { "label": "Safari", "value": 19 },
    { "label": "Firefox", "value": 10 },
    { "label": "Edge", "value": 4 },
    { "label": "其他", "value": 2 }
  ]
}
```

**布局计算**：

```
numItems = 5
totalValue = 65 + 19 + 10 + 4 + 2 = 100
totalWidth = 600
totalHeight = max(400, 60 + 5 * 30) = 400
centerX = 600 * 0.42 = 252
centerY = 400 / 2 = 200
PIE_RADIUS = min(600 * 0.35, 400 * 0.40) = min(210, 160) = 160
START_OFFSET = -90
```

**Slice 1 — Chrome (65)**：

```
sliceAngle = 65/100 * 360 = 234°
startAngle = 0, endAngle = 234

startRad = (0 - 90) * π/180 = -π/2 = -1.5708
endRad = (234 - 90) * π/180 = 144° * π/180 = 2.5133

x1 = 252 + 160 * cos(-1.5708) = 252 + 160 * 0     = 252.0
y1 = 200 + 160 * sin(-1.5708) = 200 + 160 * (-1)   = 40.0
x2 = 252 + 160 * cos(2.5133)  = 252 + 160 * (-0.809) = 122.6
y2 = 200 + 160 * sin(2.5133)  = 200 + 160 * 0.5878   = 294.0

largeArcFlag = 1  (234 > 180)
percentage = 65.0%

path = "M 252 200 L 252.0 40.0 A 160 160 0 1 1 122.6 294.0 Z"

midAngle = 117°, midRad = 0.4712
labelR = 160 * 0.55 = 88 (> 15%, 放在扇区中心)
labelX = 252 + 88 * cos(0.4712) = 252 + 78.4 = 330.4
labelY = 200 + 88 * sin(0.4712) = 200 + 40.0 = 240.0
```

**Slice 2 — Safari (19)**：

```
sliceAngle = 19/100 * 360 = 68.4°
startAngle = 234, endAngle = 302.4

startRad = (234 - 90) * π/180 = 144° * π/180 = 2.5133
endRad = (302.4 - 90) * π/180 = 212.4° * π/180 = 3.7071

x1 = 252 + 160 * cos(2.5133) = 252 + 160 * (-0.809) = 122.6
y1 = 200 + 160 * sin(2.5133) = 200 + 160 * 0.5878   = 294.0
x2 = 252 + 160 * cos(3.7071) = 252 + 160 * (-0.8443) = 116.9
y2 = 200 + 160 * sin(3.7071) = 200 + 160 * (-0.5358) = 114.3

largeArcFlag = 0  (68.4 <= 180)
percentage = 19.0%

path = "M 252 200 L 122.6 294.0 A 160 160 0 0 1 116.9 114.3 Z"

midAngle = 268.2°, midRad = 3.1102
labelR = 160 * 0.55 = 88 (> 15%, 放在扇区中心)
labelX = 252 + 88 * cos(3.1102) = 252 + (-88.0) = 164.0
labelY = 200 + 88 * sin(3.1102) = 200 + 2.8 = 202.8
```

**Slice 3 — Firefox (10)**：

```
sliceAngle = 10/100 * 360 = 36°
startAngle = 302.4, endAngle = 338.4

startRad = (302.4 - 90) * π/180 = 212.4° * π/180 = 3.7071
endRad = (338.4 - 90) * π/180 = 248.4° * π/180 = 4.3354

x1 = 252 + 160 * cos(3.7071) = 116.9
y1 = 200 + 160 * sin(3.7071) = 114.3
x2 = 252 + 160 * cos(4.3354) = 252 + 160 * (-0.3681) = 193.1
y2 = 200 + 160 * sin(4.3354) = 200 + 160 * (-0.9298) = 51.2

largeArcFlag = 0  (36 <= 180)
percentage = 10.0%

path = "M 252 200 L 116.9 114.3 A 160 160 0 0 1 193.1 51.2 Z"

midAngle = 320.4°, midRad = 4.0212
labelR = 160 * 0.75 = 120 (5%-15%, 靠近外边缘)
labelX = 252 + 120 * cos(4.0212) = 252 + (-76.5) = 175.5
labelY = 200 + 120 * sin(4.0212) = 200 + (-92.5) = 107.5
```

**Slice 4 — Edge (4)**：

```
sliceAngle = 4/100 * 360 = 14.4°
startAngle = 338.4, endAngle = 352.8
percentage = 4.0%

path = "M 252 200 L 193.1 51.2 A 160 160 0 0 1 231.9 41.3 Z"
```

Edge = 4.0% < 5%，不显示扇区标签。

**Slice 5 — 其他 (2)**：

```
sliceAngle = 2/100 * 360 = 7.2°
startAngle = 352.8, endAngle = 360.0
percentage = 2.0%

path = "M 252 200 L 231.9 41.3 A 160 160 0 0 1 252.0 40.0 Z"
```

其他 = 2.0% < 5%，不显示扇区标签。

**颜色**：dark-professional → Palette B

```
Chrome: #6366f1, Safari: #f472b6, Firefox: #34d399, Edge: #fbbf24, 其他: #a78bfa
```

**完整扇区坐标汇总**：

| 数据项 | value | sliceAngle | startAngle | endAngle | x1 | y1 | x2 | y2 | largeArcFlag | % | 标签 |
|--------|-------|-----------|------------|----------|------|------|------|------|-------------|------|------|
| Chrome | 65 | 234.0° | 0.0 | 234.0 | 252.0 | 40.0 | 122.6 | 294.0 | 1 | 65.0% | 内部中心 |
| Safari | 19 | 68.4° | 234.0 | 302.4 | 122.6 | 294.0 | 116.9 | 114.3 | 0 | 19.0% | 内部中心 |
| Firefox | 10 | 36.0° | 302.4 | 338.4 | 116.9 | 114.3 | 193.1 | 51.2 | 0 | 10.0% | 内部偏外 |
| Edge | 4 | 14.4° | 338.4 | 352.8 | 193.1 | 51.2 | 231.9 | 41.3 | 0 | 4.0% | 无 |
| 其他 | 2 | 7.2° | 352.8 | 360.0 | 231.9 | 41.3 | 252.0 | 40.0 | 0 | 2.0% | 无 |
