---
name: nk-close
description: Close a delivered version before merge or release (close version, pre-merge cleanup, harvest and delete plans): transfer leftovers, harvest decisions and terms, delete delivered artifacts, rewrite docs/current.md, and make the single R4 close commit. 版本收尾、发布前清理、close version、合并前收尾、提炼删除 plan。
---

# /nk-close

> **路径解析说明：** 本文件及其 references 中引用的文件（`references/`、`../conventions/`、`../nk-commit/`）均相对于本技能所在目录解析，不在目标代码仓库中查找。`docs/plans/`、`docs/reviews/`、`docs/ideation/`、`docs/solutions/`、`docs/current.md`、`CONCEPTS.md` 指目标仓库中的文件。

版本或特性交付完成、准备合并前（或单分支模式的发版收尾节点）执行的收尾闭环：把过程工件中的长期价值提炼进知识库，清理已交付工件，让仓库以干净状态进入下一个版本。本技能是 [`../conventions/artifact-lifecycle.md`](../conventions/artifact-lifecycle.md) 第五章"版本收尾六步法"的可执行展开。

**完成标志：** 遗留项与用户决策点全部处置完毕，有价值内容已提炼，已交付的 plan/审查记录已删除，`docs/current.md` 覆写为交付后状态，以上改动合为一次 R4 收尾提交入库。
**工作原则：** 提炼先于删除；只删已交付完成的工件；收尾提交只含本技能涉及的文件。

---

## 执行步骤

### 0. 前置检查
确认收尾前提成立；前提不成立时列出缺口并停下问用户，不放行：

1. **单元交付核对**：对当前 plan 的每个实施单元，用 `git log --oneline --grep "(U<编号>)"` 确认存在带单元编号的验证提交（进度以提交为准，见 [`../conventions/commit-cadence.md`](../conventions/commit-cadence.md) R1）。
2. **工作区清点**：`git status` 中不应有未交代的半成品；有则先处置——能收尾的随最后单元提交，不能收尾的如实登记进 `docs/current.md` 的工作区字段，并向用户说明。
3. **验证证据核对**：交付声明必须由实际运行过的测试或走查支撑；未运行的记为未验证而非通过（纪律见 commit-cadence 第三节）。证据缺失时警告用户，由用户决定是否继续收尾。

### 1. 遗留项转移与甄别
* 检查 `docs/reviews/` 中的遗留条目（该目录由 `nk-review` 产生，此技能尚未提供；目录不存在则跳过并向用户说明），以及 `docs/plans/` 各 plan 中未完成的待办。
* **未完成或推迟到后续版本的 plan 不随本技能删除**，逐项转入下方"用户决策点"流程；审查记录的遗留项转为 Issue（无 GitHub 远端时记入 `docs/backlog.md`，降级规则见生命周期矩阵）。

### 2. 价值提炼 (Harvest)
从即将删除的 plan 与审查记录中提炼有长期价值的内容。主要提炼对象是 plan 中"为什么这么做"的决策理由；找什么、怎么判断、怎么写的细则见 [`references/harvest.md`](references/harvest.md)：

* 重大架构选型与踩坑因果：先过 [`../conventions/solution-schema.md`](../conventions/solution-schema.md) 的双轨准入门槛，合格才写入 `docs/solutions/`，平庸内容不建档；
* 新稳定领域术语：按 [`../conventions/concepts-vocabulary.md`](../conventions/concepts-vocabulary.md) 写入根目录 `CONCEPTS.md`。

### 3. 清理已交付工件
确认第 1 步无遗留、第 2 步提炼完成后，用 `git rm` 删除本次**已交付完成**的 plan 与审查记录。只删已交付的：推迟的已在第 1 步转走，未消费的发想记录按用户决策点处置，均不在此删除。完整设计演进由 Git 历史保留。

### 4. 更新 `docs/current.md`
版本收尾属于"版本/里程碑状态跃迁"（R5 的合法更新时机）。按 [`../conventions/current-md.md`](../conventions/current-md.md) 将 `docs/current.md` 覆写为交付后的真实状态：已具备能力、验证结果（含未验证项）、阻断与 `[待确认]` 项、下一步指向（Issue 编号或后续版本入口）。

### 5. 单个收尾提交（R4）
读取 [`../nk-commit/SKILL.md`](../nk-commit/SKILL.md) 并遵循其规则：

* 本次属于 [`../conventions/commit-cadence.md`](../conventions/commit-cadence.md) R4 规定的"版本收尾点"，允许且只发起**一次**纯文档收尾提交；
* **显式暂存并限定路径**：只含本技能涉及的文件——`docs/solutions/` 新增、`CONCEPTS.md`、`docs/current.md`、被 `git rm` 的 plan/审查记录、可能新增的 `docs/backlog.md` 或 `docs/releases/`。不使用 `git add -A`，防止把工作区半成品带入提交；
* 提交信息风格遵循项目既有惯例，不写死格式。

### 6. 发布摘要（可选）
项目走 PR 流程且用户要求时，生成精炼的 PR 摘要，或在 `docs/releases/` 写一份发布说明并随第 5 步一同提交；用户没要求则跳过。

---

## 用户决策点

收尾时对以下两类产物**逐项询问用户**，遵循 [`../conventions/decision-autonomy.md`](../conventions/decision-autonomy.md) 第三节的批量提问规则：选项驱动、标注 `(Recommended)`、互不依赖的合并为一轮、每轮最多 3 个。

1. **未被消费的发想记录**（`docs/ideation/` 中方向未进入任何 plan 的）：
   * 选项：保留 / 转为 Issue / 删除；
   * 推荐项按内容质量判断并说明理由——方向仍有辨识度且日后可能复用则保留，方向明确且值得排期则转 Issue，已被取代或没有信息量则删除。
2. **推迟的 plan**：
   * 选项：转为 GitHub Issue（Recommended，可追踪）/ 移至后续版本分支 / 其他。

无人值守模式下按兜底规则推进：采用推荐默认（推迟 plan → 转 Issue；未消费发想记录 → 保留），并在 `docs/current.md` 阻断/缺口章节逐项登记 `[待确认]`，供人类事后审查。无 GitHub 远端时，Issue 一律降级为 `docs/backlog.md` 条目。

---

> 主要参考：NexusKit 共享约定 [`../conventions/artifact-lifecycle.md`](../conventions/artifact-lifecycle.md)（本技能为其第五章的可执行展开）
>
> 关键设计决定：
> * 未消费发想记录与推迟 plan 逐项询问用户、每轮最多 3 个——用户 2026-09-25 拍板；无人值守时采用推荐默认并在 `docs/current.md` 登记 `[待确认]`。
> * 在六步法前增加第 0 步前置检查（单元提交核对、工作区清点、验证证据核对）：证据缺失时警告用户而非放行，依据 commit-cadence 第三节的通用纪律补入。
> * 提炼的判断细则下沉到 `references/harvest.md`，SKILL.md 保持聚焦"怎么做"。
> * `docs/reviews/` 目录不存在时跳过并说明：`nk-review` 是规划中的技能，尚未提供。
> * 收尾提交显式限定本技能涉及的文件路径：收尾时工作区可能仍有后续版本的半成品，防止混入提交。
> * 提交信息风格遵循项目惯例而不写死格式：与 nk-commit、nk-handoff 的口径一致。
