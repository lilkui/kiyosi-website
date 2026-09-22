---
description: C++ API declarations from kiyosi/pricing/engines/digital/analytic.hpp.
outline: [2, 4]
---

# `<kiyosi/pricing/engines/digital/analytic.hpp>`

```cpp
#include <kiyosi/pricing/engines/digital/analytic.hpp>
```

## `kiyosi::AnalyticDigitalEngine`

```cpp
class kiyosi::AnalyticDigitalEngine
```

Closed-form cash-or-nothing and asset-or-nothing valuation with analytic delta and gamma.

### Members

#### `price`

```cpp
template <OptionPayoff Payoff, OptionExercise Exercise>
Result< PricingResult > kiyosi::AnalyticDigitalEngine::price(const ExerciseBasedOption< Payoff, Exercise > &option, const PricingContext &context) const
```

Prices a European cash-or-nothing or asset-or-nothing option. 
**Returns:** Pricing measures, or a contract or context error.
