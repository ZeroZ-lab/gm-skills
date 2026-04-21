# ER Diagram — Complete Reference

## Overview

ER (Entity-Relationship) diagrams visualize database schemas — tables, columns, primary/foreign keys, and the relationships between entities. They map directly to relational database structure and are essential for data model documentation.

## When to Use

- Database schema design and documentation
- Entity relationship visualization
- Data model reviews before implementation
- ORM mapping documentation
- Explaining table relationships to stakeholders
- Migration planning (visualizing before/after)

## JSON Schema

See `assets/schema-er.json` for the formal schema.

Key structure:
```json
{
  "title": "E-Commerce Database",
  "diagramType": "er",
  "style": "blueprint",
  "format": "html",
  "entities": [
    {
      "id": "user",
      "label": "User",
      "attributes": [
        { "name": "id", "type": "int", "pk": true },
        { "name": "email", "type": "string", "nullable": false },
        { "name": "name", "type": "string" }
      ]
    }
  ],
  "relationships": [
    { "from": "user", "to": "order", "fromCard": "1", "toCard": "N", "label": "has many" }
  ]
}
```

## Key Fields

| Field | Required | Description |
|-------|----------|-------------|
| `title` | Yes | Diagram title |
| `diagramType` | Yes | Must be `"er"` |
| `style` | Yes | Visual style preset |
| `format` | No | Output format (default: `"html"`) |
| `entities` | Yes | Array of entity objects with attributes |
| `relationships` | No | Array of relationship objects with cardinality |
| `legend` | No | Auto-generated if omitted |

## Entity Fields

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique kebab-case identifier |
| `label` | Yes | Display name (table name) |
| `attributes` | Yes | Array of attribute objects |
| `icon` | No | Icon from catalog (e.g., `"database"`) |
| `color` | No | Hex color override |

## Attribute Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Column/field name |
| `type` | Yes | Data type (int, string, text, boolean, uuid, float, json, timestamp, date) |
| `pk` | No | Primary key marker |
| `fk` | No | Foreign key marker |
| `nullable` | No | Nullability (default: true) |

## Relationship Cardinality

| Value | Meaning | Notation |
|-------|---------|----------|
| `"1"` | Exactly one | `──|` |
| `"N"` | Many | `──<` or `──┤` |
| `"0..1"` | Zero or one | `──○` |

## Layout Rules

See `references/layout-er.md` for complete coordinate calculation formulas.

## Component Templates

See `references/components-er.md` for SVG snippets.

## Style Templates

All 6 styles apply. Blueprint is especially recommended for ER diagrams.

| Style | Recommended for ER |
|-------|-------------------|
| blueprint | Engineering specs, database docs |
| dark-professional | Technical articles |
| light-corporate | Enterprise docs |
| hand-drawn | Teaching, brainstorming |
| cyberpunk-neon | Developer tools |
| warm-cozy | Tutorials |

## Generation Workflow

1. Extract entities and their attributes from the user's description
2. Identify primary keys (pk) and foreign keys (fk)
3. Define relationships with cardinality (1, N, 0..1)
4. Choose style (default: blueprint for ER)
5. Compute layout using `layout-er.md` formulas
6. Build SVG using `components-er.md` snippets
7. Wrap in HTML using the style's template file

## Examples

- `assets/examples/er-ecommerce.json` — E-commerce database (6 entities, 6 relationships)
- `assets/examples/er-blog.json` — Blog system (5 entities, M:N via junction table)
