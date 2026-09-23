---
description: C++ API declarations from kiyosi/instruments/exercise_based_option.hpp.
outline: [2, 4]
---

# `<kiyosi/instruments/exercise_based_option.hpp>`

```cpp
#include <kiyosi/instruments/exercise_based_option.hpp>
```

## `validate_observation_dates`

```cpp
template <OptionPayoff Payoff, OptionExercise Exercise>
Result<void> kiyosi::validate_observation_dates(std::span<const Date> observation_dates, Date valuation_date, const ExerciseBasedOption<Payoff, Exercise> &option, const TradingCalendar &calendar)
```

Validates observation dates against an option's expiry and a trading calendar. 
**Returns:** Success, or an `invalid_date` error.

## `kiyosi::ExerciseBasedOption`

```cpp
template <OptionPayoff Payoff, OptionExercise Exercise>
class kiyosi::ExerciseBasedOption
```

An option built from an independent payoff and exercise style over shared option terms. 
**Template parameters**

- `Payoff` — Copyable payoff tag satisfying `OptionPayoff`.
- `Exercise` — Copyable exercise-style tag satisfying `OptionExercise`.

### Members

#### `option_type`

```cpp
OptionType kiyosi::ExerciseBasedOption<Payoff, Exercise>::option_type() const noexcept
```

Returns the call-or-put direction.

#### `strike`

```cpp
double kiyosi::ExerciseBasedOption<Payoff, Exercise>::strike() const noexcept
```

Returns the positive strike price.

#### `effective_date`

```cpp
Date kiyosi::ExerciseBasedOption<Payoff, Exercise>::effective_date() const noexcept
```

Returns the first date of the option life.

#### `expiry_date`

```cpp
Date kiyosi::ExerciseBasedOption<Payoff, Exercise>::expiry_date() const noexcept
```

Returns the option expiry date.

#### `terms`

```cpp
const OptionTerms & kiyosi::ExerciseBasedOption<Payoff, Exercise>::terms() const noexcept
```

Returns the validated contractual terms.

#### `payoff`

```cpp
const Payoff & kiyosi::ExerciseBasedOption<Payoff, Exercise>::payoff() const noexcept
```

Returns the payoff tag.

#### `exercise`

```cpp
const Exercise & kiyosi::ExerciseBasedOption<Payoff, Exercise>::exercise() const noexcept
```

Returns the exercise-style tag.

#### `payout`

```cpp
double kiyosi::ExerciseBasedOption<Payoff, Exercise>::payout() const noexcept
```

Returns the fixed payout when the payoff type provides one.
