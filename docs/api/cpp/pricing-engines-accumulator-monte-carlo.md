---
description: C++ API declarations from kiyosi/pricing/engines/accumulator/monte_carlo.hpp.
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

Simulates the trading-day accrual, terminating each path at the knock-out level.

### Members

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
Result<PricingResult> kiyosi::MonteCarloAccumulatorEngine::price(const Accumulator &, const PricingContext &) const
```

Prices an accumulator by Monte Carlo simulation. 
**Returns:** Pricing measures, or a contract, context, settings, or backend error.

#### `settings`

```cpp
TradingDayMonteCarloSettings kiyosi::MonteCarloAccumulatorEngine::settings() const noexcept
```

Returns the engine settings.
