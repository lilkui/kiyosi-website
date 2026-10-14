---
layout: page
sidebar: false
title: 期权定价的模型、数值方法与 C++ 实现
description: 基于 Black-Scholes-Merton 模型，以解析法、二叉树、有限差分、积分和蒙特卡洛方法求解期权价格。C++23 核心，Python 接口，可选 CUDA 蒙特卡洛后端。
---

<main class="kiyosi-home">
<section class="home-hero" aria-labelledby="hero-title">
<div>
<p class="eyebrow">kiyosi · 开源衍生品定价库</p>
<h1 id="hero-title">期权定价，<br><span>模型与数值求解。</span></h1>
<p class="hero-description">以 Black-Scholes-Merton 模型为基础，将合约条款与市场参数转化为价格和风险敏感度。C++23 核心实现解析与数值定价，Python 接口覆盖普通期权、奇异期权及结构化产品。</p>
<div class="hero-actions">

[安装与配置](./guide/installation){.primary}
[Python API](./reference/python)

</div>
</div>
<div class="code-example vp-doc">
<p class="example-title">同一合约与市场参数，比较解析解和蒙特卡洛估计</p>

```python
from kiyosi.pricing import (
    AnalyticVanillaEngine,
    MonteCarloVanillaEngine,
)

# 使用相同的期权和市场上下文。
analytic = AnalyticVanillaEngine()
price = analytic.price(option, context)

monte_carlo = MonteCarloVanillaEngine()
estimate = monte_carlo.price(option, context)
```

[查看完整定价示例 →](./guide/first-price){.example-link}

</div>
</section>

<section class="home-start vp-doc" aria-label="安装 kiyosi">
<div>
<h2>安装 Python 接口</h2>
<p>Python 3.11+ · 提供 Windows 和 Linux x64 预编译 wheel 包</p>
</div>

```sh
python -m pip install kiyosi
```

</section>

<section class="home-paths" aria-labelledby="explore-title">
<h2 id="explore-title">模型假设、数值方法与工程实现</h2>
<div class="path-grid">
<a href="./guide/first-price.html">
<h3>Black-Scholes-Merton 解析定价 <span aria-hidden="true">↗</span></h3>
<p>在恒定无风险利率、股息率与波动率假设下，用闭式解计算欧式普通期权价格。合约定义行权价与期限，市场上下文提供现价、模型参数和估值时点。</p>
</a>
<a href="./guide/engines.html">
<h3>数值离散与随机模拟 <span aria-hidden="true">↗</span></h3>
<p>按产品选择 CRR 二叉树、有限差分、积分或蒙特卡洛方法。有限差分支持 Crank-Nicolson 格式；欧式普通期权的蒙特卡洛定价直接采样终值分布。比较结果时需区分近似误差与模拟误差。</p>
</a>
<a href="./reference/python.html">
<h3>风险敏感度与隐含参数求解 <span aria-hidden="true">↗</span></h3>
<p>合约、市场输入与定价引擎分别由三个 Python 模块定义。按需计算 Greeks，以价格差分求数值敏感度，并提供隐含波动率与隐含票息求解器。不可用的 Greeks 返回空值，区别于零敏感度。</p>
</a>
<a href="./cpp/building.html">
<h3>C++23 核心与计算后端 <span aria-hidden="true">↗</span></h3>
<p>原生核心可独立于 Python 构建，通过 CMake 导出目标接入应用。蒙特卡洛默认使用 CPU；启用 CUDA 的构建可在兼容的 NVIDIA GPU 与驱动环境下使用 CUDA 后端。</p>
</a>
</div>
</section>

<p class="home-note">定价测试以 QuantLib 独立生成的数值为基准，C++ 核心的构建与运行均不依赖 QuantLib。当前模型尚不支持波动率曲面与利率曲线，详见<a href="./guide/introduction.html#model-scope">模型适用范围</a>。本文档对应 Kiyosi 0.10.0；项目处于 Alpha 阶段，API 可能发生变化。</p>
</main>
