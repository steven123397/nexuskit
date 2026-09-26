---
name: nk-wayfinder
description: Chart an oversized, foggy goal into a shared decision map on the issue tracker, then resolve decision tickets one per session until the path to the destination is clear. Use when a goal is too big and too unknown for a single plan or session, when the path forward cannot be seen, for decision maps and wayfinding. 超大模糊目标、看不清路径、决策地图、decision ticket、wayfinding。
argument-hint: "[可选：map issue URL 或编号；留空则带着新想法 chart]"
disable-model-invocation: true
---

# /nk-wayfinder

> **路径解析说明：** 本文件及其 references 中引用的文件（`references/`、`../conventions/`、`../nk-*/`）均相对于本技能所在目录解析，不在目标代码仓库中查找。

一个松散想法出现了：它太大，单个会话装不下，而且被 fog 包围，通往 **destination** 的路还看不见。Wayfinding 的目标是找到这条路，而不是朝 destination 猛冲：把路径绘制成 issue tracker 上的 **shared map**，逐个解决 **decision tickets**——它们承载需要决策才能解决的问题，而不是要执行的 build slice——直到路线清晰。

**完成标志：** 别人动手前已没有任何事情需要决定、路径完全清晰，map 上不再有 tickets；charting 会话的完成标志是 map 与首批 tickets 建好、research 已派出。**工作原则：** map 是索引不是 store；ticket 只承载 decision；每个会话最多 resolve 一个 ticket（research 除外）；fog 不预切成 tickets。

## 前置条件：GitHub tracker

Tracker 固定为 GitHub Issues，通过 `gh` CLI 操作。开始前确认仓库有 GitHub 远端且 `gh` 可用（`gh repo view`）。Wayfinder 强依赖 tracker 的查询与可视化能力，**无远端时本技能不可用**：不要发明本地降级格式，改用 [`../nk-brainstorm/SKILL.md`](../nk-brainstorm/SKILL.md)（澄清目标）或 [`../nk-plan/SKILL.md`](../nk-plan/SKILL.md)（直接规划）。所需 label 不存在时用 `gh label create` 创建。Map、child tickets、blocking 与 frontier 查询的具体操作见 [`references/tracker-operations.md`](references/tracker-operations.md)。

## Plan, don't do

Wayfinder 默认用于 **planning**：每个 ticket 解决一个 decision，只产出 decisions，不产出 deliverables。想直接动手做的冲动通常表示你已到达 map 边缘，该交接了。Effort 可以在 map 的 **Notes** 中覆盖这个默认值，把 execution 纳入 map。

## The Map

Map 是带 `wayfinder:map` label 的单个 issue，是 canonical artifact；tickets 是它的 child issues。Map 是 **index**，不是 store：只列已做 decisions 的一行 gist 与链接，细节只存在 ticket 一处；open tickets 不列在 map body 里，通过查询找到。**Refer by name**：每张 map 和每个 ticket 的 name 就是它的 title，所有给人看的内容都用 name 加链接引用，不单独写裸编号——一堵 `#42, #43, #44` 很难读，name 一眼能懂。

### Map body

```markdown
## Destination
<走到 map 尽头是什么样子——要找的 spec、decision 或 change。一两行；每个会话选 ticket 前先向它对齐。>

## Notes
<领域背景；每个会话应查阅的技能与资料；本 effort 的常备偏好>

## Decisions so far
- [<closed ticket title>](link) — <答案的一行 gist；细节 zoom 进 ticket 看>

## Not yet specified
<在 scope 内但还说不清的 fog；frontier 推进时升级为 ticket>

## Out of scope
<被有意识排除在 destination 之外的工作；关闭，永不升级>
```

### Tickets

每个 ticket 是 map 的 child issue；body 是一节 `## Question`，写清这个 ticket 要解决的 decision 或 investigation，大小控制在单个会话能装下。每个 ticket 带一个 `wayfinder:<type>` label；四种类型与 HITL/AFK 判定细则见 [`references/ticket-types.md`](references/ticket-types.md)。

- **Claim**：开始任何工作**之前**先把 ticket assign 给自己，并发会话才会跳过它。Open 且 unassigned 才算 unclaimed。
- **Blocking**：优先用 GitHub 原生依赖关系，tracker UI 会可视化 frontier；不支持时退回 body 约定。所有 blockers 关闭后 ticket 即 unblocked；**frontier** = open + unblocked + unclaimed 的 tickets，也就是已知世界的边缘。
- 答案不写进 body，在 resolution 时以 comment 记录；解决中产生的 assets 从 issue 链接出去，不粘贴进 body。

## Fog of war 与 Out of scope

Map 是**有意**不完整的：不描绘还看不见的东西；判定与维护细则见 [`references/fog-and-scope.md`](references/fog-and-scope.md)。还说不清的问题写进 **Not yet specified**，不预切成 tickets——判定标准是"现在能不能把问题说清楚"，不是"能不能回答"。超出 destination 的工作进 **Out of scope**，永不升级；已有 ticket 被发现出界时 close 它，并在该节留一行 gist、原因与链接，不计入 Decisions so far。

## 术语与提问

HITL 对话按 [`../conventions/decision-autonomy.md`](../conventions/decision-autonomy.md) 的提问规则进行：互不依赖的问题合并一轮（至多 3 个）、选项驱动并标注推荐项；HITL ticket 的答案只能来自人类，Agent 不替人类回答。解决过程中敲定的新领域术语、或发现用词与 `CONCEPTS.md` 冲突时，按 [`../conventions/concepts-vocabulary.md`](../conventions/concepts-vocabulary.md) 当场处理并即时写入。

## 两种模式

**Chart the map**（用户带着松散想法调用）：命名 destination → 广撒网式对话浮现 open decisions（没有 fog 则停下建议直接 `nk-plan`）→ 建 map 与首批 tickets → 派发 research → 停止，charting 就是一个会话的工作。**Work through the map**（用户带 map 调用）：加载 map → claim 一个 frontier ticket → resolve → 以 comment 记录并 close、维护 map。两种模式下**每个会话最多 resolve 一个 ticket**（research 除外）。

详细步骤见 [`references/modes.md`](references/modes.md)；稳定下来值得实施的 build 工作在到达 map 边缘后交给 [`../nk-plan/SKILL.md`](../nk-plan/SKILL.md) / [`../nk-work/SKILL.md`](../nk-work/SKILL.md)。

## 与体系衔接

- ticket 解决中沉淀出非显而易见的经验或决策理由 → [`../nk-compound/SKILL.md`](../nk-compound/SKILL.md)。
- 会话结束 → [`../nk-handoff/SKILL.md`](../nk-handoff/SKILL.md) 登记现场；无人值守时的 `[待确认]` 项登记在 `docs/current.md`（见 decision-autonomy 约定第三章）。HITL ticket 在无人值守下不可 resolve，登记后跳过。
