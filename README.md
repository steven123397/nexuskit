# NexusKit (`nk-*`)

> 面向 AI 编程 Agent 的个人工程技能体系。
> 取 **Compound Engineering (EveryInc)** 的规划严谨性与知识沉淀，取 **Matt Pocock Skills** 的单任务新会话、测试先行与术语维护，按个人项目、多 Agent 协作的实际画像重新组织。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Prefix: nk-](https://img.shields.io/badge/Prefix-nk--*-brightgreen.svg)](#)

---

## 背景

两套体系都在实战项目（paper-30min，私有仓库）中完整运行过：

* **Matt Pocock Skills**（[mattpocock/skills](https://github.com/mattpocock/skills)，2026-08 本地备份）
* **Compound Engineering**（[EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin)，v3.28.2）

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

仓库布局：技能与共享约定都在 [`skills/`](skills/) 下（`skills/nk-*` + `skills/conventions/`；`conventions` 是共享约定参考库，不是可执行技能，但必须以同名目录与 `nk-*` 平级安装，技能正文里的 `../conventions/` 引用才能解析）。

### Kimi Code 插件

```
/plugins install https://github.com/steven123397/nexuskit-skills
```

清单为根目录 `kimi.plugin.json`（`skills: "./skills/"`，整树随插件分发）。安装后 `/reload` 或开新会话生效。

### Codex 插件

清单为 [`.codex-plugin/plugin.json`](.codex-plugin/plugin.json)（`skills: "./skills/"`），按 Codex 的插件安装方式指向本仓库即可。

### npx（skills CLI）

```
npx skills add steven123397/nexuskit-skills
```

逐技能安装到 `.agents/skills/` 并平铺。注意：**务必连同 `conventions` 一起安装**（交互多选时全选，或 `--all`）——它是各技能 `../conventions/` 引用的共享约定库。也支持 `-s nk-plan` 单选技能。

---

## 许可证

[MIT](LICENSE)。本体系部分技能派生自 mattpocock/skills 与 EveryInc/compound-engineering-plugin（均 MIT），归属声明见 [NOTICE](NOTICE)。
