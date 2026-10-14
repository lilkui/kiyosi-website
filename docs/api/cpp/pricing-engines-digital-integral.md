---
description: C++ API declarations from kiyosi/pricing/engines/digital/integral.hpp.
outline: [2, 4]
---

# `<kiyosi/pricing/engines/digital/integral.hpp>`

```cpp
#include <kiyosi/pricing/engines/digital/integral.hpp>
```

## `kiyosi::QuadratureDigitalEngine`

```cpp
class kiyosi::QuadratureDigitalEngine
```

Simpson quadrature over the terminal lognormal density.

### Members

#### `price`

```cpp
Result<double> kiyosi::QuadratureDigitalEngine::price(const CashOrNothingOption &option, const PricingContext &context) const
```

Prices a cash-or-nothing option by numerical quadrature.
**Returns:** Price, or a contract or context error.

#### `price_with_greeks`

```cpp
Result<PricingResult> kiyosi::QuadratureDigitalEngine::price_with_greeks(const CashOrNothingOption &option, const PricingContext &context, GreeksRequest greeks, NumericalShiftSettings settings={}) const
```

Prices with the explicitly requested Greeks; unavailable measures remain empty.

#### `price`

```cpp
Result<double> kiyosi::QuadratureDigitalEngine::price(const AssetOrNothingOption &option, const PricingContext &context) const
```

Prices an asset-or-nothing option by numerical quadrature.
**Returns:** Price, or a contract or context error.

#### `price_with_greeks`

```cpp
Result<PricingResult> kiyosi::QuadratureDigitalEngine::price_with_greeks(const AssetOrNothingOption &option, const PricingContext &context, GreeksRequest greeks, NumericalShiftSettings settings={}) const
```

Prices with the explicitly requested Greeks; unavailable measures remain empty.
