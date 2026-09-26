---
name: conventions
description: NexusKit 共享约定参考库（提交节奏、产物生命周期、术语、plan 格式等），由 nk-* 技能正文按需引用；不是可执行技能，不要直接调用。Shared conventions referenced by nk-* skills; not an executable skill — do not invoke directly.
disable-model-invocation: true
---

# NexusKit 共享约定 (Shared Conventions)

本目录是 `nk-*` 技能的共享约定库：技能正文只放流程框架，跨技能统一的规则集中在这里，由各技能按需引用。直接使用本体系时无需阅读本目录；编写或维护技能时，按各技能正文的指引查阅对应文件。

- [artifact-lifecycle.md](artifact-lifecycle.md)：产物与生命周期——每类产物的位置、终点与版本收尾规则
- [commit-cadence.md](commit-cadence.md)：提交节奏 R1–R6 与通用执行纪律
- [concepts-vocabulary.md](concepts-vocabulary.md)：CONCEPTS.md 术语表的格式与写入时机
- [current-md.md](current-md.md)：docs/current.md 的字段与更新时机
- [decision-autonomy.md](decision-autonomy.md)：自主决断与提问的边界
- [issue-writing.md](issue-writing.md)：Issue / backlog 条目写作规范
- [plan-format.md](plan-format.md)：plan 文件结构契约
- [settled-decisions.md](settled-decisions.md)：已定决策的判定与标注
- [solution-schema.md](solution-schema.md)：docs/solutions/ 的格式与准入门槛
