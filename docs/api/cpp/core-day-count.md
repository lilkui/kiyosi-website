---
description: C++ API declarations from kiyosi/core/day_count.hpp.
outline: [2, 4]
---

# `<kiyosi/core/day_count.hpp>`

```cpp
#include <kiyosi/core/day_count.hpp>
```

## `year_fraction`

```cpp
Result<double> kiyosi::year_fraction(Date start, Date end)
```

Computes the Actual/365 Fixed year fraction between two dates.
**Parameters**

- `start` — Inclusive start date.
- `end` — End date, which must not precede `start`.

**Returns:** Year fraction, or an `invalid_date` or `invalid_time_range` error.

## `year_fraction`

```cpp
Result<double> kiyosi::year_fraction(Timestamp start, Timestamp end)
```

Computes the Actual/365 Fixed year fraction between two timestamps.
**Parameters**

- `start` — Start timestamp.
- `end` — End timestamp, which must not precede `start`.

**Returns:** Year fraction, or an `invalid_date` or `invalid_time_range` error.
