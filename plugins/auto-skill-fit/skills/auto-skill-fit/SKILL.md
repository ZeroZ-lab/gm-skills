---
name: auto-skill-fit
description: 扫描项目技术栈，推荐并安装匹配的 agent skills 套装。Use when starting a new project, onboarding to a codebase, or when the user asks "what skills should I install", "recommend skills for this project", "auto setup skills".
argument-hint: "[项目路径，默认当前目录]"
---

# auto-skill-fit

扫描项目 → 提取技术栈 → 搜索 skills.sh → 用户选择安装方式和 skills → 安装。

## 流程

### Step 1: 扫描项目，提取技术栈关键词

读取项目根目录下的配置文件：

| 文件 | 提取方式 |
|------|---------|
| `package.json` | dependencies + devDependencies 的 key |
| `next.config.*` | → `nextjs` |
| `nuxt.config.*` | → `nuxt` |
| `vite.config.*` | → `vite` |
| `tailwind.config.*` 或 CSS 含 `@import "tailwindcss"` | → `tailwind` |
| `components.json` | → `shadcn` |
| `pyproject.toml` / `requirements.txt` | 提取依赖名 |
| `Cargo.toml` | → `rust` + dependencies |
| `go.mod` | → `go` + module 关键词 |
| `Dockerfile` / `docker-compose.yml` | → `docker` |
| `supabase/` 目录 | → `supabase` |
| `.github/workflows/` | → `github-actions` |

**归一化**：`react-dom` → `react`，`@next/font` → `nextjs`，`tailwindcss` → `tailwind`。

只保留框架级关键词（react, nextjs, vue, svelte, tailwind, supabase, prisma, drizzle, fastapi, django 等），过滤工具库（lodash, axios 等）。

### Step 2: 搜索 skills.sh

检查是否已安装 `find-skills`（检查 `~/.kiro/skills/find-skills/`、`~/.claude/skills/find-skills/`、`.kiro/skills/find-skills/`）。

- **已安装** → 按 find-skills 流程搜索和质量筛选
- **未安装** → 直接用 `npx skills find <keyword>` 搜索

对每个关键词搜索，合并去重，过滤安装量 < 5K 的，跳过已安装的 skills。

### Step 3: 询问安装偏好

在让用户选择 skills 之前，依次确认两个问题：**安装方式** 和 **目标客户端**。

#### 3a: 安装方式

**在 Claude Code 中**，使用 AskUserQuestion：

```
AskUserQuestion:
  question: "选择安装方式："
  options:
    - "全局 + symlink（推荐，所有项目共享，自动更新）(Recommended)"
    - "全局 + copy（所有项目共享，独立副本）"
    - "项目级 + symlink（仅当前项目，团队可共享）"
    - "项目级 + copy（仅当前项目，适合提交到仓库）"
```

**在其他 agent 中**，降级为文本：

```
📋 安装方式：
  [1] 全局 + symlink（推荐）  [2] 全局 + copy
  [3] 项目级 + symlink        [4] 项目级 + copy
👉 输入编号（默认 1）：
```

对应 flags：

| 选择 | flags |
|------|-------|
| 全局 + symlink | `-g -y` |
| 全局 + copy | `-g -y --copy` |
| 项目级 + symlink | `-y` |
| 项目级 + copy | `-y --copy` |

#### 3b: 目标客户端

**在 Claude Code 中**，使用 AskUserQuestion（multiSelect: true）：

```
AskUserQuestion:
  question: "安装到哪些客户端？"
  multiSelect: true
  options:
    - "所有已检测到的客户端（推荐）(Recommended)"
    - "Claude Code"
    - "Kiro CLI"
    - "Cursor"
    - "Codex"
    - "Windsurf"
    - "GitHub Copilot"
```

**在其他 agent 中**，降级为文本：

```
🖥️ 安装到哪些客户端？
  [1] 所有已检测到的（推荐）
  [2] 指定客户端（输入名称，逗号分隔，如：claude-code,kiro-cli,cursor）
👉 输入编号（默认 1）：
```

对应 flags：
- 选"所有" → 不加 `-a`（默认安装到所有检测到的）
- 选指定客户端 → 加 `-a claude-code -a kiro-cli` 等

记住用户选择的 flags，后续所有安装命令统一使用。

### Step 4: 用户选择 Skills

输出技术栈摘要，让用户选择要安装的 skills。

**在 Claude Code 中**：使用 AskUserQuestion，设置 `multiSelect: true`。将推荐项标记 `(Recommended)` 放在选项列表最前面。示例：

```
AskUserQuestion:
  question: "检测到技术栈：React, Next.js, Tailwind, Supabase。以下是推荐的 skills（已过滤已安装和低质量），请选择要安装的："
  multiSelect: true
  options:
    - "vercel-react-best-practices (332K installs) — React/Next.js 最佳实践 (Recommended)"
    - "web-design-guidelines (265K installs) — Web 设计规范 (Recommended)"
    - "frontend-design (315K installs) — 前端设计"
    - "supabase-postgres-best-practices (109K installs) — Supabase 最佳实践 (Recommended)"
    - "shadcn (96K installs) — shadcn/ui 组件"
    - "next-best-practices (68K installs) — Next.js 进阶"
```

**在其他 agent 中**，降级为编号文本：

```
🔍 检测到技术栈：React, Next.js, Tailwind, Supabase

📦 推荐 Skills：

  [1] ✅ vercel-react-best-practices    332K installs  (react, nextjs)
  [2] ✅ web-design-guidelines           265K installs  (前端通用)
  [3]    frontend-design                 315K installs  (前端通用)
  [4] ✅ supabase-postgres-best-practices 109K installs  (supabase)
  [5]    shadcn                           96K installs  (shadcn)
  [6]    next-best-practices              68K installs  (nextjs)

  ✅ = 推荐

👉 请选择：all / 1,3,5 / recommended / 不装了
```

### Step 5: 安装

根据用户选择的 skills 和 Step 3 的安装偏好，逐条执行：

```bash
npx skills add <owner/repo@skill-name> <flags>
```

每条安装后输出结果（成功/失败）。

### Step 6: 完成总结

```
✅ 安装完成！共安装 N 个 skills（全局 + symlink）：
  - vercel-react-best-practices
  - shadcn
  - supabase-postgres-best-practices

💡 这些 skills 会在后续对话中自动生效。
```

## 规则

1. **必须等用户选择后才安装** — 不要自动安装
2. **安装偏好先于 skills 选择** — 先问怎么装，再问装什么
3. **优先使用原生交互** — Claude Code 用 AskUserQuestion，其他降级为文本
4. **依赖 find-skills 做搜索**（如果已安装）
5. **关键词要精准** — 用框架名，不用泛词
6. **宁缺毋滥** — 搜不到高质量结果就不列出
