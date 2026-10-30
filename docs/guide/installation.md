---
description: 安装 kiyosi Python 包，或使用 Rust 和 maturin 从固定源码构建。
---

# 安装

## Python 环境要求 {#python-requirements}

需要 **Python 3.11+**。本网站对应 **kiyosi 0.14.0**。建议在虚拟环境中安装固定版本：

::: code-group

```sh [Linux / macOS]
python3 -m venv .venv
source .venv/bin/activate
python -m pip install "kiyosi==0.14.0"
```

```powershell [Windows]
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install "kiyosi==0.14.0"
```

:::

有匹配平台的预编译 wheel 时，安装无需 Rust。上游 wheel 构建配置覆盖 Python 3.11–3.15；具体可用文件以该版本发布结果为准。

安装后确认版本和入口：

```sh
python -c "import kiyosi; from kiyosi.pricing import AnalyticEuropeanEngine; print(kiyosi.__version__)"
```

导入成功后，可以运行[首次定价](./first-price)示例。

## 从源码构建 {#building-from-source}

没有匹配的 wheel 时，需要 **Rust 1.85+**、Cargo，以及本机编译和链接工具。Linux 通常使用系统编译工具；Windows 使用 Visual Studio 的 C++ Build Tools 与 MSVC Rust 工具链。Python 包通过 maturin 构建，绑定由 PyO3 提供。

如需安装与本文档完全对应的源码：

```sh
git clone https://github.com/lilkui/kiyosi.git
cd kiyosi
git checkout 748942203c99ffb5f011dbdcd06312d6b5f4a06c
python -m pip install .
python -c "import kiyosi; print(kiyosi.__version__)"  # 0.14.0
```

pip 自动安装构建所需的 maturin，并由 Cargo 使用源码中的锁文件构建 Rust 扩展。首次构建需要联网下载依赖。若只使用 Rust，请参阅[构建 Rust 核心](../rust/building)。

## 常见问题 {#troubleshooting}

| 问题 | 排查方法 |
| --- | --- |
| `ModuleNotFoundError: No module named 'kiyosi'` | 确认安装包和运行脚本使用同一 Python 解释器，并激活虚拟环境。 |
| pip 开始编译原生代码 | 当前平台可能没有匹配的 wheel；准备 Rust/Cargo 和本机链接工具。 |
| 找不到 Cargo 或链接器 | 检查 `cargo --version`，确保本机编译工具可在终端调用。 |
| 示例找不到引擎名 | 检查安装版本是否为 0.14.0，使用本版本参考页中的公开名称。 |

来源：[kiyosi 安装说明](https://github.com/lilkui/kiyosi/blob/748942203c99ffb5f011dbdcd06312d6b5f4a06c/README.md#安装)、[构建配置](https://github.com/lilkui/kiyosi/blob/748942203c99ffb5f011dbdcd06312d6b5f4a06c/pyproject.toml)。
