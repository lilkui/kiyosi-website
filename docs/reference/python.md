---
description: 了解 kiyosi 的 instruments、market 和 pricing 模块，以及历史、时间戳、Greeks 和并发约定。
---

# Python API 概览

本页对应 **kiyosi 0.20.0**，按合约、市场输入和定价结果组织常用接口。完整签名、属性和方法见 [Python API 参考](/api/python/)，其中的英文说明来自源码文档字符串。

## `kiyosi.instruments`

该模块定义金融工具、结构化产品预设与观察记录。`OptionType` 等用于指定选项的类型是 `typing.Literal` 类型别名，调用时直接传入小写字符串。

产品包括欧式与美式普通期权、数字期权、亚式期权、单／双障碍期权、触碰期权、雪球、凤凰、累购及区间累计。产品与算法的对应关系见[引擎支持范围](../guide/engines#instrument-coverage)。

### 结构化产品与观察记录

`standard_phoenix()` 和 `step_down_phoenix()` 提供标准与降敲凤凰，`coupon_per_period` 表示每个合格观察时点支付的每期绝对票息率。`lockout_periods` 设置前若干期的敲出锁定期，期间票息与敲入观察仍有效。锁定期后须至少保留一次可敲出观察，降敲障碍从首次允许敲出的观察开始递减。`PhoenixOption` 分别保存敲出观察（`KnockOutObservation`、`knock_out_observations` / `knock_out_times`）与派息观察（`CouponObservation`、`coupon_observations` / `coupon_times`），可独立修改其中一组列表。

`fixed_coupon_note()`（FCN）和 `digital_coupon_note()`（DCN）返回 `PhoenixOption`，使用每期票息 `coupon_per_period`，仅在到期时观察敲入。

`early_profit_snowball()` 和 `butterfly_snowball()` 分别提供两段和三段年化票息。阶段截止时刻归入前一阶段；敲出时，将所选阶段的票息率用于整个持有期，到期则使用最后阶段的票息率。

雪球和凤凰的价格按单位原始名义本金计量，表示尚未结算的现金流现值，包含条款规定的本金、票息、返息及损失。`principal_redemption_ratio` 是归一化本金偿还比例；`rebate_rate` 为单位名义本金的固定返息，`annual_rebate_rate` 为按 Actual/365 Fixed 从生效日计息至实际敲出或到期的年化返息率。使用持仓名义本金时，需在外部同时缩放完整价格和 Greeks。

`Accumulator` 默认 `option_type="call"` 表示累购，`"put"` 表示累沽。`knock_out_observation_times=None` 表示每个交易日按显式的 `observation_clock_time` 观察敲出，空序列表示不提前敲出；显式时间须严格递增且位于合约期限内。每次观察先判定敲出，触发敲出时结束累计。

`AutocallableObservation.snowball()` 构造雪球专用的敲出观察记录；`autocallable_observations()` 可从等长数组构建记录。雪球合约的 `autocall_observations`、`autocall_times` 分别返回记录与时间戳。

敲入观察单独使用 `KnockInObservation.every_trading_day(time(...))` 或 `.at_expiry()` 设置；每日敲入的预设工厂要求显式传入 `knock_in_observation_clock_time`。直接构造自动赎回合约时，必须显式提供 `calendar`；预设工厂可以继承日程的日历。

### 障碍与触碰产品 {#barrier-and-touch-contracts}

`BarrierOption` 和 `DoubleBarrierOption` 描述带行权价的单／双障碍普通期权。`BinaryBarrierOption` 描述带行权条件的二元障碍支付；`TouchOption` 不含行权价，按是否触碰支付。后两者使用必填的 `payoff_type="cash"` 或 `"asset"` 选择支付类型，现金支付必须提供正数 `payout`，资产支付不接受该金额。

`TouchOption` 的 `barrier_type="up_and_in"` 或 `"down_and_in"` 表示单触碰，`"up_and_out"` 或 `"down_and_out"` 表示单不触碰。`DoubleTouchOption` 仅支付现金：`barrier_type="knock_in"` 表示触及任一边界支付，`"knock_out"` 表示始终未触及两侧边界支付。默认在到期结算；`settlement_timing="at_hit"` 仅适用于触碰后支付的合约。

沿用[首次定价](../guide/first-price)的 `option` 和 `context`：

```python
from kiyosi.instruments import DoubleTouchOption, TouchOption
from kiyosi.pricing import AnalyticBinaryBarrierEngine, AnalyticDoubleTouchEngine

touch = TouchOption(
    effective_time=option.effective_time, expiry_time=option.expiry_time,
    barrier_level=120.0, barrier_type="up_and_in",
    payoff_type="cash", payout=10.0, settlement_timing="at_hit",
)
no_touch = DoubleTouchOption(
    effective_time=option.effective_time, expiry_time=option.expiry_time,
    lower_barrier=80.0, upper_barrier=120.0,
    barrier_type="knock_out", payout=10.0,
)
print(AnalyticBinaryBarrierEngine().price(touch, context))
print(AnalyticDoubleTouchEngine().price(no_touch, context))
```

标的价格等于障碍水平时，也计为触碰。`observation_times=None` 表示连续监控，非空时间序列表示离散监控；只读属性 `observation_mode` 返回 `"continuous"` 或 `"scheduled"`。连续监控的 `observation_times` 和 `observation_schedule` 均为 `None`。

离散监控合约的 `observation_schedule` 可作为另一合约的 `observation_times` 传入，同时保留日历。单独传递时间戳元组时，需显式转交 `calendar`。各引擎的监控模式支持范围见[金融工具 API](/api/python/kiyosi-instruments)和[定价 API](/api/python/kiyosi-pricing)。

### 历史与替换 {#history-and-replacement}

产品的 `replace()` 返回经过验证的新对象，原对象不变。省略字段或传入 `...`（`Ellipsis`）时保留原值；`None` 将可空字段清为未知，必填字段要求具体值。

条款与历史一起验证，未指定的历史字段各自保留原值。修改条款时，需按新条款核对并更新历史字段。可替换字段见[金融工具 API](/api/python/kiyosi-instruments)。

历史描述估值时点**严格之前**的事件；恰好在估值时点的观察使用当前现价处理一次。缺失历史表示未知；已知的零、未触碰或未敲出状态需显式传入。

| 产品 | 历史字段 |
| --- | --- |
| 障碍与触碰产品 | `touch_state` |
| 自动赎回产品 | `barrier_state` |
| 亚式期权 | 已实现平均价 `realized_average` |
| 区间累计 | 已实现命中次数 `realized_hit_count` |
| 累购／累沽 | `accumulated_quantity`、`knock_out_settled` |

`barrier_state="knocked_out"` 和 `knock_out_settled=True` 表示此前已敲出并结算。

`RangeAccrualOption` 在构造和 `replace()` 时要求 `realized_hit_count` 不超过到期时点严格之前的观察次数，定价时进一步要求不超过估值时点严格之前的观察次数。到期时刻本身的观察不计入历史。

定价前，需按估值时点整理历史快照，确保其与合约条款、结算进度一致，并随合约传入。定价使用该快照，缺少必需历史时抛出 `MissingHistoryError`。计算数值时间敏感度时，所提供的历史保持固定。

## `kiyosi.market`

该模块提供市场输入、利率曲线、估值上下文、日历和观察日程。

`BlackScholesMertonParameters` 接收无风险利率、股息率和非负恒定波动率，零波动率使用确定性定价；`LocalVolatilityParameters` 使用局部波动率曲面；`HestonParameters` 描述随机方差过程。

三种模型的利率和股息率可以是连续复利标量，也可以是 `RateTermStructure`。三者均接受 `time_convention`（默认 `"actual_365_fixed"`）与 `calendar` 参数；BSM 和局部波动率的一维有限差分引擎支持 `time_convention="business"` 并指定 `calendar`，实现波动率交易时间与利率自然时间的双时钟 PDE 定价。`PricingContext` 将模型参数与 `spot_price`、`valuation_time` 组合为估值上下文。

### 利率期限结构 {#rate-curves}

`RateTermStructure` 根据参考时点、节点时点和因子构建，在对数空间对因子做线性插值，时间采用 Actual/365 Fixed。查询节点曲线时，查询时点必须位于其覆盖范围内：

```python
from datetime import datetime
from kiyosi.market import BlackScholesMertonParameters, RateTermStructure

curve = RateTermStructure(
    reference_time=datetime(2025, 1, 1),
    times=[datetime(2026, 1, 1)],
    factors=[0.95],
)
model = BlackScholesMertonParameters(
    risk_free_rate=curve,
    dividend_yield=0.02,
    volatility=0.20,
)
```

`RateTermStructure.flat()` 构造无上界的恒定曲线；同时需要精确恒定利率和双端覆盖范围时，使用 `RateTermStructure.bounded_flat(rate, reference_time=..., max_time=..., calendar=...)`。传入 `calendar` 时，按各开市日经过的时段与该日历年化基准的比值计息，休市日计息为零。恒定性按实际远期利率判断，节点因子舍入会影响计算出的远期利率。

转交模型利率时，使用 `risk_free_curve` 和 `dividend_curve` 保留覆盖范围。`flat_risk_free_rate`、`flat_dividend_yield` 返回恒定曲线的标量，非恒定曲线会抛出异常。

### 更新市场输入 {#replace-market-inputs}

模型参数和上下文只读。`replace()` 创建经过验证的新对象，省略字段或传入 `...` 保持原值，更新字段需提供具体值。沿用[首次定价](../guide/first-price)的 `context`：

```python
stressed = context.replace(
    spot_price=105.0,
    model_parameters=context.model_parameters.replace(volatility=0.25),
)
```

### 局部波动率 {#local-volatility}

`LocalVolatilitySurface` 保存矩形网格，行对应时间，列对应绝对标的价格。时间与价格各须至少两个节点，且各自严格递增；价格和波动率必须为正有限值。

波动率按时间和价格做双线性插值，价格超出网格时使用端点值，查询时间须位于网格覆盖范围内。曲面节点固定在绝对价格和时间坐标上，改变上下文的现价或估值时点后仍使用这些坐标。

沿用[首次定价](../guide/first-price)的 `option` 和 `context`：

```python
from kiyosi.market import LocalVolatilityParameters, LocalVolatilitySurface
from kiyosi.pricing import FiniteDifferenceVanillaEngine

surface = LocalVolatilitySurface(
    times=[option.effective_time, option.expiry_time],
    spots=[80.0, 100.0, 120.0],
    values=[[0.24, 0.20, 0.22], [0.23, 0.21, 0.22]],
)
local_context = context.replace(
    model_parameters=LocalVolatilityParameters(
        risk_free_rate=0.05,
        dividend_yield=0.02,
        surface=surface,
    ),
)
local_result = FiniteDifferenceVanillaEngine().price_with_greeks(
    option, local_context, greeks=["delta", "gamma"],
)
print(local_result.price, local_result.delta, local_result.gamma)
```

一维有限差分的所有产品族均可计算该模型的价格，以及固定绝对曲面下的 delta、gamma；其他 Greeks 返回 `None`，状态为 `unsupported`。到期时，Greeks 按支付函数判断；导数无定义或数值模板不可用时也返回 `None`，可用 `status()` 区分原因。数字期权有限差分要求利率和股息率为恒定曲线。

自动赎回有限差分支持该模型的隐含票息求解。局部波动率模型的定价入口为一维有限差分引擎，Greeks 通过其 `price_with_greeks()` 请求；`numerical_greeks()` 与隐含波动率求解适用于 BSM 标量波动率。

曲面须覆盖剩余随机演化时段，利率须覆盖所需折现时段。自动空间边界使用该演化时段内插值后的最大局部波动率。分别细化时间、空间网格并扩大边界，比较价格与 Greeks 的变化，以检查收敛性。

### Heston 模型 {#heston}

`HestonParameters` 保存风险中性下的恒定方差过程参数。`initial_variance` 是估值时点的方差，20% 初始波动率对应 `0.04`；`long_run_variance` 是长期方差，`mean_reversion_speed` 是按年计量的均值回复速度，`vol_of_vol` 是方差过程的波动系数，`correlation` 是标的与方差布朗运动的相关系数。

四个方差过程参数须为非负有限值，相关系数须位于 `[-1, 1]`（包含端点），不要求满足 Feller 条件 `2 * mean_reversion_speed * long_run_variance >= vol_of_vol**2`。模型只读，可用 `replace()` 创建经过验证的新值。

沿用[首次定价](../guide/first-price)的 `option` 和 `context`：

```python
from kiyosi.market import HestonParameters
from kiyosi.pricing import (
    AnalyticHestonEuropeanEngine,
    FiniteDifferenceHestonVanillaEngine,
)

heston_context = context.replace(
    model_parameters=HestonParameters(
        risk_free_rate=0.05,
        dividend_yield=0.02,
        initial_variance=0.04,
        long_run_variance=0.04,
        mean_reversion_speed=1.5,
        vol_of_vol=0.3,
        correlation=-0.7,
    ),
)
print(AnalyticHestonEuropeanEngine().price(option, heston_context))
print(FiniteDifferenceHestonVanillaEngine().price(option, heston_context))
```

Fourier 积分引擎计算欧式普通期权价格，二维有限差分引擎还可计算美式普通期权价格。两者均支持确定性利率曲线、零方差参数及相关系数端点。

`price_with_greeks()` 返回价格，将请求的 Greeks 标记为 `unsupported`。引擎仍会验证传入的扰动控制，并使用模型自身的算法计算价格。

Heston 定价使用这两个专用引擎，`numerical_greeks()` 和隐含参数求解对该模型抛出 `UnsupportedOperationError`。积分容差、评估预算、网格与边界设置见 [Heston 定价](../guide/engines#heston-pricing)。

### 日历与观察日程 {#calendars-and-schedules}

`weekdays_calendar()`、`all_days_calendar()` 和 `sse_calendar()` 提供内置日历（其中工作日日历的年化基准为 261 天）。`custom_calendar()` 可在基础日历上覆盖开市日和休市日，两组日期须互斥。交易年分母来自日历，利率曲线默认使用 Actual/365 Fixed。

```python
from datetime import date, datetime, time
from kiyosi.market import custom_calendar, monthly_schedule, weekdays_calendar

calendar = custom_calendar(
    base=weekdays_calendar(),
    closed_dates=[date(2025, 2, 3)],
    open_dates=[date(2025, 2, 8)],
)
schedule = monthly_schedule(
    start_time=datetime(2025, 1, 1),
    end_time=datetime(2025, 4, 1, 15),
    first_observation_month=1,
    observation_clock_time=time(15),
    calendar=calendar,
)
```

`first_observation_month=1` 表示从起始时刻后一个月开始观察。月末会按原始锚点处理，并按日历调整，再应用显式的 `observation_clock_time`。也可用 `ObservationSchedule(times=..., start_time=..., end_time=...)` 验证不规则时间序列。

`ObservationSchedule` 支持迭代、`reversed()`、长度、整数索引（含负数）和切片。正向与反向迭代按需产生时间戳，并保留所属日程对象。切片返回保留原日历的独立日程，不接受递减选择；布尔索引抛出 `TypeError`，越界索引抛出 `IndexError`。

接收日程的合约会继承其日历，也可显式传入 `calendar` 覆盖；普通列表与元组不携带日历。日程边界和日历约定见[市场 API](/api/python/kiyosi-market)。

## `kiyosi.pricing`

该模块提供解析与数值引擎、Greeks、隐含波动率和隐含票息求解器。

欧式解析定价使用 `AnalyticEuropeanEngine`；CPU 蒙特卡洛定价可用 `MonteCarloVanillaEngine`，单／双障碍产品共用 `MonteCarloBarrierEngine`。`price(option, context)` 直接返回 `float`。有限差分引擎还提供 `solve(instrument, context, spot_range=...)` 返回可复用的 `FiniteDifferenceSolution`，用于批量查询不同现价下的价格与 Greeks。

引擎只读。构造字段可配置的引擎支持 `engine.replace(...)`，用于创建新引擎并执行构造验证；省略配置或传入 `...` 时保留原值，`None` 只用于可空配置。无配置字段的解析引擎可直接构造使用。

### Greeks 与结果状态

调用 `price_with_greeks()` 时必须传入 `greeks`，可用单个名称、名称序列或 `"all"`；空序列仅请求价格。该方法返回只读的 `PricingResult`。

共有十二项指标：delta、gamma、speed、theta、charm、color、vega、volga、vanna、zomma、rho、dividend_rho。各指标均为未缩放偏导，波动率与利率使用小数单位，估值时间使用年（Actual/365 Fixed），其余输入保持不变。Rho 与 dividend_rho 分别对应无风险利率曲线和股息率曲线的平行移动。

不可用指标为 `None`，用 `result.status(name)` 查询原因：

| 状态 | 含义 |
| --- | --- |
| `available` | 有可用数值 |
| `not_requested` | 未请求该指标 |
| `unsupported` | 引擎或模型不支持 |
| `undefined` | 当前估值下导数无定义 |
| `stencil_unavailable` | 数值差分模板不可用，可尝试调整扰动 |

即使所有请求的指标均为 `unsupported`，结果仍包含价格与指标状态。`requested` 和 `supported` 分别列出请求的指标名称和引擎／模型支持的指标名称；`result.require(name)` 返回指标数值，无数值时则抛出带 `greek` 和 `status` 属性的 `GreekUnavailableError`。

### Greeks 扰动控制 {#greek-controls}

`engine.greek_method(instrument, context)` 查询估计方法，`engine.active_greek_controls(instrument, context)` 查询可能使用的扰动控制。`price_with_greeks()` 使用原生估计方法，通过扰动控制调节数值回退及可用性检查；`numerical_greeks()` 显式选择 BSM 标量数值差分。

两种调用都可在每次请求中指定以下扰动控制：

| 参数 | 单位 | 默认设置 |
| --- | --- | --- |
| `spot_shift` | 标的价格单位的绝对扰动 | 自动选择 |
| `volatility_shift` | 小数单位 | 自动选择，步长为 `min(0.0001, volatility / 2)` |
| `rate_shift` | 小数单位 | `0.0001`，要求具体数值 |
| `time_shift` | 正的 `datetime.timedelta` | 自动选择，至多一天，并缩短以避开观察事件 |

省略扰动控制或传入 `...` 时使用共享默认值；现价、波动率和时间扰动的 `None` 表示自动选择。显式指定时间扰动时使用给定步长，所有显式控制都会验证。引擎构造函数和 `replace()` 接收网格、积分或采样配置。

沿用[首次定价](../guide/first-price)的 `engine`、`option` 和 `context`：

```python
from datetime import timedelta
from kiyosi.pricing import numerical_greeks

print(engine.greek_method(option, context))
print(engine.active_greek_controls(option, context))
numerical_result = numerical_greeks(
    engine, option, context, greeks=["delta", "gamma", "vega", "theta"],
    spot_shift=0.01, volatility_shift=0.0001,
    rate_shift=0.0001, time_shift=timedelta(hours=1),
)
print(numerical_result.price, numerical_result.require("delta"))
```

`QuadratureVanillaEngine` 和 `QuadratureDigitalEngine` 使用恒定利率 BSM，提供价格与数值 Greeks；单／双障碍蒙特卡洛的原生 Greeks 仅支持 delta、gamma。配置与收敛检查见[定价引擎](../guide/engines)。

### 隐含参数 {#implied-parameters}

调用 `implied_volatility()` 时，需显式提供 `lower_bound` 和 `upper_bound`，指定波动率根的搜索区间。数字与障碍产品可能有多个根，可通过搜索区间选择目标根。容差控制所选引擎价格曲线上的求根精度，引擎本身的数值精度需通过[收敛与采样检查](../guide/engines#compare-methods-carefully)评估。

以下示例沿用[首次定价](../guide/first-price)中的对象：

```python
from kiyosi.pricing import implied_volatility

sigma = implied_volatility(
    engine, option, context, observed_price=engine.price(option, context),
    lower_bound=0.1, upper_bound=0.3,
)
print(sigma)
```

`implied_snowball_coupon()` 返回包含年化 `first_observation_coupon` 和 `quote_convention` 的字典。必填的 `quote_convention` 可为 `"shift_maturity_coupon"`（同步平移到期票息）或 `"preserve_maturity_coupon"`（固定到期票息）；用 `note.with_coupon(**quote)` 应用报价，保留各观察票息的利差。

`implied_phoenix_coupon()` 返回包含 `coupon_per_period` 的字典，同样可用 `note.with_coupon(**quote)` 应用。凤凰、FCN／DCN 的求解边界、容差和返回值均使用每期绝对票息率。

蒙特卡洛求解需使用显式种子：先保存 `engine.with_resolved_seed()` 返回的引擎，再用它求解与回代，保持抽样一致。签名、单位和参数要求见[定价 API](/api/python/kiyosi-pricing)。

## 错误处理与并发 {#errors-and-concurrency}

领域错误均继承 `KiyosiError`，可以按异常类型处理：

| 异常 | 含义 |
| --- | --- |
| `InvalidInputError` | 参数、日期、日程或历史不合法 |
| `MissingHistoryError` | 缺少必需历史，继承 `InvalidInputError` |
| `UnsupportedOperationError` | 不支持的定价组合或不可用的结果指标 |
| `GreekUnavailableError` | 请求的 Greek 无数值，继承 `UnsupportedOperationError` |
| `ComputationFailureError` | 数值结果非有限或计算状态不可用 |
| `RootNotBracketedError` | 给定区间没有包围根 |
| `NonConvergenceError` | 迭代或积分未收敛 |

`InvalidInputError` 同时继承 `ValueError`。表示和调用签名错误使用 Python 原生异常，运行环境报告的错误使用 `OSError`。可按异常类型分类处理，通过错误文本诊断原因。

启用 Rust 栈展开时，panic 抛出继承 `BaseException` 的 `pyo3_runtime.PanicException`；终止式 panic 和内存耗尽可能终止进程。

### 时间与数值输入

| 输入 | 类型与约定 |
| --- | --- |
| 合约、估值、曲线和观察时间 | 无时区的 `datetime.datetime`，精度为微秒，所有输入采用同一时间基准 |
| 日历日期 | `datetime.date`，以纯日期传入 |
| 观察时钟 | 无时区的 `datetime.time` |

超出 Python 年份 1–9999 的结果抛出 `ValueError`。

数值输入拒绝布尔值和隐式舍入。精确实数必须能无损表示为浮点数，显式调用 `float(value)` 表示接受舍入。整数输入要求支持 `__index__`；传入小数时抛出 `TypeError`，超出范围时抛出 `OverflowError`。

集合属性返回自有元组，曲面使用嵌套元组。对象只读，支持 `copy` 与 `deepcopy`；不支持 `pickle`。

### 并发与取消

在 Python 层并行定价时，优先使用多线程（如 `concurrent.futures.ThreadPoolExecutor`）。共享或独立实例均支持并发读取和定价。长计算会释放 GIL，短调用可能保留 GIL。每次调用同步执行，正常完成后返回完整结果。

若必须使用多进程，请采用 `spawn` 启动方式并在各子进程内构造 kiyosi 对象，返回可序列化的基础数据；通过 `fork` 继承的蒙特卡洛线程池不可用。

长请求中，调用线程会轮询信号。收到 `KeyboardInterrupt` 等信号处理异常后，会协作取消计算，等待工作停止后再传播异常。取消响应时间受内存分配和单个工作单元耗时影响。完整约定见[包级参考](/api/python/kiyosi)。

## 实用示例 {#working-examples}

- [首次定价](../guide/first-price)：完整 Python 脚本与 Greeks。
- [采样与误差估计](../guide/engines#sampling-and-error)：蒙特卡洛统计接口。
- [上游 Python 示例](https://github.com/lilkui/kiyosi/tree/be67a2427fbf3cb14de6d7e03c83eff2473d0c28/examples/python)：产品定价、历史输入、日历和票息求解。
- [上游 Python 测试](https://github.com/lilkui/kiyosi/tree/be67a2427fbf3cb14de6d7e03c83eff2473d0c28/python/tests)：更多产品用法。
