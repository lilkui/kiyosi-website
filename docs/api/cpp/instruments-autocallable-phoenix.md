---
description: C++ API declarations from kiyosi/instruments/autocallable/phoenix.hpp.
outline: [2, 4]
---

# `<kiyosi/instruments/autocallable/phoenix.hpp>`

```cpp
#include <kiyosi/instruments/autocallable/phoenix.hpp>
```

## `make_phoenix_option`

```cpp
Result<PhoenixOption> kiyosi::make_phoenix_option(PhoenixTerms terms)
```

Creates a validated Phoenix product, owning its supplied terms.
**Returns:** The option, or an input-validation error with a stable category.

## `kiyosi::PhoenixTerms`

```cpp
struct kiyosi::PhoenixTerms
```

Input terms used to construct a `PhoenixOption`.

### Members

#### `coupon_rate`

```cpp
double kiyosi::PhoenixTerms::coupon_rate
```

Finite annualized coupon rate per observation period (ACT/365 Fixed).

#### `initial_spot`

```cpp
double kiyosi::PhoenixTerms::initial_spot
```

Positive reference spot.

#### `knock_in_level`

```cpp
double kiyosi::PhoenixTerms::knock_in_level
```

Positive downside knock-in level.

#### `upper_strike`

```cpp
double kiyosi::PhoenixTerms::upper_strike
```

Positive upper settlement strike.

#### `lower_strike`

```cpp
double kiyosi::PhoenixTerms::lower_strike
```

Non-negative lower settlement strike.

#### `knock_in_observation_mode`

```cpp
KnockInObservationMode kiyosi::PhoenixTerms::knock_in_observation_mode
```

Knock-in monitoring frequency.

#### `barrier_state`

```cpp
std::optional<AutocallableBarrierState> kiyosi::PhoenixTerms::barrier_state
```

Prior barrier state; required after monitoring begins.

#### `principal_ratio`

```cpp
double kiyosi::PhoenixTerms::principal_ratio
```

Non-negative principal component in normalized payoff units.

#### `effective_date`

```cpp
Date kiyosi::PhoenixTerms::effective_date
```

First date of the note life.

#### `expiry_date`

```cpp
Date kiyosi::PhoenixTerms::expiry_date
```

Final date of the note life.

#### `observations`

```cpp
std::vector<AutocallableObservation> kiyosi::PhoenixTerms::observations
```

Complete contractual observations, with each date and its terms associated.
