---
description: 使用 kiyosi 的 Python 接口和 Black-Scholes 解析引擎为欧式看涨期权定价。
---

# 首次定价

本示例对一份行权价 100、期限一年的欧式看涨期权定价。请先[安装 kiyosi](./installation)，再将以下代码保存为 `first_price.py`。

## 完整示例 {#a-complete-example}

```python
from datetime import datetime

from kiyosi.instruments import EuropeanOption
from kiyosi.market import BlackScholesMertonParameters, PricingContext
from kiyosi.pricing import AnalyticEuropeanEngine

valuation = datetime(2025, 1, 1)
option = EuropeanOption(
    option_type="call",
    strike=100.0,
    effective_time=valuation,
    expiry_time=datetime(2026, 1, 1),
)
context = PricingContext(
    model_parameters=BlackScholesMertonParameters(
        risk_free_rate=0.05,
        dividend_yield=0.02,
        volatility=0.20,
    ),
    spot_price=100.0,
    valuation_time=valuation,
)

price = AnalyticEuropeanEngine().price(option, context)
print(f"Price: {price:.6f}")  # 9.227006
```

运行脚本：

```sh
python first_price.py
```

输出为 `Price: 9.227006`。示例通过固定的 `valuation_time` 指定估值时点。时间参数使用无时区的 `datetime`，所有输入采用同一时间基准。

## 理解输入参数 {#understand-the-inputs}

| 参数 | 取值 | 含义 |
| --- | --- | --- |
| `option_type` | `"call"` | 看涨期权；看跌期权使用 `"put"` |
| `strike` | `100.0` | 合约行权价 |
| `spot_price` | `100.0` | 估值时点的标的现价 |
| `risk_free_rate` | `0.05` | 恒定的年化无风险利率，以小数表示 |
| `dividend_yield` | `0.02` | 恒定的年化股息率，以小数表示 |
| `volatility` | `0.20` | 年化波动率，以小数表示 |

`effective_time` 和 `expiry_time` 分别是合约的生效时刻和到期时刻；`valuation_time` 是估值时点，属于市场上下文。利率和股息率采用连续复利。`price()` 只计算价格，直接返回 `float`。

## 计算 Greeks {#calculate-greeks}

需要计算敏感度时，调用 `price_with_greeks()`，显式指定所需指标：

```python
engine = AnalyticEuropeanEngine()
result = engine.price_with_greeks(option, context, greeks=["delta", "gamma", "vega"])
print(result.price, result.delta, result.gamma, result.vega)
```

该方法返回只读的 `PricingResult`。`greeks` 是必填参数，可传入单个名称（如 `"delta"`）或名称序列，也可用 `"all"` 请求全部十二项指标；空序列仅请求价格。

指标为 `None` 时，可用 `result.status("delta")` 查询原因。`result.require("delta")` 在指标可用时返回数值，否则抛出 `GreekUnavailableError`。`None` 表示缺少可用数值，零表示该偏导的计算值为零。

`price_with_greeks()` 使用引擎自身的估计方法。数值差分与扰动设置见 [Greeks 扰动控制](../reference/python#greek-controls)。

所有 Greeks 均为未缩放偏导：波动率和利率以小数为单位，时间以年（Actual/365 Fixed）为单位。例如，波动率上升 1 个百分点的近似价格变化为 `result.vega * 0.01`；估值时点前进一天的近似价格变化为 `result.theta / 365`。完整定义见 [`PricingResult`](/api/python/kiyosi#pricingresult)。

## 更换定价引擎 {#change-the-engine}

沿用上面的 `option` 和 `context`，可以改用 CPU 蒙特卡洛引擎为同一合约定价：

```python
from kiyosi.pricing import MonteCarloVanillaEngine

estimate = MonteCarloVanillaEngine(seed=42, max_active_workers=4).price(option, context)
print(estimate)
```

蒙特卡洛方法通过随机抽样估算价格，可用统计接口查看采样误差。`seed` 固定随机种子，`max_active_workers` 限制单次 CPU 调用的活跃工作线程数。

产品与引擎的对应关系见[定价引擎](./engines)，统计接口见[采样与误差估计](./engines#sampling-and-error)。

本示例改编自 [kiyosi Python 定价模块示例](https://github.com/lilkui/kiyosi/blob/95dc91155223b9095d06cbbf7ba4bda5bc72b7c1/python/src/kiyosi/pricing.py)。
