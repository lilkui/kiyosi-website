---
description: C++ API declarations from kiyosi/pricing/engines/vanilla/integral.hpp.
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

### Members

#### `price`

```cpp
template <OptionPayoff Payoff, OptionExercise Exercise>
Result<PricingResult> kiyosi::QuadratureVanillaEngine::price(const ExerciseBasedOption<Payoff, Exercise> &option, const PricingContext &context) const
```

Prices a European vanilla option by numerical quadrature. 
**Returns:** Pricing measures, or a contract or context error.
