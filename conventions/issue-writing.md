# Issue / Backlog 条目写作规范 (Issue Writing)

> **定位：** 统一"落档为待办"的写法。Issue 是跨 plan 事务的载体（D5），它可能在 backlog 里躺上数周，然后被一个毫无现场上下文的 Agent 或会话认领（`nk-work` 的合法输入之一）——写作质量直接决定接手质量。
> **生产者与消费者：** `nk-to-issue` 是核实分析后的主要生产者；`nk-debug`、`nk-close`、`nk-review`、`nk-wayfinder` 在流程内"转 Issue"时遵循同一格式。本约定只管"长什么样"，不管"何时转"（时机见 [`artifact-lifecycle.md`](artifact-lifecycle.md) 第四章）。

---

## 一、去向

1. **有 GitHub 远端**：用 `gh issue create` 落档，标题与正文按本规范。
2. **无远端**：写入 `docs/backlog.md`，每条一个条目，格式与 Issue 正文同构；文件改动不单独提交，随下一个代码提交或会话交接入库（[`commit-cadence.md`](commit-cadence.md) R2/R4）。

## 二、写作四原则（吸收自 Matt `AGENT-BRIEF`）

1. **持久性优于精确**：Issue 落档后代码会继续演化。定位用接口、类型、行为契约的名字，**不引用文件路径和行号**——它们会过期（这与 `docs/reviews/` 里的短期审查条目相反，后者用 `file:line` 是因为活不过一个版本）。
2. **行为而非步骤**：描述系统应该做什么，不写实现步骤。接手的 Agent 会重新探索代码库并自行决定实现方式。
3. **验收标准可独立验证**：每条标准单独可测，让接手者知道什么时候算完成。
4. **范围边界明确**：写清不做什么，防止接手者镀金或误伤相邻功能。

## 三、条目格式

```markdown
**Category**：bug / enhancement

**Current behavior**：（现状；bug 写损坏的行为，enhancement 写现状基础）

**Desired behavior**：（完成后的预期行为，含边界与错误情况）

**Key interfaces**：（涉及的接口/类型/配置形状及需要的改变；不知道就省略本节）

**Acceptance criteria**：
- [ ] 每条可独立验证

**Out of scope**：（明确排除的相邻工作）

**Evidence**（bug 必填）：核实结论（已确认 / 未能复现）、复现步骤、脱敏后的报错摘要。
未能复现时写明还缺什么信息。

**Source**：（一行溯源：来自哪个 plan / 审查条目编号 / 会话，及日期）
```

小节标题用英文锚点；正文语言随项目惯例。琐碎小项（一句话能说清的待办）可以只写标题加一句 Desired behavior，不强套全格式。

## 四、例外

`nk-wayfinder` 的 map 与 decision ticket 有自己的专用格式（Destination / Question / Decisions so far），由该技能自行定义，不适用本规范。
