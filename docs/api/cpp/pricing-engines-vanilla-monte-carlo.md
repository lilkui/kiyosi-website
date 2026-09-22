---
description: C++ API declarations from kiyosi/pricing/engines/vanilla/monte_carlo.hpp.
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

Monte Carlo valuation for vanilla European and American options.

### Members

#### `MonteCarloVanillaEngine`

```cpp
kiyosi::MonteCarloVanillaEngine::MonteCarloVanillaEngine(MonteCarloSettings settings={})
```

Creates an engine with aggregate Monte Carlo settings.

#### `MonteCarloVanillaEngine`

```cpp
kiyosi::MonteCarloVanillaEngine::MonteCarloVanillaEngine(int path_count, int step_count, std::optional< std::uint64_t > seed=MonteCarloSettings{}.seed, MonteCarloBackend backend=MonteCarloSettings{}.backend)
```

Creates an engine with explicit path count, step count, seed, and backend.

#### `price`

```cpp
template <OptionPayoff Payoff, OptionExercise Exercise>
Result< PricingResult > kiyosi::MonteCarloVanillaEngine::price(const ExerciseBasedOption< Payoff, Exercise > &option, const PricingContext &context) const
```

Prices a European or American vanilla option. 
**Returns:** Pricing measures, or a contract, context, settings, or backend error.

#### `settings`

```cpp
MonteCarloSettings kiyosi::MonteCarloVanillaEngine::settings() const noexcept
```

Returns the engine settings.
