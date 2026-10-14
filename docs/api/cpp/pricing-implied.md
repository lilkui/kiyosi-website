---
description: kiyosi/pricing/implied.hpp 中的 C++ API 声明。
outline: [2, 4]
---

# `<kiyosi/pricing/implied.hpp>`

```cpp
#include <kiyosi/pricing/implied.hpp>
```

## `implied_volatility`

```cpp
template <typename Engine, typename Option>
Result<double> kiyosi::implied_volatility(const Engine &engine, const Option &option, const PricingContext &context, double observed_price, ImpliedVolatilitySettings settings={})
```

Uses safeguarded Brent interpolation in volatility; the caller's bounds must bracket the quote. For CRR trees, the interval is intersected with the tree's admissible volatility range.
**模板参数**

- `Engine` — Pricing engine providing `price(option, context)`.
- `Option` — Instrument accepted by the engine.

**参数**

- `engine` — Pricing engine used for each trial volatility.
- `option` — Instrument to value.
- `context` — Market state whose volatility is replaced for each trial.
- `observed_price` — Finite market price to match.
- `settings` — Positive bounds and convergence controls. Built-in Monte Carlo trials share one seed per solve when the engine has no explicit seed; tolerance applies to that sampled price curve and does not bound sampling error. CPU European Monte Carlo trials reuse per-solve samples with storage linear in path count. CUDA accumulator and autocallable trials reuse a workspace local to each solve. A root is not guaranteed unique; known states with volatility-independent remaining cashflows, including fixed touch payments, are rejected. Built-in autocallable Monte Carlo engines reject fixed cashflows after input validation, before executing a simulation backend.

**返回值:** Implied volatility, or a validation, bracketing, pricing, or convergence error.

## `implied_volatility< AnalyticBarrierEngine, BarrierOption >`

```cpp
template <>
Result<double> kiyosi::implied_volatility<AnalyticBarrierEngine, BarrierOption>(const AnalyticBarrierEngine &engine, const BarrierOption &option, const PricingContext &context, double observed_price, ImpliedVolatilitySettings settings)
```

Scheduled analytic barriers validate their calendar once per solve.

## `implied_volatility< AnalyticBinaryBarrierEngine, BinaryBarrierOption >`

```cpp
template <>
Result<double> kiyosi::implied_volatility<AnalyticBinaryBarrierEngine, BinaryBarrierOption>(const AnalyticBinaryBarrierEngine &engine, const BinaryBarrierOption &option, const PricingContext &context, double observed_price, ImpliedVolatilitySettings settings)
```

## `implied_volatility< AnalyticBinaryBarrierEngine, TouchOption >`

```cpp
template <>
Result<double> kiyosi::implied_volatility<AnalyticBinaryBarrierEngine, TouchOption>(const AnalyticBinaryBarrierEngine &engine, const TouchOption &option, const PricingContext &context, double observed_price, ImpliedVolatilitySettings settings)
```

## `implied_volatility< MonteCarloVanillaEngine, EuropeanOption >`

```cpp
template <>
Result<double> kiyosi::implied_volatility<MonteCarloVanillaEngine, EuropeanOption>(const MonteCarloVanillaEngine &engine, const EuropeanOption &option, const PricingContext &context, double observed_price, ImpliedVolatilitySettings settings)
```

## `implied_volatility< MonteCarloVanillaEngine, AmericanOption >`

```cpp
template <>
Result<double> kiyosi::implied_volatility<MonteCarloVanillaEngine, AmericanOption>(const MonteCarloVanillaEngine &engine, const AmericanOption &option, const PricingContext &context, double observed_price, ImpliedVolatilitySettings settings)
```

Reuses request-local exercise buffers across trials; growth factors are recomputed.

## `implied_volatility`

```cpp
template <AutocallableProduct Note>
Result<double> kiyosi::implied_volatility(const FiniteDifferenceAutocallableEngine &engine, const Note &option, const PricingContext &context, double observed_price, ImpliedVolatilitySettings settings={})
```

Finite-difference autocallables validate immutable contracts and calendars once per solve.

## `implied_volatility< MonteCarloAccumulatorEngine, Accumulator >`

```cpp
template <>
Result<double> kiyosi::implied_volatility<MonteCarloAccumulatorEngine, Accumulator>(const MonteCarloAccumulatorEngine &engine, const Accumulator &option, const PricingContext &context, double observed_price, ImpliedVolatilitySettings settings)
```

Reuses CUDA buffers within one solve without sharing storage between requests.

## `implied_volatility`

```cpp
template <AutocallableProduct Note>
Result<double> kiyosi::implied_volatility(const MonteCarloAutocallableEngine &engine, const Note &option, const PricingContext &context, double observed_price, ImpliedVolatilitySettings settings={})
```

Reuses CUDA buffers within one solve without sharing storage between requests.

## `implied_coupon`

```cpp
template <typename Engine, typename Option>
Result<double> kiyosi::implied_coupon(const Engine &engine, const Option &option, const PricingContext &context, double observed_price, CouponQuoteConvention convention, ImpliedCouponSettings settings={})
```

Solves a Snowball engine's price curve in its knock-out coupon.
**参数**

- `engine` — Pricing engine used for each trial coupon.
- `option` — Snowball-family instrument to value.
- `context` — Market state used for every trial.
- `observed_price` — Finite market price to match.
- `convention` — Whether the maturity coupon shifts with the quoted coupon.
- `settings` — Finite coupon bounds and convergence controls. Built-in Monte Carlo trials share one seed per solve when the engine has no explicit seed; tolerance applies to that sampled price curve and does not bound sampling error. Built-in Monte Carlo engines share paths between coupon bounds. Built-in Monte Carlo and FD engines try interpolation, verify its price residual, then bisect if needed. States with no quoted coupon exposure on the engine's sampled price curve are rejected.

**返回值:** Implied coupon, or a validation, bracketing, pricing, or convergence error.

## `implied_coupon`

```cpp
template <typename Engine, typename Option>
Result<double> kiyosi::implied_coupon(const Engine &engine, const Option &option, const PricingContext &context, double observed_price, ImpliedCouponSettings settings={})
```

Solves the engine's price curve in an unambiguous product coupon, such as a Phoenix coupon. Built-in Monte Carlo trials share one seed per solve when the engine has no explicit seed; tolerance applies to that sampled price curve and does not bound sampling error. Built-in Monte Carlo engines share paths between coupon bounds. Built-in Monte Carlo and FD engines try interpolation, verify its price residual, then bisect if needed. States with no quoted coupon exposure on the engine's sampled price curve are rejected.
**返回值:** Implied coupon, or a validation, bracketing, pricing, or convergence error.

## `implied_coupon`

```cpp
template <AutocallableProduct Note>
Result<double> kiyosi::implied_coupon(const FiniteDifferenceAutocallableEngine &engine, const Note &option, const PricingContext &context, double observed_price, CouponQuoteConvention convention, ImpliedCouponSettings settings={})
```

Reuse grids, buffers and compatible factors within one solve; requests share no storage.

## `implied_coupon`

```cpp
Result<double> kiyosi::implied_coupon(const FiniteDifferenceAutocallableEngine &engine, const PhoenixOption &option, const PricingContext &context, double observed_price, ImpliedCouponSettings settings={})
```
