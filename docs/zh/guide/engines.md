---
description: 按金融工具类型比较 kiyosi 的定价方法，并选择 CPU 或 CUDA 蒙特卡洛后端。
---

# 定价引擎

请根据金融工具选择支持它的引擎。统一的 `price(instrument, context)` 接口并不意味着每个引擎都能为所有产品定价。

## 支持的产品与方法 {#instrument-coverage}

| 产品类型 | 可用定价方法 |
| --- | --- |
| 欧式普通期权 | 解析法、CRR 二叉树法、有限差分法、积分法、蒙特卡洛法 |
| 美式普通期权 | Bjerksund-Stensland 近似、CRR 二叉树法、有限差分法、蒙特卡洛法 |
| 现金或无、资产或无数字期权 | 解析法、有限差分法、积分法 |
| 障碍期权 | 解析法、有限差分法 |
| 二元障碍期权和触碰期权 | 解析法 |
| 几何平均亚式期权 | 闭式解 |
| 算术平均亚式期权 | Turnbull-Wakeman 近似 |
| 累购产品 | 有限差分法、蒙特卡洛法 |
| 凤凰产品和各类雪球结构 | 有限差分法、蒙特卡洛法 |

上表依据 [kiyosi 定价支持矩阵](https://github.com/lilkui/kiyosi#pricing-coverage)整理。API 仍处于 Alpha 阶段，支持范围的变化请以源码仓库为准。

## 选择计算后端 {#select-a-backend}

蒙特卡洛引擎默认使用 CPU。如需使用 CUDA，可沿用[首次定价](./first-price)中的 `option` 和 `context`：

```python
from kiyosi.pricing import MonteCarloBackend, MonteCarloVanillaEngine

engine = MonteCarloVanillaEngine(backend=MonteCarloBackend.CUDA)
result = engine.price(option, context)
print(result.price)
```

CUDA 需要兼容的 NVIDIA GPU 和驱动。它仅作为蒙特卡洛方法的计算后端；选择 CUDA 不会让解析引擎或有限差分引擎转到 GPU 上运行。

## 如何比较定价方法 {#compare-methods-carefully}

比较不同引擎时，应保持合约条款和市场输入一致。解析法直接计算公式，而数值方法会引入近似误差或模拟误差。各引擎的具体设置可查阅[定价模块](https://github.com/lilkui/kiyosi/blob/main/python/kiyosi/pricing.py)和[源码示例](https://github.com/lilkui/kiyosi/tree/main/examples)。

当前所有模型均受 [Black-Scholes-Merton 模型适用范围](./introduction#model-scope)的限制。
