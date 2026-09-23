---
description: C++ API declarations from kiyosi/pricing/engines/asian/analytic.hpp.
outline: [2, 4]
---

# `<kiyosi/pricing/engines/asian/analytic.hpp>`

```cpp
#include <kiyosi/pricing/engines/asian/analytic.hpp>
```

## `kiyosi::AnalyticGeometricAveragePriceEngine`

```cpp
class kiyosi::AnalyticGeometricAveragePriceEngine
```

Closed-form geometric average-rate option under lognormal spot.

### Members

#### `price`

```cpp
Result<PricingResult> kiyosi::AnalyticGeometricAveragePriceEngine::price(const GeometricAveragePriceOption &, const PricingContext &) const
```

Prices a geometric-average option. 
**Returns:** Pricing measures, or a contract or context error.

## `kiyosi::TurnbullWakemanArithmeticAveragePriceEngine`

```cpp
class kiyosi::TurnbullWakemanArithmeticAveragePriceEngine
```

Turnbull-Wakeman moment-matched approximation for arithmetic averaging.

### Members

#### `price`

```cpp
Result<PricingResult> kiyosi::TurnbullWakemanArithmeticAveragePriceEngine::price(const ArithmeticAveragePriceOption &, const PricingContext &) const
```

Prices an arithmetic-average option using moment matching. 
**Returns:** Pricing measures, or a contract or context error.
