---
description: kiyosi/pricing/engines/vanilla/finite_difference.hpp 中的 C++ API 声明。
outline: [2, 4]
---

# `<kiyosi/pricing/engines/vanilla/finite_difference.hpp>`

```cpp
#include <kiyosi/pricing/engines/vanilla/finite_difference.hpp>
```

## `kiyosi::FiniteDifferenceVanillaEngine`

```cpp
class kiyosi::FiniteDifferenceVanillaEngine
```

Uniform-grid finite-difference engine for vanilla European and American options. European upper-edge values include exact BSM time value; American edges also permit immediate exercise. Accepts 3..10,000 asset steps and 1..100,000 time steps.

### 成员

#### `FiniteDifferenceVanillaEngine`

```cpp
kiyosi::FiniteDifferenceVanillaEngine::FiniteDifferenceVanillaEngine(FiniteDifferenceSettings settings={})
```

Creates an engine with aggregate finite-difference settings.

#### `FiniteDifferenceVanillaEngine`

```cpp
kiyosi::FiniteDifferenceVanillaEngine::FiniteDifferenceVanillaEngine(int asset_step_count, int time_step_count, FiniteDifferenceScheme scheme=FiniteDifferenceSettings{}.scheme)
```

Creates an engine with explicit grid dimensions and scheme.

#### `price`

```cpp
Result<double> kiyosi::FiniteDifferenceVanillaEngine::price(const EuropeanOption &option, const PricingContext &context) const
```

Prices a European or American vanilla option.
**返回值:** Price, or a contract, context, or settings error.

#### `price`

```cpp
Result<double> kiyosi::FiniteDifferenceVanillaEngine::price(const AmericanOption &option, const PricingContext &context) const
```

#### `price_with_greeks`

```cpp
Result<PricingResult> kiyosi::FiniteDifferenceVanillaEngine::price_with_greeks(const EuropeanOption &option, const PricingContext &context, GreeksRequest greeks, NumericalShiftSettings settings={}) const
```

Prices with the explicitly requested Greeks; unavailable measures remain empty. Delta, gamma, and speed reuse the solved layer.

#### `price_with_greeks`

```cpp
Result<PricingResult> kiyosi::FiniteDifferenceVanillaEngine::price_with_greeks(const AmericanOption &option, const PricingContext &context, GreeksRequest greeks, NumericalShiftSettings settings={}) const
```

#### `settings`

```cpp
FiniteDifferenceSettings kiyosi::FiniteDifferenceVanillaEngine::settings() const noexcept
```

Returns the engine settings.
