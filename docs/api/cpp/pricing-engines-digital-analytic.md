---
description: C++ API declarations from kiyosi/pricing/engines/digital/analytic.hpp.
outline: [2, 4]
---

# `<kiyosi/pricing/engines/digital/analytic.hpp>`

```cpp
#include <kiyosi/pricing/engines/digital/analytic.hpp>
```

## `kiyosi::AnalyticDigitalEngine`

```cpp
class kiyosi::AnalyticDigitalEngine
```

Closed-form cash-or-nothing and asset-or-nothing valuation with analytic delta and gamma.

### Members

#### `price`

```cpp
Result<double> kiyosi::AnalyticDigitalEngine::price(const CashOrNothingOption &option, const PricingContext &context) const
```

Prices a European cash-or-nothing or asset-or-nothing option.
**Returns:** Price, or a contract or context error.

#### `price`

```cpp
Result<double> kiyosi::AnalyticDigitalEngine::price(const AssetOrNothingOption &option, const PricingContext &context) const
```

#### `price_with_greeks`

```cpp
Result<PricingResult> kiyosi::AnalyticDigitalEngine::price_with_greeks(const CashOrNothingOption &option, const PricingContext &context, GreeksRequest greeks, NumericalShiftSettings settings={}) const
```

Prices with the explicitly requested Greeks; unavailable measures remain empty.

#### `price_with_greeks`

```cpp
Result<PricingResult> kiyosi::AnalyticDigitalEngine::price_with_greeks(const AssetOrNothingOption &option, const PricingContext &context, GreeksRequest greeks, NumericalShiftSettings settings={}) const
```
