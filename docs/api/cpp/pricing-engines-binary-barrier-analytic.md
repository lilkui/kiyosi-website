---
description: C++ API declarations from kiyosi/pricing/engines/binary_barrier/analytic.hpp.
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

Closed-form Rubinstein-Reiner binary barrier and touch valuation.

### Members

#### `price`

```cpp
Result< PricingResult > kiyosi::AnalyticBinaryBarrierEngine::price(const BinaryBarrierOption &, const PricingContext &) const
```

Prices a strike-based binary barrier option. 
**Returns:** Pricing measures, or a contract, context, or unsupported-operation error.

#### `price`

```cpp
Result< PricingResult > kiyosi::AnalyticBinaryBarrierEngine::price(const TouchOption &, const PricingContext &) const
```

Prices a one-touch or no-touch option. 
**Returns:** Pricing measures, or a contract, context, or unsupported-operation error.
