---
description: C++ API declarations from kiyosi/instruments/structured/snowball.hpp.
outline: [2, 4]
---

# `<kiyosi/instruments/structured/snowball.hpp>`

```cpp
#include <kiyosi/instruments/structured/snowball.hpp>
```

## `make_snowball_option`

```cpp
Result<SnowballOption> kiyosi::make_snowball_option(SnowballTerms terms)
```

Creates a validated knock-in snowball. 
**Returns:** The option, or an `invalid_parameter` or `invalid_schedule` error.

## `make_ternary_snowball_option`

```cpp
Result<TernarySnowballOption> kiyosi::make_ternary_snowball_option(TernarySnowballTerms terms)
```

Creates a validated ternary snowball. 
**Returns:** The option, or an `invalid_parameter` or `invalid_schedule` error.

## `make_binary_snowball_option`

```cpp
Result<BinarySnowballOption> kiyosi::make_binary_snowball_option(BinarySnowballTerms terms)
```

Creates a validated binary snowball. 
**Returns:** The option, or an `invalid_parameter` or `invalid_schedule` error.

## `kiyosi::BinarySnowballOption`

```cpp
class kiyosi::BinarySnowballOption : kiyosi::AutocallableNote
```

Snowball variant settling a flat coupon at maturity regardless of the terminal spot.

### Members

#### `knock_out_coupon_rates`

```cpp
const std::vector<double> & kiyosi::BinarySnowballOption::knock_out_coupon_rates() const noexcept
```

Returns one finite knock-out coupon rate per observation date.

#### `maturity_coupon_rate`

```cpp
double kiyosi::BinarySnowballOption::maturity_coupon_rate() const noexcept
```

Returns the finite flat maturity coupon rate.

## `kiyosi::BinarySnowballTerms`

```cpp
struct kiyosi::BinarySnowballTerms
```

Input terms used to construct a `BinarySnowballOption`.

### Members

#### `knock_out_coupon_rates`

```cpp
std::vector<double> kiyosi::BinarySnowballTerms::knock_out_coupon_rates
```

Finite knock-out coupons by observation.

#### `maturity_coupon_rate`

```cpp
double kiyosi::BinarySnowballTerms::maturity_coupon_rate
```

Finite flat maturity coupon.

#### `initial_spot`

```cpp
double kiyosi::BinarySnowballTerms::initial_spot
```

Positive reference spot.

#### `knock_out_levels`

```cpp
std::vector<double> kiyosi::BinarySnowballTerms::knock_out_levels
```

Positive knock-out levels by observation.

#### `upper_strike`

```cpp
double kiyosi::BinarySnowballTerms::upper_strike
```

Positive upper settlement strike.

#### `lower_strike`

```cpp
double kiyosi::BinarySnowballTerms::lower_strike
```

Non-negative lower settlement strike.

#### `observation_dates`

```cpp
std::vector<Date> kiyosi::BinarySnowballTerms::observation_dates
```

Strictly ordered event dates.

#### `barrier_state`

```cpp
AutocallableBarrierState kiyosi::BinarySnowballTerms::barrier_state
```

Prior barrier state.

#### `principal_ratio`

```cpp
double kiyosi::BinarySnowballTerms::principal_ratio
```

Non-negative principal multiplier.

#### `effective_date`

```cpp
Date kiyosi::BinarySnowballTerms::effective_date
```

First date of the note life.

#### `expiry_date`

```cpp
Date kiyosi::BinarySnowballTerms::expiry_date
```

Final date of the note life.

## `kiyosi::SnowballOption`

```cpp
class kiyosi::SnowballOption : kiyosi::KnockInAutocallableNote
```

Knock-in autocallable accruing a coupon until knock-out, with downside participation.

### Members

#### `knock_out_coupon_rates`

```cpp
const std::vector<double> & kiyosi::SnowballOption::knock_out_coupon_rates() const noexcept
```

Returns one finite knock-out coupon rate per observation date.

#### `maturity_coupon_rate`

```cpp
double kiyosi::SnowballOption::maturity_coupon_rate() const noexcept
```

Returns the finite maturity coupon rate.

## `kiyosi::SnowballTerms`

```cpp
struct kiyosi::SnowballTerms
```

Input terms used to construct a `SnowballOption`.

### Members

#### `knock_out_coupon_rates`

```cpp
std::vector<double> kiyosi::SnowballTerms::knock_out_coupon_rates
```

Finite knock-out coupons by observation.

#### `maturity_coupon_rate`

```cpp
double kiyosi::SnowballTerms::maturity_coupon_rate
```

Finite coupon paid at maturity when applicable.

#### `initial_spot`

```cpp
double kiyosi::SnowballTerms::initial_spot
```

Positive reference spot.

#### `knock_in_level`

```cpp
double kiyosi::SnowballTerms::knock_in_level
```

Positive downside knock-in level.

#### `knock_out_levels`

```cpp
std::vector<double> kiyosi::SnowballTerms::knock_out_levels
```

Positive knock-out levels by observation.

#### `upper_strike`

```cpp
double kiyosi::SnowballTerms::upper_strike
```

Positive upper settlement strike.

#### `lower_strike`

```cpp
double kiyosi::SnowballTerms::lower_strike
```

Non-negative lower settlement strike.

#### `observation_dates`

```cpp
std::vector<Date> kiyosi::SnowballTerms::observation_dates
```

Strictly ordered event dates.

#### `knock_in_observation_mode`

```cpp
KnockInObservationMode kiyosi::SnowballTerms::knock_in_observation_mode
```

Knock-in monitoring frequency.

#### `barrier_state`

```cpp
AutocallableBarrierState kiyosi::SnowballTerms::barrier_state
```

Prior barrier state.

#### `principal_ratio`

```cpp
double kiyosi::SnowballTerms::principal_ratio
```

Non-negative principal multiplier.

#### `effective_date`

```cpp
Date kiyosi::SnowballTerms::effective_date
```

First date of the note life.

#### `expiry_date`

```cpp
Date kiyosi::SnowballTerms::expiry_date
```

Final date of the note life.

## `kiyosi::TernarySnowballOption`

```cpp
class kiyosi::TernarySnowballOption : kiyosi::KnockInAutocallableNote
```

Snowball variant whose maturity coupon steps down to a floor once knocked in.

### Members

#### `knock_out_coupon_rates`

```cpp
const std::vector<double> & kiyosi::TernarySnowballOption::knock_out_coupon_rates() const noexcept
```

Returns one finite knock-out coupon rate per observation date.

#### `maturity_coupon_rate`

```cpp
double kiyosi::TernarySnowballOption::maturity_coupon_rate() const noexcept
```

Returns the finite pre-adjustment maturity coupon rate.

#### `minimum_coupon_rate`

```cpp
double kiyosi::TernarySnowballOption::minimum_coupon_rate() const noexcept
```

Returns the finite maturity-coupon floor after knock-in.

## `kiyosi::TernarySnowballTerms`

```cpp
struct kiyosi::TernarySnowballTerms
```

Input terms used to construct a `TernarySnowballOption`.

### Members

#### `knock_out_coupon_rates`

```cpp
std::vector<double> kiyosi::TernarySnowballTerms::knock_out_coupon_rates
```

Finite knock-out coupons by observation.

#### `maturity_coupon_rate`

```cpp
double kiyosi::TernarySnowballTerms::maturity_coupon_rate
```

Finite coupon paid at maturity before knock-in adjustment.

#### `minimum_coupon_rate`

```cpp
double kiyosi::TernarySnowballTerms::minimum_coupon_rate
```

Finite maturity-coupon floor after knock-in.

#### `initial_spot`

```cpp
double kiyosi::TernarySnowballTerms::initial_spot
```

Positive reference spot.

#### `knock_in_level`

```cpp
double kiyosi::TernarySnowballTerms::knock_in_level
```

Positive downside knock-in level.

#### `knock_out_levels`

```cpp
std::vector<double> kiyosi::TernarySnowballTerms::knock_out_levels
```

Positive knock-out levels by observation.

#### `upper_strike`

```cpp
double kiyosi::TernarySnowballTerms::upper_strike
```

Positive upper settlement strike.

#### `lower_strike`

```cpp
double kiyosi::TernarySnowballTerms::lower_strike
```

Non-negative lower settlement strike.

#### `observation_dates`

```cpp
std::vector<Date> kiyosi::TernarySnowballTerms::observation_dates
```

Strictly ordered event dates.

#### `knock_in_observation_mode`

```cpp
KnockInObservationMode kiyosi::TernarySnowballTerms::knock_in_observation_mode
```

Knock-in monitoring frequency.

#### `barrier_state`

```cpp
AutocallableBarrierState kiyosi::TernarySnowballTerms::barrier_state
```

Prior barrier state.

#### `principal_ratio`

```cpp
double kiyosi::TernarySnowballTerms::principal_ratio
```

Non-negative principal multiplier.

#### `effective_date`

```cpp
Date kiyosi::TernarySnowballTerms::effective_date
```

First date of the note life.

#### `expiry_date`

```cpp
Date kiyosi::TernarySnowballTerms::expiry_date
```

Final date of the note life.
