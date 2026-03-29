# gm-writing-kit

长文写作流程套件。

## 包含 Skills

| Skill | 功能 | 使用时机 |
|-------|-----|---------|
| `topic-picker` | 选题决策 | 有想法但不确定写不写 |
| `research-assistant` | 调研整理 | 确定选题，缺素材 |
| `hook-crafter` | 开头钩子 | 不知道怎么开头 |
| `structure-designer` | 结构设计 | 素材多，需组织 |
| `draft-generator` | 初稿生成 | 按结构写成文 |
| `revision-tuner` | 改稿调优 | 初稿完成，需修改 |
| `publish-prep` | 发布准备 | 起标题、配图、适配平台 |

## 完整流程

```
topic-picker → research-assistant → structure-designer
                                          ↓
hook-crafter → draft-generator → revision-tuner → publish-prep
```

## 快速开始

1. 有个模糊想法？→ 用 `topic-picker`
2. 确定了写什么？→ 用 `research-assistant` 收集素材
3. 素材够了？→ 用 `structure-designer` 搭结构
4. 结构有了？→ 用 `hook-crafter` 写开头
5. 要填充内容？→ 用 `draft-generator`
6. 要修改？→ 用 `revision-tuner`
7. 要发布？→ 用 `publish-prep`

## 和现有 skills 配合

- 用 `gm-writing`（关木式）改写长文？→ 在 **draft-generator** 或 **revision-tuner** 后使用
- 要更好的 hooks？→ 用 `gm-x-hook-writer` 替代 **hook-crafter**

## 目录结构

```
gm-writing/
├── skills/
│   ├── topic-picker/        # 选题决策
│   ├── research-assistant/  # 调研整理
│   ├── hook-crafter/        # 开头钩子
│   ├── structure-designer/  # 结构设计
│   ├── draft-generator/     # 初稿生成
│   ├── revision-tuner/      # 改稿调优
│   ├── publish-prep/        # 发布准备
│   └── writing-kit/         # 套件入口
└── README.md
```
