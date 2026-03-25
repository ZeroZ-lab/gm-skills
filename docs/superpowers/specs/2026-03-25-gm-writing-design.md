# gm-writing Design

## Goal

Create a single `gm-writing` skill that packages the Guanmu writing method into a reusable writing workflow.

The skill should auto-trigger mainly for requests to rewrite or strengthen an existing draft with more:

- system structure
- mechanism explanation
- judgment
- practical paths
- critical reflection

It should still support manual invocation for explicit "write from scratch with Guanmu style" requests, but that is not the default trigger.

## Primary Use Case

The default job is:

- take an existing article draft
- diagnose what is structurally weak
- choose the right Guanmu template
- rewrite or deepen the draft at the structure level rather than only polishing sentences

## Trigger Boundary

The skill should trigger for requests like:

- use Guanmu style to rewrite this draft
- make this article more systematic
- strengthen mechanism and judgment
- turn this into a more structured long-form article
- add practical path and critical reflection

The skill should not be the default choice for:

- topic ideation only
- X/Twitter hooks
- pure de-AI cleanup without structural rewriting
- lightweight copy polishing

## Modes

### `draft-rewrite`

Default mode.

Activated when the user provides a draft, partial draft, or rough article sections.

### `from-scratch`

Secondary mode.

Activated only when the user clearly asks to write a new article directly with the Guanmu method.

## Template System

The skill should expose the four Guanmu templates:

1. Professional knowledge
2. Thought essay
3. Strategic analysis
4. Creative practice

Default to the professional knowledge template unless the topic clearly fits another template or the user explicitly requests one.

## Core Workflow

1. Diagnose the draft
2. Select template and strength
3. Rebuild the opening around tension or contradiction
4. Add system model and mechanism explanation
5. Add practice path, rhythm, or priorities
6. Add critique of weak framings or fake solutions
7. Close with a principle-level takeaway

## Output Shape

Default output should include:

1. Diagnosis summary
2. Rewrite strategy
3. Rewritten draft

For long drafts, partial deep rewrite is acceptable if the skill clearly states what was changed and what was left untouched.

## Non-Goals

- pretend to preserve all of the original wording
- invent cases or evidence the user did not provide
- replace `gm-de-ai-article`, `gm-topic-engine`, or `gm-x-hook-writer`
