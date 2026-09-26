# 当前状态

- **所在分支**：`main`（仓库在 `D:\codex_project\nexuskit`）
- **版本/里程碑**：P6 已完成；2026-09-26 完成**布局迁移方案 (a)**——技能与共享约定移入 `skills/`（`skills/nk-*` + `skills/conventions/`），SKILL.md 的 `../conventions/` 引用零改动，三种形态（仓库内 / junction 加载 / 未来插件）路径几何全等。
- **已具备能力**：
  - 共享约定 9 份：[`skills/conventions/`](../skills/conventions/)（含 `issue-writing.md`：Issue 格式四原则，吸收 Matt AGENT-BRIEF）。
  - 执行闭环：`nk-commit`、`nk-work`、`nk-handoff`。
  - 规划链：`nk-ideate` → `nk-brainstorm` → `nk-plan`。
  - 知识库闭环：`nk-close`、`nk-compound`（沉淀 + 审计双模式）。
  - 质量链：`nk-debug`、`nk-simplify`、`nk-review`。
  - 其余：`nk-wayfinder`（决策地图，GitHub Issues 承载）、`nk-to-issue`（核实分析后落档）、`nk-wizard`（手动操作引导脚本）、`nk-wait-what`（重新对齐）。
  - 工程保障：`tests/run_checks.py` 四项机械检查（链接完整性 / K-R 引用解析 / SKILL.md 8000 字节上限带 ratchet / 重复提示词清单锁定）+ GitHub Actions CI（ubuntu + windows）。
  - 来源记录集中化：技能来源/取舍全部移入 [`docs/skill-sources.md`](skill-sources.md)（SKILL.md 正文不再带脚注），仓库根 `AGENTS.md` 为维护者入口。
- **验证结果**：
  - `python tests/run_checks.py` 四项全绿；CI 已上线。
  - 布局迁移后验证：全仓 Markdown 相对链接 0 失效；`~/.agents/skills` 18 个 junction 已重指向 `skills/` 内目录，`nk-work/../conventions/` 经 junction 解析验证通过。
  - 未验证：真实项目中的端到端使用——各客户端对新布局的实际加载行为待实测确认。

## 阻断与已知缺口

- 10 组重复子代理提示词（分叉声明 + 清单锁定）的终局方案：已落档 Issue #1，打包前必须先逐组评审分叉深度再定方案 B/C。
- 中文 description 触发可靠性（RFC 开放问题 1）：推迟到 v1.1.0，走"实弹观察 + 迷你对照实验兜底"，已落档 Issue #2。

## 下一步

按用户 2026-09-26 拍板的顺序推进（迁移验收往后移，先打包再实测）：

- [x] **迁仓库（2026-09-26 完成）**：仓库已在 `D:\codex_project\nexuskit`，GitHub 已改名 `nexuskit-skills`；`~/.agents/skills` 只含 18 个 junction，由 PowerShell `New-Item -ItemType Junction` 建立（Git Bash 调 cmd 的 `mklink /J` 会被 MSYS 路径转换弄坏，用 PowerShell）。
- [x] **布局迁移方案 (a)（2026-09-26 完成）**：`nk-*` 与 `conventions/` 移入 `skills/`，junction 重指向并验证；run_checks 路径前缀同步更新。
- [ ] **打包 v0.1.0**：三形态——Claude plugin、Kimi plugin（格式待查）、npx 安装器（仿 Matt skills-cli；conventions/ 随安装一起复制解决共享问题）。前置：Issue #1（提示词副本终局）、许可证归属声明（两上游均 MIT）、公开前个人信息清扫。
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
