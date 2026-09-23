---
description: C++ API declarations from kiyosi/market/calendar.hpp.
outline: [2, 4]
---

# `<kiyosi/market/calendar.hpp>`

```cpp
#include <kiyosi/market/calendar.hpp>
```

## `make_trading_calendar`

```cpp
Result<TradingCalendar> kiyosi::make_trading_calendar(TradingCalendar::TradingDayPredicate predicate, int trading_days_per_year)
```

Creates a validated trading calendar. 
**Parameters**

- `predicate` — Callable returning whether a date is a trading day.
- `trading_days_per_year` — Positive annualization basis.

**Returns:** The calendar, or an `invalid_calendar` error.

## `all_days_calendar`

```cpp
TradingCalendar kiyosi::all_days_calendar()
```

Creates a calendar in which every supported date is a trading day. 
**Returns:** Calendar with a 365-day annualization basis.

## `weekdays_calendar`

```cpp
TradingCalendar kiyosi::weekdays_calendar()
```

Holiday-unaware Monday-through-Friday calendar with a 252-day annualization basis. 
**Returns:** A weekday-only calendar.

## `kiyosi::TradingCalendar`

```cpp
class kiyosi::TradingCalendar
```

Calendar queries follow the library thread-safety default. Predicates supplied to make_trading_calendar must return the same answer for a `Date` throughout each operation; callers must not depend on query frequency or order. The caller must also ensure that the predicate and any state shared by its copies support concurrent invocation.

### Members

#### `TradingDayPredicate`

```cpp
using kiyosi::TradingCalendar::TradingDayPredicate = std::function<bool(Date)>
```

Predicate returning whether a supported date is a trading day.

#### `is_trading_day`

```cpp
bool kiyosi::TradingCalendar::is_trading_day(Date value) const
```

Tests whether a supported date is a trading day. 
**Returns:** `false` for unsupported dates or when the predicate rejects the date.

#### `trading_days_per_year`

```cpp
int kiyosi::TradingCalendar::trading_days_per_year() const noexcept
```

Returns the positive annual trading-day basis.

#### `trading_days_between`

```cpp
Result<int> kiyosi::TradingCalendar::trading_days_between(Date start, Date end) const
```

Counts trading days in the half-open interval `[start, end)`. 
**Returns:** The count, or an `invalid_date` or `invalid_time_range` error.

#### `trading_year_fraction`

```cpp
Result<double> kiyosi::TradingCalendar::trading_year_fraction(Date start, Date end) const
```

Computes a trading-day year fraction over `[start, end)`. 
**Returns:** Trading days divided by `trading_days_per_year()`, or a range error.
