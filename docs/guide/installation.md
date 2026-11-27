---
description: 安装 kiyosi Python 包，或使用 Rust 和 maturin 从固定源码构建。
---

# 安装

## Python 环境要求 {#python-requirements}

使用 **Python 3.12+**，在虚拟环境中安装本文档对应的 **kiyosi 0.23.0**：

::: code-group

```sh [Linux / macOS]
python3 -m venv .venv
source .venv/bin/activate
python -m pip install "kiyosi==0.23.0"
```

```powershell [Windows]
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install "kiyosi==0.23.0"
```

:::

PyPI 提供采用 `abi3-py312` 稳定 ABI 的 CPython wheel，支持 Windows x86-64 和 Linux x86-64（glibc 2.28+）。pip 在平台与解释器匹配时直接安装 wheel。macOS 等其他平台需要按下节准备源码构建环境。发布文件见 [PyPI](https://pypi.org/project/kiyosi/0.23.0/#files)。

安装后，确认包版本并检查能否导入定价引擎：

```sh
python -c "import kiyosi; from kiyosi.pricing import AnalyticEuropeanEngine; print(kiyosi.__version__)"
```

导入成功后，可以运行[首次定价](./first-price)示例。

## 从源码构建 {#building-from-source}

源码构建需要 **Rust 1.85+**、Cargo，以及本机编译和链接工具。Linux 通常使用系统编译工具；Windows 使用 Visual Studio 的 C++ Build Tools 与 MSVC Rust 工具链。Python 包通过 maturin 构建，绑定由 PyO3 提供。

检出本文档对应的提交并安装：

```sh
git clone https://github.com/lilkui/kiyosi.git
cd kiyosi
git checkout 9231574344cbc2173d3ccdea1e52f4cf749504ed
python -m pip install .
python -c "import kiyosi; print(kiyosi.__version__)"  # 0.23.0
```

pip 会自动安装构建所需的 maturin，Cargo 按源码中的锁文件构建 Rust 扩展。首次构建需要联网下载依赖。若只使用 Rust，请参阅[构建 Rust 核心](../rust/building)。

## 常见问题 {#troubleshooting}

| 问题 | 排查方法 |
| --- | --- |
| `ModuleNotFoundError: No module named 'kiyosi'` | 确认安装包和运行脚本使用同一 Python 解释器，并激活虚拟环境。 |
| pip 开始编译原生代码 | pip 正在从源码安装；准备 Rust/Cargo 和本机编译、链接工具。 |
| 找不到 Cargo 或链接器 | 检查 `cargo --version`，确保本机编译工具可在终端调用。 |
| 示例找不到引擎名 | 用 `python -c "import kiyosi; print(kiyosi.__version__)"` 检查版本，并核对[定价 API](/api/python/kiyosi-pricing)中的名称与导入路径。 |

来源：[kiyosi 安装说明](https://github.com/lilkui/kiyosi/blob/9231574344cbc2173d3ccdea1e52f4cf749504ed/README.md#安装)、[构建配置](https://github.com/lilkui/kiyosi/blob/9231574344cbc2173d3ccdea1e52f4cf749504ed/pyproject.toml)。
