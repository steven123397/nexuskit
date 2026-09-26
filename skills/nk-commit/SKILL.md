---
name: nk-commit
description: Create commits that follow NexusKit commit cadence (R1–R6): one verified change per commit, docs ride with code, docs-only commits only at session handoff or version close. 按提交节奏规则提交代码；提交、commit、amend。
---

# /nk-commit

> **路径解析说明：** 本文件中引用的参考文件（如 `../conventions/`）均相对于本技能所在目录解析，不在目标代码仓库中查找。

根据 NexusKit 提交节奏规则（R1–R6）创建规范的本地 Git 提交。既可单独调用，也由 `nk-work`、`nk-handoff` 内部读取遵循。

**完成标志：** 每一个经过验证的交付变化以显式文件列表和阐述成果的提交说明入库，工作区清除已提交改动。  
**停止条件：** 工作区干净（无可提交内容），或当前变动仅属于中途纯状态记录（R2，留待随下次交付提交入库）。

---

## 一、收集现场 (Context)

依次单独执行以下命令（每条命令独立调用，不使用 `&&`、`;` 或管道符拼接，确保跨平台与 PowerShell 兼容）：

| 命令 | 目的 | 非零或空值含义 |
| :-- | :-- | :-- |
| `git status` | 检查工作区与暂存区状态 | 非 git 仓库则停止 |
| `git diff HEAD` | 查看未提交的差异 | 无初始提交的历史则为空 |
| `git branch --show-current` | 查看当前分支 | 空表示 detached HEAD |
| `git log --oneline -10` | 获取近期提交信息风格 | 新仓库无提交历史 |
| `git rev-parse --abbrev-ref @{u}` | 检查是否存在跟踪的上游分支 | 非零表示未设置 upstream 分支 |

---

## 二、执行流程 (Workflow)

### 0. 现场收集与无改动检查
运行上述收集命令。若 `git status` 显示工作区完全干净（无 modified、staged 或 untracked 文件），报告无待提交内容并结束。

### 1. 判定提交类型 (Cadence Evaluation)
**不按文件扩展名（如 `.md`）判断**，而是根据本次改动是否构成“一个经过验证的交付变化”与“纯状态记录”来判定动作：

1. **经过验证的交付变化（适用 R1 普通提交）**：
   * 只要改动本身是本次任务/实施单元的交付成果，**不论文件类型是源码、测试、配置文件、规则还是文档（如 `SKILL.md`、架构规范）**，均属于 **R1 普通提交**。
   * 配套的说明文档变更（如 `CONCEPTS.md` 术语更新、Plan 范围调整）随交付成果同行提交。
2. **仅含状态记录的改动（适用 R2 / R3 / R4）**：
   * 指仅修改了过程状态文件（如 `docs/current.md`、Plan 的变更记录、审查记录 `docs/reviews/` 中的已修复标记），而没有任何实质交付物的变动：
     * **补记判定（R3 amend）**：若上一个提交属于本会话产生，且尚未推送到远端（`git log @{u}..HEAD` 包含该提交，或当前分支无 upstream），本次改动仅为补充该提交对应的状态记录 -> 显式暂存这些状态文件后执行 **`git commit --amend --no-edit -- <路径...>`** 并入上一个提交。amend 同样必须限定路径，否则工作区里的半成品或外来脏文件可能被一并带入。
     * **交接与收尾判定（R4 纯文档提交）**：若当前明确处于会话结束交接（`/nk-handoff`）或版本收尾（`/nk-close`） -> 允许创建**单次纯文档提交**。
     * **规划会话判定（R4 纯文档提交）**：若当前处于纯规划会话（`/nk-brainstorm` / `/nk-plan`）收尾，产出的 Plan 与 `CONCEPTS.md` 算作该会话交接提交 -> 允许创建**纯文档提交**。
     * **其他中途状态改动（R2 暂不提交）**：不属于上述情况的纯状态变动（如中途微调 `current.md`），**终止提交**，改动保留在工作区，告知用户该状态记录将随下一个交付提交一并入库。

### 2. 分支策略 (Branch)
遵循项目既有策略（见 [`../conventions/artifact-lifecycle.md`](../conventions/artifact-lifecycle.md)）：
* 检查项目工作流文档（由 `AGENTS.md` 索引，如 `docs/release-workflow.md`）。若项目明确规定了分支模式，遵照执行。
* 若项目未作规定，**留在当前所在分支工作，不自动创建额外特性分支**（在默认分支/main 上提交时用一句话说明即可）。

### 3. 确定提交风格 (Convention)
按以下优先级确定提交信息格式：
`项目自定约定 -> 近期 Git Log 风格 -> Conventional Commits (type(scope): description)`

* 使用 Conventional Commits 时：修复或补齐缺陷用 `fix:`，新增能力用 `feat:`，文档用 `docs:`，重构用 `refactor:`。
* **实施单元后缀**：当该提交对应 Plan 中的某个具体实施单元编号时，在主题行末尾追加 `(U-ID)`，例如：`feat(parser): add token stream iterator (U3)`。

### 4. 逻辑拆分 (Logical Commits)
* 若工作区的改动明显属于多个相互独立的修复或功能变更，按文件粒度拆分成 2~3 个独立提交（R6），不使用 `git add -p`。
* 无法明确区分或存在耦合时，合并为一个提交。审查记录更新随最后一个修复一同入库。

### 5. 编写提交信息 (Message & Evidence)
* **主题行**：说明取得的成果（现在能做什么、修好了什么），不罗列修改的文件名。有 U-ID 时末尾附带 `(U-ID)`。
* **正文**：
  * 若设计动机或关键取舍不够直观，用 1~2 句话简述原因。
  * **验证证据**：用 1~3 行记录运行过的验证命令、实际结果与未验证项。  
    例如：
    ```text
    Verified: cargo test parser (42/42 passed).
    Unverified: Large file stress test (>100MB) not run.
    ```

### 6. 显式暂存与限定提交 (Stage & Commit)
* **显式暂存**：只暂存明确属于本次提交的文件列表（`git add path1 path2`），不使用 `git add -A` 或 `git add .`。
* **隔离外来脏文件**：跳过非本单元所属的外来脏文件。当 `/nk-commit` 被单独调用时，通过读取 `docs/current.md` 的“工作区未提交改动”字段区分本会话半成品与外来脏文件；若仍无法判断归属，向用户询问确认。
* **文件传递提交信息（防转义）**：将完整的提交说明写入仓库外的临时文件，然后执行带路径限定的提交命令：
  ```bash
  git commit -F <temp-message-file> -- path1 path2 ...
  ```
  *(注：`git commit` 结尾必须明确列出文件路径，防止将暂存区里其他无关文件一并带入。)*

### 7. 确认结果 (Confirm)
运行 `git status` 确认工作区状态，报告生成的 Commit 哈希与主题行。
