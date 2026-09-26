# 网络调研缓存

派发 `web-researcher` 之前检查缓存时，或派发后把新调研追加到缓存时读本文件。这里的行为是条件性的——大多数调用要么命中缓存，要么写入一次后继续。

## 缓存文件格式

```json
[
  {
    "key": {
      "mode": "repo|elsewhere-software|elsewhere-non-software",
      "focus_hint_normalized": "<小写、合并空白后的关注点，或空字符串>",
      "topic_surface_hash": "<用户提供的话题内容的短哈希>"
    },
    "result": "<web-researcher 的纯文本输出>",
    "ts": "<iso8601>"
  }
]
```

文件位于 `<scratch-dir>/web-research-cache.json`，其中 `<scratch-dir>` 是系统临时目录下的 `nk-ideate/<run-id>`，在 `grounding.md` Phase 1 中确定一次。

## 复用检查

派发 `web-researcher` 之前，取 `<scratch-dir>` 的父目录（系统临时目录下的 `nk-ideate/`），用文件搜索工具列出其下各 run-id 目录中的 `web-research-cache.json`——同一会话中的反复打磨可能合理地按话题复用另一次运行的缓存，而不是按 run-id。没有任何缓存文件时就是首次运行，继续派发。

读取每个匹配的文件。如果某个条目的 `key` 与当前派发一致（完全相同的模式变体——`repo`、`elsewhere-software` 或 `elsewhere-non-software`——加上相同的、不区分大小写的规范化关注点，加上相同的 `topic_surface_hash`），跳过派发，把缓存的 `result` 交给合并后的扎根摘要。模式变体必须完全一致：`elsewhere-software` 与 `elsewhere-non-software` 是不同领域，不能互相复用。在摘要中注明："复用本会话之前的网络调研——说'重新调研'可以刷新。"

用户说"重新调研"时，删除匹配的条目并重新派发。

## 新派发后追加

新派发完成后，把结果追加到本次运行的缓存文件 `<scratch-dir>/web-research-cache.json`（使用 Phase 1 的绝对路径；目录和文件不存在时创建）。同一会话中的下一次调用就能通过上面的列举复用它。

## 话题内容哈希

`topic_surface_hash` 是对网络调研所依据的用户提供内容做的哈希。这些内容是：

* **仓库外模式（`elsewhere-software`、`elsewhere-non-software`）：** 用户的话题请求加上 Phase 0.4 的问答回答（Agent 实际调研的主题）。两个子模式分开作键——同一话题哈希在软件与非软件之间重新分类时必须重新派发，因为调研领域不同。
* **仓库模式：** 关注点加上一个稳定的仓库区分符。这样在关注点为空时缓存键仍有意义——同一仓库中两次无关注点的调用可以合理地共享调研，但键仍能区分不同仓库。因为所有仓库的缓存文件都放在同一个系统临时目录下，只用 `app` 或 `frontend` 这样的目录名会在无关仓库之间冲突。按以下顺序取区分符并哈希（sha256 前 8 位十六进制即可）：
  1. `git remote get-url origin` —— 跨机器稳定，对同一远端的协作者也正确。
  2. `git rev-parse --show-toplevel` —— 仓库的绝对路径；只在本机有效，但在 git 仓库中总能取到。
  3. 当前工作目录的绝对路径 —— 不在 git 仓库中时的最后手段。

哈希之前规范化：小写、合并空白。（仓库区分符的哈希基于命令原始输出；只有关注点和话题文字需要规范化。）每条 git 命令单独执行，不用管道或 `&&` 拼接，兼容 PowerShell。

## 降级

当前平台上缓存文件在多次调用之间无法访问时（文件系统隔离、沙箱、临时工作目录），降级为"不复用，每次都派发"。在合并后的扎根摘要中注明这一限制并继续，不要假设平台具备它可能没有的能力。
