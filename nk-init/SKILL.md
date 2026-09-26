---
name: nk-init
description: Initialize a repository for NexusKit on first adoption — probe existing state, confirm with the user, then idempotently set up AGENTS.md guidance, docs/current.md and the backlog fallback. Use when asked to initialize, set up, or bootstrap a repo for NexusKit. 初始化仓库、首次启用 NexusKit、setup、bootstrap。
disable-model-invocation: true
---

# /nk-init

> **路径解析说明：** 本文件中引用的参考文件（如 `../conventions/`、`../nk-commit/`）均相对于本技能所在目录解析；`docs/`、`AGENTS.md`、`CONCEPTS.md` 等产物路径均指**目标代码仓库**中的路径。

在目标仓库首次启用 NexusKit 时运行一次，把仓库变成"体系就绪"状态：知识入口在全局指令文件中可见、会话入口 `docs/current.md` 就位、待办去向明确。全程幂等，可重复运行；已存在的内容一律跳过并向用户说明，不覆盖既有内容。

**完成标志：** 全局指令文件具备知识入口指引、`docs/current.md` 就位、待办去向确定，产物按提交节奏入库，用户得到收尾指引。
**工作原则：** 先探测再提问、幂等不覆盖、只建必要产物、不动项目代码。

---

## 执行步骤

### 1. 探测现状 (Explore)
先读仓库，不凭空发问：
- `git remote -v` 与 `gh --version`：有无 GitHub 远端、`gh` 是否可用，两者共同决定待办去向（GitHub Issue 或降级为 `docs/backlog.md`，见 [`../conventions/issue-writing.md`](../conventions/issue-writing.md)）。
- 根目录的 `AGENTS.md`（或 `CLAUDE.md` 等等价全局指令文件）：是否存在；若存在，是否已有指向 `docs/current.md`、`docs/solutions/`、`CONCEPTS.md` 的指引行。
- 已有产物盘点：`docs/current.md`、`CONCEPTS.md`、`docs/solutions/`、`docs/plans/`、`docs/reviews/`、`docs/ideation/`、`docs/backlog.md` 各自是否存在。

### 2. 展示发现并确认 (Confirm)
向用户汇总已有与缺失，然后按 [`../conventions/decision-autonomy.md`](../conventions/decision-autonomy.md) 批量提问（互不依赖的问题合并一轮，单轮最多 3 个，选项带推荐）。典型问题：
- 有 GitHub 远端且 `gh` 可用时：是否启用 GitHub Issue 作为待办承载（推荐：是）。
- 项目是否已有自己的流程文档需要在全局指令文件中索引（收集事实，可开放式问）。

探测已能确定答案的不提问（如无远端时直接采用 `docs/backlog.md` 降级，并在展示中说明）。

### 3. 写入产物 (Write)
逐项检查，幂等写入；每跳过一个已存在项，向用户说明一次。

- **全局指令文件**：`AGENTS.md` 不存在则新建最小骨架（项目名占位 + 知识入口指引）；已存在（或仅有 `CLAUDE.md` 等等价文件）则只追加缺失的指引行，不改动其他内容，也不新建第二份等价文件。指引指向 `docs/current.md`、`docs/solutions/`、`CONCEPTS.md`，用描述性语气（如"`docs/solutions/` 收录本项目已验证的经验与决策，在已记录领域实施或排障时相关"），不写命令句。依据：[`../conventions/artifact-lifecycle.md`](../conventions/artifact-lifecycle.md) 第二章。
- **`docs/current.md`**：按 [`../conventions/current-md.md`](../conventions/current-md.md) 模板创建，填"刚启用 NexusKit"的初始状态——所在分支与 HEAD、已具备能力用一句话概述项目现状、阻断写"无"、下一步写从描述第一个任务开始。
- **不创建 `CONCEPTS.md`**：由第一个合格词条创建（见 [`../conventions/concepts-vocabulary.md`](../conventions/concepts-vocabulary.md)）；**不创建空目录**：`docs/solutions/`、`docs/plans/` 等在首个条目产生时再建（git 不跟踪空目录）。
- **无远端降级**：创建 `docs/backlog.md`，带格式说明头部——"本文件是无 GitHub 远端时的待办降级承载，每条一个条目，格式遵循 NexusKit 的 issue-writing 约定（Category / Current behavior / Desired behavior / Acceptance criteria / Out of scope / Source）"——不预填条目。

### 4. 提交入库 (Commit)
以上产物是本次初始化的交付物。读取 [`../nk-commit/SKILL.md`](../nk-commit/SKILL.md)，按提交节奏规则显式暂存这些文件并发起一次初始化提交，提交信息风格遵循项目既有惯例。

### 5. 收尾指引 (Done)
告诉用户体系已就绪，列出本次创建、补充与跳过的产物清单，说明之后可手动编辑这些文件。建议从 `/ask-ljq`（场景路由）或直接描述任务开始。

---

## 边界

- 不迁移既有产物（从其他体系迁入历史文档是单独的迁移方案，不在本技能范围）。
- 不修改项目代码，不创建本清单之外的文件或目录。
- 重复运行时，探测步骤会发现一切就绪，仅报告现状，不产生任何改动。
