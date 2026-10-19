---
description: kiyosi/pricing/engines/accumulator/monte_carlo.hpp 中的 C++ API 声明。
outline: [2, 4]
---

# `<kiyosi/pricing/engines/accumulator/monte_carlo.hpp>`

```cpp
#include <kiyosi/pricing/engines/accumulator/monte_carlo.hpp>
```

## `make_monte_carlo_accumulator_engine`

```cpp
Result<MonteCarloAccumulatorEngine> kiyosi::make_monte_carlo_accumulator_engine(TradingDayMonteCarloSettings settings)
```

Creates an engine after validating its configuration.
**返回值:** The engine, or an `invalid_parameter` error.

## `kiyosi::MonteCarloAccumulatorEngine`

```cpp
class kiyosi::MonteCarloAccumulatorEngine
```

Simulates the trading-day accrual, terminating each path at the knock-out level. Accepts 1..10,000,000 paths.

### 成员

#### `MonteCarloAccumulatorEngine`

```cpp
kiyosi::MonteCarloAccumulatorEngine::MonteCarloAccumulatorEngine()=default
```

Creates an engine with valid default settings.

#### `price`

```cpp
Result<double> kiyosi::MonteCarloAccumulatorEngine::price(const Accumulator &option, const PricingContext &context) const
```

Prices an accumulator by Monte Carlo simulation.
**返回值:** Price, or a contract, context, numerical, or backend error.

#### `price_with_greeks`

```cpp
Result<PricingResult> kiyosi::MonteCarloAccumulatorEngine::price_with_greeks(const Accumulator &option, const PricingContext &context, GreeksRequest greeks, NumericalShiftSettings settings={}) const
```

Prices with the explicitly requested Greeks; unavailable measures remain empty. CPU spot bumps share per-call random draws and growth factors with per-block reduction storage.

#### `settings`

```cpp
TradingDayMonteCarloSettings kiyosi::MonteCarloAccumulatorEngine::settings() const noexcept
```

Returns the engine settings.
