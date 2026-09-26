# Direct 与 Chat brief 两个聊天档位

阶段 0.6 选中 Direct 或 Chat brief 时读本文件。Durable 路线不读。

## 两者共同点

* 结果在聊天里用平实的句子给出；除非用户要求，不在 `docs/plans/` 写文件。
* 不派子代理、不做置信度检查、不做写后自检、不出收尾菜单，结果本身就结束本次运行。
* `nk-plan` 仍然不动手实现。Direct 只描述改动，实现交给 `nk-work` 或用户。

## Direct

用几句话说明改什么、在哪里改、怎么验证。然后用一行提供交接：交给 `nk-work`，或用户自己改。只有用户接受时才调用 `nk-work`，并把这段说明作为它的输入；规划调用本身不构成实施授权。说明和交接提议都在聊天里给出后即完成。

## Chat brief

在聊天中给出：

* 几句话说明改什么、为什么；
* 实施单元，每个写明文件和测试预期；
* 请求或 brainstorm 已定下、实现者必须遵守的决策，写一行；没有就不写。

最后一行提议：保存为文件，或交给 `nk-work`。用户说"继续"时，把这份 brief 作为 `nk-work` 的直接需求输入。

brainstorm 摘要中带有实现者必须遵守的已定决策时，至少选 Chat brief，让这个决策有地方落下。

## 保存 Chat brief

用户要的东西超出 brief 的范围（完整 plan 的全部章节）时，按 Durable 重新规划。否则把 brief 写成普通 Markdown：路径形如 `docs/plans/YYYY-MM-DD-HHMM-<type>-<topic>-plan.md`，frontmatter 只写 `title`、`type`、`date`，代码交付物加 `execution: code`；不写 `plan_contract`，因为它不满足完整 plan 的章节要求。路径冲突时在扩展名前加最小可用的数字后缀，不覆盖已有文件。
