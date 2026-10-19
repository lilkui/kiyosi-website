---
description: 按金融工具类型比较 kiyosi 的定价方法，并选择 CPU 或 CUDA 蒙特卡洛后端。
---

# 定价引擎

请按金融工具类型选择引擎。虽然各引擎都使用 `price(instrument, context)` 接口，但支持的产品范围不同。

## 支持的产品与方法 {#instrument-coverage}

| 产品类型 | 可用定价方法 |
| --- | --- |
| 欧式普通期权 | 解析法、CRR 二叉树法、有限差分法、积分法、蒙特卡洛法 |
| 美式普通期权 | Bjerksund-Stensland 近似、CRR 二叉树法、有限差分法、蒙特卡洛法 |
| 现金或无、资产或无数字期权 | 解析法、有限差分法、积分法 |
| 障碍期权 | 解析法、有限差分法 |
| 二元障碍期权和触碰期权 | 解析法 |
| 几何平均亚式期权 | 闭式解 |
| 算术平均亚式期权 | Turnbull-Wakeman 近似 |
| 累购产品 | 有限差分法、蒙特卡洛法 |
| 凤凰产品和各类雪球结构 | 有限差分法、蒙特卡洛法 |

上表根据 kiyosi 0.11.0 的公开引擎和[产品说明](https://github.com/lilkui/kiyosi/blob/main/README.md#支持的产品与功能)整理。雪球和凤凰产品共用 `FiniteDifferenceAutocallableEngine` 或 `MonteCarloAutocallableEngine`，累购产品仍使用各自的引擎。完整签名见[定价 API](/api/python/kiyosi-pricing)。

`AnalyticBarrierEngine` 和 `AnalyticBinaryBarrierEngine` 使用 BGK 障碍平移近似处理离散观察。对于尚未触碰障碍、且仍有未来观察日的合约，最后一次观察必须安排在到期日，现价也必须位于平移后障碍的未触碰一侧。不满足支持条件时，引擎会抛出类别为 `UNSUPPORTED_OPERATION` 的 `KiyosiError`。详见[定价 API](/api/python/kiyosi-pricing#analyticbarrierengine)。

## 引擎配置与验证 {#engine-settings}

Python 数值引擎在构造时验证配置。二叉树步数须为 1–1,000,000；蒙特卡洛路径数须为 1–10,000,000，普通期权的 `step_count` 须为 2–10,000，美式期权在到期前定价时至少需要 3 步。有限差分网格还受各引擎的上限约束。无效配置会在构造时抛出 `KiyosiError`，合约、市场和后端可用性则在定价时检查。

引擎配置只读。如需修改路径数、网格或后端，请创建新引擎。

## 选择计算后端 {#select-a-backend}

蒙特卡洛引擎默认使用 CPU。如需使用 CUDA，可沿用[首次定价](./first-price)中的 `option` 和 `context`：

```python
from kiyosi.pricing import MonteCarloVanillaEngine

engine = MonteCarloVanillaEngine(backend="cuda")
price = engine.price(option, context)
print(price)
```

使用 CUDA 需要启用了 CUDA 支持的 kiyosi 构建，以及兼容的 NVIDIA GPU 和驱动。默认后端是 `"cpu"`。CUDA 仅用于蒙特卡洛方法，解析引擎和有限差分引擎不会因此转到 GPU 上运行。所选后端不可用时，会抛出类别为 `BACKEND_UNAVAILABLE` 的 `KiyosiError`。

## CPU 并发与复现 {#cpu-concurrency}

三个蒙特卡洛引擎均支持 `thread_count`，用于限制单次 CPU 调用的并发数：`0` 为自动选择，`1` 为串行，正整数为并发上限。它不限制整个进程的线程总数。沿用首次定价的对象：

```python
from kiyosi.pricing import MonteCarloVanillaEngine

engine = MonteCarloVanillaEngine(seed=42, thread_count=4)
estimate = engine.price(option, context)
print(estimate)
```

固定种子时，同一库版本、构建和标准库实现下的 CPU 结果不随线程数改变；不保证跨版本或 CPU / CUDA 结果一致。CUDA 要求 `thread_count=0`。并发调用可共享只读引擎，每次调用会同步完成自己的计算。

## 如何比较定价方法 {#compare-methods-carefully}

比较不同引擎时，应使用相同的合约条款和市场输入。解析法直接按公式计算，数值方法则会引入近似误差或模拟误差。各引擎的具体设置见[定价模块](https://github.com/lilkui/kiyosi/blob/main/python/kiyosi/pricing.py)和[定价测试](https://github.com/lilkui/kiyosi/tree/main/tests/pricing)。

当前所有模型的适用范围均受 [Black-Scholes-Merton 模型假设](./introduction#model-scope)限制。
