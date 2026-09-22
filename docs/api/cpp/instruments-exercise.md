---
description: C++ API declarations from kiyosi/instruments/exercise.hpp.
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

Requirement for a value type used as an option exercise-style tag.
