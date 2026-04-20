---
name: auto-skill-fit
description: 扫描项目技术栈，推荐并安装匹配的 agent skills 套装。Use when starting a new project, onboarding to a codebase, or when the user asks "what skills should I install", "recommend skills for this project", "auto setup skills".
argument-hint: "[项目路径，默认当前目录]"
---

# auto-skill-fit

扫描项目 → 提取技术栈 → 搜索 skills.sh → 编号列出 → 用户选择 → 安装。

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

### Step 3: 编号列出，等待用户选择

输出格式（必须严格遵守）：

```
🔍 检测到技术栈：React, Next.js, Tailwind, shadcn/ui, Supabase

📦 推荐 Skills：

  [1] ✅ vercel-react-best-practices    332K installs  (react, nextjs)
  [2] ✅ web-design-guidelines           265K installs  (前端通用)
  [3] ✅ frontend-design                 315K installs  (前端通用)
  [4] ✅ supabase-postgres-best-practices 109K installs  (supabase)
  [5] ✅ shadcn                           96K installs  (shadcn)
  [6]    next-best-practices              68K installs  (nextjs)
  [7]    tailwind-design-system           --  installs  (tailwind)

  ✅ = 强烈推荐（安装量 ≥ 50K 且与技术栈直接相关）

👉 请选择要安装的编号：
   - "all" 或 "全部" → 安装全部
   - "1,3,5" → 安装指定项
   - "recommended" 或 "推荐" → 只装 ✅ 标记的
   - "去掉 3" → 从全部中排除
   - "不装了" → 取消
```

**关键规则：**
- 必须等用户回复后才执行安装，不要自动安装
- 编号从 1 开始，连续编号
- ✅ 标记安装量 ≥ 50K 且与检测到的技术栈直接相关的
- 按安装量降序排列
- 每条显示：编号、推荐标记、skill 名、安装量、命中关键词

### Step 4: 解析用户选择并安装

根据用户回复解析要安装的列表：

| 用户输入 | 行为 |
|---------|------|
| `all` / `全部` / `装吧` / `都装` | 安装全部 |
| `1,3,5` / `1 3 5` / `装 1、3、5` | 安装指定编号 |
| `recommended` / `推荐` / `推荐的` | 只装 ✅ 标记的 |
| `去掉 3` / `除了 3` / `不要 3` | 全部减去指定编号 |
| `不装了` / `取消` / `算了` | 取消，不执行任何安装 |

安装命令格式：

```bash
npx skills add <owner/repo@skill-name> -g -y
```

逐条执行，每条安装后输出结果（成功/失败）。

### Step 5: 安装完成总结

```
✅ 安装完成！共安装 N 个 skills：
  - vercel-react-best-practices
  - shadcn
  - supabase-postgres-best-practices

💡 这些 skills 会在后续对话中自动生效。
```

## 规则

1. **必须等用户选择后才安装** — 列出清单后停下来等回复
2. **依赖 find-skills 做搜索**（如果已安装）— 不重复造轮子
3. **关键词要精准** — 用框架名（`react`、`nextjs`），不用泛词（`frontend`）
4. **宁缺毋滥** — 搜不到高质量结果就不列出
