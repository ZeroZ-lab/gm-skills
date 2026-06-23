# Test Cases — GM Skill Manager Stage 1

## 测试范围矩阵

| AC | P0 用例 | 优先级理由 |
|---|---|---|
| AC-S1-01 | TC-001 三 adapter 产出 required evidence | 缺证据则全部视图失真 |
| AC-S1-02 | TC-002 三格式汇聚；TC-003 不同 Revision 同 Identity；TC-004 Unresolved 不合并 | 身份是所有 Action 的前提 |
| AC-S1-03 | TC-005 三视图实体与计数一致 | 防止不同视图给出冲突结论 |
| AC-S1-04 | TC-006 mutation 仅调用 Native Installer | 防止 Manager 成为第四个 installer |
| AC-S1-05 | TC-007 doctor 零写入；TC-008 repair 需要授权 | 保护本机状态 |
| AC-S1-06 | TC-009 duplicate；TC-010 drift；TC-011 broken | 核心诊断价值 |
| AC-S1-07 | TC-012 registry/discovery evidence 完整 | 安装不等于可用 |
| AC-S1-08 | TC-013 fixtures 可重复；TC-014 real smoke 只读 | 保证可复现与真实可用 |
| AC-S1-09 | TC-015 ZCode unmanaged 且无 mutation | 防止弱证据越权 |
| AC-S1-10 | TC-016 redact 清除路径与 secret | 防止分享泄密 |

## P0 用例骨架

- **TC-001**：输入三类 native fixture；预期均输出 package/installation/capability/exposure evidence。
- **TC-002**：相同 remote + skill path 经 Codex、Claude、npx 安装；预期一个 Capability、三个 Installation。
- **TC-003**：同 Identity 两个 commit；预期 Revision Relation=`different`，Capability 数不增加。
- **TC-004**：仅有 marketplace label/name；预期 Identity=`unresolved`，不参与去重。
- **TC-005**：同一 fixture 生成三视图；预期引用实体集合与诊断一致。
- **TC-006**：执行四类 mutation 场景；预期命令来自 codex/claude/npx，native files 无直接写入。
- **TC-007/008**：doctor 前后 hash 不变；repair 无授权不执行。
- **TC-009/010/011**：双 Exposure、Revision 差异、registry/path 冲突分别产生明确 finding。
- **TC-012**：registry 成功但 discovery 失败；预期 installed + exposure unknown/inactive，不报告 active。
- **TC-013/014**：fixture 重复执行输出一致；真实 smoke 前后 registry/lock hash 一致。
- **TC-015/016**：ZCode 仅 unmanaged；redact 输出不含 home、token、credential query。

## 测试数据

- 每个 adapter 使用独立临时 home；fixture 不访问真实 registry。
- CLI 输出由固定 JSON/text fixture 提供；每个测试使用全新目录并在结束后删除。
- Remote URL 包含 HTTPS、SSH、credential/query 变体，用于 normalization 与 redaction。
- 真实机器只执行 list/doctor，并对 native registry、lock 与 config 做前后 hash 比较。
