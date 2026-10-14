---
description: kiyosi/pricing/engines/autocallable/finite_difference.hpp 中的 C++ API 声明。
outline: [2, 4]
---

# `<kiyosi/pricing/engines/autocallable/finite_difference.hpp>`

```cpp
#include <kiyosi/pricing/engines/autocallable/finite_difference.hpp>
```

## `kiyosi::FiniteDifferenceAutocallableEngine`

```cpp
class kiyosi::FiniteDifferenceAutocallableEngine
```

One- or two-layer backward induction, depending on whether the note has knock-in state, with knock-out and coupon events anchored onto the time grid. Accepts 3..2,000 asset steps and 1..2,000 time steps.

### 成员

#### `FiniteDifferenceAutocallableEngine`

```cpp
kiyosi::FiniteDifferenceAutocallableEngine::FiniteDifferenceAutocallableEngine(FiniteDifferenceSettings settings={})
```

Creates an engine with aggregate finite-difference settings.

#### `FiniteDifferenceAutocallableEngine`

```cpp
kiyosi::FiniteDifferenceAutocallableEngine::FiniteDifferenceAutocallableEngine(int asset_step_count, int time_step_count, FiniteDifferenceScheme scheme=FiniteDifferenceSettings{}.scheme)
```

Creates an engine with explicit grid dimensions and scheme.

#### `price`

```cpp
template <AutocallableProduct Note>
Result<double> kiyosi::FiniteDifferenceAutocallableEngine::price(const Note &note, const PricingContext &context) const
```

Prices an autocallable note by finite differences.
**返回值:** Price, or a contract, context, or settings error.

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
