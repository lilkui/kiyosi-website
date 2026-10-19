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

## `kiyosi::BlackScholesMertonParameterChanges`

```cpp
struct kiyosi::BlackScholesMertonParameterChanges
```

Fields to replace; absent fields retain their current values.

### 成员

#### `risk_free_rate`

```cpp
std::optional<double> kiyosi::BlackScholesMertonParameterChanges::risk_free_rate
```

#### `dividend_yield`

```cpp
std::optional<double> kiyosi::BlackScholesMertonParameterChanges::dividend_yield
```

#### `volatility`

```cpp
std::optional<double> kiyosi::BlackScholesMertonParameterChanges::volatility
```

## `kiyosi::BlackScholesMertonParameters`

```cpp
class kiyosi::BlackScholesMertonParameters
```

Black-Scholes-Merton model parameters: continuously compounded rates and a flat volatility.

### 成员

#### `replace`

```cpp
Result<BlackScholesMertonParameters> kiyosi::BlackScholesMertonParameters::replace(BlackScholesMertonParameterChanges changes={}) const
```

Returns a validated owning copy with the supplied fields replaced. Uses make_bsm_parameters validation and error categories; never changes this object. Concurrent calls and reads are safe without concurrent assignment to this object.

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
