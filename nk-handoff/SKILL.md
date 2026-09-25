---
name: nk-handoff
description: End a session cleanly: rewrite docs/current.md (state, evidence, blockers, next unit, uncommitted work) and commit it per cadence rules so any agent can resume. 会话交接、结束会话、更新 current.md。
---

# /nk-handoff

在会话结束时覆盖更新单例入口 `docs/current.md`，根据提交节奏规则入库，确保任何 Agent（或人类）在下一个全新会话中能够零信息损耗接手。

**完成标志：** `docs/current.md` 覆盖更新并入库（amend 或 R4 交接提交），向用户清晰汇报交接摘要与下一步建议。  
**工作原则：** 单例覆盖、只放指针、如实登记工作区半成品、不记流水账。

---

## 执行步骤

### 1. 收集现场事实 (Gather Facts)
1. **工作树与分支**：核对当前分支、HEAD 提交哈希，运行 `git status --short --untracked-files=all`。
2. **本会话产出**：通过 `git log` 提取本会话生成的带 U-ID 的提交及正文中的验证证据。
3. **工作区残留**：检查工作区是否残留未完成或未验证的代码半成品；识别外来脏文件。
4. **用户参数**：若用户调用 `/nk-handoff` 时传入了关注点参数（如 `/nk-handoff 重点解决语法解析报错`），将其作为“下一步”的首要关注点。

### 2. 覆盖写入 `docs/current.md`
严格依照 [`conventions/current-md.md`](../conventions/current-md.md) 模板重写文件，保持在 20~40 行内：

* **`# 当前状态`**：记录所在分支、版本/关联 Plan、当前系统已具备的核心能力、以及客观验证结果（测试命令与通过数；未运行的必须注明未验证）。
* **`## 阻断与已知缺口`**：记录阻塞推进的外部依赖、Issue 链接或 `[待确认]` 决策项；无阻断则写“无”。
* **`## 下一步`**：直接引用 Plan 中的实施单元编号（如 `实施单元 U4`）或最紧迫的 Issue 编号，单处维护不复制描述。
* **`## 工作区未提交改动`**（若存在半成品代码必填）：说明涉及文件/单元、当前完成阶段、明确标注验证状态（如“未验证，尚无法通过编译”）。
* **`## 已排除的方案`**（可选，最多 3 条）：记录本会话或前期验证不可行的路径及原因，防止后续接手者重蹈覆辙。

#### 编写质量原则：
* **只写可核实的现状**：客观陈述存在什么、缺什么，不给下一个 Agent 下主观指令；
* **注明来源归属**：关键意图或决策说明是用户指定的、代码推断的还是 Agent 自选的；
* **只放指针**：引用 Plan、Issue、提交、代码文件时给出路径并说明关键点，不全文复制内容；
* **信息脱敏**：绝对不写入 API Key、密码、Token 或无关的个人敏感信息。

### 3. 可见性维护检查 (Discoverability Check)
* 若项目尚未建立 `docs/current.md`，新建该文件；
* 检查项目根目录的 `AGENTS.md`（或等价指令文件）：若缺少指向 `docs/current.md`、`docs/solutions/` 与 `CONCEPTS.md` 的指引，进行补充（履行 `conventions/artifact-lifecycle.md` 规定的维护责任）。

### 4. 提交入库 (Commit per Cadence)
按以下优先级调用 `/nk-commit` 规则执行提交：

1. **优先级 1（R3 amend 优先）**：
   * 若上一个提交属于本会话产生，且尚未推送到远端（通过 `git log @{u}..HEAD` 或无 upstream 判定）；
   * 优先执行 `git commit --amend` 将 `docs/current.md` 的修改直接并入上一个提交，连纯文档提交都省去。
2. **优先级 2（R4 纯文档提交）**：
   * 若上一个提交已推送到远端，或本会话尚未发起过代码提交；
   * 发起一次规范的纯文档交接提交，提交信息风格遵循项目惯例（如 `docs: handoff session - <下一步简述>` 或 `docs(流程): 交接会话`）。

### 5. 汇报交接摘要 (Handoff Report)
向用户输出结构化汇报：
* 2~3 句话概括本会话交付的成果与当前系统状态；
* 明确提醒遗留的工作区半成品与任何 `[待确认]` 事项；
* 给出下一个会话的建议技能（如：建议接手会话调用 `/nk-work` 认领下一步单元）。

---

> 主要参考：CE `ce-handoff` (2026-09)、Matt `handoff`、NexusKit 共享约定 [`conventions/current-md.md`](../conventions/current-md.md)
