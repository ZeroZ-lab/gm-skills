# Plan — GM Skill Manager Stage 1

> 版本化 Unified Inventory + Native Installer 协调

## 版本信息

| 项目 | 值 |
|------|-----|
| 版本 | v1.0 |
| 日期 | 2026-06-23 |
| 来源 | `CONTEXT.md` + ADR-0001–0018 |
| 验收来源 | ADR-0018 |

## 验收条件

| ID | 条件 |
|---|---|
| AC-S1-01 | Codex Plugin、Claude Code Plugin、`npx skills` 均产出 Observed Evidence |
| AC-S1-02 | 相同 Remote Source + canonical `SKILL.md` path 跨三种格式聚合为同一 Capability |
| AC-S1-03 | Capability、Package、Runtime 三种视图结果一致 |
| AC-S1-04 | install、uninstall、enable、disable、repair 只调用 Native Installer |
| AC-S1-05 | doctor 只读，repair 需要独立 Action Authorization |
| AC-S1-06 | 检出 Duplicate Exposure、Revision drift、Unresolved Identity、broken Installation |
| AC-S1-07 | Registry Verification 与 Discovery Verification 产出证据 |
| AC-S1-08 | 合成 Inventory Fixtures 通过，真实电脑 smoke test 只读 |
| AC-S1-09 | ZCode 仅报告 unmanaged，不执行 mutation |
| AC-S1-10 | Redacted Inventory 不泄露本机敏感信息 |

## 规划决策

- **PL1**：先稳定 Inventory Schema Version 与 Identity Resolution，再接 runtime adapter；否则 adapter 会继续各自定义身份。
- **PL2**：三个 evidence adapter 在核心 schema 稳定后并行开发，禁止共享 runtime-specific 解析文件。
- **PL3**：不新增人类操作的 manager CLI；`inventory.py --json` 是只读接口，mutation 由 Agent 按 `SKILL.md` 调用 Native Installer。
- **PL4**：最终 Unified Inventory JSON 是主要 test surface，私有 helper 不形成兼容契约。
- **PL5**：Stage 1 不实现 sync、Format Alignment、Source Claim、Invocation Verification 或 ZCode mutation。

## 模块全景

| Module | 职责 | 风险 |
|---|---|---|
| Identity Resolution | 将 Observed Evidence 裁决为 Resolved/Unresolved Identity | 高：决定跨格式聚合正确性 |
| Inventory Model | 表达 Package、Format、Installation、Capability、Exposure 与 diagnostics | 高：当前 flat schema 需替换 |
| Codex Adapter | 读取 Codex native plugin evidence 与 built-ins | 中 |
| Claude Adapter | 读取 registry、marketplace、scope 与 Capability Set | 中 |
| npx Skills Adapter | 合并 lock、list、Runtime link 证据 | 高：Installation/Exposure 证据分离 |
| Derived Views | 生成 Capability、Package、Runtime Views | 中 |
| Doctor/Redaction | 只读 findings、recommendations 与可分享输出 | 中 |
| Action Coordination | 让 Agent 选择并调用 Native Installer，完成验证 | 高：不得演变为第四个 installer |

## 依赖图

```text
Task-01 版本化 Identity Resolution + Inventory contract
  ├── Task-02 Codex Evidence → Capability View
  ├── Task-03 Claude Evidence → Scoped Exposure
  └── Task-04 npx Evidence → Managed/Duplicate Exposure
            ↓
Task-05 三视图 + doctor + redact
            ↓
Task-06 Remote Package Impact + install 协调
            ↓
Task-07 uninstall / enable / disable / repair 协调
            ↓
Task-08 Stage 1 集成验收与文档收口
```

## 并行矩阵

| 任务 | 可并行 | 原因 |
|------|--------|------|
| Task-01 | 否 | 所有 adapter 依赖 schema 与 identity contract |
| Task-02 | 是（与 03、04） | Codex adapter、fixture、测试文件独立 |
| Task-03 | 是（与 02、04） | Claude adapter、fixture、测试文件独立 |
| Task-04 | 是（与 02、03） | npx adapter、fixture、测试文件独立 |
| Task-05 | 否 | 依赖三个 adapter 的统一结果 |
| Task-06 | 否 | 依赖 Package/Capability Views 与 Remote Source |
| Task-07 | 否 | 依赖 Package Impact、Native Installer 选择和验证 |
| Task-08 | 否 | 汇总全部验收条件 |

**关键路径**：Task-01 → Task-04 → Task-05 → Task-06 → Task-07 → Task-08

**风险排序**：Identity Resolution → npx evidence 合并 → mutation 所有权 → 三视图一致性 → redaction。

## 任务清单

### Task-01: 跨格式 Capability Identity 可被稳定解析

**验收来源**：AC-S1-02、AC-S1-06、AC-S1-08
**目标**：给定合成 evidence，输出 versioned inventory contract，并正确区分 Capability、Revision 与 Unresolved Identity。
**依赖**：无
**文件**：
- `plugins/gm-skill-manager/skills/gm-skill-manager/scripts/inventory.py`
- `plugins/gm-skill-manager/skills/gm-skill-manager/scripts/inventory_model.py`
- `plugins/gm-skill-manager/skills/gm-skill-manager/scripts/identity.py`
- `plugins/gm-skill-manager/skills/gm-skill-manager/tests/test_identity_inventory.py`
- `plugins/gm-skill-manager/skills/gm-skill-manager/tests/fixtures/identity.json`

**步骤**：
1. RED：用 fixture 定义跨 Codex/Claude/npx 的相同 Capability、不同 Revision 与证据不足场景。
2. GREEN：建立 Inventory Schema Version、required fields 与 explicit `unknown`。
3. GREEN：集中实现 Remote Source normalization、canonical skill path 与 built-in identity。
4. GREEN：输出 Observed Evidence 与 Identity Resolution，禁止 adapter 直接生成身份。
5. REFACTOR：让最终 JSON 成为唯一公开 test surface。

**验证方式**：TDD
**验证标准**：
- 相同 remote/path 聚合为一个 Capability。
- Revision 仅产生 `same/different/unknown`，不改变身份。
- 证据不足保持 Unresolved，不按名称合并。
- Built-in 使用 Runtime Identity + built-in path。

### Task-02: Codex 安装可进入 Unified Inventory

**验收来源**：AC-S1-01、AC-S1-06、AC-S1-07
**目标**：Operator 能看到 Codex Plugin、built-ins、enabled 状态与 development-local 安装的可信证据。
**依赖**：Task-01
**文件**：
- `plugins/gm-skill-manager/skills/gm-skill-manager/scripts/adapters/codex.py`
- `plugins/gm-skill-manager/skills/gm-skill-manager/scripts/inventory.py`
- `plugins/gm-skill-manager/skills/gm-skill-manager/tests/test_codex_adapter.py`
- `plugins/gm-skill-manager/skills/gm-skill-manager/tests/fixtures/codex/`

**步骤**：
1. RED：覆盖 native list、config fallback、missing cache、built-in 与 local marketplace。
2. GREEN：从 Codex native records 产出 Observed Evidence，不构造 Capability Identity。
3. GREEN：将 registry 与文件冲突归为 broken Installation。
4. GREEN：产出 Registry/Discovery Verification evidence。
5. REFACTOR：保证 fallback 与 native adapter 输出相同 contract。

**验证方式**：TDD
**验证标准**：
- native 与 fallback 字段一致。
- disabled 与 installed 分离表达。
- development-local 只读标记，不与 Remote Capability 自动合并。

### Task-03: Claude Code scope 与 Capability Set 可被准确盘点

**验收来源**：AC-S1-01、AC-S1-03、AC-S1-06、AC-S1-07
**目标**：Operator 能看到 Claude user/project/local Installations、format Capability Set 与 scope drift。
**依赖**：Task-01
**文件**：
- `plugins/gm-skill-manager/skills/gm-skill-manager/scripts/adapters/claude.py`
- `plugins/gm-skill-manager/skills/gm-skill-manager/tests/test_claude_adapter.py`
- `plugins/gm-skill-manager/skills/gm-skill-manager/tests/fixtures/claude/`
- `plugins/gm-skill-manager/skills/gm-skill-manager/scripts/inventory.py`

**步骤**：
1. RED：覆盖 user/project/local、多 Revision、missing cache 与不同 Capability Set。
2. GREEN：读取 installed registry、marketplaces 与 package manifests。
3. GREEN：产出 Installation Package、Package Format、scope 和 Capability Set evidence。
4. GREEN：识别 Format Capability Drift 与 Native Record Inconsistency。
5. REFACTOR：项目路径只作为 scope evidence，不进入 Capability Identity。

**验证方式**：TDD
**验证标准**：
- 同 package root 的 Codex/Claude formats 属于同一 Installation Package。
- scoped Installations 不被错误合并。
- manifest capability 集合差异可检测。

### Task-04: npx skills 的 Installation 与 Exposure 可分别验证

**验收来源**：AC-S1-01、AC-S1-02、AC-S1-06、AC-S1-07
**目标**：Operator 能区分 managed Installation、active/inactive Exposure 与 unmanaged link。
**依赖**：Task-01
**文件**：
- `plugins/gm-skill-manager/skills/gm-skill-manager/scripts/adapters/npx_skills.py`
- `plugins/gm-skill-manager/skills/gm-skill-manager/tests/test_npx_skills_adapter.py`
- `plugins/gm-skill-manager/skills/gm-skill-manager/tests/fixtures/npx-skills/`
- `plugins/gm-skill-manager/skills/gm-skill-manager/scripts/inventory.py`

**步骤**：
1. RED：覆盖 lock+link、lock-only、link-only、global+project overlap。
2. GREEN：从 `.skill-lock.json` 解析 Remote Source、skill path 与 Revision evidence。
3. GREEN：从 `npx skills list` 与 Runtime links 解析 Exposure evidence。
4. GREEN：识别 Unmanaged Exposure、Duplicate Exposure 与 Revision drift。
5. REFACTOR：确保 npx、Codex、Claude 的相同 remote/path 汇聚。

**验证方式**：TDD
**验证标准**：
- lock+link 为 installed+active。
- lock-only 为 installed+inactive。
- link-only 为 broken+Unresolved。
- global/project 重叠为 ambiguous。

### Task-05: Operator 可通过三视图诊断当前电脑

**验收来源**：AC-S1-03、AC-S1-05、AC-S1-06、AC-S1-09、AC-S1-10
**目标**：`list` 与 `doctor` 提供一致的 Capability、Package、Runtime Views，并安全分享结果。
**依赖**：Task-02、Task-03、Task-04
**文件**：
- `plugins/gm-skill-manager/skills/gm-skill-manager/scripts/inventory.py`
- `plugins/gm-skill-manager/skills/gm-skill-manager/scripts/views.py`
- `plugins/gm-skill-manager/skills/gm-skill-manager/scripts/doctor.py`
- `plugins/gm-skill-manager/skills/gm-skill-manager/tests/test_views_doctor.py`
- `plugins/gm-skill-manager/skills/gm-skill-manager/tests/test_redaction.py`

**步骤**：
1. RED：定义三视图交叉一致性、Facts/Findings/Recommendations 分离。
2. GREEN：生成 Capability View、Package View、Runtime View。
3. GREEN：实现只读 doctor findings，覆盖 identity、state、scope 和 installer diagnostics。
4. GREEN：将 ZCode 报告为 unmanaged，不读取其私有状态作权威判断。
5. GREEN：加入 `--redact`，清除 home、project detail、credential 与 URL secret。
6. REFACTOR：Recommendations 不产生 Execution Plan。

**验证方式**：TDD
**验证标准**：
- 三视图引用同一组实体且计数一致。
- doctor 执行前后 fixture 文件无变化。
- redact 输出无 home 绝对路径、token、query secret。

### Task-06: Operator 可安全预检并安装远程 Package

**验收来源**：AC-S1-04、AC-S1-07、ADR-0017
**目标**：明确选择 Remote Source、Package/Capability、Runtime 与 scope 后，Agent 选择正确 Native Installer 并验证安装。
**依赖**：Task-05
**文件**：
- `plugins/gm-skill-manager/skills/gm-skill-manager/SKILL.md`
- `plugins/gm-skill-manager/skills/gm-skill-manager/references/runtime-map.md`
- `plugins/gm-skill-manager/skills/gm-skill-manager/references/action-contract.md`
- `plugins/gm-skill-manager/skills/gm-skill-manager/tests/action-scenarios.md`

**步骤**：
1. 定义安装 preflight：Selection Set、Package Impact、Runtime、scope、Installer Availability/Compatibility。
2. 定义选择规则：Runtime native Plugin 优先，无原生格式时使用 `npx skills`。
3. 定义可执行扩展的额外确认规则。
4. 定义 Native Installer 命令模板，禁止直接改 registry、lock、cache 或 link。
5. 定义安装后的 Registry 与 Discovery Verification。
6. 用场景表验证 Codex、Claude、npx 与 Unsupported Format 分支。

**验证方式**：直接验证 + 场景审查
**验证标准**：
- 不存在 manager 自有 mutation 命令。
- 多 package remote 不默认全选，scope 不从 cwd 推断。
- 每个安装场景明确使用一个 Native Installer 并重新 inventory。

### Task-07: Operator 可安全卸载、启用、禁用和修复

**验收来源**：AC-S1-04、AC-S1-05、AC-S1-07
**目标**：所有基础 mutation 都形成可审查 Execution Plan，并保留 Native Installer 所有权。
**依赖**：Task-06
**文件**：
- `plugins/gm-skill-manager/skills/gm-skill-manager/SKILL.md`
- `plugins/gm-skill-manager/skills/gm-skill-manager/references/action-contract.md`
- `plugins/gm-skill-manager/skills/gm-skill-manager/references/runtime-map.md`
- `plugins/gm-skill-manager/skills/gm-skill-manager/tests/action-scenarios.md`

**步骤**：
1. 定义 Package Removal 与 Data Removal 的独立授权。
2. 定义 Plugin enable/disable 与 npx target-Runtime link 语义映射。
3. 定义 doctor 只读、repair 独立授权与 Native Record Inconsistency 修复。
4. 定义动态风险排序、逐步验证、失败即停和 Partial Success。
5. 定义 Duplicate Exposure 的 ambiguous 状态与不自动删除规则。
6. 场景审查所有 Action 是否只调用 Native Installer。

**验证方式**：直接验证 + 场景审查
**验证标准**：
- uninstall 默认保留数据。
- disable 不等同于删除 Capability。
- repair 不直接编辑 native state。
- 部分失败不自动回滚。

### Task-08: Stage 1 验收门通过

**验收来源**：AC-S1-01–AC-S1-10
**目标**：合成 fixtures、真实机器只读 smoke test、skill/plugin packaging 与文档全部满足 ADR-0018。
**依赖**：Task-05、Task-06、Task-07
**文件**：
- `plugins/gm-skill-manager/skills/gm-skill-manager/tests/test_stage1_acceptance.py`
- `plugins/gm-skill-manager/skills/gm-skill-manager/SKILL.md`
- `plugins/gm-skill-manager/skills/gm-skill-manager/references/runtime-map.md`
- `README.md`
- `plugins/gm-skill-manager/.codex-plugin/plugin.json`

**步骤**：
1. 汇总 AC-S1-01–10 的自动化与手动证据。
2. 运行全部 synthetic fixtures，验证 schema 和三视图。
3. 在真实电脑运行只读 inventory/doctor，对比前后 native records 未变化。
4. 验证 ZCode unmanaged 与 redaction。
5. 运行 skill、plugin 与 monorepo validators。
6. 更新用户文档和插件描述，准确声明 Stage 1 支持范围。

**验证方式**：自动化验收 + 手动 smoke test
**验证标准**：
- ADR-0018 每项均有证据。
- `npm run plugin:validate`、skill validator、plugin validator 通过。
- `git diff --check` 通过。
- 真实机器 smoke test 无 mutation。

## 检查点

| 检查点 | 时机 | 验收标准 | 回退方案 |
|--------|------|---------|---------|
| CP-1 Identity Contract | Task-01 后 | 三格式同 Capability 可聚合；Revision/Identity 分离 | 不开始 adapter，修正 schema 与 fixtures |
| CP-2 Evidence Integration | Task-04 后 | 三 adapter 只产 evidence，跨格式 fixture 收敛 | 退回对应 adapter，不在 views 层补 identity |
| CP-3 Read-only Product | Task-05 后 | 三视图一致、doctor 无 mutation、redact 安全 | 暂停 Action 工作，修正 inventory contract |
| CP-4 Native Ownership | Task-07 后 | 所有 mutation 场景只走 Native Installer | 删除任何自有 mutation helper，重做 Action 文档 |
| CP-5 Stage 1 Gate | Task-08 后 | ADR-0018 全部通过 | 不发布，回到失败 AC 对应任务 |

## 执行顺序

```text
第 1 步：Task-01
第 2 步：Task-02 + Task-03 + Task-04（可并行）
第 3 步：Task-05
第 4 步：Task-06
第 5 步：Task-07
第 6 步：Task-08
```

## 非目标

- Coverage Sync、Revision Sync、Format Alignment、Source Claim。
- Invocation Verification。
- ZCode mutation adapter。
- Manager-owned registry、history 或 Action Log。
- 自动升级 Codex、Claude Code、Node/npm 或 `skills` CLI。
- 本地开发 Package 的新安装。
