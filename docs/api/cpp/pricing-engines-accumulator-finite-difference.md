---
description: C++ API declarations from kiyosi/pricing/engines/accumulator/finite_difference.hpp.
outline: [2, 4]
---

# `<kiyosi/pricing/engines/accumulator/finite_difference.hpp>`

```cpp
#include <kiyosi/pricing/engines/accumulator/finite_difference.hpp>
```

## `kiyosi::FiniteDifferenceAccumulatorEngine`

```cpp
class kiyosi::FiniteDifferenceAccumulatorEngine
```

Marches the accrual value back as an affine function of the accumulated quantity, so a single sweep prices every opening position.

### Members

#### `FiniteDifferenceAccumulatorEngine`

```cpp
kiyosi::FiniteDifferenceAccumulatorEngine::FiniteDifferenceAccumulatorEngine(FiniteDifferenceSettings settings={})
```

Creates an engine with aggregate finite-difference settings.

#### `FiniteDifferenceAccumulatorEngine`

```cpp
kiyosi::FiniteDifferenceAccumulatorEngine::FiniteDifferenceAccumulatorEngine(int asset_step_count, int time_step_count, FiniteDifferenceScheme scheme=FiniteDifferenceSettings{}.scheme)
```

Creates an engine with explicit grid dimensions and scheme.

#### `price`

```cpp
Result<PricingResult> kiyosi::FiniteDifferenceAccumulatorEngine::price(const Accumulator &, const PricingContext &) const
```

Prices an accumulator by finite differences. 
**Returns:** Pricing measures, or a contract, context, or settings error.

#### `settings`

```cpp
FiniteDifferenceSettings kiyosi::FiniteDifferenceAccumulatorEngine::settings() const noexcept
```

Returns the engine settings.
