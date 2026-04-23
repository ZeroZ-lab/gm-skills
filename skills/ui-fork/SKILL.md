---
name: ui-fork
description: 从一张或多张 UI 截图中提炼可复用设计指南、设计系统草案、design tokens 和后续 AI 延续设计约束。Use when users want to analyze UI screenshots, fork an interface style, create a design guide from images, extract UI design-system rules, or generate a prompt contract for future AI-generated pages.
argument-hint: "[UI 截图/产品背景/输出模式 brief|guide|system]"
---

# ui-fork

把 UI 截图转成可复用的设计系统草案和后续 AI 续写约束。目标不是描述图片，而是把图片中的界面逻辑提炼成可延续、可实现、可评估的设计资产。

## 默认行为

- 默认输出模式：`guide`。
- 默认范围：分析截图并输出设计指南、tokens 草案、组件规则、Prompt Contract。
- 不直接生成前端代码，除非用户明确要求。
- 如果用户没有提供产品背景，先基于截图推断页面类型和目标，并在 `Confidence Split` 中标注为推断。

## 输出语言

在开始分析前，必须询问用户：

**"生成的 DESIGN.md 文档使用中文还是英文？"**

使用 AskUserQuestion 提供选项：
- **中文**：所有章节标题和内容使用中文
- **英文**：所有章节标题和内容使用英文
- **双语**：章节标题使用英文，内容使用中文（推荐用于国际化项目）

根据用户选择，后续所有输出内容都必须严格遵循该语言设置。

## 输入

接受任意组合：

- 一张或多张 UI 截图
- 产品背景、目标用户、业务目标
- 输出模式：`brief`、`guide`、`system`
- 额外要求：是否包含 tokens、是否包含前端实现建议、是否对比 light/dark

当用户没有指定输出模式时，使用 `guide`。只有缺失信息会显著改变结论时才追问；否则继续分析并明确列出假设。

## 输出模式

### brief

用于快速判断和方向提炼。输出：

- 页面类型
- 页面目标和用户主任务
- 结构骨架
- 核心视觉语言
- 核心组件
- 后续 AI 续写约束

### guide

标准模式。使用 `templates/output_template.md` 的完整结构，输出：

- Design Brief
- Structural System
- Visual System
- Component System
- Interaction Assumptions
- Design Tokens Draft
- Prompt Contract
- Confidence Split

### system

重度模式。在 `guide` 基础上加强：

- component anatomy
- semantic tokens
- reuse rules
- edge cases and failure modes
- frontend implementation hints

即使在 `system` 模式，也不要直接写完整代码，除非用户明确要求。

## 输出文件处理

完成分析后，必须将结果输出为 `DESIGN.md` 文件：

### 文件检查流程

1. **检查是否存在 DESIGN.md**
   - 使用 Read 工具检查当前目录是否已有 DESIGN.md

2. **根据情况询问用户**
   - 如果文件不存在：询问是否创建 DESIGN.md
   - 如果文件已存在：提供三个选项
     - **新建**：在当前目录创建 DESIGN.md（覆盖原文件）
     - **覆盖**：完全替换现有内容
     - **融合**：保留原有内容，将新分析结果追加或合并

3. **执行操作**
   - 新建/覆盖：使用 Write 工具直接写入
   - 融合：先读取原文件，智能合并后写入

### 融合策略

当用户选择"融合"时：
- 保留原有的 Design Brief 和核心结构
- 新增或更新 Component System 中的组件
- 合并 Design Tokens，标注来源
- 追加新的 Prompt Contract 规则
- 在文档开头添加更新日志

## 工作流

### Step 1: 判断页面类型和意图

先判断页面属于哪类，再进入视觉提炼。必要时读取 `references/page_types.md`。

必须识别：

- 页面类型
- 产品或业务目标
- 用户主任务
- 主阅读路径和辅助路径
- 页面是展示型、操作型、浏览型还是混合型

### Step 2: 抽象结构系统

把截图从“画面”转成布局骨架：

- 页面一级区域
- 主次内容关系
- 栅格、列宽、容器推断
- 模块组织逻辑
- 信息密度策略
- 扫描路径和注意力引导

### Step 3: 提炼视觉系统

用设计系统语言描述视觉，不写空泛审美评价。

必须提炼：

- 主题特征
- 色彩策略
- 字体层级
- 间距节奏
- 圆角系统
- 边框与阴影系统
- light/dark 映射关系，如适用

不要编造无法确认的精确值。可以给近似值，但必须标注为“估计”。

### Step 4: 提炼组件系统

对每个重要组件描述：

- 作用
- 结构
- 层级
- 复用规则
- 可变项
- 不可变项

常见组件包括：

- 导航栏
- Hero
- 搜索
- 按钮
- 标签/分类
- 卡片
- 列表/趋势/数据模块
- 侧栏
- 图表
- 分页
- 页脚

只分析截图中存在或强相关的组件，不要为了填模板虚构组件。

### Step 5: 推断交互模式

从截图中推断交互规则，并明确它们是推断：

- hover
- focus
- active
- 筛选和导航切换
- 主题切换
- 动效节奏
- 状态反馈

### Step 6: 输出可复用资产

必须输出四类核心资产：

- Design Brief
- Design Guide
- Design Tokens Draft
- Prompt Contract

tokens 使用 `templates/tokens_template.yaml` 的结构。不要把 tokens 写成最终权威值；除非截图或用户明确给出数值，否则标记为草案或估计。

### Step 7: 质量自检

完成后用 `templates/rubric.md` 检查输出是否达标。不要把完整评分过程展开成冗长报告；只在需要时给出简短自检结论或风险提示。

### Step 8: 输出到 DESIGN.md

分析完成后，必须执行以下流程：

#### 8.1 文件格式：双层结构

输出文件采用 **YAML Front Matter + Markdown Body** 的双层结构：

**YAML Front Matter（机器可读层）**：
```yaml
---
colors:
  brand:
    primary: "#3B82F6"
    primaryHover: "#2563EB"
  background:
    default: "#FFFFFF"
    surface: "#F9FAFB"
  text:
    primary: "#111827"
    secondary: "#6B7280"

typography:
  fontFamily:
    base: "Inter, system-ui, sans-serif"
  fontSize:
    h1: "36px"
    body: "14px"
  fontWeight:
    regular: 400
    semibold: 600

spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"

components:
  button:
    primary:
      backgroundColor: "{colors.brand.primary}"
      textColor: "#FFFFFF"
      padding: "12px 24px"
      rounded: "8px"
---
```

**优势**：
- AI 可直接解析 YAML 获取精确值
- 人类可阅读 Markdown 理解设计理念
- 一份文件同时服务 AI 和人类

**Markdown Body（人类可读层）**：
- Overview：页面类型、目标、用户任务
- Colors：色彩策略和使用场景
- Typography：字体层级和排版规则
- Layout：布局系统和栅格
- Components：组件详细说明
- Interaction：交互模式
- Prompt Contract：AI 延续设计约束

#### 8.2 Token 引用系统

使用 `{path.to.token}` 语法建立引用关系：
- 组件引用基础 token：`backgroundColor: "{colors.brand.primary}"`
- 避免硬编码重复值
- 修改一处，全局生效
- 提高可维护性

#### 8.3 章节顺序（固定）

1. Overview
2. Colors
3. Typography
4. Layout
5. Elevation & Depth（如适用）
6. Shapes
7. Components
8. Interaction Patterns
9. Prompt Contract
10. Confidence Split

**固定顺序的优势**：
- 标准化输出，易于解析
- 便于版本对比
- 降低认知负担

#### 8.4 文件操作流程

1. **检查文件是否存在**
   ```
   使用 Read 工具检查当前目录的 DESIGN.md
   ```

2. **询问用户操作方式**
   - 如果文件不存在：
     - 询问："是否创建 DESIGN.md 文件保存设计规范？"
   
   - 如果文件已存在：
     - 使用 AskUserQuestion 提供三个选项：
       - **新建**：创建新的 DESIGN.md（覆盖原文件）
       - **追加**：在原文件末尾追加新的分析结果
       - **融合**：智能合并原有内容和新分析结果

3. **执行对应操作**
   - **新建/覆盖**：直接使用 Write 工具写入完整内容（YAML + Markdown）
   - **追加**：使用 Edit 工具在文件末尾添加新内容，包含时间戳和分隔符
   - **融合**：
     - 读取原文件内容
     - 合并 YAML Front Matter（保留原有 token，标注新增）
     - 保留原有 Overview
     - 合并 Components（去重，标注来源）
     - 追加新的 Prompt Contract 规则
     - 在文档开头添加更新日志

4. **确认完成**
   告知用户文件已保存，并说明保存位置和操作类型。

## Prompt Contract 要求

Prompt Contract 是这个 skill 的关键产物。它必须说明后续 AI 继续生成页面时：

- 必须继承的页面类型和信息架构
- 必须复用的组件骨架
- 必须保持的视觉系统
- 可以变化的局部内容
- 禁止破坏的布局和风格边界
- 对装饰、动效、主题切换、组件扩展的约束

Prompt Contract 要写成后续 AI 可以直接遵守的规则，不要写成模糊建议。

## 观察、推断与未知

始终区分三类信息：

- 直接观察：截图中明确可见的事实。
- 高概率推断：基于 UI 经验和上下文得出的判断。
- 无法确认：截图不足以证明的部分。

不要把推断写成事实。不要因为模板需要而补齐不存在的内容。

## 禁止项

必要时读取 `references/anti_patterns.md`。始终避免：

- 泛泛审美评价，例如只说“简洁、高级、现代”
- 只总结颜色和字体
- 混淆观察和推断
- 编造精确 hex、字体名、尺寸
- 把所有页面套成同一种结构
- 直接跳到前端代码
- 无依据加入玻璃拟态、复杂发光、噪点、过度渐变

## 输出风格

- 专业、结构化、直接。
- 以实现价值为目标，而不是审美评论。
- 优先写规则、结构和约束，再写视觉感受。
- 对不确定项诚实标注。
- 内容应能直接作为后续设计、前端实现或 AI 续写的输入。
