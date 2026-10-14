---
description: C++ API declarations from kiyosi/pricing/numerical_greeks.hpp.
outline: [2, 4]
---

# `<kiyosi/pricing/numerical_greeks.hpp>`

```cpp
#include <kiyosi/pricing/numerical_greeks.hpp>
```

## `calculate_numerical_greeks`

```cpp
template <typename Engine, typename Option>
Result<PricingResult> kiyosi::calculate_numerical_greeks(const Engine &engine, const Option &option, const PricingContext &context, NumericalShiftSettings settings={})
```

Computes price and all feasible Greeks using only numerical price differences. At expiry or a monitored barrier hit-state boundary, only price is available. Missing legal stencils leave individual measures empty; a failed feasible valuation fails the operation. Built-in Monte Carlo valuations share one seed per request. Spot stencils crossing a currently monitored event threshold are unavailable. Built-in finite-difference valuations share the unshifted context's asset domain. Custom engines are used as supplied and control their own sampling and asset domain. Shifts and units follow `NumericalShiftSettings` and `Greek`, respectively.
