---
description: kiyosi/instruments/vanilla.hpp 中的 C++ API 声明。
outline: [2, 4]
---

# `<kiyosi/instruments/vanilla.hpp>`

```cpp
#include <kiyosi/instruments/vanilla.hpp>
```

## `EuropeanOption`

```cpp
using kiyosi::EuropeanOption = ExerciseBasedOption<VanillaPayoff, EuropeanExercise>
```

European vanilla call or put.

## `AmericanOption`

```cpp
using kiyosi::AmericanOption = ExerciseBasedOption<VanillaPayoff, AmericanExercise>
```

American vanilla call or put.

## `make_european_option`

```cpp
Result<EuropeanOption> kiyosi::make_european_option(OptionType option_type, double strike, Date effective_date, Date expiry_date)
```

Creates a validated European vanilla option.
**返回值:** The option, or an `invalid_option`, `invalid_strike`, `invalid_date`, or `invalid_time_range` error.

## `make_american_option`

```cpp
Result<AmericanOption> kiyosi::make_american_option(OptionType option_type, double strike, Date effective_date, Date expiry_date)
```

Creates a validated American vanilla option.
**返回值:** The option, or an `invalid_option`, `invalid_strike`, `invalid_date`, or `invalid_time_range` error.
