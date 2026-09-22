---
description: C++ API declarations from kiyosi/market/schedule.hpp.
outline: [2, 4]
---

# `<kiyosi/market/schedule.hpp>`

```cpp
#include <kiyosi/market/schedule.hpp>
```

## `validate_date_schedule`

```cpp
Result< void > kiyosi::validate_date_schedule(std::span< const Date > observation_dates, Date instrument_start, Date instrument_end)
```

Validates ordering and instrument-life bounds for a date schedule. 
**Returns:** Success, or an `invalid_date` error.

## `validate_observation_date`

```cpp
Result< void > kiyosi::validate_observation_date(Date observation_date, Date instrument_start, Date instrument_end, const TradingCalendar &calendar)
```

Validates one observation date against an instrument life and calendar. 
**Returns:** Success, or an `invalid_date` error.

## `validate_observation_dates`

```cpp
Result< void > kiyosi::validate_observation_dates(std::span< const Date > observation_dates, Date instrument_start, Date instrument_end, const TradingCalendar &calendar)
```

Validates ordering, life bounds, and trading-day status for observation dates. 
**Returns:** Success, or an `invalid_date` error.

## `kiyosi::ObservationSchedule`

```cpp
class kiyosi::ObservationSchedule
```

Immutable, strictly ordered collection of contract observation dates.

### Members

#### `dates`

```cpp
const std::vector< Date > & kiyosi::ObservationSchedule::dates() const noexcept
```

Returns the underlying ordered dates.

#### `size`

```cpp
std::size_t kiyosi::ObservationSchedule::size() const noexcept
```

Returns the number of dates.

#### `empty`

```cpp
bool kiyosi::ObservationSchedule::empty() const noexcept
```

Returns whether the schedule has no dates.

#### `operator[]`

```cpp
const Date & kiyosi::ObservationSchedule::operator[](std::size_t index) const noexcept
```

Returns the date at `index` without bounds checking.

#### `begin`

```cpp
auto kiyosi::ObservationSchedule::begin() const noexcept
```

Returns an iterator to the first date.

#### `end`

```cpp
auto kiyosi::ObservationSchedule::end() const noexcept
```

Returns the past-the-end iterator.
