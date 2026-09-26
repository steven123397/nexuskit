---
title: "三形态分发共用同一 skills/ 布局，conventions 作为第 18 个可安装单元"
date: 2026-09-26
problem_type: architecture_decision
component: distribution_packaging
module: skills-layout
severity: high
applies_when:
  - "新增/移动技能或共享约定文件时"
  - "修改插件清单或安装方式时"
  - "排查某客户端安装后技能缺文件时"
tags:
  - packaging
  - skills-cli
  - plugin-manifest
status: accepted
---

# 三形态分发共用同一 skills/ 布局，conventions 作为第 18 个可安装单元

## Context & Decision

NexusKit 需要三种分发形态（Kimi 插件 / Codex 插件 / npx skills CLI），三者对"共享的 `conventions/` 如何随技能到达用户机器"的处理能力完全不同。决定：仓库布局即分发布局（`skills/nk-*` + `skills/conventions/` 平级），`conventions/` 带一个最小 SKILL.md（`name: conventions` + `disable-model-invocation: true`）成为第 18 个可安装单元，所有技能继续用 `../conventions/` 相对引用。放弃了两个备选：CE 式"构建期把共享内容内联进各技能"（引入生成管线与漂移面）和"改引用深度为 `../../conventions/`"（junction 加载侧与插件侧深度不一致，必有一侧失效）。

## Why & Trade-offs

关键约束来自三形态的交集：skills CLI 只安装**含合规 SKILL.md 的目录**（无 SKILL.md 的目录静默跳过），且按 **frontmatter name** 命名安装目录、全部平铺到 `.agents/skills/`；Kimi/Codex 插件则整树分发。平级布局 + `name: conventions` 恰好让三种形态下 `../conventions/` 的相对几何完全一致，零引用改写。代价：`conventions` 在各客户端的技能列表里作为一个"伪技能"可见（用 disable-model-invocation 抑制触发），以及新增技能必须保证 frontmatter `name` 与目录同名（已由 run_checks 第五项机械强制）。

## Downstream Impact

- 新增技能：`name` 必须与目录同名，description 中的 `: ` 必须加引号（严格 YAML 消费方存在，run_checks 已锁定）。
- 新增共享约定文件：只需放进 `skills/conventions/` 并在其 SKILL.md 索引中加一行，三形态自动携带。
- Codex 市场安装的必需文件是 `.agents/plugins/marketplace.json`（不是 `.codex-plugin/plugin.json`，后者是插件清单）；缺它报 "marketplace root does not contain a supported manifest"。
- 已知环境问题：Kimi 的 GitHub URL 安装在 Windows 上最后一步临时目录 rename 时可能 EPERM（Defender 对带 Mark-of-the-Web 文件的瞬态锁），与网络、清单无关；同一 URL 在 WSL 中安装成功（2026-09-26 实测）。Windows 上的兜底：本地路径安装（`/plugins install <本地目录>`）或重试。
