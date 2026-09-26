# AGENTS.md

本仓库是 NexusKit（`nk-*`）技能体系的开发目录。技能与共享约定位于 [`skills/`](skills/)（`skills/nk-*` + `skills/conventions/`）；各客户端通过 `~/.agents/skills/` 下指向 `skills/` 内各目录的 junction 加载。

## 维护者入口

- **[`docs/current.md`](docs/current.md)**：仓库当前状态、验证结果、下一步——新会话先读它。
- **[`docs/skill-sources.md`](docs/skill-sources.md)**：每个技能的上游来源与取舍理由（维护者向；执行技能的 Agent 不需要读）。
- **[`conventions/`](skills/conventions/)**：全部共享约定（提交节奏、产物生命周期、术语、plan 格式等）。技能正文引用这里的规则，不重述。
- **[`docs/ideation/nexuskit-framework-ideation.md`](docs/ideation/nexuskit-framework-ideation.md)**：体系设计 RFC（D1–D10 设计决定、阶段路线图）。
- **[`README.md`](README.md)**：按场景选用技能的路由表。

## 改动规则

- 修改任何 `skills/nk-*/` 或 `skills/conventions/` 后，运行 `python tests/run_checks.py`，五项检查（链接、引用、字节上限、提示词副本清单、frontmatter 严格 YAML 与 name/目录同名）必须全绿；CI 会在推送时复跑。
- **新增技能目录后必须重建加载链接**：在 `~/.agents/skills/` 下建同名 junction 指向本仓库 `skills/<name>`，否则各客户端加载不到。junction 操作用 PowerShell（`New-Item -ItemType Junction`）；Git Bash 调 cmd 的 `mklink /J` 会被 MSYS 路径转换弄坏；删除 junction 用 `[IO.Directory]::Delete()`，勿用 `Remove-Item -Recurse`（旧版 PowerShell 会连目标内容一起删）。
- 提交节奏遵循 [`conventions/commit-cadence.md`](skills/conventions/commit-cadence.md)：一个经过验证的变化一次提交，纯状态改动不单独提交。
- `docs/skill-sources.md` 随技能的新建/修改同步更新；技能的 `SKILL.md` 正文不写来源备注。
