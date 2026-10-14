---
description: kiyosi/pricing/engines/vanilla/analytic.hpp 中的 C++ API 声明。
outline: [2, 4]
---

# `<kiyosi/pricing/engines/vanilla/analytic.hpp>`

```cpp
#include <kiyosi/pricing/engines/vanilla/analytic.hpp>
```

## `kiyosi::AnalyticVanillaEngine`

```cpp
class kiyosi::AnalyticVanillaEngine
```

Closed-form Black-Scholes-Merton engine for European vanilla options.

### 成员

#### `price`

```cpp
Result<double> kiyosi::AnalyticVanillaEngine::price(const EuropeanOption &option, const PricingContext &context) const
```

Computes only price; returns intrinsic value at expiry_date.
**返回值:** Price, or a contract or context error.

#### `price_with_greeks`

```cpp
Result<PricingResult> kiyosi::AnalyticVanillaEngine::price_with_greeks(const EuropeanOption &option, const PricingContext &context, GreeksRequest greeks, NumericalShiftSettings settings={}) const
```

Prices with the explicitly requested Greeks; unavailable measures remain empty.
