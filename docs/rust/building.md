---
description: 使用 Cargo 构建 kiyosi Rust 核心、生成 rustdoc，并接入 Rust 应用。
---

# 构建 Rust 核心

核心 crate `kiyosi` 可独立于 Python 构建和使用。本文档对应 **kiyosi 0.22.0**，需要 **Rust 1.85+**（edition 2024）、Cargo 和本机链接工具。

## 获取源码

检出本文档对应的固定提交：

```sh
git clone https://github.com/lilkui/kiyosi.git
cd kiyosi
git checkout d8413d14ab2f7a53ecc3df145d394bd3c5ba783e
cargo build -p kiyosi --release --locked
cargo test -p kiyosi --locked
```

首次构建时，Cargo 会下载锁文件指定的依赖，整个构建过程均由 Rust 工具链完成。

## 接入应用

在应用的 `Cargo.toml` 中固定同一提交：

```toml
[dependencies]
kiyosi = { git = "https://github.com/lilkui/kiyosi.git", rev = "d8413d14ab2f7a53ecc3df145d394bd3c5ba783e" }
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

领域错误通过 `kiyosi::Result` 返回。公开的内置类型持有自身数据，支持并发读取和定价；修改值需要独占访问。`replace()` 通过对应的 `*Changes` 类型创建并验证新值。完整约定见 <a href="../api/rust/kiyosi/index.html" target="_self">Rust API</a>。

## Greeks 与引擎设置

导入 `PricingEngine` trait 后，用 `price_with_greeks()` 请求指定指标，默认使用共享扰动设置。需要指定扰动时，将 `NumericalShiftSettings` 传给 `price_with_greeks_with_settings()`；`spot_shift`、`volatility_shift`、`rate_shift` 和 `time_shift` 仅作用于本次请求。若要显式使用 BSM 标量差分，调用 `numerical_greeks(engine, option, context, request, settings)`。

结果包含价格与各指标的状态。不可用指标为 `None`，通过 `status(Greek::...)` 查看原因；`require(Greek::...)` 返回指标数值，或在指标不可用时返回错误。

通过各引擎的配置类型设置采样与网格；`MonteCarloBarrierEngine` 可为 `BarrierOption` 和 `DoubleBarrierOption` 定价。修改合约日历时，设置对应 `*Changes` 类型中的 `calendar` 字段，再调用 `replace()` 重新验证条款和历史。

## 生成原生 API 文档

在 kiyosi 源码目录执行：

```sh
cargo doc -p kiyosi --no-deps --locked --open
```

入口为 `target/doc/kiyosi/index.html`。本网站也提供同一提交生成的 <a href="../api/rust/kiyosi/index.html" target="_self">Rust API 参考</a>，包含类型、trait、实现、源码链接和搜索。Python 调用方式见 [Python API 参考](/api/python/)。
