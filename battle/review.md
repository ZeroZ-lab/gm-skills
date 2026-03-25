# gm-skills Documentation Review

Reviewed on 2026-03-25.

## Findings

### Major

1. Command naming is still inconsistent across the repository.
   - `README.md` documents commands such as `/gm:gm-changelog` and `/gm:gm-write-plan`.
   - `skills/gm-changelog/SKILL.md` still references `/gm:changelog [version]`.
   - `skills/gm-write-plan/SKILL.md` still references `/gm:write-plan`.
   - `skills/gm-template/SKILL.md` comments still describe the old `/gm:skill-name` convention.
   - Impact: the repository now mixes two command schemes, so future edits are likely to drift further and users may follow the wrong examples.

### Minor

1. `battle/review.md` had become stale after earlier documentation fixes.
   - The previous review still reported issues that have already been corrected in `README.md`, `skills/gm-code-review/SKILL.md`, and `skills/gm-write-doc/SKILL.md`.
   - Impact: keeping outdated review notes in the repo creates confusion about which problems are still open.

## Open Question

- Is `/gm:gm-*` the intended long-term command format, or should the user-facing commands be `/gm:code-review`, `/gm:write-plan`, and similar? The repository is currently split between those two conventions.

## Summary

The documentation is in much better shape than the previous review. The main remaining issue is naming consistency: README, individual skills, and the template should all commit to the same slash-command format. After that, the docs will be substantially more coherent.
