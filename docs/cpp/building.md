---
description: Build and install the kiyosi C++23 library, then consume its exported CMake target.
---

# Build the C++ library

## Prerequisites

Install CMake 3.28 or newer, Ninja, and a C++23-capable compiler. Clone the source repository and run the following commands from its root:

```sh
git clone https://github.com/lilkui/kiyosi.git
cd kiyosi
```

## Configure, build, and test

::: code-group

```sh [Linux]
cmake --preset linux-release
cmake --build --preset linux-release
ctest --preset linux-release
cmake --install out/build/linux-release
```

```powershell [Windows]
cmake --preset windows-release
cmake --build --preset windows-release
ctest --preset windows-release
cmake --install out/build/windows-release
```

:::

On Windows, use a **Visual Studio Developer PowerShell** so the compiler toolchain is available. For a custom install directory, pass `--prefix <directory>` to `cmake --install`.

## Link your application

After installing kiyosi, add these lines after creating your application's `my_app` target:

```cmake
find_package(kiyosi CONFIG REQUIRED)
target_link_libraries(my_app PRIVATE kiyosi::kiyosi)
```

If CMake cannot locate the package, add your installation prefix to `CMAKE_PREFIX_PATH` when configuring the consuming application.

Include the umbrella header:

```cpp
#include <kiyosi/kiyosi.hpp>
```

The [all-pricing-engines example](https://github.com/lilkui/kiyosi/blob/main/examples/all_pricing_engines.cpp) demonstrates the native API across instrument families.

Source: [kiyosi C++ build instructions](https://github.com/lilkui/kiyosi#c-library) and [CMake presets](https://github.com/lilkui/kiyosi/blob/main/CMakePresets.json).
