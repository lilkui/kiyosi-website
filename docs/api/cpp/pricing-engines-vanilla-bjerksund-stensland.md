---
description: C++ API declarations from kiyosi/pricing/engines/vanilla/bjerksund_stensland.hpp.
outline: [2, 4]
---

# `<kiyosi/pricing/engines/vanilla/bjerksund_stensland.hpp>`

```cpp
#include <kiyosi/pricing/engines/vanilla/bjerksund_stensland.hpp>
```

## `kiyosi::BjerksundStenslandVanillaEngine`

```cpp
class kiyosi::BjerksundStenslandVanillaEngine
```

Bjerksund-Stensland (2002) two-step American approximation. Before expiry, calls require a non-negative risk-free rate and puts require a non-negative dividend yield (the interest rate under put-call symmetry). The approximation rejects market inputs whose exercise boundaries do not exceed the strike.

### Members

#### `price`

```cpp
Result<double> kiyosi::BjerksundStenslandVanillaEngine::price(const AmericanOption &option, const PricingContext &context) const
```

Prices an American vanilla option with the two-step approximation.
**Returns:** Price, a contract or context error, or `unsupported_operation` for a negative transformed rate or nonphysical exercise boundaries. Use a tree or finite-difference engine for those inputs. Returns `invalid_result` when the exercise exponent or price cannot be represented reliably.

#### `price_with_greeks`

```cpp
Result<PricingResult> kiyosi::BjerksundStenslandVanillaEngine::price_with_greeks(const AmericanOption &option, const PricingContext &context, GreeksRequest greeks, NumericalShiftSettings settings={}) const
```

Prices with the explicitly requested Greeks; unavailable measures remain empty.
