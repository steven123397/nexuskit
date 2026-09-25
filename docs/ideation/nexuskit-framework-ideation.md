# NexusKit 体系架构立项与设计构想 (Ideation RFC)

> **Document Version:** 2.0.0
> **Date:** 2026-09-25
> **Status:** Approved — 进入实施
> **Author:** steven123397（设计评审：Claude）

v2.0 相对 v1.0 的主要变化：从"固定流水线"改为"按场景取用的工具箱"；Issue 的职责收窄到跨 plan 的事务；新增产物生命周期、`current.md` 入口约定、提交节奏规则、术语维护时机；ADR 并入 `solutions/`；新增实施方法一章。

---

## 一、背景

实战验证基地：[`D:\codex_project\paper-30min`](file:///D:/codex_project/paper-30min)（先后完整运行过 Matt 体系与 CE 体系）。

参考源：
* **Matt Pocock Skills**：[`C:/Users/29617\.agents\backups\mattpocock-skills-20260824-193425`](file:///C:/Users/29617/.agents/backups/mattpocock-skills-20260824-193425)
* **Compound Engineering (CE)**：[`C:/Users/29617\.gemini\config\plugins\compound-engineering`](file:///C:/Users/29617/.gemini/config/plugins/compound-engineering)

NexusKit 是一套**个人体系**：用户画像是个人项目、同时使用多种 Agent（Claude Code / Codex / Antigravity 等）、不强制走 PR、中文协作。两套参考源是素材库，不是需要保持同步的上游。

---

## 二、两套体系的得失（基于 paper-30min 实证）

### CE

**优势**
* `ideate → brainstorm → plan` 层次清楚，抓大放小，不纠缠细节。
* `ce-compound` 把非显而易见的因果沉淀进 `solutions/`，解决跨会话失忆。
* 技能文本打磨得细，边界情况考虑周全（代价是很重：`ce-plan` 连同 references 约 3500 行）。

**问题**
1. **主会话上下文膨胀**：`ce-work` 倾向由一个主对话承包整份 plan，上下文飙升后注意力漂移。
2. **产物无生命周期**：plan、review 写成本地 Markdown 后没有归宿（paper-30min 一天内产生 5 份 `docs/reviews/`）。
3. **术语表只在 compound 时生长**：`ce-brainstorm` 只把 `CONCEPTS.md` 当冲突检查读，从不写；新术语恰恰诞生在 brainstorm/plan 阶段。paper-30min 迁移到 CE（`56dc422`）后 `CONCEPTS.md` 再无改动。
4. **无提交节奏约束**：常见"代码提交后再为 `current.md` 小改单独提交一次"（见 `54849fd`、`0e05c8d`、`9f32bdf`、`894f51a`、`5df3454`）。

### Matt

**优势**
* 一个任务对应一个干净的新会话，上下文始终在最佳区间。
* 用 GitHub Issues 管理任务与阻塞关系，状态更新不产生 commit。
* `wayfinder`：面对超大未知目标时用探针逐步驱散迷雾。
* `domain-modeling`：术语一经敲定立即写入术语表。
* `tdd`：测试先行的纪律。

**问题**
1. **`grill` 盘问繁琐**：把大量可推断的细节抛回给人，违背分担认知负荷的初衷。
2. **同样存在产物堆积**：Matt 时期留下 11 份 `docs/draft/*-walkthrough.md`、大量 `docs/background/` 与每份仅 7 行的 ADR，最终在 `56dc422` 统一清理。**堆积是生命周期问题，不是哪套体系独有的问题。**
3. **缺少跨会话的长期知识沉淀**。

---

## 三、设计决定

| # | 决定 | 要点 |
| :-- | :-- | :-- |
| D1 | **工具箱，不是流水线** | 每个技能可独立使用；README 给出"什么场景用哪个"的路由表，而非必经链路。与 paper-30min `release-workflow.md` 的结论一致："不要求每个版本走固定的技能链"。 |
| D2 | **`docs/current.md` 是跨会话入口** | 新会话从这里进入。只记当前能力、验证结果、阻断项、下一步、所在分支；不记操作流水。 |
| D3 | **所有产物都有生命周期** | 每类产物诞生时就确定终点（见第四章）。清理挂在"版本收尾"上，不挂在 PR 上；PR 可选。 |
| D4 | **plan 与审查记录"活时在本地，死后从 main 消失"** | 执行期留在版本分支、随代码一起修改提交；收尾时提炼长期价值后删除，git 历史保留原文。 |
| D5 | **Issue 负责跨 plan 的事务** | 待办、疑难缺陷、推迟的工作、wayfinder 探针。plan 内部的实施单元不拆 Issue，靠 plan + `current.md` 接力。`nk-to-tasks` 降为可选（并行或长期挂起时才用）。 |
| D6 | **去掉 grill；术语即时写入** | 以 CE 的 ideate/brainstorm 为主体。Agent 对可逆、局部、有惯例可循的事自行决定并注明理由；只对范围变化、不可逆、数据/API 契约类分歧询问人。术语写入时机取 Matt（brainstorm/plan 中敲定即写），格式规则取 CE（`concepts-vocabulary.md`）。 |
| D7 | **ADR 并入 `solutions/`** | 取消 `docs/adr/`，"决策"作为 solution 的一种类型。入选门槛沿用 Matt 三条：难以撤回、无背景会困惑、确有取舍。D4 删除 plan 后，决策理由需要去处，这正是收尾时提炼的主要内容。 |
| D8 | **自主体系，审慎派生** | 以 CE/Matt 原文为起点改写，按自己的画像取舍；每个技能记录一行来源备注，不维护同步机制。删减原则见第七章。 |
| D9 | **提交节奏规则** | 见第五章。 |
| D10 | **任务粒度按实现内容切** | 200k~300k Token 是设计理念（单会话能舒适完成），不是硬约束，不写进任何可执行规则。 |

---

## 四、产物与生命周期

| 产物 | 位置 | 生命周期 |
| :-- | :-- | :-- |
| Plan（目标、范围、关键决策、实施单元、变更记录） | 版本分支 `docs/plans/` | 执行中直接修改，与代码同一提交；版本收尾时提炼后删除 |
| 审查记录（待修清单、收敛结论） | 版本分支 `docs/reviews/` | 同上；遗留项转 Issue 或 `current.md` 阻断项 |
| 进度、阻断项、下一步 | `docs/current.md` | 常驻，在交接点覆盖更新 |
| 待办、疑难缺陷、推迟项、探针 | GitHub Issues（无远端时退化为 `docs/backlog.md`） | 关闭即结束 |
| 踩坑因果、决策理由 | `docs/solutions/` | 永久；由 refresh 审计过期 |
| 领域术语 | `CONCEPTS.md` | 永久；由 refresh 审计 |
| 项目特有流程（分支、发布、签名等） | 项目自己的工作流文档，由 `AGENTS.md` 指向 | 项目自行维护；技能读取、不内置 |
| PR 描述 | 可选 | 有 PR 时收尾步骤写摘要，没有就跳过 |

**执行中新发现的分流规则**
* 影响当前 plan 的范围或做法 → 改 plan，末尾加一行变更记录，随代码提交。
* 与当前 plan 无关的需求或疑难缺陷 → 开 Issue。
* 小缺陷 → 随当前实施单元修复并验证。

**版本收尾**（`nk-close`）依次完成：遗留项转移 → 提炼 solutions/术语 → 删除 plans 与 reviews → 更新 `current.md` 为合并后仍准确的状态 → 单个收尾提交 →（可选）写 PR 摘要。

---

## 五、提交节奏规则

* **R1 提交单位是"一个经过验证的变化"**：代码、测试及描述该变化的文档（plan、`CONCEPTS.md`、`current.md`）同一提交。顺序固定为 实现 → 验证 → 更新文档 → 一次性提交。
* **R2 纯状态改动不单独提交**：中途产生的 `current.md`、plan 进度、审查记录改动留在工作区，随下一个代码提交走。
* **R3 未推送的补记用 amend**：上一个提交未推送、要补的只是它的状态记录时，`git commit --amend`。已推送则走 R2。
* **R4 纯文档提交只允许两个时刻**：会话结束交接（每会话最多一次）和版本收尾。
* **R5 `current.md` 只在交接点更新**：会话结束、阻断项变化、版本状态变化时。
* **R6 不同的行为变化可以分开提交**，但相关的审查记录更新随最后一个修复一起，不追加提交。

这套规则由 `nk-commit` 持有，`nk-work`、`nk-debug`、`nk-compound`、`nk-close`、`nk-handoff` 引用，不各写一遍。

通用的执行纪律（同样作为共享约定）：
* 未运行的测试或走查不记为通过。
* 子代理交回改动和验证证据，由主对话核对后提交。

---

## 六、技能清单

| 技能 | 用途 | 主要来源 | 阶段 |
| :-- | :-- | :-- | :-- |
| `nk-work` | 认领一个实施单元或 Issue，测试先行实现、验证、按 R1 提交 | CE `ce-work` + Matt `tdd`/`implement` | P1 |
| `nk-commit` | 提交信息 + 提交节奏规则的唯一持有者 | CE `ce-commit` | P1 |
| `nk-handoff` | 会话结束：更新 `current.md`，按 R4 提交；接手时读取 | CE `ce-handoff` + Matt `handoff` | P1 |
| `nk-brainstorm` | 澄清要做什么、范围与边界；术语即时写入 | CE `ce-brainstorm` + Matt `domain-modeling` | P2 |
| `nk-plan` | 技术方案与实施单元；plan 落在版本分支 | CE `ce-plan` | P2 |
| `nk-ideate` | 基于代码现状发散并筛选改进方向 | CE `ce-ideate` | P2 |
| `nk-close` | 版本收尾（第四章流程） | 新增 | P3 |
| `nk-compound` | 沉淀 solution（含决策类型）与术语；refresh 作为模式或独立技能，实施时定 | CE `ce-compound` / `ce-compound-refresh` + Matt ADR 门槛 | P3 |
| `nk-debug` | 先建立可快速变红的复现，再做因果排错 | CE `ce-debug` + Matt `diagnosing-bugs` | P4 |
| `nk-review` | 代码审查；结果写版本分支 `docs/reviews/` | CE `ce-code-review` + Matt `code-review` | P4 |
| `nk-simplify` | 交付后精简 | CE `ce-simplify-code` | P4 |
| `nk-wayfinder` | 超大未知目标的决策地图与探针（Issue 承载） | Matt `wayfinder` | P5 |
| `nk-to-tasks` | 可选：把 plan 拆成 Issue（并行或长期挂起时） | Matt `to-tickets` | P5 |
| `nk-wizard` | 生成引导人完成手动操作的交互脚本 | Matt `wizard` | P5 |
| `nk-wait-what` | 暂停发散，重新梳理上下文 | Matt `wait-what` | P5 |

尚未实现的技能，期间继续使用 CE 原版。

---

## 七、派生与删减原则

"重"主要贵在**常驻上下文**：技能的 `description` 始终加载，`SKILL.md` 正文在触发时加载，`references/` 只在需要时读取。因此：

1. **瘦身优先级**：`description` 与 `SKILL.md` 正文优先精简；`references/` 可以保留得宽松。
2. **每一段内容三选一**：保留 / 改写 / 删除，并写明理由。
3. **删除需要理由**：与第三章决定冲突，或依赖确定不会使用的基础设施。paper-30min 没用到不构成删除理由。
4. **拿不准就下沉**：从正文移入 `references/`，改成按需读取，而不是删掉。
5. **多 Agent 中立**：正文不依赖某个客户端专有的工具名；写成"支持子代理时……否则……"。
6. **来源备注**：每个技能在文末记一行"主要参考：CE `xxx`（版本/日期）、Matt `yyy`"。

---

## 八、实施方法

### 分工

* **实施**：在其他 Agent 中编写技能。
* **审核**：Claude Code 在两个检查点介入——技能简报评审、成稿评审；阶段完成时做一次整体评审。

### 共享约定先行（P0）

在写任何技能之前，先在 `conventions/` 下写出被多个技能引用的约定：

* `current-md.md`：`current.md` 的字段与更新时机
* `artifact-lifecycle.md`：第四章内容
* `commit-cadence.md`：第五章内容
* `concepts-vocabulary.md`：术语格式与写入时机（改写自 CE）
* `solution-schema.md`：solution 格式，含"决策"类型与三条门槛
* `decision-autonomy.md`：D6 的自决/询问分类

插件化时如何让各技能共享这些文件（引用 vs 构建时复制进各技能 `references/`），留到打包阶段决定；开发期先用相对路径引用。

### 单个技能的流程

1. **写简报** `docs/briefs/nk-xxx.md`：
   * 来源技能与版本
   * 保留 / 改写 / 删除清单（逐段，附理由）
   * 与其他 nk 技能、共享约定的接口
   * 验收场景：2~3 个真实场景，说明期望行为
2. **简报评审**（Claude）。
3. **编写** `nk-xxx/SKILL.md` 与 `references/`。
4. **成稿评审**（Claude）：对照简报与共享约定，检查冲突、遗漏、客户端相关写法、`description` 的触发准确度。
5. **实战**：在 paper-30min 的真实任务上使用，问题记入简报末尾。

简报在技能定稿后按 D3 的精神处理：有长期价值的取舍理由并入技能的来源备注，简报本身删除。

### 阶段

| 阶段 | 内容 | 完成标志 |
| :-- | :-- | :-- |
| P0 | 共享约定 | 6 份约定评审通过 |
| P1 | `nk-work`、`nk-commit`、`nk-handoff` | 在 paper-30min 完成至少一个实施单元，无多余的纯文档提交 |
| P2 | `nk-brainstorm`、`nk-plan`、`nk-ideate` | 用 nk 规划一个 v2 需求，术语在规划中写入 `CONCEPTS.md` |
| P3 | `nk-close`、`nk-compound` | 完成一次版本收尾，main 上不残留 plan/review |
| P4 | `nk-debug`、`nk-review`、`nk-simplify` | 在真实缺陷与审查中使用 |
| P5 | `nk-wayfinder`、`nk-to-tasks`、`nk-wizard`、`nk-wait-what` | 按需 |
| 打包 | 仿照 CE 结构做多 Agent 插件 | 各客户端可安装 |

---

## 九、开放问题

1. **技能正文用中文还是英文**：影响各 Agent 的触发与遵循效果，建议 P1 时对 `description` 做一次对比试验。
2. **refresh 是 `nk-compound` 的模式还是独立技能**：P3 时定。
3. **共享约定的打包方式**：打包阶段定。
4. **开发目录即加载目录**：`~/.agents/skills` 会被部分 Agent 直接加载，半成品技能会影响所有项目。需要确认哪些 Agent 会读取它；必要时开发期把技能放在子目录，定稿后再移出。
