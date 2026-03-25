# gm-x-hook-writer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `gm-x-hook-writer` robust against all 7 battle issues by tightening workflow gates and adding a focused smoke test.

**Architecture:** A dedicated shell smoke test locks the workflow contract. The skill document is rewritten to add boundary classification, gate failure behavior, conservative mode, executable angle-difference rules, and batch-output safeguards.

**Tech Stack:** Markdown skill files, shell smoke tests.

---

## File Map

| File | Action | Responsibility |
|------|--------|----------------|
| `test/gm_x_hook_writer_skill_test.sh` | Create | Assert the skill documents the new workflow gates and safeguards |
| `skills/gm-x-hook-writer/SKILL.md` | Modify | Define the strengthened x-hook workflow and output contract |

### Task 1: Add a failing smoke test

**Files:**
- Create: `test/gm_x_hook_writer_skill_test.sh`

- [ ] **Step 1: Assert the x-hook skill file exists and exposes its frontmatter**
- [ ] **Step 2: Assert the skill documents boundary classification and conservative mode**
- [ ] **Step 3: Assert the skill documents executable difference checks and batch-mode safeguards**
- [ ] **Step 4: Run `sh test/gm_x_hook_writer_skill_test.sh` and verify it fails before the skill rewrite**

### Task 2: Rewrite the skill workflow

**Files:**
- Modify: `skills/gm-x-hook-writer/SKILL.md`

- [ ] **Step 1: Update frontmatter and overview for clearer triggering and boundary handling**
- [ ] **Step 2: Add boundary classification, core-sentence gate, and conservative mode**
- [ ] **Step 3: Add executable angle-difference and filtering rules**
- [ ] **Step 4: Update output rules for no-explanation and batch requests**

### Task 3: Verify

**Files:**
- Test: `test/gm_x_hook_writer_skill_test.sh`

- [ ] **Step 1: Run `sh test/gm_x_hook_writer_skill_test.sh` and verify it passes**
- [ ] **Step 2: Re-run `sh test/skills_smoke_test.sh` to make sure broader skill checks still pass**
