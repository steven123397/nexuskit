---
name: nk-to-issue
description: "Verify and analyze a bug or new requirement spotted mid-development, then file it as a ready-to-pick-up Issue without interrupting the ongoing task. Use when asked to note a todo, file a bug, record a finding, or defer something into an issue. 记个待办、落档 bug、把这个发现记下来、先不处理转成 issue、nk-to-issue。"
argument-hint: "[一句话 bug 报告 / 新需求描述 / Issue 编号]"
---

# /nk-to-issue

> **路径解析说明：** 本文件中引用的参考文件（如 `../conventions/`）均相对于本技能所在目录解析，不在目标代码仓库中查找；`docs/`、`CONCEPTS.md`、`AGENTS.md` 等路径指目标代码仓库。

典型场景：正在推进开发任务时发现了 bug 或冒出新需求，但当前任务不适合中断。用户另开一个会话调用本技能，核实问题、分析需求，落档为一条可接手的 Issue，然后回到原会话继续。

**完成标志：** 产出一条符合写作规范的 Issue（或 backlog 条目），证据与核实结论齐全，用户拿到链接/位置；或核实后判定不该落档，向用户如实报告原因。
**工作原则：** 只核实不修复；只落档不开始做；证据不足如实写明缺口，不编造。

---

## 执行步骤

### 1. 分诊 (Triage Input)
判定输入属于哪一类：
- **bug 报告**：某个行为不符合预期；
- **新需求**：想要的功能或改进；
- **Issue 编号**（如 `#42`）：核实既有 Issue，补充证据后更新它，而不是新建。

能根据描述与代码库推断的就先推断；仅当输入完全不足以行动（无法定位涉及的行为、不知是 bug 还是需求）时才向用户提问，按 [`../conventions/decision-autonomy.md`](../conventions/decision-autonomy.md) 批量提出，单轮最多 3 个；无人值守时用推荐方案推进并登记 `[待确认]`。

### 2. 核实与分析 (Verify & Analyze)
- **bug 路径**：轻量核实——按描述读相关代码、跑一次复现步骤，目标是确认问题真实存在并收集证据（脱敏后的报错摘要、涉及的接口与行为契约）。**核实中不修复**：顺手把 bug 修掉属于越界——用户正在别的会话推进任务，修复归 [`../nk-debug/SKILL.md`](../nk-debug/SKILL.md)。确实无法复现也如实落档，写清已尝试的步骤与还缺什么信息。
- **需求路径**：界定范围与大致规模；说明与 `CONCEPTS.md` 领域概念、当前 Plan、`docs/ideation/` 发想记录的关系。确实复杂到需要规划的，落档时在条目中注明"建议走 nk-brainstorm / nk-plan"，本技能不替它做规划。

### 3. 查重与历史 (Dedup & History)
落档前运行三项检查，发现的重复/已否决/已实现**向用户报告并结束**，不照常落档：
1. **重复**：`gh issue list`（含已关闭）与 `docs/backlog.md` 中是否已有同一事项；
2. **已实现**：按领域概念（而非仅按请求的措辞）搜索代码库，防止把已实现的功能记成需求；
3. **曾否决/已沉淀**：查 `docs/ideation/`（未选中的方向）、已关闭 Issue、`docs/solutions/`，看该想法是否曾被否决或已有沉淀结论——命中时把当时的理由呈现给用户。

### 4. 落档 (File It)
按 [`../conventions/issue-writing.md`](../conventions/issue-writing.md) 的条目格式写作（遵循四原则：持久性优于精确、行为而非步骤、验收标准可独立验证、范围边界明确；bug 必填 Evidence 小节，写明核实结论与复现步骤）：
- **有 GitHub 远端**：`gh issue create` 创建；核实既有 Issue 的用 `gh issue comment` 补充证据。
- **无远端**：追加到 `docs/backlog.md`。该改动按提交节奏 R2 不单独提交，随下一个代码提交或会话交接入库。

把 Issue 链接或 backlog 位置给用户看。

### 5. 结束 (Wrap Up)
一句话提示用户回原会话继续。本技能不发起交接提交：没有仓库改动时不涉及 `nk-handoff`；若写了 `docs/backlog.md`，提示一句该改动留在工作区、将随下次提交或交接入库即可。

---

## 边界

- **只核实不修复**：确认问题存在、收集证据即停手；动手修复走 [`../nk-debug/SKILL.md`](../nk-debug/SKILL.md)。
- **只落档不开始做**：不为新落档的 Issue 开工；认领执行是 [`../nk-work/SKILL.md`](../nk-work/SKILL.md) 的事。
- **不落档的场景**：查重发现重复、已实现、曾被否决，或用户听完分析后决定放弃——如实报告即结束，不产生任何条目。
