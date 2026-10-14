---
description: kiyosi/pricing/engines/barrier/analytic.hpp 中的 C++ API 声明。
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

Closed-form Reiner-Rubinstein barrier valuation with a BGK shift for scheduled monitoring. Untouched contracts with future scheduled observations require a final observation at expiry; shorter monitoring windows return unsupported_operation. Spot must lie strictly on the unbreached side of the shifted barrier; otherwise the approximation returns unsupported_operation. Resolved settlements remain supported.

### 成员

#### `price`

```cpp
Result<double> kiyosi::AnalyticBarrierEngine::price(const BarrierOption &option, const PricingContext &context) const
```

Prices a barrier option analytically.
**返回值:** Price, or a contract, context, or unsupported-operation error.

#### `price_with_greeks`

```cpp
Result<PricingResult> kiyosi::AnalyticBarrierEngine::price_with_greeks(const BarrierOption &option, const PricingContext &context, GreeksRequest greeks, NumericalShiftSettings settings={}) const
```

Prices with the explicitly requested Greeks; unavailable measures remain empty. Scheduled dates are validated once per call against the context's calendar.
