---
description: C++ API declarations from kiyosi/pricing/engines/structured/finite_difference.hpp.
outline: [2, 4]
---

# `<kiyosi/pricing/engines/structured/finite_difference.hpp>`

```cpp
#include <kiyosi/pricing/engines/structured/finite_difference.hpp>
```

## `FiniteDifferencePhoenixEngine`

```cpp
using kiyosi::FiniteDifferencePhoenixEngine = FiniteDifferenceAutocallableEngine<PhoenixOption>
```

Finite-difference engine for Phoenix options.

## `FiniteDifferenceSnowballEngine`

```cpp
using kiyosi::FiniteDifferenceSnowballEngine = FiniteDifferenceAutocallableEngine<SnowballOption>
```

Finite-difference engine for snowball options.

## `FiniteDifferenceBinarySnowballEngine`

```cpp
using kiyosi::FiniteDifferenceBinarySnowballEngine = FiniteDifferenceAutocallableEngine<BinarySnowballOption>
```

Finite-difference engine for binary snowball options.

## `FiniteDifferenceTernarySnowballEngine`

```cpp
using kiyosi::FiniteDifferenceTernarySnowballEngine = FiniteDifferenceAutocallableEngine<TernarySnowballOption>
```

Finite-difference engine for ternary snowball options.

## `price_autocallable_finite_difference`

```cpp
template <typename Note>
KIYOSI_EXPORT Result< PricingResult > kiyosi::price_autocallable_finite_difference(const Note &, const PricingContext &, FiniteDifferenceSettings)
```

Prices an autocallable note with the finite-difference implementation. 
**Returns:** Pricing measures, or a contract, context, or settings error.

## `kiyosi::FiniteDifferenceAutocallableEngine`

```cpp
template <typename Note>
class kiyosi::FiniteDifferenceAutocallableEngine
```

One- or two-layer backward induction, depending on whether the note has knock-in state, with knock-out and coupon events anchored onto the time grid.

### Members

#### `FiniteDifferenceAutocallableEngine`

```cpp
kiyosi::FiniteDifferenceAutocallableEngine< Note >::FiniteDifferenceAutocallableEngine(FiniteDifferenceSettings settings={})
```

Creates an engine with aggregate finite-difference settings.

#### `FiniteDifferenceAutocallableEngine`

```cpp
kiyosi::FiniteDifferenceAutocallableEngine< Note >::FiniteDifferenceAutocallableEngine(int asset_step_count, int time_step_count, FiniteDifferenceScheme scheme=FiniteDifferenceSettings{}.scheme)
```

Creates an engine with explicit grid dimensions and scheme.

#### `price`

```cpp
Result< PricingResult > kiyosi::FiniteDifferenceAutocallableEngine< Note >::price(const Note &note, const PricingContext &context) const
```

Prices an autocallable note by finite differences. 
**Returns:** Pricing measures, or a contract, context, or settings error.

#### `settings`

```cpp
FiniteDifferenceSettings kiyosi::FiniteDifferenceAutocallableEngine< Note >::settings() const noexcept
```

Returns the engine settings.
