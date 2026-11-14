---
description: 使用 Cargo 构建 kiyosi Rust 核心、生成 rustdoc，并接入 Rust 应用。
---

# 构建 Rust 核心

核心 crate `kiyosi` 可独立于 Python 构建和使用。本文档对应 **kiyosi 0.19.0**，需要 **Rust 1.85+**（edition 2024）、Cargo 和本机链接工具。

## 获取源码

检出本文档对应的固定提交：

```sh
git clone https://github.com/lilkui/kiyosi.git
cd kiyosi
git checkout fb6ea0f626e81b4e62beff9d9c8027855e94b015
cargo build -p kiyosi --release --locked
cargo test -p kiyosi --locked
```

Cargo 首次构建需要下载锁文件指定的依赖。核心构建无需 Python 或 maturin。

## 接入应用

在应用的 `Cargo.toml` 中固定同一提交：

```toml
[dependencies]
kiyosi = { git = "https://github.com/lilkui/kiyosi.git", rev = "fb6ea0f626e81b4e62beff9d9c8027855e94b015" }
```

以下代码与 [Python 首次定价](../guide/first-price)使用相同的参数：

```rust
use kiyosi::{
    AnalyticEuropeanEngine, BlackScholesMertonParameters, Date,
    EuropeanOption, Greek, GreeksRequest, OptionType, PricingContext, PricingEngine,
};

fn main() -> kiyosi::Result<()> {
    let start = Date::new(2025, 1, 1)?.start_of_day();
    let expiry = Date::new(2026, 1, 1)?.start_of_day();
    let option = EuropeanOption::new(OptionType::Call, 100.0, start, expiry)?;
    let model = BlackScholesMertonParameters::new(0.05, 0.02, 0.2)?;
    let context = PricingContext::new(model, 100.0, start)?;
    let price = AnalyticEuropeanEngine.price(&option, &context)?;
    println!("Price: {price:.6}"); // 9.227006
    let result = PricingEngine::price_with_greeks(
        &AnalyticEuropeanEngine, &option, &context,
        GreeksRequest::new([Greek::Delta, Greek::Vega]),
    )?;
    println!("Delta: {:.6}", result.require(Greek::Delta)?); // 0.586851
    Ok(())
}
```

合约边界和估值时点使用 `Timestamp`，按调用方选定的同一时间基准解释；`Date::start_of_day()` 构造当天零点，`Date::at_time(TimeOfDay)` 可指定日内时刻。

领域错误通过 `kiyosi::Result` 返回。公开内置类型拥有自己的数据，并支持并发读取和定价；修改值需要独占访问。`replace()` 使用对应的 `*Changes` 类型创建经过验证的新值。完整约定见 <a href="../api/rust/kiyosi/index.html" target="_self">Rust API</a>。

## Greeks 与引擎设置

导入 `PricingEngine` trait 后，用 `price_with_greeks()` 请求指定指标，默认使用共享扰动设置。需要指定扰动时，将 `NumericalShiftSettings` 传给 `price_with_greeks_with_settings()`；`spot_shift`、`volatility_shift`、`rate_shift` 和 `time_shift` 属于本次请求。显式 BSM 标量差分使用 `numerical_greeks(engine, option, context, request, settings)`。

结果中的不可用指标为 `None`，通过 `status(Greek::...)` 查看原因，或通过 `require(Greek::...)` 获取数值并在不可用时返回错误。无受支持指标的请求仍返回价格和状态。

采样与网格通过各引擎的配置类型设置；`MonteCarloBarrierEngine` 同时为 `BarrierOption` 和 `DoubleBarrierOption` 定价。修改合约日历使用对应的 `*Changes` 中的 `calendar` 字段，经 `replace()` 重新验证条款和历史。

## 生成原生 API 文档

在 kiyosi 源码目录执行：

```sh
cargo doc -p kiyosi --no-deps --locked --open
```

入口为 `target/doc/kiyosi/index.html`。本网站托管同一提交生成的完整 rustdoc 目录，保留类型链接、源码和搜索资源。Python API 与 Rust API 的名称、接口和覆盖范围可能不同，使用时以各自参考文档为准。
