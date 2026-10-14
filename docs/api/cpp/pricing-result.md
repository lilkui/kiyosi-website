---
description: C++ API declarations from kiyosi/pricing/result.hpp.
outline: [2, 4]
---

# `<kiyosi/pricing/result.hpp>`

```cpp
#include <kiyosi/pricing/result.hpp>
```

## `Greek`

```cpp
enum class Greek
```

Public `Greek` contract:
- delta, gamma, and speed are price changes per one spot unit, squared spot unit, and cubed spot unit, respectively;
- vega, vanna, and zomma are price, delta, and gamma changes per one volatility percentage point (an absolute volatility change of 0.01);
- rho is the price change per one interest-rate percentage point (an absolute rate change of 0.01);
- theta, charm, and color are price, delta, and gamma changes per calendar day as valuation time moves forward. Unrequested, undefined, or unsupported Greeks are unavailable (`std::nullopt`), never zero sentinels.

**Values**

- `delta` — First derivative with respect to spot.
- `gamma` — Second derivative with respect to spot.
- `speed` — Third derivative with respect to spot.
- `theta` — Value change per calendar day of forward valuation time.
- `charm` — Delta change per calendar day of forward valuation time.
- `color` — Gamma change per calendar day of forward valuation time.
- `vega` — Value change per volatility percentage point.
- `vanna` — Delta change per volatility percentage point.
- `zomma` — Gamma change per volatility percentage point.
- `rho` — Value change per interest-rate percentage point.

## `greek_count`

```cpp
std::size_t kiyosi::greek_count
```

Number of defined `Greek` values.

## `greek_index`

```cpp
std::optional<std::size_t> kiyosi::greek_index(Greek greek) noexcept
```

Converts a `Greek` to its `PricingResult` storage index.
**Returns:** The index, or `std::nullopt` for an unknown enumerator.

## `make_pricing_result`

```cpp
Result<PricingResult> kiyosi::make_pricing_result(double price, std::initializer_list<std::pair<Greek, std::optional<double>>> entries={})
```

Builds a result from a price and runtime `Greek` entries. Unknown Greeks are rejected with `invalid_parameter`. Later duplicate entries replace earlier entries for the same `Greek`. The final price and every available `Greek` must be finite.
**Returns:** The populated result, or an `invalid_parameter` or `invalid_result` error.

## `kiyosi::GreeksRequest`

```cpp
class kiyosi::GreeksRequest
```

Greeks requested from a joint valuation. Price is always included separately. Construct from one or more `Greek` values, or from true for every `Greek`. Duplicates are ignored; empty requests and unknown values are rejected by price_with_greeks() with an invalid_parameter error.

### Members

#### `GreeksRequest`

```cpp
kiyosi::GreeksRequest::GreeksRequest()=default
```

Used internally for price-only valuations; invalid for price_with_greeks().

#### `GreeksRequest`

```cpp
kiyosi::GreeksRequest::GreeksRequest(std::initializer_list<Greek> greeks)
```

#### `GreeksRequest`

```cpp
kiyosi::GreeksRequest::GreeksRequest(std::span<const Greek> greeks)
```

#### `GreeksRequest`

```cpp
template <std::same_as< bool > T>
kiyosi::GreeksRequest::GreeksRequest(T all_greeks)
```

#### `has`

```cpp
bool kiyosi::GreeksRequest::has(Greek greek) const noexcept
```

#### `empty`

```cpp
bool kiyosi::GreeksRequest::empty() const noexcept
```

#### `validate`

```cpp
Result<void> kiyosi::GreeksRequest::validate() const
```

## `kiyosi::PricingResult`

```cpp
class kiyosi::PricingResult
```

Finite price and a fixed-size collection of optional finite Greeks.

### Members

#### `GreekValues`

```cpp
using kiyosi::PricingResult::GreekValues = std::array<std::optional<double>, greek_count>
```

Storage type indexed by `greek_index()`.

#### `price`

```cpp
double kiyosi::PricingResult::price() const noexcept
```

A finite price is present in every successfully constructed result.

#### `has`

```cpp
bool kiyosi::PricingResult::has(Greek greek) const noexcept
```

Reports whether the `Greek` is available; a stored zero is available.

#### `get`

```cpp
Result<std::optional<double>> kiyosi::PricingResult::get(Greek greek) const
```

Retrieves a `Greek` when its enumerator is valid.
**Returns:** The optional value, or an `invalid_parameter` error for an unknown `Greek`.

#### `require`

```cpp
Result<double> kiyosi::PricingResult::require(Greek greek) const
```

Retrieves a required `Greek`.
**Returns:** The value, or an `invalid_parameter` or `invalid_result` error.

#### `values_view`

```cpp
const GreekValues & kiyosi::PricingResult::values_view() const noexcept
```

Returns a read-only view of all `Greek` slots.
**Note:** The reference remains valid until this result is destroyed, moved from, or assigned.

#### `selected`

```cpp
PricingResult kiyosi::PricingResult::selected(GreeksRequest greeks) const noexcept
```

Returns price and only the requested Greeks.

#### `all_finite`

```cpp
bool kiyosi::PricingResult::all_finite() const noexcept
```

Tests whether price and every available `Greek` are finite.
