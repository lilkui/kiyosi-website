---
description: Price a European call using kiyosi's analytic Black-Scholes engine in Python.
---

# Your first price

This example prices a European call with a strike of 100 and a one-year term. [Install kiyosi](./installation) first, then save the following code as `first_price.py`.

## A complete example

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

Run the script:

```sh
python first_price.py
```

The script prints the option price. Dates are fixed historical example inputs; the calculation uses `valuation_time`, not today's date.

## Understand the inputs

| Input | Value | Meaning |
| --- | --- | --- |
| `option_type` | `OptionType.CALL` | A call option |
| `strike` | `100.0` | The contract's strike price |
| `spot_price` | `100.0` | The underlying spot price at valuation |
| `risk_free_rate` | `0.05` | Flat annual rate, expressed as a decimal |
| `dividend_yield` | `0.02` | Flat annual dividend yield, expressed as a decimal |
| `volatility` | `0.20` | Annual volatility, expressed as a decimal |

`effective_date` and `expiry_date` define the contract dates. `valuation_time` belongs to the market context. The analytic engine combines those inputs and exposes the result through `result.price`.

## Change the engine

After defining `option` and `context` above, you can price the same instrument with a CPU Monte Carlo engine:

```python
from kiyosi.pricing import MonteCarloVanillaEngine

estimate = MonteCarloVanillaEngine().price(option, context)
print(estimate.price)
```

A Monte Carlo estimate can differ from an analytic result because it uses numerical simulation. See [Pricing engines](./engines) for instrument coverage and CUDA selection.

Example adapted from the [kiyosi Python quick start](https://github.com/lilkui/kiyosi#quick-start-with-python).
