---
description: 了解 kiyosi 的功能、定价流程和当前模型的适用范围。
---

# 简介

Kiyosi 是一个开源衍生品定价库。它以 C++23 实现核心功能，并提供以 Python 为主要使用入口的 API，支持普通期权、奇异期权和结构化产品。

::: warning Alpha 阶段
目前 API 仍可能发生变化，不保证向后兼容。升级时请查阅 kiyosi 源码仓库。
:::

## 定价流程 {#how-pricing-fits-together}

一次定价计算由三个对象共同完成：

1. **金融工具（instrument）**：描述合约，包括行权价、日期和收益类型。
2. **市场上下文（market context）**：提供模型参数、标的现价和估值时点。
3. **定价引擎（engine）**：根据金融工具和市场上下文，使用指定方法计算价格。

引擎返回包含价格的结果对象。Kiyosi 也通过结果类型提供希腊字母风险指标（Greeks）。不同金融工具支持的定价方法有所不同，详见[定价引擎](./engines)。

## 模型适用范围 {#model-scope}

当前模型采用 Black-Scholes-Merton 参数，无风险利率、股息率和波动率均为常数。目前 API 尚不支持波动率曲面和利率曲线。

库中还提供交易日历和观察日程构建工具，包括上交所节假日安排。支持的产品涵盖欧式期权、美式期权、累购产品、凤凰产品及多种雪球结构。

## 结果验证 {#validation}

Kiyosi 的定价测试以 QuantLib 独立生成的数值作为基准。QuantLib 用于生成参考值和维护日历，C++ 核心库在构建和运行时均不依赖它。

## 从哪里开始 {#where-to-begin}

- [安装 Python 包](./installation)，快速开始定价。
- [完成首次定价](./first-price)，运行一个完整示例。
- [构建 C++ 库](../cpp/building)，直接使用原生 API。

来源：[kiyosi README](https://github.com/lilkui/kiyosi#readme)。Kiyosi 采用 [MIT 许可证](https://github.com/lilkui/kiyosi/blob/main/LICENSE.txt)。
