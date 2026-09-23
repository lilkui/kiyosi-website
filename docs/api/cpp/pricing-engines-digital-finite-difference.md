---
description: C++ API declarations from kiyosi/pricing/engines/digital/finite_difference.hpp.
outline: [2, 4]
---

# `<kiyosi/pricing/engines/digital/finite_difference.hpp>`

```cpp
#include <kiyosi/pricing/engines/digital/finite_difference.hpp>
```

## `kiyosi::FiniteDifferenceDigitalEngine`

```cpp
class kiyosi::FiniteDifferenceDigitalEngine
```

Uniform-grid finite-difference engine for European digital options.

### Members

#### `FiniteDifferenceDigitalEngine`

```cpp
kiyosi::FiniteDifferenceDigitalEngine::FiniteDifferenceDigitalEngine(FiniteDifferenceSettings settings={})
```

Creates an engine with aggregate finite-difference settings.

#### `FiniteDifferenceDigitalEngine`

```cpp
kiyosi::FiniteDifferenceDigitalEngine::FiniteDifferenceDigitalEngine(int asset_step_count, int time_step_count, FiniteDifferenceScheme scheme=FiniteDifferenceSettings{}.scheme)
```

Creates an engine with explicit grid dimensions and scheme.

#### `price`

```cpp
template <OptionPayoff Payoff, OptionExercise Exercise>
Result<PricingResult> kiyosi::FiniteDifferenceDigitalEngine::price(const ExerciseBasedOption<Payoff, Exercise> &option, const PricingContext &context) const
```

Prices a European cash-or-nothing or asset-or-nothing option. 
**Returns:** Pricing measures, or a contract, context, or settings error.

#### `settings`

```cpp
FiniteDifferenceSettings kiyosi::FiniteDifferenceDigitalEngine::settings() const noexcept
```

Returns the engine settings.
