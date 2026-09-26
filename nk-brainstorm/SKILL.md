---
name: nk-brainstorm
description: Explore a vague or ambitious idea into a right-sized requirements-only plan (Goal Capsule + Product Contract) that nk-plan can build on; resolve WHAT to build, scope and success criteria through dialogue, capturing domain terms into CONCEPTS.md as they settle. Not for executing specified work (nk-work) or planning HOW (nk-plan). 头脑风暴、需求澄清、明确范围、要做什么、产品需求。
---

# /nk-brainstorm

> **路径解析说明：** 本文件中的路径相对于本技能目录解析（共享约定位于 `../conventions/`，其他技能位于 `../nk-*/`）；`references/` 内文件中的路径相对于该文件所在目录解析（即 `../../conventions/`、`../../nk-*/`）。不在目标代码仓库中查找这些文件。

通过对话回答**要做什么**（WHAT）：产品行为、范围边界、成功标准。`nk-plan` 随后在同一个 plan 文件里补充**怎么做**（HOW）。本技能不写代码、不做技术方案。

**产出：** 与工作规模相称的结果，让 `nk-plan` 不必自行发明产品行为、范围或成功标准：
* **Lightweight**：在对话中以一段话结束，不写文件。
* **需要文件时**：按 [`../conventions/plan-format.md`](../conventions/plan-format.md) 写一个需求阶段的 plan（Goal Capsule + Product Contract），`product_contract_source: nk-brainstorm`。

**完成标志：** 文件已写入并通过 Ready for Planning Check（或按规则不需要文件）；对话中敲定的术语已写入 `CONCEPTS.md`；第 4 阶段的交接选项已呈现。

**改为分流的三种情况**（由 `references/phase-0.md` 判定）：非软件话题改走 `references/universal-brainstorming.md`；简单求助、事实问题、单步任务直接回答；需求已经明确到可以直接实施的，建议 `/nk-plan` 或 `/nk-work`。

调用时未带需求描述：先问用户想探讨什么，得到回答前不继续。

---

## 执行流程

进入某个阶段时读取该阶段的 reference，不凭记忆代替。

| 阶段 | 先读 | 该文件负责的内容 |
| :-- | :-- | :-- |
| 第一个问题之前（全程有效） | `references/interaction-rules.md` | 核心原则；提问规则（批量合并、选项带推荐、只问用户才能决定的事、无人值守处理） |
| 把对话中的决定当作已定之前 | [`../conventions/settled-decisions.md`](../conventions/settled-decisions.md) | 已定判定标准与标注格式，避免重复追问已定的事 |
| 0 续作、分类、规模 | `references/phase-0.md` | 续作检查；软件/非软件/无需头脑风暴的分类；规模分级；单一工作单元检查；可视化与陌生领域两个触发条件 |
| 1 理解想法 | `references/dialogue.md` | 现状扫描与 grounding 侦察；产品压力测试；对话推进；退出条件 |
| 1 全程：术语 | `references/terminology.md` | 术语即时质疑与即时写入 `CONCEPTS.md` 的操作流程 |
| 2–2.6 方案、综述、核实 | `references/approaches.md`，写综述前再读 `references/synthesis-summary.md` | 方案生成；范围综述与确认；声明核实 |
| 3 写入 plan | `references/sections.md` | 是否需要文件；Product Contract 各节要求；Markdown 写法；Ready for Planning Check |
| 4 交接 | `references/handoff.md` | 交接选项、会话结束与提交方式、结束摘要 |

按需读取：`references/product-pressure-test.md`（第 1.2 步）、`references/blindspot-pass.md`（陌生领域）、`references/visual-probes.md`（形状类决策）、`references/model-tiers.md`（派发子代理前）。

以下规则无需读取任何文件即成立：

* **只输出 Markdown。**
* **写入文件时产物契约不变**：路径、frontmatter、章节以 `plan-format.md` 为准；本技能只写 Goal Capsule 与 Product Contract，不写空的实施章节。
* **Ready for Planning Check 有任何一项不通过，不宣告写入完成，也不进入第 4 阶段。**
* **术语在对话中敲定即写入 `CONCEPTS.md`**，不攒到最后；用户用词与术语表冲突时当场指出。
* **不提交。** 同一会话继续规划或实施时，产出留在工作区随下一个提交入库；会话在此结束时，由 `../nk-handoff/SKILL.md` 把 plan、`CONCEPTS.md`、`current.md` 合为一次提交（见 `../conventions/commit-cadence.md` R4）。

子代理（grounding 侦察、声明核实）按任务形态分档，不写死模型名；支持子代理时派发，否则在主会话内联完成，读取预算与产出上限不变。
