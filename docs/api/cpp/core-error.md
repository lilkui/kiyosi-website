---
description: C++ API declarations from kiyosi/core/error.hpp.
outline: [2, 4]
---

# `<kiyosi/core/error.hpp>`

```cpp
#include <kiyosi/core/error.hpp>
```

## `ErrorCategory`

```cpp
enum class ErrorCategory
```

Stable categories for errors returned by the public API.

**Values**

- `invalid_option= 1` — An option type or combination is unsupported.
- `invalid_strike= 2` — A strike is non-finite or outside its valid range.
- `invalid_volatility= 3` — A volatility is non-finite or non-positive.
- `invalid_risk_free_rate= 4` — A risk-free rate is non-finite.
- `invalid_dividend_yield= 5` — A dividend yield is non-finite.
- `invalid_spot_price= 6` — A spot price is non-finite or non-positive.
- `invalid_date= 7` — A date is unsupported or invalid for the operation.
- `invalid_time_range= 8` — A time range is reversed or outside an instrument life.
- `invalid_result= 9` — A requested pricing result is unavailable or invalid.
- `invalid_schedule= 10` — Schedule dates or counts violate contract rules.
- `invalid_calendar= 11` — A trading-calendar definition is invalid.
- `invalid_parameter= 12` — Another numeric or enum parameter is invalid.
- `unbracketed_volatility= 13` — Volatility bounds do not bracket the observed price.
- `solver_non_convergence= 14` — A numerical solver exhausted its iterations.
- `solver_non_finite= 15` — A numerical solver encountered a non-finite value.
- `unbracketed_coupon= 16` — Coupon bounds do not bracket the observed price.
- `backend_unavailable= 17` — The requested pricing backend is not available.
- `backend_failure= 18` — The selected backend failed during pricing.
- `unsupported_operation= 19` — The operation is not supported for the supplied inputs.

## `Result`

```cpp
template <typename T>
using kiyosi::Result = std::expected<T, Error>
```

`Result` of a public operation, containing either `T` or an `Error`.

## `kiyosi::Error`

```cpp
struct kiyosi::Error
```

Describes a failed domain or operational result.

### Members

#### `category`

```cpp
ErrorCategory kiyosi::Error::category
```

Stable machine-readable failure category.

#### `message`

```cpp
std::string kiyosi::Error::message
```

Human-readable diagnostic; callers must not parse it.
