---
description: C++ API declarations from kiyosi/market/schedule_builders.hpp.
outline: [2, 4]
---

# `<kiyosi/market/schedule_builders.hpp>`

```cpp
#include <kiyosi/market/schedule_builders.hpp>
```

## `make_fixed_interval_schedule`

```cpp
Result< ObservationSchedule > kiyosi::make_fixed_interval_schedule(Date start, Date end, std::chrono::days interval, const TradingCalendar &calendar=weekdays_calendar())
```

Builds candidates at `start + n * interval` for positive `n`; `start` is excluded and `end` is an inclusive upper bound. Each candidate moves forward to the next trading day, duplicate adjusted dates are removed, and generation stops rather than crossing `end`. Consequently, `end` is not guaranteed to be an observation `Date`. For example, the weekdays calendar maps a daily schedule from 2025-01-03 through 2025-01-07 to [2025-01-06, 2025-01-07]. Supply explicit observation dates to an instrument factory when the contract requires a bespoke terminal `Date`. 
**Returns:** The validated schedule, or an `invalid_schedule` or `invalid_date` error.

## `make_monthly_schedule`

```cpp
Result< ObservationSchedule > kiyosi::make_monthly_schedule(Date start, Date end, int lock_up_months, const TradingCalendar &calendar=weekdays_calendar())
```

Builds monthly candidates beginning at `start + lock_up_months`; `start` is excluded and `end` is an inclusive upper bound. The start day is clamped to each target month's last day, then each candidate moves forward to the next trading day. Generation stops rather than crossing `end`, so `end` is not guaranteed to be an observation `Date`. For example, the weekdays calendar maps 2025-01-01 through 2025-03-01 with one lock-up month to [2025-02-03]; the Saturday end candidate would adjust past the bound. Supply explicit observation dates to an instrument factory when the contract requires a bespoke terminal `Date`. 
**Returns:** The validated schedule, or an `invalid_schedule` or `invalid_date` error.
