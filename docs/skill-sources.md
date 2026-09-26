# 技能来源与差异记录 (Skill Sources)

> 维护者向文档：每个技能改写自哪些上游、做了什么取舍、为什么。执行技能的 Agent 不需要读它；修改技能或考虑吸收上游更新时来这里查。由 `AGENTS.md` 指向本文件。

---

## nk-brainstorm

主要参考：CE `ce-brainstorm` (2026-09)、Matt `domain-modeling`（术语即时质疑、用具体场景压力测试概念边界）、Matt `to-spec`（上下文已充分时不访谈、直接综合）。
与 CE 的主要差异及原因：
* 术语在对话中敲定即写入 `CONCEPTS.md`，文件不存在时新建：CE 只在写完 plan 后、且文件已存在时才补录，规划期敲定的术语因此流失。
* 互不依赖的问题合并为一轮提问（最多 3 个）：CE 规定每轮一问，交互轮数过多；合并规则见 `../conventions/decision-autonomy.md`。
* 只输出 Markdown；可视化探针改为对话内的 mermaid/文字草图，不启动本地网页服务。
* 去掉跨模型提权、Compound Packs、Slack 调研、Bake-off、CE 配置层与 `lfg`/pipeline 调用模式：本体系不使用这些基础设施。
* 指向 `ce-pov`、`ce-prototype`、`ce-doc-review`、`ce-proof` 等技能的分流改为内联原则或交接选项：NexusKit 没有这些技能。
* 不提交，会话结束的提交交给 `nk-handoff`：与提交节奏规则一致。

## nk-close

主要参考：NexusKit 共享约定 [`../conventions/artifact-lifecycle.md`](../conventions/artifact-lifecycle.md)（本技能为其第五章的可执行展开）
关键设计决定：
* 未消费发想记录与推迟 plan 逐项询问用户、每轮最多 3 个——用户 2026-09-25 拍板；无人值守时采用推荐默认并在 `docs/current.md` 登记 `[待确认]`。
* 在六步法前增加第 0 步前置检查（单元提交核对、工作区清点、验证证据核对）：证据缺失时警告用户而非放行，依据 commit-cadence 第三节的通用纪律补入。
* 提炼的判断细则下沉到 `references/harvest.md`，SKILL.md 保持聚焦"怎么做"。
* `docs/reviews/` 目录不存在时跳过并说明（项目可能尚未运行过 `nk-review`）。
* 收尾提交显式限定本技能涉及的文件路径：收尾时工作区可能仍有后续版本的半成品，防止混入提交。
* 提交信息风格遵循项目惯例而不写死格式：与 nk-commit、nk-handoff 的口径一致。

## nk-commit

主要参考：CE `ce-commit` (2026-09)、NexusKit 共享约定 [`../conventions/commit-cadence.md`](../conventions/commit-cadence.md)
与 CE 的主要差异及原因：
* 按"交付变化 / 状态记录"而非文件类型判定提交类型：文档本身也可能是交付物（例如本仓库的技能文件）。
* 不在默认分支上自动建分支：个人项目常直接在 main 上工作，分支策略交给项目工作流文档。
* 验证证据写进提交正文：证据随提交永久保存，不需要额外文档。

## nk-compound

主要参考：CE `ce-compound` / `ce-compound-refresh` (2026-09)、NexusKit 共享约定
与 CE 的主要差异及原因：
* refresh 并入为审计模式而非独立技能：同一知识库的写入与维护收拢在一个入口，`refresh` 参数切换。
* scripts/ 整体删除：两份校验脚本转写为 `references/frontmatter-checklist.md` 与 `references/claims-checklist.md` 的人工核对清单；session-history 脚本组删除，改用当前会话上下文 + `git log` 定位刚解决的问题，依赖脚本的 session-historian 提示词随之删除。
* CE 基础设施删除：`docs_root` / `.compound-engineering` 配置层、Compound Packs、Proof 发布、Slack、auto-memory 与浏览器相关步骤。
* 模式裁剪：去掉 mode/depth token 体系（interactive/non-interactive、full/lightweight），沉淀走单一流程；无人值守场景由 `../conventions/decision-autonomy.md` 统一覆盖。
* 提交纪律改为 commit-cadence R4 第 4 条（优先随代码提交、未推送则限定路径 amend、已推送则留工作区），而非 CE 的独立文档提交与建分支。
* 可见性检查并入首运行职责：按 artifact-lifecycle 第二章补 `AGENTS.md` 指引，而非每次运行单独征询。
* 术语表规则归 `../conventions/concepts-vocabulary.md`：本技能沉淀模式只做 Add/Refine，Fold/Retire/Scrub 与整库初建归审计模式。

## nk-debug

主要参考：CE `ce-debug` (2026-09)、Matt `diagnosing-bugs`、NexusKit 共享约定
与上游的主要差异及原因：
* 复现优先（Matt 的 feedback loop）前置为流程灵魂：CE 把复现放在调查阶段的一个小节，本技能将"没有红得起来的复现就不得进入假设阶段"立为硬关卡。
* 删除 CE 的编排与平台层：pipeline / return-to-caller 模式（mode 令牌、JSON 返回契约）、PR 路由、分支自动创建、branding、Artifact Root / `docs_root` 配置解析——NexusKit 没有流水线编排层，产物位置由约定固定，分支与 PR 策略归项目，提交统一走 nk-commit + commit-cadence。
* 删除 post-fix-handoff 的修复后精简/审查编排：审查发生在版本层面（nk-review）；其通用残值（尾部改动后复跑回归、遗留发现落地记录）并入 references/fix.md 与收尾步骤。
* issue-of-record 规则简化：无法本轮定位的疑难缺陷本来就要按 artifact-lifecycle 转 Issue，无需禁令。
* Matt 的 `hitl-loop.template.sh` 与 `agents/openai.yaml` 删除：体系纯 Markdown 约定驱动、客户端中立；人工在环复现转写为 references/reproduction.md 第十种回路。
* defense-in-depth.md 保留为独立 reference：35 行的通用分层防御模式，触发条件清晰，便于按需加载。

## nk-handoff

主要参考：CE `ce-handoff` (2026-09)、Matt `handoff`、NexusKit 共享约定 [`../conventions/current-md.md`](../conventions/current-md.md)
与 CE 的主要差异及原因：
* 交接载体是仓库内单例 `docs/current.md`，而不是临时目录中的独立文件：不堆积、不丢失，新会话经 `AGENTS.md` 自动找到。
* 没有 resume 模式：会话开始时的核对由 `nk-work` 第 0 步负责。
* 交接时优先 amend 进本会话未推送的提交：尽量不产生纯文档提交。

## nk-ideate

主要参考：CE `ce-ideate` (2026-09)、NexusKit 共享约定 [`../conventions/`](../conventions/)
与 CE 的主要差异及原因：
* 只输出 Markdown，去掉 HTML 渲染、浏览器打开与 Proof 发布：用户选择统一使用 Markdown，发想记录由人和 Agent 都直接读文件。
* 去掉 `.compound-engineering` 配置层与 `docs_root`：NexusKit 不使用 CE 配置文件，产物位置固定在 `docs/ideation/`。
* 去掉 Slack 调研：用户不使用 Slack 作为信息来源。
* 临时目录改为不依赖 bash 的中立描述：技能需要在 PowerShell 等多种 shell 与客户端中运行。
* 提问改为批量规则（每轮最多 3 个）：遵循 NexusKit 的决策自主约定；"累计超过 3 个问题说明选错流程"的原则保留。
* 下一步改为 `nk-brainstorm` / `nk-handoff`，提交遵循 NexusKit 提交节奏：发想记录不单独提交。
* 子代理编队规模、六视角、依据核查、tactical 与 `go deep` 变体保持 CE 原样：用户选择质量优先。

## nk-plan

主要参考：CE `ce-plan`（2026-09，含 `references/agents/` 研究员与深化视角）、CE `ce-doc-review` 的审阅视角（并入写后自检）、Matt `codebase-design`（Design It Twice、依赖分类）。
与 CE 的主要差异及原因：
* 只输出 Markdown：`nk-work` 按标题定位 plan 章节，单一格式最稳；HTML 渲染规则和预览脚本不再需要。
* 不调用 `ce-doc-review`，改为写后自检：保留其连贯性、可行性、范围、安全、设计、产品、对抗性视角的检查要点，由主会话执行，避免依赖一个单独的审阅技能和强制多代理审查。
* 去掉模型提权、跨模型调度脚本、Compound Packs、Slack 调研、`docs_root` 等 CE 配置层与流水线模式：这些依赖 CE 专有的基础设施或编排方，本体系不使用。研究员与深化视角的子代理规模保持 CE 原样。
* Bake-off 改为设计对比（取自 Matt 的 Design It Twice）：不依赖单独的竞赛技能，同样用于后果重大、难以推翻的"怎么做"。
* 提问从"每轮一个问题"改为批量提问：按 `decision-autonomy.md` 减少一问一答的往返。
* 规划中即时写入术语，而不是只在术语表已存在时补漏：让规划期诞生的术语不流失。
* 收尾菜单改为 NexusKit 流程：推荐结束会话交接、新会话用 `nk-work` 接手，规划产出与交接合成一次提交；去掉 `/goal`、原型和浏览器打开选项。

## nk-review

主要参考：CE `ce-code-review`（2026-09，personas 与复核机制）、Matt `code-review`（固定点 diff、早停、意图/规范双轴思想）、NexusKit 共享约定
与 CE 的主要差异及原因：
* 产出从临时运行目录与报告改为目标仓库 `docs/reviews/` 的状态化条目：审查记录是本体系的短期生命周期产物，由 `nk-close` 消费。
* 删除全部脚本（范围信号、findings 机制、跨模型调度、运行日志等）：规则性内容转写为 references 中的 Markdown 条款，编排与跨模型对抗审查不内置（可一句话建议用另一个客户端复核）。
* 删除 mode:agent JSON 输出、本地修复（apply）与 autofix 路由字段：本技能只报告不修复，修复归 `nk-work`，分流按严重级别与条目内容判断。
* 深度闸门（lite/focused/full）简化为范围信号 + 后果判断：个人项目规模下三档编排的收益不抵复杂度；200 行阈值与静默放行守卫规则保留。
* PR 路径降级为可选：保留只读取数与 previous-comments persona 的适用条件，不切换分支。
* reviewer 返回紧凑 JSON、由主会话渲染条目：persona 提示词保持英文原文，条目格式集中在 entry-format.md 单处维护。

## nk-simplify

主要参考：CE `ce-simplify-code` (2026-09)、NexusKit 共享约定 [`../conventions/commit-cadence.md`](../conventions/commit-cadence.md)
与 CE 的主要差异及原因：
* 删除 CE 的平台编排细节（受限派发、代理生命周期、模型档位、权限模式参数、任务跟踪提示、阻塞提问工具的探测规则）：NexusKit 客户端中立，只保留“支持子代理则派发、否则内联”的一条规则。
* 三视角从“固定并行三个”改为“按信号选用、默认全跑”：NexusKit 以单会话串行为主，小范围改动不必机械跑满三个视角。
* 删除 `session-settled:` 结构钉与计划路径传参机制：NexusKit 的等价物是 `conventions/settled-decisions.md`，直接引用共享约定。
* 验证与提交并入 NexusKit 提交节奏（R1 验证证据入提交说明），CE 原文只要求跑检查、不管提交。
* 增加与 `nk-compound`、`nk-review` 的衔接一句话：精简在体系内的位置是实现之后、版本审查之前。

## nk-to-issue

主要参考：Matt `triage`（核实与 brief 部分）、NexusKit 共享约定 [`../conventions/issue-writing.md`](../conventions/issue-writing.md)
与 Matt `triage` 的主要差异及原因：
* **不是状态机形态**：Matt 围绕 maintainer 的 labels/buckets/state roles（needs-triage、ready-for-agent 等）组织批量分诊；NexusKit 是个人项目、用户自己就是 maintainer，没有"分诊队列"，本技能只处理单条"开发中冒出的发现"，状态流转交给 Issue 平台自身。
* 删除 external PR surface、AI disclaimer 与 setup 配置探测：个人项目无外部贡献者分诊需求，产物位置由 artifact-lifecycle 约定固定。
* 删除 grilling 循环：体系已移除 grill；需求澄清按 decision-autonomy 的批量提问规则进行。
* 保留第 1 步的查重与冗余检查、第 3 步"按步骤复现后再落档"，以及 triage notes 的"已确认事实/还缺什么"二分——后者转写为 issue-writing 约定中 Evidence 小节的核实结论与缺口写法。
* `.out-of-scope/` 知识库未引入：其"曾被否决的请求"在本体系中的对应物是 `docs/ideation/` 未选中方向、已关闭 Issue 与 `docs/solutions/`（见第 3 步）。

## nk-wait-what

主要参考：Matt `wait-what`。差异：术语表从 `CONTEXT.md` 换成 `CONCEPTS.md`；ASD-STE100 的硬性要求放宽为"简单直接、没有歧义"（中文协作场景）。

## nk-wayfinder

主要参考：Matt `wayfinder`（2026-08 本地备份，128 行全文）。
与 Matt 版的主要差异及原因：
* Tracker 固定为 GitHub Issues（`gh` CLI），label 缺失时用 `gh label create` 创建；删除 tracker 配置探测与安装引导步骤：体系不需要多 tracker 抽象。
* 无远端时明确不可用并建议改用 `nk-plan`/`nk-brainstorm`：wayfinder 的价值在 tracker 的查询与可视化，不发明本地降级格式。
* `/grilling` → 按 `decision-autonomy.md` 提问规则进行 HITL 对话：体系有意移除了 grill 技能。
* `/domain-modeling` → 术语即时写入 `CONCEPTS.md`，规则在 `concepts-vocabulary.md`。
* `/research` subagent → 中性写法：支持子代理则派发，否则主会话内联完成；去掉一次性 research branch 约定（客户端无关性，findings 直接从 ticket 链接）。
* `/prototype` → 一句话内联：构建廉价粗糙的具体产物辅助讨论，不依赖技能。
* 删除 `agents/openai.yaml`：客户端专有配置。
* 新增与 `nk-compound`、`nk-handoff`、`nk-plan`/`nk-work` 的衔接说明，以及无人值守下 HITL ticket 的登记规则。

## nk-wizard

主要参考：Matt `wizard`（2026-08 备份，`skills/wizard/`）
与上游的差异及原因：
* 正文改写为中文并套用 NexusKit 体例（执行步骤编号、"Done when" 判据原义保留）；上游描述段精简为适用场景说明。
* `template.sh` 逐字节保留为 `assets/template.sh`，不翻译不精简：上游明确 library 部分永不手改，一致性正是重点；该文件是技能交付物的模板资产，不是技能自身的自动化设施，不违反体系"纯 Markdown 无脚本"原则。
* 删除 `agents/openai.yaml`：客户端专用配置，NexusKit 客户端中立。
* 新增两处衔接：Windows 下用 Git Bash 运行的说明；入库例外明确指向 commit-cadence R1，并提示用 `nk-compound` 沉淀过程中发现的非显性知识。

## nk-init

主要参考：Matt `setup-matt-pocock-skills`（2026-08 备份；仅借鉴骨架）

关键设计决定：
* 保留"探测 → 展示确认 → 幂等写入"的三段 explore-first 骨架与"探测已确定答案的不提问"；不移植 Matt 专有的 issue tracker 选择、triage label 词汇表、CONTEXT.md/ADR 布局等配置面——那些是 Matt 体系的配置，与 NexusKit 产物矩阵无关。
* 写入对象是 NexusKit 自有产物：全局指令文件的知识入口指引（artifact-lifecycle 第二章）、`docs/current.md`、无远端时的 `docs/backlog.md` 降级。
* 负向清单写进流程：不建 `CONCEPTS.md`（由第一个合格词条创建）、不建空目录（git 不跟踪空目录）。
* 带 `disable-model-invocation: true`（手动技能）；提交遵循 commit-cadence。

## nk-ask-ljq

主要参考：Matt `ask-matt`（2026-08 备份）

关键设计决定：
* 名字含作者缩写 ljq（个人元素）；曾定名无前缀的 `ask-ljq`，后统一回 `nk-` 前缀保持命名一致。
* Matt 的"main flow + on-ramps"单主线结构改为"工具箱宣言 → 参考路径 → 按场景入口"：落实 D1（工具箱不是流水线），路由而不规训，明说每步可单独用、可跳过、可从中间进入。
* 保留"问我就行"的作者口吻与语境卫生建议（`docs/current.md` 接手、Smart Zone <100k/理想 <30k、单元边界交接）。
* 新增 R1–R6 提交节奏一句话版（细节路由给 `nk-commit`）；删去 phase boundaries 决策树、prototype/triage/vocabulary layer 等 NexusKit 无对应物的内容。

## nk-work

主要参考：CE `ce-work` (2026-09)、Matt `tdd` / `implement`、NexusKit 共享约定

与 CE 的主要差异及原因：
* 未移植调度脚本、跨模型执行与默认并行波次：本体系是一个会话串行推进、主对话提交，不需要这层编排。
* 进度以带 U-ID 的提交为准，不为记进度修改 plan：plan 的每次改动都应是有意义的范围或决策变化。
* 一个会话默认一个单元、可顺延：避免小单元被迫逐个交接、产生多余的交接提交。
* 接手时"一致则继续，不一致才停"：`current.md` 是本仓库的单例文件，不像 CE 的交接文档那样来源不可信。
* 脏文件分两类：`current.md` 登记的半成品由本会话接管，其余一律不暂存。
* 不设代码审查关卡：审查发生在版本层面，由 `nk-review` 负责。
* 测试 seam 由 Agent 自选（改写 Matt `tdd` 的"先与用户确认"）：测试结构属于自主决断区。
