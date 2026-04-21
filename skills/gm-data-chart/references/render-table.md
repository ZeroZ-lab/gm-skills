# 表格渲染规则 (Table Rendering Rules)

本参考文档定义了 table chart 的完整渲染流程，包含布局公式和 worked example。LLM 在 Step 2 生成 HTML/SVG 输出时必须遵循这些规则。

---

## 安全规则 (SECURITY — 最高优先级)

> **Table 在 foreignObject 中渲染完整 HTML，是所有图表类型中注入风险最高的。**
> 违反以下任何规则都可能导致 XSS 漏洞。

| 规则 | 说明 |
|------|------|
| **禁止 HTML 标签** | `<td>` 内容必须是纯文本。所有 `<`、`>`、`&`、`"`、`'` 必须用 HTML 实体编码替换（`&lt;`、`&gt;`、`&amp;`、`&quot;`、`&#39;`） |
| **width 严格验证** | `columns[].width` 必须匹配 `^(\d{1,4}px|auto)$`，禁止任意 CSS 值 |
| **sanitizedString** | `columns[].label` 和 `rows[]` 的所有值使用 `sanitizedString`（不含 `<>`） |
| **高亮颜色固定** | Max 高亮色 `rgba(34,197,94,0.15)`，Min 高亮色 `rgba(239,68,68,0.15)`。这些是系统固定值，**不得**来自用户输入，**不得**自定义 |

---

## 渲染架构

Table 采用 **纯 foreignObject 渲染模式**：

| 层次 | 技术 | 元素 |
|------|------|------|
| 容器 | SVG `<foreignObject>` | 唯一的外层包装 |
| 表格 | HTML `<table>` | `<thead>` + `<tbody>` |
| 数据 | HTML `<td>` | 纯文本内容 |

**关键差异**：Table 是唯一不使用任何 SVG 图形元素（`<rect>`、`<line>`、`<circle>` 等）的图表类型。SVG 仅用作 foreignObject 的容器。

---

## 布局常量

| 名称 | 值 | 用途 |
|------|-----|------|
| `TABLE_PADDING` | 16px | foreignObject 内边距 |
| `HEADER_HEIGHT` | 36px | 表头行高 |
| `ROW_HEIGHT` | 36px | 数据行高 |
| `ROW_NUMBER_WIDTH` | 40px | 行号列宽（showRowNumbers=true 时） |

### 尺寸计算

```
totalWidth = clamp(500, columns.length * 120, 900)
totalHeight = 60 + (rows.length + 1) * 36
```

- `totalWidth`：最少 500px，最多 900px，默认按每列 120px 估算
- `totalHeight`：60px 顶部留白 + 表头行 36px + 数据行每行 36px

---

## 逐步渲染流程

### Step A：读取数据

从 JSON 中读取：
- `columns[]` — 列定义（key, label, align, width）
- `rows[]` — 数据行（键值对，键匹配 column.key）
- `showRowNumbers` — 是否显示行号列
- `stripeRows` — 是否启用斑马纹
- `highlightMax` — 高亮最大值的列 key
- `highlightMin` — 高亮最小值的列 key

### Step B：计算高亮单元格

**highlightMax 逻辑**：

```
if highlightMax is specified:
  targetColumn = highlightMax
  maxValues = rows 中该列所有 typeof value === 'number' 的值
  if maxValues.length > 0:
    maxValue = Math.max(...maxValues)
    highlightRow = 找到 maxValue 所在的行索引
```

**highlightMin 逻辑**：

```
if highlightMin is specified:
  targetColumn = highlightMin
  minValues = rows 中该列所有 typeof value === 'number' 的值
  if minValues.length > 0:
    minValue = Math.min(...minValues)
    highlightRow = 找到 minValue 所在的行索引
```

> 注意：只对数值类型的单元格计算 max/min。字符串值不参与比较。

### Step C：构建 SVG + foreignObject 外壳

```html
<svg viewBox="0 0 {totalWidth} {totalHeight}" xmlns="http://www.w3.org/2000/svg">
  <foreignObject x="0" y="0" width="{totalWidth}" height="{totalHeight}">
    <div xmlns="http://www.w3.org/1999/xhtml" style="padding: {TABLE_PADDING}px;">
      <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
        <!-- thead and tbody go here -->
      </table>
    </div>
  </foreignObject>
</svg>
```

### Step D：构建表头 (`<thead>`)

```html
<thead>
  <tr class="table-header">
    <!-- 可选：行号列 -->
    <!-- 如果 showRowNumbers === true -->
    <th class="table-cell" style="width: 40px; text-align: center; font-weight: 700;
        padding: 8px 12px; border-bottom: 2px solid rgba(255,255,255,0.1);
        color: {headerTextColor};">#</th>

    <!-- 数据列 -->
    <!-- 对每个 column -->
    <th class="table-cell" style="text-align: {column.align}; font-weight: 700;
        padding: 8px 12px; border-bottom: 2px solid rgba(255,255,255,0.1);
        color: {headerTextColor};{如果 column.width 存在，加 width: column.width}">
      {column.label（HTML 转义后）}
    </th>
  </tr>
</thead>
```

### Step E：构建数据行 (`<tbody>`)

```html
<tbody>
  <!-- 对每一行（index = i） -->
  <tr class="table-row" style="
    {如果 stripeRows && i % 2 === 1}: background: rgba(255,255,255,0.03);
  ">
    <!-- 可选：行号 -->
    <!-- 如果 showRowNumbers === true -->
    <td class="table-cell row-number" style="text-align: center;
        color: {mutedTextColor}; padding: 8px 12px;
        border-bottom: 1px solid rgba(255,255,255,0.04);">
      {i + 1}
    </td>

    <!-- 对每个 column -->
    <td class="table-cell" style="text-align: {column.align};
        padding: 8px 12px;
        border-bottom: 1px solid rgba(255,255,255,0.04);
        {如果是高亮单元格，加 background + font-weight}">
      {rows[i][column.key]（HTML 转义后）}
    </td>
  </tr>
</tbody>
```

### Step F：应用高亮样式

高亮单元格的内联样式：

**Max 高亮**（固定值，不可自定义）：

```
background: rgba(34,197,94,0.15);
font-weight: 700;
```

CSS 类名：`highlight-max`

**Min 高亮**（固定值，不可自定义）：

```
background: rgba(239,68,68,0.15);
font-weight: 700;
```

CSS 类名：`highlight-min`

### Step G：包裹页面模板

使用所选 style 的 HTML 模板包装：
- `<html>` / `<head>` / `<style>` 页面结构
- `.container` > `.header`（标题 + 脉冲点）
- `.diagram-container` 包裹 SVG
- `.footer` 底部信息

---

## CSS 类定义

| 类名 | 用途 | 典型样式 |
|------|------|----------|
| `.table-header` | 表头行 | 深背景色，底部边框 |
| `.table-row` | 数据行 | 继承基线样式 |
| `.table-cell` | 所有单元格 | padding、border-bottom、对齐 |
| `.row-number` | 行号列 | 浅色文字，居中对齐 |
| `.highlight-max` | 最大值高亮 | 绿色半透明背景 `rgba(34,197,94,0.15)` |
| `.highlight-min` | 最小值高亮 | 红色半透明背景 `rgba(239,68,68,0.15)` |

---

## 暗色专业风格颜色参考

以下为 `dark-professional` 风格的 Table 相关颜色：

| 元素 | 颜色 |
|------|------|
| 页面背景 | `#020617` |
| 容器背景 | `#0f172a` |
| 表头文字 | `#f1f5f9` |
| 表头下边框 | `rgba(255,255,255,0.1)` |
| 数据文字 | `#e2e8f0` |
| 斑马纹行 | `rgba(255,255,255,0.03)` |
| 行下边框 | `rgba(255,255,255,0.04)` |
| 行号文字 | `#64748b` |
| Max 高亮 | `rgba(34,197,94,0.15)` |
| Min 高亮 | `rgba(239,68,68,0.15)` |
| Max 高亮文字 | `#22c55e` |
| Min 高亮文字 | `#ef4444` |

---

## Worked Example

**输入**：团队绩效表格 JSON

```json
{
  "diagramType": "table",
  "title": "Team Performance Q1 2025",
  "columns": [
    { "key": "name", "label": "Name", "align": "left" },
    { "key": "revenue", "label": "Revenue ($k)", "align": "right" },
    { "key": "deals", "label": "Deals", "align": "right" },
    { "key": "avg-deal-size", "label": "Avg Deal Size ($k)", "align": "right" }
  ],
  "rows": [
    { "name": "Alice", "revenue": 120, "deals": 8, "avg-deal-size": 15 },
    { "name": "Bob", "revenue": 95, "deals": 6, "avg-deal-size": 15.8 },
    { "name": "Carol", "revenue": 140, "deals": 10, "avg-deal-size": 14 }
  ],
  "stripeRows": true,
  "highlightMax": "revenue"
}
```

**计算**：

```
columns.length = 4
rows.length = 3

totalWidth = clamp(500, 4 * 120, 900) = clamp(500, 480, 900) = 500
totalHeight = 60 + (3 + 1) * 36 = 60 + 144 = 204
```

**高亮计算**：

```
highlightMax = "revenue"
revenue 列数值: [120, 95, 140]
maxValue = 140  →  行索引 2 (Carol)
```

**渲染结果结构**：

```html
<svg viewBox="0 0 500 204" xmlns="http://www.w3.org/2000/svg">
  <foreignObject x="0" y="0" width="500" height="204">
    <div xmlns="http://www.w3.org/1999/xhtml" style="padding: 16px;">
      <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
        <thead>
          <tr class="table-header">
            <th class="table-cell" style="text-align: left; font-weight: 700;
                padding: 8px 12px; border-bottom: 2px solid rgba(255,255,255,0.1);
                color: #f1f5f9;">Name</th>
            <th class="table-cell" style="text-align: right; font-weight: 700;
                padding: 8px 12px; border-bottom: 2px solid rgba(255,255,255,0.1);
                color: #f1f5f9;">Revenue ($k)</th>
            <th class="table-cell" style="text-align: right; font-weight: 700;
                padding: 8px 12px; border-bottom: 2px solid rgba(255,255,255,0.1);
                color: #f1f5f9;">Deals</th>
            <th class="table-cell" style="text-align: right; font-weight: 700;
                padding: 8px 12px; border-bottom: 2px solid rgba(255,255,255,0.1);
                color: #f1f5f9;">Avg Deal Size ($k)</th>
          </tr>
        </thead>
        <tbody>
          <!-- Row 0: Alice (stripeRows=true, index=0, even → no stripe) -->
          <tr class="table-row">
            <td class="table-cell" style="text-align: left; padding: 8px 12px;
                border-bottom: 1px solid rgba(255,255,255,0.04); color: #e2e8f0;">
              Alice</td>
            <td class="table-cell" style="text-align: right; padding: 8px 12px;
                border-bottom: 1px solid rgba(255,255,255,0.04); color: #e2e8f0;">
              120</td>
            <td class="table-cell" style="text-align: right; padding: 8px 12px;
                border-bottom: 1px solid rgba(255,255,255,0.04); color: #e2e8f0;">
              8</td>
            <td class="table-cell" style="text-align: right; padding: 8px 12px;
                border-bottom: 1px solid rgba(255,255,255,0.04); color: #e2e8f0;">
              15</td>
          </tr>
          <!-- Row 1: Bob (stripeRows=true, index=1, odd → stripe) -->
          <tr class="table-row" style="background: rgba(255,255,255,0.03);">
            <td class="table-cell" style="text-align: left; padding: 8px 12px;
                border-bottom: 1px solid rgba(255,255,255,0.04); color: #e2e8f0;">
              Bob</td>
            <td class="table-cell" style="text-align: right; padding: 8px 12px;
                border-bottom: 1px solid rgba(255,255,255,0.04); color: #e2e8f0;">
              95</td>
            <td class="table-cell" style="text-align: right; padding: 8px 12px;
                border-bottom: 1px solid rgba(255,255,255,0.04); color: #e2e8f0;">
              6</td>
            <td class="table-cell" style="text-align: right; padding: 8px 12px;
                border-bottom: 1px solid rgba(255,255,255,0.04); color: #e2e8f0;">
              15.8</td>
          </tr>
          <!-- Row 2: Carol (stripeRows=true, index=2, even → no stripe)
               highlightMax=revenue, maxValue=140 at this row -->
          <tr class="table-row">
            <td class="table-cell" style="text-align: left; padding: 8px 12px;
                border-bottom: 1px solid rgba(255,255,255,0.04); color: #e2e8f0;">
              Carol</td>
            <td class="table-cell highlight-max" style="text-align: right;
                padding: 8px 12px;
                border-bottom: 1px solid rgba(255,255,255,0.04);
                background: rgba(34,197,94,0.15);
                font-weight: 700; color: #22c55e;">
              140</td>
            <td class="table-cell" style="text-align: right; padding: 8px 12px;
                border-bottom: 1px solid rgba(255,255,255,0.04); color: #e2e8f0;">
              10</td>
            <td class="table-cell" style="text-align: right; padding: 8px 12px;
                border-bottom: 1px solid rgba(255,255,255,0.04); color: #e2e8f0;">
              14</td>
          </tr>
        </tbody>
      </table>
    </div>
  </foreignObject>
</svg>
```

---

## 与其他图表类型的差异

| 差异点 | Table | 其他图表 |
|--------|-------|----------|
| SVG 图形元素 | 无（仅 foreignObject） | 使用 `<rect>`、`<line>`、`<circle>` 等 |
| 坐标系 | 无（CSS 布局） | Cartesian 或 Polar |
| foreignObject 数量 | 1 个（包裹整个表格） | 多个（每个标签/图例一个） |
| 数据映射 | 键值对 → 单元格 | 数值 → 像素坐标 |
| Mermaid 支持 | 不支持 | 部分支持 |
| 注入风险 | 最高（完整 HTML） | 低（属性值注入） |
