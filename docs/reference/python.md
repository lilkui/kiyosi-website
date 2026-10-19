---
description: 了解 kiyosi 的 instruments、market 和 pricing 三个 Python 模块。
---

# Python API 概览

所有公开导出对象的签名、成员、异常和文档字符串，均可在[完整 Python API 参考](/api/python/)中查阅。这部分参考文档由工具自动生成，保留英文以与源码文档保持一致。

本页对应 **kiyosi 0.11.0**。公开 Python API 主要分布在三个模块中；包根目录还提供 `Greek`、`PricingResult`、`KiyosiError`、`ErrorCategory` 和 `__version__`。

## `kiyosi.instruments`

该模块提供合约定义和结构化产品预设。[首次定价示例](../guide/first-price)用 `EuropeanOption(option_type="call", ...)` 定义看涨期权。`OptionType` 等用于选择参数取值的类型是 `typing.Literal` 类型别名，调用时直接传入小写字符串。

支持的产品包括普通期权、数字期权、亚式期权、障碍期权、累购产品、凤凰产品和雪球产品。选择定价方法前，请先确认[引擎支持范围](../guide/engines#instrument-coverage)。

雪球和凤凰产品使用 `AutocallableObservation` 记录每个观察日及对应的敲出水平、票息和票息障碍。如果已有平行数组，可用 `autocallable_observations()` 将其转换为记录，输入序列须等长。用这些记录构建合约时，核心会验证日期顺序和条款。完整参数见[金融工具 API](/api/python/kiyosi-instruments)。

带历史状态的产品提供 `replace()`，返回保留合约条款的已验证副本：障碍和触碰产品可替换 `touch_state`，雪球和凤凰可替换 `barrier_state`，亚式期权可替换 `realized_average`，累购可替换 `accumulated_quantity`。历史由调用者提供，不会根据现价推断；时间一致性在定价时检查。`None` 表示未知障碍历史，`"untouched"` 或 `"none"` 则表示已知没有历史触碰或障碍事件。替换成功或失败均不改变原对象。

[查看 instruments 模块源码 →](https://github.com/lilkui/kiyosi/blob/main/python/kiyosi/instruments.py)

## `kiyosi.market`

该模块提供市场输入、估值上下文、日历和观察日程。

`BlackScholesMertonParameters` 保存恒定的无风险利率、股息率和波动率。`PricingContext` 将这些参数与 `spot_price`、`valuation_time` 组合成定价所需的市场上下文。

`PricingContext` 默认使用不含节假日的工作日日历，交易年分母为 252。处理上交所业务时，可显式传入 `calendar=sse_calendar()`，该日历的交易年分母为 **243**。节假日表覆盖 1991–2099；超出已公布安排的未来日期包含预测值，不能视为交易所公告。详见[市场 API](/api/python/kiyosi-market#sse-calendar)。

### 更新市场输入 {#replace-market-inputs}

模型参数和上下文均不可变。使用 `replace()` 创建修改后的副本，省略的字段保持原值。沿用[首次定价](../guide/first-price)的 `context`：

```python
stressed = context.replace(
    spot_price=105.0,
    model_parameters=context.model_parameters.replace(volatility=0.25),
)
```

这些参数采用构造函数的单位和验证规则，显式传入 `None` 或未知字段会抛出 `TypeError`。

### 自定义日历与观察日程 {#calendars-and-schedules}

`custom_calendar()` 可在基础日历上覆盖休市日和开市日，无需 Python 回调。日期可乱序或重复，但同一天不能同时列为休市和开市。默认继承基础日历的交易年分母；增减交易日不会自动重算该值。

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

`first_observation_month` 是首个观察候选日相对起始日的正整数月偏移：`1` 表示下个月开始，此后每月观察。候选日向后调整到交易日，并去重；起始日不计入结果，到期边界也不保证成为观察日。合约要求特定末次观察日时，应显式提供观察日期。

[查看 market 模块源码 →](https://github.com/lilkui/kiyosi/blob/main/python/kiyosi/market.py)

## `kiyosi.pricing`

该模块提供定价引擎、数值 Greeks、隐含波动率和隐含票息求解器。

欧式看涨期权示例使用 `AnalyticVanillaEngine`。也可使用基于模拟的 `MonteCarloVanillaEngine(backend="cpu")`，或选择 CUDA 后端。这两个引擎的 `price(option, context)` 都直接返回 `float`。调用 `price_with_greeks()` 时，须用 `greeks` 或 `all_greeks=True` 选择指标，返回结果为 `PricingResult`。

Greeks 的缺失值为 `None`。Vega、vanna、zomma 按波动率变动 1 个百分点计量，rho 按利率变动 1 个百分点计量，theta、charm、color 按估值时点向前移动 1 个自然日计量。

`price_with_greeks()` 优先复用引擎原生指标，其余可计算指标使用价格差分。可用 `spot_shift`、`volatility_shift`、`rate_shift` 和 `time_shift_days` 设置绝对扰动量，分别使用标的价格、小数波动率、小数利率和自然日单位。美式蒙特卡洛的默认现价扰动为现价的 8%，仍需检查采样误差和扰动大小带来的偏差。

`implied_volatility()` 和 `implied_coupon()` 分别求解隐含波动率和票息。引擎在构造时验证数值配置，蒙特卡洛支持单次 CPU 调用的 `thread_count` 并发上限，详见[定价引擎](../guide/engines)和[定价 API](/api/python/kiyosi-pricing)。

[查看 pricing 模块源码 →](https://github.com/lilkui/kiyosi/blob/main/python/kiyosi/pricing.py)

## 错误处理与并发 {#errors-and-concurrency}

Python 表示或调用签名有误时，会抛出 `TypeError`、`OverflowError` 等内置异常。核心领域错误会抛出 `KiyosiError`；处理时请检查其 `category`，不要解析错误文本。资源分配失败会抛出 `MemoryError`。

定价调用是同步的。核心计算期间没有取消接口，也不轮询信号，主线程会等到计算返回后才处理 Ctrl-C。较长的计算会释放 GIL，部分较短的解析计算会保留 GIL。详细约定见[包级文档](/api/python/kiyosi)。

## 实用示例 {#working-examples}

- [首次定价](../guide/first-price)：完整的 Python 脚本。
- [选择计算后端](../guide/engines#select-a-backend)：CUDA 配置示例。
- [Python 测试](https://github.com/lilkui/kiyosi/tree/main/tests/python)：更多产品和引擎的用法。

::: info API 稳定性
API 仍处于早期开发阶段。更新 kiyosi 包后，应重新生成完整 API 参考。
:::
