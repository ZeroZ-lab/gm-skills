# 雷达图渲染规则 (Radar Chart Rendering Rules)

本参考文档定义了 radar chart 的完整渲染流程，包含坐标公式和 worked example。LLM 在 Step 2 生成 SVG 输出时必须遵循这些规则。

---

## 渲染架构

Radar chart 采用 **混合渲染模式**：

| 层次 | 技术 | 元素 |
|------|------|------|
| 数据图形 | SVG 原生元素 | `<polygon>`（数据多边形、网格多边形）、`<line>`（轴线） |
| 文字区域 | foreignObject + CSS | 标题、副标题、轴标签、刻度值、图例 |

**为什么这样分**：多边形顶点坐标 = `center + radius * cos/sin(angle)`，这是简单三角函数运算，LLM 可以可靠计算。文字对齐和布局交给 CSS。

---

## 布局常量

| 名称 | 值 | 用途 |
|------|-----|------|
| `centerX` | totalWidth / 2 | 雷达中心 X |
| `centerY` | totalHeight / 2 | 雷达中心 Y |
| `radius` | min(totalWidth, totalHeight) * 0.35 | 外半径（网格最外层） |
| `numAxes` | axes.length | 轴数量 |
| `angleStep` | 360 / numAxes | 相邻轴夹角（度） |
| `LABEL_RADIUS` | radius + 25 | 轴标签距离中心的距离 |

### 尺寸计算

```
totalWidth = totalHeight = max(500, 300 + numAxes * 20)
```

正方形 ViewBox，确保雷达图各方向等距。

### 中心坐标和半径

```
centerX = totalWidth / 2
centerY = totalHeight / 2
radius = min(totalWidth, totalHeight) * 0.35
angleStep = 360 / numAxes
```

---

## 逐步渲染流程

### Step A：读取数据

从 JSON 中读取：
- `axes[].label` — 轴标签
- `axes[].maxValue` — 各轴最大值（all-or-nothing）
- `series[].data[]` — 各系列各轴数值
- `series[].fillOpacity` — 填充透明度（默认 0.15）
- `scaleLevels` — 同心多边形层数（默认 5）

### Step B：验证 maxValue

**all-or-nothing 规则**：`axes[].maxValue` 要么全部指定，要么全部不指定。

- 全部不指定时：对每个轴 i，取 `max(series[0..N-1].data[i])` 并向上取整
- 部分指定时：Step 1 验证时拒绝，要求用户补全或移除所有 maxValue

### Step C：绘制同心多边形（网格）

```
For level = 1..scaleLevels:
  levelRadius = radius * (level / scaleLevels)
  points = []
  For each axis i (0..numAxes-1):
    angle = (-90 + i * angleStep) * π / 180   // 从 12 点钟开始
    px = centerX + levelRadius * cos(angle)
    py = centerY + levelRadius * sin(angle)
    points += "{px},{py}"

  <polygon points="{points joined by space}"
           fill="none" stroke="{gridColor}" stroke-width="0.5" class="grid-line" />
```

**要点**：
- 角度从 -90° 开始（12 点钟方向），确保第一个轴在正上方
- 使用 `.grid-line` CSS 类（与 bar/pie 保持一致）
- `scaleLevels` 默认 5，产生 5 层同心多边形

### Step D：绘制轴线

从中心到每个轴的端点画线，使用 `.grid-line` CSS 类：

```svg
<line x1="{centerX}" y1="{centerY}" x2="{endX}" y2="{endY}" class="grid-line" />
```

其中：

```
For each axis i:
  angle = (-90 + i * angleStep) * π / 180
  endX = centerX + radius * cos(angle)
  endY = centerY + radius * sin(angle)
```

### Step E：绘制数据多边形

```
For each series s:
  points = []
  For each axis i (0..numAxes-1):
    normalizedValue = series[s].data[i] / axes[i].maxValue
    r = radius * normalizedValue
    angle = (-90 + i * angleStep) * π / 180
    px = centerX + r * cos(angle)
    py = centerY + r * sin(angle)
    points += "{px},{py}"

  <polygon points="{points joined by space}"
           fill="{color}" fill-opacity="{fillOpacity}"
           stroke="{color}" stroke-width="2" stroke-linejoin="round" />
```

**颜色**：`color` 通过 `color-palettes.md` 的规则确定。未指定时使用 `palette[s % 10]`。

**渲染顺序**：先绘制第一个 series，后绘制最后一个（后画的在上层）。

### Step F：绘制轴标签（foreignObject）

在每个轴端点外侧放置标签：

```
For each axis i:
  angle = (-90 + i * angleStep) * π / 180
  labelRadius = radius + 25
  labelX = centerX + labelRadius * cos(angle) - labelWidth / 2
  labelY = centerY + labelRadius * sin(angle) - 8
```

```svg
<foreignObject x="{labelX}" y="{labelY}" width="{labelWidth}" height="20">
  <div xmlns="http://www.w3.org/1999/xhtml" class="tick-label"
       style="text-align: center;">
    {axes[i].label}
  </div>
</foreignObject>
```

**labelWidth 估算**：按每个字符约 8px 估算，最小 40px，最大 120px。

### Step G：绘制刻度值

沿第一个轴（axis 0）显示刻度值：

```
For level = 1..scaleLevels:
  value = axes[0].maxValue * (level / scaleLevels)
  levelRadius = radius * (level / scaleLevels)
  angle = (-90 + 0 * angleStep) * π / 180
  tickX = centerX + levelRadius * cos(angle) - 25
  tickY = centerY + levelRadius * sin(angle) - 2
```

```svg
<foreignObject x="{tickX}" y="{tickY}" width="25" height="16">
  <div xmlns="http://www.w3.org/1999/xhtml" class="tick-label"
       style="text-align: right; font-size: 10px;">
    {value}
  </div>
</foreignObject>
```

### Step H：绘制图例（foreignObject + CSS）

```svg
<foreignObject x="{centerX - plotWidth/2}" y="{centerY + radius + 40}"
               width="{plotWidth}" height="30">
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

Radar chart **不支持** Mermaid 输出。如果用户请求 Mermaid 格式，告知限制并建议 HTML 或 SVG。

---

## Worked Example

**输入**：开发者技能对比 JSON

```json
{
  "diagramType": "radar",
  "title": "Developer Skills",
  "axes": [
    { "label": "Frontend", "maxValue": 10 },
    { "label": "Backend",  "maxValue": 10 },
    { "label": "DevOps",   "maxValue": 10 },
    { "label": "Design",   "maxValue": 10 },
    { "label": "Testing",  "maxValue": 10 }
  ],
  "series": [
    {
      "name": "Dev A",
      "fillOpacity": 0.15,
      "data": [8, 6, 7, 5, 9]
    },
    {
      "name": "Dev B",
      "fillOpacity": 0.15,
      "data": [6, 9, 5, 8, 7]
    }
  ],
  "scaleLevels": 5
}
```

**布局计算**：

```
numAxes = 5
totalWidth = totalHeight = max(500, 300 + 5 * 20) = 500
centerX = 500 / 2 = 250
centerY = 500 / 2 = 250
radius = min(500, 500) * 0.35 = 175
angleStep = 360 / 5 = 72
```

**角度表**：

| Axis i | angle (deg) | angle (rad) | cos | sin | endX | endY |
|--------|-------------|-------------|-----|-----|------|------|
| 0 (Frontend) | -90 | -1.5708 | 0 | -1 | 250.0 | 75.0 |
| 1 (Backend) | -18 | -0.3142 | 0.9511 | -0.3090 | 416.4 | 195.9 |
| 2 (DevOps) | 54 | 0.9425 | 0.5878 | 0.8090 | 352.9 | 391.6 |
| 3 (Design) | 126 | 2.1991 | -0.5878 | 0.8090 | 147.1 | 391.6 |
| 4 (Testing) | 198 | 3.4558 | -0.9511 | -0.3090 | 83.6 | 195.9 |

**同心五边形网格**（scaleLevels = 5）：

```
levelRadius = 175 * (level / 5) = 35, 70, 105, 140, 175
```

| Level | radius | tickValue | 五边形顶点 |
|-------|--------|-----------|-----------|
| 1 | 35 | 2 | 250.0,215.0 283.3,239.2 270.6,278.3 229.4,278.3 216.7,239.2 |
| 2 | 70 | 4 | 250.0,180.0 316.6,228.4 291.1,306.6 208.9,306.6 183.4,228.4 |
| 3 | 105 | 6 | 250.0,145.0 349.9,217.6 311.7,334.9 188.3,334.9 150.1,217.6 |
| 4 | 140 | 8 | 250.0,110.0 383.1,206.7 332.3,363.3 167.7,363.3 116.9,206.7 |
| 5 | 175 | 10 | 250.0,75.0 416.4,195.9 352.9,391.6 147.1,391.6 83.6,195.9 |

**Dev A 数据多边形**（data = [8, 6, 7, 5, 9], maxValue = 10）：

| Axis | data | normalized | r | px | py |
|------|------|-----------|---|------|------|
| 0 Frontend | 8 | 0.8 | 140.0 | 250.0 | 110.0 |
| 1 Backend | 6 | 0.6 | 105.0 | 349.9 | 217.6 |
| 2 DevOps | 7 | 0.7 | 122.5 | 322.0 | 349.1 |
| 3 Design | 5 | 0.5 | 87.5 | 198.6 | 320.8 |
| 4 Testing | 9 | 0.9 | 157.5 | 100.2 | 201.3 |

polygon points = "250.0,110.0 349.9,217.6 322.0,349.1 198.6,320.8 100.2,201.3"

**Dev B 数据多边形**（data = [6, 9, 5, 8, 7], maxValue = 10）：

| Axis | data | normalized | r | px | py |
|------|------|-----------|---|------|------|
| 0 Frontend | 6 | 0.6 | 105.0 | 250.0 | 145.0 |
| 1 Backend | 9 | 0.9 | 157.5 | 399.8 | 201.3 |
| 2 DevOps | 5 | 0.5 | 87.5 | 301.4 | 320.8 |
| 3 Design | 8 | 0.8 | 140.0 | 167.7 | 363.3 |
| 4 Testing | 7 | 0.7 | 122.5 | 133.5 | 212.1 |

polygon points = "250.0,145.0 399.8,201.3 301.4,320.8 167.7,363.3 133.5,212.1"

**颜色**：dark-professional -> Palette B

```
Dev A: palette[0] = #6366f1
Dev B: palette[1] = #f472b6
```

**轴标签位置**（labelRadius = 175 + 25 = 200）：

| Axis | labelX | labelY |
|------|--------|--------|
| 0 Frontend | 250.0 | 50.0 |
| 1 Backend | 440.2 | 188.2 |
| 2 DevOps | 367.6 | 411.8 |
| 3 Design | 132.4 | 411.8 |
| 4 Testing | 59.8 | 188.2 |
