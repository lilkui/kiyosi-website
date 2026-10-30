---
description: 了解 kiyosi 的 instruments、market 和 pricing 模块，以及错误、日期和并发约定。
---

# Python API 概览

本页对应 **kiyosi 0.14.0**。所有公开导出对象、运行时签名、属性和文档字符串均可在[完整 Python API 参考](/api/python/)中查阅。参考文档保留英文，与源码注释一致。

## `kiyosi.instruments`

该模块定义金融工具、结构化产品预设与观察记录。`OptionType` 等选择类型为 `typing.Literal` 类型别名，调用时直接传入小写字符串。

产品包括欧式与美式普通期权、数字期权、亚式期权、单／双障碍期权、触碰期权、雪球、凤凰、累购及区间累计。选择方法前，确认[引擎支持范围](../guide/engines#instrument-coverage)。

`AutocallableObservation` 保存观察日、敲出水平、票息和票息障碍。已有平行数组时，可用 `autocallable_observations()` 转换；序列须等长，构造合约时验证日期与条款。

产品的 `replace()` 返回经过验证的新对象，原对象不变。可替换的字段取决于产品，详见[金融工具 API](/api/python/kiyosi-instruments)。调用方须提供真实历史；库不会仅根据当前现价推断过去是否触碰障碍。

## `kiyosi.market`

该模块提供市场输入、利率曲线、估值上下文、日历和观察日程。

`BlackScholesMertonParameters` 接收无风险利率、股息率和恒定波动率。利率和股息率可以是连续复利标量，也可以是 `RateTermStructure`。`PricingContext` 将模型参数与 `spot_price`、`valuation_time` 组合。

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

模型参数和上下文只读。`replace()` 创建经过验证的新对象，省略字段保持原值。沿用[首次定价](../guide/first-price)的 `context`：

```python
stressed = context.replace(
    spot_price=105.0,
    model_parameters=context.model_parameters.replace(volatility=0.25),
)
```

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

欧式解析定价使用 `AnalyticEuropeanEngine`；CPU 蒙特卡洛定价可用 `MonteCarloVanillaEngine`。`price(option, context)` 直接返回 `float`。`price_with_greeks()` 用 `greeks` 或 `all_greeks=True` 选择指标，返回只读的 `PricingResult`。

未请求、无定义或不受支持的 Greeks 为 `None`；`result.require("delta")` 在指标不可用时抛出 `UnsupportedOperationError`。Vega、vanna、zomma 按波动率变动一个百分点计量，rho 按利率变动一个百分点计量，theta、charm、color 按估值时点向前移动一个自然日计量。

数值差分可通过 `spot_shift`、`volatility_shift`、`rate_shift` 和 `time_shift_days` 调整。`implied_volatility()`、`implied_coupon()` 分别求解隐含波动率和票息。签名、单位和限制见[定价 API](/api/python/kiyosi-pricing)。

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
- [上游 Python 测试](https://github.com/lilkui/kiyosi/tree/748942203c99ffb5f011dbdcd06312d6b5f4a06c/tests/python)：更多产品用法。
