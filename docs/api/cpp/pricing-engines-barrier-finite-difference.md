---
description: C++ API declarations from kiyosi/pricing/engines/barrier/finite_difference.hpp.
outline: [2, 4]
---

# `<kiyosi/pricing/engines/barrier/finite_difference.hpp>`

```cpp
#include <kiyosi/pricing/engines/barrier/finite_difference.hpp>
```

## `kiyosi::FiniteDifferenceBarrierEngine`

```cpp
class kiyosi::FiniteDifferenceBarrierEngine
```

Uniform-grid finite-difference engine for barrier options.

### Members

#### `FiniteDifferenceBarrierEngine`

```cpp
kiyosi::FiniteDifferenceBarrierEngine::FiniteDifferenceBarrierEngine(FiniteDifferenceSettings settings={})
```

Creates an engine with aggregate finite-difference settings.

#### `FiniteDifferenceBarrierEngine`

```cpp
kiyosi::FiniteDifferenceBarrierEngine::FiniteDifferenceBarrierEngine(int asset_step_count, int time_step_count, FiniteDifferenceScheme scheme=FiniteDifferenceSettings{}.scheme)
```

Creates an engine with explicit grid dimensions and scheme.

#### `price`

```cpp
Result< PricingResult > kiyosi::FiniteDifferenceBarrierEngine::price(const BarrierOption &option, const PricingContext &context) const
```

Prices a barrier option by finite differences. 
**Returns:** Pricing measures, or a contract, context, or settings error.

#### `settings`

```cpp
FiniteDifferenceSettings kiyosi::FiniteDifferenceBarrierEngine::settings() const noexcept
```

Returns the engine settings.
