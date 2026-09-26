# AGENTS.md

本仓库是 NexusKit（`nk-*`）技能体系的开发目录。技能与共享约定位于 [`skills/`](skills/)（`skills/nk-*` + `skills/conventions/`）。

**加载模型：本仓库是半成品工作区，不直接作为技能加载源。** 各客户端通过发布形态消费成品——Kimi Code 插件、Codex 插件、`npx skills add`（见 [`README.md`](README.md) 安装节）。开发期想让客户端立即试用未发布改动时，手动重装本地插件（`/plugins install D:\codex_project\nexuskit`）或在 `~/.agents/skills/` 建临时 junction（用 PowerShell `New-Item -ItemType Junction`；删除用 `[IO.Directory]::Delete()`，勿用 `Remove-Item -Recurse`）。

## 维护者入口

- **[`docs/current.md`](docs/current.md)**：仓库当前状态、验证结果、下一步——新会话先读它。
- **[`docs/solutions/`](docs/solutions/)**：经验与决策库（长期资产）；沉淀与审计规则见 `skills/conventions/solution-schema.md`。
- **[`docs/skill-sources.md`](docs/skill-sources.md)**：每个技能的上游来源与取舍理由（维护者向；执行技能的 Agent 不需要读）。
- **[`conventions/`](skills/conventions/)**：全部共享约定（提交节奏、产物生命周期、术语、plan 格式等）。技能正文引用这里的规则，不重述。
- **[`docs/ideation/nexuskit-framework-ideation.md`](docs/ideation/nexuskit-framework-ideation.md)**：体系设计 RFC（D1–D10 设计决定、阶段路线图）。
- **[`README.md`](README.md)**：按场景选用技能的路由表。

## 改动规则

- 修改任何 `skills/nk-*/` 或 `skills/conventions/` 后，运行 `python tests/run_checks.py`，五项检查（链接、引用、字节上限、提示词副本清单、frontmatter 严格 YAML 与 name/目录同名）必须全绿；CI 会在推送时复跑。
- **新增技能目录不建加载链接**：发布模型下各客户端消费的是安装快照（见头部加载模型），仓库内改动不直接影响线上；需要即时试用时按头部说明重装本地插件或建临时 junction。
- 提交节奏遵循 [`conventions/commit-cadence.md`](skills/conventions/commit-cadence.md)：一个经过验证的变化一次提交，纯状态改动不单独提交。
- `docs/skill-sources.md` 随技能的新建/修改同步更新；技能的 `SKILL.md` 正文不写来源备注。
