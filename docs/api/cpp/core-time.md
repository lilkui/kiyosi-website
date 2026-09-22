---
description: C++ API declarations from kiyosi/core/time.hpp.
outline: [2, 4]
---

# `<kiyosi/core/time.hpp>`

```cpp
#include <kiyosi/core/time.hpp>
```

## `Date`

```cpp
using kiyosi::Date = std::chrono::sys_days
```

Civil date represented as a day on the system clock timeline.

## `Timestamp`

```cpp
using kiyosi::Timestamp = std::chrono::sys_time<std::chrono::nanoseconds>
```

UTC-like instant with nanosecond precision; date-only contracts are midnight anchored.

## `is_supported_date`

```cpp
KIYOSI_EXPORT bool kiyosi::is_supported_date(Date value) noexcept
```

Tests whether a date is representable by `std::chrono::year`. 
**Parameters**

- `` — `Date` to test.

**Returns:** `true` when `value` is in the supported inclusive civil-date range.

## `start_of_day`

```cpp
Timestamp kiyosi::start_of_day(Date value) noexcept
```

Converts a date to its midnight timestamp. 
**Parameters**

- `` — `Date` to convert.

**Returns:** `Timestamp` at the start of `value`.

## `date_of`

```cpp
Date kiyosi::date_of(Timestamp value) noexcept
```

Extracts the civil date containing a timestamp. 
**Parameters**

- `` — `Timestamp` to convert.

**Returns:** `Date` obtained by flooring `value` to whole days.

## `validate_valuation_not_after_expiry`

```cpp
KIYOSI_EXPORT Result< void > kiyosi::validate_valuation_not_after_expiry(Date valuation_date, Date expiry_date)
```

Validates that a date valuation does not follow an expiry date. 
**Returns:** Success, or an `invalid_date` or `invalid_time_range` error.

## `validate_valuation_not_after_expiry`

```cpp
KIYOSI_EXPORT Result< void > kiyosi::validate_valuation_not_after_expiry(Timestamp valuation_time, Date expiry_date)
```

Validates that a timestamp valuation does not follow the end of an expiry date. 
**Returns:** Success, or an `invalid_date` or `invalid_time_range` error.

## `validate_valuation_within_instrument_life`

```cpp
Result< void > kiyosi::validate_valuation_within_instrument_life(Date valuation_date, Date effective_date, Date expiry_date)
```

Validates that a valuation date lies within an instrument's inclusive life. 
**Returns:** Success, or an `invalid_date` or `invalid_time_range` error.

## `validate_valuation_within_instrument_life`

```cpp
Result< void > kiyosi::validate_valuation_within_instrument_life(Timestamp valuation_time, Date effective_date, Date expiry_date)
```

Validates that a valuation timestamp lies within an instrument's inclusive life. 
**Returns:** Success, or an `invalid_date` or `invalid_time_range` error.
