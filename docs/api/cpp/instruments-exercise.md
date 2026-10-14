---
description: kiyosi/instruments/exercise.hpp 中的 C++ API 声明。
outline: [2, 4]
---

# `<kiyosi/instruments/exercise.hpp>`

```cpp
#include <kiyosi/instruments/exercise.hpp>
```

## `kiyosi::AmericanExercise`

```cpp
struct kiyosi::AmericanExercise
```

Tag for exercise at any time during the option life.

## `kiyosi::EuropeanExercise`

```cpp
struct kiyosi::EuropeanExercise
```

Tag for exercise only at expiry.

## `kiyosi::OptionExercise`

```cpp
template <typename Value>
concept kiyosi::OptionExercise
```

Exercise styles whose semantics are defined by the core.
