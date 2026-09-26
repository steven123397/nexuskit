---
name: nk-wizard
description: Generate an interactive bash wizard that walks a human through manual-only procedures — setup, provisioning infrastructure, configuring credentials or CI secrets, one-time migrations or cutovers, guiding manual operations. Not for steps the agent can execute itself. 生成引导脚本、交互式向导、配置 secrets、provisioning、一次性迁移、引导手动操作。
---

# /nk-wizard

> **路径解析说明：** 本文件中引用的参考文件（如 `assets/`、`../conventions/`）均相对于本技能所在目录解析，不在目标代码仓库中查找。

生成一个交互式 bash wizard，逐步引导人完成只有人能执行的手动流程——这类流程手动做很繁琐，每次重新向 AI 解释一遍也很繁琐。适用场景：provisioning 基础设施、配置凭据或 CI secrets、走查不熟悉的第三方 dashboard、一次性 migration 或 cutover。Agent 自己就能执行的步骤，不要用它。

Wizard 会打开每个 URL、准确说明该点什么该复制什么、捕获这些值并写到该去的地方（`.env`、GitHub secrets）、逐阶段确认并显示剩余进度。Windows 下用 Git Bash 运行（template 已含跨平台 URL 打开）。

出色的 UX 已由 [assets/template.sh](assets/template.sh) 解决：逐阶段进度、confirmation gates、跨平台 URL 打开（含 WSL）、隐藏的 secret 输入、幂等的 `.env` upsert、`gh secret`/`gh variable` 写入、收尾 summary。**你的工作只是确定流程范围并编写各个 stage。** `STAGES` 标记之上的 library 在每个 wizard 中都完全相同——这种一致性正是重点，永远不要手动编辑它。

Wizard 默认是一次性产物：为单次运行而构建，保存到 scratch 或 `scripts/` 路径，任务完成后删除，不进入版本生命周期。只有当用户想要一条应留在仓库中的可重复 setup 路径时才入库——入库按 [`../conventions/commit-cadence.md`](../conventions/commit-cadence.md) R1 随验证证据正常提交，并从 README 链接过去。

## 执行步骤

### 1. 界定流程范围 (Scope the procedure)

梳理出人必须执行的每一个手动步骤，以及沿途捕获的每一个值。先读仓库——不要凭空发问：

- 对于 setup：`.env`、`.env.example`、`.env.*`、`README`、`docker-compose*`、framework config，以及 `.github/workflows/*`（每一处 `secrets.*` / `vars.*` 引用都是 wizard 必须产出的一个值）。
- 对于 migration 或 cutover：当前状态、目标状态，以及两者之间不可逆的操作。

然后向用户展示有序的 stages 列表以及每个 stage 产出的值，并请其确认——用户可能增删或重新排序。

**Done when：** 每个 stage 都按顺序命名；对于每个捕获的值，你知道 (a) 人从哪里获取它，(b) 它写到哪里（`.env`、一个 GitHub secret、两者，或都不写——有些 stage 是纯操作），以及 (c) 它是 secret（隐藏输入）还是 public。

### 2. 映射每个 stage 的操作路径 (Map each stage's journey)

对于每个 stage，写出人遵循的精确路径：打开哪个 URL、在那里做什么、值在哪里显示、它填充哪个变量——例如 "Dashboard → Developers → API keys → Reveal test key → copy"。在你确实不知道当前 UI 或确切命令的地方，如实说明并询问用户或查阅文档——不要编造可能不存在的步骤。

**Done when：** 每个 stage 都能追溯到陌生人也能照做的具体指令。

### 3. 编写 wizard (Author)

把 `assets/template.sh` 复制到目标路径。用每个步骤一个 `stage` 替换示例 stage，按依赖顺序排列。使用 library helpers——`stage`、`say`/`step`、`open_url`、`ask`/`ask_secret`、`write_env`、`set_secret`/`set_var`、`pause`/`confirm`——并把 `TOTAL_STAGES` 设为你编写的 stage 数量。

守住 template 设定的标准：在索取某个 URL 的值之前先打开它；对任何 secret 使用 `ask_secret`；对每个持久化的值使用 `write_env`；只对 CI 确实需要的值使用 `set_secret`；在任何不可逆操作之前 `confirm`。每个 `stage` 都会清屏，只显示当前步骤——让一个 stage 只聚焦一项任务，这样人需要的内容就不会滚出视野。不要触碰标记之上的 library。

### 4. 验证与交付 (Verify and hand off)

- `bash -n <script>`；环境中有 `shellcheck` 则一并运行。
- `chmod +x <script>`。
- 不要自己端到端运行它——它会打开浏览器并阻塞在人的输入上。改为静态追踪：步骤 1 中列出的每个值都被捕获并落到它该去的位置，并且每个 `set_secret` 名称都与 CI 中的某处 `secrets.*` 引用精确匹配。
- 告诉用户如何运行它。如果它是一条可重复的 setup 路径，按上文规则入库，让下一个人运行脚本而不是询问 AI。
- 生成过程中发现值得沉淀的非显性知识（如某服务配置文档没写的坑），建议调用 `nk-compound` 记入知识库。

---

> 主要参考：Matt `wizard`（2026-08 备份，`skills/wizard/`）
>
> 与上游的差异及原因：
> * 正文改写为中文并套用 NexusKit 体例（执行步骤编号、"Done when" 判据原义保留）；上游描述段精简为适用场景说明。
> * `template.sh` 逐字节保留为 `assets/template.sh`，不翻译不精简：上游明确 library 部分永不手改，一致性正是重点；该文件是技能交付物的模板资产，不是技能自身的自动化设施，不违反体系"纯 Markdown 无脚本"原则。
> * 删除 `agents/openai.yaml`：客户端专用配置，NexusKit 客户端中立。
> * 新增两处衔接：Windows 下用 Git Bash 运行的说明；入库例外明确指向 commit-cadence R1，并提示用 `nk-compound` 沉淀过程中发现的非显性知识。
