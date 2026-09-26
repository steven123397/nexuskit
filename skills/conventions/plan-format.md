# 统一 Plan 格式 (Plan Format)

> **归属与引用：** 本约定定义 plan 文件的结构契约。`nk-brainstorm` 写入 Product Contract，`nk-plan` 补全实施部分，`nk-work` 按本约定定位章节。三者都以本文件为准，不各自重述章节规则。
> **来源：** 改写自 CE `ce-plan/references/plan-sections.md` 与 `markdown-rendering.md`（2026-09）。只输出 Markdown。

---

## 一、一个需求一个文件

同一个需求只有一个 plan 文件，随规划阶段逐步充实：

1. **需求阶段**（`nk-brainstorm` 产出）：只有 Goal Capsule 与 Product Contract。
2. **可实施阶段**（`nk-plan` 补全）：追加 Planning Contract、Implementation Units、Verification Contract、Definition of Done。

不另写单独的需求文档。需求阶段的文件不能出现指向尚不存在的实施章节的内容。

**位置与命名**：`docs/plans/YYYY-MM-DD-HHMM-<type>-<topic>-plan.md`，`HHMM` 取写入时的本地时间，`<type>` 与 frontmatter 的 `type` 一致。

**生命周期**：见 [`artifact-lifecycle.md`](artifact-lifecycle.md)。执行期在分支上随代码修改，版本收尾时提炼后删除。

---

## 二、章节登记表（稳定标题）

下游按标题定位章节，标题文字就是契约，保持英文 ASCII、不得改名；正文可以用中文。

| 章节 | Markdown 标题 | 何时出现 | 用途 |
| :-- | :-- | :-- | :-- |
| Goal Capsule | `## Goal Capsule` | 始终 | 目标、手段、权威顺序、停止条件 |
| Product Contract | `## Product Contract` | 始终 | 要做什么：摘要、问题背景、需求、范围 |
| Requirements | `### Requirements`（位于 Product Contract 下） | 始终 | 带 R-ID 的需求 |
| Planning Contract | `## Planning Contract` | 可实施阶段 | 关键技术决策（KTD）、技术设计、假设、顺序 |
| Implementation Units | `## Implementation Units` | 可实施阶段 | 带 U-ID 的实施单元，标题形如 `### U3. <标题>` |
| Verification Contract | `## Verification Contract` | 可实施阶段 | 本仓库的具体验证命令与质量关卡 |
| Definition of Done | `## Definition of Done` | 可实施阶段 | 整体与各单元的完成标准 |
| Appendix | `## Appendix` | 可选 | 较长的调研材料 |
| 变更记录 | `## Change Log` | 执行期发生范围或做法变化时 | 每次变化一行：日期、改了什么、原因 |

Goal Capsule 放在最前，便于快速定位。

**按需阅读**：较长的 plan 先用 `rg -n '^#{1,3} ' <plan>` 取得章节与单元目录，再只读当前任务需要的部分（Goal Capsule、当前 U-ID 及其引用的 R/KTD、Verification Contract、Definition of Done）。一两屏以内的短 plan 直接全文阅读。

---

## 三、各章节要点

### Goal Capsule
* **Objective**：做完之后对用户或使用者而言什么成立。换一种实现方式它仍应是目标；不了解被改组件内部的人也能判断是否达成。
* **Means**：只有请求或 plan 已经确定做法时才写，一行，引用负责它的 KTD（如 `Means: … (KTD2)`），不重述机制。
* **权威顺序与停止条件**：遇到冲突时以什么为准；出现什么情况必须停下报告。

### Product Contract
必有：Summary（几句话说明提议）、Problem Frame（为什么要做，不重述方案；动机已在上游说清时写一两行即可）、Requirements。
按需：Key Decisions、Success Criteria、Actors、Key Flows、Acceptance Examples、Scope Boundaries、Open Questions、Dependencies、Sources、How This Work Fits Together（本需求是更大请求拆分出的一部分时）。判断标准是"这个 plan 有没有这一节要说的内容"，没有就省略，不写占位文字。

**语义标记**：How This Work Fits Together 一节的标题前一行放 `<!-- nk-section: work-relationships -->`。标题措辞可以改，标记不变；各技能按标记识别该节，修订时保留。

### Planning Contract
关键技术决策（KTD）、需要图示才能说清时的高层设计、假设、约束、顺序、支撑决策的调研线索。按需包括 System-Wide Impact、Risks & Dependencies。

### Implementation Units
每个单元包含：Goal、Requirements（引用 R-ID）、Files、Approach（只写本单元特有的内容，引用 R/KTD 而不重述）、Test Scenarios、Verification。单元约 10 个以上时，在本节开头加一张索引表（U-ID、标题、主要文件、依赖）。

单元的粒度按实现内容划分：一个单元应能在一个会话内完成并独立验证（参见 RFC D10，token 预算只是理念）。

### Verification Contract 与 Definition of Done
写本仓库的具体命令（如 `cargo test`、`npm test`），不写笼统的"运行测试"。优化类目标写成可度量的阈值。Definition of Done 包含清理要求：放弃的尝试留下的代码必须删除。

---

## 四、ID 与内容规则

* **稳定 ID**：R（需求）、U（单元）、KTD（关键技术决策）、A（参与者）、F（流程）、AE（验收示例）。修订时不重新编号，不为"填补空号"改号。
* **前缀写法**：`R1.`、`U1.`、`KTD1.` 作为条目开头，不加粗。
* **一条规则只在一处写全**：产品行为写在对应 R 上，实现机制写在对应 KTD 上；其他地方引用 ID，只补充本处特有的内容。层级冲突时，产品行为以 R 为准，实现机制以 KTD 为准，单元不能推翻二者。
* **已定决策标注**：用户在对话中确定的决策，在对应条目上内联标注 `(session-settled: user-directed — chosen over <备选>: <一句理由>)` 或 `user-approved`。Agent 不给自己未经用户确认的提议加这个标注。
* **术语**：使用 `CONCEPTS.md` 中的规范术语，不用同义词。规划中新确定的术语按 [`concepts-vocabulary.md`](concepts-vocabulary.md) 即时写入。
* **路径**：一律使用仓库相对路径。
* **不记录规划过程**：不写"在第几阶段得出"、不写指向下一个技能的 `## Next Steps`。下一步写在 `docs/current.md`。
* **plan 里不放跨技能契约**：plan 只记录"这次怎么做"（本次的范围、决策与单元）；"下次也照这么办"的规则属于 `conventions/` 共享约定。plan 会在版本收尾时被删除，写进去的契约会随之悬空（本体系在 P1 实际犯过一次：K 编码定义随 plan 删除，技能里的引用全部悬空）。
* **就地修改**：新的决定取代旧文字时直接改写或删除原文，不保留删除线，也不另起"补充说明"层。唯一的例外是 `## Change Log`：执行期的范围或做法变化各记一行，方便追溯。
* **行文**：先写结论再写理由；一个需求或单元是一句意图加至多一个限定；一个句子不超过一个括号说明、不超过两个分号。

---

## 五、Frontmatter

```yaml
---
title: "分页会话列表 - Plan"   # 与 H1 一致，以 " - Plan" 结尾
type: feat                     # feat / fix / refactor / chore / docs / perf / test
date: 2026-09-25
plan_contract: nk-plan/v1
product_contract_source: nk-brainstorm   # 或 nk-plan（未经 brainstorm 直接规划）
topic: paginated-sessions      # 可选：主题短名，续作时用于识别同一需求
deepened: 2026-09-26           # 可选：nk-plan 第一次实质深化本 plan 的日期，影响续作时是否再次深化
origin: docs/ideation/2026-09-20-reader-ideation.md   # 可选：上游文档
execution: code                # 可选：code（默认）或 knowledge-work（非代码交付物）
---
```

* 不设 `status` 字段，不记录执行进度。进度以带 U-ID 的提交为准（见 [`commit-cadence.md`](commit-cadence.md) R1）。
* 字段名固定，不得改名；可以新增字段。
