# Architecture Diagram JSON Schema Reference

This document defines the intermediate JSON schema used between architecture description extraction and SVG rendering.

## Overview

The schema has 5 main sections:

```
{
  title, subtitle, style,    → page metadata
  layers: [...],              → architectural layers (top-level)
  connections: [...],         → arrows between components
  groups: [...],              → boundary boxes around components
  legend: [...],              → legend entries
  metadata: {...}             → optional page metadata
}
```

## Component Types

Each component has a `type` that determines its visual style:

| Type | Color (dark theme) | Use for |
|------|-------------------|---------|
| `process` | Cyan (#22d3ee) | Processes, services, runtime components |
| `module` | Emerald (#34d399) | Libraries, sub-modules, functional units |
| `data` | Violet (#a78bfa) | Databases, caches, storage, data stores |
| `infra` | Amber (#fbbf24) | Infrastructure, cloud resources, platform services |
| `security` | Rose (#fb7185) | Auth, encryption, security boundaries |
| `channel` | Orange (#fb923c) | Message queues, IPC, event buses |
| `external` | Slate (#94a3b8) | External systems, third-party services, user clients |

## Layers

Layers are the primary organizational unit. Each layer renders as a horizontal band.

```json
{
  "id": "browser-process",        // required, unique, kebab-case
  "label": "Browser Process",      // required, display name
  "type": "process",               // required, component type
  "count": "single",               // optional: "single" or "multiple"
  "description": "Main process",   // optional, shown inside card
  "children": [...]                // optional, sub-modules
}
```

- `id` must be unique across the entire diagram (layers + modules + groups)
- `count: "multiple"` adds a stacked-cards visual effect to indicate multiple instances
- `children` are rendered horizontally within the layer band

## Modules (Children)

Modules are sub-components inside a layer.

```json
{
  "id": "v8",                     // required, unique
  "label": "V8 Engine",           // required
  "type": "module",               // required
  "description": "JavaScript",    // optional annotation
  "tech": ["JavaScript", "C++"]   // optional tech badges
}
```

- `tech` renders as small pill badges below the label
- `description` renders as small gray text below the label

## Connections

Connections define arrows between components (layers or modules).

```json
{
  "from": "browser-process",          // required, must be an existing id
  "to": "renderer-process",           // required, must be an existing id
  "label": "IPC",                      // optional, shown on the line
  "direction": "bidirectional",        // optional, default: "unidirectional"
  "style": "solid"                     // optional: "solid", "dashed", "dotted"
}
```

- `from` and `to` must reference valid `id` values from layers or modules
- `direction: "bidirectional"` renders arrows on both ends
- `style: "dashed"` typically represents async or optional connections

## Groups

Groups draw boundary boxes around multiple components.

```json
{
  "id": "aws-region",                  // required, unique
  "label": "AWS Region: us-east-1",    // required, shown on border
  "type": "region",                    // required: region, vpc, security-group, cluster
  "children": ["api-server", "db"]     // required, list of component ids
}
```

- `children` must reference existing layer or module ids
- Groups render as dashed borders around their children
- Group types determine border color: region=amber, vpc=amber, security-group=rose, cluster=cyan

## Legend

Legend entries can be auto-generated or manually specified.

```json
{
  "label": "Process",     // required
  "type": "process",      // optional, auto-derives color
  "color": "#22d3ee"      // optional, overrides type color
}
```

If `legend` is empty or omitted, auto-generate from the unique `type` values used in layers and modules.

## Validation Rules

1. All `id` values must be unique across the entire document
2. All `from`/`to` in connections must reference existing ids
3. All `children` in groups must reference existing ids
4. `layers` must have at least 1 entry
5. `layers[].id` must match pattern `^[a-z0-9][a-z0-9-]*$`

## Size Guidelines

| Architecture complexity | Layers | Modules per layer | Total modules |
|------------------------|--------|-------------------|---------------|
| Small | 2-3 | 1-3 | 4-8 |
| Medium | 3-5 | 2-4 | 8-15 |
| Large | 5-7 | 3-5 | 15-30 |

For diagrams larger than 30 modules, consider splitting into multiple sub-diagrams.
