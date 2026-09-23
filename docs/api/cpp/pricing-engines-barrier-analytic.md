---
description: C++ API declarations from kiyosi/pricing/engines/barrier/analytic.hpp.
outline: [2, 4]
---

# `<kiyosi/pricing/engines/barrier/analytic.hpp>`

```cpp
#include <kiyosi/pricing/engines/barrier/analytic.hpp>
```

## `kiyosi::AnalyticBarrierEngine`

```cpp
class kiyosi::AnalyticBarrierEngine
```

Closed-form Reiner-Rubinstein barrier valuation with a BGK shift for scheduled monitoring.

### Members

#### `price`

```cpp
Result<PricingResult> kiyosi::AnalyticBarrierEngine::price(const BarrierOption &, const PricingContext &) const
```

Prices a barrier option analytically. 
**Returns:** Pricing measures, or a contract, context, or unsupported-operation error.
