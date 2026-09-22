---
description: C++ API declarations from kiyosi/pricing/implied.hpp.
outline: [2, 4]
---

# `<kiyosi/pricing/implied.hpp>`

```cpp
#include <kiyosi/pricing/implied.hpp>
```

## `implied_volatility`

```cpp
template <typename Engine, typename Option>
Result< double > kiyosi::implied_volatility(const Engine &engine, const Option &option, const PricingContext &context, double observed_price, ImpliedVolatilitySettings settings={})
```

Bisects the engine's price curve in volatility; the caller's bounds must bracket the quote. 
**Template parameters**

- `` — Pricing engine providing `price(option, context)`.
- `` — Instrument accepted by the engine.

**Parameters**

- `` — Pricing engine used for each trial volatility.
- `` — Instrument to value.
- `` — Market state whose volatility is replaced for each trial.
- `` — Finite market price to match.
- `` — Positive bounds and convergence controls.

**Returns:** Implied volatility, or a validation, bracketing, pricing, or convergence error.

## `implied_coupon`

```cpp
template <typename Engine, typename Option>
Result< double > kiyosi::implied_coupon(const Engine &engine, const Option &option, const PricingContext &context, double observed_price, CouponQuoteConvention convention, ImpliedCouponSettings settings={})
```

Bisects a Snowball engine's price curve in its knock-out coupon. 
**Parameters**

- `` — Pricing engine used for each trial coupon.
- `` — Snowball-family instrument to value.
- `` — Market state used for every trial.
- `` — Finite market price to match.
- `` — Whether the maturity coupon shifts with the quoted coupon.
- `` — Non-negative bounds and convergence controls.

**Returns:** Implied coupon, or a validation, bracketing, pricing, or convergence error.

## `implied_coupon`

```cpp
template <typename Engine, typename Option>
Result< double > kiyosi::implied_coupon(const Engine &engine, const Option &option, const PricingContext &context, double observed_price, ImpliedCouponSettings settings={})
```

Bisects the engine's price curve in an unambiguous product coupon, such as a Phoenix coupon. 
**Returns:** Implied coupon, or a validation, bracketing, pricing, or convergence error.
