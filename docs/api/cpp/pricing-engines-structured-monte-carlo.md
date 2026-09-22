---
description: C++ API declarations from kiyosi/pricing/engines/structured/monte_carlo.hpp.
outline: [2, 4]
---

# `<kiyosi/pricing/engines/structured/monte_carlo.hpp>`

```cpp
#include <kiyosi/pricing/engines/structured/monte_carlo.hpp>
```

## `MonteCarloPhoenixEngine`

```cpp
using kiyosi::MonteCarloPhoenixEngine = MonteCarloAutocallableEngine<PhoenixOption>
```

Monte Carlo engine for Phoenix options.

## `MonteCarloSnowballEngine`

```cpp
using kiyosi::MonteCarloSnowballEngine = MonteCarloAutocallableEngine<SnowballOption>
```

Monte Carlo engine for snowball options.

## `MonteCarloBinarySnowballEngine`

```cpp
using kiyosi::MonteCarloBinarySnowballEngine = MonteCarloAutocallableEngine<BinarySnowballOption>
```

Monte Carlo engine for binary snowball options.

## `MonteCarloTernarySnowballEngine`

```cpp
using kiyosi::MonteCarloTernarySnowballEngine = MonteCarloAutocallableEngine<TernarySnowballOption>
```

Monte Carlo engine for ternary snowball options.

## `kiyosi::MonteCarloAutocallableEngine`

```cpp
template <typename Note>
class kiyosi::MonteCarloAutocallableEngine
```

Steps the trading calendar path by path, applying knock-in, knock-out, and coupon events.

### Members

#### `MonteCarloAutocallableEngine`

```cpp
kiyosi::MonteCarloAutocallableEngine< Note >::MonteCarloAutocallableEngine(TradingDayMonteCarloSettings settings={})
```

Creates an engine with aggregate trading-day simulation settings.

#### `MonteCarloAutocallableEngine`

```cpp
kiyosi::MonteCarloAutocallableEngine< Note >::MonteCarloAutocallableEngine(int path_count, std::optional< std::uint64_t > seed=TradingDayMonteCarloSettings{}.seed, MonteCarloBackend backend=TradingDayMonteCarloSettings{}.backend)
```

Creates an engine with explicit path count, seed, and backend.

#### `price`

```cpp
Result< PricingResult > kiyosi::MonteCarloAutocallableEngine< Note >::price(const Note &, const PricingContext &) const
```

Prices an autocallable note by Monte Carlo simulation. 
**Returns:** Pricing measures, or a contract, context, settings, or backend error.

#### `settings`

```cpp
TradingDayMonteCarloSettings kiyosi::MonteCarloAutocallableEngine< Note >::settings() const noexcept
```

Returns the engine settings.
