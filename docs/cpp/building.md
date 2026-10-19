---
description: 构建并安装 kiyosi C++23 库，通过导出的 CMake 目标将其链接到应用程序。
---

# 构建 C++ 库

## 准备工作 {#prerequisites}

先安装 CMake 3.28 或更高版本、Ninja，以及支持 C++23 的编译器。Windows 预设使用 clang-cl，需安装 Visual Studio C++ 工具及 C++ Clang 编译器组件。克隆源码仓库并检出本文档对应版本：

```sh
git clone https://github.com/lilkui/kiyosi.git
cd kiyosi
git checkout 541546c
```

核心库依赖 **oneTBB 2023.1+**。CMake 优先查找已安装的 TBB；找不到时会自动下载并构建 oneTBB v2023.1.0，此时配置阶段需要联网。

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

Windows 下请在 **Visual Studio Developer PowerShell** 中运行这些命令，确保编译工具链可用。如需指定安装目录，可在 `cmake --install` 后添加 `--prefix <directory>`。

## 链接到应用程序 {#link-your-application}

安装 kiyosi 后，在应用程序的 CMake 配置中创建 `my_app` 目标，再添加以下配置：

```cmake
find_package(kiyosi CONFIG REQUIRED)
target_link_libraries(my_app PRIVATE kiyosi::kiyosi)
```

如果 CMake 找不到该包，请在配置应用程序时将 kiyosi 的安装前缀加入 `CMAKE_PREFIX_PATH`。

静态库的 `kiyosi::kiyosi` 目标会传递 oneTBB 链接依赖，消费方需能通过 `find_package(TBB 2023.1 CONFIG)` 找到它。即使 kiyosi 构建为静态库，运行应用程序时仍需 oneTBB 动态运行库。自动下载的 oneTBB 会随 kiyosi 一起安装；Windows 下需将运行库放在应用程序旁或加入 `PATH`。

在代码中包含统一入口头文件：

```cpp
#include <kiyosi/kiyosi.hpp>
```

[定价测试](https://github.com/lilkui/kiyosi/tree/main/tests/pricing)包含使用原生 API 为不同类型金融工具定价的示例。

核心库不依赖 Python 或 nanobind，可以独立构建、安装和使用。当前版本的 `price()` 返回 `Result<double>`。需要计算 Greeks 时，调用 `price_with_greeks()` 并传入 `GreeksRequest`。接口和线程安全约定见 [C++ API 参考](/api/cpp/)。

数值引擎的默认构造函数提供有效的默认配置。自定义配置通过返回 `Result<Engine>` 的工厂创建，例如 [`make_monte_carlo_vanilla_engine(settings)`](/api/cpp/pricing-engines-vanilla-monte-carlo#make-monte-carlo-vanilla-engine)；调用方须检查结果后再定价。二叉树、有限差分及累购、自动赎回蒙特卡洛引擎也使用各自的 `make_*_engine()` 工厂，在创建时验证设置。

模型参数和市场上下文的 `replace()` 分别接受 `BlackScholesMertonParameterChanges` 和 `PricingContextChanges`，返回已验证副本。产品历史也通过对应的 `replace()` 更新。完整声明见[市场上下文](/api/cpp/market-context)和[金融工具头文件索引](/api/cpp/)。

## 生成 Doxygen XML {#generate-doxygen-xml}

安装 Doxygen 后，可在单独的构建目录中生成 XML：

```sh
cmake -S . -B build/docs -DBUILD_TESTING=OFF -DKIYOSI_BUILD_DOCS=ON
cmake --build build/docs --target kiyosi-doxygen
```

入口文件为 `build/docs/docs/xml/index.xml`。启用 `KIYOSI_BUILD_DOCS` 后，默认构建也会生成 XML。生成 XML 无需编译核心库，也不需要 Graphviz 或 Python。此选项默认关闭，普通构建无需 Doxygen。Windows 下仍需先打开 Visual Studio Developer PowerShell。

本网站的 C++ API 页面由这些 XML 转换生成，内容对应 kiyosi 0.11.0。结构化产品头文件位于 `kiyosi/instruments/autocallable/`，对应引擎位于 `kiyosi/pricing/engines/autocallable/`。

来源：[kiyosi C++ 构建配置](https://github.com/lilkui/kiyosi/blob/main/CMakeLists.txt)和 [CMake 预设](https://github.com/lilkui/kiyosi/blob/main/CMakePresets.json)。
