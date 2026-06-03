# Request Patterns

Use these templates to turn vague requests into inputs that fit this skill well.

## 1. State Machine Template

- Goal: explain how `[entity]` moves through allowed states
- Audience: `[audience]`
- Recommended topology: state machine
- Required inputs: `[main states]`, `[terminal states]`, `[exception states]`
- Optional inputs: `[compensation states]`, `[labels that clarify transitions]`
- Output expectation: single-file HTML + SVG with main row, secondary row, route labels, legend, and audit result

Prompt skeleton:

```text
Create a mobile-readable state machine for [entity]. Show [main states], [terminal states], and [exception states]. If present, place [compensation states] off the primary row. Make the main reading path obvious and keep labels specific.
```

## 2. Swimlane Template

- Goal: explain who does what and when
- Audience: `[audience]`
- Recommended topology: swimlane
- Required inputs: `[actors]`, `[handoff sequence]`, `[final owner]`
- Optional inputs: `[callback path]`, `[exception owner]`
- Output expectation: single-file HTML + SVG with rows as actors, specific relationship labels, and audit result

Prompt skeleton:

```text
Create a swimlane diagram for [process]. Use [actors] as rows. Show [handoff sequence] and make [final owner] explicit. If present, keep [callback path] on its own rail instead of blending it into the main lane.
```

## 3. Linear Flow Template

- Goal: explain a mostly linear procedure with one or two branches
- Audience: `[audience]`
- Recommended topology: flowchart
- Required inputs: `[main steps]`, `[branch trigger]`, `[branch outcome]`
- Optional inputs: `[retry step]`, `[terminal failure]`
- Output expectation: single-file HTML + SVG with a strong main path and a clearly separated branch row

Prompt skeleton:

```text
Create a flowchart for [procedure]. Show [main steps] on the primary path. Separate the branch triggered by [branch trigger] and show the result as [branch outcome]. If present, include [retry step] and [terminal failure] without weakening the main reading path.
```

## 4. Layered Architecture Template

- Goal: explain responsibility boundaries by abstraction
- Audience: `[audience]`
- Recommended topology: layered architecture
- Required inputs: `[layers]`, `[cross-layer relationships]`
- Optional inputs: `[shared service]`, `[persistence boundary]`
- Output expectation: single-file HTML + SVG with clear layer titles, consistent node sizing, and downward-biased routes

Prompt skeleton:

```text
Create a layered architecture diagram for [system]. Use [layers] as the responsibility boundaries. Show [cross-layer relationships] and keep the abstraction order readable without relying on surrounding narration.
```

## 5. Hub-And-Spoke Template

- Goal: explain how `[central coordinator]` interacts with surrounding modules
- Audience: `[audience]`
- Recommended topology: hub-and-spoke
- Required inputs: `[central coordinator]`, `[spoke groups]`, `[relationship meanings]`
- Optional inputs: `[outer rail relationship]`, `[grouping legend]`
- Output expectation: single-file HTML + SVG with a dominant center, grouped spokes, legend, and audit result

Prompt skeleton:

```text
Create a hub-and-spoke diagram for [central coordinator]. Group [spoke groups] around the center and label each relationship using [relationship meanings]. If present, keep [outer rail relationship] visually separate from the core spokes.
```
