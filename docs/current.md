# 当前状态

- **所在分支**：`main`
- **版本/里程碑**：Phase 0 完成（共享约定就绪并通过条件审查修复）
- **已具备能力**：
  - 6 份核心共享约定已在 [`conventions/`](../conventions/) 落地并通过自洽审查：
    - [`current-md.md`](../conventions/current-md.md)：明确单例接力分工，增加工作区未提交改动声明，杜绝单元级重复记账；
    - [`commit-cadence.md`](../conventions/commit-cadence.md)：明确纯规划会话与 compound 的合法提交时机，给出未推送的可执行判定；
    - [`artifact-lifecycle.md`](../conventions/artifact-lifecycle.md)：明确收尾甄别迁移、收尾时机（合并前）与 AGENTS.md 知识指引责任；
    - [`concepts-vocabulary.md`](../conventions/concepts-vocabulary.md)：引入即时质疑机制、删除需正面证据与老项目 refresh 初建路径；
    - [`solution-schema.md`](../conventions/solution-schema.md)：严格对齐 CE schema 与语料优先原则，支持轻量决策与结构化决策双档粒度；
    - [`decision-autonomy.md`](../conventions/decision-autonomy.md)：收紧决策自决边界，补充批量提问规则与无人值守模式推断处理。
  - 全文已完成去绝对化润色，语气平实客观。
- **验证结果**：
  - 6 份约定内部交叉引用（R1~R6、收尾六步法、双轨准入）已完整闭环对齐。
  - Claude Code P0 评审指出的 10 项改进点已全部落实修复。

## 阻断与已知缺口

- 无

## 下一步

- [ ] 编写 P1 技能简报：`docs/briefs/nk-work.md`
- [ ] 编写 P1 技能简报：`docs/briefs/nk-commit.md`
- [ ] 编写 P1 技能简报：`docs/briefs/nk-handoff.md`

## 阶段总览

| 阶段 | 内容 | 状态 |
| :-- | :-- | :-- |
| **P0** | 共享约定（6 份规范） | **已完成** |
| **P1** | 核心执行三件套（`nk-work`, `nk-commit`, `nk-handoff`） | 待启动简报 |
| **P2** | 规划与设计三件套（`nk-brainstorm`, `nk-plan`, `nk-ideate`） | 待排期 |
| **P3** | 沉淀与收尾两件套（`nk-close`, `nk-compound`） | 待排期 |
| **P4** | 诊断与质控三件套（`nk-debug`, `nk-review`, `nk-simplify`） | 待排期 |
| **P5** | 寻路与扩展（`nk-wayfinder`, `nk-to-tasks` 等） | 待排期 |
