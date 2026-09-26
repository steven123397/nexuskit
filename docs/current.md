# 当前状态

- **所在分支**：`main`
- **版本/里程碑**：P4 已完成（沿用既定模式：并行子代理编写、Kimi Code 评审后分技能提交）
- **已具备能力**：
  - 共享约定 9 份：[`conventions/`](../conventions/)。
  - 执行闭环：`nk-commit`、`nk-work`、`nk-handoff`。
  - 规划链：`nk-ideate` → `nk-brainstorm` → `nk-plan`。
  - 知识库闭环：`nk-close`、`nk-compound`（沉淀 + 审计双模式）。
  - 质量链：`nk-debug`（复现优先 + 因果排错）、`nk-simplify`（交付后精简，行为保持）、`nk-review`（版本层面审查，产出 `docs/reviews/` 状态化条目，遗留项由 nk-close 消费）。
- **验证结果**：
  - 全仓 123 个 Markdown 文件相对链接检查：0 失效。
  - 禁用词 grep：新技能仅来源备注豁免项。
  - 集成修订：nk-work 回写审查条目状态、nk-close 引用 entry-format 状态词表、commit-cadence 归属行补全。
  - 未验证：真实项目中的端到端使用，统一放到"迁移与验收"阶段。

## 阻断与已知缺口

- 规划类技能引用了尚未实现的 `nk-to-tasks`（P5），已写不可用时的兜底；P5 完成后需回来核对（`nk-plan/references/handoff.md`）。
- `learnings-researcher`、`web-researcher` 提示词在 nk-ideate、nk-plan、nk-review 各有一份，打包阶段决定是否共享。

## 下一步

- [ ] P5：`nk-wayfinder`、`nk-to-tasks`、`nk-wizard`、`nk-wait-what`

## 阶段总览

| 阶段 | 内容 | 完成标志 | 状态 |
| :-- | :-- | :-- | :-- |
| **P0** | 共享约定 | 6 份约定评审通过 | **已完成** |
| **P1** | `nk-work`、`nk-commit`、`nk-handoff` | 单元验证与成稿评审通过；开始在本仓库自用 | **已完成** |
| **P2** | `nk-brainstorm`、`nk-plan`、`nk-ideate` | 单元验证与成稿评审通过 | **已完成** |
| **P3** | `nk-close`、`nk-compound` | 单元验证与成稿评审通过 | **已完成** |
| **P4** | `nk-debug`、`nk-review`、`nk-simplify` | 单元验证与成稿评审通过 | **已完成** |
| **P5** | `nk-wayfinder`、`nk-to-tasks`、`nk-wizard`、`nk-wait-what` | 单元验证与成稿评审通过 | 待启动 |
| **迁移与验收** | paper-30min 从 CE 迁移到 NexusKit，集中验收 | 产物整理、指令对齐、验收场景通过 | 待启动 |
| **打包** | 仿照 CE 结构做多 Agent 插件 | 各客户端可安装 | 待启动 |
