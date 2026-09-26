# NexusKit (`nk-*`)

> 面向 AI 编程 Agent 的个人工程技能体系。
> 取 **Compound Engineering (EveryInc)** 的规划严谨性与知识沉淀，取 **Matt Pocock Skills** 的单任务新会话、测试先行与术语维护，按个人项目、多 Agent 协作的实际画像重新组织。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Prefix: nk-](https://img.shields.io/badge/Prefix-nk--*-brightgreen.svg)](#)

---

## 背景

两套体系都在实战项目 [`D:\codex_project\paper-30min`](file:///D:/codex_project/paper-30min) 中完整运行过：

* **Matt Pocock Skills**（本地备份：[`C:/Users/29617\.agents\backups\mattpocock-skills-20260824-193425`](file:///C:/Users/29617/.agents/backups/mattpocock-skills-20260824-193425)）
* **Compound Engineering**（本地安装：[`C:/Users/29617\.gemini\config\plugins\compound-engineering`](file:///C:/Users/29617/.gemini/config/plugins/compound-engineering)）

| 维度 | Matt | CE | NexusKit |
| :-- | :-- | :-- | :-- |
| 上下文管理 | 一个任务一个新会话 | 主对话承包整份 plan，上下文膨胀 | 新会话 + `current.md` 入口 + 单个实施单元 |
| 需求对齐 | `grill` 盘问繁琐 | ideate/brainstorm 节奏合适 | 采用 CE 方式，去掉 grill，Agent 自决可推断细节 |
| 产物管理 | walkthrough、ADR 等本地文件堆积 | plan、review 本地文件堆积 | 每类产物有明确终点，版本收尾时统一清理 |
| 知识沉淀 | 术语即时维护，缺少经验库 | `solutions/` 经验库，术语只在 compound 时生长 | `solutions/`（含决策类型）+ 术语在规划中即时写入 |
| 提交节奏 | 无约束 | 无约束 | 统一规则，杜绝零碎的纯文档提交 |

完整设计见 [NexusKit 架构设计 RFC](docs/ideation/nexuskit-framework-ideation.md)。

---

## 核心约定

1. **工具箱，不是流水线**：每个技能可单独使用，按场景选取。
2. **`docs/current.md` 是跨会话入口**：记录当前能力、验证结果、阻断项、下一步与所在分支。
3. **产物有生命周期**：plan 与审查记录在版本分支上随代码演进，版本收尾时提炼长期价值后删除；Issue 只承载跨 plan 的待办、缺陷与探针。
4. **知识双轨**：踩坑因果与决策理由进 `docs/solutions/`，领域术语进 `CONCEPTS.md`。
5. **提交节奏**：一个经过验证的变化一次提交，文档随代码走；纯文档提交只发生在会话交接和版本收尾。
6. **项目流程归项目**：分支、发布、签名等项目特有约定写在项目自己的工作流文档中，技能读取而不内置。

---

## 按场景选用

| 场景 | 技能 |
| :-- | :-- |
| 不确定该用哪个 | `/nk-ask-ljq` |
| 在新仓库首次启用本体系 | `/nk-init` |
| 想找改进方向 | `/nk-ideate` |
| 有想法，要明确做什么、做到哪 | `/nk-brainstorm` |
| 需求明确，要设计怎么做 | `/nk-plan` |
| 实现一个实施单元或 Issue | `/nk-work` |
| 提交代码 | `/nk-commit` |
| 结束会话 / 接手工作 | `/nk-handoff` |
| 排查缺陷或异常 | `/nk-debug` |
| 审查代码 | `/nk-review` |
| 交付后精简代码 | `/nk-simplify` |
| 沉淀一条经验或决策 | `/nk-compound` |
| 版本收尾 | `/nk-close` |
| 目标巨大、未知太多，无法直接写 plan | `/nk-wayfinder` |
| 开发中冒出 bug 或新需求，先记下来不打断当前任务 | `/nk-to-issue` |
| 引导人完成一系列手动操作 | `/nk-wizard` |
| Agent 发散了，需要重新梳理 | `/nk-wait-what` |

实施进度见 RFC 第八章；全部技能已就位，接下来是 paper-30min 的迁移与集中验收。

---

## 安装

本目录是开发目录。体系定型后将仿照 CE 打包为多 Agent 插件。

---

## 许可证

[MIT](LICENSE)
