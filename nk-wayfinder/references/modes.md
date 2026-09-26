# 两种模式的详细步骤 (Modes)

> **路径解析说明：** 本文件中引用的技能文件（`../../nk-*/`）相对于本技能所在目录解析，不在目标代码仓库中查找。

无论哪种模式，**每个会话最多 resolve 一个 ticket**（research 除外）。用户可能并行运行多个会话处理 unblocked tickets，预期 tracker 被并发编辑；claim 与查询都以 tracker 实时状态为准。

## Chart the map（用户带着松散想法调用）

1. **Name the destination.** 与用户对话确定 map 要找到的 spec、decision 或 change。Destination 固定 scope，先解决它。
2. **Map the frontier.** 再对话一轮，**breadth-first** 覆盖整个空间而不深入单条线索，浮现 open decisions 与现在可开始的 first steps。**如果没有 fog**，说明路径已经清晰，不需要 map；停止并建议直接走 `nk-plan`。
3. **Create the map**（`wayfinder:map`）：填好 Destination 与 Notes，Decisions so far 留空，fog 勾勒进 **Not yet specified**。
4. **Create the tickets you can specify now** 作为 child issues，然后第二遍再 wire blocking edges（issues 需要编号后才能互相引用）。现在还说不清的留在 **Not yet specified**。
5. **启动 research。** 对刚创建的每个 `research` ticket，如果支持子代理则并行派发，否则在主会话内联完成；findings 从 ticket 链接出去。
6. 停止。Charting 是一个会话的工作；不在本会话手动 resolve tickets。

## Work through the map（用户带 map URL 或编号调用）

1. 加载 **map**：低分辨率全局视图，不逐个读 ticket body。
2. 选 ticket：用户点名就用它；未点名时由你按序拿第一个 frontier ticket。先 claim 再开工。
3. Resolve it：按需 **zoom**——只在需要时读相关或已关闭 ticket 的完整 body；调用 map **Notes** 指定的技能与资料。Prototype 类 ticket 构建廉价粗糙的具体产物（outline、rough take、stub）辅助讨论，作为 asset 链接。
4. 记录 resolution：答案作为 **resolution comment** 发布，**close** issue，向 map 的 Decisions so far 追加一行 gist 与链接。
5. 维护 map：把答案已经说清的 fog 升级成新 tickets（create-then-wire），并从 **Not yet specified** 清掉每个已升级条目；发现出界的 ticket 按 Out of scope 规则处理；答案使其他 tickets 失效时更新或删除它们。

到达 map 边缘（不再有 open tickets）时，稳定下来值得实施的 build 工作交给 `nk-plan` / `nk-work`。
