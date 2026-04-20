---
name: gm-agent-docs
description: 为项目生成 CLAUDE.md 和 AGENTS.md，分析项目结构后输出命令优先、按任务分区的 agent 配置文件。Use when users want to create or improve CLAUDE.md, AGENTS.md, or agent instruction files for their project.
argument-hint: "[项目路径或描述]"
---

# gm-agent-docs

为任意项目生成高质量的 CLAUDE.md 和 AGENTS.md。

## 流程

### Step 1: 分析项目

扫描项目根目录，收集以下信息：

1. **语言和框架** — 读 package.json / pyproject.toml / Cargo.toml / go.mod / pom.xml / Gemfile 等
2. **构建命令** — 找到 build / compile / bundle 的具体命令
3. **测试框架** — 找到 test runner 和运行命令
4. **Lint/Format** — 找到 linter 和 formatter 配置
5. **项目结构** — 关键目录和架构模式
6. **Git 规范** — 分支策略、commit 格式（从历史 commit 推断）
7. **特殊约束** — monorepo / submodule / CI 配置 / 部署方式

输出分析摘要给用户确认，再进入生成。

### Step 2: 生成 CLAUDE.md

严格遵循以下原则：

**格式规则：**
- 总行数不超过 100 行
- 每条指令必须能回答："什么命令能证明这件事做对了？"
- 写操作指令，不写人类文档
- 不包含 agent 能从代码推断出的信息

**必须包含的 section（按顺序）：**

```markdown
# 项目名

一句话说明。

## 常用命令

具体的 shell 命令，直接可复制执行。包括：
- 启动开发服务器
- 运行测试
- lint / format
- 构建

## 写代码时

- 具体的编码规则 + 对应的验证命令
- 架构约束（哪些目录不能改、依赖方向等）
- 命名规范（仅当项目有非标准约定时）

## 完成标准

编号列表，每条是一个具体命令 + 期望的退出码：
1. `命令` 退出码 0
2. `命令` 退出码 0
3. commit message 符合格式

## 卡住时

- 具体场景 → 具体操作
- 绝不：列出禁止的破坏性操作
```

**禁止出现的内容：**
- 大段散文解释
- "请注意"、"建议"、"小心" 等模糊措辞
- API key、密码等敏感信息
- 项目历史或背景故事

### Step 3: 生成 AGENTS.md

只写一行：

```markdown
See [CLAUDE.md](./CLAUDE.md) for all project instructions.
```

### Step 4: 输出

1. 展示生成的 CLAUDE.md 内容给用户 review
2. 用户确认后写入文件
3. 如果项目已有 CLAUDE.md，先展示 diff 再确认覆盖

## 示例输出

对一个 Next.js 项目：

```markdown
# my-app

Next.js 14 全栈应用，App Router + Prisma + PostgreSQL。

## 常用命令

pnpm dev          # 开发服务器 localhost:3000
pnpm build        # 生产构建
pnpm test         # vitest 单元测试
pnpm lint         # eslint
pnpm db:migrate   # prisma migrate dev

## 写代码时

- 新页面放 `app/` 目录，API 路由放 `app/api/`
- 数据库操作只通过 `lib/db.ts` 的 prisma client
- 服务端组件默认，客户端组件加 `'use client'`
- 运行 `pnpm lint` 验证代码规范

## 完成标准

1. `pnpm build` 退出码 0
2. `pnpm test` 退出码 0，无失败用例
3. `pnpm lint` 退出码 0
4. commit message 格式：`type(scope): description`

## 卡住时

- 类型错误连续修不好：运行 `pnpm tsc --noEmit` 看完整报错
- 数据库 schema 冲突：`pnpm prisma migrate reset`（会清数据，先确认）
- 绝不：跳过 build 检查、直接改 migrations 文件、force push main
```
