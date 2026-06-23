# The Manager is an agent skill, not a human-operated CLI

## Context

The Manager could be built two ways:
1. A **CLI** the Operator types at (`skills-mgr install xxx --to codex`), with formal args, exit codes, transactions.
2. An **agent skill** (a SKILL.md) that an agent reads and then executes per-runtime operations itself, driven by the Operator's natural-language requests.

## Decision

Build it as an **agent skill**, not a CLI or a fourth installer. The Operator says things like "把我电脑上的 skills 整理一下" or "把 gm-skills 装到所有 runtime"; the Manager reads native evidence, coordinates the appropriate Codex, Claude Code, or `npx skills` operation, records a unified inventory, and verifies the result.

## Why

- The pain being solved is **"I can't keep track of skills across three runtimes"** — a *comprehension and judgment* problem, not a *typing* problem. An agent that can look at the whole machine and reason about what's safe to change fits the pain; a CLI that requires the Operator to already know the exact target runtime/scope does not.
- The runtimes and `npx skills` have different config formats, scopes, registries, and native operations. Hard-fusing these into one installer forces lossy abstraction. An agent skill can select the correct native mechanism without taking ownership away from it.
- It composes with everything else already in this repo: the Manager is just another plugin in gm-skills, consumed the same way, and an agent is the natural executor.

## Consequences

- The Manager's primary artifact is a **SKILL.md that documents coordination and evidence rules**, not a binary. Any scripts are read-only inventory or verification helpers.
- The "command grammar" question (what args does install take?) is **downgraded** — there is no grammar. Instead the SKILL.md must teach the agent: for each runtime, the exact files/edits that constitute an install/uninstall, and the safety checks to run first.
- Native installers and registries remain authoritative. The Manager must not directly edit plugin registries, caches, lock files, or private runtime databases when a native operation exists.
- **Safety becomes paramount and explicit**: the Manager previews coordinated effects, invokes native operations, and verifies their records rather than emulating their mutations.
- Success is measured by "the Operator describes an outcome in their own words and the agent achieves it across runtimes," not by CLI ergonomics.
