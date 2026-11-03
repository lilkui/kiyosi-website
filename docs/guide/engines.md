---
description: 按产品选择 kiyosi 定价算法，配置数值方法和 CPU 蒙特卡洛采样。
---

# 定价引擎

请按金融工具类型选择引擎。虽然各引擎都使用 `price(instrument, context)` 接口，但支持的产品和模型条件不同。本页对应 kiyosi **0.17.0**。

## 支持的产品与方法 {#instrument-coverage}

| 产品类型 | 可用定价方法 |
| --- | --- |
| 欧式普通期权 | BSM 解析法、积分、CRR 二叉树、有限差分、蒙特卡洛；Heston Fourier 积分与二维有限差分 |
| 美式普通期权 | Bjerksund–Stensland 2002 近似、积分、CRR、有限差分、最小二乘蒙特卡洛；Heston 二维有限差分 |
| 现金或无、资产或无数字期权 | 解析法、积分、CRR、有限差分、蒙特卡洛 |
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

双触碰类产品可用 `AnalyticDoubleTouchEngine`。表中未标注模型的方法适用于 BSM；局部波动率仅支持一维有限差分，详见[局部波动率](../reference/python#local-volatility)。Heston 使用专用引擎，详见 [Heston 定价](#heston-pricing)。

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

一维有限差分在自动选择空间边界且使用非显式格式时，为欧式普通期权和局部波动率数字期权在行权价附近集中布点；BSM 数字期权和显式指定上边界时使用均匀标的网格，美式期权使用双曲正弦网格。自动赎回有限差分引擎默认 `asset_step_count=800`、`time_step_count=400`；观察事件与平滑可能增加子步，仍须验证网格收敛。

## 普通与数字期权积分 {#quadrature-pricing}

`QuadratureVanillaEngine` 支持欧式和美式普通期权，`QuadratureDigitalEngine` 支持欧式现金或无、资产或无数字期权；两者均要求 BSM 参数中的无风险利率和股息率显式为平坦曲线。

沿用[首次定价](./first-price)中的 `option` 和 `context`：

```python
from kiyosi.pricing import QuadratureVanillaEngine

engine = QuadratureVanillaEngine(
    asset_step_count=512,
    time_step_count=200,
    integration_standard_deviations=8.0,
)
print(engine.price(option, context))
```

欧式定价采用复合 Simpson 积分；美式普通期权使用高斯积分反向递推，在估值时点、均匀时间网格与到期时点允许行权。`time_step_count` 至少为 1，仅用于美式普通期权；欧式普通期权忽略此参数，数字期权引擎不接受此参数。两者的空间步数至少为 4，积分范围须为正有限值。

数字期权的积分范围以支付加权正态密度为中心，截断范围外的贡献按零处理；到期时现价等于行权价不支付。应分别检查空间步数、积分范围、美式行权时间步及数值 Greeks 扰动的收敛性；固定网格计算完成不提供误差估计。

`QuadratureAutocallableEngine` 的空间范围同时考虑正向漂移和事件边界的反向移动。低波动率、每日观察等情况下，应分别检查空间分辨率和积分范围。

## Heston 定价 {#heston-pricing}

使用 [Heston 市场上下文](../reference/python#heston)时，欧式普通期权可选 `AnalyticHestonEuropeanEngine`，欧式和美式普通期权均可选 `FiniteDifferenceHestonVanillaEngine`。这两个引擎只计算价格；Greeks 与隐含参数求解会抛出 `UnsupportedOperationError`，其他引擎不接受 Heston 模型。

Fourier 积分引擎采用自适应积分和确定性方差控制变量，默认 `absolute_tolerance=1e-8`、`relative_tolerance=1e-8`、`max_evaluations=10000`。绝对容差按价格单位计量，两种容差均须为非负有限值且至少一个为正；评估预算须为正整数，覆盖一次请求中的特征函数、控制变量与尾部检查。预算或数值分辨率不足会抛出 `NonConvergenceError`。到期与确定性方差分支不消耗积分预算；误差估计不保证所有参数下的精度，尾部价格尤其需要收敛检查。

二维有限差分使用修正 Craig–Sneyd（MCS）交替方向隐式（ADI）格式，美式行权使用 Ikonen–Toivanen 分裂。默认标的、方差和时间区间数分别为 400、100、400；空间区间数至少为 3，时间区间数至少为 1，利率曲线节点会加入时间网格。`asset_upper_boundary` 和 `variance_upper_boundary` 默认为 `None`，由引擎自动选择；显式边界须为正有限值，并在需要相应数值网格时严格高于现价与行权价、或初始方差。应分别检查空间、时间细化和边界扩大后的收敛性，计算完成不提供误差估计。

Heston 二维有限差分的设置独立于一维引擎，不接受 `scheme` 参数；局部波动率模型使用一维有限差分引擎。

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

美式蒙特卡洛行权网格每次调用最多保留 1 GiB 路径数据，大小为 `8 * path_count * (step_count - 1)` 字节；对偶采样的奇数路径数按下一偶数预留，其他缓冲区另计。超限时在抽样前抛出 `InvalidInputError`，需减少路径数或时间步数。到期定价，以及股息率非正且利率非负、仅需终值采样的美式看涨期权，不分配该网格，也不受此限额约束。

未来的障碍、敲入、敲出、票息和加速观察使用模拟的对数价格变化进行判定，即使还原后的现价因浮点舍入恰好等于阈值；单／双障碍期权的到期收益也保留此精度。估值时点的观察仍使用传入的现价。

## 如何比较定价方法 {#compare-methods-carefully}

使用相同的合约条款、估值时点与市场输入。数值方法引入离散或模拟误差，需要分别检查网格收敛与采样误差。隐含参数求解器的容差不能衡量蒙特卡洛误差。

模型范围见[简介](./introduction#model-scope)。产品与算法表依据[上游 README](https://github.com/lilkui/kiyosi/blob/aa80d636ef804deff7daf0a4db355c7f70a781c0/README.md#支持的产品与算法)整理，更多用例见[Python 测试](https://github.com/lilkui/kiyosi/tree/aa80d636ef804deff7daf0a4db355c7f70a781c0/python/tests)。
