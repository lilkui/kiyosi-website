---
description: 了解 kiyosi 的 instruments、market 和 pricing 模块，以及错误、日期和并发约定。
---

# Python API 概览

本页对应 **kiyosi 0.16.0**。所有公开导出对象、运行时签名、属性和文档字符串均可在[完整 Python API 参考](/api/python/)中查阅。参考文档保留英文，与源码注释一致。

## `kiyosi.instruments`

该模块定义金融工具、结构化产品预设与观察记录。`OptionType` 等选择类型为 `typing.Literal` 类型别名，调用时直接传入小写字符串。

产品包括欧式与美式普通期权、数字期权、亚式期权、单／双障碍期权、触碰期权、雪球、凤凰、累购及区间累计。选择方法前，确认[引擎支持范围](../guide/engines#instrument-coverage)。

`fixed_coupon_note()`（FCN）和 `digital_coupon_note()`（DCN）返回 `PhoenixOption`，使用固定的每期票息 `coupon_per_period`，仅在到期时观察敲入。直接构造凤凰时，年化 `coupon_rate` 与每期 `coupon_per_period` 必须恰好提供一个。`early_profit_snowball()` 和 `butterfly_snowball()` 分别提供两段和三段年化票息；阶段截止日包含当天，敲出票息将所选阶段利率用于整个持有期，到期使用最后阶段利率。

`Accumulator` 默认 `option_type="call"` 表示累购，`"put"` 表示累沽。`knock_out_observation_dates=None` 表示每个交易日观察敲出，空序列表示不提前敲出；显式日期须严格递增且位于合约期限内。敲出日先判定敲出，不再增加数量。

`cash_touch_option()` 和 `asset_touch_option()` 分别构造现金和资产结算的单触碰／单不触碰期权，通过 `barrier_type` 选择方向与触碰规则；只有单触碰（`"up_and_in"`、`"down_and_in"`）可在触碰时结算。

`AutocallableObservation` 保存观察日、敲出水平、票息和票息障碍。已有平行数组时，可用 `autocallable_observations()` 转换；序列须等长，构造合约时验证日期与条款。

产品的 `replace()` 返回经过验证的新对象，原对象不变。可替换的字段取决于产品，详见[金融工具 API](/api/python/kiyosi-instruments)。省略字段或传入 `...`（`Ellipsis`）保留原值；可空历史字段的 `None` 表示清除历史，必填字段不接受 `None`。调用方须提供真实历史；库不会仅根据当前现价推断过去是否触碰障碍。

## `kiyosi.market`

该模块提供市场输入、利率曲线、估值上下文、日历和观察日程。

`BlackScholesMertonParameters` 接收无风险利率、股息率和恒定波动率；`LocalVolatilityParameters` 使用局部波动率曲面。两种模型的利率和股息率可以是连续复利标量，也可以是 `RateTermStructure`。`PricingContext` 将模型参数与 `spot_price`、`valuation_time` 组合。

### 利率期限结构 {#rate-curves}

`RateTermStructure` 以参考时点、节点时点和因子构建，因子在对数空间线性插值，时间采用 Actual/365 Fixed。节点曲线的查询必须位于覆盖范围内：

```python
from datetime import date
from kiyosi.market import BlackScholesMertonParameters, RateTermStructure

curve = RateTermStructure(
    reference_time=date(2025, 1, 1),
    times=[date(2026, 1, 1)],
    factors=[0.95],
)
model = BlackScholesMertonParameters(
    risk_free_rate=curve,
    dividend_yield=0.02,
    volatility=0.20,
)
```

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
    times=[option.effective_date, option.expiry_date],
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

所有有限差分产品族均支持该模型的价格与固定曲面 delta、gamma。到期时或差分模板跨越事件、无法计算时，delta／gamma 为 `None`。请求其他 Greeks（包括 `greeks="all"`）、使用非有限差分引擎或进行隐含参数求解，会抛出 `UnsupportedOperationError`；数字期权有限差分还要求利率和股息率显式为平坦曲线。

曲面须覆盖剩余随机演化时段，利率须覆盖所需折现时段。自动空间边界使用该演化时段内插值后的最大局部波动率；仍应检查时间、空间网格和边界的收敛性。

### 日历与观察日程 {#calendars-and-schedules}

`weekdays_calendar()`、`all_days_calendar()` 和 `sse_calendar()` 提供内置日历。`custom_calendar()` 可在基础日历上覆盖开市日和休市日，同一天不能同时出现在两组中。交易年分母来自日历，与利率曲线的 Actual/365 Fixed 时间不同。

```python
from datetime import date
from kiyosi.market import custom_calendar, monthly_schedule, weekdays_calendar

calendar = custom_calendar(
    base=weekdays_calendar(),
    closed_dates=[date(2025, 2, 3)],
    open_dates=[date(2025, 2, 8)],
)
schedule = monthly_schedule(
    start=date(2025, 1, 1),
    end=date(2025, 4, 1),
    first_observation_month=1,
    calendar=calendar,
)
```

`first_observation_month=1` 表示从起始日后一个月开始观察。月末会按原始锚点处理，并按日历调整。日程边界和日历的详细约定见[市场 API](/api/python/kiyosi-market)。

## `kiyosi.pricing`

该模块提供解析与数值引擎、Greeks、隐含波动率和隐含票息求解器。

欧式解析定价使用 `AnalyticEuropeanEngine`；CPU 蒙特卡洛定价可用 `MonteCarloVanillaEngine`。`price(option, context)` 直接返回 `float`。`price_with_greeks()` 必须传入 `greeks`：可用单个名称、名称序列或 `"all"`，返回只读的 `PricingResult`。

共有十二项 Greeks：delta、gamma、speed、theta、charm、color、vega、volga、vanna、zomma、rho、dividend_rho。未请求、无定义或不受支持的指标为 `None`；`result.require("delta")` 在指标不可用时抛出 `UnsupportedOperationError`。Vega、vanna、zomma 按波动率变动一个百分点计量，volga 为波动率二阶导数除以 10000；rho 和 dividend_rho 分别按无风险利率、股息率曲线平行移动一个百分点计量。Theta、charm、color 按估值时点向前移动一个自然日计量。

数值差分引擎按各自签名提供 `spot_shift`、`volatility_shift`、`rate_shift` 和 `time_shift_days`。`volatility_shift` 用于 vega 与 volga，数值 volga 的较低波动率扰动值必须严格为正；`rate_shift` 用于 rho 与 dividend_rho。仅使用原生 Greeks 的引擎不接受这些扰动参数；`MonteCarloBarrierEngine` 和 `MonteCarloDoubleBarrierEngine` 仅支持 delta、gamma，扰动参数只有 `spot_shift`。

`implied_volatility()`、`implied_coupon()` 分别求解隐含波动率和票息。雪球票息求解须指定 `quote_convention`，控制是否同步平移到期票息；凤凰省略该参数。FCN／DCN 的求解边界、容差和返回值沿用合约的每期票息单位。签名、单位和限制见[定价 API](/api/python/kiyosi-pricing)。

## 错误处理与并发 {#errors-and-concurrency}

领域错误均继承 `KiyosiError`，可以按异常类型处理：

| 异常 | 含义 |
| --- | --- |
| `InvalidInputError` | 参数、日期、日程或历史不合法 |
| `UnsupportedOperationError` | 不支持的定价组合或不可用的结果指标 |
| `ComputationFailureError` | 数值结果非有限或计算状态不可用 |
| `RootNotBracketedError` | 给定区间没有包围根 |
| `NonConvergenceError` | 迭代或积分未收敛 |

表示和调用签名错误使用 Python 原生异常，已报告的运行环境错误使用 `OSError`。不要解析错误文本判断类别。Rust 内部 panic 与领域异常不同；内存耗尽可能终止进程。

合约日期使用 `datetime.date`，不接受 `datetime`；估值时点可使用日期（UTC 零点）或带时区的 `datetime`，不接受无时区的 `datetime`。数值输入会拒绝布尔值和意外的有损转换。

共享或独立实例均支持并发读取和定价。长计算会释放 GIL，较短的解析调用可能保留 GIL。调用是同步的，核心没有取消或信号轮询接口，Python 在计算返回后恢复信号处理。完整约定见[包级参考](/api/python/kiyosi)。

## 实用示例 {#working-examples}

- [首次定价](../guide/first-price)：完整 Python 脚本与 Greeks。
- [采样与误差估计](../guide/engines#sampling-and-error)：蒙特卡洛统计接口。
- [上游 Python 测试](https://github.com/lilkui/kiyosi/tree/2ec75ab8462bcef8f32bd32aba4468f78e7ee6a9/python/tests)：更多产品用法。
