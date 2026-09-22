---
description: C++ API declarations from kiyosi/instruments/digital.hpp.
outline: [2, 4]
---

# `<kiyosi/instruments/digital.hpp>`

```cpp
#include <kiyosi/instruments/digital.hpp>
```

## `CashOrNothingOption`

```cpp
using kiyosi::CashOrNothingOption = ExerciseBasedOption<CashOrNothingPayoff, EuropeanExercise>
```

European option paying fixed cash when it expires in the money.

## `AssetOrNothingOption`

```cpp
using kiyosi::AssetOrNothingOption = ExerciseBasedOption<AssetOrNothingPayoff, EuropeanExercise>
```

European option paying the underlying asset when it expires in the money.

## `make_cash_or_nothing_option`

```cpp
Result< CashOrNothingOption > kiyosi::make_cash_or_nothing_option(OptionType option_type, double strike, double payout, Date effective_date, Date expiry_date)
```

Creates a validated cash-or-nothing European option. 
**Parameters**

- `` — Call-or-put direction.
- `` — Positive strike price.
- `` — Positive finite cash amount paid in the money.
- `` — First date of the option life.
- `` — Final date of the option life.

**Returns:** The option, or an input-validation error.

## `make_asset_or_nothing_option`

```cpp
Result< AssetOrNothingOption > kiyosi::make_asset_or_nothing_option(OptionType option_type, double strike, Date effective_date, Date expiry_date)
```

Creates a validated asset-or-nothing European option. 
**Returns:** The option, or an input-validation error.
