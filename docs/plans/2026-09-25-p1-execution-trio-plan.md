# P1 实施方案：执行三件套（nk-work / nk-commit / nk-handoff）

> **状态**：待评审
> **日期**：2026-09-25
> **依据**：[RFC v2.0](../ideation/nexuskit-framework-ideation.md)、[`conventions/`](../../conventions/)、P1 简报评审意见
> **生命周期**：本 plan 在 P1 收尾时提炼后删除（见 `conventions/artifact-lifecycle.md`）。本方案第三章的逐技能规格即 P1 的技能简报，不再单独写 `docs/briefs/`。

---

## 一、目标与范围

**目标**：交付三个技能，打通"会话开始 → 实现并验证一个单元 → 按节奏提交 → 会话交接"的闭环。paper-30min 实战验收在全部阶段完成后统一进行（见第五章）。

**范围内**
* `nk-commit/`、`nk-work/`、`nk-handoff/` 三个技能目录（`SKILL.md` + `references/`）
* 因本方案决定而需要的共享约定修订（U0）

**范围外**
* 代码审查、审查发现的修复与归档 → P4 `nk-review`
* 开 PR、版本收尾、Issue 批量归档 → P3 `nk-close`
* 交付后精简 → P4 `nk-simplify`（P1 期间 `nk-work` 不主动调用任何精简技能）
* 插件打包

**参考源路径**
* CE：`C:/Users/29617/.gemini/config/plugins/compound-engineering/skills/`（下文简写 `CE/`）
* Matt：`C:/Users/29617/.agents/backups/mattpocock-skills-20260824-193425/skills/`（下文简写 `Matt/`）

---

## 二、关键决策

| # | 决策 | 理由 |
| :-- | :-- | :-- |
| K1 | **去掉 CE 的调度脚本与跨模型执行**：`scripts/` 全部、`execution-engines.md`、`cross-model-execution.md`、`implementation-result-schema.json` 不移植 | 约 8300 行 Python/Shell，解决的是跨模型、并行隔离执行；我们的模式是一个会话串行推进、主对话提交，不需要这层编排。维护与 Windows 兼容成本高 |
| K2 | **默认一个会话做一个单元，可以顺延** | 上下文仍宽裕、下一单元紧密相关时可继续做；每个单元单独提交（R1），交接只在会话结束时做一次。避免小单元被迫逐个交接，放大 R4 纯文档提交。token 预算只是理念（D10） |
| K3 | **测试 seam 由 Agent 自选** | 改写 Matt `tdd` 的"先与用户确认 seams"。测试结构属于 `decision-autonomy.md` 的自主区；选定的 seam 写进提交说明。只有 seam 选择会改变对外接口时才按询问区提问 |
| K4 | **进度以提交为准，不为记进度改 plan** | 采纳 CE 做法（`ce-work/references/workspace-setup.md`："Do not edit the plan body during execution"）：单元完成的标志是带 `(U-ID)` 的提交，可用 `git log --grep "(U3)"` 查询。plan 只在范围或做法变化时修改（附变更记录）。这样 plan 的每次改动都是有意义的决策变化，还去掉了一类状态改动。**需要修订 P0 约定，见 U0** |
| K5 | **分支策略交给项目** | 项目工作流文档规定了分支约定就照做；没有规定时留在当前分支、不自动建分支，在默认分支上工作时用一句话说明。改写 CE `ce-work` 与 `ce-commit` 的"在默认分支上自动建 feature 分支"，因为个人项目常直接在 main 上工作，本仓库即如此 |
| K6 | **会话开始由 `nk-work` 负责，`nk-handoff` 只负责结束** | 删除 CE `ce-handoff` 的 resume 模式。`current.md` 通过 `AGENTS.md` 指引，任何会话都会先读到它；需要"开工前核对现场"的只有执行类工作，所以放在 `nk-work` 第 0 步 |
| K7 | **接手规则是"一致则继续，不一致才停"** | 不移植 CE resume 的强制 Stop-and-Ask。只在以下情况停下：分支与 `current.md` 不符；工作区实际改动与"未提交改动"字段不符；存在影响本单元的 `[待确认]` 项 |
| K8 | **工作区脏文件分两类** | `current.md` "未提交改动"字段登记的半成品由本会话接管；其余脏文件视为他人或用户的改动，永不暂存；本单元必须改动这类文件时，在第一次提交前统一问一次。沿用 CE 的 pre-work scope，并与交接机制对接 |
| K9 | **`nk-work` 不设代码审查关卡** | CE `ce-work` 强制每次运行都有审查凭据。我们的审查发生在版本层面（合并或发布前，见 paper-30min `release-workflow.md`），由 P4 `nk-review` 负责 |
| K10 | **验证证据写进提交说明正文** | 每个单元提交的正文用 1~3 行写明运行的验证命令与结果、未验证项。证据随提交永久保存，不需要额外文档。交接时 `current.md` 只做汇总 |
| K11 | **提交信息风格跟随项目** | 按"项目约定 → 近期提交风格 → conventional commits"的顺序确定，任何技能都不写死提交格式。有 U-ID 时在末尾追加 `(U3)` |
| K12 | **技能正文用中文，`description` 中英双语关键词** | 与使用习惯一致；`description` 决定能否被自动触发，双语关键词兼顾各客户端。在 A6 验收中对比触发效果，必要时调整 |

---

## 三、逐技能规格

### 3.1 `nk-commit`

**职责**：提交信息与提交节奏规则的唯一持有者。既可单独调用，也由 `nk-work`、`nk-handoff` 在内部按其规则执行。

**description 草案**：
> Create commits that follow NexusKit commit cadence (R1–R6): one verified change per commit, docs ride with code, docs-only commits only at session handoff or version close. 按提交节奏规则提交代码；提交、commit、amend。

**流程**
1. **收集现场**：每条命令单独执行，不用 `&&`、管道等拼接，兼容 PowerShell（沿用 CE）。
   * `git status`、`git diff HEAD`、`git branch --show-current`、`git log --oneline -10`
   * 上游是否存在：`git rev-parse --abbrev-ref @{u}`
2. **无改动则停止**。
3. **判定提交类型**，这是新增的核心步骤：
   * 含代码或测试 → 普通提交（R1）
   * 只有文档或状态改动：
     * 属于上一个**未推送**提交的补记 → amend（R3）
     * 当前处于会话交接或版本收尾 → 纯文档提交（R4）
     * 规划会话结束 → 纯文档提交（R4）
     * 其他情况 → **不提交**，留在工作区，并告知用户改动会随下一个代码提交一起入库（R2）
4. **分支**：按 K5。
5. **确定提交风格**：按 K11。
6. **拆分逻辑提交**：改动明显属于不同行为变化时拆成 2~3 个（R6），按文件粒度拆，不用 `git add -p`；拿不准就合成一个。
7. **写提交信息**：
   * 主题说明结果（现在能做什么、修好了什么），不罗列文件；有 U-ID 时追加 `(U3)`
   * 正文：动机或取舍不明显时写一两句；按 K10 写验证证据
8. **暂存并提交**：
   * 只暂存明确列出的文件，不用 `git add -A` 或 `git add .`
   * 跳过 K8 所说的外来脏文件
   * 提交信息先写入仓库外的临时文件，再执行 `git commit -F <文件> -- <路径...>`
   * 提交命令末尾必须带路径列表，避免把索引里别人已暂存的内容一起带进去
9. **确认**：运行 `git status`，报告提交哈希与主题。

**references**
* `conventions/commit-cadence.md`：开发期用相对路径 `../conventions/commit-cadence.md` 引用

**来源取舍**

| 来源 | 处理 | 理由 |
| :-- | :-- | :-- |
| `CE/ce-commit/SKILL.md` Context 表、单独执行命令 | 保留 | Windows/PowerShell 兼容，实测有效 |
| 同上 Workflow 1、3、4、5、6、7 | 保留 | 显式暂存、`-F` 临时文件、路径限定提交、U-ID 后缀都与约定一致 |
| 同上 Workflow 2"Branch first" | 改写 | 按 K5 |
| 同上 `exclude:<paths>` 参数 | 改写 | 改为 K8 的脏文件分类，不再依赖调用方传参 |
| 提交类型判定（第 3 步） | 新增 | 把 R1–R6 变成可执行的判定流程 |
| 验证证据写进正文 | 新增 | 按 K10 |

---

### 3.2 `nk-work`

**职责**：接手现场，实现并验证一个或多个单元，每个单元按 `nk-commit` 规则提交。

**description 草案**：
> Execute one implementation unit from a plan, an Issue, or a clear request: orient from docs/current.md, test-first implementation, verification evidence, cadence-compliant commits. Use ce-debug/nk-debug for open-ended bugs. 执行实施单元、按计划实现、测试先行。

**流程（`SKILL.md` 正文保持在 80 行左右，细节放进 references）**

0. **定位**（新增）
   * 读 `docs/current.md`（如果存在）和项目工作流文档（从 `AGENTS.md` 找）。
   * 核对当前分支；运行 `git status --short --untracked-files=all` 记录现场，按 K8 给脏文件分类。
   * 按 K7 判断能否继续。
1. **确定输入**
   * **plan 单元**：给了 U-ID，或 plan 路径加单元编号。
   * **Issue**：给了编号，用 `gh issue view` 读取。
   * **直接需求**：一段描述，没有 plan。
   * **空输入**：取 `current.md` "下一步"的第一项；没有就询问。这里替换 CE 按最新 plan 自动发现的做法。
   * 直接需求按规模分流（沿用 CE `work-intake.md` 的表格）：
     * 琐碎：直接做
     * 中小：在会话里列任务清单
     * 大：建议先 `nk-plan`，由用户决定
   * 读 plan 时只读需要的部分：先列章节结构，再读当前单元及它引用的内容；同时留意"推迟到实现时决定的问题"和范围边界。
2. **执行循环**（每个单元）
   * **已完成检查**：代码库里已经有这个单元要做的东西、且满足验证标准时，核实后直接标记完成，不重做（跨会话接力时很重要）。
   * **准备**：找可参照的现有代码写法；做测试发现（Test Discovery）；选定证据策略（沿用 CE 的五种情形表）。
   * **测试先行**：按 vertical slices 做 red → green，每轮一个 seam、一个测试、一段最小实现（按 K3 自选 seam）。
   * **测试质量**：遵守 CE 的证据守则和 Matt 列出的反模式（与实现耦合、同义反复、先写完所有测试再写实现的水平切片）。
   * **收尾检查**：做 System-Wide Test Check（5 问）。
   * **验证**：运行相关测试；未运行的不算通过。
3. **新发现分流**：按 `artifact-lifecycle.md` 第三章处理。影响当前 plan 的，修改 plan 并附变更记录，随本单元提交。
4. **单元完成**：按 `nk-commit` 规则提交，带 U-ID 和验证证据。
5. **继续或结束**：按 K2 决定继续下一单元，还是建议运行 `nk-handoff`。
   * 单元做不完或验证不过时：能拆分的，拆分单元并修改 plan；拆不了的，保留半成品，直接进入交接。

**子代理**（可选，不作为默认）
* 用途：调查、并行阅读，或在全新上下文中实现一个单元。
* 子代理不提交；交回改动文件和验证证据。
* 主对话核对实际工作树后再提交。

**references**

| 文件 | 内容 | 来源 |
| :-- | :-- | :-- |
| `references/intake.md` | 输入分类、规模分流、plan 读取方法、前置条件核实 | CE `input-triage.md`（节选）+ `work-intake.md` |
| `references/implementation-loop.md` | 执行循环、测试发现、证据策略表、测试场景完整性、System-Wide 5 问、延续既有写法、持续测试 | CE `implementation-loop.md` |
| `references/testing.md` | 好测试与坏测试、seam、何时 mock、为可 mock 而设计 | Matt `tdd/SKILL.md` + `tests.md` + `mocking.md` |
| `references/subagents.md` | 单元任务包内容、全新上下文、子代理不提交、核对实际工作树；附录：共享目录下的并行波次（非默认） | CE `execution-strategy.md`（精简）+ `agents/implementation-worker.md` |
| `references/ui-work.md` | 前端改动的检查要点（桌面与窄屏宽度、文字溢出、有浏览器就实际查看） | CE `implementation-loop.md` 第 7 节 |
| `references/non-code.md` | 交付物不是代码时的执行方式 | CE `non-code-execution.md` |
| `references/out-of-repo-state.md` | 完成标志依赖仓库外状态（控制台配置、线上数据等）时的判定方法 | CE `implementation-loop.md` 循环内的一条规则 |

**来源取舍**

| 来源 | 处理 | 理由 |
| :-- | :-- | :-- |
| `CE/ce-work/SKILL.md` Outcome、Phase 0–2 结构 | 改写 | 去掉引擎选择与 Return-to-Caller 分支后重组为第 0–5 步 |
| 同上 Phase 3–4 审查关卡 | 删除 | 按 K9 |
| `references/input-triage.md` 恢复语法、mode 参数、`docs_root` 配置、最新 plan 发现 | 删除 | 依赖 K1 删除的控制器；`docs_root` 是 CE 专有配置；空输入改从 `current.md` 取 |
| 同上 plan 充分性判断、前置条件核实 | 保留 → `intake.md` | 能防止在不成熟的 plan 上开工 |
| `references/work-intake.md` 规模分流、plan 读取方法、任务清单 | 保留 → `intake.md` | 实战有效；任务清单改成"有任务工具就用" |
| 同上 "Do not re-scope the plan into human-time phases" 一节 | 改写 | 它认为上下文压力应靠子代理解决，与我们一个会话一个单元的模型相反；改写为 K2 |
| `references/workspace-setup.md` pre-work scope、已脏文件只问一次 | 保留并改写 | 与 K8 对接 |
| 同上 分支设置 | 改写 | 按 K5 |
| 同上 "Do not edit the plan body" | 保留 | 即 K4 |
| `references/implementation-loop.md` 循环、证据策略、守则、测试发现、测试场景完整性、System-Wide 5 问 | 保留 | 这是 CE 最有价值的工程纪律 |
| 同上 跨模型执行、并行波次两段 | 删除 / 下沉 | 跨模型按 K1 删除；并行波次下沉到 `subagents.md` 附录 |
| 同上 增量提交一节 | 改写 | 统一交给 `nk-commit` |
| 同上 Simplify as You Go | 删除（P4 重新评估） | P1 不调用精简技能；留给 P4 `nk-simplify` 决定是否在执行中触发 |
| 同上 Figma Design Sync、`references/agents/figma-design-sync.md` | **默认删除，请你确认** | 依赖 Figma 相关工具，paper-30min 与个人项目目前没有 Figma 设计稿。如果以后可能用上，改为下沉 |
| 同上 前端设计指引 | 下沉 → `ui-work.md` | 通用，paper-30min 有 UI |
| 同上 进度记录、已定决策（settled decisions） | 保留（精简） | 已定决策的规则防止执行者擅自推翻用户定过的事；进度按 K4 以提交为准 |
| `references/execution-strategy.md` | 精简 → `subagents.md` | 保留全新上下文、任务包、子代理不提交、核对实际工作树；删除默认并行调度与各客户端的集成细节 |
| `references/shipping-workflow.md` | 删除，部分移交 | 审查关卡与剩余发现处理 → P4；PR 与上线监控 → P3 评估；"项目自定的交付流程优先"的原则保留进 SKILL.md 第 0 步 |
| `references/review-findings-followup.md`、`tracker-defer.md` | 移交 P4/P3 | 属于审查与归档；P1 的"开 Issue"直接用 `gh issue create` |
| `references/return-to-caller.md` | 删除 | 目前没有编排型的调用方；将来需要时再看 |
| `references/execution-engines.md`、`cross-model-execution.md`、`implementation-result-schema.json`、`scripts/` | 删除 | 按 K1 |
| `Matt/tdd/SKILL.md` 什么是好测试、seam、反模式、循环规则 | 保留 → `testing.md` | 与 CE 证据策略互补：CE 管证据，Matt 管测试写法 |
| 同上 "先与用户确认 seams" | 改写 | 按 K3 |
| 同上 "Refactoring 不属于循环" | 保留 | 与 P1 不做精简一致 |
| 同上 读 `CONTEXT.md` 与 ADR | 改写 | 改为读 `CONCEPTS.md` 与 `docs/solutions/` |
| `Matt/tdd/tests.md`、`mocking.md` | 保留 → `testing.md` | 质量高、体量小 |
| `Matt/implement/SKILL.md` | 吸收 | "定期跑类型检查、单个测试文件，最后跑完整套件"的节奏写入 `implementation-loop.md`；"完成后 code-review"按 K9 不采纳 |

---

### 3.3 `nk-handoff`

**职责**：会话结束时覆盖更新 `docs/current.md`，按提交规则入库，并告诉用户下一个会话从哪里开始。

**description 草案**：
> End a session cleanly: rewrite docs/current.md (state, evidence, blockers, next unit, uncommitted work) and commit it per cadence rules so any agent can resume. 会话交接、结束会话、更新 current.md。

**流程**
1. **收集事实**：
   * 分支、HEAD、`git status`
   * 本会话的提交：`git log` 查带 U-ID 的提交
   * 本会话运行过的验证及结果
   * 仍在工作区的半成品
2. **覆盖写 `current.md`**：按 `conventions/current-md.md` 的字段。写法要求：
   * **只写可核实的现状**：存在什么、做了一半的是什么、缺什么、什么依赖什么。不给下一个 Agent 下命令。
   * **注明来源**：意图和决定要写清是用户说的、Agent 推断的，还是 Agent 自己定的。
   * **只放指针**：引用 plan、Issue、提交、文件时写路径，并说明其中具体哪部分重要，不复制内容。
   * **写已放弃的路径**：失败过的方案和下一个 Agent 容易重蹈的弯路（写入 U0 新增的可选字段）。
   * **脱敏**：去掉密钥、凭据和无关个人信息。
3. **初始化检查**：项目还没有 `current.md` 时新建；`AGENTS.md` 缺少指向 `current.md`、`solutions/`、`CONCEPTS.md` 的指引时补上（`artifact-lifecycle.md` 规定的维护责任）。
4. **提交**，按优先级：
   * 上一个提交是本会话的且未推送 → amend 并入（R3，连纯文档提交都省掉）
   * 否则 → 一次纯文档提交（R4）
   * 提交信息风格按 K11。
5. **报告**：
   * 两三句话说明交接内容
   * 半成品和 `[待确认]` 项的提醒
   * 下一会话的建议技能（沿用 Matt 的 suggested skills）

**references**：`conventions/current-md.md`、`conventions/commit-cadence.md`

**来源取舍**

| 来源 | 处理 | 理由 |
| :-- | :-- | :-- |
| `CE/ce-handoff/SKILL.md` Create 部分的只放指针、脱敏、完成后确认写入 | 保留 | 通用原则 |
| 同上 Resume 部分、`references/resume.md` | 删除 | 按 K6、K7 |
| 同上 输出可复制的恢复命令 | 删除 | 新会话通过 `AGENTS.md` → `current.md` 自动定位，不需要命令 |
| `references/create.md` 临时目录存储、frontmatter 协议、原子文件名 | 删除 | 交接载体改为仓库内单例 `current.md`，文件不再堆积、也不会丢失 |
| 同上 正文覆盖要点（已放弃的路径、意图归属、可核实的现状、只放指针） | 保留 | 这是 CE 交接质量的核心，写进第 2 步 |
| `Matt/handoff/SKILL.md` 不重复已有产物、建议下一步技能、参数作为下一会话关注点 | 保留 | 参数改为"下一步"的优先项 |
| 同上 保存到系统临时目录 | 删除 | 同上 |

---

## 四、实施单元

每个单元完成后按 R1 提交，提交信息带 `(U-ID)`。

### U0 共享约定修订
* **文件**：`conventions/current-md.md`、`conventions/commit-cadence.md`、`conventions/decision-autonomy.md`、`conventions/artifact-lifecycle.md`
* **内容**：
  * **K4**：删除"在 Plan 中勾选单元进度"的说法（`current-md.md` 第 57 行附近、`commit-cadence.md` R1/R2 的举例），改为"进度以带 U-ID 的提交为准；plan 只在范围或做法变化时修改"。
  * **`current-md.md` 新增可选字段"已排除的方案"**：最多 3 条，记录试过但不可行的做法。
  * **`commit-cadence.md` R4 补充**：交接时如果上一个提交是本会话的且未推送，优先 amend。
  * **`decision-autonomy.md`**：把 `mode:non-interactive` 改为不依赖具体客户端的写法。
  * **`artifact-lifecycle.md`**：补一句分支策略由项目决定（K5）。
* **验证**：6 份约定之间交叉检查，没有残留的"勾选"表述；`grep -rn "勾选" conventions/` 的结果只剩合理用法。

### U1 `nk-commit`
* **文件**：`nk-commit/SKILL.md`
* **验证**：
  * 在临时 git 仓库里手动走一遍第 3 步的五种判定。
  * 用含 `$`、引号、多行正文的提交信息测试 `-F` 提交。
  * 工作区存在外来脏文件时，确认它不会被提交。

### U2 `nk-work`
* **文件**：`nk-work/SKILL.md`、`nk-work/references/` 下 7 个文件
* **验证**：
  * 逐条对照 3.2 的来源取舍表，确认"保留"项都已移入，"删除"项没有残留引用（`grep -rn "ce-code-review\|cross-model\|unit-workspace\|return-to-caller" nk-work/` 无结果）。
  * `SKILL.md` 引用的每个 reference 文件都存在。

### U3 `nk-handoff`
* **文件**：`nk-handoff/SKILL.md`
* **验证**：用本仓库自身做一次交接，生成的 `docs/current.md` 符合 `current-md.md` 格式，提交方式符合第 4 步的优先级。

### U4 成稿评审（Claude）
* 对照本方案、共享约定和原文检查：
  * 冲突与遗漏
  * 是否写了某个客户端专有的工具名
  * `description` 的触发是否准确
  * 三个技能之间的衔接（`nk-work` 第 5 步 → `nk-handoff`；二者 → `nk-commit`）
* 意见修复后 P1 完成。

### P1 之后：自用试用
从 P2 起，NexusKit 仓库自身的开发用 `nk-work`、`nk-commit`、`nk-handoff` 推进，以便在进入 paper-30min 前暴露基础约定的问题。发现的问题记入本 plan 的变更记录，修复随相应提交。

---

## 五、验收场景（全部阶段完成后在 paper-30min 统一执行）

P1 不单独在 paper-30min 验收。原因是各技能按接口配合：`nk-work` 读取 `nk-plan` 的产出，混用 CE 格式的 plan 测到的是错误的接口。以下场景并入统一迁移后的整体验收（RFC 第八章"迁移与验收"阶段）。验收期间如果 CE 仍在安装状态，一律按名字显式调用 nk 技能。

| # | 场景 | 通过标准 |
| :-- | :-- | :-- |
| A1 | 按 plan 单元正常完成 | 实现、测试先行、提交各一次；提交带 U-ID 与验证证据；没有额外的纯文档提交 |
| A2 | 一个会话连续完成两个紧密相关的小单元 | 两个单元各一次提交；会话结束时只有一次交接更新（amend 或 R4 提交） |
| A3 | 带半成品交接 | `current.md` 如实填写"未提交改动"；半成品没有被提交；外来脏文件没有被暂存 |
| A4 | **用另一个客户端接手**（例如 Claude Code 交给 Codex） | 接手方读取 `current.md`，现场一致时直接继续；人为制造分支不一致时停下询问 |
| A5 | 验证失败或无法运行 | 没有把未通过的内容提交；未运行的测试在提交说明或 `current.md` 中标记为未验证 |
| A6 | 直接需求（没有 plan） | 按规模分流；提交不带 U-ID；在两个客户端中对比 `description` 能否正确触发（验证 K12） |

**总体检查**：验收结束后在 paper-30min 执行 `git log --stat`。纯文档提交只出现在交接点；`current.md` 只在交接提交或被 amend 的提交里出现。

---

## 六、风险与待确认

1. **Figma 相关内容默认删除**：需要你确认（见 3.2 取舍表）。
2. **开发目录就是加载目录**：`~/.agents/skills` 下写到一半的 `nk-*` 会被部分 Agent 直接加载。U1–U3 期间如果担心影响其他项目，可以先在 `SKILL.md` 的 `description` 里标注"开发中"，或者在 U4 之前暂不放到顶层目录。
3. **共享约定用相对路径引用**：开发期可用；打包时如何分发留到打包阶段决定（RFC 开放问题 3）。
4. **K4 改变了 P0 约定**：需要你认可后才能执行 U0。

---

## 变更记录

* 2026-09-25：初稿。
* 2026-09-25：实战验收从 P1 移到全部阶段完成后统一进行；U5 改为从 P2 起在 NexusKit 仓库自用试用。
