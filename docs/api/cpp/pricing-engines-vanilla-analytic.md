---
description: C++ API declarations from kiyosi/pricing/engines/vanilla/analytic.hpp.
outline: [2, 4]
---

# `<kiyosi/pricing/engines/vanilla/analytic.hpp>`

```cpp
#include <kiyosi/pricing/engines/vanilla/analytic.hpp>
```

## `kiyosi::AnalyticVanillaEngine`

```cpp
class kiyosi::AnalyticVanillaEngine
```

Closed-form Black-Scholes-Merton engine for European vanilla options.

### Members

#### `price`

```cpp
template <OptionPayoff Payoff, OptionExercise Exercise>
Result<PricingResult> kiyosi::AnalyticVanillaEngine::price(const ExerciseBasedOption<Payoff, Exercise> &option, const PricingContext &context) const
```

Returns intrinsic value with Greeks unavailable when valued at expiry_date. 
**Returns:** Pricing measures, or a contract or context error.
