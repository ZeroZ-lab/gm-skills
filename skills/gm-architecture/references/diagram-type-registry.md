# Diagram Type Registry

All supported diagram types with their trigger keywords, schema files, and reference files.

## Registry

| Type | Schema | Diagram Reference | Layout Rules | Components | Trigger Keywords |
|------|--------|-------------------|-------------|------------|-----------------|
| `architecture` | `assets/schema-architecture.json` | `references/diagram-architecture.md` | `references/layout-rules.md` | `references/component-templates.md` | architecture, system diagram, infrastructure, layered, component, platform, microservice, tech stack, 分层架构, 系统架构, 架构图 |
| `flowchart` | `assets/schema-flowchart.json` | `references/diagram-flowchart.md` | `references/layout-flowchart.md` | `references/components-flowchart.md` | flowchart, flow chart, decision tree, process flow, algorithm, branching, 流程图, 决策树, 流程 |
| `mindmap` | `assets/schema-mindmap.json` | `references/diagram-mindmap.md` | `references/layout-mindmap.md` | `references/components-mindmap.md` | mind map, mindmap, brainstorm, concept map, feature tree, roadmap, 思维导图, 头脑风暴, 概念图 |
| `er` | `assets/schema-er.json` | `references/diagram-er.md` | `references/layout-er.md` | `references/components-er.md` | ER diagram, entity relationship, database schema, data model, table relationship, ER图, 数据库设计, 实体关系 |
| `sequence` | `assets/schema-sequence.json` | `references/diagram-sequence.md` | `references/layout-sequence.md` | `references/components-sequence.md` | sequence diagram, interaction diagram, message flow, API flow, protocol, 时序图, 序列图, 交互图 |
| `gantt` | `assets/schema-gantt.json` | `references/diagram-gantt.md` | `references/layout-gantt.md` | `references/components-gantt.md` | gantt, timeline, schedule, milestone, project plan, 甘特图, 时间线, 项目计划 |
| `uml-class` | `assets/schema-uml-class.json` | `references/diagram-uml-class.md` | `references/layout-uml-class.md` | `references/components-uml-class.md` | UML, class diagram, OOP, inheritance, interface, 类图, UML图, 继承关系 |
| `network` | `assets/schema-network.json` | `references/diagram-network.md` | `references/layout-network.md` | `references/components-network.md` | network, topology, infrastructure, subnet, VLAN, 网络拓扑, 网络架构, 服务器 |
| `card` | `assets/schema-card.json` | `references/diagram-card.md` | `references/layout-card.md` | `references/components-card.md` | social card, knowledge card, comparison card, quote card, ranked list, 知识卡片, 社交卡片, 对比卡片, 引用卡片, 排行卡片 |

## Shared Resources

All diagram types share:
- **12 visual styles**: `references/style-*.md` + `assets/template-*.html`
- **Design system**: `references/design-system.md`
- **Icon catalog**: `references/icons-catalog.md`
- **Output formats**: `references/output-svg.md`, `references/output-mermaid.md`, `references/output-png-pdf.md`

## Output Format

All schemas include an optional `format` field:
```json
{
  "format": "html"  // "html" | "svg" | "mermaid" (default: "html")
}
```

PNG and PDF are generated via `scripts/export.sh` after creating HTML or SVG.
