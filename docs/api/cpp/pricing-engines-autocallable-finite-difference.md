---
description: kiyosi/pricing/engines/autocallable/finite_difference.hpp 中的 C++ API 声明。
outline: [2, 4]
---

# `<kiyosi/pricing/engines/autocallable/finite_difference.hpp>`

```cpp
#include <kiyosi/pricing/engines/autocallable/finite_difference.hpp>
```

## `make_finite_difference_autocallable_engine`

```cpp
Result<FiniteDifferenceAutocallableEngine> kiyosi::make_finite_difference_autocallable_engine(FiniteDifferenceSettings settings)
```

Creates an engine after validating its configuration.
**返回值:** The engine, or an `invalid_parameter` error.

## `kiyosi::FiniteDifferenceAutocallableEngine`

```cpp
class kiyosi::FiniteDifferenceAutocallableEngine
```

One- or two-layer backward induction, depending on whether the note has knock-in state, with knock-out and coupon events anchored onto the time grid. Accepts 3..2,000 asset steps and 1..2,000 time steps.

### 成员

#### `FiniteDifferenceAutocallableEngine`

```cpp
kiyosi::FiniteDifferenceAutocallableEngine::FiniteDifferenceAutocallableEngine()=default
```

Creates an engine with valid default settings.

#### `price`

```cpp
template <AutocallableProduct Note>
Result<double> kiyosi::FiniteDifferenceAutocallableEngine::price(const Note &note, const PricingContext &context) const
```

Prices an autocallable note by finite differences.
**返回值:** Price, or a contract, context, or numerical error.

#### `price_with_greeks`

```cpp
template <AutocallableProduct Note>
Result<PricingResult> kiyosi::FiniteDifferenceAutocallableEngine::price_with_greeks(const Note &option, const PricingContext &context, GreeksRequest greeks, NumericalShiftSettings settings={}) const
```

Prices with the explicitly requested Greeks; unavailable measures remain empty. Delta, gamma, and speed reuse the solved layer; vanna/zomma and charm/color difference native delta/gamma shifted in volatility and time. Other measures use numerical price differences.

#### `settings`

```cpp
FiniteDifferenceSettings kiyosi::FiniteDifferenceAutocallableEngine::settings() const noexcept
```

Returns the engine settings.
