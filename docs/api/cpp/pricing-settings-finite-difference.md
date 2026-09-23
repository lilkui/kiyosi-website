---
description: C++ API declarations from kiyosi/pricing/settings/finite_difference.hpp.
outline: [2, 4]
---

# `<kiyosi/pricing/settings/finite_difference.hpp>`

```cpp
#include <kiyosi/pricing/settings/finite_difference.hpp>
```

## `FiniteDifferenceScheme`

```cpp
enum class FiniteDifferenceScheme
```

Time-marching schemes supported by finite-difference engines.

**Values**

- `explicit_euler` — First-order explicit Euler scheme.
- `implicit_euler` — First-order implicit Euler scheme.
- `crank_nicolson` — Second-order Crank-Nicolson scheme.

## `validate_finite_difference_settings`

```cpp
Result<void> kiyosi::validate_finite_difference_settings(const FiniteDifferenceSettings &settings)
```

Validates finite-difference grid settings. 
**Parameters**

- `settings` — Settings to validate.

**Returns:** Success, or an `invalid_parameter` error.

## `kiyosi::FiniteDifferenceSettings`

```cpp
struct kiyosi::FiniteDifferenceSettings
```

Aggregate configuration validated by finite-difference engines when price() is called.

### Members

#### `asset_step_count`

```cpp
int kiyosi::FiniteDifferenceSettings::asset_step_count
```

Number of spatial grid steps; must be at least three.

#### `time_step_count`

```cpp
int kiyosi::FiniteDifferenceSettings::time_step_count
```

Number of time steps; must be positive.

#### `scheme`

```cpp
FiniteDifferenceScheme kiyosi::FiniteDifferenceSettings::scheme
```

Time-marching scheme.

#### `asset_upper_boundary`

```cpp
std::optional<double> kiyosi::FiniteDifferenceSettings::asset_upper_boundary
```

Positive upper spot boundary, or automatic when absent.
