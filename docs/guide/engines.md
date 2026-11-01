---
description: 按产品选择 kiyosi 定价算法，配置数值方法和 CPU 蒙特卡洛采样。
---

# 定价引擎

请按金融工具类型选择引擎。虽然各引擎都使用 `price(instrument, context)` 接口，但支持的产品和模型条件不同。本页对应 kiyosi **0.16.0**。

## 支持的产品与方法 {#instrument-coverage}

| 产品类型 | 可用定价方法 |
| --- | --- |
| 欧式普通期权 | BSM 解析法、CRR 二叉树、有限差分、蒙特卡洛 |
| 美式普通期权 | Bjerksund–Stensland 2002 近似、CRR、有限差分、最小二乘蒙特卡洛 |
| 现金或无、资产或无数字期权 | 解析法、CRR、有限差分、蒙特卡洛 |
| 几何平均亚式期权 | 连续平均解析法、蒙特卡洛 |
| 算术平均亚式期权 | Turnbull–Wakeman 连续平均近似、蒙特卡洛 |
| 单障碍期权 | 解析法、CRR、积分、有限差分、蒙特卡洛 |
| 双障碍期权 | 解析级数、有限差分、蒙特卡洛 |
| 二元障碍、单触碰、单不触碰期权 | 解析法、有限差分 |
| 双触碰、双不触碰期权 | 解析级数、有限差分 |
| 雪球、二元雪球、三元雪球、凤凰、FCN、DCN | 积分、有限差分、蒙特卡洛 |
| 累购／累沽 | 积分、有限差分、蒙特卡洛 |
| 区间累计 | BSM 区间概率解析求和 |

雪球和凤凰共用 `QuadratureAutocallableEngine`、`FiniteDifferenceAutocallableEngine` 或 `MonteCarloAutocallableEngine`。累购使用对应的 `AccumulatorEngine`。欧式解析引擎为 `AnalyticEuropeanEngine`。完整名称、参数及支持条件见[定价 API](/api/python/kiyosi-pricing)。

双触碰类产品可用 `AnalyticDoubleTouchEngine`。上表描述 BSM 模型下的支持范围；局部波动率仅支持有限差分，详见[局部波动率](../reference/python#local-volatility)。

## 引擎配置与验证 {#engine-settings}

数值引擎在构造时验证配置，合约与市场条件在定价时验证。引擎配置只读；调整网格或采样时，创建新引擎。

有限差分默认使用 `"rannacher"`：前两个时间区间分别用两个隐式 Euler 半步替代，并在日程中的障碍、累购或自动赎回观察后重新平滑。`"crank_nicolson"` 表示不进行时间步平滑的标准 Crank–Nicolson 格式；另可选 `"explicit_euler"` 和 `"implicit_euler"`。

例如，显式选择默认的 Rannacher 格式：

```python
from kiyosi.pricing import FiniteDifferenceVanillaEngine

engine = FiniteDifferenceVanillaEngine(
    asset_step_count=400,
    time_step_count=800,
    scheme="rannacher",
)
```

输入不合法时会抛出 `InvalidInputError`；不受支持的产品或模型条件会抛出 `UnsupportedOperationError`。应根据各引擎的参考文档选择参数，不能仅凭共享的调用接口推断支持范围。

## CPU 并发与复现 {#cpu-concurrency}

蒙特卡洛在 CPU 上运行。并行调用共用库持有的 Rayon 线程池，首次使用时按可用 CPU 数量初始化，并保留到进程退出。`thread_count=0` 自动选择参与计算的线程数，`1` 在调用线程上串行执行，正整数限制单次调用使用的工作线程数；它不限制整个进程的线程数，也不预留工作线程。线程池忽略 `RAYON_NUM_THREADS`，不修改应用的全局 Rayon 池。沿用[首次定价](./first-price)中的对象：

```python
from kiyosi.pricing import MonteCarloVanillaEngine

engine = MonteCarloVanillaEngine(seed=42, thread_count=4)
estimate = engine.price(option, context)
print(estimate)
```

固定种子时，同一构建中的随机抽样不随线程数改变；不保证跨版本或构建完全一致。每次调用同步完成自己的计算，可并发共享只读引擎。

使用 Python 多进程时选择 `spawn` 启动方式；线程池初始化后再 `fork`，子进程中的该池将无法使用。

## 采样与误差估计 {#sampling-and-error}

可选 `sampling="pseudo_random"` 或经过扰乱的 `"sobol"`。Sobol 要求路径数为二的幂；`antithetic=True` 将相反的正态随机数配对。欧式普通期权可使用统计接口：

```python
engine = MonteCarloVanillaEngine(path_count=100_000, seed=42)
result = engine.price_with_statistics(option, context)
print(result.price, result.standard_error, result.confidence_interval)
```

Sobol 采样不报告采样标准误差和置信区间，相应字段为 `None`。欧式普通期权直接采样终值，`step_count` 不影响其价格；美式期权使用离散行权网格。详细约束见 [MonteCarloVanillaEngine](/api/python/kiyosi-pricing#montecarlovanillaengine)。

`step_count` 仅由 `MonteCarloVanillaEngine` 和 `MonteCarloAsianEngine` 接受；其他蒙特卡洛引擎按各自的观察或监控日程计算。

## 如何比较定价方法 {#compare-methods-carefully}

使用相同的合约条款、估值时点与市场输入。数值方法引入离散或模拟误差，需要分别检查网格收敛与采样误差。隐含参数求解器的容差不能衡量蒙特卡洛误差。

模型范围见[简介](./introduction#model-scope)。产品与算法表依据[上游 README](https://github.com/lilkui/kiyosi/blob/2ec75ab8462bcef8f32bd32aba4468f78e7ee6a9/README.md#支持的产品与算法)整理，更多用例见[Python 测试](https://github.com/lilkui/kiyosi/tree/2ec75ab8462bcef8f32bd32aba4468f78e7ee6a9/python/tests)。
