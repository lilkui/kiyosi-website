---
description: kiyosi/pricing/engines/binary_barrier/analytic.hpp 中的 C++ API 声明。
outline: [2, 4]
---

# `<kiyosi/pricing/engines/binary_barrier/analytic.hpp>`

```cpp
#include <kiyosi/pricing/engines/binary_barrier/analytic.hpp>
```

## `kiyosi::AnalyticBinaryBarrierEngine`

```cpp
class kiyosi::AnalyticBinaryBarrierEngine
```

Closed-form Rubinstein-Reiner binary barrier and touch valuation. Scheduled monitoring uses a BGK barrier shift. Untouched contracts with future observations require a final observation at expiry; shorter windows return unsupported_operation. Spot must lie strictly on the unbreached side of the shifted barrier; otherwise the approximation returns unsupported_operation. Resolved settlements remain supported. `Greek` requests validate scheduled dates once per call against the context's calendar.

### 成员

#### `price`

```cpp
Result<double> kiyosi::AnalyticBinaryBarrierEngine::price(const BinaryBarrierOption &option, const PricingContext &context) const
```

Prices a strike-based binary barrier option.
**返回值:** Price, or a contract, context, or unsupported-operation error.

#### `price_with_greeks`

```cpp
Result<PricingResult> kiyosi::AnalyticBinaryBarrierEngine::price_with_greeks(const BinaryBarrierOption &option, const PricingContext &context, GreeksRequest greeks, NumericalShiftSettings settings={}) const
```

Prices with the explicitly requested Greeks; unavailable measures remain empty.

#### `price`

```cpp
Result<double> kiyosi::AnalyticBinaryBarrierEngine::price(const TouchOption &option, const PricingContext &context) const
```

Prices a one-touch or no-touch option.
**返回值:** Price, or a contract, context, or unsupported-operation error.

#### `price_with_greeks`

```cpp
Result<PricingResult> kiyosi::AnalyticBinaryBarrierEngine::price_with_greeks(const TouchOption &option, const PricingContext &context, GreeksRequest greeks, NumericalShiftSettings settings={}) const
```

Prices with the explicitly requested Greeks; unavailable measures remain empty.
