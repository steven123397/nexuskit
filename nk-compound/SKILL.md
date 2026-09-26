---
name: nk-compound
description: "Capture a verified solved problem or durable decision as a learning in docs/solutions/, or audit the knowledge base (docs/solutions/ + CONCEPTS.md) for stale, drifted, or contradictory entries. Use when verified work produced non-obvious reasoning the final code and tests don't record, when asked to document a lesson or decision, or when asked to audit/refresh/clean up the learnings store. 沉淀经验、记录决策、复盘工作流、审计知识库、清理过期条目、refresh。"
argument-hint: "[可选：简短上下文 | refresh [范围提示]]"
---

# /nk-compound

> **路径解析说明：** 本文件及其 references 中引用的文件（`references/`、`../conventions/`、`../nk-commit/`）均相对于本技能所在目录解析，不在目标代码仓库中查找。`docs/solutions/`、`docs/current.md`、`CONCEPTS.md`、`AGENTS.md` 指目标仓库中的文件。

两个模式：**沉淀模式**（默认）把刚解决并验证过的问题或决策写入 `docs/solutions/`；**审计模式**（`refresh`）对照当前代码库审计既有条目与 `CONCEPTS.md`。条目的 frontmatter 与正文模板以 [`../conventions/solution-schema.md`](../conventions/solution-schema.md) 为准，本技能不另造格式。

**完成标志：** 沉淀模式——一条合格条目写入（或明确报告为何不建档），术语补全、可见性检查、提交去向处理完毕并汇报；审计模式——范围内每条目得到分类，动作执行完毕，报告直接呈现给用户。

## 模式判定

- 参数以 `refresh` 开头，或明确要求审计/清理知识库 → **审计模式**，其余词作范围提示；无提示则全量。
- 明确要求初建 `CONCEPTS.md`（建立整个项目的术语表）→ 审计模式的整库初建路径（见 `references/audit.md`）。
- 其余 → **沉淀模式**，其余词作简短上下文。

## 准入门槛（沉淀模式）

只沉淀**已解决且已验证**的问题（未运行的验证不记为通过，见 [`../conventions/commit-cadence.md`](../conventions/commit-cadence.md) 通用纪律）。按 solution-schema 第一章的双轨准入判断：

- **Bug 轨**（排查/缺陷/性能/构建）：反事实检验——若无此文，未来仅凭代码与单测是否仍极可能重蹈覆辙或耗时重探？
- **Knowledge 轨**（架构决策/规范/最佳实践）：决策三门槛——难以撤回、无背景会困惑、确有取舍。`workflow_issue` 让工作流与协作过程本身的复盘也可入库。

任一不通过：不建档，向用户说明原因。完成度、工作量、diff 大小不构成资格；已有条目失准则更新它，不建重复文档。**一次运行只沉淀一条**；一个会话产出多条时分多次运行。

## 沉淀模式流程

进入各阶段时完整读取对应 reference：

| 阶段 | 先读 | 内容 |
| :-- | :-- | :-- |
| 1 定位与采样 | `references/capture.md` | 从当前会话上下文与 `git log`/diff 定位刚解决的问题；语料优先采样；重叠判定（高重叠→更新既有条目） |
| 2 编写与自检 | `references/capture.md`、`references/frontmatter-checklist.md`、`references/claims-checklist.md` | 按 solution-schema 模板成文；frontmatter 与正文引用逐项自检 |
| 3 术语补全 | `references/capture.md`、[`../conventions/concepts-vocabulary.md`](../conventions/concepts-vocabulary.md) | 只做 Add/Refine，不整库初建 |
| 4 可选增强评审 | `references/capture.md` | 按 problem_type 映射 `references/agents/` 提示词；只评审文档，不改产品代码 |
| 5 可见性与提交 | `references/capture.md` | 首运行检查 `AGENTS.md` 入口指引；按 R4 第 4 条决定提交去向 |

## 审计模式流程

| 阶段 | 先读 | 内容 |
| :-- | :-- | :-- |
| 1 范围与调查 | `references/audit.md` | 范围提示收窄；逐条对照当前代码库核对；`retire_when` 条件检查；集合层面查重叠/取代/矛盾 |
| 2 分类与执行 | `references/audit.md` | Keep / Update / Consolidate / Replace / Delete；删除需正面证据 |
| 3 术语对账 | `references/audit.md` | `CONCEPTS.md` 全操作集（含 Fold/Retire/Scrub）与老项目整库初建 |
| 4 报告与提交 | `references/audit.md` | 报告直接呈现，分 Applied / Recommended；默认不落地成长期文件 |

## 始终成立的规则

- **写入边界**：沉淀模式只写本次条目（或更新既有条目）、`CONCEPTS.md` 补全、缺指引时 `AGENTS.md` 的一行指引；审计模式只改知识库文件。两种模式都不改产品代码；条目与其点名的指导文件（SKILL.md、runbook、指令文件）冲突时只报告，不编辑指导文件。
- **删除需要正面证据**：代码被删不构成删除条目的理由；不确定时保留（细则见 `references/audit.md`）。
- **子代理**：`references/agents/` 是提示词资产而非具名 Agent——读取文件内容初始化通用子代理；客户端不支持子代理时由主会话内联完成。子代理不写产品文件、不执行 `git commit`。
- **提交**：沉淀严格按 [`../conventions/commit-cadence.md`](../conventions/commit-cadence.md) R4 第 4 条；amend 必须显式限定路径（`git add <具体文件>` + `git commit --amend --no-edit -- <路径>`）。本技能自己发起提交时先读 [`../nk-commit/SKILL.md`](../nk-commit/SKILL.md)。
- **提问**：按 [`../conventions/decision-autonomy.md`](../conventions/decision-autonomy.md) 批量选项提问；无人值守时的待确认项在 `docs/current.md` 登记 `[待确认]`。

---

> 主要参考：CE `ce-compound` / `ce-compound-refresh` (2026-09)、NexusKit 共享约定
>
> 与 CE 的主要差异及原因：
> * refresh 并入为审计模式而非独立技能：同一知识库的写入与维护收拢在一个入口，`refresh` 参数切换。
> * scripts/ 整体删除：两份校验脚本转写为 `references/frontmatter-checklist.md` 与 `references/claims-checklist.md` 的人工核对清单；session-history 脚本组删除，改用当前会话上下文 + `git log` 定位刚解决的问题，依赖脚本的 session-historian 提示词随之删除。
> * CE 基础设施删除：`docs_root` / `.compound-engineering` 配置层、Compound Packs、Proof 发布、Slack、auto-memory 与浏览器相关步骤。
> * 模式裁剪：去掉 mode/depth token 体系（interactive/non-interactive、full/lightweight），沉淀走单一流程；无人值守场景由 `../conventions/decision-autonomy.md` 统一覆盖。
> * 提交纪律改为 commit-cadence R4 第 4 条（优先随代码提交、未推送则限定路径 amend、已推送则留工作区），而非 CE 的独立文档提交与建分支。
> * 可见性检查并入首运行职责：按 artifact-lifecycle 第二章补 `AGENTS.md` 指引，而非每次运行单独征询。
> * 术语表规则归 `../conventions/concepts-vocabulary.md`：本技能沉淀模式只做 Add/Refine，Fold/Retire/Scrub 与整库初建归审计模式。
