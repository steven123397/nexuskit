# 当前状态

- **所在分支**：`main`（仓库已迁至 `D:\codex_project
exuskit`）
- **版本/里程碑**：P6 已完成——17 个技能就位（沿用既定模式：子代理编写、Kimi Code 评审后分技能提交；`nk-wait-what` 源文仅 6 行，由 Kimi Code 直接编写）
- **已具备能力**：
  - 共享约定 10 份：[`conventions/`](../conventions/)（新增 `issue-writing.md`：Issue 格式四原则，吸收 Matt AGENT-BRIEF）。
  - 执行闭环：`nk-commit`、`nk-work`、`nk-handoff`。
  - 规划链：`nk-ideate` → `nk-brainstorm` → `nk-plan`。
  - 知识库闭环：`nk-close`、`nk-compound`（沉淀 + 审计双模式）。
  - 质量链：`nk-debug`、`nk-simplify`、`nk-review`。
  - 其余：`nk-wayfinder`（决策地图，GitHub Issues 承载）、`nk-to-issue`（核实分析后落档）、`nk-wizard`（手动操作引导脚本）、`nk-wait-what`（重新对齐）。
  - 设计变更：`nk-to-tasks` 取消（长期挂起由 nk-close 覆盖，并行认领按 YAGNI 不建）——用户 2026-09-26 拍板。
  - 工程保障：`tests/run_checks.py` 四项机械检查（链接完整性 / K-R 引用解析 / SKILL.md 8000 字节上限带 ratchet / 重复提示词清单锁定）+ GitHub Actions CI（ubuntu + windows）。
  - 来源记录集中化：技能来源/取舍全部移入 [`docs/skill-sources.md`](skill-sources.md)（SKILL.md 正文不再带脚注），仓库根新增 `AGENTS.md` 维护者入口。
- **验证结果**：
  - `python tests/run_checks.py` 四项全绿；CI 已上线。
  - 全仓 Markdown 相对链接 0 失效；SKILL.md 全部 ≤ 8000 字节。
  - 未验证：真实项目中的端到端使用——下一阶段正是这件事。

## 阻断与已知缺口

- `learnings-researcher` 等 10 组重复提示词已加分叉声明并锁定集合成员（tests/prompt-copies.txt）；是否合并共享留待打包阶段决定。
- 无其他阻断项。

## 下一步

按用户 2026-09-26 拍板的顺序推进（迁移验收往后移，先打包再实测）：

- [x] **迁仓库（2026-09-26 完成）**：仓库已在 `D:\codex_project\nexuskit`，GitHub 已改名 `nexuskit-skills`；加载目录 `~/.agents/skills` 只含 18 个 junction（`nk-*`（含 nk-ask-ljq）、`conventions`），由 PowerShell `New-Item -ItemType Junction` 建立。经验：跨盘 `mv` 是 copy+delete，源目录被本会话占用删不掉，清空内容后建 junction 即可；Git Bash 调 cmd 的 `mklink /J` 会被 MSYS 路径转换弄坏，用 PowerShell。
- [x] **P6 已完成**：`nk-init`（首次启用初始化）+ `nk-ask-ljq`（场景路由器；曾定名无前缀的 ask-ljq，后统一回 nk- 前缀，个人元素留在名字里）
- [ ] **打包 v0.1.0**：三形态——Claude plugin、Kimi plugin（格式待查）、npx 安装器（仿 Matt skills-cli；conventions/ 随安装一起复制解决共享问题）
- [ ] **迁移与验收**：paper-30min 从 CE 迁移到 NexusKit，首跑 nk-init；按 RFC 第八章先写迁移方案（产物处理、指令文档更新、CE 停用或并存、验收场景、迁移前打 tag 可回退）

## 阶段总览

| 阶段 | 内容 | 完成标志 | 状态 |
| :-- | :-- | :-- | :-- |
| **P0** | 共享约定 | 6 份约定评审通过 | **已完成** |
| **P1** | `nk-work`、`nk-commit`、`nk-handoff` | 单元验证与成稿评审通过；开始在本仓库自用 | **已完成** |
| **P2** | `nk-brainstorm`、`nk-plan`、`nk-ideate` | 单元验证与成稿评审通过 | **已完成** |
| **P3** | `nk-close`、`nk-compound` | 单元验证与成稿评审通过 | **已完成** |
| **P4** | `nk-debug`、`nk-review`、`nk-simplify` | 单元验证与成稿评审通过 | **已完成** |
| **P5** | `nk-wayfinder`、`nk-to-issue`、`nk-wizard`、`nk-wait-what` | 单元验证与成稿评审通过 | **已完成** |
| **P6** | `nk-init`、`nk-ask-ljq` | 单元验证与成稿评审通过 | **已完成** |
| **迁移与验收** | paper-30min 从 CE 迁移到 NexusKit，集中验收 | 产物整理、指令对齐、验收场景通过 | 待启动 |
| **打包** | 仿照 CE 结构做多 Agent 插件 | 各客户端可安装 | 待启动 |
