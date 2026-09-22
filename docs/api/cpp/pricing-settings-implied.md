---
description: C++ API declarations from kiyosi/pricing/settings/implied.hpp.
outline: [2, 4]
---

# `<kiyosi/pricing/settings/implied.hpp>`

```cpp
#include <kiyosi/pricing/settings/implied.hpp>
```

## `CouponQuoteConvention`

```cpp
enum class CouponQuoteConvention
```

Determines whether a Snowball maturity coupon moves with its quoted knock-out coupon.

**Values**

- `shift_maturity_coupon` — Shift the maturity coupon with the quoted knock-out coupon.
- `preserve_maturity_coupon` — Keep the maturity coupon fixed while solving.

## `kiyosi::ImpliedCouponSettings`

```cpp
struct kiyosi::ImpliedCouponSettings
```

Bracketing bounds and convergence controls for the implied-coupon solver.

### Members

#### `lower_bound`

```cpp
double kiyosi::ImpliedCouponSettings::lower_bound
```

Non-negative lower coupon bound.

#### `upper_bound`

```cpp
double kiyosi::ImpliedCouponSettings::upper_bound
```

Upper coupon bound, greater than the lower bound.

#### `tolerance`

```cpp
double kiyosi::ImpliedCouponSettings::tolerance
```

Positive price and interval convergence tolerance.

#### `max_iterations`

```cpp
int kiyosi::ImpliedCouponSettings::max_iterations
```

Positive maximum bisection iteration count.

## `kiyosi::ImpliedVolatilitySettings`

```cpp
struct kiyosi::ImpliedVolatilitySettings
```

Bracketing bounds and convergence controls for the implied-volatility solver.

### Members

#### `lower_bound`

```cpp
double kiyosi::ImpliedVolatilitySettings::lower_bound
```

Positive lower volatility bound.

#### `upper_bound`

```cpp
double kiyosi::ImpliedVolatilitySettings::upper_bound
```

Upper volatility bound, greater than the lower bound.

#### `tolerance`

```cpp
double kiyosi::ImpliedVolatilitySettings::tolerance
```

Positive price and interval convergence tolerance.

#### `max_iterations`

```cpp
int kiyosi::ImpliedVolatilitySettings::max_iterations
```

Positive maximum bisection iteration count.
