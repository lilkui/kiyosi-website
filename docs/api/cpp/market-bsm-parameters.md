---
description: kiyosi/market/bsm_parameters.hpp 中的 C++ API 声明。
outline: [2, 4]
---

# `<kiyosi/market/bsm_parameters.hpp>`

```cpp
#include <kiyosi/market/bsm_parameters.hpp>
```

## `make_bsm_parameters`

```cpp
Result<BlackScholesMertonParameters> kiyosi::make_bsm_parameters(double risk_free_rate, double dividend_yield, double volatility)
```

Creates validated Black-Scholes-Merton model parameters.
**返回值:** The parameters, or a rate, yield, or volatility validation error.

## `kiyosi::BlackScholesMertonParameters`

```cpp
class kiyosi::BlackScholesMertonParameters
```

Black-Scholes-Merton model parameters: continuously compounded rates and a flat volatility.

### 成员

#### `risk_free_rate`

```cpp
double kiyosi::BlackScholesMertonParameters::risk_free_rate() const noexcept
```

Returns the continuously compounded risk-free rate as a decimal.

#### `dividend_yield`

```cpp
double kiyosi::BlackScholesMertonParameters::dividend_yield() const noexcept
```

Returns the continuously compounded dividend yield as a decimal.

#### `volatility`

```cpp
double kiyosi::BlackScholesMertonParameters::volatility() const noexcept
```

Returns the positive annualized volatility as a decimal.
