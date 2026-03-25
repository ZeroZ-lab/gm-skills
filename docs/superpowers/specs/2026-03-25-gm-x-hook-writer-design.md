# gm-x-hook-writer Design

## Goal

Strengthen `gm-x-hook-writer` so its workflow reliably produces distinct, non-fabricated hooks under weak materials, no-explanation requests, and batch output requests.

## Primary Problems

- The current workflow can skip core-claim extraction and jump straight to writing.
- Angle selection is descriptive, so many outputs collapse into synonym rewrites.
- Boundary handling is too loose when the user actually wants a full tweet or thread.
- Weak-material and batch-output scenarios do not have explicit failure handling.

## Design

### Boundary Gate

Add a first-step classification:

- `hook-only`
- `hook + follow-up line`
- full-post request

The skill still only delivers the hook layer. Full-post requests should receive the hook first, then a brief boundary reminder.

### Core Sentence Gate

The workflow must define a pass condition for the core sentence. If the source material cannot support a strong core sentence, the skill enters conservative mode instead of silently lowering the bar.

### Conservative Mode

Conservative mode must define:

- what angles remain allowed
- which high-risk angles are disabled
- how output quantity can shrink instead of padding with weak hooks

### Executable Difference Test

Angle diversity must be checked by observable dimensions rather than by “don’t rewrite the same sentence.” Hooks should differ on at least two dimensions before both are kept.

### Filter Priority

The skill must resolve the tension between “short” and “information-dense” by making brevity subordinate to minimum information content.

### Batch Mode

When the user asks for many hooks or says “no explanation,” the workflow should keep the same internal gate and filtering standards. If not enough hooks survive, the skill should return fewer rather than pad with near-duplicates.

## Validation

Add a shell smoke test that asserts the rewritten skill documents:

- boundary classification
- core-sentence pass/fail handling
- conservative mode and high-risk angle restrictions
- executable difference testing
- short-vs-information priority
- no-explanation behavior
- batch-output anti-padding rule
