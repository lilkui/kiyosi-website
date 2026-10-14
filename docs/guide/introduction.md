---
description: 了解 kiyosi 的功能、定价流程和当前模型的适用范围。
---

# 简介

Kiyosi 是一个开源衍生品定价库，支持普通期权、奇异期权和结构化产品。核心功能用 C++23 实现，主要通过 Python API 使用。

::: warning 早期开发阶段
本文档对应 **kiyosi 0.10.0**。项目处于 Alpha 阶段，API 可能发生变化，不保证向后兼容。
:::

## 定价流程 {#how-pricing-fits-together}

定价需要三个对象：

1. **金融工具**：描述合约，包括行权价、日期和收益类型。
2. **市场上下文**：提供模型参数、标的现价和估值时点。
3. **定价引擎**：根据金融工具和市场上下文，使用指定方法计算价格。

Python 的 `price()` 直接返回价格数值。需要计算希腊字母风险指标（Greeks）时，调用 `price_with_greeks()` 并指定指标；该方法返回的 `PricingResult` 包含价格和所选 Greeks。

不同金融工具支持的定价方法不同，详见[定价引擎](./engines)。

## 模型适用范围 {#model-scope}

当前模型采用 Black-Scholes-Merton 参数，无风险利率、股息率和波动率均为常数。API 尚不支持波动率曲面和利率曲线。

库中还提供交易日历和观察日程构建工具，包含上交所节假日安排。支持的产品包括欧式期权、美式期权、累购产品、凤凰产品及多种雪球结构。

## 结果验证 {#validation}

Kiyosi 的定价测试以 QuantLib 独立生成的数值为基准。QuantLib 用于生成参考值和维护日历；C++ 核心库的构建和运行均不依赖 QuantLib。

## 从哪里开始 {#where-to-begin}

- [安装 Python 包](./installation)，快速开始定价。
- [完成首次定价](./first-price)，运行一个完整示例。
- [构建 C++ 库](../cpp/building)，直接使用原生 API。

来源：[kiyosi README](https://github.com/lilkui/kiyosi/blob/main/README.md)。Kiyosi 采用 [MIT 许可证](https://github.com/lilkui/kiyosi/blob/main/LICENSE.txt)。
