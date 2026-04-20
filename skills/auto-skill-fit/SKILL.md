---
name: auto-skill-fit
description: 扫描项目技术栈，推荐并安装匹配的 agent skills 套装。Use when starting a new project, onboarding to a codebase, or when the user asks "what skills should I install", "recommend skills for this project", "auto setup skills".
argument-hint: "[项目路径，默认当前目录]"
---

# auto-skill-fit

扫描项目 → 提取技术栈 → 搜索 skills.sh → 用户选择 → 安装。

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

### Step 3: 用户选择

先输出技术栈摘要，然后让用户选择要安装的 skills。

**在 Claude Code 中**：使用 AskUserQuestion 工具，渲染原生选择框。设置 `multiSelect: true` 允许多选。将推荐项标记 `(Recommended)` 放在选项列表最前面。示例：

```
AskUserQuestion:
  question: "检测到技术栈：React, Next.js, Tailwind, Supabase。以下是推荐的 skills，请选择要安装的："
  multiSelect: true
  options:
    - "vercel-react-best-practices (332K installs) — React/Next.js 最佳实践 (Recommended)"
    - "web-design-guidelines (265K installs) — Web 设计规范 (Recommended)"
    - "frontend-design (315K installs) — 前端设计"
    - "supabase-postgres-best-practices (109K installs) — Supabase 最佳实践 (Recommended)"
    - "shadcn (96K installs) — shadcn/ui 组件"
    - "next-best-practices (68K installs) — Next.js 进阶"
```

**在其他 agent 中**（Kiro CLI、Cursor、Codex 等）：降级为编号文本列表，等用户自然语言回复：

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

**如何判断环境**：如果当前 agent 有 AskUserQuestion 工具可用，就用它；否则降级为文本。

### Step 4: 安装

根据用户选择，逐条执行：

```bash
npx skills add <owner/repo@skill-name> -g -y
```

每条安装后输出结果（成功/失败）。

### Step 5: 完成总结

```
✅ 安装完成！共安装 N 个 skills：
  - vercel-react-best-practices
  - shadcn
  - supabase-postgres-best-practices

💡 这些 skills 会在后续对话中自动生效。
```

## 规则

1. **必须等用户选择后才安装** — 不要自动安装
2. **优先使用原生交互** — Claude Code 用 AskUserQuestion，其他降级为文本
3. **依赖 find-skills 做搜索**（如果已安装）
4. **关键词要精准** — 用框架名，不用泛词
5. **宁缺毋滥** — 搜不到高质量结果就不列出
