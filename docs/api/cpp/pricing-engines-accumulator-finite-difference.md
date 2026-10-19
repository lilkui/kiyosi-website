---
description: kiyosi/pricing/engines/accumulator/finite_difference.hpp 中的 C++ API 声明。
outline: [2, 4]
---

# `<kiyosi/pricing/engines/accumulator/finite_difference.hpp>`

```cpp
#include <kiyosi/pricing/engines/accumulator/finite_difference.hpp>
```

## `make_finite_difference_accumulator_engine`

```cpp
Result<FiniteDifferenceAccumulatorEngine> kiyosi::make_finite_difference_accumulator_engine(FiniteDifferenceSettings settings)
```

Creates an engine after validating its configuration.
**返回值:** The engine, or an `invalid_parameter` error.

## `kiyosi::FiniteDifferenceAccumulatorEngine`

```cpp
class kiyosi::FiniteDifferenceAccumulatorEngine
```

Marches the accrual value back as an affine function of the accumulated quantity, so a single sweep prices every opening position. Accepts 3..2,000 asset steps and 1..2,000 time steps.

### 成员

#### `FiniteDifferenceAccumulatorEngine`

```cpp
kiyosi::FiniteDifferenceAccumulatorEngine::FiniteDifferenceAccumulatorEngine()=default
```

Creates an engine with valid default settings.

#### `price`

```cpp
Result<double> kiyosi::FiniteDifferenceAccumulatorEngine::price(const Accumulator &option, const PricingContext &context) const
```

Prices an accumulator by finite differences.
**返回值:** Price, or a contract, context, or numerical error.

#### `price_with_greeks`

```cpp
Result<PricingResult> kiyosi::FiniteDifferenceAccumulatorEngine::price_with_greeks(const Accumulator &option, const PricingContext &context, GreeksRequest greeks, NumericalShiftSettings settings={}) const
```

Prices with the explicitly requested Greeks; unavailable measures remain empty. Delta, gamma, and speed reuse the solved layers; vanna/zomma and charm/color difference native delta/gamma shifted in volatility and time. Other measures use numerical price differences.

#### `settings`

```cpp
FiniteDifferenceSettings kiyosi::FiniteDifferenceAccumulatorEngine::settings() const noexcept
```

Returns the engine settings.
