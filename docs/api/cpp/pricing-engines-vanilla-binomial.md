---
description: C++ API declarations from kiyosi/pricing/engines/vanilla/binomial.hpp.
outline: [2, 4]
---

# `<kiyosi/pricing/engines/vanilla/binomial.hpp>`

```cpp
#include <kiyosi/pricing/engines/vanilla/binomial.hpp>
```

## `kiyosi::CoxRossRubinsteinVanillaEngine`

```cpp
class kiyosi::CoxRossRubinsteinVanillaEngine
```

Cox-Ross-Rubinstein binomial-tree engine for vanilla European and American options. Value is tree-derived; delta and gamma are numerical tree estimates; higher Greeks are unavailable.

### Members

#### `CoxRossRubinsteinVanillaEngine`

```cpp
kiyosi::CoxRossRubinsteinVanillaEngine::CoxRossRubinsteinVanillaEngine(BinomialSettings settings={})
```

Creates an engine with aggregate binomial settings.

#### `CoxRossRubinsteinVanillaEngine`

```cpp
kiyosi::CoxRossRubinsteinVanillaEngine::CoxRossRubinsteinVanillaEngine(int step_count)
```

Creates an engine with an explicit tree step count.

#### `price`

```cpp
template <OptionPayoff Payoff, OptionExercise Exercise>
Result< PricingResult > kiyosi::CoxRossRubinsteinVanillaEngine::price(const ExerciseBasedOption< Payoff, Exercise > &option, const PricingContext &context) const
```

Prices a European or American vanilla option. 
**Returns:** Pricing measures, or a contract, context, or settings error.

#### `settings`

```cpp
BinomialSettings kiyosi::CoxRossRubinsteinVanillaEngine::settings() const noexcept
```

Returns the engine settings.
