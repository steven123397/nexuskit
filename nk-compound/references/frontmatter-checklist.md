# Frontmatter 自检清单

> 路径解析：`../../conventions/` 相对于本技能目录解析。

沉淀或重写 solution 条目后逐项核对。此清单替代 CE 的 `validate-frontmatter.py`（脚本已删除），核对范围与脚本一致：**解析安全**（防止 YAML 静默截断），另加 solution-schema 字段核对。

## A. 解析安全（静默损坏防线）

1. **分隔线**：frontmatter 的开、闭分隔线各自独占一行且内容恰为 `---`（行尾空白可以；`----`、`---extra` 不是合法分隔线）。
2. **顶层标量值中的 ` #`**：对每条顶层映射项（行首无缩进的 `key: value`），若值未加引号也不是结构（不以 `"`、`'`、`[`、`{`、`|`、`>` 开头），值中不得出现空格+`#`——YAML 把它当注释，**静默截断**其后内容。出现则给整个值加双引号。
3. **顶层标量值中的 `: `**：同样范围内，值中不得出现冒号+空格——严格解析器可能读成嵌套映射。出现则给整个值加双引号。
4. **数组项引号**：`symptoms`、`applies_when`、`tags` 等所有字符串数组字段，数组项以保留指示符（`` ` ``、`[`、`*`、`&`、`!`、`|`、`>`、`%`、`@`、`?`）开头或包含 `: ` 时，整项加双引号。

核对范围说明：第 2、3 条只管顶层映射项——嵌套值、数组项本身、已加引号或结构化的值不在其内；值以保留指示符开头会产生响亮的解析错误而非静默损坏，不在此列。修到全部通过为止，不带着未通过项宣告完成。

## B. 字段核对（对照 [`../../conventions/solution-schema.md`](../../conventions/solution-schema.md)）

- [ ] `problem_type` 取值在其轨道表内，轨道判定正确（Bug / Knowledge）；
- [ ] 共享必填字段齐全（`title`、`date`、`problem_type`、`component`、`module`、`severity`），`date` 为 `YYYY-MM-DD`；
- [ ] Bug 轨必填 `symptoms`（1~5 条）、`root_cause`、`resolution_type`；Knowledge 轨不强行填 Bug 轨字段；
- [ ] 枚举字段（`severity`、`resolution_type`）取值精确匹配；
- [ ] 开放词汇字段（`component`、`root_cause`）沿用语料既有拼写，不新造近义词；
- [ ] `retire_when` 只在指导成立依赖仓库外部条件时填写，且写清如何检查；不需要时省略该字段；
- [ ] 架构决策类条目按需填 `status` / `superseded_by`。
