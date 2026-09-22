---
description: C++ API declarations from kiyosi/pricing/settings/binomial.hpp.
outline: [2, 4]
---

# `<kiyosi/pricing/settings/binomial.hpp>`

```cpp
#include <kiyosi/pricing/settings/binomial.hpp>
```

## `kiyosi::BinomialSettings`

```cpp
struct kiyosi::BinomialSettings
```

Aggregate configuration validated by binomial engines when price() is called.

### Members

#### `step_count`

```cpp
int kiyosi::BinomialSettings::step_count
```

Number of tree time steps; must be positive.
