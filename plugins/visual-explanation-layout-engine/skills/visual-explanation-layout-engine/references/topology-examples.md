# Topology Examples

Use this file only to choose the topology and identify the main reading path.

## State Machine

Use when the reader must understand allowed state transitions.

Example:

```text
STATE A -> STATE B -> STATE C -> END
             |
      EXCEPTION / COMPENSATION
```

Main row:

- STATE A
- STATE B
- STATE C
- END

Secondary row:

- EXCEPTION
- COMPENSATION

Typical routes:

- `right-left` for main flow
- `left-down` for terminal exceptions
- `side-channel` for compensation branches

## Swimlane

Use when responsibility matters more than pure sequence.

Rows:

- Actor A
- Actor B
- Actor C
- Actor D
- Actor E

Columns:

- Start
- Request
- Confirm
- Notify
- Finish

Typical routes:

- `right-left` within the same lane family
- `bottom-top` when the main reading path moves vertically
- `outer-right` for async callback rails

## Flowchart

Use when the reader must understand a mostly linear procedure with one or two branching decisions.

Typical shape:

```text
Start -> Validate -> Decide -> Process -> Finish
                     |
                  Retry / Escalate
```

Typical routes:

- `right-left` for the main horizontal path
- `bottom-top` when the flow is stacked vertically
- `left-down` for exception or retry branches

## Layered Architecture

Use when the reader must understand responsibility boundaries by abstraction level.

Layers:

- Interface
- Orchestration
- Services
- Data / Infrastructure

Typical rules:

- vertical position indicates abstraction
- same layer nodes share size and style
- routes should mainly move downward or across nearby layers

## Hub-And-Spoke

Use when one central coordinator interacts with surrounding modules.

Example:

```text
       Module A
          |
Input -> Hub -> Module B
          |
       Module C
```

Typical rules:

- center node is visually dominant
- spokes are grouped by function
- avoid turning the diagram into a spider web
- keep spoke relationship labels specific, not generic
