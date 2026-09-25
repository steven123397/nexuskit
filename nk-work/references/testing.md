# 测试先行与质量设计 (Testing)

> **路径解析说明：** 本文件中引用的共享约定（如 `../../conventions/`）均相对于本文件所在目录解析。

本文件规范测试驱动开发（TDD）中的好测试与坏测试辨别、测试 Seam 选择与 Mock 原则。

---

## 一、什么是测试接缝 (Seam)？

**接缝 (Seam)** 是可以在不修改业务代码内部实现的前提下，观察系统行为或改变系统行为的接入点（如公开函数、Trait、接口、API 端点）。

* **Agent 自选 Seam（K3）**：在规划与编码时，Agent 依据既有代码模式自主选择最自然的测试接缝，测试用例应当直接作用于接缝，而非探测私有变量。
* **何时向人类提问**：仅当选择的接缝会导致对外公开 API、协议契约发生变更，且落入 [`../../conventions/decision-autonomy.md`](../../conventions/decision-autonomy.md) 的确认区时，才向人类发起确认。

---

## 二、好测试 vs 坏测试

| 维度 | 好测试 (Good Tests) | 坏测试 (Anti-Patterns) |
| :-- | :-- | :-- |
| **测试目标** | 测试可观测的**行为与结果**（Behavior / WHAT） | 测试内部实现细节、私有函数与调用次数（HOW） |
| **重构耐受力** | 只要行为不变，重构内部实现时测试**依然保持常绿** | 一旦重构内部辅助函数或变量名，测试立即大面积红掉 |
| **断言有效性** | 明确断言独立已知的预期输出、返回状态或结果 | 同义反复（Tautology）：在测试里重算一遍业务算法 |
| **编写时序** | 垂直切片（Red -> Green 循环） | 水平切片：先写出整套空测试再开始写实现 |
| **可读性** | 测试名称精确描述业务场景，每个测试一个逻辑断言 | 测试名称模糊不清（如 `test_func_1`） |

---

## 三、Mock 模拟准则

过度 Mock 会导致“测试只测了 Mock 本身”，形成虚假的安全感。

### 1. 只在系统边界 (System Boundaries) 处 Mock
* 外部 API（支付、邮件、第三方服务）；
* 数据库（优先使用测试数据库，必要时可 Mock）；
* 时间与随机数（时钟、定时器、随机种子）；
* 文件系统或破坏性系统调用。

### 2. 不得 Mock 的范围（系统内部逻辑）
* **不 Mock 自己控制的内部类、模块或协作函数**；
* **不 Mock 纯计算业务领域逻辑**（数据转换、解析器、数学运算一律直接用真实代码测试）。

---

## 附录：典型正反代码示例 (Code Examples)

### 1. 观测行为 vs 耦合内部实现
```typescript
// GOOD: 测试调用方关心的可观测行为
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});

// BAD: 耦合内部协作细节与调用次数
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

### 2. 通过公开接口验证 vs 绕过接口直接查底层
```typescript
// GOOD: 通过公开接口闭环验证
test("createUser makes user retrievable", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});

// BAD: 绕过业务接口直接查库表细节
test("createUser saves to database", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
  expect(row).toBeDefined();
});
```

### 3. 独立已知期望值 vs 同义反复 (Tautological Tests)
```typescript
// GOOD: 期望值是独立、确定的字面量
test("calculateTotal sums line items", () => {
  expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
});

// BAD: 用与被测代码相同的逻辑重算期望值，测试天然恒真
test("calculateTotal sums line items", () => {
  const items = [{ price: 10 }, { price: 5 }];
  const expected = items.reduce((sum, i) => sum + i.price, 0);
  expect(calculateTotal(items)).toBe(expected);
});
```

### 4. 为可 Mock 性设计：依赖注入与 SDK 风格接口
```typescript
// 1. 依赖注入：传入外部客户端，而非在函数内硬编码实例化
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// 2. 优先使用 SDK 风格接口，而非通用条件分发函数
// GOOD: 每个外部操作独立可 Mock、具备类型安全，无需在测试中写条件分支
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch('/orders', { method: 'POST', body: data }),
};

// BAD: 泛用 fetcher 迫使测试在 Mock 内部编写复杂的 URL 匹配条件逻辑
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```
