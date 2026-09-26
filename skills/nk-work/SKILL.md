---
name: nk-work
description: "Execute one implementation unit from a plan, an Issue, or a clear request: orient from docs/current.md, test-first implementation, verification evidence, cadence-compliant commits. Use nk-debug for open-ended bugs. 执行实施单元、按计划实现、测试先行。"
---

# /nk-work

> **路径解析说明：** 本文件中引用的参考文件（如 `references/`、`../conventions/`、`../nk-commit/`）均相对于本技能所在目录解析，不在目标代码仓库中查找。

接手现场，执行并验证一个或多个实施单元，每个单元读取并遵循 `../nk-commit/SKILL.md` 规则独立提交。

**完成标志：** 认领的单元通过测试先行实现，通过验证，提交信息携带 `(U-ID)` 与验证证据，代码与文档同行提交。  
**工作原则：** 单会话聚焦推进；进度以提交为准；未运行的测试不记为通过。

---

## 执行步骤

### 0. 定位与环境核对 (Orient)
1. **读取状态与指引**：读取目标仓库的 `docs/current.md`（若存在）获取当前能力、验证结果、阻断项与下一步；从 `AGENTS.md` 索引项目工作流文档（如 `docs/release-workflow.md`），必要时查阅 `CONCEPTS.md` 与 `docs/solutions/` 相关背景。
2. **核对现场与分支**：核对当前所在分支；运行 `git status --short --untracked-files=all` 记录现场；用 `git rev-parse --short HEAD` 与 `current.md` 记录的 HEAD 比对——不一致时不阻断，向用户报告"检测到 N 个未记录的中间提交"（`git rev-list --count <旧哈希>..HEAD`）再继续。
3. **脏文件分类**：
   * `current.md` 中“工作区未提交改动”登记的文件视为上一个会话交接的半成品，由本会话接管；
   * 其余未跟踪或未提交的改动视为外来脏文件，本次工作不暂存或提交；若本单元必须修改这些文件，在第一次提交前向用户统一确认一次。
4. **接手准则**：现场一致则直接开始；仅在以下情况停下询问用户：
   * 当前分支与 `current.md` 记录不一致；
   * 工作区实际改动与 `current.md` 登记的未提交改动不符；
   * 存在直接阻碍本单元的 `[待确认]` 项。

### 1. 确定输入与范围 (Intake)
* **来源识别**（详见 [`references/intake.md`](references/intake.md)）：
  * **Plan 单元**：输入携带 U-ID 或 Plan 路径加单元编号。按需阅读 Plan（先看章节结构，仅精读当前单元与依赖项，并核实 Plan 充分性）。
  * **Issue**：输入携带编号，读取 Issue 内容。
  * **空输入**：默认取 `docs/current.md` 中“下一步”的第一项；若无下一步则询问用户。
  * **直接需求**：按规模分流（琐碎直接做、中小列清单、大型建议先执行 `/nk-plan` 由用户决定）。

### 2. 单元执行循环 (Implementation Loop)
对认领的每一个单元，执行标准循环（详见 [`references/implementation-loop.md`](references/implementation-loop.md)）：
1. **已完成检查**：核查现有代码库是否已包含该单元目标且满足验证标准（若涉及仓库外状态见 [`references/out-of-repo-state.md`](references/out-of-repo-state.md)）。若已满足，核实后直接视为完成，不重复编码。
2. **准备与对齐**：检索参考现有代码写法；执行测试发现（Test Discovery）；根据**已有测试状况**选定证据策略；补全测试场景（正常、边界、错误、集成）。
3. **测试先行（TDD）**：按照垂直切片推进红绿循环（Red -> Green），每轮自选一个 Seam、写一个失败测试并确认因预期原因变红、再写最小实现使测试通过（详见 [`references/testing.md`](references/testing.md)，遵守证据守则，循环内不做重构精简）。
4. **系统级因果检查**：执行 System-Wide 5 问（回调传播、真实调用链、孤立状态、平行接口、跨层错误对齐）；根据改动类型核对 [`references/ui-work.md`](references/ui-work.md) 或 [`references/non-code.md`](references/non-code.md)。
5. **实际验证**：在终端实际运行测试命令并捕获证据。未运行的测试不记为通过。

### 3. 执行中新发现分流 (Triage)
* **影响当前 Plan 范围或做法**：直接修改当前 Plan 正文，在末尾附一行变更说明，随本单元一同提交（见 [`../conventions/artifact-lifecycle.md`](../conventions/artifact-lifecycle.md)）。尊重已定决策（Settled Decisions），不擅自推翻用户已敲定的方案。
* **无关需求或疑难 Bug**：不顺手扩大范围，直接创建 GitHub Issue（无远端时记入 `docs/backlog.md`）。
* **伴生小缺陷**：随当前单元一并修复并补齐测试。

### 4. 单元完成与提交 (Unit Commit)
* 单元验证通过后，读取 [`../nk-commit/SKILL.md`](../nk-commit/SKILL.md) 并按其规则发起提交：
  * 主题行包含成果说明，末尾追加实施单元编号，例如：`feat(auth): add token expiry check (U2)`；
  * 正文写入 1~3 行实际运行的验证命令、结果与未验证项；
  * 若本单元修复了 `docs/reviews/` 中的审查条目，在同一提交中把该条目状态改为 `已修复`（格式与状态词表见 [`../nk-review/references/entry-format.md`](../nk-review/references/entry-format.md)；节奏见 R2/R6）。

### 5. 顺延或结束会话 (Next or Wrap up)
* **顺延判断**：若当前上下文依然宽裕，且下一单元与本单元紧密相关，可顺延执行下一单元，重复步骤 2~4。
* **结束交接**：若单元完成且上下文消耗较多，或单元遇阻形成半成品，停止开发，读取 [`../nk-handoff/SKILL.md`](../nk-handoff/SKILL.md) 更新 `current.md` 并交接会话。

---

## 子代理支持 (Subagents，可选)
* **适用场景**：独立调查、并行阅读文档、或在全新干净上下文中实现具体算法单元。
* **纪律**：子代理不执行 `git commit`；将改动文件与验证证据回传至主对话，由主对话核对实际工作区后统一提交（详见 [`references/subagents.md`](references/subagents.md)）。
