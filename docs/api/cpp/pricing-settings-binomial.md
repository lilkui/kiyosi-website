---
description: kiyosi/pricing/settings/binomial.hpp 中的 C++ API 声明。
outline: [2, 4]
---

# `<kiyosi/pricing/settings/binomial.hpp>`

```cpp
#include <kiyosi/pricing/settings/binomial.hpp>
```

## `validate_binomial_settings`

```cpp
Result<void> kiyosi::validate_binomial_settings(BinomialSettings settings)
```

Validates the binomial tree size.

## `kiyosi::BinomialSettings`

```cpp
struct kiyosi::BinomialSettings
```

Aggregate configuration validated when creating a binomial engine.

### 成员

#### `step_count`

```cpp
int kiyosi::BinomialSettings::step_count
```

Number of tree time steps; must be between 1 and 1,000,000.
