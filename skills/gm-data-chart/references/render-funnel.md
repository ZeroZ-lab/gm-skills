# 漏斗图渲染规则 (Funnel Chart Rendering Rules)

本参考文档定义了 funnel chart 的完整渲染流程，包含坐标公式和 worked example。LLM 在 Step 2 生成 SVG 输出时必须遵循这些规则。

---

## 渲染架构

Funnel chart 采用 **SVG 原生元素** 渲染：

| 层次 | 技术 | 元素 |
|------|------|------|
| 数据图形 | SVG `<polygon>` | 梯形/圆角梯形 |
| 文字区域 | foreignObject + CSS | 标题、阶段名称、数值、转化率 |

---

## 布局常量

| 名称 | 值 | 用途 |
|------|-----|------|
| `FUNNEL_MAX_WIDTH_RATIO` | 0.7 | 最大层宽度占 totalWidth 比例 |
| `FUNNEL_GAP` | 4px | 层间距 |
| `FUNNEL_TOP_PADDING` | 60px | 标题区域 |

### 高度计算

```
barHeight by density:
  compact  = 40px
  normal   = 55px
  spacious = 70px

totalWidth = 600
totalHeight = FUNNEL_TOP_PADDING + numItems * barHeight + (numItems - 1) * FUNNEL_GAP
```

### 宽度与居中

```
maxWidth = totalWidth * FUNNEL_MAX_WIDTH_RATIO
centerX = totalWidth / 2
```

---

## 逐步渲染流程

### Step A：读取数据

从 JSON 中读取：
- `data[].label` — 阶段名称
- `data[].value` — 数值
- `variant` — trapezoid 或 rounded
- `showConversionRate` — 是否显示转化率

如果 `data` 未按 value 降序排列，先排序（保留原始顺序的 label-value 对应关系）。

### Step B：计算梯形几何

```
maxValue = data[0].value

For each item i:
  topWidth = maxWidth * (data[i].value / maxValue)
  bottomWidth = (i < numItems - 1)
    ? maxWidth * (data[i+1].value / maxValue)
    : topWidth  // 最后一层：flat bottom（底边与顶边等宽）

  itemY = FUNNEL_TOP_PADDING + i * (barHeight + FUNNEL_GAP)

  // 四个顶点
  topLeft     = (centerX - topWidth/2, itemY)
  topRight    = (centerX + topWidth/2, itemY)
  bottomRight = (centerX + bottomWidth/2, itemY + barHeight)
  bottomLeft  = (centerX - bottomWidth/2, itemY + barHeight)
```

### Step C：绘制梯形

**Trapezoid 变体**：

```svg
<polygon points="{topLeft.x},{topLeft.y} {topRight.x},{topRight.y} {bottomRight.x},{bottomRight.y} {bottomLeft.x},{bottomLeft.y}"
         fill="{paletteColor}" class="funnel-stage" />
```

**Rounded 变体**：使用 `<path>` 替代 `<polygon>`，顶部/底部边用二次贝塞尔曲线（`Q` 命令）产生圆角效果：

```
cornerR = 6  // 圆角半径

// 简化版：仅对梯形上下边的转角做圆弧
path = "M {topLeft.x + cornerR},{topLeft.y}
        Q {topLeft.x},{topLeft.y} {topLeft.x},{topLeft.y + cornerR}
        L {bottomLeft.x},{bottomLeft.y - cornerR}
        Q {bottomLeft.x},{bottomLeft.y} {bottomLeft.x + cornerR},{bottomLeft.y}
        L {bottomRight.x - cornerR},{bottomRight.y}
        Q {bottomRight.x},{bottomRight.y} {bottomRight.x},{bottomRight.y - cornerR}
        L {topRight.x},{topRight.y + cornerR}
        Q {topRight.x},{topRight.y} {topRight.x - cornerR},{topRight.y}
        Z"
```

### Step D：绘制标签（foreignObject + CSS）

阶段名称和数值居中显示在梯形内部：

```svg
<foreignObject x="{centerX - topWidth/2}" y="{itemY + 8}" width="{topWidth}" height="{barHeight - 8}">
  <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%;">
    <div class="funnel-label">{label}</div>
    <div class="tick-label">{value}</div>
  </div>
</foreignObject>
```

### Step E：绘制转化率

当 `showConversionRate: true` 时，在相邻层之间显示转化百分比：

```
For i = 0..numItems-2:
  rate = (data[i+1].value / data[i].value * 100).toFixed(1)
  betweenY = itemY + barHeight + FUNNEL_GAP / 2
```

```svg
<foreignObject x="{centerX - 40}" y="{betweenY - 8}" width="80" height="16">
  <div xmlns="http://www.w3.org/1999/xhtml" class="tick-label"
       style="text-align: center; font-size: 11px; color: #64748b;">
    ↓ {rate}%
  </div>
</foreignObject>
```

### Step F：绘制标题和副标题

与 bar chart 相同的 foreignObject 模式。

### Step G：绘制图例

如果 `legend.visible: true`，在底部或顶部显示各阶段的颜色和名称。

---

## 颜色分配

每个阶段使用调色板的顺序颜色：

```
For each item i:
  if data[i].color is set:
    use that color
  else:
    use palette[i % 10]
```

---

## Worked Example

**输入**：销售漏斗

```json
{
  "data": [
    { "label": "线索", "value": 1000 },
    { "label": "合格线索", "value": 600 },
    { "label": "方案报价", "value": 300 },
    { "label": "商务谈判", "value": 150 },
    { "label": "成交", "value": 80 }
  ],
  "density": "normal",
  "variant": "trapezoid"
}
```

**计算**：

```
numItems = 5, maxValue = 1000
totalWidth = 600
maxWidth = 600 * 0.7 = 420
centerX = 300
barHeight = 55 (normal)
totalHeight = 60 + 5 * 55 + 4 * 4 = 60 + 275 + 16 = 351

颜色 (Palette B): #6366f1, #f472b6, #34d399, #fbbf24, #a78bfa

// 线索 (i=0): value=1000
topWidth = 420 * (1000/1000) = 420
bottomWidth = 420 * (600/1000) = 252
itemY = 60
topLeft = (300-210, 60) = (90, 60)
topRight = (300+210, 60) = (510, 60)
bottomRight = (300+126, 115) = (426, 115)
bottomLeft = (300-126, 115) = (174, 115)
polygon = "90,60 510,60 426,115 174,115"

// 合格线索 (i=1): value=600
topWidth = 252
bottomWidth = 420 * (300/1000) = 126
itemY = 60 + 1 * 59 = 119
topLeft = (174, 119), topRight = (426, 119)
bottomRight = (363, 174), bottomLeft = (237, 174)
polygon = "174,119 426,119 363,174 237,174"

// 方案报价 (i=2): value=300
topWidth = 126
bottomWidth = 420 * (150/1000) = 63
itemY = 178
topLeft = (237, 178), topRight = (363, 178)
bottomRight = (331.5, 233), bottomLeft = (268.5, 233)
polygon = "237,178 363,178 331.5,233 268.5,233"

// 商务谈判 (i=3): value=150
topWidth = 63
bottomWidth = 420 * (80/1000) = 33.6
itemY = 237
topLeft = (268.5, 237), topRight = (331.5, 237)
bottomRight = (316.8, 292), bottomLeft = (283.2, 292)
polygon = "268.5,237 331.5,237 316.8,292 283.2,292"

// 成交 (i=4): value=80
topWidth = 33.6
bottomWidth = 33.6 (最后一层 flat bottom)
itemY = 296
topLeft = (283.2, 296), topRight = (316.8, 296)
bottomRight = (316.8, 351), bottomLeft = (283.2, 351)
polygon = "283.2,296 316.8,296 316.8,351 283.2,351"

转化率:
  线索→合格: 60.0%
  合格→方案: 50.0%
  方案→谈判: 50.0%
  谈判→成交: 53.3%
```
