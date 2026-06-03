# Failure Patterns

Use this file when the first layout pass fails review or audit.

## 1. Label Covers A Node

### Symptom

An edge label sits on top of a node body, title, or meta chip.

### Why It Fails

The label has no dedicated rail or the `labelAt` point was chosen from path midpoint habit instead of from available space.

### How To Fix

- move the label to a rail outside the node body
- increase `tokens.spacing.labelRailGap`
- reroute the edge through a clearer channel before moving individual coordinates

## 2. Secondary Routes Blend Into The Main Path

### Symptom

A branch, callback, or exception route looks like part of the primary reading path.

### Why It Fails

The secondary route uses the same channel and label position as the primary sequence.

### How To Fix

- move the secondary route to `outer-right`, `left-down`, or `side-channel`
- give the route its own label rail
- reduce visual competition by keeping the main path on the primary row or axis

## 3. Rows Feel Cramped

### Symptom

Main and secondary rows nearly touch, or labels are trapped between them.

### Why It Fails

`rowGap` is too small for the current node height, label chips, and route turns.

### How To Fix

- increase `tokens.spacing.rowGap`
- increase section height before shrinking type
- move the secondary row instead of nudging one node

## 4. Nodes Touch Container Edges

### Symptom

Bottom nodes, notes, or side nodes feel glued to the section frame.

### Why It Fails

The section does not leave enough `pad`, `innerBottomPad`, or `sectionToNoteGap`.

### How To Fix

- increase section height or width
- increase `innerBottomPad`
- increase `sectionToNoteGap`
- keep the frame stable and move the row or note area as a group

## 5. Peer Nodes Drift In Size Or Style

### Symptom

Same-level nodes use different widths, typography, or chip treatment without semantic reason.

### Why It Fails

Local adjustments replaced token discipline.

### How To Fix

- return peer nodes to the shared `tokens.node` and `tokens.font`
- only vary size when the difference encodes meaning
- remove one-off overrides before rebalancing layout

## 6. Color Meaning Breaks Down

### Symptom

The same color means different things in different parts of the same diagram.

### Why It Fails

Color is being used decoratively instead of semantically.

### How To Fix

- reassign each tone to one meaning only
- add or strengthen a legend when the mapping is not obvious
- keep secondary routes, exceptions, and neutral states visually distinct

## 7. Relationship Labels Are Too Generic

### Symptom

Labels say things like `Uses`, `Calls`, or `Data` without telling the reader what the relationship means.

### Why It Fails

The diagram assumes the surrounding narrative will do the explanatory work.

### How To Fix

- replace generic labels with specific action or state phrases
- name the direction or purpose of the relationship
- if the relationship is obvious, remove the label instead of keeping a weak one

## 8. Template Fields Are Incomplete

### Symptom

The template cannot stabilize because nodes, routes, or topology cues are underspecified.

### Why It Fails

The input omits the minimum structure needed to choose placement and routing rules.

### How To Fix

- return to `references/request-patterns.md`
- fill the required inputs before revising geometry
- do not compensate for missing structure with arbitrary coordinates

## 9. Case-Study Vocabulary Leaks Into A Template

### Symptom

The supposed template reads like a domain example rather than a reusable method skeleton.

### Why It Fails

The template uses case-study vocabulary instead of neutral placeholders and abstract roles.

### How To Fix

- replace domain nouns with topology-neutral placeholders
- move domain-specific content into a case study
- keep the template focused on layout method, not on one business scenario
