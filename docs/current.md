# 当前状态

- **所在分支**：`main`
- **版本/里程碑**：P2 已完成（按用户决定不单独写 plan，由 Claude 直接实施；三个技能由并行子代理编写、Claude 评审后提交）
- **已具备能力**：
  - 共享约定 9 份：[`conventions/`](../conventions/)。P2 新增 `plan-format.md`（统一 plan 格式，brainstorm 写需求部分、plan 补全实施部分、nk-work 按标题读取）与 `settled-decisions.md`（brainstorm/plan 共用）。
  - 执行闭环：`nk-commit`、`nk-work`、`nk-handoff`。
  - 规划链：`nk-ideate`（发想，产出 `docs/ideation/`）→ `nk-brainstorm`（需求，术语即时写入 CONCEPTS.md）→ `nk-plan`（实施方案，含写后自检）。按用户决定：只输出 Markdown；ce-doc-review 并入 nk-plan 自检；子代理保持 CE 原规模。
- **验证结果**：
  - 全仓 77 个 Markdown 文件相对链接检查：0 失效。
  - 三个技能逐一核对 CE 专有基础设施残留（lfg、html、/tmp、docs_root、packs、slack）：只剩来源备注与单词片段。
  - 未验证：真实项目中的端到端使用，统一放到"迁移与验收"阶段。

## 阻断与已知缺口

- 规划类技能引用了尚未实现的 `nk-to-tasks`（P5）、`nk-debug`（P4）、`nk-compound`（P3），均已写不可用时的兜底；对应阶段完成后需回来核对（`nk-plan/references/handoff.md`、`phase-0.md`、`synthesis-summary.md`，`nk-brainstorm/references/terminology.md`）。
- `learnings-researcher`、`web-researcher` 提示词在 nk-ideate 与 nk-plan 各有一份，打包阶段决定是否共享。

## 下一步

- [ ] P3：`nk-close`、`nk-compound`

## 阶段总览

| 阶段 | 内容 | 完成标志 | 状态 |
| :-- | :-- | :-- | :-- |
| **P0** | 共享约定 | 6 份约定评审通过 | **已完成** |
| **P1** | `nk-work`、`nk-commit`、`nk-handoff` | 单元验证与成稿评审通过；开始在本仓库自用 | **已完成** |
| **P2** | `nk-brainstorm`、`nk-plan`、`nk-ideate` | 单元验证与成稿评审通过 | **已完成** |
| **P3** | `nk-close`、`nk-compound` | 单元验证与成稿评审通过 | 待启动 |
| **P4** | `nk-debug`、`nk-review`、`nk-simplify` | 单元验证与成稿评审通过 | 待启动 |
| **P5** | `nk-wayfinder`、`nk-to-tasks`、`nk-wizard`、`nk-wait-what` | 单元验证与成稿评审通过 | 待启动 |
| **迁移与验收** | paper-30min 从 CE 迁移到 NexusKit，集中验收 | 产物整理、指令对齐、验收场景通过 | 待启动 |
| **打包** | 仿照 CE 结构做多 Agent 插件 | 各客户端可安装 | 待启动 |
