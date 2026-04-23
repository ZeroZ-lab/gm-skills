# ui-fork 示例

本目录包含 ui-fork skill 的示例输入和输出。

## 示例说明

由于示例需要实际的 UI 截图，这里提供示例结构说明。

### 使用方式

1. 准备你的 UI 截图
2. 运行 `/ui-fork [mode] screenshot.png`
3. 获得结构化的设计系统规范

### 示例场景

#### 场景 1：导航聚合型网站
- **输入**：类似 Product Hunt、Hacker News 的导航首页截图
- **输出**：提炼信息架构、卡片系统、标签系统、侧栏辅助发现机制
- **模式**：`guide`

#### 场景 2：Dashboard 看板
- **输入**：数据看板截图
- **输出**：提炼数据层级、图表权重、筛选逻辑、指标与趋势模块关系
- **模式**：`system`

#### 场景 3：官网首页
- **输入**：SaaS 产品官网截图
- **输出**：提炼品牌叙事、信息节奏、section pattern、CTA 层级
- **模式**：`brief`

## 输出文件命名规范

```
<page-type>_<mode>_input.png
<page-type>_<mode>_output.md
<page-type>_<mode>_tokens.yaml  (仅 system 模式)
```

例如：
- `directory_guide_input.png`
- `directory_guide_output.md`
- `dashboard_system_input.png`
- `dashboard_system_output.md`
- `dashboard_system_tokens.yaml`

## 快速测试

如果你想快速测试 ui-fork，可以：

1. 找一个你喜欢的网站截图
2. 运行 `/ui-fork screenshot.png`
3. 查看生成的设计系统规范
4. 将规范用于后续 AI 设计或前端实现
