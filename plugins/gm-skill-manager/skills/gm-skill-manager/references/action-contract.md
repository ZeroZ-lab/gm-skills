# Action Contract

## Preflight

每个 mutation Execution Plan 必须包含：

| Field | Requirement |
|---|---|
| Action | install / uninstall / enable / disable / repair |
| Selection | Capability 或 Installation Package |
| Remote Source | Remote install 必需 |
| Target Runtime | 必须由 Operator 指定 |
| Package Format | 根据目标 Runtime 独立选择 |
| Scope | 有多个选项时必须由 Operator 指定 |
| Revision | 首次安装可 floating；最终记录 resolved Revision |
| Package Impact | Capabilities、hooks、MCP、commands、scripts、apps、auth |
| Verification | Registry + Discovery |

多 package/multi-skill remote 不默认全选。可执行扩展、多个 Capabilities、project/local scope、Data Removal 和批量 Action 需要额外确认。

## Installation

1. 读取 Remote catalog 和 manifests。
2. 选择目标 Runtime 的原生 Plugin format；不可用时检查 `npx skills`。
3. 展示 Package Impact。
4. 调用 Native Installer。
5. 重新生成 Unified Inventory。
6. 完成 Registry 与 Discovery Verification。

禁止：复制文件、手工创建 Runtime link、写 registry/lock/cache。

## Uninstall

- 默认 Package Removal 保留数据。
- Claude Code 默认 `--keep-data`。
- Package 级卸载必须列出全部受影响 Capabilities。
- Data Removal 需要独立明确授权。

## Enable / Disable

- Claude Code：`claude plugin enable|disable ... --scope ...`
- Codex：使用 Plugin UI；没有可靠 UI 时 blocked。
- `npx skills`：通过 add/remove 目标 Runtime Exposure 实现。

Installation State 与 Exposure State 分别验证。

## Repair

doctor 只生成 finding。Operator 选择后才生成 repair Execution Plan。修复 registry/path/link 不一致时，只调用其 Native Installer 的 reinstall/remove/add，不直接修改原生记录。

## Ordering and failure

1. 预检所有目标。
2. 动态按风险与可验证性排序。
3. 每步执行后立即验证。
4. 第一个失败后停止。
5. 重新 inventory，报告 Partial Success。
6. 由 Operator 选择保留成功结果或显式恢复；不自动回滚。

## Recommendations are not authorization

Recommendation 只描述建议。只有 Operator 选择后才形成 Execution Plan。若原请求已明确 Action、目标、Runtime 和 scope，则视为已授权；新增影响必须再次确认。
