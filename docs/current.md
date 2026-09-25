# 当前状态

- **所在分支**：`main`
- **版本/里程碑**：P1 执行三件套成稿审核问题修复完成（关联计划：[`docs/plans/2026-09-25-p1-execution-trio-plan.md`](plans/2026-09-25-p1-execution-trio-plan.md)）
- **已具备能力**：
  - `nk-commit`：修正提交类型判定（区分“交付变化”与“纯状态记录”，不按 `.md` 扩展名一刀切，支持纯文档/规则交付物）；补全单独调用时的外来脏文件判定；路径相对技能目录解析。
  - `nk-work`：完整恢复 CE 核心工程纪律（系统级因果 5 问、按已有测试状况划分的证据策略表、执行证据守则、测试场景完整性检查、已定决策保护）；删除红绿循环中的 Refactor；补全 Plan 充分性判断；恢复 Matt 好坏测试与可 Mock 性正反代码示例；路径相对技能目录解析。
  - `nk-handoff`：强化 amend 时的显式路径限定（`-- docs/current.md`），杜绝带入工作区未完成代码；路径相对技能目录解析。
- **验证结果**：
  - 逐条对照方案 3.2 来源取舍表核对无遗漏；
  - 检索禁词（`ce-code-review|cross-model|unit-workspace|return-to-caller`）零残留；
  - 检索所有引用的共享约定路径均已采用相对技能目录的 `../conventions/` 或 `../../conventions/` 解析，无裸路径残留。

## 阻断与已知缺口

- 无

## 下一步

- [ ] P1 结项，并在本仓库自用试用（推进 P2: `nk-brainstorm`, `nk-plan`, `nk-ideate`）

## 阶段总览

| 阶段 | 内容 | 完成标志 | 状态 |
| :-- | :-- | :-- | :-- |
| **P0** | 共享约定 | 6 份约定评审通过 | **已完成** |
| **P1** | `nk-work`、`nk-commit`、`nk-handoff` | 单元验证与成稿评审通过；开始在本仓库自用 | **已完成 (评审问题已闭环)** |
| **P2** | `nk-brainstorm`、`nk-plan`、`nk-ideate` | 单元验证与成稿评审通过；用 `nk-plan` 规划本仓库的后续阶段 | 待启动 |
| **P3** | `nk-close`、`nk-compound` | 单元验证与成稿评审通过 | 待启动 |
| **P4** | `nk-debug`、`nk-review`、`nk-simplify` | 单元验证与成稿评审通过 | 待启动 |
| **P5** | `nk-wayfinder`、`nk-to-tasks`、`nk-wizard`、`nk-wait-what` | 单元验证与成稿评审通过 | 待启动 |
| **迁移与验收** | paper-30min 从 CE 迁移到 NexusKit，集中验收 | 产物整理、指令对齐、验收场景通过 | 待启动 |
| **打包** | 仿照 CE 结构做多 Agent 插件 | 各客户端可安装 | 待启动 |
