---
description: C++ API declarations from kiyosi/pricing/analytics.hpp.
outline: [2, 4]
---

# `<kiyosi/pricing/analytics.hpp>`

```cpp
#include <kiyosi/pricing/analytics.hpp>
```

## `kiyosi::NumericalAnalyticsEngine`

```cpp
template <typename Engine>
class kiyosi::NumericalAnalyticsEngine
```

Wraps any price-only engine so it also reports bump-derived risk and implied quantities without the caller threading shift settings through each call. Infeasible boundary stencils leave their measures unavailable without discarding a valid price; other bump failures remain operation failures. Its thread-safety guarantees are those of the wrapped engine; built-in engines follow the library default.

### Members

#### `NumericalAnalyticsEngine`

```cpp
kiyosi::NumericalAnalyticsEngine< Engine >::NumericalAnalyticsEngine(Engine engine={}, NumericalShiftSettings settings={})
```

Creates an analytics adapter around an engine and numerical-shift settings.

#### `price`

```cpp
template <typename Option>
Result< PricingResult > kiyosi::NumericalAnalyticsEngine< Engine >::price(const Option &option, const PricingContext &context) const
```

Prices an option and derives risk measures by revaluation. 
**Returns:** Pricing measures, or a validation, pricing, or result error.

#### `implied_volatility`

```cpp
template <typename Option>
Result< double > kiyosi::NumericalAnalyticsEngine< Engine >::implied_volatility(const Option &option, const PricingContext &context, double observed_price, ImpliedVolatilitySettings settings={}) const
```

Solves for the volatility matching an observed price. 
**Returns:** Implied volatility, or a validation, bracketing, pricing, or convergence error.

#### `implied_coupon`

```cpp
template <typename Option>
Result< double > kiyosi::NumericalAnalyticsEngine< Engine >::implied_coupon(const Option &option, const PricingContext &context, double observed_price, ImpliedCouponSettings settings={}) const
```

Solves for an unambiguous product coupon matching an observed price. 
**Returns:** Implied coupon, or a validation, bracketing, pricing, or convergence error.

#### `implied_coupon`

```cpp
template <typename Option>
Result< double > kiyosi::NumericalAnalyticsEngine< Engine >::implied_coupon(const Option &option, const PricingContext &context, double observed_price, CouponQuoteConvention convention, ImpliedCouponSettings settings={}) const
```

Solves for a quoted coupon using an explicit maturity-coupon convention. 
**Returns:** Implied coupon, or a validation, bracketing, pricing, or convergence error.

#### `engine`

```cpp
const Engine & kiyosi::NumericalAnalyticsEngine< Engine >::engine() const noexcept
```

Returns the wrapped pricing engine.

#### `settings`

```cpp
NumericalShiftSettings kiyosi::NumericalAnalyticsEngine< Engine >::settings() const noexcept
```

Returns the numerical-shift settings.
