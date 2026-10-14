---
description: C++ API declarations from kiyosi/instruments/autocallable/fwd.hpp.
outline: [2, 4]
---

# `<kiyosi/instruments/autocallable/fwd.hpp>`

```cpp
#include <kiyosi/instruments/autocallable/fwd.hpp>
```

## `PhoenixOption`

```cpp
using kiyosi::PhoenixOption = AutocallableNote<PhoenixTerms>
```

Knock-in note paying conditional coupons at each observation.

## `SnowballOption`

```cpp
using kiyosi::SnowballOption = AutocallableNote<SnowballTerms>
```

Knock-in note with downside participation and knock-out coupons.

## `BinarySnowballOption`

```cpp
using kiyosi::BinarySnowballOption = AutocallableNote<BinarySnowballTerms>
```

Note settling a flat maturity coupon regardless of terminal spot.

## `TernarySnowballOption`

```cpp
using kiyosi::TernarySnowballOption = AutocallableNote<TernarySnowballTerms>
```

Knock-in note whose maturity coupon steps down to a floor.

## `kiyosi::AutocallableProduct`

```cpp
template <typename Note>
concept kiyosi::AutocallableProduct
```

Complete products supported by the autocallable pricing engines.

## `kiyosi::AutocallableTerms`

```cpp
template <typename Terms>
concept kiyosi::AutocallableTerms
```
