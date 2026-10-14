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

Execution backends supported by Monte Carlo engines. CUDA operations use the calling thread's current device and leave it unchanged. Each call owns a nonblocking stream and waits only for its own work, including cleanup. The device and runtime must support CUDA stream-ordered memory allocation.

**Values**

- `cpu` — Host CPU implementation.
- `cuda` — CUDA implementation, when built and available.

## `kiyosi::MonteCarloSettings`

```cpp
struct kiyosi::MonteCarloSettings
```

Vanilla simulation settings, validated when price() is called; an absent seed draws from the system entropy source. Vanilla engines accept 1..10,000,000 paths and 2..10,000 steps; American pricing before expiry requires at least 3 steps. European pricing samples the exact terminal distribution without intermediate steps.

### Members

#### `path_count`

```cpp
int kiyosi::MonteCarloSettings::path_count
```

Number of simulated paths; 1..10,000,000.

#### `step_count`

```cpp
int kiyosi::MonteCarloSettings::step_count
```

American grid points; 2..10,000 (American: >= 3); validated but unused for European pricing.

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

`Accumulator` and autocallable products step the trading calendar directly, so no step count is needed; settings are validated when price() is called. These engines accept 1..10,000,000 paths. CPU paths use separate PCG32 streams, so early knock-out cannot shift later paths' draws. Seeded prices are reproducible within a library version, standard-library implementation and backend.

### Members

#### `path_count`

```cpp
int kiyosi::TradingDayMonteCarloSettings::path_count
```

Number of simulated paths; 1..10,000,000.

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
