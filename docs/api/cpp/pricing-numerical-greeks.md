---
description: C++ API declarations from kiyosi/pricing/numerical_greeks.hpp.
outline: [2, 4]
---

# `<kiyosi/pricing/numerical_greeks.hpp>`

```cpp
#include <kiyosi/pricing/numerical_greeks.hpp>
```

## `calculate_numerical_risk_measures`

```cpp
template <typename Engine, typename Option>
Result< PricingResult > kiyosi::calculate_numerical_risk_measures(const Engine &engine, const Option &option, const PricingContext &context, NumericalShiftSettings settings={})
```

Derives risk measures for any engine by revaluing it on bumped market states. Spot, volatility, and rate shifts are absolute; time shifts are calendar days. Central stencils are used except where time is clamped to the instrument life. Measures with no supported stencil inside a model boundary are unavailable, while the valid base price and independent measures are retained. A failure while pricing any feasible bumped state fails the whole operation. 
**Template parameters**

- `` — Pricing engine providing `price(option, context)`.
- `` — Instrument accepted by the engine.

**Returns:** Pricing and risk measures, or a settings, pricing, or result error.
