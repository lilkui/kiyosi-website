---
description: kiyosi/pricing/settings/implied.hpp 中的 C++ API 声明。
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

**枚举值**

- `shift_maturity_coupon` — Shift the maturity coupon with the quoted knock-out coupon.
- `preserve_maturity_coupon` — Keep the maturity coupon fixed while solving.

## `kiyosi::ImpliedCouponSettings`

```cpp
struct kiyosi::ImpliedCouponSettings
```

Bracketing bounds and convergence controls for the implied-coupon solver. Stops when either the price error or the parameter interval meets its own tolerance.

### 成员

#### `lower_bound`

```cpp
double kiyosi::ImpliedCouponSettings::lower_bound
```

Finite lower coupon bound.

#### `upper_bound`

```cpp
double kiyosi::ImpliedCouponSettings::upper_bound
```

Finite upper coupon bound, greater than the lower bound.

#### `price_tolerance`

```cpp
double kiyosi::ImpliedCouponSettings::price_tolerance
```

Positive absolute price-error tolerance.

#### `parameter_tolerance`

```cpp
double kiyosi::ImpliedCouponSettings::parameter_tolerance
```

Positive absolute coupon-interval tolerance.

#### `max_iterations`

```cpp
int kiyosi::ImpliedCouponSettings::max_iterations
```

Positive maximum bisection iteration count.

## `kiyosi::ImpliedVolatilitySettings`

```cpp
struct kiyosi::ImpliedVolatilitySettings
```

Bracketing bounds and convergence controls for the implied-volatility solver. Stops when either the price error or the parameter interval meets its own tolerance.

### 成员

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

#### `price_tolerance`

```cpp
double kiyosi::ImpliedVolatilitySettings::price_tolerance
```

Positive absolute price-error tolerance.

#### `parameter_tolerance`

```cpp
double kiyosi::ImpliedVolatilitySettings::parameter_tolerance
```

Positive absolute volatility-interval tolerance.

#### `max_iterations`

```cpp
int kiyosi::ImpliedVolatilitySettings::max_iterations
```

Positive maximum Brent iteration count, excluding endpoint prices.
