# gm-writing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `gm-writing` skill that auto-triggers for Guanmu-style draft rewriting and also supports manual invocation.

**Architecture:** A single `skills/gm-writing/SKILL.md` file carries the workflow, mode selection, template system, defaults, and output contract. A focused shell smoke test checks discoverability and key prompt terms. README is updated so install and usage docs stay aligned with the repository contents.

**Tech Stack:** Markdown skill files, shell smoke tests, repository README.

---

## File Map

| File | Action | Responsibility |
|------|--------|----------------|
| `test/gm_writing_skill_test.sh` | Create | Verify the new skill file exists and exposes key trigger text and workflow sections |
| `skills/gm-writing/SKILL.md` | Create | Define the Guanmu writing workflow, boundaries, templates, defaults, and output format |
| `README.md` | Modify | Document the new skill in the repository skill list and structure summary |

---

### Task 1: Add a failing smoke test

**Files:**
- Create: `test/gm_writing_skill_test.sh`

- [ ] **Step 1: Write a smoke test that asserts `skills/gm-writing/SKILL.md` exists**
- [ ] **Step 2: Assert frontmatter contains `name: gm-writing` and an `argument-hint`**
- [ ] **Step 3: Assert the body names the default `draft-rewrite` mode and the four templates**
- [ ] **Step 4: Run `sh test/gm_writing_skill_test.sh` and verify it fails before implementation**

---

### Task 2: Implement the skill

**Files:**
- Create: `skills/gm-writing/SKILL.md`

- [ ] **Step 1: Add frontmatter optimized for auto-triggering and manual invocation**
- [ ] **Step 2: Document the default rewrite mode and explicit from-scratch mode**
- [ ] **Step 3: Define template selection rules and output format**
- [ ] **Step 4: Add boundary rules so the skill does not overlap with topic, hook, or de-AI skills**

---

### Task 3: Update repository docs

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add `gm-writing` to the skills table**
- [ ] **Step 2: Update the structure summary to include the new skill**

---

### Task 4: Verify

**Files:**
- Test: `test/gm_writing_skill_test.sh`

- [ ] **Step 1: Run `sh test/gm_writing_skill_test.sh` and verify it passes**
- [ ] **Step 2: Re-run a broader repo smoke check if the current local test file set is usable**
