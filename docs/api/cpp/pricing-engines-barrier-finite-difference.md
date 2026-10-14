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

Uniform-grid finite-difference engine for barrier options. Accepts 3..10,000 asset steps and 1..100,000 time steps.

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
Result<double> kiyosi::FiniteDifferenceBarrierEngine::price(const BarrierOption &option, const PricingContext &context) const
```

Prices a barrier option by finite differences.
**Returns:** Price, or a contract, context, or settings error.

#### `price_with_greeks`

```cpp
Result<PricingResult> kiyosi::FiniteDifferenceBarrierEngine::price_with_greeks(const BarrierOption &option, const PricingContext &context, GreeksRequest greeks, NumericalShiftSettings settings={}) const
```

Prices with the explicitly requested Greeks; unavailable measures remain empty. Delta, gamma, and speed reuse the solved layer; vanna/zomma and charm/color difference native delta/gamma shifted in volatility and time. Other measures use numerical price differences. Scheduled observation dates are validated once per request; shifted valuations retain their other checks.

#### `settings`

```cpp
FiniteDifferenceSettings kiyosi::FiniteDifferenceBarrierEngine::settings() const noexcept
```

Returns the engine settings.
