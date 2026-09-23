---
description: C++ API declarations from kiyosi/instruments/barrier/binary.hpp.
outline: [2, 4]
---

# `<kiyosi/instruments/barrier/binary.hpp>`

```cpp
#include <kiyosi/instruments/barrier/binary.hpp>
```

## `make_cash_binary_barrier_option`

```cpp
Result<BinaryBarrierOption> kiyosi::make_cash_binary_barrier_option(BinaryBarrierTerms terms, double payout)
```

Creates a validated cash-paying binary barrier option. 
**Parameters**

- `terms` — Strike, life, and barrier terms.
- `payout` — Positive finite cash payout.

**Returns:** The option, or an input-validation error.

## `make_asset_binary_barrier_option`

```cpp
Result<BinaryBarrierOption> kiyosi::make_asset_binary_barrier_option(BinaryBarrierTerms terms)
```

Creates a validated asset-paying binary barrier option. 
**Returns:** The option, or an input-validation error.

## `make_cash_one_touch_up`

```cpp
Result<TouchOption> kiyosi::make_cash_one_touch_up(Date effective_date, Date expiry_date, double barrier_level, double payout, kiyosi::SettlementTiming settlement_timing=kiyosi::SettlementTiming::at_expiry, kiyosi::ObservationMode observation_mode=kiyosi::ObservationMode::continuous, std::vector<Date> observation_dates={})
```

Creates an up one-touch option with a fixed cash payout. 
**Returns:** The option, or an input-validation error.

## `make_cash_one_touch_down`

```cpp
Result<TouchOption> kiyosi::make_cash_one_touch_down(Date effective_date, Date expiry_date, double barrier_level, double payout, kiyosi::SettlementTiming settlement_timing=kiyosi::SettlementTiming::at_expiry, kiyosi::ObservationMode observation_mode=kiyosi::ObservationMode::continuous, std::vector<Date> observation_dates={})
```

Creates a down one-touch option with a fixed cash payout. 
**Returns:** The option, or an input-validation error.

## `make_cash_no_touch_up`

```cpp
Result<TouchOption> kiyosi::make_cash_no_touch_up(Date effective_date, Date expiry_date, double barrier_level, double payout, kiyosi::ObservationMode observation_mode=kiyosi::ObservationMode::continuous, std::vector<Date> observation_dates={})
```

Creates an up no-touch option with a fixed cash payout at expiry. 
**Returns:** The option, or an input-validation error.

## `make_cash_no_touch_down`

```cpp
Result<TouchOption> kiyosi::make_cash_no_touch_down(Date effective_date, Date expiry_date, double barrier_level, double payout, kiyosi::ObservationMode observation_mode=kiyosi::ObservationMode::continuous, std::vector<Date> observation_dates={})
```

Creates a down no-touch option with a fixed cash payout at expiry. 
**Returns:** The option, or an input-validation error.

## `make_asset_one_touch_up`

```cpp
Result<TouchOption> kiyosi::make_asset_one_touch_up(Date effective_date, Date expiry_date, double barrier_level, kiyosi::SettlementTiming settlement_timing=kiyosi::SettlementTiming::at_expiry, kiyosi::ObservationMode observation_mode=kiyosi::ObservationMode::continuous, std::vector<Date> observation_dates={})
```

Creates an up one-touch option paying the underlying asset. 
**Returns:** The option, or an input-validation error.

## `make_asset_one_touch_down`

```cpp
Result<TouchOption> kiyosi::make_asset_one_touch_down(Date effective_date, Date expiry_date, double barrier_level, kiyosi::SettlementTiming settlement_timing=kiyosi::SettlementTiming::at_expiry, kiyosi::ObservationMode observation_mode=kiyosi::ObservationMode::continuous, std::vector<Date> observation_dates={})
```

Creates a down one-touch option paying the underlying asset. 
**Returns:** The option, or an input-validation error.

## `make_asset_no_touch_up`

```cpp
Result<TouchOption> kiyosi::make_asset_no_touch_up(Date effective_date, Date expiry_date, double barrier_level, kiyosi::ObservationMode observation_mode=kiyosi::ObservationMode::continuous, std::vector<Date> observation_dates={})
```

Creates an up no-touch option paying the underlying asset at expiry. 
**Returns:** The option, or an input-validation error.

## `make_asset_no_touch_down`

```cpp
Result<TouchOption> kiyosi::make_asset_no_touch_down(Date effective_date, Date expiry_date, double barrier_level, kiyosi::ObservationMode observation_mode=kiyosi::ObservationMode::continuous, std::vector<Date> observation_dates={})
```

Creates a down no-touch option paying the underlying asset at expiry. 
**Returns:** The option, or an input-validation error.

## `kiyosi::BinaryBarrierOption`

```cpp
class kiyosi::BinaryBarrierOption
```

Strike-based binary option whose payoff also depends on a barrier_level event.

### Members

#### `option_type`

```cpp
OptionType kiyosi::BinaryBarrierOption::option_type() const noexcept
```

Returns the call-or-put direction.

#### `strike`

```cpp
double kiyosi::BinaryBarrierOption::strike() const noexcept
```

Returns the positive strike price.

#### `payoff`

```cpp
const BinaryPayoff & kiyosi::BinaryBarrierOption::payoff() const noexcept
```

Returns the cash-or-asset payoff.

#### `payoff_type`

```cpp
PayoffType kiyosi::BinaryBarrierOption::payoff_type() const noexcept
```

Returns the payoff denomination.

#### `barrier_terms`

```cpp
const BarrierTerms & kiyosi::BinaryBarrierOption::barrier_terms() const noexcept
```

Returns the validated barrier terms.

#### `barrier_level`

```cpp
double kiyosi::BinaryBarrierOption::barrier_level() const noexcept
```

Returns the positive barrier level.

#### `barrier_type`

```cpp
BarrierType kiyosi::BinaryBarrierOption::barrier_type() const noexcept
```

Returns the barrier direction and activation behavior.

#### `observation_mode`

```cpp
kiyosi::ObservationMode kiyosi::BinaryBarrierOption::observation_mode() const noexcept
```

Returns the monitoring frequency.

#### `observation_schedule`

```cpp
const ObservationSchedule & kiyosi::BinaryBarrierOption::observation_schedule() const noexcept
```

Returns the validated observation schedule.

#### `observation_dates`

```cpp
const std::vector<Date> & kiyosi::BinaryBarrierOption::observation_dates() const noexcept
```

Returns the ordered observation dates.

#### `mean_observation_year_fraction`

```cpp
double kiyosi::BinaryBarrierOption::mean_observation_year_fraction() const noexcept
```

Returns the average spacing between scheduled observations in years.

#### `effective_date`

```cpp
Date kiyosi::BinaryBarrierOption::effective_date() const noexcept
```

Returns the first date of the contract life.

#### `expiry_date`

```cpp
Date kiyosi::BinaryBarrierOption::expiry_date() const noexcept
```

Returns the final date of the contract life.

## `kiyosi::BinaryBarrierTerms`

```cpp
struct kiyosi::BinaryBarrierTerms
```

Input terms shared by cash and asset binary barrier options.

### Members

#### `option_type`

```cpp
OptionType kiyosi::BinaryBarrierTerms::option_type
```

Call-or-put direction.

#### `strike`

```cpp
double kiyosi::BinaryBarrierTerms::strike
```

Positive binary strike.

#### `effective_date`

```cpp
Date kiyosi::BinaryBarrierTerms::effective_date
```

First date of the contract life.

#### `expiry_date`

```cpp
Date kiyosi::BinaryBarrierTerms::expiry_date
```

Final date of the contract life.

#### `barrier_level`

```cpp
double kiyosi::BinaryBarrierTerms::barrier_level
```

Positive barrier trigger level.

#### `barrier_type`

```cpp
BarrierType kiyosi::BinaryBarrierTerms::barrier_type
```

Barrier direction and activation behavior.

#### `observation_mode`

```cpp
kiyosi::ObservationMode kiyosi::BinaryBarrierTerms::observation_mode
```

Monitoring frequency.

#### `observation_dates`

```cpp
std::vector<Date> kiyosi::BinaryBarrierTerms::observation_dates
```

Ordered dates for scheduled monitoring.

## `kiyosi::TouchOption`

```cpp
class kiyosi::TouchOption
```

Strike-free one-touch or no-touch contract paying cash or the asset.

### Members

#### `payoff`

```cpp
const BinaryPayoff & kiyosi::TouchOption::payoff() const noexcept
```

Returns the cash-or-asset payoff.

#### `payoff_type`

```cpp
PayoffType kiyosi::TouchOption::payoff_type() const noexcept
```

Returns the payoff denomination.

#### `settlement_timing`

```cpp
kiyosi::SettlementTiming kiyosi::TouchOption::settlement_timing() const noexcept
```

Returns when the payoff settles.

#### `barrier_terms`

```cpp
const BarrierTerms & kiyosi::TouchOption::barrier_terms() const noexcept
```

Returns the validated barrier terms.

#### `barrier_level`

```cpp
double kiyosi::TouchOption::barrier_level() const noexcept
```

Returns the positive barrier level.

#### `is_one_touch`

```cpp
bool kiyosi::TouchOption::is_one_touch() const noexcept
```

Returns whether this contract pays when the barrier is touched.

#### `is_up`

```cpp
bool kiyosi::TouchOption::is_up() const noexcept
```

Returns whether this is an upward barrier.

#### `observation_mode`

```cpp
kiyosi::ObservationMode kiyosi::TouchOption::observation_mode() const noexcept
```

Returns the monitoring frequency.

#### `observation_schedule`

```cpp
const ObservationSchedule & kiyosi::TouchOption::observation_schedule() const noexcept
```

Returns the validated observation schedule.

#### `observation_dates`

```cpp
const std::vector<Date> & kiyosi::TouchOption::observation_dates() const noexcept
```

Returns the ordered observation dates.

#### `mean_observation_year_fraction`

```cpp
double kiyosi::TouchOption::mean_observation_year_fraction() const noexcept
```

Returns the average spacing between scheduled observations in years.

#### `effective_date`

```cpp
Date kiyosi::TouchOption::effective_date() const noexcept
```

Returns the first date of the contract life.

#### `expiry_date`

```cpp
Date kiyosi::TouchOption::expiry_date() const noexcept
```

Returns the final date of the contract life.
