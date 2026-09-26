---
name: nk-review
description: "Review a version-level diff (current branch, named base ref, files, uncommitted changes, or a PR) for bugs, regressions, standards, and intent; record findings as statused entries in docs/reviews/. Use when asked to review code, review a version before merge, or audit a branch. 代码审查、版本审查、合并前审查、review。"
argument-hint: "[空=当前分支相对基线，或 base ref / 文件路径 / PR 编号]"
---

# /nk-review

> **路径解析说明：** 本文件及其 references 中引用的文件（`references/`、`../conventions/`、`../nk-commit/` 等）均相对于本技能所在目录解析，不在目标代码仓库中查找。`docs/reviews/`、`docs/plans/`、`docs/current.md`、`docs/solutions/`、`CONCEPTS.md` 指目标仓库中的文件。

在版本层面对一段 diff 做代码审查：按风险选出一队 reviewer persona，各自独立产出发现，合并复核后写入目标仓库的 `docs/reviews/`。审查发生在版本层面（合并前或阶段性），不是每个实施单元的关卡——实施单元内不设审查，由 `nk-work` 声明并执行。

**完成标志：** 被审范围解析明确，存留发现均有证据支撑并按条目格式写入 `docs/reviews/<版本或分支标识>.md`，向用户给出结论、修复顺序与覆盖说明。
**工作原则：** 只报告不修改（审查本身不改代码、不提交、不推送）；按变更的意图与项目准则评判，不按个人偏好重写；零发现是合法结果；拿不准的下沉进条目并标注缺失证据，不臆造。

---

## 执行步骤

各阶段依次执行。**进入某阶段时完整读取它要求的 reference**；提前读过的不算。读不到必需的 reference 时，在它管辖的动作之前停下，报告缺哪个文件。

```mermaid
flowchart LR
    A[1 定界] --> B[2 意图] --> C[3 编队] --> D[4 派发审查] --> E[5 合并复核] --> F[6 成文汇报]
```

### 1. 定界 (Scope)
读取 [`references/scope.md`](references/scope.md)，解析被审 diff：基线 ref、文件清单、diff 文本、范围信号与规范文件映射。基线解析失败或 diff 为空在此早停。

### 2. 意图 (Intent)
写一段 2~3 句的意图摘要（本次变更要达成什么），来源依次为：关联 plan、提交信息、PR 标题与正文、用户口述。每个 reviewer 都会收到它；意图与代码不符是高价值发现。找不到任何意图来源时在覆盖说明中注明"无意图来源"，不编造。

### 3. 编队 (Select reviewers)
读取 [`references/select-and-route.md`](references/select-and-route.md)，按 diff 的实际风险选定 persona 编队：correctness 常驻，其余按条件触发。派发前向用户宣布编队与每个条件 reviewer 的一句入选原因。

### 4. 派发审查 (Dispatch)
按 [`references/reviewer-prompt.md`](references/reviewer-prompt.md) 的模板，用 `references/personas/` 下的 persona 文件内容初始化通用子代理，一批并行派发；客户端不支持子代理时，由主会话按同一模板依次内联扮演，评审纪律（置信度锚点、引用原文门、误报抑制目录）不变。

### 5. 合并与复核 (Merge & validate)
读取 [`references/validate.md`](references/validate.md)：校验与去重各 reviewer 的返回，套用置信度闸门，再对存留发现做一轮独立复核（confirmed / rejected / unresolved），定稿后一次性分配条目编号。

### 6. 成文与汇报 (Record & report)
读取 [`references/entry-format.md`](references/entry-format.md)：新一轮审查向本版本的 `docs/reviews/` 文件追加一轮区块，写入条目与覆盖说明；在聊天中给出浓缩结论（结论 / 理由 / 修复顺序）。

**可选：PR 评论。** 项目走 PR 流程且用户需要时，把审查摘要同步为 PR 评论；不走 PR 的项目完全不影响主流程。

---

## 与体系衔接（各守边界，规则以被引用方为准）

- **修复**：本技能不改代码。条目由 `nk-work` 认领修复；修复时顺手把条目状态改为 `已修复`，随修复提交入库（[`../conventions/commit-cadence.md`](../conventions/commit-cadence.md) R2/R6）。
- **新发现分流**：审查发现的处理遵循 [`../conventions/artifact-lifecycle.md`](../conventions/artifact-lifecycle.md) 第四章——小问题随修复走 `nk-work`，跨 plan 疑难转 Issue（无远端记 `docs/backlog.md`），不顺手扩大范围。
- **阻断登记**：结论为"存在阻断项"（未修复的 P0）时，按 [`../conventions/current-md.md`](../conventions/current-md.md) 登记到目标仓库 `docs/current.md` 的"阻断与已知缺口"。
- **提交**：本技能不发起提交；新建的审查记录留在工作区，随下一个代码提交（R2）或会话交接（`nk-handoff`，R4）入库。
- **收尾**：版本收尾时由 `nk-close` 依据条目的状态标记甄别遗留项、转 Issue 并删除审查记录文件。
