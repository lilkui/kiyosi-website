---
description: kiyosi/pricing/engines/accumulator/monte_carlo.hpp 中的 C++ API 声明。
outline: [2, 4]
---

# `<kiyosi/pricing/engines/accumulator/monte_carlo.hpp>`

```cpp
#include <kiyosi/pricing/engines/accumulator/monte_carlo.hpp>
```

## `kiyosi::MonteCarloAccumulatorEngine`

```cpp
class kiyosi::MonteCarloAccumulatorEngine
```

Simulates the trading-day accrual, terminating each path at the knock-out level. Accepts 1..10,000,000 paths.

### 成员

#### `MonteCarloAccumulatorEngine`

```cpp
kiyosi::MonteCarloAccumulatorEngine::MonteCarloAccumulatorEngine(TradingDayMonteCarloSettings settings={})
```

Creates an engine with aggregate trading-day simulation settings.

#### `MonteCarloAccumulatorEngine`

```cpp
kiyosi::MonteCarloAccumulatorEngine::MonteCarloAccumulatorEngine(int path_count, std::optional<std::uint64_t> seed=TradingDayMonteCarloSettings{}.seed, MonteCarloBackend backend=TradingDayMonteCarloSettings{}.backend)
```

Creates an engine with explicit path count, seed, and backend.

#### `price`

```cpp
Result<double> kiyosi::MonteCarloAccumulatorEngine::price(const Accumulator &option, const PricingContext &context) const
```

Prices an accumulator by Monte Carlo simulation.
**返回值:** Price, or a contract, context, settings, or backend error.

#### `price_with_greeks`

```cpp
Result<PricingResult> kiyosi::MonteCarloAccumulatorEngine::price_with_greeks(const Accumulator &option, const PricingContext &context, GreeksRequest greeks, NumericalShiftSettings settings={}) const
```

Prices with the explicitly requested Greeks; unavailable measures remain empty. CPU spot bumps share per-call random draws and growth factors with storage independent of path count.

#### `settings`

```cpp
TradingDayMonteCarloSettings kiyosi::MonteCarloAccumulatorEngine::settings() const noexcept
```

Returns the engine settings.
