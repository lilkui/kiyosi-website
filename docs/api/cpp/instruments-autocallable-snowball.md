---
description: C++ API declarations from kiyosi/instruments/autocallable/snowball.hpp.
outline: [2, 4]
---

# `<kiyosi/instruments/autocallable/snowball.hpp>`

```cpp
#include <kiyosi/instruments/autocallable/snowball.hpp>
```

## `make_snowball_option`

```cpp
Result<SnowballOption> kiyosi::make_snowball_option(SnowballTerms terms)
```

Creates a validated Snowball product, owning its supplied terms.
**Returns:** The option, or an input-validation error with a stable category.

## `make_ternary_snowball_option`

```cpp
Result<TernarySnowballOption> kiyosi::make_ternary_snowball_option(TernarySnowballTerms terms)
```

Creates a validated TernarySnowball product, owning its supplied terms.
**Returns:** The option, or an input-validation error with a stable category.

## `make_binary_snowball_option`

```cpp
Result<BinarySnowballOption> kiyosi::make_binary_snowball_option(BinarySnowballTerms terms)
```

Creates a validated BinarySnowball product, owning its supplied terms.
**Returns:** The option, or an input-validation error with a stable category.

## `kiyosi::BinarySnowballTerms`

```cpp
struct kiyosi::BinarySnowballTerms
```

Input terms used to construct a `BinarySnowballOption`.

### Members

#### `maturity_coupon_rate`

```cpp
double kiyosi::BinarySnowballTerms::maturity_coupon_rate
```

Finite flat maturity coupon.

#### `barrier_state`

```cpp
std::optional<AutocallableBarrierState> kiyosi::BinarySnowballTerms::barrier_state
```

Prior barrier state; required after monitoring begins.

#### `principal_ratio`

```cpp
double kiyosi::BinarySnowballTerms::principal_ratio
```

Normalized principal repayment component.

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

#### `observations`

```cpp
std::vector<AutocallableObservation> kiyosi::BinarySnowballTerms::observations
```

Complete contractual observations, with each date and its terms associated.

## `kiyosi::SnowballTerms`

```cpp
struct kiyosi::SnowballTerms
```

Input terms used to construct a `SnowballOption`.

### Members

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

#### `knock_in_observation_mode`

```cpp
KnockInObservationMode kiyosi::SnowballTerms::knock_in_observation_mode
```

Knock-in monitoring frequency.

#### `barrier_state`

```cpp
std::optional<AutocallableBarrierState> kiyosi::SnowballTerms::barrier_state
```

Prior barrier state; required after monitoring begins.

#### `principal_ratio`

```cpp
double kiyosi::SnowballTerms::principal_ratio
```

Normalized principal repayment component.

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

#### `observations`

```cpp
std::vector<AutocallableObservation> kiyosi::SnowballTerms::observations
```

Complete contractual observations, with each date and its terms associated.

## `kiyosi::TernarySnowballTerms`

```cpp
struct kiyosi::TernarySnowballTerms
```

Input terms used to construct a `TernarySnowballOption`.

### Members

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

#### `knock_in_level`

```cpp
double kiyosi::TernarySnowballTerms::knock_in_level
```

Positive downside knock-in level.

#### `knock_in_observation_mode`

```cpp
KnockInObservationMode kiyosi::TernarySnowballTerms::knock_in_observation_mode
```

Knock-in monitoring frequency.

#### `barrier_state`

```cpp
std::optional<AutocallableBarrierState> kiyosi::TernarySnowballTerms::barrier_state
```

Prior barrier state; required after monitoring begins.

#### `principal_ratio`

```cpp
double kiyosi::TernarySnowballTerms::principal_ratio
```

Normalized principal repayment component.

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

#### `observations`

```cpp
std::vector<AutocallableObservation> kiyosi::TernarySnowballTerms::observations
```

Complete contractual observations, with each date and its terms associated.
