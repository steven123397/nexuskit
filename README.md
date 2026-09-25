# NexusKit (`nk-*`)

> **The Symbiotic Engineering Framework for AI Coding Agents.**  
> 融合 **Matt Pocock** 的敏捷结对直觉、TDD 工匠精神与 GitHub Issue 上下文控制，以及 **Compound Engineering (EveryInc)** 的工程严谨性、架构契约与知识复利体系。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Prefix: nk-](https://img.shields.io/badge/Prefix-nk--*-brightgreen.svg)](#)
[![GitHub Issues 1st Class](https://img.shields.io/badge/GitHub%20Issues-1st--Class-orange.svg)](#)
[![Context: 200k--300k](https://img.shields.io/badge/Context-Bounded%20(200k--300k)-purple.svg)](#)

---

## 📖 背景与诞生

在实际生产级项目（实战验证基地：[`D:\codex_project\paper-30min`](file:///D:/codex_project/paper-30min)）的长期深度实践中，目前业界最知名的两套 AI Agent 技能体系展现了各自的强项与局限：
* **Matt Pocock Skills**（本地参考备份：[`C:\Users\29617\.agents\backups\mattpocock-skills-20260824-193425`](file:///C:/Users/29617/.agents/backups/mattpocock-skills-20260824-193425)）
* **Compound Engineering**（本地安装路径：[`C:\Users\29617\.gemini\config\plugins\compound-engineering`](file:///C:/Users/29617/.gemini/config/plugins/compound-engineering)）

| 维度 | Matt Pocock Skills | Compound Engineering (CE) | **NexusKit (`nk-*`)** |
| :--- | :--- | :--- | :--- |
| **任务与上下文管理** | **极佳**：通过原生 GitHub Issues 拆任务，单任务对应一个 Fresh Session。 | **硬伤**：单主代理大包大揽承包整个 Plan，主会话上下文失控雪崩。 | **继承 Matt 并优化**：以 GitHub Issues 为一等公民，每个任务严格封装在 200k~300k Token 的独立会话中。 |
| **工件与生命周期** | **清爽**：依赖 Issue 追踪，不污染本地仓库。 | **硬伤**：生成几十个本地 Markdown（plans/reviews），无序堆积且缺乏归档。 | **原生闭环**：临时过程走 GitHub Issues/PRs，长期资产走 `solutions/` 和 `CONCEPTS.md`，代码树永远清爽。 |
| **交互与心流** | **繁琐**：Grill 流程像查户口，琐碎细节全抛给人类做选择。 | **适度**：从 Brainstorm 到 Plan 节奏紧凑、架构契约严谨。 | **去芜存菁**：引入 `Ideate` + `Brainstorm`，Agent 自主决策琐碎细节，只向人类确认关键架构分歧。 |
| **超大任务规划** | **先锋**：提出 `Wayfinder`（战争迷雾与决策探针）。 | **薄弱**：缺乏面对未知超大目标的递进探针机制。 | **纯粹保留**：保留 `nk-wayfinder` 专门作为史诗级未知任务的“决策探针寻路器”。 |
| **经验复利与沉淀** | **偏弱**：以会话为中心，缺乏跨会话知识库。 | **极佳**：`compound` 机制沉淀 `solutions/`，解决跨会话失忆。 | **双轨复利**：系统级知识沉淀（`solutions/`）+ 协作级流程复盘（Retro 优化规则）。 |

更多架构决策细节与深度分析，请参阅架构立项文档：[NexusKit 架构设计与体系构想 (Ideation RFC)](docs/ideation/nexuskit-framework-ideation.md)。

---

## 🌟 核心设计原则

1. **GitHub Issues 作为一等公民（1st-Class Issue Tracking）**：
   任务与依赖关系天然生长在 GitHub Issues/PRs 上，具备天然的状态流转、标签过滤、线程讨论与关闭归档能力，拒绝本地临时 Markdown 工件堆积成灾。
2. **严苛的上下文边界守护（200k~300k Token Envelope）**：
   绝不让一个主代理承担超长任务。将计划拆解为垂直切片任务（Tracer-bullet Tasks），每一个 Task 严格控制在 20~30 万 Token 的独立生命周期内完成。
3. **消除冗余盘问（Autonomous Defaults, Socratic Essentials）**：
   AI 编程的价值在于释放人类认知负荷。对于常规技术选型、命名惯例、推断式配置，Agent 自行裁决；只对核心产品边界与重大架构抉择向人类发起关键对齐。
4. **双轨经验复利（Dual-Track Compounding）**：
   * **代码知识轨（System Learning）**：将非显而易见的踩坑因果提炼至 `docs/solutions/` 和 `CONCEPTS.md`。
   * **流程复盘轨（Workflow Retro）**：复盘人机协作中的阻碍，动态更新 Agent 规则与配置（`AGENTS.md` / `RULES.md`）。
5. **极简顺滑的前缀人机工效（Ergonomic Prefix `nk-*`）**：
   统一采用键盘击键极其舒适的双字母前缀 `nk-`（右手食指两键流畅顺按），既消除命名污染，又实现行云流水的呼出体验。

---

## 🗺️ 技能矩阵全景规划

### 1. 史诗未知寻路（Epic Exploration）
* **`/nk-wayfinder`**：当面临“规模极大、未知数极多、无法直接编写 Plan”的史诗级目标时启动。在 GitHub Issues 建立决策地图，派发 `research`（预研）、`prototype`（原型）、`decision`（决断）探针，逐一驱散迷雾。

### 2. 特性研发主干流水线（Core Feature Pipeline）
```text
/nk-ideate ──► /nk-brainstorm ──► /nk-plan ──► /nk-to-tasks ──► /nk-work ──► /nk-compound
 (做哪个?)       (做什么?)        (怎么做?)      (拆任务推Issue)   (独立会话执行)   (双轨复利入库)
```
* **`/nk-ideate`**：立足当前代码库现状，运用 6 个认知透镜并发发散，经严苛批判筛选后产出 3~5 个高杠杆改进方向。
* **`/nk-brainstorm`**：针对选中方向，快速澄清 WHAT 与边界，产出产品需求契约（Product Contract），拒绝无休止琐碎盘问。
* **`/nk-plan`**：技术架构设计，产出统一技术方案（Unified Plan），定义接口契约、时序与测试策略。
* **`/nk-to-tasks`**：将 Plan 切割为具有业务价值的垂直切片（Tracer Bullets），原生调用 `gh` CLI 发布至 GitHub Issues，标注依赖关系与上下文预算。
* **`/nk-work`**：在清爽会话中认领单个未阻塞 Task，**深度融合 CE 的波次执行严谨性与 Matt 的测试先行（TDD/Red-Green-Refactor）原则**，自测通过后提交并关闭 Issue（无需单独拆分多余的 `nk-tdd` 指令）。
* **`/nk-compound`**：双轨经验复利，提炼系统解决方案文档并复盘人机协作流程。

### 3. 诊断与质控（Diagnose & Quality）
* **`/nk-debug`**：严苛五阶段因果排错循环。强迫在提出假设前建立 2 秒内可复现的极速变红反馈环（Tight Red-capable Loop），拒绝凭空猜想。
* **`/nk-simplify`**：功能交付后的防腐化精简与代码重构，降低认知复杂度。
* **`/nk-review`**：针对当前 Task 或 PR 的多维度代码与规范审查。

### 4. 辅助与衔接（Utilities & Flow）
* **`/nk-wizard`**：自动生成交互式 Bash 向导脚本，引导人类一步步走完繁琐的手动凭证配置、云端操作或数据迁移。
* **`/nk-wait-what`**：即时刹车令，要求 Agent 暂停发散，用最精炼的技术语言重新梳理上下文。
* **`/nk-commit`**：组织符合规范的高语义 Git Commit 消息。
* **`/nk-handoff`**：跨 Agent / 跨会话零信息损耗接力。

---

## 🛠️ 快速安装

克隆或配置本仓库至你的 Agent 配置目录（如 `~/.agents/skills` 或 Antigravity 插件目录）：

```bash
git clone https://github.com/steven123397/nexuskit.git
```

在支持 Skills 规范的客户端（如 Claude Code / Antigravity / Codex / Cursor）中直接通过 `/nk-<command>` 调用。

---

## 📄 开源许可证

本项目基于 [MIT 许可证](LICENSE) 开源。
