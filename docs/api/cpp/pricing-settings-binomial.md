---
description: kiyosi/pricing/settings/binomial.hpp 中的 C++ API 声明。
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

### 成员

#### `step_count`

```cpp
int kiyosi::BinomialSettings::step_count
```

Number of tree time steps; must be positive.
