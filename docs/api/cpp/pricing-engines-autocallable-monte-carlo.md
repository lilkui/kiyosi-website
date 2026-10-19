---
description: kiyosi/pricing/engines/autocallable/monte_carlo.hpp 中的 C++ API 声明。
outline: [2, 4]
---

# `<kiyosi/pricing/engines/autocallable/monte_carlo.hpp>`

```cpp
#include <kiyosi/pricing/engines/autocallable/monte_carlo.hpp>
```

## `make_monte_carlo_autocallable_engine`

```cpp
Result<MonteCarloAutocallableEngine> kiyosi::make_monte_carlo_autocallable_engine(TradingDayMonteCarloSettings settings)
```

Creates an engine after validating its configuration.
**返回值:** The engine, or an `invalid_parameter` error.

## `kiyosi::MonteCarloAutocallableEngine`

```cpp
class kiyosi::MonteCarloAutocallableEngine
```

Simulates observation dates and expiry, adding trading days for daily knock-in monitoring. Accepts 1..10,000,000 paths.

### 成员

#### `MonteCarloAutocallableEngine`

```cpp
kiyosi::MonteCarloAutocallableEngine::MonteCarloAutocallableEngine()=default
```

Creates an engine with valid default settings.

#### `price`

```cpp
template <AutocallableProduct Note>
Result<double> kiyosi::MonteCarloAutocallableEngine::price(const Note &note, const PricingContext &context) const
```

Prices an autocallable note by Monte Carlo simulation.
**返回值:** Price, or a contract, context, numerical, or backend error.

#### `price_with_greeks`

```cpp
template <AutocallableProduct Note>
Result<PricingResult> kiyosi::MonteCarloAutocallableEngine::price_with_greeks(const Note &option, const PricingContext &context, GreeksRequest greeks, NumericalShiftSettings settings={}) const
```

Prices with the explicitly requested Greeks; unavailable measures remain empty. CPU spot sensitivities share per-path draws with separate event states and per-block reduction storage.

#### `settings`

```cpp
TradingDayMonteCarloSettings kiyosi::MonteCarloAutocallableEngine::settings() const noexcept
```

Returns the engine settings.
