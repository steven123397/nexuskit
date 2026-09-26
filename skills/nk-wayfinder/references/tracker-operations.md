# Tracker 操作细则（GitHub Issues + `gh`）

> 本文件定义 map、child tickets、blocking 与 frontier 在 GitHub Issues 上的物理表达。原则：优先使用 GitHub 原生关系（sub-issues、blocked-by），因为 tracker UI 会可视化它们，人类不用打开 map 也能看到哪些 ticket 可拿；原生能力不可用时退回 body 约定。

## 前置检查与 label 准备

```bash
gh repo view --json nameWithOwner   # 确认远端与 gh 可用；失败则本技能不可用
```

所需 labels：`wayfinder:map`、`wayfinder:research`、`wayfinder:prototype`、`wayfinder:grilling`、`wayfinder:task`。缺失时创建：

```bash
gh label create wayfinder:map --color 1D76DB --description "Wayfinder decision map"
gh label create wayfinder:research --color 0E8A16
# …其余类推
```

## 创建 map

```bash
gh issue create --label wayfinder:map --title "<map name>" --body-file <body>
```

body 按 SKILL.md 的 map body 模板填写。Map 的 title 就是它的 name；所有引用都用 name 加链接。

## 创建 child tickets

先建全部 tickets，拿到编号后第二遍再 wire blocking edges。

1. **优先：GitHub 原生 sub-issues。** 用 GraphQL API 把 ticket 挂为 map 的 sub-issue（`addSubIssue` mutation，需要双方的 node id）。GitHub UI 会在 map 下直接列出 tickets。
2. **退回：body 约定。** ticket body 末尾加一行 `Part of: [<map name>](<map url>)`；查询时按 label + 正文中的 map 链接过滤。

无论哪种方式，ticket 都带 `wayfinder:<type>` label，body 是 `## Question` 一节。

## Blocking

1. **优先：GitHub 原生依赖关系。** 用 REST API `POST /repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocked_by`（或对应的 gh api 调用）建立 blocked-by。UI 会展示依赖，frontier 一目了然。
2. **退回：body 约定。** ticket body 加一节：

   ```markdown
   ## Blocked by

   - [ ] [<blocker ticket name>](link)
   ```

   blocker 关闭后勾掉对应行；全部勾掉即 unblocked。

不确定当前账号/仓库支持哪种时，先尝试原生调用，失败后退回 body 约定，并在 map 的 **Notes** 里记一行本 effort 采用的约定，让后续会话一致。

## Claim 与 frontier 查询

- **Claim**：`gh issue edit <number> --add-assignee @me`。任何工作开始之前执行；assignee 就是 claim。
- **Frontier**：open、unblocked、unclaimed 的 tickets。基础查询：

  ```bash
  gh issue list --state open --search "label:wayfinder:research OR label:wayfinder:prototype OR label:wayfinder:grilling OR label:wayfinder:task" --json number,title,assignees,labels
  ```

  再过滤掉有 assignee 的（已 claim）和仍有 open blocker 的（blocked）：原生依赖用 `gh api` 查 `blocked_by`；body 约定则读 body 中未勾选的 `## Blocked by` 行。属于哪张 map 由 sub-issue 关系或 `Part of:` 行判定。

## Resolution 与关闭

```bash
gh issue comment <number> --body "<resolution：答案、理由、后续 tickets 依赖的事实>"
gh issue close <number>
gh issue edit <map number> --body "<在 Decisions so far 追加一行后的完整 body>"
```

Resolution comment 至少包含：答案本身、关键理由、解决中产生的 assets 链接、后续 tickets 依赖的事实（凭据位置、新 URL、数据规模等）。向 map 追加时遵循 Refer by name：`[name](link) — 一行 gist`。

## 并发

多个会话可能同时处理 unblocked tickets。所有判定（claim 是否成功、frontier 内容）以查询时刻的 tracker 实时状态为准；claim 失败（已被 assign）就换下一个 frontier ticket，不等待、不抢占。
