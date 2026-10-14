---
description: 安装 kiyosi Python 包，了解预编译 wheel 的支持范围，以及 CUDA 和源码构建的要求。
---

# 安装

## Python 环境要求 {#python-requirements}

需要 **Python 3.11 或更高版本**。当前源码配置了 Python 3.11–3.15 的 wheel 构建，目标平台为 Windows 和 Linux x64。本网站的 API 参考对应 kiyosi 0.10.0。

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

安装后，确认能正常导入 kiyosi：

```sh
python -c "from kiyosi.pricing import AnalyticVanillaEngine; print('kiyosi 已就绪')"
```

导入成功后，可以运行[首次定价](./first-price)示例。

## CUDA 加速 {#cuda-acceleration}

项目的 Windows 和 Linux x64 wheel 构建配置启用了蒙特卡洛引擎的 CUDA 支持，但定价时默认使用 CPU 后端。使用 CUDA 需要兼容的 NVIDIA GPU 和驱动，还需显式设置 `backend="cuda"`。自行从源码构建时，CUDA 默认关闭。

配置方法见[选择计算后端](./engines#select-a-backend)。

## 从源码构建 {#building-from-source}

如果当前平台没有可用的预编译 wheel，安装时会从源码构建，需要 CMake 3.28 或更高版本、Ninja，以及支持 C++23 的编译器。最新工具链要求见 [kiyosi 构建配置](https://github.com/lilkui/kiyosi/blob/main/CMakeLists.txt)。

如需安装与本文档对应的开发版本，可检出相应的源码提交后安装：

```sh
git clone https://github.com/lilkui/kiyosi.git
cd kiyosi
git checkout 7e2f3e3
python -m pip install .
python -c "import kiyosi; print(kiyosi.__version__)"  # 0.10.0
```

Windows 下请在 Visual Studio Developer PowerShell 中执行源码构建命令。从 PyPI 安装后，也请用上面的版本检查命令确认实际安装的版本。

如需直接使用 C++，请参阅[构建 C++ 库](../cpp/building)。

## 常见问题 {#troubleshooting}

| 问题 | 排查方法 |
| --- | --- |
| `ModuleNotFoundError: No module named 'kiyosi'` | 确认安装包和运行脚本使用的是同一个 Python 解释器，并先激活虚拟环境。 |
| pip 开始编译原生代码 | 检查 Python 版本和平台架构，可能没有匹配的预编译 wheel。 |
| 源码构建找不到 CMake 或编译器 | 安装所需构建工具，并确保能在当前终端中调用。 |
| CUDA 定价失败 | 检查 NVIDIA 驱动和 GPU 的兼容性。先使用默认 CPU 后端，确认基本定价配置能正常工作。 |

来源：[kiyosi 安装说明](https://github.com/lilkui/kiyosi/blob/main/README.md#安装-python-包)、[PyPI 包页面](https://pypi.org/project/kiyosi/)。
