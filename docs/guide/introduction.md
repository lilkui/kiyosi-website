---
description: 了解 kiyosi 的定价流程、模型、产品与验证方式。
---

# 简介

kiyosi 是一个开源衍生品定价库，支持普通期权、奇异期权和结构化产品。核心功能用 Rust 实现，主要通过 Python API 使用。

本文档对应 **kiyosi 0.20.0**，源码提交为 `be67a24`，项目处于 Alpha 开发阶段。

## 定价流程 {#how-pricing-fits-together}

定价需要三个对象：

1. **金融工具**：描述合约，包括行权价、日期和收益类型。
2. **市场上下文**：提供模型参数、标的现价和估值时点。
3. **定价引擎**：根据金融工具和市场上下文，使用指定方法计算价格。

Python 的 `price()` 直接返回价格数值；需要计算希腊字母风险指标（Greeks）时，调用 `price_with_greeks()` 指定所需指标，返回的 `PricingResult` 包含价格和所选 Greeks。

不同金融工具支持的定价方法不同，详见[定价引擎](./engines)。

## 模型与产品 {#model-scope}

`BlackScholesMertonParameters` 使用非负恒定波动率；零波动率对应确定性定价。无风险利率和股息率可使用常数，或用 `RateTermStructure` 表示确定性期限结构。BSM、局部波动率和 Heston 参数均支持通过 `time_convention` 和 `calendar` 指定波动率及方差时钟（一维有限差分支持 `"business"` 交易日历时间与利率自然时间双时钟定价）。

`LocalVolatilitySurface` 和 `LocalVolatilityParameters` 用时间与绝对标的价格网格描述局部波动率。一维有限差分引擎可计算该模型的价格，以及固定曲面下的 delta 和 gamma；自动赎回有限差分还支持隐含票息求解。模型条件与用法见[局部波动率](../reference/python#local-volatility)。

`HestonParameters` 描述风险中性下的随机波动率模型，支持确定性利率与股息率曲线。`AnalyticHestonEuropeanEngine` 通过 Fourier 积分计算欧式普通期权价格；`FiniteDifferenceHestonVanillaEngine` 通过二维有限差分计算欧式与美式普通期权价格。用法见 [Heston 模型](../reference/python#heston)。

库中还提供交易日历和观察日程构建工具，包含上交所节假日安排。支持的产品包括欧式期权、美式期权、累购／累沽、凤凰、固定票息票据（FCN）、数字票息票据（DCN）及多种雪球结构。

## 结果验证 {#validation}

kiyosi 的定价测试以 QuantLib 独立生成的数值为基准。QuantLib 用于生成参考值和维护日历；Rust 核心库可独立构建和运行。

## 从哪里开始 {#where-to-begin}

- [安装 Python 包](./installation)，准备定价环境。
- [完成首次定价](./first-price)，运行一个完整示例。
- [构建 Rust 核心](../rust/building)，直接使用原生 API。

来源：[kiyosi README](https://github.com/lilkui/kiyosi/blob/be67a2427fbf3cb14de6d7e03c83eff2473d0c28/README.md)。kiyosi 采用 [MIT 许可证](https://github.com/lilkui/kiyosi/blob/be67a2427fbf3cb14de6d7e03c83eff2473d0c28/LICENSE.txt)。
