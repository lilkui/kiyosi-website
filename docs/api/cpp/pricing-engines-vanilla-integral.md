---
description: kiyosi/pricing/engines/vanilla/integral.hpp 中的 C++ API 声明。
outline: [2, 4]
---

# `<kiyosi/pricing/engines/vanilla/integral.hpp>`

```cpp
#include <kiyosi/pricing/engines/vanilla/integral.hpp>
```

## `kiyosi::QuadratureVanillaEngine`

```cpp
class kiyosi::QuadratureVanillaEngine
```

Simpson quadrature over the terminal lognormal density.

### 成员

#### `price`

```cpp
Result<double> kiyosi::QuadratureVanillaEngine::price(const EuropeanOption &option, const PricingContext &context) const
```

Prices a European vanilla option by numerical quadrature.
**返回值:** Price, or a contract or context error.

#### `price_with_greeks`

```cpp
Result<PricingResult> kiyosi::QuadratureVanillaEngine::price_with_greeks(const EuropeanOption &option, const PricingContext &context, GreeksRequest greeks, NumericalShiftSettings settings={}) const
```

Prices with the explicitly requested Greeks; unavailable measures remain empty.
