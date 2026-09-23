---
description: 安装 kiyosi Python 包，了解预编译 wheel 的支持范围，以及 CUDA 和源码构建的要求。
---

# 安装

## Python 环境要求 {#python-requirements}

请使用 **Python 3.11 或更高版本**。PyPI 提供适用于 Windows 和 Linux 的 x64 预编译 wheel 包。

建议先创建虚拟环境，再安装：

::: code-group

```sh [Linux / macOS]
python3 -m venv .venv
source .venv/bin/activate
python -m pip install kiyosi
```

```powershell [Windows]
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install kiyosi
```

:::

确认 Python 能正常导入：

```sh
python -c "from kiyosi.pricing import AnalyticVanillaEngine; print('kiyosi is ready')"
```

接下来可以尝试[首次定价](./first-price)。

## CUDA 加速 {#cuda-acceleration}

Windows 和 Linux 的 x64 wheel 包内置了蒙特卡洛引擎的 CUDA 加速支持。默认使用 CPU 后端；如需使用 CUDA，须配备兼容的 NVIDIA GPU 和驱动，并显式选择 CUDA 后端。

配置方法见[选择计算后端](./engines#select-a-backend)。

## 从源码构建 {#building-from-source}

如果当前平台没有可用的预编译 wheel，安装过程会从源码构建。此时需要 CMake 3.28 或更高版本、Ninja，以及支持 C++23 的编译器。最新工具链要求请参阅 [kiyosi 构建配置](https://github.com/lilkui/kiyosi/blob/main/CMakeLists.txt)。

如需直接使用 C++ 开发，请参阅[构建 C++ 库](../cpp/building)。

## 常见问题 {#troubleshooting}

| 问题 | 排查方法 |
| --- | --- |
| `ModuleNotFoundError: No module named 'kiyosi'` | 确认安装包和运行脚本使用的是同一个 Python 解释器，并先激活虚拟环境。 |
| pip 开始编译原生代码 | 检查 Python 版本和平台架构，可能没有匹配的预编译 wheel。 |
| 源码构建找不到 CMake 或编译器 | 安装所需构建工具，并确保能在当前终端中调用。 |
| CUDA 定价失败 | 检查 NVIDIA 驱动和 GPU 的兼容性。先使用默认 CPU 后端，确认基本定价配置能正常工作。 |

来源：[kiyosi 安装说明](https://github.com/lilkui/kiyosi#quick-start-with-python)、[PyPI 包页面](https://pypi.org/project/kiyosi/)。
