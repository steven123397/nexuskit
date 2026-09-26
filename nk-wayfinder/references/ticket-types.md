# Ticket 类型与 HITL/AFK 判定

> 每个 ticket 带一个 `wayfinder:<type>` label。每个 ticket 同时是 **HITL**（human in the loop，与能代表自己发言的人类一起处理）或 **AFK**（Agent 独立驱动）。HITL ticket 只能通过 live exchange 解决——一旦 Agent 开始自问自答，这个 ticket 的处理就已经坏了。

## 四种类型

### Research（AFK）

阅读文档、第三方 API、本地知识库等资源，找出某项 decision 正在等待的事实。当需要当前工作目录之外的知识时使用。

- 支持子代理的客户端并行派发研究子代理；不支持时在主会话内联完成。
- Resolution 记录找到的事实、来源链接，以及它对 pending decisions 意味着什么。
- Research tickets 不受"每会话一个 ticket"限制：它们互不依赖、无状态，可以在 charting 会话中成批派出。

### Prototype（HITL）

核心问题是 "how should it look" 或 "how should it behave" 时使用。构建廉价、粗糙、具体的产物提高讨论保真度：outline、rough take、stub，或一小段 UI/逻辑代码。产物作为 asset 从 ticket 链接，不粘贴进 body。

- 廉价是约束不是缺点：原型用来暴露问题供人讨论，不是交付物。一旦开始打磨它，就超出了 ticket 的职责。

### Grilling（HITL，默认类型）

纯对话。拿不准类型时用 grilling。

- 对话按 [`../../conventions/decision-autonomy.md`](../../conventions/decision-autonomy.md) 的提问规则进行：选项驱动、互不依赖的问题合并一轮（至多 3 个）、标注推荐项；收集事实与叙述的问题可以开放式提问。
- 对话中敲定的新领域术语按 [`../../conventions/concepts-vocabulary.md`](../../conventions/concepts-vocabulary.md) 即时写入 `CONCEPTS.md`；用词与术语表冲突时当面指出并对齐。

### Task（HITL 或 AFK）

做出 decision 之前必须完成、但本身没有要 decide、prototype 或 research 的手工工作。例如：注册一个服务以评估其 API、配置访问权限、移动一批数据以看清它的 shape。

- 这是唯一会 **do** 而不是 decide 的类型；它凭借解锁 decision 而存在，不交付 destination。
- Agent 能独立完成时按 AFK 处理；否则给人类一份精确的 checklist（HITL）。
- Resolution 记录做了什么，以及后续 tickets 依赖的事实：凭据位置、新 URL、行数等。

## 无人值守限制

无人值守（无人类即时响应）时，HITL ticket 不可 resolve：按 decision-autonomy 约定的兜底规则，不挂起等待，而是把该 ticket 在 `docs/current.md` 登记为 `[待确认]`，附当前卡点，然后结束本会话或转去处理 AFK 工作。

## 每会话一个 ticket

无论类型（research 除外），每个会话最多 resolve 一个 ticket。原因：ticket 之间的依赖靠 resolution 后的 map 维护（升级 fog、wire 新 edges、作废失效 tickets）保持准确，一次解决多个会跳过这些维护，让 map 失真；而且每个 ticket 都值得一个干净的会话上下文。完成一个 ticket 的全部记录与 map 维护后，本会话结束，下一个 ticket 交给下一个会话（或交给你自己新开的一轮）。
