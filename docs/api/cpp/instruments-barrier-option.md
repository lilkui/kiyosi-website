---
description: C++ API declarations from kiyosi/instruments/barrier/option.hpp.
outline: [2, 4]
---

# `<kiyosi/instruments/barrier/option.hpp>`

```cpp
#include <kiyosi/instruments/barrier/option.hpp>
```

## `make_barrier_option`

```cpp
Result<BarrierOption> kiyosi::make_barrier_option(BarrierOptionTerms terms)
```

Creates a validated barrier option. 
**Returns:** The option, or an input-validation error.

## `kiyosi::BarrierOption`

```cpp
class kiyosi::BarrierOption
```

Knock-in or knock-out vanilla payoff with an optional rebate.

### Members

#### `option_type`

```cpp
OptionType kiyosi::BarrierOption::option_type() const noexcept
```

Returns the call-or-put direction.

#### `strike`

```cpp
double kiyosi::BarrierOption::strike() const noexcept
```

Returns the positive strike price.

#### `rebate`

```cpp
double kiyosi::BarrierOption::rebate() const noexcept
```

Returns the non-negative rebate.

#### `rebate_timing`

```cpp
kiyosi::RebateTiming kiyosi::BarrierOption::rebate_timing() const noexcept
```

Returns when the rebate is paid.

#### `barrier_terms`

```cpp
const BarrierTerms & kiyosi::BarrierOption::barrier_terms() const noexcept
```

Returns the validated barrier terms.

#### `barrier_level`

```cpp
double kiyosi::BarrierOption::barrier_level() const noexcept
```

Returns the positive barrier level.

#### `barrier_type`

```cpp
BarrierType kiyosi::BarrierOption::barrier_type() const noexcept
```

Returns the barrier direction and activation behavior.

#### `observation_mode`

```cpp
kiyosi::ObservationMode kiyosi::BarrierOption::observation_mode() const noexcept
```

Returns the monitoring frequency.

#### `observation_schedule`

```cpp
const ObservationSchedule & kiyosi::BarrierOption::observation_schedule() const noexcept
```

Returns the validated observation schedule.

#### `observation_dates`

```cpp
const std::vector<Date> & kiyosi::BarrierOption::observation_dates() const noexcept
```

Returns the ordered observation dates.

#### `mean_observation_year_fraction`

```cpp
double kiyosi::BarrierOption::mean_observation_year_fraction() const noexcept
```

Returns the average spacing between scheduled observations in years.

#### `effective_date`

```cpp
Date kiyosi::BarrierOption::effective_date() const noexcept
```

Returns the first date of the contract life.

#### `expiry_date`

```cpp
Date kiyosi::BarrierOption::expiry_date() const noexcept
```

Returns the final date of the contract life.

## `kiyosi::BarrierOptionTerms`

```cpp
struct kiyosi::BarrierOptionTerms
```

Input terms used to construct a `BarrierOption`.

### Members

#### `option_type`

```cpp
OptionType kiyosi::BarrierOptionTerms::option_type
```

Call-or-put direction.

#### `strike`

```cpp
double kiyosi::BarrierOptionTerms::strike
```

Positive option strike.

#### `effective_date`

```cpp
Date kiyosi::BarrierOptionTerms::effective_date
```

First date of the contract life.

#### `expiry_date`

```cpp
Date kiyosi::BarrierOptionTerms::expiry_date
```

Final date of the contract life.

#### `barrier_level`

```cpp
double kiyosi::BarrierOptionTerms::barrier_level
```

Positive barrier trigger level.

#### `barrier_type`

```cpp
BarrierType kiyosi::BarrierOptionTerms::barrier_type
```

Barrier direction and activation behavior.

#### `rebate`

```cpp
double kiyosi::BarrierOptionTerms::rebate
```

Non-negative cash rebate.

#### `rebate_timing`

```cpp
kiyosi::RebateTiming kiyosi::BarrierOptionTerms::rebate_timing
```

Rebate payment timing.

#### `observation_mode`

```cpp
kiyosi::ObservationMode kiyosi::BarrierOptionTerms::observation_mode
```

Monitoring frequency.

#### `observation_dates`

```cpp
std::vector<Date> kiyosi::BarrierOptionTerms::observation_dates
```

Ordered dates for scheduled monitoring.
