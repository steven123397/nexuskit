# 价值提炼细则 (Harvest)

> **路径解析说明：** 本文件中引用的约定文件（`../../conventions/`）均相对于本技能所在目录解析，不在目标代码仓库中查找。`docs/solutions/`、`CONCEPTS.md` 指目标仓库中的文件。

收尾第 2 步的操作细则。准入门槛本身以约定为准，本文件只讲从 plan 里怎么找、找到后怎么办。

## 找什么

按价值密度从高到低扫读即将删除的 plan 与审查记录：

1. **决策理由（主要提炼对象）**：plan 中"为什么这么做"的段落——关键技术选型、被否决的备选方案及否决原因、敲定方案时接受的妥协。
2. **踩坑因果**：实施中暴露的缺陷与返工的因果链，通常散落在 plan 末尾的变更说明、审查记录的遗留条目里。
3. **新领域术语**：实施过程中稳定下来、且规划期未及时录入的业务概念。

不提炼：实现细节本身（代码即文档）、例行技术选型、纯进度记录。

## 怎么判断

* 写入 `docs/solutions/` 前，先过 [`../../conventions/solution-schema.md`](../../conventions/solution-schema.md) 的双轨准入：Bug 轨过反事实检验，Knowledge 轨过决策三门槛；任一不满足则不建档，内容留在 Git 历史中即可。
* 写入 `CONCEPTS.md` 前，过 [`../../conventions/concepts-vocabulary.md`](../../conventions/concepts-vocabulary.md) 的准入标准（领域专属性 + 独立概念性）。
* 拿不准的一律不建档：收尾提炼是减量动作，宁缺毋滥，错过的东西可由后续的 `nk-compound` 或 refresh 机制补捞。

## 怎么写

* **`docs/solutions/`**：先检索既有语料，子目录与 `component`、`tags` 等开放词汇沿用既有拼写（语料优先）；frontmatter 与正文模板按 solution-schema 的第三、四节，决策类记录按内容分量选轻量或结构化档位。
* **`CONCEPTS.md`**：按 concepts-vocabulary 的词条结构书写，只使用其规定的 5 种原子变更；退役术语需要正面证据，拿不准保持现状。
* 提炼产物不单独提交，与被删除的 plan 一起进入收尾那一次 R4 提交（见 SKILL.md 第 5 步）。
