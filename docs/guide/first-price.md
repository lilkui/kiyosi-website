---
description: 使用 kiyosi 的 Python 接口和 Black-Scholes 解析引擎为欧式看涨期权定价。
---

# 首次定价

本示例计算一份欧式看涨期权的价格，行权价为 100，期限为一年。请先[安装 kiyosi](./installation)，再将以下代码保存为 `first_price.py`。

## 完整示例 {#a-complete-example}

```python
from datetime import date

from kiyosi.instruments import EuropeanOption
from kiyosi.market import BlackScholesMertonParameters, PricingContext
from kiyosi.pricing import AnalyticVanillaEngine

valuation = date(2025, 1, 1)
option = EuropeanOption(
    option_type="call",
    strike=100.0,
    effective_date=valuation,
    expiry_date=date(2026, 1, 1),
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

price = AnalyticVanillaEngine().price(option, context)
print(f"Price: {price:.6f}")  # 9.227006
```

运行脚本：

```sh
python first_price.py
```

脚本会输出期权价格。示例中的历史日期是固定的，计算以 `valuation_time` 为估值时点，与脚本运行当天的日期无关。

## 理解输入参数 {#understand-the-inputs}

| 参数 | 取值 | 含义 |
| --- | --- | --- |
| `option_type` | `"call"` | 看涨期权；看跌期权使用 `"put"` |
| `strike` | `100.0` | 合约行权价 |
| `spot_price` | `100.0` | 估值时点的标的现价 |
| `risk_free_rate` | `0.05` | 恒定的年化无风险利率，以小数表示 |
| `dividend_yield` | `0.02` | 恒定的年化股息率，以小数表示 |
| `volatility` | `0.20` | 年化波动率，以小数表示 |

`effective_date` 和 `expiry_date` 分别是合约的生效日和到期日；`valuation_time` 是估值时点，属于市场上下文。利率和股息率采用连续复利。`price()` 只计算价格，直接返回 `float`。

## 计算 Greeks {#calculate-greeks}

需要计算敏感度时，调用 `price_with_greeks()`，显式指定所需指标：

```python
engine = AnalyticVanillaEngine()
result = engine.price_with_greeks(option, context, greeks=["delta", "gamma", "vega"])
print(result.price, result.delta, result.gamma, result.vega)
```

该方法返回只读的 `PricingResult`。也可用 `all_greeks=True` 请求全部十项指标，此时不要同时传入 `greeks`。未请求、无定义或不支持的指标为 `None`，不能当作零处理。

Vega 按波动率变动 1 个百分点计量，theta 按估值时点向前移动 1 个自然日计量。完整的单位说明见 [`PricingResult`](/api/python/kiyosi#pricingresult)。

## 更换定价引擎 {#change-the-engine}

沿用上面的 `option` 和 `context`，可以改用 CPU 蒙特卡洛引擎为同一合约定价：

```python
from kiyosi.pricing import MonteCarloVanillaEngine

estimate = MonteCarloVanillaEngine().price(option, context)
print(estimate)
```

蒙特卡洛方法通过数值模拟估算价格，结果可能与解析解不同。各类产品支持哪些引擎，以及如何配置 CUDA，见[定价引擎](./engines)。

本示例改编自 [kiyosi Python 快速入门](https://github.com/lilkui/kiyosi/blob/main/README.md#python-快速上手)。
