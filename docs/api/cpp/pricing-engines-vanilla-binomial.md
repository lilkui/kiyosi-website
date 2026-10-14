---
description: C++ API declarations from kiyosi/pricing/engines/vanilla/binomial.hpp.
outline: [2, 4]
---

# `<kiyosi/pricing/engines/vanilla/binomial.hpp>`

```cpp
#include <kiyosi/pricing/engines/vanilla/binomial.hpp>
```

## `kiyosi::CoxRossRubinsteinVanillaEngine`

```cpp
class kiyosi::CoxRossRubinsteinVanillaEngine
```

Cox-Ross-Rubinstein binomial-tree engine for vanilla European and American options. Value is tree-derived; delta and gamma are numerical tree estimates; higher Greeks use numerical differences. Before expiry, volatility must be at least abs(r - q) * sqrt(T / step_count).

### Members

#### `CoxRossRubinsteinVanillaEngine`

```cpp
kiyosi::CoxRossRubinsteinVanillaEngine::CoxRossRubinsteinVanillaEngine(BinomialSettings settings={})
```

Creates an engine with aggregate binomial settings.

#### `CoxRossRubinsteinVanillaEngine`

```cpp
kiyosi::CoxRossRubinsteinVanillaEngine::CoxRossRubinsteinVanillaEngine(int step_count)
```

Creates an engine with an explicit tree step count.

#### `price`

```cpp
Result<double> kiyosi::CoxRossRubinsteinVanillaEngine::price(const EuropeanOption &option, const PricingContext &context) const
```

Prices a European or American vanilla option.
**Returns:** Price, or a contract, context, or settings error.

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
