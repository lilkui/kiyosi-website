---
description: 按产品选择 kiyosi 定价算法，配置数值方法和 CPU 蒙特卡洛采样。
---

# 定价引擎

按产品与市场模型选择引擎，再设置网格、积分或采样参数。各引擎统一使用 `price(instrument, context)` 接口。本页对应 kiyosi **0.19.0**。

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

数值引擎在构造时验证配置，在定价时验证合约与市场条件。引擎配置只读；构造字段可配置的引擎提供 `engine.replace(...)`，用于创建并验证新引擎。无配置字段的解析引擎可直接构造使用。

构造函数与 `replace()` 接收网格、积分或采样设置。Greeks 的 `spot_shift`、`volatility_shift`、`rate_shift` 和 `time_shift` 则在每次 `price_with_greeks()` 或 `numerical_greeks()` 请求中指定。省略扰动参数或传入 `...` 时使用共享默认值，详见 [Greeks 扰动控制](../reference/python#greek-controls)。

有限差分默认使用 `"rannacher"`：前两个时间区间分别用两个隐式 Euler 半步替代，并在日程中的障碍、累购或自动赎回观察后重新平滑。`"crank_nicolson"` 表示不做时间步平滑的标准 Crank–Nicolson 格式；另可选 `"explicit_euler"` 和 `"implicit_euler"`。

以下示例显式选择默认的 Rannacher 格式：

```python
from kiyosi.pricing import FiniteDifferenceVanillaEngine

engine = FiniteDifferenceVanillaEngine(
    asset_step_count=400,
    time_step_count=800,
    scheme="rannacher",
)
```

输入不合法时抛出 `InvalidInputError`；产品或模型条件超出引擎支持范围时抛出 `UnsupportedOperationError`。各引擎的参数和适用条件见[定价 API](/api/python/kiyosi-pricing)。

一维有限差分自动选择空间边界且使用非显式格式时，会在欧式普通期权和局部波动率数字期权的行权价附近集中布点。BSM 数字期权和显式指定上边界的情况使用均匀标的网格，美式期权使用双曲正弦网格。

自动赎回有限差分引擎默认使用 `asset_step_count=800`、`time_step_count=400`，观察事件与平滑可能增加子步。检查网格收敛性时，逐步增加空间和时间步数，比较价格与 Greeks 的变化。

## 普通与数字期权积分 {#quadrature-pricing}

`QuadratureVanillaEngine` 支持欧式和美式普通期权，`QuadratureDigitalEngine` 支持欧式现金或无、资产或无数字期权；两者均要求 BSM 参数中的无风险利率和股息率为恒定曲线。需要精确恒定且有覆盖边界的曲线时，可用 `RateTermStructure.bounded_flat()`。

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

欧式定价采用复合 Simpson 积分；美式普通期权使用高斯积分反向递推，允许在估值时点、均匀时间网格与到期时点行权。

`time_step_count` 至少为 1，仅用于美式普通期权；欧式普通期权忽略此参数，数字期权引擎不接受此参数。两个引擎的空间步数都至少为 4，积分范围须为正有限值。

数字期权的积分范围以支付加权正态密度为中心，截断范围外的贡献按零处理；到期时，现价等于行权价则不支付。

评估固定网格积分的精度时，分别增加空间步数、扩大积分范围、细化美式行权时间步，并调整数值 Greeks 扰动，比较结果变化以检查收敛性。

`QuadratureAutocallableEngine` 的空间范围同时考虑正向漂移和事件边界的反向移动。低波动率、每日观察等情况下，应分别检查空间分辨率和积分范围。

## 单／双障碍蒙特卡洛 {#barrier-monte-carlo}

`MonteCarloBarrierEngine` 同时接受 `BarrierOption` 和 `DoubleBarrierOption`，要求恒定利率与股息率的 BSM 模型。两种合约共用采样设置、种子、统计接口及 Greeks 接口；原生 Greeks 仅支持 delta 和 gamma。

沿用[首次定价](./first-price)的 `option` 和 `context`：

```python
from kiyosi.instruments import BarrierOption, DoubleBarrierOption
from kiyosi.pricing import MonteCarloBarrierEngine

single = BarrierOption(
    option_type="call", strike=100.0,
    effective_time=option.effective_time, expiry_time=option.expiry_time,
    barrier_level=120.0, barrier_type="up_and_out",
)
double = DoubleBarrierOption(
    option_type="call", strike=100.0,
    effective_time=option.effective_time, expiry_time=option.expiry_time,
    lower_barrier=80.0, upper_barrier=120.0, barrier_type="knock_out",
)
barrier_engine = MonteCarloBarrierEngine(path_count=131_072, seed=42)
for contract in (single, double):
    estimate = barrier_engine.price_with_statistics(contract, context)
    print(estimate.price, estimate.standard_error)
```

`observation_times=None` 表示连续监控，使用终值抽样与 Brownian bridge 存活概率；双障碍存活概率采用像方法／谱级数。显式传入非空观察时间序列时使用离散监控，模拟保留原始观察时点，必要时补充不作障碍观察的到期段。

引擎不接受 `step_count`。合约监控与历史输入见[障碍与触碰产品](../reference/python#barrier-and-touch-contracts)。

## Heston 定价 {#heston-pricing}

使用 [Heston 市场上下文](../reference/python#heston)时，欧式普通期权可选 `AnalyticHestonEuropeanEngine`，欧式和美式普通期权均可选 `FiniteDifferenceHestonVanillaEngine`。

这两个引擎只计算价格；`price_with_greeks()` 返回价格并将请求的 Greeks 标记为 `unsupported`。`numerical_greeks()` 与隐含参数求解抛出 `UnsupportedOperationError`，其他引擎不接受 Heston 模型。

Fourier 积分引擎采用自适应积分和确定性方差控制变量，默认 `absolute_tolerance=1e-8`、`relative_tolerance=1e-8`、`max_evaluations=10000`。绝对容差按价格单位计量，两种容差均须为非负有限值且至少一个为正；评估预算须为正整数，覆盖一次请求中的特征函数、控制变量与尾部检查。

预算或数值分辨率不足时抛出 `NonConvergenceError`；到期与确定性方差分支直接计算价格。检查积分收敛时，收紧容差并增加评估预算，比较价格变化，尤其关注尾部价格。

二维有限差分使用修正 Craig–Sneyd（MCS）交替方向隐式（ADI）格式，美式行权使用 Ikonen–Toivanen 分裂。默认标的、方差和时间区间数分别为 400、100、400；空间区间数至少为 3，时间区间数至少为 1，利率曲线节点会加入时间网格。

`asset_upper_boundary` 和 `variance_upper_boundary` 默认为 `None`，由引擎自动选择。显式边界须为正有限值；需要相应数值网格时，标的上边界须严格高于现价与行权价，方差上边界须严格高于初始方差。评估精度时，分别细化空间、时间网格并扩大边界，比较价格变化。

Heston 二维有限差分的设置独立于一维引擎，不接受 `scheme` 参数；局部波动率模型使用一维有限差分引擎。

## CPU 并发与复现 {#cpu-concurrency}

蒙特卡洛在 CPU 上运行。并行调用共用库持有的 Rayon 线程池，该池在首次并行使用时初始化，并保留到进程退出。

`max_active_workers=0` 自动选择活跃工作线程数，`1` 在调用线程上串行执行，正整数限制单次调用的活跃工作线程数。线程池大小由 `configure_monte_carlo_pool()` 单独配置，池中工作线程供并行调用共享。

如需限制该池在进程内创建的工作线程数，在首次并行请求前调用 `configure_monte_carlo_pool(max_workers=...)`。实际线程数还受可用 CPU 数限制；未配置时按可用 CPU 数选择。线程池忽略 `RAYON_NUM_THREADS`，不修改应用的全局 Rayon 池。

以下示例在新进程中沿用[首次定价](./first-price)的合约与上下文：

```python
from kiyosi.pricing import MonteCarloVanillaEngine, configure_monte_carlo_pool

configure_monte_carlo_pool(max_workers=4)
engine = MonteCarloVanillaEngine(seed=42, max_active_workers=4)
estimate = engine.price(option, context)
print(estimate)
```

同一构建中，固定种子可在不同线程数下复现随机抽样。复现实验时，保存使用的构建、引擎配置和实际种子。`engine.with_resolved_seed()` 返回带具体种子的独立引擎，保留其余设置；`price_with_seed()` 返回 `(price, seed)`，统计结果和 Greeks 结果也通过 `seed` 提供实际种子。无需抽样时，种子为 `None`。

每次调用同步完成自身计算，只读引擎可由并发调用共享。

使用 Python 多进程时选择 `spawn` 启动方式，让各子进程独立初始化线程池。

## 采样与误差估计 {#sampling-and-error}

可选 `sampling="pseudo_random"` 或经过扰乱的 `"sobol"`。Sobol 要求路径数为二的幂；`antithetic=True` 将相反的正态随机数配对。各蒙特卡洛产品引擎提供统计接口，普通期权引擎的统计接口仅支持欧式产品：

```python
engine = MonteCarloVanillaEngine(path_count=100_000, seed=42)
result = engine.price_with_statistics(option, context)
print(result.price, result.standard_error, result.confidence_interval)
print(result.seed, result.uncertainty_status)
```

伪随机独立样本或完整对偶样本对可提供标准误差和渐近 95% 正态置信区间。使用 Sobol、独立样本不足或对偶采样的路径数为奇数时，不报告不确定度，相应字段为 `None`；`uncertainty_status` 分别为 `unsupported_sampling`、`insufficient_observations` 或 `incomplete_antithetic_pair`。不确定度可用时，状态为 `available`。

欧式普通期权直接采样终值，`step_count` 不影响其价格；美式期权使用最小二乘蒙特卡洛，`step_count` 表示行权时间区间数，到期前至少为 2。详细约束见 [MonteCarloVanillaEngine](/api/python/kiyosi-pricing#montecarlovanillaengine)。

`step_count` 仅由 `MonteCarloVanillaEngine` 和 `MonteCarloAsianEngine` 接受；其他蒙特卡洛引擎按各自的观察或监控日程计算。

美式蒙特卡洛行权网格每次调用最多保留 1 GiB 路径数据，大小为 `8 * path_count * step_count` 字节；对偶采样的路径数为奇数时，按下一个偶数预留，其他缓冲区另计。超限时在抽样前抛出 `InvalidInputError`，需减少路径数或时间区间数。

到期、确定性定价，以及股息率非正且利率非负、仅需终值采样的美式看涨期权，不分配该网格，也不受此限额约束。

未来的障碍、敲入、敲出、票息和加速观察直接使用模拟的对数价格变化判定，以保留阈值附近的精度；单／双障碍期权的到期收益也使用这一精度。估值时点的观察使用传入的现价。

## 如何比较定价方法 {#compare-methods-carefully}

使用相同的合约条款、估值时点与市场输入，再按误差来源检查结果：

- **网格与积分误差**：逐步细化网格、扩大边界或收紧积分容差，比较价格与 Greeks 的变化。
- **采样误差**：使用 `price_with_statistics()` 查看可用的标准误差和置信区间，再增加路径数比较结果。
- **隐含参数求解误差**：求解器容差约束所选引擎价格曲线上的求根过程；使用蒙特卡洛时，同时检查采样误差。

模型范围见[简介](./introduction#model-scope)。产品与算法表依据[上游 README](https://github.com/lilkui/kiyosi/blob/fb6ea0f626e81b4e62beff9d9c8027855e94b015/README.md#支持产品与算法)整理，更多用例见[Python 示例](https://github.com/lilkui/kiyosi/tree/fb6ea0f626e81b4e62beff9d9c8027855e94b015/examples/python)与[测试](https://github.com/lilkui/kiyosi/tree/fb6ea0f626e81b4e62beff9d9c8027855e94b015/python/tests)。
