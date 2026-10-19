---
description: kiyosi/pricing/engines/barrier/finite_difference.hpp 中的 C++ API 声明。
outline: [2, 4]
---

# `<kiyosi/pricing/engines/barrier/finite_difference.hpp>`

```cpp
#include <kiyosi/pricing/engines/barrier/finite_difference.hpp>
```

## `make_finite_difference_barrier_engine`

```cpp
Result<FiniteDifferenceBarrierEngine> kiyosi::make_finite_difference_barrier_engine(FiniteDifferenceSettings settings)
```

Creates an engine after validating its configuration.
**返回值:** The engine, or an `invalid_parameter` error.

## `kiyosi::FiniteDifferenceBarrierEngine`

```cpp
class kiyosi::FiniteDifferenceBarrierEngine
```

Uniform-grid finite-difference engine for barrier options. Accepts 3..10,000 asset steps and 1..100,000 time steps.

### 成员

#### `FiniteDifferenceBarrierEngine`

```cpp
kiyosi::FiniteDifferenceBarrierEngine::FiniteDifferenceBarrierEngine()=default
```

Creates an engine with valid default settings.

#### `price`

```cpp
Result<double> kiyosi::FiniteDifferenceBarrierEngine::price(const BarrierOption &option, const PricingContext &context) const
```

Prices a barrier option by finite differences.
**返回值:** Price, or a contract, context, or numerical error.

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
