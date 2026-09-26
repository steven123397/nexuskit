# 当前状态

- **所在分支**：`main`
- **HEAD**：`c88c105`（本文件随其后的交接提交入库）
- **版本/里程碑**：v0.1.0 已发布并收尾（2026-09-26）。版本规则（用户拍板）：v1.0.0 前均为试用版；大迭代走 minor，小迭代走 patch。
- **已具备能力**：17 个 `nk-*` 技能 + 共享约定 `skills/conventions/`（选用见 [`../README.md`](../README.md) 路由表）；三形态分发——Kimi 插件、Codex 插件、npx skills CLI（安装方式见 README）；五项机械检查 + 双平台 CI。
- **加载模型**（用户 2026-09-26 拍板）：本仓库是半成品工作区，客户端消费发布快照（插件/npx 安装）；junction 已全部拆除，仅作开发期可选的临时手段。细节见 `AGENTS.md`。
- **验证结果**：
  - `python tests/run_checks.py` 五项全绿；CI 通过。
  - 安装实装：Kimi 本地路径 ✅、Kimi GitHub URL（WSL）✅、Codex marketplace ✅、npx 临时目录 ✅。Kimi GitHub URL 在 Windows 桌面端 rename EPERM（上游安装器问题，见 `docs/solutions/architecture-decisions/2026-09-26-distribution-layout.md`）。
  - 未验证：真实项目端到端使用（paper-30min 迁移验收，v0.2.0 目标）。

## 阻断与已知缺口

- [Issue #1](https://github.com/steven123397/nexuskit-skills/issues/1)：提示词副本终局——触发时机为"首次需要跨副本同步修订"。
- [Issue #2](https://github.com/steven123397/nexuskit-skills/issues/2)：中文 description 触发可靠性（v1.1.0）。
- [Issue #3](https://github.com/steven123397/nexuskit-skills/issues/3)：增强泊车场（未拍板，随时可逐项处理）。
- Issue #4（nk-grill）、#5（分支收尾）、#6（Issue 规范）已并入下方 plan，不再单独跟踪。

## 下一步

- [ ] **新会话交互深化 plan**（用户明确：先逐项深化再动手，不直接实施）：[`docs/plans/2026-09-26-2246-feat-issue-lifecycle-branch-close-plan.md`](plans/2026-09-26-2246-feat-issue-lifecycle-branch-close-plan.md)——用 `nk-plan` 的深化快速通道（交互模式）逐章过；深化完成后用 `nk-work` 从 U1 接手。
- [ ] 深化/实施完成后关闭 Issue #4、#5、#6（评论注明提交哈希）。
- [ ] 日常使用中观察各客户端触发情况，案例喂给 Issue #2。
