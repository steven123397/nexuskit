---
name: nk-plan
description: "Create or enrich a technical implementation plan (HOW) for multi-step work, including non-software tasks: research, key technical decisions, implementation units, verification. Use when asked to plan, break down implementation, plan from a brainstorm/requirements doc, or deepen an existing plan; prefer nk-brainstorm for exploratory scoping. 技术规划、实施计划、拆分实施单元、补全需求文档、深化 plan。"
argument-hint: "[需求描述、需求阶段 plan 路径、要深化的 plan 路径，或任何要规划的任务]"
---

# /nk-plan

> **路径解析说明：** 本文件及其 references 中引用的文件（`references/`、`../conventions/`、`../nk-work/`、`../nk-handoff/`）均相对于本技能所在目录解析，不在目标代码仓库中查找。`docs/plans/`、`docs/solutions/`、`docs/current.md`、`CONCEPTS.md` 指目标仓库中的文件。

`nk-brainstorm` 定义**做什么**，`nk-plan` 规划**怎么做**，`nk-work` 执行。上游 brainstorm 不是必需的。

**完成标志**：产出一份能指导执行和验证的 plan，保留约定的结果和约束；技术选择以证据为依据，已经足够的说明不改动。Durable 路线要到收尾菜单的所选动作真正执行后才算完成；Direct 与 Chat brief 在聊天中给出结果和交接提议即完成。

**只调研、决策、写 plan，不实现。** 不写生产代码、不运行测试、不从执行结果中学习。方向性的伪代码或语法草图可以用来表达设计。

**plan 文件的结构契约是 [`../conventions/plan-format.md`](../conventions/plan-format.md)**：章节标题、ID 规则、frontmatter 都以它为准，本技能的 references 只补充"怎么写好"。

## 提问方式

按 [`../conventions/decision-autonomy.md`](../conventions/decision-autonomy.md)：可逆、局部、有惯例可循的事自己定并写明理由；只有答案会实质影响架构、范围、顺序或风险、又无法合理推断时才问。互不依赖的问题合并为一轮（至多 3 个），每个给 2–3 个选项并标出 `(Recommended)`；有依赖关系时才分轮。有选择题工具就用，没有时在聊天中列编号选项，不悄悄跳过必要的问题。无人值守时采用推荐项，推断项写进 plan 的 `### Assumptions`，需要确认的事项在 `docs/current.md` 登记 `[待确认]`。

没有给出要规划的内容时，先问要规划什么。

## 术语

规划中敲定了新的领域术语、或发现用词与 `CONCEPTS.md` 冲突时，按 [`../conventions/concepts-vocabulary.md`](../conventions/concepts-vocabulary.md) 当场处理：冲突当面指出并对齐，合格的新术语立即写入 `CONCEPTS.md`。

## 流程

各阶段依次执行，某个 reference 选定了其他路线就照那条走。**进入某阶段时完整读取它要求的 reference**；提前读过的不算，要求"在某步再读一次"的就再读。读不到必需的 reference 时，在它管辖的动作之前停下，报告缺哪个文件，不凭记忆补规则。

| 阶段 | 先读 | 内容 |
| :-- | :-- | :-- |
| 0 续写、分流、定界 | `references/phase-0.md` | 核心原则与质量底线；续写与深化快速通道；做法层规划与非软件分流；查找上游 Product Contract（含 `topic:` 识别）并就地补全；规划引导；阻塞处理；输出档位（Direct / Chat brief / Durable）与规划深度；独立规划的范围确认 |
| 0 的分支 | `references/output-contracts.md`、`references/approach-altitude.md`、`references/universal-planning.md`、[`../conventions/settled-decisions.md`](../conventions/settled-decisions.md) | 两个聊天档位；先规划做法；非软件规划；本会话已定决策的判定与标注 |
| 范围确认（0.7 / 5.1.5） | `references/synthesis-summary.md` | 内部三分草稿、分歧点保留测试、确认模板、写入 plan 的去向 |
| 1 调研 | `references/research.md` | 本地研究员、Agent 原生能力评估、执行方向、外部调研决策与派出、整合、升档、行为追踪、流程分析、设计对比入口 |
| 1.6 设计对比（按需） | `references/design-alternatives.md` | 后果重大的"怎么做"未定时，并行展开截然不同的设计并比较 |
| 2–4 问题、结构、成文 | `references/structure.md` | 规划问题归类与提问；单元划分与字段；高层设计触发条件；行文与 Markdown 写法；规划规则 |
| 5.1–5.3 写前检查、写入、深化判断 | `references/final-review.md` | 写前清单；承接上游的范围确认；写入 plan；置信度检查与是否深化 |
| 5.3.3–5.3.7 深化（按需） | `references/deepening-workflow.md` | 章节打分、章节到子代理的对应、执行方式、交互审阅、整合 |
| 5.3.8 写后自检 | `references/self-review.md` | 连贯性与可行性（总是）、范围守护、安全、设计、产品、对抗性（按信号） |
| 5.4 收尾 | `references/handoff.md` | 能否交给实施；自检结果；NexusKit 收尾菜单与执行 |

调研与深化用到的研究员和审阅视角提示词在 `references/agents/`，是提示词资产而不是可按名字调用的 Agent：读取文件内容，用它初始化一个通用子代理。支持子代理的客户端并行派出；不支持时在主会话中依次完成。

## 始终成立的规则

* **先写文件，再给选项**：Durable 路线在展示收尾菜单前 plan 已写入 `docs/plans/`。
* **一个需求一个文件**：已有 `nk-brainstorm` 产出的需求阶段 plan 时，就地补全同一文件，保留 Product Contract 的含义、稳定 ID、`topic:` 字段和 `<!-- nk-section: ... -->` 标记。
* **plan 不记执行进度**：没有 `status` 字段，不加复选框；进度以带 U-ID 的提交为准。
* **不重问已定决策**；已定标注也不压制缺陷证据。
* **提交**：`nk-plan` 本身不提交。会话在规划后结束时，由 `nk-handoff` 把规划产出和 `docs/current.md` 合成一次交接提交；同一会话接着用 `nk-work` 实施时，规划产出随第一个单元的提交一起入库（[`../conventions/commit-cadence.md`](../conventions/commit-cadence.md) R4）。
