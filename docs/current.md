# 当前状态

- **所在分支**：`main`
- **版本/里程碑**：P1 已结项；P2 进行中（按 Claude 与用户商定，P2 不单独写 plan，由 Claude 直接实施）
- **已具备能力**：
  - 共享约定 6 份：[`conventions/`](../conventions/)
  - `nk-commit`、`nk-work`、`nk-handoff`：执行闭环（接手 → 测试先行实现 → 按节奏提交 → 交接）。P1 的关键设计决策已写入各技能末尾的来源备注；P1 plan 已按生命周期规则删除，原文可在提交 `fbf6c6e` 中查到。
- **验证结果**：
  - P1 单元验证与两轮成稿评审通过（U4 评审问题已闭环，R3 amend 路径限定已补齐）。
  - 未验证：真实项目中的端到端使用，统一放到"迁移与验收"阶段。

## 阻断与已知缺口

- 无

## 下一步

- [ ] P2：`nk-brainstorm`、`nk-plan`、`nk-ideate`

## 阶段总览

| 阶段 | 内容 | 完成标志 | 状态 |
| :-- | :-- | :-- | :-- |
| **P0** | 共享约定 | 6 份约定评审通过 | **已完成** |
| **P1** | `nk-work`、`nk-commit`、`nk-handoff` | 单元验证与成稿评审通过；开始在本仓库自用 | **已完成** |
| **P2** | `nk-brainstorm`、`nk-plan`、`nk-ideate` | 单元验证与成稿评审通过 | 进行中 |
| **P3** | `nk-close`、`nk-compound` | 单元验证与成稿评审通过 | 待启动 |
| **P4** | `nk-debug`、`nk-review`、`nk-simplify` | 单元验证与成稿评审通过 | 待启动 |
| **P5** | `nk-wayfinder`、`nk-to-tasks`、`nk-wizard`、`nk-wait-what` | 单元验证与成稿评审通过 | 待启动 |
| **迁移与验收** | paper-30min 从 CE 迁移到 NexusKit，集中验收 | 产物整理、指令对齐、验收场景通过 | 待启动 |
| **打包** | 仿照 CE 结构做多 Agent 插件 | 各客户端可安装 | 待启动 |
