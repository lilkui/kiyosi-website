---
description: kiyosi/pricing/engines/digital/finite_difference.hpp 中的 C++ API 声明。
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

Uniform-grid finite-difference engine for European digital options. Upper-edge values use BSM exercise probabilities at each time step. Accepts 3..10,000 asset steps and 1..100,000 time steps. Prices materially outside the non-negative payoff bounds return `invalid_result`.

### 成员

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
Result<double> kiyosi::FiniteDifferenceDigitalEngine::price(const CashOrNothingOption &option, const PricingContext &context) const
```

Prices a European cash-or-nothing or asset-or-nothing option.
**返回值:** Price, or a contract, context, or settings error.

#### `price`

```cpp
Result<double> kiyosi::FiniteDifferenceDigitalEngine::price(const AssetOrNothingOption &option, const PricingContext &context) const
```

#### `price_with_greeks`

```cpp
Result<PricingResult> kiyosi::FiniteDifferenceDigitalEngine::price_with_greeks(const CashOrNothingOption &option, const PricingContext &context, GreeksRequest greeks, NumericalShiftSettings settings={}) const
```

Prices with the explicitly requested Greeks; unavailable measures remain empty. Delta, gamma, and speed reuse the solved layer.

#### `price_with_greeks`

```cpp
Result<PricingResult> kiyosi::FiniteDifferenceDigitalEngine::price_with_greeks(const AssetOrNothingOption &option, const PricingContext &context, GreeksRequest greeks, NumericalShiftSettings settings={}) const
```

#### `settings`

```cpp
FiniteDifferenceSettings kiyosi::FiniteDifferenceDigitalEngine::settings() const noexcept
```

Returns the engine settings.
