---
description: kiyosi/instruments/exercise_based_option.hpp 中的 C++ API 声明。
outline: [2, 4]
---

# `<kiyosi/instruments/exercise_based_option.hpp>`

```cpp
#include <kiyosi/instruments/exercise_based_option.hpp>
```

## `kiyosi::ExerciseBasedOption`

```cpp
template <OptionPayoff Payoff, OptionExercise Exercise>
class kiyosi::ExerciseBasedOption
```

An option built from an independent payoff and exercise style over shared option terms.
**模板参数**

- `Payoff` — Copyable payoff tag satisfying `OptionPayoff`.
- `Exercise` — Copyable exercise-style tag satisfying `OptionExercise`.

### 成员

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
