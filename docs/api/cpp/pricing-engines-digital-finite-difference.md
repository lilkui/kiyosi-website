---
description: kiyosi/pricing/engines/digital/finite_difference.hpp 中的 C++ API 声明。
outline: [2, 4]
---

# `<kiyosi/pricing/engines/digital/finite_difference.hpp>`

```cpp
#include <kiyosi/pricing/engines/digital/finite_difference.hpp>
```

## `make_finite_difference_digital_engine`

```cpp
Result<FiniteDifferenceDigitalEngine> kiyosi::make_finite_difference_digital_engine(FiniteDifferenceSettings settings)
```

Creates an engine after validating its configuration.
**返回值:** The engine, or an `invalid_parameter` error.

## `kiyosi::FiniteDifferenceDigitalEngine`

```cpp
class kiyosi::FiniteDifferenceDigitalEngine
```

Uniform-grid finite-difference engine for European digital options. Upper-edge values use BSM exercise probabilities at each time step. Accepts 3..10,000 asset steps and 1..100,000 time steps. Prices materially outside the non-negative payoff bounds return `invalid_result`.

### 成员

#### `FiniteDifferenceDigitalEngine`

```cpp
kiyosi::FiniteDifferenceDigitalEngine::FiniteDifferenceDigitalEngine()=default
```

Creates an engine with valid default settings.

#### `price`

```cpp
Result<double> kiyosi::FiniteDifferenceDigitalEngine::price(const CashOrNothingOption &option, const PricingContext &context) const
```

Prices a European cash-or-nothing or asset-or-nothing option.
**返回值:** Price, or a contract, context, or numerical error.

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
