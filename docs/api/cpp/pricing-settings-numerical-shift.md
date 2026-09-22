---
description: C++ API declarations from kiyosi/pricing/settings/numerical_shift.hpp.
outline: [2, 4]
---

# `<kiyosi/pricing/settings/numerical_shift.hpp>`

```cpp
#include <kiyosi/pricing/settings/numerical_shift.hpp>
```

## `kiyosi::NumericalShiftSettings`

```cpp
struct kiyosi::NumericalShiftSettings
```

Absolute bump sizes for finite-difference risk measures computed by revaluing any engine. Spot uses asset-price units, volatility and rates use decimal units, and time uses calendar days. Reported vega, vanna, zomma, and rho are still scaled per percentage point.

### Members

#### `spot_shift`

```cpp
double kiyosi::NumericalShiftSettings::spot_shift
```

Positive absolute spot bump.

#### `volatility_shift`

```cpp
double kiyosi::NumericalShiftSettings::volatility_shift
```

Positive absolute volatility bump.

#### `rate_shift`

```cpp
double kiyosi::NumericalShiftSettings::rate_shift
```

Positive absolute interest-rate bump.

#### `time_shift_days`

```cpp
int kiyosi::NumericalShiftSettings::time_shift_days
```

Positive calendar-day bump.
