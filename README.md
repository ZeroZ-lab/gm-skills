# gm-skills

Personal Claude Code plugin — a curated collection of skills for development workflow, documentation, and agent collaboration.

## Skills

### Dev Workflow
| Command | Description | Trigger |
|---------|-------------|---------|
| `/gm:gm-code-review` | Review code for bugs, security, style, maintainability | Auto or manual |
| `/gm:gm-pr-summary [branch]` | Generate structured PR description from git diff | Manual |
| `/gm:gm-debug-assist` | Systematic debugging: reproduce → locate → hypothesize → fix | Auto or manual |

### Documentation
| Command | Description | Trigger |
|---------|-------------|---------|
| `/gm:gm-write-doc` | Write or improve technical docs (README, API, guides) | Auto or manual |
| `/gm:gm-changelog [version]` | Generate user-facing changelog from git history | Manual |

### Agent / Planning
| Command | Description | Trigger |
|---------|-------------|---------|
| `/gm:gm-brainstorm [topic]` | Structured brainstorm: diverge → converge → rank | Manual |
| `/gm:gm-write-plan` | Break a goal into an actionable plan with steps and risks | Manual |
| `/gm:gm-research [topic]` | Deep research: collect → analyze → synthesize | Manual |

## Install

```bash
./install.sh
```

This links each directory under `skills/` into `~/.claude/skills/`.
The script prints progress logs and exits with an error if a target path already exists but is not the expected symlink.

## Uninstall

```bash
./uninstall.sh
```

This removes only the symlinks in `~/.claude/skills/` that point back to this repository's `skills/` entries.
The script prints which links were removed and which unrelated links were skipped.

## Structure

```
gm-skills/
├── .claude-plugin/
│   └── plugin.json       # Plugin identity
├── skills/
│   ├── gm-template/      # Copy this to create new skills
│   ├── gm-code-review/
│   ├── gm-pr-summary/
│   ├── gm-debug-assist/
│   ├── gm-write-doc/
│   ├── gm-changelog/
│   ├── gm-brainstorm/
│   ├── gm-write-plan/
│   └── gm-research/
└── README.md
```

## Adding New Skills

1. Copy `skills/gm-template/` to `skills/gm-your-skill-name/`
2. Edit `SKILL.md` — update `name` to `gm-your-skill-name`, update `description` and instructions
3. The skill becomes available as `/gm:gm-your-skill-name`

Key frontmatter fields:
- `name` — must match directory name, becomes the slash command
- `description` — drives auto-invocation; include keywords users naturally say
- `argument-hint` — shown in autocomplete (e.g., `[topic]`)
- `context: fork` — run in isolated subagent (good for long tasks)
- `allowed-tools` — pre-approve tools without permission prompts
- `disable-model-invocation: true` — require explicit invocation only
