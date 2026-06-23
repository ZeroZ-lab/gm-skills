# Identity is determined by Source of Truth, not by name

## Context

The machine has skills/plugins spread across codex, claude code, and zcode. To do anything useful — dedupe, sync, version-align, or detect conflicts — the manager needs a rule for "is this entry in codex the *same capability* as that entry in claude?"

## Decision

Two installed entries are the **same capability** if and only if their real files resolve to the same normalized Remote Source and canonical `SKILL.md` path. Revision is tracked separately: the same skill path at two commit SHAs is one Capability at two Revisions, not two capabilities. Name alone is **not** identity: two `cc-design`s from different repos are different capabilities. Codex Plugin, Claude Code Plugin, and `npx skills` may therefore install the same Capability through different Installation Channels.

## Why

- Names collide. Real example on this machine: `skill-creator` exists as a codex built-in, a claude plugin, and a zcode plugin — three different authors/sources. Treating them as "the same skill" would be wrong.
- Source is verifiable. Every managed remote entry can be traced to a Remote Source plus canonical `SKILL.md` path; built-ins use Runtime Identity plus built-in path. Registry `gitCommitSha`, content hash, and version provide Revision evidence. Name is just a label.
- It makes sync meaningful: "sync capability X across runtimes" = "make sure every runtime has an install whose files resolve to X's SoT."
- It makes version drift visible: installs sharing a Capability Identity can be compared by Revision.

## Consequences

The manager **must** be able to resolve every entry's Source of Truth. This forces an explicit resolution step:

- Remote install → read the Codex Plugin, Claude Code Plugin, or `npx skills` registry; Capability Identity is `<normalized remote>:<canonical SKILL.md path>`, while Revision is commit SHA, content hash, or version evidence.
- Built-in → Capability Identity is `<runtime identity>:<built-in path>` and Revision is the runtime version. Different built-ins in one runtime remain distinct, while the same built-in remains one capability across runtime upgrades. Built-ins are never "the same as" any installable capability.

Entries that cannot be resolved to a SoT, including orphaned links and unmanaged local directories, are flagged, not silently grouped.

Runtime metadata that contains only a marketplace label, name, version, cache path, or other partial facts is **Observed Evidence**, not Capability Identity. When marketplace source or plugin path cannot be established reliably, identity remains **Unresolved**. The Manager must not complete identity from name, guess cross-runtime equality, or include unresolved entries in deduplication and sync decisions.

When two installs have the same Capability Identity but either Revision is missing or the Revisions are not comparable, their Revision Relation is `unknown` and Sync Status is `indeterminate`. They may be grouped as the same Capability, but the Manager must not claim version equality or drift and must not automatically overwrite either install.
