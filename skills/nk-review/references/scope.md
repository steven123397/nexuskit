# 范围判定（审什么）

第 1 步读取本文件。目标是解析出**被审 diff**：基线 ref、文件清单、带上下文的 diff 文本，以及供编队使用的范围信号。解析不出来就早停，不带着半个 diff 进入编队。

## 一、四种审查对象

按用户输入分流；命令尽量合并执行以减少打断。

### 1. 空参数（默认：版本层面审查）

审当前分支相对基线分支的全部改动（已提交 + 已暂存 + 未暂存一起）：

```bash
BASE=$(git merge-base HEAD <base-ref>)
echo "BASE:$BASE" && echo "FILES:" && git diff --name-only $BASE && echo "DIFF:" && git diff -U10 $BASE && echo "UNTRACKED:" && git ls-files --others --exclude-standard
```

- `<base-ref>` 的确定顺序：目标项目工作流文档规定的基线分支 > 当前分支的 upstream > 远端默认分支（`origin/main` / `origin/master`）> 本地 `main` / `master`。
- `git diff $BASE`（不带 `..HEAD`）对 merge-base 与工作树求 diff，三种状态的改动都覆盖到。
- 无法解析出基线时停下说明，不要把范围悄悄退化成"只看未提交改动"——那会漏掉分支上已提交的工作。按 [`../../conventions/decision-autonomy.md`](../../conventions/decision-autonomy.md) 询问用户审查对象；无人值守时以"未提交改动"为兜底并在覆盖说明中注明。

### 2. 指定基线 ref

用户给了 commit、分支、tag（"review since X"）：先 `git rev-parse <ref>` 确认可解析，再 `BASE=$(git merge-base HEAD <ref>) || BASE=<ref>`，产出同上。**diff 为空就在这里失败**，不要进入编队后才发现无事可审。同时用 `git log <ref>..HEAD --oneline` 记录提交清单，供意图摘要使用。

### 3. 指定文件或路径

用户点名文件/目录：diff 限定到这些路径（`git diff -U10 $BASE -- <paths>`）；其中未跟踪的新文件按全文阅读。审查结论只对这些路径负责，在覆盖说明中写明"范围为用户指定路径"。

### 4. 未提交改动

用户明确只看手头改动：`git diff -U10 HEAD`（含暂存区），加上 `git ls-files --others --exclude-standard` 中已被暂存的文件。

### 附：PR 编号或 URL（可选路径）

项目走 PR 流程时，PR 编号/URL 也可作为审查对象：用 `gh pr view <n> --json title,body,baseRefName,headRefName,files,reviews,comments` 与 `gh pr diff <n>` 只读取数，**不切换分支、不 checkout**。当前分支与 PR head 一致（同名、非 fork、head 提交是 HEAD 祖先）时按本地 diff 审；不一致时以 PR 远端 diff 为准，且 reviewer 不得用工作区文件内容代替被审版本（用 `git show <ref>:<path>` 或只看 diff hunk）。已关闭/已合并的 PR 不审；明显的琐碎自动 PR（锁文件、版本号 chore）向用户确认后跳过。

## 二、未跟踪文件

`UNTRACKED:` 非空时：未暂存的未跟踪文件在范围外，列入覆盖说明后继续，不停下也不追问。

## 三、范围信号（路径分类规则）

以下规则转写自原辅助脚本的确定性逻辑，由 Agent 按路径模式直接判定，供第 3 步编队使用：

**测试文件识别**（这些路径的改动不计入"可执行改动行数"）：`tests?/`、`spec/`、`__tests__/` 目录；`*._-test / *._-spec / *.test.* / *.spec.*` 后缀；`test_*.py`、`conftest.py`；Java/C#/Scala/Swift/Kotlin 的 `*Test.*` / `*Tests.*` / `*Spec.*` 类文件（大小写敏感，`Contest.java` 这类不算）。

**路径信号 → 编队提示**（信号是提示，不是自动派发决定）：

| 信号 | 路径模式（不区分大小写） | 提示的 persona |
| :-- | :-- | :-- |
| 迁移 | `db/migrate/`、`schema.rb/sql`、`/migrations?/`、alembic/flyway/liquibase | data-migration（+ 风险高时 deployment-verification） |
| 前端 | `.tsx/.jsx/.vue/.svelte/.css/.scss`、`/components?/`、stimulus/turbo | julik-frontend-races（有异步 UI 行为变化时） |
| API | `/routes?/`、`/controllers?/`、`/api/`、`/serializers?/`、`.proto`、openapi | api-contract |
| iOS | `.swift`、`.pbxproj`、`.entitlements`、`.xcconfig` | swift-ios |
| Agent 界面 | `/skills?/`、`/agents?/`、`/prompts?/`、`/tools?/`、`SKILL.md`、`AGENTS.md` 等指令文件 | agent-native、project-standards |

**静默放行守卫（无论改动多小都触发 adversarial）**：CI/CD 与门禁类路径——`.github/workflows/`、`.gitlab-ci.yml`、`.circleci/`、`Jenkinsfile`、`.buildkite/` 等。这类改动本身是"验证机制"，风险不在爆炸半径而在保真度：它可能在真实产物已坏时照样放行。

**规模阈值**：可执行非测试改动行数 ≥ 200 时 maintainability 必选，且不缩减编队；低于此值时由后果判断，行数本身不构成缩减理由。

## 四、规范文件映射（供 project-standards）

枚举被审版本中的 `CODING_STANDARDS.md`、`CLAUDE.md`、`AGENTS.md`（任意深度），保留其目录是被改文件祖先的文件：根级文件管整个仓库，`skills/AGENTS.md` 只管 `skills/` 之下。

- `CODING_STANDARDS.md` 是指定的准则来源：一个被改文件有它管辖时，不再用指令类文件（`CLAUDE.md`/`AGENTS.md`）评它；任何文件不同时被两类准则评判。
- 没有准则文件管辖某些被改文件是完整结果，不是缺口；搜索失败或范围不确定要如实记录为不确定，不记为"无准则"。
- 映射结果（哪个准则文件管哪些被改文件）传给 project-standards persona；空结果则跳过该 persona 并在覆盖说明中注明。
