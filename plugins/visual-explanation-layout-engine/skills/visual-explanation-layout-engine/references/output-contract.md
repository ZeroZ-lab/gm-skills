# Output Contract

Use this file after choosing topology and tokens, before writing final HTML.

## Required Decisions

State these decisions explicitly:

1. chosen topology
2. main reading path
3. minimum node schema
4. minimum edge schema
5. token scheme
6. label rail strategy
7. audit result
8. whether a legend or key is required
9. whether the artifact is a template or a case study

## Required Output Shape

- complete single-file HTML unless the user asks for a fragment
- SVG uses `viewBox`
- diagram built from structured `nodes[]` and `edges[]`
- tokens control spacing, radii, border widths, type sizes, and arrow sizes
- labels use rails or explicit `labelAt`
- final output remains readable on mobile
- title is present
- legend or key is present when notation is not self-evident
- template outputs remain domain-neutral unless the artifact is explicitly a case study

## Prohibited Shortcuts

- starting with raw SVG coordinates
- mixing route vocabulary arbitrarily
- ad hoc font-size changes on individual nodes
- labels placed at crowded path midpoints by habit
- skipping the anti-overlap audit
- entering the SVG workflow even though the request matches `non-goals.md`
- mixing case-study vocabulary into a template skeleton
