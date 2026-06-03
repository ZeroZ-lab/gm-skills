---
name: gm-agent-docs
description: 为项目生成 CLAUDE.md 和 AGENTS.md，分析项目结构后输出命令优先、按任务分区的 agent 配置文件。Use when users want to create or improve CLAUDE.md, AGENTS.md, or agent instruction files for their project.
argument-hint: "[项目路径或描述]"
---

# gm-agent-docs

为任意项目生成高质量的 CLAUDE.md 和 AGENTS.md。

## 核心原则

好的 agent md 文档 = 操作手册，不是人类文档。

1. **命令优先** — 每条指令必须能回答"什么命令证明做对了"
2. **代码示例 > 文字描述** — 一个 snippet 胜过三段解释
3. **精简** — 100 行以内（上限 200，超过 300 agent 会丢失信号）
4. **只写 agent 推断不出的** — 标准语法、库用法不用写
5. **三层边界** — ✅ 必须做 / ⚠️ 先问 / 🚫 绝不做
6. **持续演进** — agent 每犯一次可预防的错误，加一条规则

## 流程

### Step 1: 分析项目

扫描项目根目录，收集 6 大核心领域的信息：

| 领域 | 扫描目标 | 产出 |
|------|---------|------|
| 命令 | package.json scripts / Makefile / pyproject.toml / Cargo.toml / go.mod | 构建、测试、lint、启动的具体命令 |
| 测试 | jest.config / vitest.config / pytest.ini / test 目录 | 框架、运行方式、覆盖率要求 |
| 项目结构 | 顶层目录 + 框架约定 | 关键目录职责、架构模式 |
| 代码风格 | eslint / prettier / ruff / .editorconfig + 最近 10 条 commit | 命名规范、格式规则（用代码示例展示） |
| Git 工作流 | 最近 20 条 commit message + branch 命名 | commit 格式、分支策略 |
| 边界 | .gitignore / CI 配置 / 敏感文件 | 不能碰的文件、需要审批的操作 |

**额外扫描（大型项目）：**
- `docs/` / `ADR/` / `specs/` → 生成文档索引表
- monorepo 子包 → 生成目录级 scoping 建议
- CI/CD 配置 → 提取部署约束

输出分析摘要给用户确认，再进入生成。

### Step 2: 生成 CLAUDE.md

**必须包含的 6 个 section（按此顺序）：**

```markdown
# 项目名

一句话说明（技术栈 + 版本，要具体）。

## 常用命令

直接可执行的 shell 命令，含 flags。按频率排序：
- 开发服务器
- 运行测试
- lint / format
- 构建 / 部署

## 写代码时

- 架构约束（目录职责、依赖方向）
- 代码风格（用 ✅/❌ 代码示例展示，不用文字描述）
- 验证命令

## 完成标准

编号列表，每条 = 具体命令 + 期望退出码：
1. `命令` 退出码 0
2. `命令` 退出码 0
3. commit message 符合格式

## 卡住时

- 具体场景 → 具体操作
- 连续失败 3 次 → 停下来报告，不要继续尝试
- 绝不：列出禁止的破坏性操作

## 参考文档（可选，大型项目才加）

| 文件 | 何时读取 |
|------|---------|
| `docs/xxx.md` | 做 xxx 时 |
```

**禁止出现的内容：**
- 大段散文、项目历史
- "请注意"、"建议"、"小心" 等模糊措辞
- agent 能从代码推断的信息
- API key、密码等敏感信息
- 没有排序的矛盾优先级

### Step 3: 生成 AGENTS.md

只写一行：

```markdown
See [CLAUDE.md](./CLAUDE.md) for all project instructions.
```

### Step 4: 输出与确认

1. 展示生成的 CLAUDE.md 给用户 review
2. 用户确认后写入文件
3. 如果已有 CLAUDE.md，展示 diff 再确认覆盖

## 示例输出

### Next.js 项目

```markdown
# my-app

Next.js 14 全栈应用，App Router + Prisma + PostgreSQL + TypeScript。

## 常用命令

pnpm dev          # localhost:3000
pnpm build        # 生产构建
pnpm test         # vitest
pnpm lint         # eslint + prettier check

## 写代码时

- 页面放 `app/`，API 路由放 `app/api/`
- 数据库操作只通过 `lib/db.ts`
- 服务端组件默认，客户端组件加 `'use client'`

```typescript
// ✅
export async function getUser(id: string): Promise<User> {
  return db.user.findUniqueOrThrow({ where: { id } });
}

// ❌
export async function getUser(id) {
  const user = await db.user.findUnique({ where: { id } });
  return user;
}
```

## 完成标准

1. `pnpm build` 退出码 0
2. `pnpm test` 退出码 0
3. `pnpm lint` 退出码 0
4. commit: `type(scope): description`

## 卡住时

- 类型错误修不好 → `pnpm tsc --noEmit` 看完整报错
- 数据库冲突 → `pnpm prisma migrate reset`（会清数据，先确认）
- 绝不：跳过 build、直接改 migrations、force push main
```

### Python 项目

```markdown
# my-service

FastAPI REST API，Python 3.12 + SQLAlchemy + Alembic + PostgreSQL。

## 常用命令

uv run uvicorn app.main:app --reload   # dev server :8000
uv run pytest -v                        # 测试
uv run ruff check .                     # lint
uv run mypy app/ --strict               # 类型检查

## 写代码时

- 路由放 `app/api/`，模型放 `app/models/`
- 所有函数必须有 type hints
- 依赖注入用 `Depends()`

```python
# ✅
async def get_user(user_id: int, db: Session = Depends(get_db)) -> User:
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404)
    return user

# ❌
async def get_user(user_id, db):
    return await db.query(User).filter_by(id=user_id).first()
```

## 完成标准

1. `uv run ruff check .` 退出码 0
2. `uv run pytest -v` 退出码 0
3. `uv run mypy app/ --strict` 退出码 0
4. commit: `type: description`

## 卡住时

- 测试失败 3 次 → 停下来，贴完整 traceback
- migration 冲突 → `alembic downgrade -1` 再重新生成
- 绝不：删 migration 文件、跳过 mypy、改 alembic_version 表
```
