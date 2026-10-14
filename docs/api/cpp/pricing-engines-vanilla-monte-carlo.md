---
description: kiyosi/pricing/engines/vanilla/monte_carlo.hpp 中的 C++ API 声明。
outline: [2, 4]
---

# `<kiyosi/pricing/engines/vanilla/monte_carlo.hpp>`

```cpp
#include <kiyosi/pricing/engines/vanilla/monte_carlo.hpp>
```

## `kiyosi::MonteCarloVanillaEngine`

```cpp
class kiyosi::MonteCarloVanillaEngine
```

Monte Carlo valuation for vanilla European and American options. Accepts 1..10,000,000 paths and 2..10,000 steps; American pricing before expiry needs 3 steps. European prices sample the exact terminal distribution; the validated step count has no effect. American calls with nonpositive dividends and nonnegative rates use that distribution too, retaining the immediate-exercise lower bound. Rate stencils crossing zero use exercise-grid simulations on both sides to avoid mixing sampled estimators. American implied-volatility solves reuse request-local path and cash-flow buffers on CPU and device workspaces on CUDA; every trial recomputes its exercise decisions.

### 成员

#### `MonteCarloVanillaEngine`

```cpp
kiyosi::MonteCarloVanillaEngine::MonteCarloVanillaEngine(MonteCarloSettings settings={})
```

Creates an engine with aggregate Monte Carlo settings.

#### `MonteCarloVanillaEngine`

```cpp
kiyosi::MonteCarloVanillaEngine::MonteCarloVanillaEngine(int path_count, int step_count, std::optional<std::uint64_t> seed=MonteCarloSettings{}.seed, MonteCarloBackend backend=MonteCarloSettings{}.backend)
```

Creates an engine with explicit path count, step count, seed, and backend.

#### `price`

```cpp
Result<double> kiyosi::MonteCarloVanillaEngine::price(const EuropeanOption &option, const PricingContext &context) const
```

Prices a European or American vanilla option.
**返回值:** Price, or a contract, context, settings, or backend error.

#### `price`

```cpp
Result<double> kiyosi::MonteCarloVanillaEngine::price(const AmericanOption &option, const PricingContext &context) const
```

#### `price_with_greeks`

```cpp
Result<PricingResult> kiyosi::MonteCarloVanillaEngine::price_with_greeks(const EuropeanOption &option, const PricingContext &context, GreeksRequest greeks, NumericalShiftSettings settings={}) const
```

Prices with the explicitly requested Greeks; unavailable measures remain empty. CPU European requests with feasible stencils reuse per-call samples, with storage linear in path count. Requests without feasible stencils stream the scalar price without retaining samples. CPU and CUDA American requests reuse a path buffer; spot stencils also cache growth factors, adding about 8 bytes per rounded-even path per time interval. All storage is request-local.

#### `price_with_greeks`

```cpp
Result<PricingResult> kiyosi::MonteCarloVanillaEngine::price_with_greeks(const AmericanOption &option, const PricingContext &context, GreeksRequest greeks, NumericalShiftSettings settings) const
```

#### `price_with_greeks`

```cpp
Result<PricingResult> kiyosi::MonteCarloVanillaEngine::price_with_greeks(const AmericanOption &option, const PricingContext &context, GreeksRequest greeks) const
```

American exercise decisions amplify small-bump sampling noise. The default spot bump is 8% of spot; other shifts retain `NumericalShiftSettings` defaults. Explicit shifts are absolute. Estimates still have sampling error and bump-size bias; check convergence for the valuation.

#### `settings`

```cpp
MonteCarloSettings kiyosi::MonteCarloVanillaEngine::settings() const noexcept
```

Returns the engine settings.

#### `default_american_spot_shift`

```cpp
static double kiyosi::MonteCarloVanillaEngine::default_american_spot_shift(const PricingContext &context) noexcept
```

Core-owned default shared by C++ and language bindings.
