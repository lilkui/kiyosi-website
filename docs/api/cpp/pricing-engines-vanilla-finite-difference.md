---
description: C++ API declarations from kiyosi/pricing/engines/vanilla/finite_difference.hpp.
outline: [2, 4]
---

# `<kiyosi/pricing/engines/vanilla/finite_difference.hpp>`

```cpp
#include <kiyosi/pricing/engines/vanilla/finite_difference.hpp>
```

## `kiyosi::FiniteDifferenceVanillaEngine`

```cpp
class kiyosi::FiniteDifferenceVanillaEngine
```

Uniform-grid finite-difference engine for vanilla European and American options.

### Members

#### `FiniteDifferenceVanillaEngine`

```cpp
kiyosi::FiniteDifferenceVanillaEngine::FiniteDifferenceVanillaEngine(FiniteDifferenceSettings settings={})
```

Creates an engine with aggregate finite-difference settings.

#### `FiniteDifferenceVanillaEngine`

```cpp
kiyosi::FiniteDifferenceVanillaEngine::FiniteDifferenceVanillaEngine(int asset_step_count, int time_step_count, FiniteDifferenceScheme scheme=FiniteDifferenceSettings{}.scheme)
```

Creates an engine with explicit grid dimensions and scheme.

#### `price`

```cpp
template <OptionPayoff Payoff, OptionExercise Exercise>
Result<PricingResult> kiyosi::FiniteDifferenceVanillaEngine::price(const ExerciseBasedOption<Payoff, Exercise> &option, const PricingContext &context) const
```

Prices a European or American vanilla option. 
**Returns:** Pricing measures, or a contract, context, or settings error.

#### `settings`

```cpp
FiniteDifferenceSettings kiyosi::FiniteDifferenceVanillaEngine::settings() const noexcept
```

Returns the engine settings.
