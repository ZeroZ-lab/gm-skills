# Battle Session ID Routing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert `gm-battle` and `gm-pk` from a single global battle state into multi-session battle flows addressed by `pk_id`.

**Architecture:** Persist each battle under `battle/sessions/<pk_id>/` with a `latest.json` index for the most recent unfinished session. `gm-battle` creates a new session and returns the `pk_id`; `gm-pk` accepts an optional `pk_id`, otherwise resolves the latest unfinished session and advances only that battle.

**Tech Stack:** Markdown skill docs, shell smoke tests

---

### Task 1: Lock New Expectations In Smoke Tests

**Files:**
- Modify: `test/skills_smoke_test.sh`
- Test: `test/skills_smoke_test.sh`

- [ ] Step 1: Add checks for `pk_id`, `battle/sessions/<pk_id>/...`, and `battle/latest.json`
- [ ] Step 2: Run `sh test/skills_smoke_test.sh` and confirm it fails before docs are updated

### Task 2: Update Skill Contracts

**Files:**
- Modify: `skills/gm-battle/SKILL.md`
- Modify: `skills/gm-pk/SKILL.md`

- [ ] Step 1: Update `gm-battle` to describe generating and returning `pk_id`
- [ ] Step 2: Update `gm-pk` to accept optional `pk_id` and resolve latest unfinished battle when omitted
- [ ] Step 3: Align all state paths with `battle/sessions/<pk_id>/...`

### Task 3: Update User-Facing Docs And Verify

**Files:**
- Modify: `README.md`
- Test: `test/skills_smoke_test.sh`

- [ ] Step 1: Update README command descriptions to mention `pk_id`
- [ ] Step 2: Run `sh test/skills_smoke_test.sh` and confirm it passes
