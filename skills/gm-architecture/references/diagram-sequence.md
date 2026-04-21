# Sequence Diagram — Complete Reference

## Overview

Sequence diagrams show interactions between actors over time. They are ideal for visualizing message flows, API calls, protocol exchanges, and any scenario where the order of communication matters.

## When to Use

- API call flows and request/response patterns
- Distributed system interactions
- Protocol explanations (OAuth, WebSocket handshake)
- Login/authentication flows
- Microservice communication
- Debugging message ordering issues
- Documenting error/retry paths

## JSON Schema

See `assets/schema-sequence.json` for the formal schema.

Key structure:
```json
{
  "title": "User Login Flow",
  "diagramType": "sequence",
  "style": "dark-professional",
  "format": "html",
  "actors": [
    { "id": "user", "label": "User", "type": "actor" },
    { "id": "client", "label": "Client", "type": "participant" }
  ],
  "messages": [
    { "from": "user", "to": "client", "label": "Enter credentials", "type": "sync", "order": 1 }
  ],
  "fragments": [
    { "id": "auth-check", "type": "alt", "label": "alt", "condition": "[valid]", "children": [5,6], "else": { "condition": "[invalid]", "children": [7,8] } }
  ]
}
```

## Key Fields

| Field | Required | Description |
|-------|----------|-------------|
| `title` | Yes | Diagram title |
| `diagramType` | Yes | Must be `"sequence"` |
| `style` | Yes | Visual style preset |
| `format` | No | Output format (default: `"html"`) |
| `actors` | Yes | Array of actor objects (min 2) |
| `messages` | Yes | Array of message objects (min 1) |
| `fragments` | No | Interaction fragments (alt, loop, opt, par) |

## Actor Types

| Type | Visual | Use for |
|------|--------|---------|
| `actor` | Stick figure | Human users |
| `participant` | Rectangle | Services, systems |
| `boundary` | Rectangle with boundary marker | System edges, API gateways |
| `control` | Rectangle with control marker | Controllers, handlers |
| `entity` | Rectangle with entity marker | Database, storage |

## Message Types

| Type | Arrow Style | Use for |
|------|-------------|---------|
| `sync` | Solid filled arrow | Synchronous request |
| `async` | Open arrow | Asynchronous message |
| `return` | Dashed arrow | Response/return value |
| `create` | Dashed to new lifeline | Object creation |
| `destroy` | X on lifeline | Object destruction |

## Fragment Types

| Type | Meaning |
|------|---------|
| `alt` | Alternative (if/else) |
| `loop` | Repeated interaction |
| `opt` | Optional (skip if condition false) |
| `par` | Parallel interactions |
| `critical` | Critical region (single-threaded) |

## Layout Rules

See `references/layout-sequence.md` for coordinate calculations.

Constants:
- `ACTOR_GAP`: 150px between actors
- `MSG_GAP`: 40px between messages
- `ACTIVATION_W`: 12px activation bar width

## Component Templates

See `references/components-sequence.md` for SVG snippets.

## Style Templates

All 6 styles apply.

| Style | Recommended for Sequence |
|-------|-------------------------|
| dark-professional | API docs, technical articles |
| blueprint | Protocol specs |
| light-corporate | Enterprise integration docs |
| hand-drawn | Teaching, whiteboarding |
| cyberpunk-neon | Developer tools |
| warm-cozy | Tutorials, onboarding |

## Generation Workflow

1. Extract actors and messages from the user's description
2. Order messages by the `order` field
3. Identify fragments (alt, loop, etc.)
4. Choose style (default: dark-professional)
5. Compute layout: actor positions → lifeline lengths → message y-coordinates → fragment bounds
6. Build SVG using `components-sequence.md` snippets
7. Wrap in HTML using the style's template file

## Examples

- `assets/examples/sequence-login.json` — User login flow (4 actors, 10 messages, 1 alt)
- `assets/examples/sequence-order.json` — Order processing (5 actors, 9 messages)
