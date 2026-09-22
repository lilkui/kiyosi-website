---
description: C++ API declarations from kiyosi/instruments/structured/autocallable.hpp.
outline: [2, 4]
---

# `<kiyosi/instruments/structured/autocallable.hpp>`

```cpp
#include <kiyosi/instruments/structured/autocallable.hpp>
```

## `KnockInObservationMode`

```cpp
enum class KnockInObservationMode
```

Monitoring frequency for an autocallable knock-in barrier.

**Values**

- `every_trading_day` — Observe on every trading day in the contract life.
- `at_expiry` — Observe only at expiry.

## `AutocallableBarrierState`

```cpp
enum class AutocallableBarrierState
```

Barrier events known before valuation.

**Values**

- `none` — No barrier event has occurred.
- `knocked_out` — The note has already knocked out.
- `knocked_in` — The downside barrier has already been breached.

## `validate_autocallable_note`

```cpp
template <typename Note>
Result< void > kiyosi::validate_autocallable_note(const Note &note)
```

Authoritative domain validation for every autocallable product; optional features are detected structurally so each product only pays for the checks it needs. 
**Template parameters**

- `` — Autocallable note exposing the required term accessors.

**Returns:** Success, or an `invalid_parameter` or `invalid_schedule` error.

## `kiyosi::AutocallableNote`

```cpp
class kiyosi::AutocallableNote
```

Principal, knock-out ladder, and settlement strikes shared by every autocallable structure.

### Members

#### `initial_spot`

```cpp
double kiyosi::AutocallableNote::initial_spot() const noexcept
```

Returns the reference spot used to normalize contract levels.

#### `knock_out_levels`

```cpp
const std::vector< double > & kiyosi::AutocallableNote::knock_out_levels() const noexcept
```

Returns one positive knock-out level per observation date.

#### `upper_strike`

```cpp
double kiyosi::AutocallableNote::upper_strike() const noexcept
```

Returns the upper settlement strike.

#### `lower_strike`

```cpp
double kiyosi::AutocallableNote::lower_strike() const noexcept
```

Returns the lower settlement strike.

#### `observation_dates`

```cpp
const std::vector< Date > & kiyosi::AutocallableNote::observation_dates() const noexcept
```

Returns the strictly ordered knock-out observation dates.

#### `principal_ratio`

```cpp
double kiyosi::AutocallableNote::principal_ratio() const noexcept
```

Returns the non-negative principal multiplier.

#### `effective_date`

```cpp
Date kiyosi::AutocallableNote::effective_date() const noexcept
```

Returns the first date of the note life.

#### `expiry_date`

```cpp
Date kiyosi::AutocallableNote::expiry_date() const noexcept
```

Returns the final date of the note life.

#### `barrier_state`

```cpp
AutocallableBarrierState kiyosi::AutocallableNote::barrier_state() const noexcept
```

Returns barrier events known before valuation.

## `kiyosi::KnockInAutocallableNote`

```cpp
class kiyosi::KnockInAutocallableNote
```

An autocallable note carrying a downside knock-in barrier.

### Members

#### `initial_spot`

```cpp
double kiyosi::KnockInAutocallableNote::initial_spot() const noexcept
```

Returns the reference spot used to normalize contract levels.

#### `knock_out_levels`

```cpp
const std::vector< double > & kiyosi::KnockInAutocallableNote::knock_out_levels() const noexcept
```

Returns one positive knock-out level per observation date.

#### `upper_strike`

```cpp
double kiyosi::KnockInAutocallableNote::upper_strike() const noexcept
```

Returns the upper settlement strike.

#### `lower_strike`

```cpp
double kiyosi::KnockInAutocallableNote::lower_strike() const noexcept
```

Returns the lower settlement strike.

#### `observation_dates`

```cpp
const std::vector< Date > & kiyosi::KnockInAutocallableNote::observation_dates() const noexcept
```

Returns the strictly ordered knock-out observation dates.

#### `principal_ratio`

```cpp
double kiyosi::KnockInAutocallableNote::principal_ratio() const noexcept
```

Returns the non-negative principal multiplier.

#### `effective_date`

```cpp
Date kiyosi::KnockInAutocallableNote::effective_date() const noexcept
```

Returns the first date of the note life.

#### `expiry_date`

```cpp
Date kiyosi::KnockInAutocallableNote::expiry_date() const noexcept
```

Returns the final date of the note life.

#### `barrier_state`

```cpp
AutocallableBarrierState kiyosi::KnockInAutocallableNote::barrier_state() const noexcept
```

Returns barrier events known before valuation.

#### `knock_in_level`

```cpp
double kiyosi::KnockInAutocallableNote::knock_in_level() const noexcept
```

Returns the positive downside knock-in level.

#### `knock_in_observation_mode`

```cpp
KnockInObservationMode kiyosi::KnockInAutocallableNote::knock_in_observation_mode() const noexcept
```

Returns the knock-in monitoring frequency.
