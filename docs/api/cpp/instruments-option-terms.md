---
description: C++ API declarations from kiyosi/instruments/option_terms.hpp.
outline: [2, 4]
---

# `<kiyosi/instruments/option_terms.hpp>`

```cpp
#include <kiyosi/instruments/option_terms.hpp>
```

## `OptionType`

```cpp
enum class OptionType
```

Direction of an option payoff.

**Values**

- `call` — Right to benefit from prices above the strike.
- `put` — Right to benefit from prices below the strike.

## `kiyosi::OptionTerms`

```cpp
class kiyosi::OptionTerms
```

Contractual essentials shared by every strike-and-life option: option_type, strike, and life dates.

### Members

#### `option_type`

```cpp
OptionType kiyosi::OptionTerms::option_type() const noexcept
```

Returns the call-or-put direction.

#### `strike`

```cpp
double kiyosi::OptionTerms::strike() const noexcept
```

Returns the positive strike price.

#### `effective_date`

```cpp
Date kiyosi::OptionTerms::effective_date() const noexcept
```

Returns the first date of the contract life.

#### `expiry_date`

```cpp
Date kiyosi::OptionTerms::expiry_date() const noexcept
```

Returns the final date of the contract life.
