---
description: Install kiyosi for Python, understand wheel availability, and prepare for CUDA or source builds.
---

# Installation

## Python requirements

Use **Python 3.11 or newer**. PyPI provides prebuilt x64 wheels for Windows and Linux.

Create an isolated environment before installing:

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

Confirm that Python can import the package:

```sh
python -c "from kiyosi.pricing import AnalyticVanillaEngine; print('kiyosi is ready')"
```

Then follow [Your first price](./first-price).

## CUDA acceleration

The Windows and Linux x64 wheels include CUDA acceleration for Monte Carlo engines. CPU is the default backend. To use CUDA, you need a compatible NVIDIA GPU and driver and must select the CUDA backend explicitly.

See [Select a backend](./engines#select-a-backend) for the engine configuration.

## Building from source

On platforms without a prebuilt wheel, installation builds from source. You need CMake 3.28+, Ninja, and a C++23-capable compiler. Consult the [upstream build configuration](https://github.com/lilkui/kiyosi/blob/main/CMakeLists.txt) for current toolchain requirements.

For native C++ development, follow [Build the C++ library](../cpp/building).

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| `ModuleNotFoundError: No module named 'kiyosi'` | Run installation with the same Python interpreter used for your script. Activate your virtual environment first. |
| pip starts a native build | Check the Python version and platform architecture. A matching prebuilt wheel may not be available. |
| A source build cannot find CMake or a compiler | Install the source-build prerequisites and make them available in your shell. |
| CUDA pricing fails | Check the NVIDIA driver and GPU compatibility. Use the default CPU backend to verify the basic pricing setup. |

Sources: [upstream installation notes](https://github.com/lilkui/kiyosi#quick-start-with-python), [PyPI package](https://pypi.org/project/kiyosi/).
