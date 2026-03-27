# gm-skills

Personal Claude Code plugin — a curated collection of skills for development workflow, documentation, and agent collaboration.

## Skills

### Content Workflow
| Command | Description | Trigger |
|---------|-------------|---------|
| `/gm:gm-battle [任务描述]` | 初始化一场双模型 battle，生成 `pk_id`，写入 `battle/sessions/<pk_id>/` 状态并生成第一条给 Agent A 的 prompt | Manual |
| `/gm:gm-pk [pk_id] [stop]` | 按 `pk_id` 推进 battle 到下一阶段；不传 `pk_id` 时默认使用 `battle/latest.json` 指向的最新 battle | Manual |
| `/gm:gm-topic-engine [ideas, notes, comments, drafts]` | Mine ranked WeChat/blog topics from messy source material, sharpen angles, and suggest the best next topic | Manual |
| `/gm:gm-de-ai-article [文章草稿]` | 为公众号和博客文章去除明显 AI 味，诊断模板化表达并改成更有作者感的版本 | Manual |
| `/gm:gm-x-hook-writer [topic, draft, observation]` | 为 X/Twitter 推文生成更有停留率和点击欲的开头 hook，输出推荐版本和备选版本 | Manual |
| `/gm:gm-writing [文章草稿或主题]` | 用关木写作法重写和增强已有草稿，补强结构、机制、判断、实践路径与原则收束；也可手动调用按四型模板起草 | Auto / Manual |
| `/gm:gm-harness-init [目标项目，例如：为 skills manager 创建 harness]` | 为 AI harness 项目生成清晰的 harness / target project / `.harness/` 三层边界、最小闭环结构与创建顺序 | Manual |
| `/gm:gm-harness-plan-task [需求描述，例如：给 skills manager 加登录功能]` | 把用户需求转化为 `.harness/` 里的正确文档更新（新建 contract、更新 spec 或 project-rules），并给出可直接运行的命令 | Manual |

## Install

```bash
./install.sh
./install.sh claude
./install.sh codex
./install.sh agent
./install.sh all
```

If no argument is provided, the script prompts you to choose a target.
Supported targets:
- `claude` -> `~/.claude/skills`
- `codex` -> `~/.codex/skills`
- `agent` -> `~/.agents/skills`
- `all` -> installs into all three locations

The script links each directory under `skills/` into the selected target's `skills` directory.
It prints progress logs and exits with an error if a target path already exists but is not the expected symlink.

## Uninstall

```bash
./uninstall.sh
./uninstall.sh claude
./uninstall.sh codex
./uninstall.sh agent
./uninstall.sh all
```

If no argument is provided, the script prompts you to choose a target.
This removes only the symlinks in the selected target's `skills` directory that point back to this repository's `skills/` entries.
The script prints which links were removed and which unrelated links were skipped.

## Structure

```
gm-skills/
├── .claude-plugin/
│   └── plugin.json       # Plugin identity
├── skills/
│   ├── gm-harness-init/
│   ├── gm-harness-plan-task/
│   ├── gm-battle/
│   ├── gm-de-ai-article/
│   ├── gm-pk/
│   ├── gm-topic-engine/
│   ├── gm-writing/
│   └── gm-x-hook-writer/
└── README.md
```

## Adding New Skills

1. Create `skills/<skill-name>/SKILL.md`
2. Add frontmatter with at least `name` and `description`
3. Keep the command name aligned with the directory name
4. Re-run `./install.sh` for the target environment you want to update

Key frontmatter fields:
- `name` — must match directory name, becomes the slash command
- `description` — drives auto-invocation; include keywords users naturally say
- `argument-hint` — shown in autocomplete (e.g., `[topic]`)
- `context: fork` — run in isolated subagent (good for long tasks)
- `allowed-tools` — pre-approve tools without permission prompts
- `disable-model-invocation: true` — require explicit invocation only
