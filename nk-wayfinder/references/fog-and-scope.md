# Fog of war 与 Out of scope 判定细则

> Map 是**有意**不完整的：不描绘你还看不见的东西。本文件定义 **Not yet specified**（在 scope 内的 fog）与 **Out of scope**（被排除的工作）两节的维护规则。

## Fog of war

Tickets 之外是 fog：你能感觉到以后会来的 decisions 和 investigations，但它们悬在仍未解决的问题之上，暂时无法钉住。解决一个 ticket 会清掉它前方的一片 fog，把现在已经能说明的问题升级成新 tickets；一次一个，直到通往 destination 的路清楚、不再有 tickets 剩下。

**Not yet specified** 一节记录这种朦胧视野：怀疑中的问题、之后要回访的区域。这里的内容全部在 scope 内，只是还不够清晰成为 ticket。可以按视野允许的粗细来写；它也是协作者阅读这个 effort 走向时的路标。

### Fog or ticket?

判定标准是**你现在能不能把问题说清楚**，而不是现在能不能回答它。

- **建成 ticket**：问题已经清晰，即使它被 blocked、现在不能处理。
- **留在 Not yet specified**：还不能说清楚。不要把 fog 预切成 ticket-sized pieces——fog 比 ticket 粗，frontier 到达后，一片 fog 可能升级成多个 tickets，也可能一个都没有。

### 维护规则

- **排除**：Not yet specified 不包含已决定的内容（Decisions so far）、已是 live ticket 的内容、以及 out of scope 的内容。
- **升级（graduate）**：ticket 解决后，把答案已经说清的 fog 建成新 tickets（先创建、拿到编号后再 wire blocking edges），并从 Not yet specified 删去每个已升级条目——它只作为新 ticket 存在，不在两处重复。
- **无 fog 即无 map**：charting 时如果 breadth-first 扫完发现没有 fog，说明路径已清晰、一个会话能走完，不需要 map。

## Out of scope

Fog 只会聚集在通往 destination 的方向；destination 固定 scope。超出 destination 的工作是 **out of scope**，不是 fog，也不属于 Not yet specified。决定一件事归这里的是 **scope**，不是清晰度。

### 规则

1. **永不升级**：out-of-scope work 永远不会变成 ticket；frontier 会停在 destination。只有重画 destination 时它才会回来，而且那应成为一个新的 effort，不是原 map 的延续。
2. **排除是 scoping act，不是路线上的一步**：把某事排除出 scope 不消耗 ticket，也不计入 Decisions so far——后者只记录真正走过的路线，scope 边界不是路线上的一步。
3. **live ticket 出界**：charting 时被错误划入 scope、或被某次 resolution 暴露出在 destination 之外的已有 ticket，应 **close 它**（closed ticket 明确不在 frontier 上），并在 Out of scope 一节留一行：gist、为何出界、指向 closed ticket 的链接。不要放进 Decisions so far。

### 条目格式

```markdown
- <被排除工作的 gist> — <为何出界>（若源自 ticket：[<closed ticket name>](link)）
```
