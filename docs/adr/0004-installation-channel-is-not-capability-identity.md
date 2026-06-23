# Installation Channel is not Capability Identity

Codex Plugin, Claude Code Plugin, and `npx skills` are different Installation Channels, not different capabilities. The Manager resolves each channel's metadata to a normalized Remote Source and canonical `SKILL.md` path; matching pairs identify the same Capability even when Runtime, marketplace label, cache path, scope, or packaging differ. Channel-specific metadata remains attached to each installation for update and removal operations.
