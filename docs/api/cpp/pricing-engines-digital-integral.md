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
Result<PricingResult> kiyosi::QuadratureDigitalEngine::price(const CashOrNothingOption &, const PricingContext &) const
```

Prices a cash-or-nothing option by numerical quadrature. 
**Returns:** Pricing measures, or a contract or context error.

#### `price`

```cpp
Result<PricingResult> kiyosi::QuadratureDigitalEngine::price(const AssetOrNothingOption &, const PricingContext &) const
```

Prices an asset-or-nothing option by numerical quadrature. 
**Returns:** Pricing measures, or a contract or context error.
