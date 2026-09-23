---
description: C++ API declarations from kiyosi/instruments/barrier/terms.hpp.
outline: [2, 4]
---

# `<kiyosi/instruments/barrier/terms.hpp>`

```cpp
#include <kiyosi/instruments/barrier/terms.hpp>
```

## `BarrierType`

```cpp
enum class BarrierType
```

Direction and activation behavior of a barrier.

**Values**

- `up_and_in` — Activates when spot reaches or exceeds the barrier.
- `up_and_out` — Terminates when spot reaches or exceeds the barrier.
- `down_and_in` — Activates when spot reaches or falls below the barrier.
- `down_and_out` — Terminates when spot reaches or falls below the barrier.

## `ObservationMode`

```cpp
enum class ObservationMode
```

Barrier monitoring frequency.

**Values**

- `continuous` — Monitor continuously throughout the contract life.
- `scheduled` — Monitor only on explicit observation dates.

## `RebateTiming`

```cpp
enum class RebateTiming
```

Payment timing for a barrier-option rebate.

**Values**

- `at_hit` — Pay when the barrier is hit.
- `at_expiry` — Pay at contract expiry.

## `SettlementTiming`

```cpp
enum class SettlementTiming
```

Settlement timing for a touch option.

**Values**

- `at_hit` — Settle when the barrier is hit.
- `at_expiry` — Settle at contract expiry.

## `is_up_barrier`

```cpp
bool kiyosi::is_up_barrier(BarrierType kind) noexcept
```

Tests whether a barrier is triggered by upward spot movement. 
**Returns:** `true` for up-and-in and up-and-out barriers.

## `is_knock_in_barrier`

```cpp
bool kiyosi::is_knock_in_barrier(BarrierType kind) noexcept
```

Tests whether a barrier activates rather than terminates the contract. 
**Returns:** `true` for up-and-in and down-and-in barriers.

## `kiyosi::BarrierTerms`

```cpp
class kiyosi::BarrierTerms
```

Trigger level, knock direction, and monitoring schedule shared by every barrier contract.

### Members

#### `barrier_level`

```cpp
double kiyosi::BarrierTerms::barrier_level() const noexcept
```

Returns the positive barrier level.

#### `barrier_type`

```cpp
BarrierType kiyosi::BarrierTerms::barrier_type() const noexcept
```

Returns the barrier direction and activation behavior.

#### `observation_mode`

```cpp
kiyosi::ObservationMode kiyosi::BarrierTerms::observation_mode() const noexcept
```

Returns the monitoring frequency.

#### `observation_schedule`

```cpp
const ObservationSchedule & kiyosi::BarrierTerms::observation_schedule() const noexcept
```

Returns the validated monitoring schedule.

#### `observation_dates`

```cpp
const std::vector<Date> & kiyosi::BarrierTerms::observation_dates() const noexcept
```

Returns the ordered monitoring dates; empty for continuous monitoring.

#### `effective_date`

```cpp
Date kiyosi::BarrierTerms::effective_date() const noexcept
```

Returns the first date of the contract life.

#### `expiry_date`

```cpp
Date kiyosi::BarrierTerms::expiry_date() const noexcept
```

Returns the final date of the contract life.

#### `is_up`

```cpp
bool kiyosi::BarrierTerms::is_up() const noexcept
```

Returns whether this is an upward barrier.

#### `is_knock_in`

```cpp
bool kiyosi::BarrierTerms::is_knock_in() const noexcept
```

Returns whether this is a knock-in barrier.

#### `is_continuous`

```cpp
bool kiyosi::BarrierTerms::is_continuous() const noexcept
```

Returns whether monitoring is continuous.

#### `mean_observation_year_fraction`

```cpp
double kiyosi::BarrierTerms::mean_observation_year_fraction() const noexcept
```

Mean spacing between monitoring dates, used for the BGK discrete-barrier shift.

#### `is_monitored_on`

```cpp
bool kiyosi::BarrierTerms::is_monitored_on(Date date) const noexcept
```

Tests whether the barrier is monitored on a date. 
**Parameters**

- `date` — `Date` to test.

**Returns:** `true` for continuous monitoring or a scheduled observation date.

#### `is_breached_by`

```cpp
bool kiyosi::BarrierTerms::is_breached_by(double spot) const noexcept
```

Tests whether a spot lies on the triggered side of the barrier. 
**Parameters**

- `spot` — Spot value to test.

**Returns:** `true` when `spot` breaches the barrier.
