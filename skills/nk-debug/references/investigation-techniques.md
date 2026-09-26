# 调查技术 (Investigation Techniques)

> **路径解析说明：** 本文件中的引用均相对于本文件所在目录解析。

常规代码追踪不够用时按需查阅本文件：缺陷复现不稳定、涉及时序或并发、是性能回退、或需要语言/框架侧手段时。

---

## 根因回溯 (Root-Cause Tracing)

缺陷在调用栈深处显现时，直觉是在报错处修。那是修症状。正确做法是沿调用链反向追溯到坏状态产生的地方。

**回溯步骤：**

- 从报错处开始；
- 每层问：这个值从哪来？谁调用了这个函数？传入了什么状态？
- 持续向上游走，直到找到合法状态首次变非法的位置——那才是根因。

**示例：**

```
症状：API 返回 500，"Cannot read property 'email' of undefined"
崩溃处：NotificationService 里的 sendWelcomeEmail(user.email)
谁调的？UserController.create()，在保存用户记录之后
传了什么？user = await UserRepo.create(params) —— 而 create() 在主键冲突时返回 undefined
真正原因：UserRepo.create() 静默吞掉主键冲突错误并返回 undefined，而不是抛出
```

修复属于源头（UserRepo.create 应在主键冲突时抛出），而不是报错显现处（NotificationService）。

**手动追踪停滞时**，加埋点：

```javascript
// 在可疑操作之前
const stack = new Error().stack;
console.error('DEBUG [operation]:', { value, cwd: process.cwd(), stack });
```

测试中用 `console.error()`——logger 输出可能被抑制。在危险操作**之前**打日志，而不是失败之后。

---

## 跨组件边界埋点 (Multi-Component Boundary Instrumentation)

根因回溯走的是单一调用链。当缺陷跨越子系统——CI → 构建 → 签名，API → 服务 → 数据库，前端 → API → 后台任务——失败很难归因到单一链条。改为在一次运行中给每个组件边界埋点，捕获各自"进入"与"离开"的数据，让证据指出失败的层。

**步骤：**

1. 列出数据从触发到症状跨越的组件边界；
2. 每个边界记录进入与离开的值——带上具体数值、相关环境与标识边界的短标签；
3. 跑一次场景；
4. 线性读日志，逐个比较上一段的"离开"与下一段的"进入"；
5. 数据首次不再符合预期的边界，就是失败的层。

**示例（CI 上的应用签名）：**

```bash
# 层 1：工作流环境
echo "=== workflow env ==="
echo "IDENTITY: ${IDENTITY:+SET}${IDENTITY:-UNSET}"

# 层 2：构建脚本环境
echo "=== build script env ==="
echo "IDENTITY: ${IDENTITY:+SET}${IDENTITY:-UNSET}"

# 层 3：签名阶段的钥匙串状态
echo "=== keychain ==="
security list-keychains
security find-identity -v

# 层 4：实际签名调用
codesign --sign "$IDENTITY" --verbose=4 "$APP"
```

一次运行，日志就精确显示哪一层丢了值——secrets → 工作流 ✓、工作流 → 构建 ✗——于是聚焦工作流到构建脚本的变量继承，而不是签名本身。

**何时胜过回溯追踪：** 症状离触发很远（隔多个组件）、组件归属不同系统（CI 与应用代码）、"调用栈"是概念性的而非字面的（消息总线、HTTP、进程边界）。定位到失败层之后，层内仍然用回溯追踪。

---

## 用 Git Bisect 定位回归 (Git Bisect)

缺陷是回归（"以前是好的"）时，用二分查找找到引入它的提交：

```bash
git bisect start
git bisect bad                     # 当前提交是坏的
git bisect good <known-good-ref>   # 一个它还能正常工作的提交
# git bisect 会检出中间提交——测试它
# 标记 good 或 bad，重复直到找到引入提交
git bisect reset                   # 结束后回到原分支
```

用测试脚本自动二分：

```bash
git bisect start HEAD <known-good-ref>
git bisect run <test-command>
```

测试命令以退出码 0 表示 good、非零表示 bad。

---

## 间歇性缺陷 (Intermittent Bugs)

缺陷在 2~3 次尝试后仍不能稳定复现时：

**日志陷阱。** 在疑似失败点加定向日志，反复跑场景，捕获通过与失败两次运行之间不同的状态。

**统计复现。** 循环跑失败场景，建立复现率：

```bash
for i in $(seq 1 20); do echo "Run $i:"; <test-command> && echo "PASS" || echo "FAIL"; done
```

5% 的复现率确认缺陷存在，但提示时序或数据敏感。

**环境隔离。** 系统地消减变量：

- 同一测试，换一台机器？
- 同一测试，换数据种子？
- 同一测试，串行 vs 并行执行？
- 同一测试，有网 vs 断网？

**数据依赖的触发。** 缺陷只在特定数据下出现时，识别触发条件：失败输入独特在哪？输入的长度、编码、边界值要紧吗？数据顺序要紧吗（有序 vs 随机）？

**测试顺序污染。** 单独跑通过、套件里跑失败，说明测试之间在泄漏状态：

- 单独跑失败用例——通过则污染确认；
- 单独跑该文件——把污染范围缩小到同文件或跨文件；
- 用随机顺序跑套件（多数 runner 支持种子参数）——每次失败邻居都不同，说明有全局状态被改写；
- 对排在前面的测试做二分：失败用例先配前一半跑、再配后一半跑，逐步收窄。

隔离后的常见元凶：模块级状态、没拆除的 Mock、没清理的临时文件、没回滚的数据库行、被改写且没恢复的环境变量。

---

## 复现最小化 (Repro Minimization)

缺陷稳定复现后，复现往往很大——500 行的集成测试、巨大的载荷、漫长的表单操作序列。更小的复现让后续每步调查更快，并把真实触发点孤立出来。

**手动 delta debugging：**

1. 把复现切一半；
2. 还会失败吗？会，丢弃另一半，对剩余部分递归；不会，失败依赖你切掉的那一半里的东西——放回去，改切另一半；
3. 持续削减，直到再切任何一部分都会丢失失败。

**对输入载荷：**

- 逐个（或逐半）移除字段，同时确认缺陷仍在；
- 缩短字符串到仍能触发的最小长度；
- 把复杂嵌套结构替换为仍能复现的最小形状。

**对测试序列：**

- 移除看起来不影响失败断言的准备步骤；
- 把辅助函数内联进测试，看清实际跑的是什么；
- 移除其他断言，孤立出是哪个断言在什么状态上失败。

最小化后的复现经常直接揭示根因。

---

## 语言与框架侧提示 (Framework-Specific Debugging)

- **框架隐式执行点**：回调（`before_save`、`after_commit` 之类）、中间件链、生命周期钩子会隐式执行并改写状态——读显式代码路径之外，先检查这些；
- **Node.js**：`--async-stack-traces` 拿完整异步调用链；检查 Promise 是否缺 `.catch()` 或 `await`；事件循环延迟用 `process.hrtime()` 前后打点；内存问题用 `--inspect` 加堆快照；
- **Python**：except 块里 `traceback.print_exc()` 丰富回溯；`breakpoint()` 交互调试；`sys.settrace()` 做执行追踪；`logging.basicConfig(level=logging.DEBUG)` 开详细日志；
- **Ruby**：查隐式回调与中间件栈（如 `rake middleware`），对可疑关系查询用 `.to_sql` 看实际生成的 SQL。

---

## 单步调试器 vs 埋点 (Debugger vs Instrumentation)

打印调试是默认选择——加得快、适用面广。但有些场景交互式单步调试器收敛得快得多。经验法则：

- **用单步调试器**：失败代码路径是局部的（具体某个函数或紧凑的调用链）、缺陷可稳定复现、且你需要已知点的精确状态——一次看许多局部变量、某个结构的精确形状、循环中状态的演变。一次断点，全看到；
- **用埋点**：缺陷间歇出现、跨越多个调用或分布式组件、或发生在中断执行有破坏性的场景（生产环境、时序敏感的并发代码、长驻进程）。埋点跨时间与跨环境捕获弥散行为。

混合使用很常见：先埋点定位范围，再在定位点挂调试器。

**各语言入口：**

| 语言 | 交互断点 | 附加到运行中进程 |
| :-- | :-- | :-- |
| Python | 代码里 `breakpoint()`，或 `python -m pdb script.py` | `python -m pdb -p <pid>`（Python 3.14+）；更早版本在目标里埋 `rpdb` / `remote-pdb` 触发后连接 |
| Node.js | 代码里 `debugger;` + `node --inspect-brk`，再用 Chrome DevTools 或 VS Code 连接 | `kill -SIGUSR1 <pid>` 为运行中进程开启 inspector（Linux/macOS），再连接 DevTools 或 VS Code 的 9229 默认端口 |
| Ruby | `binding.irb`（stdlib）、`binding.pry`（pry）、`rdbg` | 加载 debug gem 后 `rdbg --attach <pid>` |
| Go | `dlv debug` 或 `dlv test`，然后 `break`、`continue`、`print` | `dlv attach <pid>` |
| Rust / C / C++ | `lldb target/debug/binary` 或 `gdb binary`，然后 `break`、`run`、`print` | `lldb -p <pid>` / `gdb -p <pid>` |
| 浏览器 JS | 代码里 `debugger;`，或 DevTools Sources 面板打断点 | DevTools 自动附加到页面 |

跑测试时，多数测试 runner 集成了上述入口——如 `node --inspect-brk $(which jest)`、`pytest --pdb`、`dlv test`。优先用 runner 的集成，而不是事后手动附加。

---

## 性能回退 (Performance Regressions)

症状是"慢"而不是"错"时，日志与读代码会误导：对时间去向的直觉不可靠，看似可疑的热点只是假设不是证据。先测量，后改动：

- 动手前先建立数值基线——给慢操作包一层计时、跑一次 profiler、看查询计划（`EXPLAIN ANALYZE`）。对性能缺陷，这个数值就是复现阶段的"红"：修复的验证方式是重新测同一个数，而不是推理"改动应该会更快"；
- 先归因再优化：profiler 或分阶段计时告诉你时间实际去了哪。优化没测过的嫌疑点，是性能版的猎枪式调试；
- 如果"慢"是回归，对着测量值做二分（见上文 Git Bisect），而不是读 diff 找看起来昂贵的东西。

---

## 竞态调查 (Race Conditions)

怀疑时序或并发时：

**时序隔离。** 在可疑点注入刻意延时，把竞态窗口拉宽到可复现：

```javascript
// 模拟慢操作以暴露竞态
await new Promise(r => setTimeout(r, 100));
```

**共享可变状态。** 搜索被多个线程或进程无同步访问的变量、缓存或数据库行。常见模式：全局或模块级可变状态；无锁的缓存读；先读后写但没有乐观锁的数据库行。

**异步顺序。** 检查操作是否假定了并无保证的执行顺序：`Promise.all` 里有相互依赖的操作；假定触发顺序的事件处理器；假定读一致性的数据库写。

**用条件等待替代拍脑袋延时。**  flaky 测试常建立在猜测操作耗时的 `setTimeout`/`sleep` 上——快机器上通过，负载下或 CI 上失败。把猜测替换为轮询测试真正依赖的条件，并以超时兜底：

```typescript
// 之前：负载下竞态
await new Promise(r => setTimeout(r, 50));
expect(getResult()).toBeDefined();

// 之后：等待条件本身
await waitFor(() => getResult() !== undefined, 'result available', 5000);
expect(getResult()).toBeDefined();
```

拍脑袋延时只在测试真实时序行为（防抖间隔、节流窗口）时才算正确——那种情况下注释说明为什么是这个时长。

---

## 海森堡缺陷与观察者效应 (Heisenbugs)

加日志、挂调试器或插埋点导致缺陷消失时，是观察改变了系统行为。这本身是诊断信息——不要得出"已修复"的结论。缺陷还在，只是被你的埋点扰动得看不见了。

**消失告诉你什么：**

- **时序敏感**：埋点拖慢了代码，竞态不再赢。去查并发、异步顺序与共享可变状态，而不是表面逻辑；
- **GC 敏感**：日志分配了内存、触发 GC 掩盖了症状。查内存压力、finalizer、对象生命周期；
- **优化敏感**：埋点阻止了某个产生错误结果的编译器/JIT 优化。罕见但真实（尤其 C/C++/Rust 的 release 构建）；
- **缓冲敏感**：日志冲刷改变了 I/O 顺序。常说明别处有未冲刷的写；
- **异步顺序敏感**：日志 I/O 引入的 microtask 边界重排了后续操作。查隐式依赖同步顺序的代码。

**如何在不扰动的前提下调查：**

- 非阻塞埋点：写内存环形缓冲区，观察到失败后才转储；
- 采样 profiler 替代追踪：从外部观察什么在跑，不向代码路径注入代码；
- 平台级手段：`strace`、`dtrace`、eBPF、平台 profiler，无需改代码；
- 事后证据：core dump、堆快照、失败后捕获的状态。

判定规则：缺陷对观察敏感时，修复必须经得起观察手段的重新引入。只在埋点存在时才成立的修复，本身就是海森堡修复。

---

## 浏览器缺陷 (Browser Debugging)

用环境可用的浏览器工具（浏览器面板、截图、console、network）调查 UI 缺陷：

- **端口确认**：项目指令明确写了开发服务器端口就用它；否则查 `package.json` 的 dev 脚本，再查环境配置文件，最后回退 3000；
- **Console**：查 JavaScript 报错、失败的网络请求、CORS 问题——它们经常在任何代码追踪之前就揭示根因；
- **Network**：查失败的 API 请求、意外状态码、缺失的 CORS 头。后端返回的 422 或 500 能立刻收窄调查范围。

---

## 跨系统取证 (Evidence Harvesting)

缺陷横跨真实环境（生产、预发、多服务）时，最丰富的证据通常已经存在于日志、trace 与错误监控的载荷里。可能的话直接用它们，而不是从零复现。

**端到端追踪单个请求。** 选一个具体的失败请求（错误监控里的精确时间戳、用户 ID 或事件 ID），然后：

- 在每个相关日志源里搜这个标识——correlation ID、request ID、trace ID、user ID；
- 按顺序拼出时间线：边缘 → API → 服务 → 数据库 → 下游调用 → 响应；
- 标出时间线的缺口（日志缺失）与矛盾（时间戳乱序、ID 没传递下去）。

一次完整的请求追踪，通常比十几次复现尝试更快揭示根因。

**Correlation ID。** 多数 Web 框架自动附带 request ID 或接受请求头传入（`X-Request-ID`、`traceparent`）。项目有时，每条日志与每个下游调用都应携带它。缺失或没传递下去本身就是发现——传递链有缺口意味着你拼不出时间线，下一次事故时值班的人也一样拼不出。

**时间戳三角定位。** 失败操作没有共享 ID 时，时间戳是兜底。把每个日志查询约束在观察到的失败前后的窄窗口内，按顺序找第一个异常。注意服务间的时钟漂移——两台主机差 30 秒就会重排证据、误导定位。

**错误监控载荷。** Sentry、Bugsnag、Honeybadger、AppSignal 之类工具在失败时刻捕获堆栈、面包屑、用户上下文、请求状态与版本元数据。追代码之前先读完整载荷——它常包含精确的 文件:行号、变量状态与通往错误的面包屑。分组规则有时会掩盖频率与变体信息，展开看每一个实例而不只是代表性那个。

**APM / 分布式 trace。** 项目有 Datadog APM、Honeycomb、New Relic 或 OpenTelemetry collector 时，trace 视图给出跨服务的完整调用树与耗时。关注：意外长的 span（阻塞或缓慢的依赖）、链条中间失败的 span、本应存在却不存在的 span（埋点缺失同样掩盖缺陷）。

**先保全再调查。** 错误监控与日志系统有保留窗口。开始长调查之前，把关键证据（事件 ID、trace ID、完整堆栈、面包屑）导出或快照，避免调查中途过期。

---

## 系统边界检查 (System Boundary Checks)

许多缺陷住在应用与其运行系统的边界上——网络、数据库、文件系统、操作系统。深度代码追踪之前快速过一遍这些边界，常能整类整类地排除嫌疑。

**网络：**

- DNS 解析：`dig <host>` / `nslookup <host>`——从这台主机解析到的名字符合预期吗；
- 可达性：`curl -v https://host/path`——完整头、重定向、TLS 错误；
- 状态码与头：4xx/5xx、意外重定向、缺失的 CORS 头、content-encoding 意外；
- 连接状态：`ss -tan` / `netstat -an` / `lsof -i`——打开的连接、监听端口、TIME_WAIT / CLOSE_WAIT；
- TLS：`openssl s_client -connect host:443`——证书链、过期时间、SNI 不匹配。

**数据库：**

- 查询计划：对可疑查询跑 `EXPLAIN` / `EXPLAIN ANALYZE`——用了预期的索引，还是在扫大表；
- 慢查询日志 / 近期查询：多数数据库能展示最近最慢的 N 条查询，失败查询常在其中；
- 锁与事务：查锁/事务表（`pg_locks`、`information_schema.innodb_trx`、`sys.dm_tran_locks`）——操作是否在等一个长事务持有的锁；
- 连接池：应用是否耗尽连接池、连接是否在泄漏；
- 复制延迟（读路径上有只读副本时）：写后立刻读可能打到还没追上的副本。

**文件系统：**

- 存在性与权限：`ls -la <path>`——文件在吗，运行用户可读可写吗；
- 大小写敏感：只在 Linux（而非 macOS）出现的缺陷常是大小写不匹配；
- 打开的句柄：`lsof <path>` 或 `lsof -p <pid>`——是否有什么还持有文件，阻止写入或删除；
- 磁盘空间：`df -h`。空间不足的错误有时在别处表现为诡异的写失败；
- 文件监听 / inotify 上限：EMFILE 或 "too many open files" 常是 inotify/FD 上限，不是代码泄漏；
- 路径分隔符与编码：Unix 代码里的 Windows 风格路径，或非 UTF-8 locale 下的 UTF-8 路径。

**进程与信号：** 确认运行中的进程确实是你以为的那个版本（`ps aux | grep`，把 pid 与构建时间交叉核对）。僵尸进程、孤儿 worker、崩溃后以旧代码重启的进程，都会伪装成代码缺陷。

---

## 缺陷类别速查 (Bug-Class Pattern Checklist)

深度追踪之前过一遍这份清单。许多缺陷属于可识别的类别，类别直接暗示先看哪里。对照症状是否命中：

- **时间与时区**：午夜前后的差几小时错误、夏令时切换期间的失败、epoch 与毫秒混淆、naive 与带时区时间混用、UTC 与本地时间假设错误；
- **编码与 locale**：输出乱码、字节数与字符数差一、文件开头的 BOM 弄坏解析器、非 ASCII 字符丢失、locale 敏感的比较产生不一致结果；
- **浮点精度**："应该"相等却不等的比较、NaN 沿计算链传播并静默污染下游、极大或极小的数丢精度；
- **整数溢出/下溢**：有界整数类型回绕、无任意精度整数语言里的 int32 溢出、假定非负处出现负值；
- **差一与边界**：空集合边界、首元素或末元素丢失、闭区间与开区间不匹配、栅栏柱错误；
- **缓存陈旧**：改动后立刻正常、过一段时间后出错、重启或清缓存就好——包括 HTTP 缓存、CDN 缓存、应用级 memoization、浏览器 service worker；
- **权限 / 鉴权**：一个用户正常另一个不行、无鉴权层的开发环境正常但生产不行、超级用户正常但真实运行身份不行；
- **依赖或版本漂移**：一台机器正常另一台不行、lockfile 与清单不同步、间接依赖升级后行为变化、原生模块编译时的运行时版本不同；
- **路径 / 大小写敏感**：macOS 正常 Linux 失败（大小写）、Linux 正常 Windows 失败（路径分隔符、`CON`/`PRN` 之类的保留名）；
- **并发 / 顺序**：串行跑测试正常、并行失败；随机顺序时一种跑法正常另一种失败；
- **陈旧构建产物**：`dist/`、`.next/`、编译出的 `.pyc`、生成的代码、Docker 镜像层——从干净状态重建再看是否复现；
- **观察者效应（海森堡缺陷）**：挂上日志、调试器或 profiler 缺陷就消失——见上文海森堡缺陷一节；
- **TOCTOU（检查时与使用时）**：检查那一刻通过了，但依赖的动作执行前底层状态已经变了。

这里做模式匹配的成本很低。花 30 秒对照症状是否属于已知类别，可以省掉数小时的盲目追踪。
