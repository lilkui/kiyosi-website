---
description: 使用 Cargo 构建 kiyosi Rust 核心、生成 rustdoc，并接入 Rust 应用。
---

# 构建 Rust 核心

核心 crate `kiyosi-core` 可独立于 Python 构建和使用。需要 **Rust 1.85+**（edition 2024）、Cargo 和本机链接工具。

## 获取源码

检出本文档对应的固定提交：

```sh
git clone https://github.com/lilkui/kiyosi.git
cd kiyosi
git checkout 748942203c99ffb5f011dbdcd06312d6b5f4a06c
cargo build -p kiyosi-core --release --locked
cargo test -p kiyosi-core --locked
```

Cargo 首次构建需要下载锁文件指定的依赖。核心构建无需 Python 或 maturin。

## 接入应用

在应用的 `Cargo.toml` 中固定同一提交：

```toml
[dependencies]
kiyosi-core = { git = "https://github.com/lilkui/kiyosi.git", rev = "748942203c99ffb5f011dbdcd06312d6b5f4a06c" }
```

以下代码与 [Python 首次定价](../guide/first-price)使用相同的参数：

```rust
use kiyosi_core::{
    AnalyticEuropeanEngine, BlackScholesMertonParameters, Date,
    EuropeanOption, OptionType, PricingContext,
};

fn main() -> kiyosi_core::Result<()> {
    let start = Date::new(2025, 1, 1)?;
    let expiry = Date::new(2026, 1, 1)?;
    let option = EuropeanOption::new(OptionType::Call, 100.0, start, expiry)?;
    let model = BlackScholesMertonParameters::new(0.05, 0.02, 0.2)?;
    let context = PricingContext::new(model, 100.0, start.into())?;
    let price = AnalyticEuropeanEngine.price(&option, &context)?;
    println!("Price: {price:.6}"); // 9.227006
    Ok(())
}
```

领域错误通过 `kiyosi_core::Result` 返回。公开内置类型拥有自己的数据，并支持并发读取和定价；修改值需要独占访问。完整约定见 <a href="../api/rust/kiyosi_core/index.html" target="_self">Rust API</a>。

## 生成原生 API 文档

在 kiyosi 源码目录执行：

```sh
cargo doc -p kiyosi-core --no-deps --locked --open
```

入口为 `target/doc/kiyosi_core/index.html`。本网站托管同一提交生成的完整 rustdoc 目录，保留类型链接、源码和搜索资源。Python API 与 Rust API 的名称、接口和覆盖范围可能不同，使用时以各自参考文档为准。
