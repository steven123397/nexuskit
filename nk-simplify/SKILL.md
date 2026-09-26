---
name: nk-simplify
description: Simplify settled, recently changed code for clarity, reuse, quality, and efficiency while preserving exact behavior. Use after implementation and before release review (nk-review); use nk-debug for bugs. 精简代码、交付后清理、实现完成后精简、simplify。
---

# /nk-simplify

> **路径解析说明：** 本文件中引用的参考文件（如 `references/`、`../conventions/`、`../nk-commit/`）均相对于本技能所在目录解析，不在目标代码仓库中查找。

对刚定型、刚改动的代码做清晰度、复用、质量与效率上的精简，行为必须保持完全不变。目标是更可读、更直白的代码，行数减少不是目标。用在实现完成之后、版本审查（`nk-review`）之前；排查 Bug 走 `nk-debug`。

**完成标志：** 范围内的精简已应用或逐条说明跳过理由，精简前后验证均实际运行通过，按提交节奏入库。  
**工作原则：** 只动刚改动的范围；行为保持优先于一切精简收益；未运行的测试不记为通过。

---

## 执行步骤

### 1. 确定精简范围 (Scope)
按以下优先级解析范围，不擅自扩大：
1. **用户指名的范围**最权威，用户说精简什么就只精简什么；
2. 否则取**当前分支相对基线的改动**（无可用基线时用 `git diff HEAD` 的暂存与未暂存改动）；
3. 不在 git 中或无 diff 时，取用户指名的文件或本会话中编辑过的文件。

以上都得不到非空范围时，停下来问用户要精简什么，不要猜。

**预检：** 若范围内没有实质的人写代码（只有文档、生成物、vendored 依赖、锁文件或机械性 churn），如实报告“无可精简”并停止。该检查只看改动性质，不看规模。

### 2. 多视角审查 (Review)
本技能提供三份英文审查提示词（原文保留，体量很小）：

- [`references/personas/code-reuse-reviewer.md`](references/personas/code-reuse-reviewer.md) —— 重复造轮子：已有工具函数、标准库原语、平台保证
- [`references/personas/code-quality-reviewer.md`](references/personas/code-quality-reviewer.md) —— 冗余状态、参数膨胀、复制粘贴、死代码等质量问题
- [`references/personas/efficiency-reviewer.md`](references/personas/efficiency-reviewer.md) —— 多余计算、错失并发、热路径臃肿、内存泄漏

按改动的信号选用视角：默认三个视角都过一遍；若范围信号明显（如纯并发重构只需效率视角），可只跑相关视角，并在汇报中说明取舍。

**执行方式：** 若客户端支持子代理，则并行派发审查子代理，每份子代理提示词 = persona 文件**逐字原文** + 完整范围（diff 或文件集）；否则在主会话内联逐视角过一遍。不得凭记忆转述 rubric，否则丢失保持行为不变的规则。

### 3. 应用或跳过 (Fix or Skip)
* 三个视角的结果齐全后，直接应用有价值的发现；误报与低价值发现记为“跳过”，不打扰用户。
* 评估发现时可以读范围外的代码，但只改范围内文件及其必需的 import/export 行。
* 每一处修改必须保持输出、错误、副作用与顺序完全不变；无法确认就跳过。
* **不精简掉安全检查**：信任边界校验、防数据丢失保护、安全与无障碍逻辑一律保留。
* 仅存在于本次未交付改动内部迭代中的接口或数据形状，确认范围外无调用方后可以移除兼容路径；不确定就保留。
* 尊重已定决策（见 [`../conventions/settled-decisions.md`](../conventions/settled-decisions.md)）：Plan 中敲定的技术决策（包括刻意的重复或拆分）不借精简之名推翻。

### 4. 验证行为不变 (Verify)
精简是行为保持型改动，仍需验证：
* 运行项目级 typecheck 与 lint；测试按影响半径选取——局部改动跑对应测试，共享或广影响改动跑更大范围，无法圈定则跑全量；
* 精简前后的测试结果都要实际运行并捕获证据，未运行不记为通过；
* 精简引入的失败：修复或回退该处改动，不放松断言、不削弱类型、不跳过测试；
* 项目未配置测试、lint 或 typecheck 时，在汇报中明确说明，不默默跳过验证。

### 5. 提交与收尾 (Commit & Report)
* 按 [`../conventions/commit-cadence.md`](../conventions/commit-cadence.md) 提交：精简改动可随当前实施单元一同提交，也可独立成一次 R1 提交；提交说明正文写入实际运行的验证命令与结果（含“行为保持不变”的依据）。
* 汇报：哪些原本就良好、哪些得到改善，按复用/质量/效率分类报告应用数与跳过数；没有任何改动就如实说明。不以净删行数作为成功指标。
* 若精简过程中发现值得沉淀的经验（非显而易见的取舍、易踩的坑），一句话建议运行 `/nk-compound`。
* 精简完成即达到版本审查前置状态，一句话建议接着运行 `nk-review`。

---

> 主要参考：CE `ce-simplify-code` (2026-09)、NexusKit 共享约定 [`../conventions/commit-cadence.md`](../conventions/commit-cadence.md)
>
> 与 CE 的主要差异及原因：
> * 删除 CE 的平台编排细节（受限派发、代理生命周期、模型档位、权限模式参数、任务跟踪提示、阻塞提问工具的探测规则）：NexusKit 客户端中立，只保留“支持子代理则派发、否则内联”的一条规则。
> * 三视角从“固定并行三个”改为“按信号选用、默认全跑”：NexusKit 以单会话串行为主，小范围改动不必机械跑满三个视角。
> * 删除 `session-settled:` 结构钉与计划路径传参机制：NexusKit 的等价物是 `conventions/settled-decisions.md`，直接引用共享约定。
> * 验证与提交并入 NexusKit 提交节奏（R1 验证证据入提交说明），CE 原文只要求跑检查、不管提交。
> * 增加与 `nk-compound`、`nk-review` 的衔接一句话：精简在体系内的位置是实现之后、版本审查之前。
