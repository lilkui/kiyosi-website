---
description: kiyosi/pricing/engines/vanilla/binomial.hpp 中的 C++ API 声明。
outline: [2, 4]
---

# `<kiyosi/pricing/engines/vanilla/binomial.hpp>`

```cpp
#include <kiyosi/pricing/engines/vanilla/binomial.hpp>
```

## `make_cox_ross_rubinstein_vanilla_engine`

```cpp
Result<CoxRossRubinsteinVanillaEngine> kiyosi::make_cox_ross_rubinstein_vanilla_engine(BinomialSettings settings)
```

Creates an engine after validating its configuration.
**返回值:** The engine, or an `invalid_parameter` error.

## `kiyosi::CoxRossRubinsteinVanillaEngine`

```cpp
class kiyosi::CoxRossRubinsteinVanillaEngine
```

Cox-Ross-Rubinstein binomial-tree engine for vanilla European and American options. Value is tree-derived; delta and gamma are numerical tree estimates; higher Greeks use numerical differences. Before expiry, volatility must be at least abs(r - q) * sqrt(T / step_count).

### 成员

#### `CoxRossRubinsteinVanillaEngine`

```cpp
kiyosi::CoxRossRubinsteinVanillaEngine::CoxRossRubinsteinVanillaEngine()=default
```

Creates an engine with valid default settings.

#### `price`

```cpp
Result<double> kiyosi::CoxRossRubinsteinVanillaEngine::price(const EuropeanOption &option, const PricingContext &context) const
```

Prices a European or American vanilla option.
**返回值:** Price, or a contract, context, or numerical error.

#### `price`

```cpp
Result<double> kiyosi::CoxRossRubinsteinVanillaEngine::price(const AmericanOption &option, const PricingContext &context) const
```

#### `price_with_greeks`

```cpp
Result<PricingResult> kiyosi::CoxRossRubinsteinVanillaEngine::price_with_greeks(const EuropeanOption &option, const PricingContext &context, GreeksRequest greeks, NumericalShiftSettings settings={}) const
```

Prices with the explicitly requested Greeks; unavailable measures remain empty.

#### `price_with_greeks`

```cpp
Result<PricingResult> kiyosi::CoxRossRubinsteinVanillaEngine::price_with_greeks(const AmericanOption &option, const PricingContext &context, GreeksRequest greeks, NumericalShiftSettings settings={}) const
```

#### `settings`

```cpp
BinomialSettings kiyosi::CoxRossRubinsteinVanillaEngine::settings() const noexcept
```

Returns the engine settings.
