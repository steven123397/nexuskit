# 当前状态

- **所在分支**：`main`
- **HEAD**：`bfa2426`（本文件随其后的 v0.1.0 收尾提交入库）
- **版本/里程碑**：v0.1.0 已收尾（2026-09-26）。版本规则（用户 2026-09-26 拍板）：v1.0.0 之前均为试用版；大迭代走 minor（0.X.0），小迭代走 patch（0.x.Y）。
- **已具备能力**：17 个 `nk-*` 技能 + 共享约定 `skills/conventions/`（选用见 [`../README.md`](../README.md) 路由表）；三形态分发——Kimi 插件（`kimi.plugin.json`）、Codex 插件（`.codex-plugin/plugin.json` + `.agents/plugins/marketplace.json`）、npx skills CLI；五项机械检查 + 双平台 CI。
- **验证结果**：
  - `python tests/run_checks.py` 五项全绿（链接 / 引用 / 字节上限 / 提示词副本 / frontmatter）；CI 通过。
  - 安装实装：Kimi 本地路径 ✅、Codex marketplace ✅、npx skills CLI 临时目录 ✅（18 目录零跳过）。
  - 未验证：真实项目端到端使用（即下一步迁移验收）。
- 归档经验：分发布局决策见 [`solutions/architecture-decisions/2026-09-26-distribution-layout.md`](solutions/architecture-decisions/2026-09-26-distribution-layout.md)；RFC 开放问题 2–4 已关闭，仅余中文触发（Issue #2）。

## 阻断与已知缺口

- [Issue #1](https://github.com/steven123397/nexuskit-skills/issues/1)：重复子代理提示词终局——触发时机为"首次需要跨副本同步修订"。
- [Issue #2](https://github.com/steven123397/nexuskit-skills/issues/2)：中文 description 触发可靠性（v1.1.0）。
- [Issue #3](https://github.com/steven123397/nexuskit-skills/issues/3)：可选增强泊车场（子代理输出体量 / Fresh Worker 纪律 / 状态返回行）。
- Kimi GitHub URL 安装在 rename 步骤 EPERM（上游安装器健壮性问题，与网络无关）；本地路径安装为可靠兜底。

## 下一步

- [ ] **迁移与验收（v0.2.0 目标）**：paper-30min 从 CE 迁移到 NexusKit，首跑 nk-init；按 RFC 第八章先写迁移方案（产物处理、指令文档更新、CE 去留、验收场景、迁移前打 tag 可回退）；验收发现的问题记入后续小迭代。
- [ ] 日常使用中观察各客户端触发情况，案例喂给 Issue #2。
