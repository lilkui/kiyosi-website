---
description: C++ API declarations from kiyosi/core/day_count.hpp.
outline: [2, 4]
---

# `<kiyosi/core/day_count.hpp>`

```cpp
#include <kiyosi/core/day_count.hpp>
```

## `DayCountConvention`

```cpp
enum class DayCountConvention
```

Supported day-count conventions.

**Values**

- `actual_365_fixed` — Actual elapsed time divided by 365 days.

## `year_fraction`

```cpp
KIYOSI_EXPORT Result< double > kiyosi::year_fraction(Date start, Date end, DayCountConvention convention=DayCountConvention::actual_365_fixed)
```

Computes the year fraction between two dates. 
**Parameters**

- `` — Inclusive start date.
- `` — End date, which must not precede `start`.
- `` — Day-count convention to apply.

**Returns:** Year fraction, or an `invalid_date`, `invalid_time_range`, or `invalid_parameter` error.

## `year_fraction`

```cpp
KIYOSI_EXPORT Result< double > kiyosi::year_fraction(Timestamp start, Timestamp end, DayCountConvention convention=DayCountConvention::actual_365_fixed)
```

Computes the year fraction between two timestamps. 
**Parameters**

- `` — Start timestamp.
- `` — End timestamp, which must not precede `start`.
- `` — Day-count convention to apply.

**Returns:** Year fraction, or an `invalid_date`, `invalid_time_range`, or `invalid_parameter` error.
