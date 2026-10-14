---
description: 了解 kiyosi 的 instruments、market 和 pricing 三个 Python 模块。
---

# Python API 概览

所有公开导出对象的签名、成员、异常和文档字符串，均可在[完整 Python API 参考（英文）](/api/python/)中查阅。这部分参考文档由工具自动生成，保留英文以与源码文档保持一致。

本页对应 **kiyosi 0.10.0**。公开 Python API 主要分布在三个模块中；包根目录还提供 `Greek`、`PricingResult`、`KiyosiError`、`ErrorCategory` 和 `__version__`。

## `kiyosi.instruments`

该模块提供合约定义和结构化产品预设。[首次定价示例](../guide/first-price)用 `EuropeanOption(option_type="call", ...)` 定义看涨期权。`OptionType` 等用于选择参数取值的类型是 `typing.Literal` 类型别名，调用时直接传入小写字符串。

支持的产品包括普通期权、数字期权、亚式期权、障碍期权、累购产品、凤凰产品和雪球产品。选择定价方法前，请先确认[引擎支持范围](../guide/engines#instrument-coverage)。

雪球和凤凰产品使用 `AutocallableObservation` 记录每个观察日及对应的敲出水平、票息和票息障碍。如果已有平行数组，可用 `autocallable_observations()` 将其转换为记录，输入序列须等长。用这些记录构建合约时，核心会验证日期顺序和条款。完整参数见[金融工具 API](/api/python/kiyosi-instruments)。

[查看 instruments 模块源码 →](https://github.com/lilkui/kiyosi/blob/main/python/kiyosi/instruments.py)

## `kiyosi.market`

该模块提供市场输入、估值上下文、日历和观察日程。

`BlackScholesMertonParameters` 保存恒定的无风险利率、股息率和波动率。`PricingContext` 将这些参数与 `spot_price`、`valuation_time` 组合成定价所需的市场上下文。

`PricingContext` 默认使用不含节假日的工作日日历，交易年分母为 252。处理上交所业务时，可显式传入 `calendar=sse_calendar()`，该日历的交易年分母为 **243**。节假日表覆盖 1991–2099；超出已公布安排的未来日期包含预测值，不能视为交易所公告。详见[市场 API](/api/python/kiyosi-market#sse-calendar)。

[查看 market 模块源码 →](https://github.com/lilkui/kiyosi/blob/main/python/kiyosi/market.py)

## `kiyosi.pricing`

该模块提供定价引擎、数值 Greeks、隐含波动率和隐含票息求解器。

欧式看涨期权示例使用 `AnalyticVanillaEngine`。也可使用基于模拟的 `MonteCarloVanillaEngine(backend="cpu")`，或选择 CUDA 后端。这两个引擎的 `price(option, context)` 都直接返回 `float`。调用 `price_with_greeks()` 时，须用 `greeks` 或 `all_greeks=True` 选择指标，返回结果为 `PricingResult`。

Greeks 的缺失值为 `None`。Vega、vanna、zomma 按波动率变动 1 个百分点计量，rho 按利率变动 1 个百分点计量，theta、charm、color 按估值时点向前移动 1 个自然日计量。

`calculate_numerical_greeks()` 使用价格差分计算指定指标；`implied_volatility()` 和 `implied_coupon()` 分别求解隐含波动率和票息。详见[定价 API](/api/python/kiyosi-pricing)。

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
