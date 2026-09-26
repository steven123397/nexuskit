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
  - 工程保障：`tests/run_checks.py` 五项机械检查（链接完整性 / K-R 引用解析 / SKILL.md 8000 字节上限带 ratchet / 重复提示词清单锁定 / frontmatter 严格 YAML 且 name 与目录同名）+ GitHub Actions CI（ubuntu + windows）。
  - 来源记录集中化：技能来源/取舍全部移入 [`docs/skill-sources.md`](skill-sources.md)（SKILL.md 正文不再带脚注），仓库根 `AGENTS.md` 为维护者入口；上游 MIT 归属声明在 [`NOTICE`](../NOTICE)。
- **验证结果**：
  - `python tests/run_checks.py` 五项全绿；CI 已上线。
  - 布局迁移后验证：全仓 Markdown 相对链接 0 失效；`~/.agents/skills` 18 个 junction 已重指向 `skills/` 内目录，`nk-work/../conventions/` 经 junction 解析验证通过。
  - 打包验证（2026-09-26）：`npx skills@1.5.23 add` 在临时目录完整实装 18 个目录（17 技能 + conventions）零跳过，`nk-commit/../conventions/` 引用解析通过。实装中抓到并修复 4 个技能 description 未加引号导致严格 YAML 解析失败的问题（nk-close/nk-commit/nk-handoff/nk-work）。
  - 已验证（2026-09-26）：Kimi 插件本地路径安装（`/plugins install D:\codex_project\nexuskit`）成功，`installed.json` 记录 enabled。GitHub URL 安装的下载与解压正常（非网络问题），失败在最后一步临时目录 rename（EPERM，疑似 Defender 对带 Mark-of-the-Web 文件的瞬态锁）——属 Kimi 安装器应加重试的健壮性问题，本地路径为可靠兜底。
  - 未验证：Codex 插件实装；真实项目中的端到端使用。

## 阻断与已知缺口

- 10 组重复子代理提示词（分叉声明 + 清单锁定）：Issue #1，2026-09-26 拍板**推迟到 v0.1.0 之后**——副本自包含不影响运转，真实触发时机是"首次需要跨副本同步修订"时。
- 中文 description 触发可靠性（RFC 开放问题 1）：推迟到 v1.1.0，走"实弹观察 + 迷你对照实验兜底"，已落档 Issue #2。

## 下一步

按用户 2026-09-26 拍板的顺序推进（迁移验收往后移，先打包再实测）：

- [x] **迁仓库（2026-09-26 完成）**：仓库已在 `D:\codex_project\nexuskit`，GitHub 已改名 `nexuskit-skills`；`~/.agents/skills` 只含 18 个 junction，由 PowerShell `New-Item -ItemType Junction` 建立（Git Bash 调 cmd 的 `mklink /J` 会被 MSYS 路径转换弄坏，用 PowerShell）。
- [x] **布局迁移方案 (a)（2026-09-26 完成）**：`nk-*` 与 `conventions/` 移入 `skills/`，junction 重指向并验证；run_checks 路径前缀同步更新。
- [x] **打包 v0.1.0 清单就位（2026-09-26）**：用户拍板第一轮形态改为 **Codex 插件 + Kimi 插件 + npx（skills CLI）**，Claude 插件不做。已落地：`kimi.plugin.json`（根，官方格式）、`.codex-plugin/plugin.json`（仿 CE 样本）、`skills/conventions/SKILL.md`（让共享约定可被 skills CLI 发现安装，disable-model-invocation 防误触发）、`NOTICE`（两上游 MIT 归属）、README 安装节与公开前路径清扫。npx 形态已实装验证通过。
- [ ] **打包收尾**：推送发布 v0.1.0（打 tag）；Kimi `/plugins install` 与 Codex 实装验证。
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
