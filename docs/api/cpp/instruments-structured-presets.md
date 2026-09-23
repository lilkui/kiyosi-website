---
description: C++ API declarations from kiyosi/instruments/structured/presets.hpp.
outline: [2, 4]
---

# `<kiyosi/instruments/structured/presets.hpp>`

```cpp
#include <kiyosi/instruments/structured/presets.hpp>
```

## `make_standard_snowball`

```cpp
Result<SnowballOption> kiyosi::make_standard_snowball(StandardSnowballTerms terms)
```

Creates a standard snowball from named market terms. 
**Returns:** The option, or an `invalid_parameter` or `invalid_schedule` error.

## `make_step_down_snowball`

```cpp
Result<SnowballOption> kiyosi::make_step_down_snowball(StepDownSnowballTerms terms)
```

Creates a step-down snowball from named market terms. 
**Returns:** The option, or an `invalid_parameter` or `invalid_schedule` error.

## `make_both_down_snowball`

```cpp
Result<SnowballOption> kiyosi::make_both_down_snowball(BothDownSnowballTerms terms)
```

Creates a both-down snowball from named market terms. 
**Returns:** The option, or an `invalid_parameter` or `invalid_schedule` error.

## `make_dual_coupon_snowball`

```cpp
Result<SnowballOption> kiyosi::make_dual_coupon_snowball(DualCouponSnowballTerms terms)
```

Creates a dual-coupon snowball from named market terms. 
**Returns:** The option, or an `invalid_parameter` or `invalid_schedule` error.

## `make_parachute_snowball`

```cpp
Result<SnowballOption> kiyosi::make_parachute_snowball(ParachuteSnowballTerms terms)
```

Creates a parachute snowball from named market terms. 
**Returns:** The option, or an `invalid_parameter` or `invalid_schedule` error.

## `make_otm_snowball`

```cpp
Result<SnowballOption> kiyosi::make_otm_snowball(OtmSnowballTerms terms)
```

Creates an out-of-the-money snowball from named market terms. 
**Returns:** The option, or an `invalid_parameter` or `invalid_schedule` error.

## `make_loss_capped_snowball`

```cpp
Result<SnowballOption> kiyosi::make_loss_capped_snowball(LossCappedSnowballTerms terms)
```

Creates a loss-capped snowball from named market terms. 
**Returns:** The option, or an `invalid_parameter` or `invalid_schedule` error.

## `make_european_snowball`

```cpp
Result<SnowballOption> kiyosi::make_european_snowball(EuropeanSnowballTerms terms)
```

Creates a European-knock-in snowball from named market terms. 
**Returns:** The option, or an `invalid_parameter` or `invalid_schedule` error.

## `kiyosi::BothDownSnowballTerms`

```cpp
struct kiyosi::BothDownSnowballTerms
```

Terms for a snowball whose coupon and knock-out level both decrease by observation.

### Members

#### `initial_coupon_rate`

```cpp
double kiyosi::BothDownSnowballTerms::initial_coupon_rate
```

Coupon rate at the first observation.

#### `coupon_rate_decrement`

```cpp
double kiyosi::BothDownSnowballTerms::coupon_rate_decrement
```

Absolute decimal-rate decrement applied at each observation (0.01 is one percentage point).

#### `initial_spot`

```cpp
double kiyosi::BothDownSnowballTerms::initial_spot
```

Positive reference spot and upper strike.

#### `knock_in_level`

```cpp
double kiyosi::BothDownSnowballTerms::knock_in_level
```

Positive downside knock-in level.

#### `initial_knock_out_level`

```cpp
double kiyosi::BothDownSnowballTerms::initial_knock_out_level
```

First positive knock-out level.

#### `knock_out_level_decrement`

```cpp
double kiyosi::BothDownSnowballTerms::knock_out_level_decrement
```

Absolute underlying-price decrement applied at each observation.

#### `observation_dates`

```cpp
std::vector<Date> kiyosi::BothDownSnowballTerms::observation_dates
```

Strictly ordered event dates.

#### `effective_date`

```cpp
Date kiyosi::BothDownSnowballTerms::effective_date
```

First date of the note life.

#### `expiry_date`

```cpp
Date kiyosi::BothDownSnowballTerms::expiry_date
```

Final date of the note life.

#### `barrier_state`

```cpp
AutocallableBarrierState kiyosi::BothDownSnowballTerms::barrier_state
```

Prior barrier state.

#### `principal_ratio`

```cpp
double kiyosi::BothDownSnowballTerms::principal_ratio
```

Non-negative principal multiplier.

## `kiyosi::DualCouponSnowballTerms`

```cpp
struct kiyosi::DualCouponSnowballTerms
```

Terms for a snowball with distinct knock-out and maturity coupons.

### Members

#### `knock_out_coupon_rate`

```cpp
double kiyosi::DualCouponSnowballTerms::knock_out_coupon_rate
```

Coupon rate paid after knock-out.

#### `maturity_coupon_rate`

```cpp
double kiyosi::DualCouponSnowballTerms::maturity_coupon_rate
```

Coupon rate paid at maturity when applicable.

#### `initial_spot`

```cpp
double kiyosi::DualCouponSnowballTerms::initial_spot
```

Positive reference spot and upper strike.

#### `knock_in_level`

```cpp
double kiyosi::DualCouponSnowballTerms::knock_in_level
```

Positive downside knock-in level.

#### `knock_out_level`

```cpp
double kiyosi::DualCouponSnowballTerms::knock_out_level
```

Positive knock-out level used at every observation.

#### `observation_dates`

```cpp
std::vector<Date> kiyosi::DualCouponSnowballTerms::observation_dates
```

Strictly ordered event dates.

#### `effective_date`

```cpp
Date kiyosi::DualCouponSnowballTerms::effective_date
```

First date of the note life.

#### `expiry_date`

```cpp
Date kiyosi::DualCouponSnowballTerms::expiry_date
```

Final date of the note life.

#### `barrier_state`

```cpp
AutocallableBarrierState kiyosi::DualCouponSnowballTerms::barrier_state
```

Prior barrier state.

#### `principal_ratio`

```cpp
double kiyosi::DualCouponSnowballTerms::principal_ratio
```

Non-negative principal multiplier.

## `kiyosi::EuropeanSnowballTerms`

```cpp
struct kiyosi::EuropeanSnowballTerms
```

Terms for a snowball whose knock-in barrier is observed only at expiry.

### Members

#### `coupon_rate`

```cpp
double kiyosi::EuropeanSnowballTerms::coupon_rate
```

Coupon rate used at knock-out and maturity.

#### `initial_spot`

```cpp
double kiyosi::EuropeanSnowballTerms::initial_spot
```

Positive reference spot and upper strike.

#### `knock_in_level`

```cpp
double kiyosi::EuropeanSnowballTerms::knock_in_level
```

Positive downside knock-in level.

#### `knock_out_level`

```cpp
double kiyosi::EuropeanSnowballTerms::knock_out_level
```

Positive knock-out level used at every observation.

#### `observation_dates`

```cpp
std::vector<Date> kiyosi::EuropeanSnowballTerms::observation_dates
```

Strictly ordered event dates.

#### `effective_date`

```cpp
Date kiyosi::EuropeanSnowballTerms::effective_date
```

First date of the note life.

#### `expiry_date`

```cpp
Date kiyosi::EuropeanSnowballTerms::expiry_date
```

Final date of the note life.

#### `barrier_state`

```cpp
AutocallableBarrierState kiyosi::EuropeanSnowballTerms::barrier_state
```

Prior barrier state.

#### `principal_ratio`

```cpp
double kiyosi::EuropeanSnowballTerms::principal_ratio
```

Non-negative principal multiplier.

## `kiyosi::LossCappedSnowballTerms`

```cpp
struct kiyosi::LossCappedSnowballTerms
```

Terms for a snowball whose downside participation is capped by a lower strike.

### Members

#### `coupon_rate`

```cpp
double kiyosi::LossCappedSnowballTerms::coupon_rate
```

Coupon rate used at knock-out and maturity.

#### `initial_spot`

```cpp
double kiyosi::LossCappedSnowballTerms::initial_spot
```

Positive reference spot and upper strike.

#### `knock_in_level`

```cpp
double kiyosi::LossCappedSnowballTerms::knock_in_level
```

Positive downside knock-in level.

#### `knock_out_level`

```cpp
double kiyosi::LossCappedSnowballTerms::knock_out_level
```

Positive knock-out level used at every observation.

#### `lower_strike`

```cpp
double kiyosi::LossCappedSnowballTerms::lower_strike
```

Non-negative downside settlement floor.

#### `observation_dates`

```cpp
std::vector<Date> kiyosi::LossCappedSnowballTerms::observation_dates
```

Strictly ordered event dates.

#### `effective_date`

```cpp
Date kiyosi::LossCappedSnowballTerms::effective_date
```

First date of the note life.

#### `expiry_date`

```cpp
Date kiyosi::LossCappedSnowballTerms::expiry_date
```

Final date of the note life.

#### `barrier_state`

```cpp
AutocallableBarrierState kiyosi::LossCappedSnowballTerms::barrier_state
```

Prior barrier state.

#### `principal_ratio`

```cpp
double kiyosi::LossCappedSnowballTerms::principal_ratio
```

Non-negative principal multiplier.

## `kiyosi::OtmSnowballTerms`

```cpp
struct kiyosi::OtmSnowballTerms
```

Terms for a snowball with an out-of-the-money upper settlement strike.

### Members

#### `coupon_rate`

```cpp
double kiyosi::OtmSnowballTerms::coupon_rate
```

Coupon rate used at knock-out and maturity.

#### `initial_spot`

```cpp
double kiyosi::OtmSnowballTerms::initial_spot
```

Positive reference spot.

#### `knock_in_level`

```cpp
double kiyosi::OtmSnowballTerms::knock_in_level
```

Positive downside knock-in level.

#### `knock_out_level`

```cpp
double kiyosi::OtmSnowballTerms::knock_out_level
```

Positive knock-out level used at every observation.

#### `upper_strike`

```cpp
double kiyosi::OtmSnowballTerms::upper_strike
```

Positive upper settlement strike.

#### `observation_dates`

```cpp
std::vector<Date> kiyosi::OtmSnowballTerms::observation_dates
```

Strictly ordered event dates.

#### `effective_date`

```cpp
Date kiyosi::OtmSnowballTerms::effective_date
```

First date of the note life.

#### `expiry_date`

```cpp
Date kiyosi::OtmSnowballTerms::expiry_date
```

Final date of the note life.

#### `barrier_state`

```cpp
AutocallableBarrierState kiyosi::OtmSnowballTerms::barrier_state
```

Prior barrier state.

#### `principal_ratio`

```cpp
double kiyosi::OtmSnowballTerms::principal_ratio
```

Non-negative principal multiplier.

## `kiyosi::ParachuteSnowballTerms`

```cpp
struct kiyosi::ParachuteSnowballTerms
```

Terms for a snowball with a distinct final knock-out level.

### Members

#### `coupon_rate`

```cpp
double kiyosi::ParachuteSnowballTerms::coupon_rate
```

Coupon rate used at knock-out and maturity.

#### `initial_spot`

```cpp
double kiyosi::ParachuteSnowballTerms::initial_spot
```

Positive reference spot and upper strike.

#### `knock_in_level`

```cpp
double kiyosi::ParachuteSnowballTerms::knock_in_level
```

Positive downside knock-in level.

#### `knock_out_level`

```cpp
double kiyosi::ParachuteSnowballTerms::knock_out_level
```

Positive knock-out level before the final observation.

#### `final_knock_out_level`

```cpp
double kiyosi::ParachuteSnowballTerms::final_knock_out_level
```

Positive knock-out level at the final observation.

#### `observation_dates`

```cpp
std::vector<Date> kiyosi::ParachuteSnowballTerms::observation_dates
```

Strictly ordered event dates.

#### `effective_date`

```cpp
Date kiyosi::ParachuteSnowballTerms::effective_date
```

First date of the note life.

#### `expiry_date`

```cpp
Date kiyosi::ParachuteSnowballTerms::expiry_date
```

Final date of the note life.

#### `barrier_state`

```cpp
AutocallableBarrierState kiyosi::ParachuteSnowballTerms::barrier_state
```

Prior barrier state.

#### `principal_ratio`

```cpp
double kiyosi::ParachuteSnowballTerms::principal_ratio
```

Non-negative principal multiplier.

## `kiyosi::StandardSnowballTerms`

```cpp
struct kiyosi::StandardSnowballTerms
```

Terms for a constant-coupon, constant-knock-out snowball preset.

Named market conventions layered over make_snowball_option; each one only shapes the coupon and knock-out ladders before delegating to the authoritative factory.

### Members

#### `coupon_rate`

```cpp
double kiyosi::StandardSnowballTerms::coupon_rate
```

Coupon rate used at knock-out and maturity.

#### `initial_spot`

```cpp
double kiyosi::StandardSnowballTerms::initial_spot
```

Positive reference spot and upper strike.

#### `knock_in_level`

```cpp
double kiyosi::StandardSnowballTerms::knock_in_level
```

Positive downside knock-in level.

#### `knock_out_level`

```cpp
double kiyosi::StandardSnowballTerms::knock_out_level
```

Positive knock-out level used at every observation.

#### `observation_dates`

```cpp
std::vector<Date> kiyosi::StandardSnowballTerms::observation_dates
```

Strictly ordered event dates.

#### `effective_date`

```cpp
Date kiyosi::StandardSnowballTerms::effective_date
```

First date of the note life.

#### `expiry_date`

```cpp
Date kiyosi::StandardSnowballTerms::expiry_date
```

Final date of the note life.

#### `barrier_state`

```cpp
AutocallableBarrierState kiyosi::StandardSnowballTerms::barrier_state
```

Prior barrier state.

#### `principal_ratio`

```cpp
double kiyosi::StandardSnowballTerms::principal_ratio
```

Non-negative principal multiplier.

## `kiyosi::StepDownSnowballTerms`

```cpp
struct kiyosi::StepDownSnowballTerms
```

Terms for a snowball whose knock-out level decreases by observation.

### Members

#### `coupon_rate`

```cpp
double kiyosi::StepDownSnowballTerms::coupon_rate
```

Coupon rate used at knock-out and maturity.

#### `initial_spot`

```cpp
double kiyosi::StepDownSnowballTerms::initial_spot
```

Positive reference spot and upper strike.

#### `knock_in_level`

```cpp
double kiyosi::StepDownSnowballTerms::knock_in_level
```

Positive downside knock-in level.

#### `initial_knock_out_level`

```cpp
double kiyosi::StepDownSnowballTerms::initial_knock_out_level
```

First positive knock-out level.

#### `knock_out_level_decrement`

```cpp
double kiyosi::StepDownSnowballTerms::knock_out_level_decrement
```

Absolute underlying-price decrement applied at each observation.

#### `observation_dates`

```cpp
std::vector<Date> kiyosi::StepDownSnowballTerms::observation_dates
```

Strictly ordered event dates.

#### `effective_date`

```cpp
Date kiyosi::StepDownSnowballTerms::effective_date
```

First date of the note life.

#### `expiry_date`

```cpp
Date kiyosi::StepDownSnowballTerms::expiry_date
```

Final date of the note life.

#### `barrier_state`

```cpp
AutocallableBarrierState kiyosi::StepDownSnowballTerms::barrier_state
```

Prior barrier state.

#### `principal_ratio`

```cpp
double kiyosi::StepDownSnowballTerms::principal_ratio
```

Non-negative principal multiplier.
