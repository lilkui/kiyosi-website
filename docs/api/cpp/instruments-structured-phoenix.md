---
description: C++ API declarations from kiyosi/instruments/structured/phoenix.hpp.
outline: [2, 4]
---

# `<kiyosi/instruments/structured/phoenix.hpp>`

```cpp
#include <kiyosi/instruments/structured/phoenix.hpp>
```

## `make_phoenix_option`

```cpp
Result< PhoenixOption > kiyosi::make_phoenix_option(PhoenixTerms terms)
```

Creates a validated Phoenix autocallable. 
**Returns:** The option, or an `invalid_parameter` or `invalid_schedule` error.

## `kiyosi::PhoenixOption`

```cpp
class kiyosi::PhoenixOption : kiyosi::KnockInAutocallableNote
```

Knock-in autocallable paying a conditional coupon whenever spot clears the coupon barrier.

### Members

#### `coupon_rate`

```cpp
double kiyosi::PhoenixOption::coupon_rate() const noexcept
```

Returns the finite conditional coupon rate.

#### `coupon_barrier_levels`

```cpp
const std::vector< double > & kiyosi::PhoenixOption::coupon_barrier_levels() const noexcept
```

Returns one non-negative coupon barrier per observation date.

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

Finite coupon rate paid at qualifying observations.

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

#### `knock_out_levels`

```cpp
std::vector<double> kiyosi::PhoenixTerms::knock_out_levels
```

Positive knock-out levels by observation.

#### `coupon_barrier_levels`

```cpp
std::vector<double> kiyosi::PhoenixTerms::coupon_barrier_levels
```

Non-negative coupon barriers by observation.

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

#### `observation_dates`

```cpp
std::vector<Date> kiyosi::PhoenixTerms::observation_dates
```

Strictly ordered event dates.

#### `knock_in_observation_mode`

```cpp
KnockInObservationMode kiyosi::PhoenixTerms::knock_in_observation_mode
```

Knock-in monitoring frequency.

#### `barrier_state`

```cpp
AutocallableBarrierState kiyosi::PhoenixTerms::barrier_state
```

Prior barrier state.

#### `principal_ratio`

```cpp
double kiyosi::PhoenixTerms::principal_ratio
```

Non-negative principal multiplier.

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
