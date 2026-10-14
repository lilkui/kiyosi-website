---
description: kiyosi/instruments/payoff.hpp 中的 C++ API 声明。
outline: [2, 4]
---

# `<kiyosi/instruments/payoff.hpp>`

```cpp
#include <kiyosi/instruments/payoff.hpp>
```

## `PayoffType`

```cpp
enum class PayoffType
```

Binary payoff denomination.

**枚举值**

- `cash` — Fixed cash payout.
- `asset` — Underlying-asset payout.

## `BinaryPayoff`

```cpp
using kiyosi::BinaryPayoff = std::variant<CashOrNothingPayoff, AssetOrNothingPayoff>
```

Cash-or-nothing or asset-or-nothing payoff.

## `payoff_type`

```cpp
PayoffType kiyosi::payoff_type(const BinaryPayoff &payoff) noexcept
```

Identifies the denomination of a binary payoff.
**参数**

- `payoff` — Payoff to inspect.

**返回值:** `PayoffType::cash` or `PayoffType::asset`.

## `kiyosi::AssetOrNothingPayoff`

```cpp
struct kiyosi::AssetOrNothingPayoff
```

Tag for a binary payoff equal to the underlying asset value.

## `kiyosi::CashOrNothingPayoff`

```cpp
class kiyosi::CashOrNothingPayoff
```

Validated fixed-cash binary payoff.

### 成员

#### `payout`

```cpp
double kiyosi::CashOrNothingPayoff::payout() const noexcept
```

Returns the positive cash payout.

## `kiyosi::VanillaPayoff`

```cpp
struct kiyosi::VanillaPayoff
```

Tag for a standard call or put payoff.

## `kiyosi::OptionPayoff`

```cpp
template <typename Value>
concept kiyosi::OptionPayoff
```

Payoff tags whose semantics are defined by the core.
