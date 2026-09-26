# 当前状态

- **所在分支**：`main`
- **版本/里程碑**：P3 已完成（沿用 P2 模式：子代理编写、Kimi Code 评审后提交；编写代理中断一次，恢复后产物完整）
- **已具备能力**：
  - 共享约定 9 份：[`conventions/`](../conventions/)。
  - 执行闭环：`nk-commit`、`nk-work`、`nk-handoff`。
  - 规划链：`nk-ideate` → `nk-brainstorm` → `nk-plan`。
  - 知识库闭环：`nk-close`（版本收尾六步法的可执行展开；未消费发想记录与推迟 plan 逐项询问、每轮最多 3 个——用户 2026-09-25 拍板）、`nk-compound`（沉淀模式 + 审计模式；refresh 并入为模式，RFC 开放问题 2 就此落定）。
- **验证结果**：
  - 全仓 90 个 Markdown 文件相对链接检查：0 失效（`file:///` 本地路径为例外）。
  - 禁用词 grep（lfg、/tmp、docs_root、packs、slack 等）：nk-close 零命中；nk-compound 只剩来源备注豁免项。
  - 未验证：真实项目中的端到端使用，统一放到"迁移与验收"阶段。

## 阻断与已知缺口

- 规划类技能引用了尚未实现的 `nk-to-tasks`（P5）、`nk-debug`（P4），均已写不可用时的兜底；对应阶段完成后需回来核对（`nk-plan/references/handoff.md`、`phase-0.md`、`synthesis-summary.md`）。
- `learnings-researcher`、`web-researcher` 提示词在 nk-ideate 与 nk-plan 各有一份，打包阶段决定是否共享。

## 下一步

- [ ] P4：`nk-debug`、`nk-review`、`nk-simplify`

## 阶段总览

| 阶段 | 内容 | 完成标志 | 状态 |
| :-- | :-- | :-- | :-- |
| **P0** | 共享约定 | 6 份约定评审通过 | **已完成** |
| **P1** | `nk-work`、`nk-commit`、`nk-handoff` | 单元验证与成稿评审通过；开始在本仓库自用 | **已完成** |
| **P2** | `nk-brainstorm`、`nk-plan`、`nk-ideate` | 单元验证与成稿评审通过 | **已完成** |
| **P3** | `nk-close`、`nk-compound` | 单元验证与成稿评审通过 | **已完成** |
| **P4** | `nk-debug`、`nk-review`、`nk-simplify` | 单元验证与成稿评审通过 | 待启动 |
| **P5** | `nk-wayfinder`、`nk-to-tasks`、`nk-wizard`、`nk-wait-what` | 单元验证与成稿评审通过 | 待启动 |
| **迁移与验收** | paper-30min 从 CE 迁移到 NexusKit，集中验收 | 产物整理、指令对齐、验收场景通过 | 待启动 |
| **打包** | 仿照 CE 结构做多 Agent 插件 | 各客户端可安装 | 待启动 |
