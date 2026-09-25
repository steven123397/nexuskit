---
name: nk-commit
description: Create commits that follow NexusKit commit cadence (R1–R6): one verified change per commit, docs ride with code, docs-only commits only at session handoff or version close. 按提交节奏规则提交代码；提交、commit、amend。
---

# /nk-commit

根据 NexusKit 提交节奏规则（R1–R6）创建规范的本地 Git 提交。既可单独调用，也由 `nk-work`、`nk-handoff` 内部复用。

**完成标志：** 每一个经过验证的变化以显式文件列表和阐述成果的提交说明入库，工作区清除已提交改动。  
**停止条件：** 工作区干净（无可提交内容），或当前变动属于 R2 状态改动（留待随下次代码提交）。

---

## 一、收集现场 (Context)

依次单独执行以下命令（每条命令独立调用，不使用 `&&`、`;` 或管道符拼接，确保跨平台与 PowerShell 兼容）：

| 命令 | 目的 | 非零或空值含义 |
| :-- | :-- | :-- |
| `git status` | 检查工作区与暂存区状态 | 非 git 仓库则停止 |
| `git diff HEAD` | 查看未提交的代码差异 | 无初始提交的历史则为空 |
| `git branch --show-current` | 查看当前分支 | 空表示 detached HEAD |
| `git log --oneline -10` | 获取近期提交信息风格 | 新仓库无提交历史 |
| `git rev-parse --abbrev-ref @{u}` | 检查是否存在跟踪的上游分支 | 非零表示未设置 upstream 分支 |

---

## 二、执行流程 (Workflow)

### 0. 现场收集与无改动检查
运行上述收集命令。若 `git status` 显示工作区完全干净（无 modified、staged 或 untracked 文件），报告无待提交内容并结束。

### 1. 判定提交类型 (Cadence Evaluation)
检查本次涉及变更的文件类型，按 R1–R6 判定合法的提交动作：

1. **含代码或测试文件**：
   * 属于**普通提交（R1）**。确保改动已经过验证，代码、测试与配套文档（如 `CONCEPTS.md` 术语更新、Plan 调整）同行提交。
2. **仅含文档或状态文件**（如仅修改了 `docs/`、`CONCEPTS.md`、Markdown 文件）：
   * **补记判定（R3 amend）**：若上一个提交属于本会话产生，且尚未推送到远端（`git log @{u}..HEAD` 包含该提交，或当前分支无 upstream），本次改动仅为补充该提交对应的文档/状态 -> 执行 **`git commit --amend`** 并入上一个提交。
   * **交接点判定（R4 纯文档提交）**：若当前明确处于会话结束交接（`/nk-handoff`）或版本收尾（`/nk-close`） -> 允许创建**单次纯文档提交**。
   * **规划会话判定（R4 纯文档提交）**：若当前处于纯规划会话（`/nk-brainstorm` / `/nk-plan`）收尾，产出的 Plan 与 `CONCEPTS.md` 算作该会话交接提交 -> 允许创建**纯文档提交**。
   * **其他中途状态改动（R2 暂不提交）**：不属于上述情况的纯状态变动（如中途微调 current.md、笔记修改），**终止提交**，改动保留在工作区，提示用户该改动将随下一个代码提交一并入库。

### 2. 分支策略 (Branch)
遵循项目既有策略：
* 检查项目工作流文档（由 `AGENTS.md` 索引，如 `docs/release-workflow.md`）。若项目明确规定了分支模式（如 `feat/*`、版本分支），遵照执行。
* 若项目未作硬性规定，**保留在当前所在分支工作，不自动创建额外特性分支**（个人项目直接在默认分支/main 上提交属正常实践；在默认分支上提交时在一句话中说明即可）。

### 3. 确定提交风格 (Convention)
按以下优先级确定提交信息格式：
`项目自定约定 -> 近期 Git Log 风格 -> Conventional Commits (type(scope): description)`

* 使用 Conventional Commits 时：修复或补齐缺陷用 `fix:`，新增能力用 `feat:`，文档用 `docs:`，重构用 `refactor:`。
* **实施单元后缀**：当该提交对应 Plan 中的某个具体实施单元编号时，必须在主题行末尾追加带有括号的编号，例如：`feat(parser): add token stream iterator (U3)`。

### 4. 逻辑拆分 (Logical Commits)
* 若工作区的改动明显属于多个相互独立的修复或功能变更，按文件粒度拆分成 2~3 个独立提交（R6），不使用交互式 `git add -p`。
* 无法明确区分或存在耦合时，统一合并为一个提交。审查记录更新随最后一个修复一同入库。

### 5. 编写提交信息 (Message & Evidence)
* **主题行**：祈使句，说明取得的成果（现在能做什么、修好了什么），不罗列修改的文件名。末尾附带 `(U-ID)`（若适用）。
* **正文（可选，但推荐）**：
  * 若设计动机或关键取舍不够直观，用 1~2 句话简述原因。
  * **验证证据（K10）**：在正文中用 1~3 行记录运行过的验证命令及实际输出结论、未验证项。  
    例如：
    ```text
    Verified: cargo test parser (42/42 passed).
    Unverified: Large file stress test (>100MB) not run.
    ```

### 6. 显式暂存与限定提交 (Stage & Commit)
* **显式暂存**：只暂存明确属于本次提交的文件列表（`git add path1 path2`），严禁使用 `git add -A` 或 `git add .`。
* **隔离外来脏文件（K8）**：跳过未在本次任务范围或非本会话半成品的文件。
* **文件传递提交信息（防转义）**：将完整的提交说明（含主题、换行、正文证据）写入仓库外的临时文件（如操作系统的临时目录），然后执行带路径限定的提交命令：
  ```bash
  git commit -F <temp-message-file> -- path1 path2 ...
  ```
  *(注：`git commit` 结尾必须明确指定提交的路径列表，防止意外带入其他已暂存内容。)*

### 7. 确认结果 (Confirm)
运行 `git status` 确认工作区状态，向用户输出新生成的 Commit 哈希与主题行。

---

> 主要参考：CE `ce-commit` (2026-09)、NexusKit 共享约定 [`conventions/commit-cadence.md`](../conventions/commit-cadence.md)
