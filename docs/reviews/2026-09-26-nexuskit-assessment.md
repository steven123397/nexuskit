# 处理结论（2026-09-26）

本评审的全部条目已处理完毕：

- 缺陷 1–3（K 编码悬空、R4.4 引用、过期表述）：已修，`851abd9`。
- 缺陷 4（契约无机械校验）：已修，`tests/run_checks.py` 四项检查 + GitHub Actions CI，`2fde272`。
- 缺陷 5（重复提示词无同步机制）：已修，10 组逐文件加 nk-copy 声明头 + 清单锁定，`52d3e7a`。
- 缺陷 6（客户端工具名残留）：以中立法声明处理（英文原文保真），`c13227d`。
- 缺陷 7（SKILL.md 超 8000 字节）：已修，nk-wayfinder / nk-debug 瘦身至 ~7.9KB，`3dcf114`。
- 结构隐患 2（常驻开销）：已做，5 个手动技能加 `disable-model-invocation`，`783c68a`。
- 章节七借鉴：Smart Zone / 子代理输出体量 / HEAD 哈希 / Context Pointer 已做（`c13227d`）；Fresh Worker 与 return-to-caller 否决并记入 RFC D11；打包范式留打包阶段。
- 结构隐患 1（conventions 打包）：已登记于 RFC 开放问题 3。
- "只做三件事"之 3（迁移验收）：即路线图下一阶段。

生命周期：本文件是已收敛的审查记录，留存于 `docs/reviews/`；本仓库首次版本收尾时由 `nk-close` 决定提炼或删除。

---

# 评审原文


# 一、结论先行

**在设计与文本质量两个维度上，NexusKit 已经超过两者，不是"接近"。在严谨度机制上达到了，但缺最后一层机械保障——而这一层恰好是它已经暴露出 6 处可验证失效的直接原因。在跨 Agent 打包和真实验证两个维度上，尚未达到。**

一句话：**体系设计是一流水准，工程质量配不上它的设计。**

---

# 二、量级对照

|                 | Matt Pocock                                        | Compound Engineering                                                                                                         | NexusKit                                               |
| :-------------- | :------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------- |
| 技能数          | 24                                                 | 35                                                                                                                           | 15                                                     |
| Markdown 总量   | ~124 KB（技能部分约 60 KB）                        | 99,976 行 / 3.3 MB                                                                                                           | 11,106 行                                              |
| `SKILL.md` 正文 | 4–11 KB，`implement` 只有 **6 行**                 | 每份 7.9 KB 左右，上限被测试卡死在 8000 字节                                                                                 | 平均 70 行，最大 `nk-wayfinder` 101 行                 |
| 常驻上下文      | 多数 `disable-model-invocation: true` → **零常驻** | 35 个 description 常驻                                                                                                       | 15 个 description 常驻                                 |
| 子代理提示词    | 无独立 persona 体系                                | 67 份 / 6,175 行                                                                                                             | 43 份 / 4,234 行                                       |
| 脚本            | `skills-cli` 打包 CLI                              | **53 个 / 44,923 行**                                                                                                        | 1 个（`nk-wizard/assets/template.sh`，上游逐字节保留） |
| 测试            | 无                                                 | **80 个测试文件，其中 17 个是 parity/contract 测试**，CI 含 windows-native job、`claude plugin validate --strict`、3690 pass | 无                                                     |
| 版本迭代证据    | 无                                                 | CHANGELOG 80+ 版本，dogfood 报告 12/12 场景                                                                                  | 29 个提交，自我声明"未验证：真实项目中的端到端使用"    |

---

# 三、NexusKit 真正强于两者之处

不是"改写得好"，是**设计决策的层级高一级**。

### 1. 产物生命周期（D3/D4）是原创洞察
CE 和 Matt 都没有。paper-30min 的实证是：Matt 时期留下 11 份 walkthrough + 一堆 7 行 ADR，CE 时期一天产生 5 份 `docs/reviews/`。NexusKit 的诊断是对的——**"堆积是生命周期问题，不是哪套体系独有的问题"**（RFC 第二章）。给每类产物定终点（plan/review 随版本收尾提炼后删除、Issue 承接跨 plan 事务、solutions/CONCEPTS 永久），挂"版本收尾"而不挂 PR，这个解法比两者的任何机制都彻底。

### 2. 决策自主权两级分类（D6）是对两套的明确修正
Matt 的 `grill` 把可推断细节抛回给人，CE 规定"每轮一问"。`conventions/decision-autonomy.md` 给了可操作判据：**可逆/局部/有惯例 → 自决；范围外溢/不可逆/外部契约破坏/用户可见行为差异 → 确认**，配 mermaid 图、典型场景清单、单轮最多 3 问的批量规则。还有一条很讲究的例外："收集事实与叙述的问题可以开放式提问……预先给出选项会把回答引向提问者的假设"——这是对选项驱动提问的反噬抑制。

### 3. 派生可审计（D8）
每个技能文末有「与上游的主要差异及原因」，逐条列删了什么、为什么。CE 和 Matt 都没有这个。这让体系能长期独立演进而不静默漂移。

### 4. 「已定决策不污染对抗性视角」
`settled-decisions.md` 结尾：把已定决策交给做对抗/核实工作的子代理时，**"不要传入支持该决策的论证理由；做对抗性或核实工作的子代理不应看到哪些决策被标为已定"**，并附固定一句 `If you find evidence a settled decision cannot work, report it — do not suppress it.`。这是防确认偏误污染子代理的机制，CE 有雏形，NexusKit 的表述更锋利。

### 5. 审查机制转写准确且更凝练
`nk-review` 完整保留了 CE 的离散置信度锚点（0/25/50/75/100，**不允许中间值**）、quote-the-line 门（"75/100 的首条证据必须引用使问题成立的原文行，引不出就降到 50"）、误报目录、独立复核三值判定（confirmed/rejected/unresolved）、受保护主题列表。并加了一条 CE 没有的硬约束：**"预算耗尽时剩余条目一律 unresolved，理由'预算耗尽，未检查'，不猜判定"**。`validate.md` 41 行做到了 CE 原文 44 KB 的核心。

### 6. 双轨知识库 + `retire_when`
`solution-schema.md` 比 CE 的 `schema.yaml` 更完整：合并了 ADR（Matt 三门槛原样保留），加了 `retire_when` 外部退役触发条件、`stale` / `stale_reason` / `stale_date` 三件套、"删除需要正面证据"。CE 的 schema.yaml 没有这些。

### 7. 完成标志制度化
15/15 个技能都有「完成标志 + 工作原则」双声明和阶段表。Matt 基本没有（`implement` 全文 6 行），CE 只有 `ce-plan` 这类核心技能有 `Mandatory Completion Contract`。

### 8. `current.md` 单例入口优于两者的交接机制
CE 的 `ce-handoff` 产出临时目录中的独立文件，每次交接新建一个，来源不可信——接手方必须怀疑它可能过期或被篡改。Matt 的 `handoff` 产出保存到 OS 临时目录的文档，同样存在多份交接文件的堆积风险。NexusKit 的 `docs/current.md` 是**仓库内单例覆盖写**——不堆积、不丢失，`AGENTS.md` 指向它让新会话自动找到，`nk-work` 的 Orient 步骤核对分支和改动一致性再决定是否询问。CE 在 `ce-work` 的 input triage 中写的是「parse the handoff document, but do not trust it」，NexusKit 反转了信任模型：本仓库控制的单例文件**默认可信**，不一致时才停。

### 9. System-Wide 因果 5 问是 CE 没有的实施纪律
`nk-work/references/implementation-loop.md` 在每个单元的 TDD 循环后插入 5 个系统级检查：(1) 回调/中间件传播、(2) 真实调用链还是全被 Mock 屏蔽、(3) 失败时是否留下孤立脏状态、(4) 平行接口是否暴露相同逻辑、(5) 跨层错误捕获策略冲突。CE 的 `ce-work` 没有这类结构化的实施后自检；Matt 的 `tdd` 也没有——它止步于 red-green 循环本身。这 5 个问题恰好对准了 AI Agent 在编写实现代码时最常犯的系统级遗漏。

### 10. `nk-to-issue` 的三重去重
Matt 的 `triage` 围绕 maintainer 的 labels/buckets/state roles 组织批量分诊，有查重但侧重外部贡献者管理。NexusKit 把它收窄为「开发中冒出的单条发现」，去掉外部贡献者表面后暴露出原版没有的检查：第三重去重查 `docs/ideation/` 与 `docs/solutions/` 看该想法是否曾被否决或已有沉淀——这用了产物生命周期提供的结构。CE 没有等价技能。

### 11. Fresh-Context Critic 的反锚定设计
`nk-ideate` 的依据核查子代理启动时不接触任何生成历史（零上下文启动），独立检验各点子的 basis 真实性。CE `ce-ideate` 同样做了但没解释为什么。NexusKit 在 `references/post-ideation-workflow.md` 中把它提升为显式设计原则：「核查者不应看到候选排名或淘汰标记，避免锚定效应」——把隐性工程判断变成可审计的设计声明。

### 12. 子代理 Prompt Caching 亲和设计
`nk-ideate/references/divergent-ideation.md` 要求所有发想子代理共享逐字节一致的 `<grounding>` 块，放在提示词最前面。这利用了 LLM 提供商的 Prompt Cache 机制——相同前缀的多个并行请求共享 KV cache，降低延迟和成本。CE 的 Scratch Dossier 模式解决的是防止子代理返回过多内容导致父窗口膨胀，但没有考虑缓存亲和。

---

# 四、已暴露的缺陷（我逐条验证过，非推测）

## 缺陷 1 —— K 编码悬空：契约被放进了会被删除的产物里 ★最尖锐

`K2`/`K3`/`K5`/`K7`/`K8`/`K10`/`K11` 在**已发布的技能里被当契约引用 11 处**：

```
nk-commit/SKILL.md:50   遵循项目既有策略（K5）
nk-commit/SKILL.md:55   按以下优先级确定提交信息格式（K11）
nk-commit/SKILL.md:69   验证证据（K10）
nk-commit/SKILL.md:78   隔离外来脏文件（K8）
nk-work/SKILL.md:22     脏文件分类（K8）
nk-work/SKILL.md:25     接手准则（K7）
nk-work/SKILL.md:41     自选一个 Seam（K3）
nk-work/SKILL.md:53     写入 1~3 行…（K10）
nk-work/SKILL.md:57     顺延判断（K2）
```

而它们的**定义只存在于 `docs/plans/2026-09-25-p1-execution-trio-plan.md`，该文件已被 `65c7940` 按 D3 规则删除**。全仓 `conventions/` 里搜 `K1|K4|K6|K9|K12` 无任何命中——说明这套编码从未被提升为共享约定。

这是 RFC 第七章 D4「plan 收尾时提炼长期价值后删除」的**自伤**：把跨技能契约写进了设计上注定被删的产物。它证明了生命周期设计的边界没划清——plan 里可以放"这次怎么做的"，不能放"下次也照这么办"。

修复成本很低（把 7 行定义移进 `conventions/`），但**发现它的机制不存在**，这才是要害。

## 缺陷 2 —— `R4.4` 引用不存在

`nk-compound` SKILL.md 第 40/56/68 行与 `references/capture.md:66` 共 4 处引用 `commit-cadence.md R4.4`。但 `commit-cadence.md` 的 R4 是 4 条编号列表，**没有 R4.4 这个编号**。同一个"引用了一个够不着的契约"的模式。

## 缺陷 3 —— 两处过期表述

- `nk-close/SKILL.md:74`：「`docs/reviews/` 目录不存在时跳过并说明：**`nk-review` 是规划中的技能，尚未提供**」——nk-review 已在 P4 交付。
- `nk-plan/references/phase-0.md:89`：「（NexusKit 的 `nk-debug`；**尚未提供时**用可用的调试方式）」——nk-debug 已交付。

P4/P5 落地后没人回改上游技能。这类漂移是重复文件的直接后果。

## 缺陷 4 —— 契约无机械校验，而 CE 有整整一层

CE 有 17 个 parity/contract 测试，机制极其对症：

- `tests/durable-bar-parity.test.ts` —— 校验 `<!-- ce-durable-bar -->` 块在 `ce-compound` 与 `ce-compound-refresh` 两份副本里**逐字节一致**
- `tests/settled-decisions-parity.test.ts`、`config-layers-rule-parity.test.ts`、`docs-root-rule-parity.test.ts` —— 同类
- `tests/codex-skill-prompt-budget.test.ts` —— 强制 SKILL.md 不越 8000 字节
- `ce-commit-contract.test.ts`、`review-skill-contract.test.ts`、`pipeline-review-contract.test.ts`

**缺陷 1/2/3 全都是 parity 测试能自动抓到的那类错误。** current.md 自己记录了"全仓 131 个 Markdown 文件相对链接检查：0 失效"——说明已经用到脚本方法，但**没有入库成测试**。（我实测链接确实 0 失效，这一点做得好。）

## 缺陷 5 —— 5 组重复提示词无同步机制

`best-practices-researcher`、`data-integrity-guardian`、`data-migration-reviewer`、`deployment-verification-agent`、`framework-docs-researcher`、`pattern-recognition-specialist`、`performance-oracle`、`security-sentinel`、`web-researcher` 各 2 份；`learnings-researcher` **3 份**（259 / 250 / 251 行）。三份实际内容已经分叉：`nk-plan` 版含 planning 专属段落和 `applies_when` 字段说明，`nk-ideate` 版换成了 ideation 措辞。**分叉本身可能是有意的**（每个调用方要不同视角），但没有任何地方声明"这 3 份刻意的差异是什么"，也没测试锁定共享部分。current.md 把它登记为待决缺口——正确，但它需要的正是 CE 的 parity 机制。

## 缺陷 6 —— 客户端专有工具名残留，违反自己的 D8 第 5 条

RFC 第七章第 5 条：「正文不依赖某个客户端专有的工具名」。实际残留：

```
nk-plan/references/agents/best-practices-researcher.md:60    mcp__context7__resolve-library-id
nk-compound/references/agents/best-practices-researcher.md:61  mcp__context7__query-docs
nk-ideate/references/agents/issue-intelligence-analyst.md:24   mcp__github__*
nk-review/references/personas/project-standards-reviewer.md:27 TodoWrite
```

最后一条尤其讽刺：`project-standards-reviewer` 把「`TodoWrite` instead of `TaskCreate`」列为**跨平台可移植性违规的示例**，而它自己就带着这个字符串。这几处都在英文 persona 原文里（`nk-review` 明确说"persona 提示词保持英文原文"），属于保留了上游但没做中立化扫描。

## 缺陷 7 —— `nk-wayfinder/SKILL.md` 9,557 字节，越过 CE 实测的 Codex 8000 字节注入上限

CE 的测试注释写得很清楚：**Codex ≥ 0.147 只注入每个 SKILL.md 的前 `MAX_SKILL_PROMPT_BYTES`（8000）**，它们为此维护了一份 `OVER_BUDGET` 名单并在逐步清空。NexusKit 的正文里完全没提这个约束，`nk-wayfinder` 已超标 19%。它的结构恰好是「前半段导航 + 后半段两种模式的详细步骤」，截断会砍掉 `Work through the map`。打包成多 Agent 插件时这会在 Codex 上静默失效。

## 次要 —— 两个结构性隐患

- **`conventions/` 的打包未决**（RFC 第九章开放问题 3）。开发期用 `../conventions/` 相对路径共享，但插件生态通常要求技能自包含。这不是文字问题，是打包时会爆的结构问题——10 份约定被 15 个技能跨目录引用。
- **15 个 description 全部常驻**。Matt 对纯手动技能一律 `disable-model-invocation: true` 换零常驻上下文，只保留真正需要自主触发的（`code-review`、`tdd`、`domain-modeling`）。NexusKit 里 `nk-wait-what`、`nk-commit`、`nk-handoff`、`nk-close`、`nk-wizard`、`nk-wayfinder` 这类基本靠人显式调用的技能，可以省下这份常驻成本。

---

# 五、分维度裁决

| 维度               | 结论           | 依据                                                                                                                                                 |
| :----------------- | :------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------- |
| **设计架构**       | **超过两套**   | D1–D10 逐条有实证依据、有删减理由、有可审计的派生记录。RFC 2.0 的组织度是 CE 的 `STRATEGY.md`（定位文档）+ 30 份散落 brainstorm 文件所不具备的       |
| **可执行性**       | **达到或超过** | 完成标志/工作原则/阶段表/路径解析说明四件套 15/15 覆盖；0 失效链接；具体命令、字段、格式齐备。CE 有但被 8 KB 散文稀释；Matt 的 `implement` 只有 6 行 |
| **严谨度（机制）** | **达到**       | 置信度锚点、quote gate、独立三值复核、受保护主题、双轨准入、反事实检验、claims-checklist——都是三者中最高质量的部分，且转写准确                       |
| **严谨度（保障）** | **未达到**     | 无测试、无 CI、无 parity 锁定、无 lint。已在 6 处失效，且**没有任何机制能发现它们**。CE 有 80 个测试 + 7 个 job 的 CI                                |
| **知识沉淀**       | **达到或超过** | `solution-schema.md` 比 CE `schema.yaml` 更完整；`CONCEPTS.md` 即时写入解决了 CE 的"只在 compound 时生长"缺陷                                        |
| **跨 Agent 打包**  | **未达到**     | CE：`plugin.json` + 10 个 host 目录 + 9 个 converter + install/cleanup CLI。Matt：`skills-cli`。NexusKit：开发目录，且 `conventions/` 共享方式未决   |
| **真实验证**       | **未达到**     | CE：dogfood 12/12 场景含 1 项带回归测试的修复、3690 pass、80+ 版本。NexusKit：15 个技能全部止步于"单元验证 + 成稿评审"，从未跑过一个完整周期         |

**回答你的问题：工程性上能否达到另外两套的水准？**

- 作为**体系设计**：已经超过了。
- 作为**可交付的工程制品**：还差一层。而缺的那一层不是能力问题，是**把已有的方法固化成代码**——你已经写了链接检查脚本，只是没入库；你已经用 parity 的思路（"同一规则只在一处写全"）约束了文档，只是没约束文件。

---

# 六、如果只做三件事

1. **把 7 个 K 编码定义移进 `conventions/`**，并立一条规则：**跨技能契约只能住在 `conventions/`，不能住在 plan 里**。顺手修 `R4.4` 和两处"尚未提供"。这修的不是 4 个错字，是"契约可继承"的存在性漏洞。

2. **把链接检查升级成 `tests/`**，优先写四个：链接完整性、`R<n>`/`K<n>` 引用必须能解析、重复提示词的共享段落 parity、SKILL.md 字节上限。这四类恰好覆盖了全部 6 处已暴露失效。CE 的 `durable-bar-parity` 是最小可抄样本。

3. **按 RFC 第八章先跑 paper-30min 迁移验收，再打包。** 目前最大的单点风险不是任何一条缺陷，而是"15 个技能从未在一个真实项目上跑完整周期"。打包会把 `conventions/` 的共享方式和 8 KB 上限两个结构问题同时引爆，而这两个问题在迁移验收里都会先以更便宜的形式暴露。

现在的状态是：**设计的严谨度已经领先，工程保障还停在"靠人工核对"**。而 `docs/current.md` 里那句"未验证：真实项目中的端到端使用"说明你对这一点是清醒的。

---

# 七、从两套上游中还可以借鉴的具体机制

以下不是"缺陷"（体系运转不依赖它们），是"如果要做，从哪里拿"的清单。

### 1. `disable-model-invocation: true` 减常驻开销

Matt 对纯手动触发的技能一律设 `disable-model-invocation: true`，只在用户显式调用时才注入 SKILL.md，系统提示词中只留 description。他实测这可以**减少 63% 的后台 token 消耗**（30+ skill 场景）。NexusKit 15 个 description 全部常驻，但 `nk-wait-what`（13 行）、`nk-commit`、`nk-handoff`、`nk-close`、`nk-wizard`、`nk-wayfinder` 这 6 个基本靠人显式调用，可以省下这份常驻成本。打包成插件时优先考虑。

### 2. Matt 的「Smart Zone」约束应显式文档化

Matt 明确提出：即使 Gemini 支持 1M–2M context window，推理质量在 **<100k tokens（理想 <30k）** 时最佳——他称之为 "Smart Zone"。NexusKit 的「一个会话一个单元」设计天然遵循了这个原则，但设计理由没有显式记录。建议在 RFC 或 `conventions/` 中补一句：**"单会话单单元的设计动机是让 Agent 始终在 context window 最佳推理区间内工作"**，让后人理解这不是任意选择。

### 3. CE 的 Scratch Dossier 模式可作为子代理输出隔离的参考

CE 的子代理把完整输出写入 `/tmp/compound-engineering-<uid>/` 专用目录，只返回 `{gist: "...", path: "/tmp/..."}` 给主会话。这防止了并行子代理返回大量内容导致编排者 context 膨胀。NexusKit 的子代理规则（`references/subagents.md`）只规定了「不 commit、改动回传主会话」，没有规定输出体量控制。当发想/规划阶段派发 5+ 子代理时，如果每个返回完整研究报告会把主会话窗口吃满。建议在 `subagents.md` 或 `decision-autonomy.md` 中补一条**输出体量约定**：子代理返回结果超过一定阈值时，写入临时文件并只返回摘要 + 路径。

### 4. CE 的 Fresh Worker Invariant 可强化子代理纪律

CE 的 `ce-work` 严格执行：每个实现子代理只处理一个单元，处理完毕后 handle 立即退休，绝不复用。这防止了跨单元 context 污染（前一个单元的 Mock 残留、错误的命名假设等渗透到下一个单元）。NexusKit 的子代理使用是「可选」的，没有这层退休纪律。如果未来允许子代理直接实现多个单元，需要这条规则。

### 5. CE 的 `mode:return-to-caller` 令牌体系的精简版

CE 能构建 `lfg` 全自动流水线的基础是每个 skill 都支持 `mode:return-to-caller`——以结构化 JSON 返回 status/artifacts/blockers 给调用方。NexusKit 的设计哲学是「工具箱不是流水线」，不需要完整的令牌体系。但可以考虑一个**极简版**：让 `nk-plan` 和 `nk-work` 在被其他技能内部引用（而非用户直接调用）时，输出一个固定格式的状态行（如 `status: complete | blocked`、`artifact: <path>`），便于未来的编排层（或 `/goal` 类自动化指令）消费。这不需要现在实现，但架构上留个口。

### 6. 跨会话 HEAD 哈希校验

`current.md` 记录了交接时的分支和状态，但没有 HEAD commit hash。下一个会话的 `nk-work` Orient 步骤可以核对分支名，但无法检测「上次交接后有人（人类或其他 Agent）在同一分支上又提交了几个 commit」。建议在 `conventions/current-md.md` 的模板中加一个 `HEAD: <short-hash>` 字段，`nk-work` 的 Orient 步骤用 `git rev-parse --short HEAD` 比对——不一致时不阻断，但在开始工作前向用户报告「检测到 N 个未记录的中间提交」。

### 7. Matt 的 Context Pointer 按需加载原则

Matt 在 `/writing-for-agents` 中明确了一个重要的 prompt 工程原则：**不要把参考材料内联到 skill 正文里，用 Context Pointer 让 Agent 按需加载**。NexusKit 已经通过 `references/` 目录做到了这一点（而且做得比 Matt 自己的 skill 更彻底），但这个设计原则本身没有显式文档化。如果未来有人为体系贡献新技能，他需要知道「为什么 SKILL.md 只放流程框架、把实质规则下沉到 references/」。建议在 RFC 或打包文档中补一段 Matt 的原话概要：**SKILL.md 是 executive controller，不是 encyclopedia；参考材料通过 Context Pointer 按需注入，不内联**。

### 8. CE 的 `plugin.json` + 多 host converter 打包范式

CE 的打包体系是目前最成熟的多客户端分发方案：一个 `plugin.json` 根清单 + 10 个 host-specific 目录（`hosts/antigravity/`、`hosts/codex/`、`hosts/cline/` 等）+ 9 个自动 converter 脚本，配合 `claude plugin validate --strict` CI 验证。打包 NexusKit 时不需要抄这个规模，但它的几个关键决策值得参考：
- **`conventions/` 共享方式**：CE 的做法是在每个 host converter 中把共享规则直接内联到生成的 skill 文件里（牺牲 DRY 换取自包含）。NexusKit 的 `../conventions/` 相对路径在插件生态中会断裂——这是 RFC 第九章的开放问题 3，也是打包时必须解决的第一个结构问题。
- **字节上限的 ratchet 机制**：CE 的 `codex-skill-prompt-budget.test.ts` 维护一个 `OVER_BUDGET` 名单（当前只剩 `ce-debug` 和 `ce-explain`），新 skill 一律禁止超标，老 skill 瘦身后从名单移除、且永不允许回到名单上。这个 ratchet（只许减不许增）比单纯设上限更有工程味。
