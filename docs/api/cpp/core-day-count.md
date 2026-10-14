---
description: kiyosi/core/day_count.hpp 中的 C++ API 声明。
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
**参数**

- `start` — Inclusive start date.
- `end` — End date, which must not precede `start`.

**返回值:** Year fraction, or an `invalid_date` or `invalid_time_range` error.

## `year_fraction`

```cpp
Result<double> kiyosi::year_fraction(Timestamp start, Timestamp end)
```

Computes the Actual/365 Fixed year fraction between two timestamps.
**参数**

- `start` — Start timestamp.
- `end` — End timestamp, which must not precede `start`.

**返回值:** Year fraction, or an `invalid_date` or `invalid_time_range` error.
