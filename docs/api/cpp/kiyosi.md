---
description: C++ API declarations from kiyosi/kiyosi.hpp.
outline: [2, 4]
---

# `<kiyosi/kiyosi.hpp>`

```cpp
#include <kiyosi/kiyosi.hpp>
```

Thread safety: Unless documented otherwise, operations on distinct objects and concurrent const operations on the same object are safe. An object must remain alive and must not be moved from, assigned to, or otherwise mutated during concurrent access. Concurrent access involving mutation requires external synchronization.
