---
description: C++ API declarations from kiyosi/pricing/result.hpp.
outline: [2, 4]
---

# `<kiyosi/pricing/result.hpp>`

```cpp
#include <kiyosi/pricing/result.hpp>
```

## `RiskMeasure`

```cpp
enum class RiskMeasure
```

Public risk-measure contract:
- price uses the instrument's value units;
- delta, gamma, and speed are price changes per one spot unit, squared spot unit, and cubed spot unit, respectively;
- vega, vanna, and zomma are price, delta, and gamma changes per one volatility percentage point (an absolute volatility change of 0.01);
- rho is the price change per one interest-rate percentage point (an absolute rate change of 0.01);
- theta, charm, and color are price, delta, and gamma changes per calendar day as valuation time moves forward. Undefined or unsupported measures are unavailable (`std::nullopt`), never represented by zero.

**Values**

- `price` — Instrument value.
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

## `risk_measure_count`

```cpp
std::size_t kiyosi::risk_measure_count
```

Number of defined `RiskMeasure` values.

## `risk_measure_index`

```cpp
std::optional<std::size_t> kiyosi::risk_measure_index(RiskMeasure measure) noexcept
```

Converts a risk measure to its `PricingResult` storage index. 
**Returns:** The index, or `std::nullopt` for an unknown enumerator.

## `make_pricing_result`

```cpp
Result<PricingResult> kiyosi::make_pricing_result(std::initializer_list<std::pair<RiskMeasure, std::optional<double>>> entries)
```

Builds a result from runtime risk-measure entries. Unknown measures are rejected with `invalid_parameter`. Later duplicate entries replace earlier entries for the same measure. 
**Returns:** The populated result, or an `invalid_parameter` error.

## `kiyosi::PricingResult`

```cpp
class kiyosi::PricingResult
```

Fixed-size collection of optional pricing and risk measures.

### Members

#### `MeasureValues`

```cpp
using kiyosi::PricingResult::MeasureValues = std::array<std::optional<double>, risk_measure_count>
```

Storage type indexed by `risk_measure_index()`.

#### `PricingResult`

```cpp
kiyosi::PricingResult::PricingResult()=default
```

Creates a result with every measure unavailable.

#### `has`

```cpp
bool kiyosi::PricingResult::has(RiskMeasure measure) const noexcept
```

Reports whether the measure is available; a stored zero is available.

#### `get`

```cpp
Result<std::optional<double>> kiyosi::PricingResult::get(RiskMeasure measure) const
```

Retrieves a measure when its enumerator is valid. 
**Returns:** The optional value, or an `invalid_parameter` error for an unknown measure.

#### `require`

```cpp
Result<double> kiyosi::PricingResult::require(RiskMeasure measure) const
```

Retrieves a required measure. 
**Returns:** The value, or an `invalid_parameter` or `invalid_result` error.

#### `values_view`

```cpp
const MeasureValues & kiyosi::PricingResult::values_view() const noexcept
```

Returns a read-only view of all measure slots. 
**Note:** The reference remains valid until this result is destroyed, moved from, or assigned.

#### `all_finite`

```cpp
bool kiyosi::PricingResult::all_finite() const noexcept
```

Tests whether every available measure is finite.
