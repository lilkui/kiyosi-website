---
description: 使用 kiyosi 的 Python 接口和 Black-Scholes 解析引擎为欧式看涨期权定价。
---

# 首次定价

本示例为行权价为 100、期限为一年的欧式看涨期权定价。请先[安装 kiyosi](./installation)，再将以下代码保存为 `first_price.py`。

## 完整示例 {#a-complete-example}

```python
from datetime import date

from kiyosi.instruments import EuropeanOption, OptionType
from kiyosi.market import BlackScholesMertonParameters, PricingContext
from kiyosi.pricing import AnalyticVanillaEngine

valuation = date(2025, 1, 1)
option = EuropeanOption(
    option_type=OptionType.CALL,
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

result = AnalyticVanillaEngine().price(option, context)
print(result.price)
```

运行脚本：

```sh
python first_price.py
```

脚本会输出期权价格。示例使用固定的历史日期，计算以 `valuation_time` 为估值时点，与运行脚本当天的日期无关。

## 理解输入参数 {#understand-the-inputs}

| 参数 | 取值 | 含义 |
| --- | --- | --- |
| `option_type` | `OptionType.CALL` | 看涨期权 |
| `strike` | `100.0` | 合约行权价 |
| `spot_price` | `100.0` | 估值时点的标的现价 |
| `risk_free_rate` | `0.05` | 恒定的年化无风险利率，以小数表示 |
| `dividend_yield` | `0.02` | 恒定的年化股息率，以小数表示 |
| `volatility` | `0.20` | 年化波动率，以小数表示 |

`effective_date` 和 `expiry_date` 分别定义合约的生效日和到期日，`valuation_time` 则属于市场上下文。解析引擎根据这些输入完成计算，价格可通过 `result.price` 获取。

## 更换定价引擎 {#change-the-engine}

定义好上面的 `option` 和 `context` 后，可以改用 CPU 蒙特卡洛引擎为同一合约定价：

```python
from kiyosi.pricing import MonteCarloVanillaEngine

estimate = MonteCarloVanillaEngine().price(option, context)
print(estimate.price)
```

蒙特卡洛方法通过数值模拟估算价格，因此结果可能与解析解有所不同。各类产品支持的引擎及 CUDA 配置方法见[定价引擎](./engines)。

本示例改编自 [kiyosi Python 快速入门](https://github.com/lilkui/kiyosi#quick-start-with-python)。
