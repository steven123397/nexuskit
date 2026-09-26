# 沉淀模式细则

> 路径解析：本文件中 `../../conventions/`、`../../nk-commit/` 相对于本技能目录解析；`docs/solutions/`、`CONCEPTS.md`、`AGENTS.md` 指目标仓库中的文件。

## 1. 定位与采样

**定位刚解决的问题**：以当前会话上下文为主——排查过程、失败的尝试、最终修复、验证证据。需要补充事实时用 `git log`、`git diff` 查看本会话的提交与工作区改动。不挖掘历史会话记录：CE 用脚本扫描各客户端的历史会话文件，NexusKit 已删除该脚本组；刚解决的问题就在当前会话里，历史会话中未沉淀的线索交给审计模式或下一次遭遇。

**一次一条**：一个会话产出多条经验时分多次运行。交叉引用在草稿之间缝合，会把"第 3 条"这类草稿编号泄漏进成文。

**语料优先采样**：写 frontmatter 前先看 `docs/solutions/` 既有条目——目录优先沿用，`component`、`root_cause`、`tags` 优先复用既有拼写。规则见 [`../../conventions/solution-schema.md`](../../conventions/solution-schema.md) 第二章，此处不重述。

**重叠判定**：检索同问题域的既有条目，按问题陈述、根因、方案、引用文件、预防规则五个维度评估：

| 重叠 | 动作 |
| :-- | :-- |
| 高（基本相同的问题与方案） | 更新既有条目：保留路径与 frontmatter 结构，更新正文、示例与预防建议；不建新文档 |
| 中（同域，不同角度/根因/方案） | 正常新建；在汇报中标注为审计候选 |
| 低/无 | 正常新建 |

更新而非重复新建的原因：两份描述同一问题的文档必然逐渐漂移；新上下文更新鲜，并入既有条目。

**文件名**：`[problem-slug].md`，不加日期后缀（`date` frontmatter 字段即创建日期）。写前确认目标路径不存在；已存在且覆盖同一问题则走更新。

## 2. 编写与自检

模板与字段以 [`../../conventions/solution-schema.md`](../../conventions/solution-schema.md) 第三、四章为准。写作纪律：

- **行为断言先读源码**：断言代码行为（枚举值、状态语义、限制、默认值）前，读当前树的定义行并在文中标注 `file:line`；无法核实的断言软化或注明"按本次会话结论"，不写成事实。
- **合并状态引用 PR 编号而非裸 SHA**：SHA 会被 rebase/squash 重写；"已在 X 修复"要求修复在当前树可达，否则写为待定（如"已在 #123 打开，本文撰写时未合并"）。
- **流程复盘线**：工作流/协作过程本身的问题用 `workflow_issue`（Knowledge 轨），正文同样走模板：当时怎么卡住、根因在流程哪个环节、以后怎么防。

写完后执行两项自检（给 Agent 读的核对清单，替代 CE 的校验脚本）：

1. [`frontmatter-checklist.md`](frontmatter-checklist.md)——frontmatter 解析安全与字段核对；
2. [`claims-checklist.md`](claims-checklist.md)——正文引用（路径、SHA、链接、草稿残留）逐项裁决：修正、标注为历史、或确认有意为之。

## 3. 术语补全

按 [`../../conventions/concepts-vocabulary.md`](../../conventions/concepts-vocabulary.md) 执行，本模式只做 **Add / Refine**：

- 扫描新文档与会话中出现的合格领域术语，增量补录 `CONCEPTS.md`；
- 文件不存在且本次确有合格术语时，可创建文件并只写本次的术语，不顺带初建整个项目的术语表（整库初建是审计模式的职责）；
- 词条的行为规则类断言（生命周期、状态流转）写入前同样先读源码核对；
- Fold / Retire / Scrub 不在本模式执行——发现需要时记入汇报，留给审计模式。

## 4. 可选增强评审（按 problem_type 映射）

支持子代理的客户端读取 `agents/` 下对应提示词，用它初始化一个通用子代理；不支持时在主会话内联评审。评审只针对文档与示例，不修改产品代码；无收益则跳过本阶段。

| problem_type / 情形 | 提示词 |
| :-- | :-- |
| `performance_issue` | `agents/performance-oracle.md` |
| `security_issue` | `agents/security-sentinel.md` |
| `database_issue` | `agents/data-integrity-guardian.md` |
| 反复出现 / 疑似反模式 | `agents/pattern-recognition-specialist.md` |
| 需要业界实践佐证 | `agents/best-practices-researcher.md` |
| 需要框架/库官方文档佐证 | `agents/framework-docs-researcher.md` |

评审发现由主会话裁决并落到文档；子代理不直接改知识库文件。

## 5. 可见性检查与提交

**可见性（首次在某项目运行时必查）**：按 [`../../conventions/artifact-lifecycle.md`](../../conventions/artifact-lifecycle.md) 第二章，检查目标项目根的 `AGENTS.md`（或等价全局指令文件）是否有指向 `docs/current.md`、`docs/solutions/`、`CONCEPTS.md` 的指引；缺则补一行最小指引，描述性语气（如"在已记录领域实施或排障时相关"），不写"必须先检索"式命令句。`CONCEPTS.md` 不存在时不补它的指引，不催促项目采纳。

**提交去向（R4 第 4 条，见 [`../../conventions/commit-cadence.md`](../../conventions/commit-cadence.md)）**：

1. 优先在修复/特性提交**之前**完成沉淀，随代码与测试一同提交；
2. 代码已提交但尚未推送 → 按 R3 amend，且必须显式限定路径，防止把工作区半成品带进提交：
   ```bash
   git add docs/solutions/<category>/<file>.md  # 以及本次改动的 CONCEPTS.md、AGENTS.md
   git commit --amend --no-edit -- docs/solutions/<category>/<file>.md  # 末尾同样列出全部路径
   ```
3. 已推送到远端 → 留在工作区，待下一个交接点或下一次代码提交一同入库，并在汇报中说明去向。

本技能自己发起提交时，先读 [`../../nk-commit/SKILL.md`](../../nk-commit/SKILL.md) 并遵循其规则。

## 6. 汇报

- **已建档**：文件路径、轨道与 problem_type、重叠结论、两项自检结果、术语补全结果（"扫描，无合格术语"也是有效结果）、可见性检查结论、提交去向、审计建议（有明确过期候选时给出最窄的范围提示）。
- **未建档**：一句话说明哪条准入门槛不通过。
