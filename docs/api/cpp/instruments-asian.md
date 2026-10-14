---
description: kiyosi/instruments/asian.hpp 中的 C++ API 声明。
outline: [2, 4]
---

# `<kiyosi/instruments/asian.hpp>`

```cpp
#include <kiyosi/instruments/asian.hpp>
```

## `GeometricAveragePriceOption`

```cpp
using kiyosi::GeometricAveragePriceOption = AveragePriceOption<GeometricAveraging>
```

Average-price option using geometric averaging.

## `ArithmeticAveragePriceOption`

```cpp
using kiyosi::ArithmeticAveragePriceOption = AveragePriceOption<ArithmeticAveraging>
```

Average-price option using arithmetic averaging.

## `default_realized_average`

```cpp
double kiyosi::default_realized_average
```

Default realized average for a contract whose averaging has not begun.

## `make_average_option`

```cpp
template <AveragingConvention Averaging>
Result<AveragePriceOption<Averaging>> kiyosi::make_average_option(OptionType option_type, double strike, Date effective_date, Date averaging_start_date, Date expiry_date, double realized_average)
```

`Date` arguments are ordered `effective_date`, `averaging_start_date`, `expiry_date`; valid terms satisfy `effective_date <= averaging_start_date <= expiry_date`. Equal averaging start and expiry dates denote a single fixing at expiry.
**模板参数**

- `Averaging` — `GeometricAveraging` or `ArithmeticAveraging`.

**返回值:** The option, or an input-validation error.

## `make_geometric_average_option`

```cpp
Result<GeometricAveragePriceOption> kiyosi::make_geometric_average_option(OptionType option_type, double strike, Date effective_date, Date averaging_start_date, Date expiry_date, double realized_average=default_realized_average)
```

Creates a geometric-average option; dates follow make_average_option ordering.
**返回值:** The option, or an input-validation error.

## `make_arithmetic_average_option`

```cpp
Result<ArithmeticAveragePriceOption> kiyosi::make_arithmetic_average_option(OptionType option_type, double strike, Date effective_date, Date averaging_start_date, Date expiry_date, double realized_average=default_realized_average)
```

Creates an arithmetic-average option; dates follow make_average_option ordering.
**返回值:** The option, or an input-validation error.

## `kiyosi::ArithmeticAveraging`

```cpp
struct kiyosi::ArithmeticAveraging
```

Tag selecting arithmetic averaging.

## `kiyosi::AveragePriceOption`

```cpp
template <AveragingConvention Averaging>
class kiyosi::AveragePriceOption
```

Average-rate option; `Averaging` distinguishes the geometric and arithmetic conventions.

### 成员

#### `option_type`

```cpp
OptionType kiyosi::AveragePriceOption<Averaging>::option_type() const noexcept
```

Returns the call-or-put direction.

#### `strike`

```cpp
double kiyosi::AveragePriceOption<Averaging>::strike() const noexcept
```

Returns the positive strike price.

#### `averaging_start_date`

```cpp
Date kiyosi::AveragePriceOption<Averaging>::averaging_start_date() const noexcept
```

Returns the first date included in the average.

#### `effective_date`

```cpp
Date kiyosi::AveragePriceOption<Averaging>::effective_date() const noexcept
```

Returns the first date of the contract life.

#### `realized_average`

```cpp
double kiyosi::AveragePriceOption<Averaging>::realized_average() const noexcept
```

Returns the non-negative average realized before valuation.

#### `expiry_date`

```cpp
Date kiyosi::AveragePriceOption<Averaging>::expiry_date() const noexcept
```

Returns the final date of the contract life and averaging window.

## `kiyosi::GeometricAveraging`

```cpp
struct kiyosi::GeometricAveraging
```

Averaging conventions; the tag selects the pricing engine overload.

## `kiyosi::AveragingConvention`

```cpp
template <typename Value>
concept kiyosi::AveragingConvention
```

Averaging conventions whose semantics are defined by the core.
