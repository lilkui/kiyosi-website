---
description: C++ API declarations from kiyosi/instruments/accumulator.hpp.
outline: [2, 4]
---

# `<kiyosi/instruments/accumulator.hpp>`

```cpp
#include <kiyosi/instruments/accumulator.hpp>
```

## `make_accumulator`

```cpp
Result< Accumulator > kiyosi::make_accumulator(AccumulatorTerms terms)
```

Creates a validated accumulator contract. 
**Parameters**

- `` — Contract terms.

**Returns:** The accumulator, or an input-validation error.

## `kiyosi::Accumulator`

```cpp
class kiyosi::Accumulator
```

Forward accrual that buys a fixed daily quantity, accelerating below strike and terminating once spot reaches the knock-out level.

### Members

#### `strike`

```cpp
double kiyosi::Accumulator::strike() const noexcept
```

Returns the purchase strike.

#### `knock_out_level`

```cpp
double kiyosi::Accumulator::knock_out_level() const noexcept
```

Returns the knock-out spot level.

#### `daily_quantity`

```cpp
double kiyosi::Accumulator::daily_quantity() const noexcept
```

Returns the base quantity accrued per trading day.

#### `acceleration_factor`

```cpp
double kiyosi::Accumulator::acceleration_factor() const noexcept
```

Returns the below-strike quantity multiplier.

#### `accumulated_quantity`

```cpp
double kiyosi::Accumulator::accumulated_quantity() const noexcept
```

Returns the quantity accrued before valuation.

#### `effective_date`

```cpp
Date kiyosi::Accumulator::effective_date() const noexcept
```

Returns the first date of the contract life.

#### `expiry_date`

```cpp
Date kiyosi::Accumulator::expiry_date() const noexcept
```

Returns the final date of the contract life.

## `kiyosi::AccumulatorTerms`

```cpp
struct kiyosi::AccumulatorTerms
```

Input terms used to construct an `Accumulator`.

### Members

#### `strike`

```cpp
double kiyosi::AccumulatorTerms::strike
```

Positive purchase strike.

#### `knock_out_level`

```cpp
double kiyosi::AccumulatorTerms::knock_out_level
```

Positive spot level that terminates accrual.

#### `daily_quantity`

```cpp
double kiyosi::AccumulatorTerms::daily_quantity
```

Non-negative base quantity accrued per trading day.

#### `acceleration_factor`

```cpp
double kiyosi::AccumulatorTerms::acceleration_factor
```

Non-negative quantity multiplier below strike.

#### `accumulated_quantity`

```cpp
double kiyosi::AccumulatorTerms::accumulated_quantity
```

Non-negative quantity already accrued.

#### `effective_date`

```cpp
Date kiyosi::AccumulatorTerms::effective_date
```

First date of the contract life.

#### `expiry_date`

```cpp
Date kiyosi::AccumulatorTerms::expiry_date
```

Final date of the contract life.
