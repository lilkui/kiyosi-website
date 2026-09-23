---
description: 构建并安装 kiyosi C++23 库，通过导出的 CMake 目标将其链接到应用程序。
---

# 构建 C++ 库

## 准备工作 {#prerequisites}

安装 CMake 3.28 或更高版本、Ninja，以及支持 C++23 的编译器。克隆源码仓库，然后进入仓库根目录：

```sh
git clone https://github.com/lilkui/kiyosi.git
cd kiyosi
```

## 配置、构建与测试 {#configure-build-and-test}

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

Windows 用户请在 **Visual Studio Developer PowerShell** 中运行这些命令，以确保编译工具链可用。如需指定安装目录，可在 `cmake --install` 后添加 `--prefix <directory>`。

## 链接到应用程序 {#link-your-application}

安装 kiyosi 后，在应用程序的 CMake 配置中创建 `my_app` 目标，再添加：

```cmake
find_package(kiyosi CONFIG REQUIRED)
target_link_libraries(my_app PRIVATE kiyosi::kiyosi)
```

如果 CMake 找不到该包，请在配置应用程序时将 kiyosi 的安装前缀加入 `CMAKE_PREFIX_PATH`。

在代码中包含统一入口头文件：

```cpp
#include <kiyosi/kiyosi.hpp>
```

[各类定价引擎示例](https://github.com/lilkui/kiyosi/blob/main/examples/all_pricing_engines.cpp)展示了如何使用原生 API 为不同类型的金融工具定价。

来源：[kiyosi C++ 构建说明](https://github.com/lilkui/kiyosi#c-library)和 [CMake 预设](https://github.com/lilkui/kiyosi/blob/main/CMakePresets.json)。
