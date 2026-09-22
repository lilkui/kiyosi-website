---
description: C++ API declarations from kiyosi/pricing/engines/vanilla/bjerksund_stensland.hpp.
outline: [2, 4]
---

# `<kiyosi/pricing/engines/vanilla/bjerksund_stensland.hpp>`

```cpp
#include <kiyosi/pricing/engines/vanilla/bjerksund_stensland.hpp>
```

## `kiyosi::BjerksundStenslandVanillaEngine`

```cpp
class kiyosi::BjerksundStenslandVanillaEngine
```

Bjerksund-Stensland (2002) two-step American approximation.

### Members

#### `price`

```cpp
template <OptionPayoff Payoff, OptionExercise Exercise>
Result< PricingResult > kiyosi::BjerksundStenslandVanillaEngine::price(const ExerciseBasedOption< Payoff, Exercise > &option, const PricingContext &context) const
```

Prices an American vanilla option with the two-step approximation. 
**Returns:** Pricing measures, or a contract or context error.
