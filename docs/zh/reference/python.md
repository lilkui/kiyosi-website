---
description: 了解 kiyosi 的 instruments、market 和 pricing 三个 Python 模块。
---

# Python API 概览

所有公开导出对象的签名、成员、异常和文档字符串均可在[完整 Python API 参考（英文）](/api/python/)中查阅。自动生成的 API 参考保留英文，与源码文档保持一致。

Kiyosi 的公开 Python API 主要分为三个模块。本页帮助你了解各模块的用途；最新导出列表请查阅下方链接中的源码。

## `kiyosi.instruments`

此模块提供合约定义和结构化产品预设。[首次定价示例](../guide/first-price)通过 `EuropeanOption` 和 `OptionType` 定义看涨期权。

支持的产品包括普通期权、数字期权、亚式期权、障碍期权、累购产品、凤凰产品和雪球产品。选择定价方法前，请先确认[引擎支持范围](../guide/engines#instrument-coverage)。

[查看 instruments 模块源码 →](https://github.com/lilkui/kiyosi/blob/main/python/kiyosi/instruments.py)

## `kiyosi.market`

此模块提供市场输入、估值上下文、日历和观察日程。

`BlackScholesMertonParameters` 保存恒定的无风险利率、股息率和波动率。`PricingContext` 将这些模型参数与 `spot_price`、`valuation_time` 组合为定价所需的市场上下文。

[查看 market 模块源码 →](https://github.com/lilkui/kiyosi/blob/main/python/kiyosi/market.py)

## `kiyosi.pricing`

此模块提供定价引擎、数值分析工具、情景分析和隐含值求解器。

欧式看涨期权示例使用 `AnalyticVanillaEngine`。也可以使用基于模拟的 `MonteCarloVanillaEngine`，并通过 `MonteCarloBackend` 选择计算后端。两者均调用 `price(option, context)`，返回的对象都包含 `price` 成员。

[查看 pricing 模块源码 →](https://github.com/lilkui/kiyosi/blob/main/python/kiyosi/pricing.py)

## 实用示例 {#working-examples}

- [首次定价](../guide/first-price)：完整的 Python 脚本。
- [选择计算后端](../guide/engines#select-a-backend)：CUDA 配置示例。
- [源码示例](https://github.com/lilkui/kiyosi/tree/main/examples)：更多产品和引擎的用法。

::: info API 稳定性
API 仍处于 Alpha 阶段。kiyosi 包更新后，应重新生成完整 API 参考。
:::
