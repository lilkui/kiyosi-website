---
description: 了解 kiyosi 的 instruments、market 和 pricing 模块，以及历史、时间戳、Greeks 和并发约定。
---

# Python API 概览

本页对应 **kiyosi 0.18.0**。所有公开导出对象、运行时签名、属性和文档字符串均可在[完整 Python API 参考](/api/python/)中查阅。参考文档保留英文，与源码注释一致。

## `kiyosi.instruments`

该模块定义金融工具、结构化产品预设与观察记录。`OptionType` 等选择类型为 `typing.Literal` 类型别名，调用时直接传入小写字符串。

产品包括欧式与美式普通期权、数字期权、亚式期权、单／双障碍期权、触碰期权、雪球、凤凰、累购及区间累计。选择方法前，确认[引擎支持范围](../guide/engines#instrument-coverage)。

`standard_phoenix()` 和 `step_down_phoenix()` 提供标准与降敲凤凰，使用每个合格观察时点支付的 `coupon_per_period`，不按时间年化。`lockout_periods` 禁止前若干期敲出，票息与敲入观察仍然有效，且至少须保留一次可敲出观察。降敲障碍从首次允许敲出的观察开始递减。

`fixed_coupon_note()`（FCN）和 `digital_coupon_note()`（DCN）返回 `PhoenixOption`，使用每期票息 `coupon_per_period`，仅在到期时观察敲入。`early_profit_snowball()` 和 `butterfly_snowball()` 分别提供两段和三段年化票息；阶段截止时刻包含在前一阶段内，敲出票息将所选阶段利率用于整个持有期，到期使用最后阶段利率。

雪球和凤凰的价格为单位原始名义本金下尚未结算现金流的现值，包含条款规定的本金、票息及损失。`principal_redemption_ratio` 是归一化本金偿还比例；持仓名义本金在外部同时缩放完整价格和 Greeks。

`Accumulator` 默认 `option_type="call"` 表示累购，`"put"` 表示累沽。`knock_out_observation_times=None` 表示每个交易日按显式的 `observation_clock_time` 观察敲出，空序列表示不提前敲出；显式时间须严格递增且位于合约期限内。观察时先判定敲出，不再增加数量。

`BinaryBarrierOption` 和 `TouchOption` 通过必填的 `payoff_type="cash"` 或 `"asset"` 选择支付类型；现金支付需要 `payout`，资产支付不接受该金额。`cash_touch_option()`、`asset_touch_option()` 构造单触碰期权，`cash_no_touch_option()`、`asset_no_touch_option()` 构造单不触碰期权；只有单触碰可在触碰时结算。障碍与触碰合约以 `observation_times=None` 选择连续监控，以非空时间序列选择离散监控，`observation_mode` 可查询模式。

`AutocallableObservation.snowball()` 和 `.phoenix()` 构造产品专用的敲出与票息观察记录；`autocallable_observations()` 可从等长数组构建。合约的 `autocall_observations`、`autocall_times` 分别返回记录与时间戳。敲入独立使用 `KnockInObservation.every_trading_day(time(...))` 或 `.at_expiry()`；每日敲入的预设工厂要求显式传入 `knock_in_observation_clock_time`。直接构造自动赎回合约时必须显式提供 `calendar`，预设工厂可以继承日程的日历。

### 历史与替换 {#history-and-replacement}

产品的 `replace()` 返回经过验证的新对象，原对象不变。省略字段或传入 `...`（`Ellipsis`）保留原值；`None` 将可空字段清为未知，必填字段不接受 `None`。条款与历史一起验证，省略的历史字段分别保留；修改条款不会自动重建历史。可替换字段见[金融工具 API](/api/python/kiyosi-instruments)。

历史描述估值时点**严格之前**的事件；恰好在估值时点的观察使用当前现价处理一次。缺失历史表示未知，不能当作零或未触碰。障碍产品使用 `touch_state`，自动赎回使用 `barrier_state`；亚式使用已实现平均价 `realized_average`，区间累计使用 `realized_hit_count`，累购使用 `accumulated_quantity` 与 `knock_out_settled`。`barrier_state="knocked_out"` 和 `knock_out_settled=True` 表示此前已敲出并结算。

调用方负责历史与估值时点、合约条款及结算进度的一致性，并防止使用过期或未来状态。库不会检查历史年龄或重放历史路径，缺少必需历史时抛出 `MissingHistoryError`。数值时间敏感度保持所提供的历史不变。

## `kiyosi.market`

该模块提供市场输入、利率曲线、估值上下文、日历和观察日程。

`BlackScholesMertonParameters` 接收无风险利率、股息率和非负恒定波动率，零波动率使用确定性定价；`LocalVolatilityParameters` 使用局部波动率曲面；`HestonParameters` 描述随机方差过程。三种模型的利率和股息率可以是连续复利标量，也可以是 `RateTermStructure`。`PricingContext` 将模型参数与 `spot_price`、`valuation_time` 组合。

### 利率期限结构 {#rate-curves}

`RateTermStructure` 以参考时点、节点时点和因子构建，因子在对数空间线性插值，时间采用 Actual/365 Fixed。节点曲线的查询必须位于覆盖范围内：

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

`RateTermStructure.flat()` 构造无上界的恒定曲线；需要精确恒定利率及双端覆盖范围时，使用 `RateTermStructure.bounded_flat(rate, reference_time=..., max_time=...)`。恒定性按实际远期利率判断，舍入后的节点因子不保证精确恒定。转交模型利率时使用 `risk_free_curve` 和 `dividend_curve` 保留覆盖范围；`flat_risk_free_rate`、`flat_dividend_yield` 只返回恒定曲线的标量，非恒定曲线会抛出异常。

### 更新市场输入 {#replace-market-inputs}

模型参数和上下文只读。`replace()` 创建经过验证的新对象，省略字段或传入 `...` 保持原值，显式 `None` 会被拒绝。沿用[首次定价](../guide/first-price)的 `context`：

```python
stressed = context.replace(
    spot_price=105.0,
    model_parameters=context.model_parameters.replace(volatility=0.25),
)
```

### 局部波动率 {#local-volatility}

`LocalVolatilitySurface` 保存矩形网格，行对应时间，列对应绝对标的价格。时间与价格节点均至少两个并严格递增，价格和波动率必须为正有限值。波动率按时间和价格双线性插值，价格超出网格时使用端点值，时间不允许外推。改变上下文的现价或估值时点不会移动曲面节点。

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

一维有限差分的所有产品族均支持该模型的价格与固定绝对曲面 delta、gamma；其他 Greeks 返回 `None`，状态为 `unsupported`。到期 Greeks 按支付函数判断，导数无定义或数值模板不可用时也返回 `None`，用 `status()` 区分原因。数字期权有限差分要求利率和股息率为恒定曲线。

自动赎回有限差分支持该模型的隐含票息求解。其他引擎族、`numerical_greeks()` 和隐含波动率求解不接受局部波动率模型。

曲面须覆盖剩余随机演化时段，利率须覆盖所需折现时段。自动空间边界使用该演化时段内插值后的最大局部波动率；仍应检查时间、空间网格和边界的收敛性。

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

Fourier 积分引擎仅支持欧式普通期权；二维有限差分引擎还支持美式普通期权。两者均支持确定性利率曲线、零方差参数及相关系数端点。`price_with_greeks()` 返回价格，请求的 Greeks 标记为 `unsupported`；扰动控制会验证但不参与计算。`numerical_greeks()` 和隐含参数求解不接受 Heston 模型；其他引擎也不接受该模型。积分容差、评估预算、网格与边界设置见 [Heston 定价](../guide/engines#heston-pricing)。

### 日历与观察日程 {#calendars-and-schedules}

`weekdays_calendar()`、`all_days_calendar()` 和 `sse_calendar()` 提供内置日历。`custom_calendar()` 可在基础日历上覆盖开市日和休市日，同一天不能同时出现在两组中。交易年分母来自日历，与利率曲线的 Actual/365 Fixed 时间不同。

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

`ObservationSchedule` 支持迭代、`reversed()`、长度、整数索引（含负数）和切片。切片返回保留原日历的独立日程，不接受递减选择；布尔索引抛出 `TypeError`，越界索引抛出 `IndexError`。接收日程的合约会继承其日历，显式 `calendar` 可覆盖；普通列表与元组不携带日历。日程边界和日历约定见[市场 API](/api/python/kiyosi-market)。

## `kiyosi.pricing`

该模块提供解析与数值引擎、Greeks、隐含波动率和隐含票息求解器。

欧式解析定价使用 `AnalyticEuropeanEngine`；CPU 蒙特卡洛定价可用 `MonteCarloVanillaEngine`。`price(option, context)` 直接返回 `float`。引擎只读，`engine.replace(...)` 创建经过构造验证的新引擎；省略配置或传入 `...` 保留原值，`None` 只用于可空配置。

`price_with_greeks()` 必须传入 `greeks`：可用单个名称、名称序列或 `"all"`，空序列仅请求价格，返回只读的 `PricingResult`。共有十二项指标：delta、gamma、speed、theta、charm、color、vega、volga、vanna、zomma、rho、dividend_rho。均为未缩放偏导，波动率与利率使用小数单位，估值时间使用年（Actual/365 Fixed），其余输入保持不变。Rho 与 dividend_rho 分别对应无风险利率曲线和股息率曲线的平行移动。

不可用指标为 `None`，用 `result.status(name)` 查询原因：

| 状态 | 含义 |
| --- | --- |
| `available` | 有可用数值 |
| `not_requested` | 未请求该指标 |
| `unsupported` | 引擎或模型不支持 |
| `undefined` | 当前估值下导数无定义 |
| `stencil_unavailable` | 数值差分模板不可用，可尝试调整扰动 |

即使请求中没有受支持的指标，仍返回价格与状态。`requested` 和 `supported` 分别给出所请求及引擎／模型支持的名称；`result.require(name)` 在无数值时抛出带 `greek` 和 `status` 属性的 `GreekUnavailableError`。

`engine.greek_method(instrument, context)` 查询估计方法，`active_greek_controls()` 查询可能使用的扰动控制。`price_with_greeks()` 统一接受 `spot_shift`、`volatility_shift`、`rate_shift`、`time_shift`，只调节数值回退及可用性检查，保留原生估计方法；`numerical_greeks()` 显式选择 BSM 标量数值差分。省略控制或传入 `...` 继承引擎设置；现价、波动率和时间扰动的 `None` 表示自动选择。`time_shift` 使用正的 `datetime.timedelta`；自动时间步至多一天，并缩短以避开观察事件。自动波动率步长为 `min(0.0001, volatility / 2)`，`rate_shift` 的共享默认值为 `0.0001`。所有显式控制都会验证。

`QuadratureVanillaEngine` 和 `QuadratureDigitalEngine` 使用恒定利率 BSM，提供价格与数值 Greeks；单／双障碍蒙特卡洛的原生 Greeks 仅支持 delta、gamma。配置与收敛检查见[定价引擎](../guide/engines)。

### 隐含参数 {#implied-parameters}

`implied_volatility()` 必须显式提供 `lower_bound` 和 `upper_bound`，以选择波动率根的搜索区间。数字与障碍产品可能有多个根；数值容差只约束所选引擎的价格曲线。沿用[首次定价](../guide/first-price)中的对象：

```python
from kiyosi.pricing import implied_volatility

sigma = implied_volatility(
    engine, option, context, observed_price=engine.price(option, context),
    lower_bound=0.1, upper_bound=0.3,
)
print(sigma)
```

`implied_snowball_coupon()` 返回包含年化 `first_observation_coupon` 和 `quote_convention` 的字典。必填的 `quote_convention` 可为 `"shift_maturity_coupon"`（同步平移到期票息）或 `"preserve_maturity_coupon"`（固定到期票息）；用 `note.with_coupon(**quote)` 应用报价，保留各观察票息的利差。

`implied_phoenix_coupon()` 返回包含 `coupon_per_period` 的字典，同样可用 `note.with_coupon(**quote)` 应用。凤凰、FCN／DCN 的求解边界、容差和返回值使用每期绝对票息率。蒙特卡洛求解须使用显式种子；可先保留 `engine.with_resolved_seed()` 返回的引擎，供求解与回代使用。签名、单位和限制见[定价 API](/api/python/kiyosi-pricing)。

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

`InvalidInputError` 同时继承 `ValueError`。表示和调用签名错误使用 Python 原生异常，已报告的运行环境错误使用 `OSError`。不要解析错误文本判断类别。Rust 内部 panic 与领域异常不同；内存耗尽可能终止进程。

合约、估值、曲线和观察时间使用无时区的 `datetime.datetime`，精度为微秒，所有输入须采用调用方选定的同一时间基准；不接受纯 `date` 或带时区的 `datetime`。日历日期使用 `datetime.date`（不含 `datetime`），观察时钟使用无时区的 `datetime.time`。超出 Python 年份 1–9999 的结果抛出 `ValueError`。

数值输入拒绝布尔值和隐式舍入；精确实数必须可无损表示为浮点数，显式 `float(value)` 表示接受舍入。整数输入要求 `__index__`，小数抛出 `TypeError`，超范围抛出 `OverflowError`。集合属性返回自有元组，曲面使用嵌套元组；对象只读、支持复制与 pickle，跨进程须使用同一 kiyosi 版本。

共享或独立实例均支持并发读取和定价。长计算会释放 GIL，较短的解析调用可能保留 GIL。调用同步完成，长请求中调用线程会轮询信号；`KeyboardInterrupt` 等信号处理异常将协作取消计算，等待工作停止后传播，不返回部分结果。内存分配或单个工作单元可能延迟取消。完整约定见[包级参考](/api/python/kiyosi)。

## 实用示例 {#working-examples}

- [首次定价](../guide/first-price)：完整 Python 脚本与 Greeks。
- [采样与误差估计](../guide/engines#sampling-and-error)：蒙特卡洛统计接口。
- [上游 Python 示例](https://github.com/lilkui/kiyosi/tree/a125eb5b6512606881d3e809ae861bac96f90880/examples/python)：产品定价、历史输入、日历和票息求解。
- [上游 Python 测试](https://github.com/lilkui/kiyosi/tree/a125eb5b6512606881d3e809ae861bac96f90880/python/tests)：更多产品用法。
