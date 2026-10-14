---
description: kiyosi/pricing/engines/asian/analytic.hpp 中的 C++ API 声明。
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

Closed-form continuous geometric average-price option under lognormal spot.

### 成员

#### `price`

```cpp
Result<double> kiyosi::AnalyticGeometricAveragePriceEngine::price(const GeometricAveragePriceOption &option, const PricingContext &context) const
```

Prices a geometric-average option. Once averaging has begun, its realized average must be positive. Before averaging begins, the realized average must be zero.
**返回值:** Price, or a contract or context error.

#### `price_with_greeks`

```cpp
Result<PricingResult> kiyosi::AnalyticGeometricAveragePriceEngine::price_with_greeks(const GeometricAveragePriceOption &option, const PricingContext &context, GreeksRequest greeks, NumericalShiftSettings settings={}) const
```

Prices with the explicitly requested Greeks; unavailable measures remain empty.

## `kiyosi::TurnbullWakemanArithmeticAveragePriceEngine`

```cpp
class kiyosi::TurnbullWakemanArithmeticAveragePriceEngine
```

Turnbull-Wakeman moment-matched approximation for arithmetic averaging.

### 成员

#### `price`

```cpp
Result<double> kiyosi::TurnbullWakemanArithmeticAveragePriceEngine::price(const ArithmeticAveragePriceOption &option, const PricingContext &context) const
```

Prices an arithmetic-average option using moment matching. For a nonzero averaging window, the realized average must be zero before averaging begins and positive afterward. A zero-length window is a single fixing at expiry and follows European vanilla pricing before expiry.
**返回值:** Price, or a contract or context error.

#### `price_with_greeks`

```cpp
Result<PricingResult> kiyosi::TurnbullWakemanArithmeticAveragePriceEngine::price_with_greeks(const ArithmeticAveragePriceOption &option, const PricingContext &context, GreeksRequest greeks, NumericalShiftSettings settings={}) const
```

Prices with the explicitly requested Greeks; unavailable measures remain empty.
