# Topology Examples

## Payment State Machine

```text
CREATED -> PENDING -> PAID -> FULFILL
              |
       CLOSED / FAILED / REFUNDED
```

Use state machine topology.

Main row:

- CREATED
- PENDING
- PAID
- FULFILL

Exception row:

- CLOSED
- FAILED
- REFUNDED

Key constraints:

- Refund is a compensation flow.
- Failure and close are terminal or exception states.
- `PAID` should not be erased by `REFUNDED`.

## Payment Swimlane

Rows:

- User
- Merchant frontend
- Merchant backend
- Payment gateway or bank
- Async callback or fulfillment
- Exception handling

Columns:

- Submit
- Create order
- Create payment
- Pay
- Notify
- Fulfill

Key insight:

- Synchronous frontend result is not final.
- Backend callback or query determines final state.

## Agent Tool Workflow

Use swimlane or hub-and-spoke depending on intent.

Choose swimlane when responsibility matters:

```text
User -> Agent -> Tool -> External API -> Agent -> User
```

Choose hub-and-spoke when orchestration matters:

```text
        Memory
          |
User -> Agent -> Tools
          |
        Policy
```

## Value Flow

Use value-flow topology when the topic is money, data, power, risk, or bargaining position.

Example:

```text
User demand -> data entry -> model invocation -> workflow lock-in -> revenue power
```
