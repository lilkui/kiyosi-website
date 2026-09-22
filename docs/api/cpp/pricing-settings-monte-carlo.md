---
description: C++ API declarations from kiyosi/pricing/settings/monte_carlo.hpp.
outline: [2, 4]
---

# `<kiyosi/pricing/settings/monte_carlo.hpp>`

```cpp
#include <kiyosi/pricing/settings/monte_carlo.hpp>
```

## `MonteCarloBackend`

```cpp
enum class MonteCarloBackend
```

Execution backends supported by Monte Carlo engines.

**Values**

- `cpu` — Host CPU implementation.
- `cuda` — CUDA implementation, when built and available.

## `kiyosi::MonteCarloSettings`

```cpp
struct kiyosi::MonteCarloSettings
```

Path simulation over a uniform time grid, validated when price() is called; an absent seed draws from the system entropy source.

### Members

#### `path_count`

```cpp
int kiyosi::MonteCarloSettings::path_count
```

Number of simulated paths; must be positive.

#### `step_count`

```cpp
int kiyosi::MonteCarloSettings::step_count
```

Uniform time steps per path; must be positive.

#### `seed`

```cpp
std::optional<std::uint64_t> kiyosi::MonteCarloSettings::seed
```

Deterministic seed, or system entropy when absent.

#### `backend`

```cpp
MonteCarloBackend kiyosi::MonteCarloSettings::backend
```

Execution backend.

## `kiyosi::TradingDayMonteCarloSettings`

```cpp
struct kiyosi::TradingDayMonteCarloSettings
```

Structured products step the trading calendar directly, so no step count is needed; settings are validated when price() is called.

### Members

#### `path_count`

```cpp
int kiyosi::TradingDayMonteCarloSettings::path_count
```

Number of simulated paths; must be positive.

#### `seed`

```cpp
std::optional<std::uint64_t> kiyosi::TradingDayMonteCarloSettings::seed
```

Deterministic seed, or system entropy when absent.

#### `backend`

```cpp
MonteCarloBackend kiyosi::TradingDayMonteCarloSettings::backend
```

Execution backend.
