---
description: C++ API declarations from kiyosi/pricing/engines/vanilla/analytic.hpp.
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

### Members

#### `price`

```cpp
Result<double> kiyosi::AnalyticVanillaEngine::price(const EuropeanOption &option, const PricingContext &context) const
```

Computes only price; returns intrinsic value at expiry_date.
**Returns:** Price, or a contract or context error.

#### `price_with_greeks`

```cpp
Result<PricingResult> kiyosi::AnalyticVanillaEngine::price_with_greeks(const EuropeanOption &option, const PricingContext &context, GreeksRequest greeks, NumericalShiftSettings settings={}) const
```

Prices with the explicitly requested Greeks; unavailable measures remain empty.
