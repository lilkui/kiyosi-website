---
layout: page
sidebar: false
title: 让衍生品定价清晰易用
description: 以 C++23 为核心，以 Python 为主要接口，用一致的方式为衍生品定价。
---

<main class="kiyosi-home">
<section class="home-hero" aria-labelledby="hero-title">
<div>
<p class="eyebrow">衍生品定价库</p>
<h1 id="hero-title">量化金融，<br><span>清晰表达。</span></h1>
<p class="hero-description">以 C++23 为核心，提供易于使用的 Python API，为普通期权、奇异期权和结构化产品定价。</p>
<div class="hero-actions">

[快速上手](./guide/installation){.primary}
[了解 API](./reference/python)

</div>
</div>
<div class="code-example vp-doc">
<p class="example-title">统一接口，灵活切换引擎</p>

```python
from kiyosi.pricing import (
    AnalyticVanillaEngine,
    MonteCarloVanillaEngine,
)

# 使用相同的期权和市场上下文。
analytic = AnalyticVanillaEngine()
result = analytic.price(option, context)

monte_carlo = MonteCarloVanillaEngine()
estimate = monte_carlo.price(option, context)
```

[查看完整定价示例 →](./guide/first-price){.example-link}

</div>
</section>

<section class="home-start vp-doc" aria-label="安装 kiyosi">
<div>
<h2>从 Python 开始。</h2>
<p>Python 3.11+ · 提供 Windows 和 Linux x64 预编译 wheel 包</p>
</div>

```sh
python -m pip install kiyosi
```

</section>

<section class="home-paths" aria-labelledby="explore-title">
<h2>从首次定价，到探索更多模型。</h2>
<div class="path-grid">
<a href="./guide/first-price.html">
<h3>为欧式期权定价 <span aria-hidden="true">↗</span></h3>
<p>定义金融工具，设置市场上下文，使用 Black-Scholes 解析引擎计算价格。</p>
</a>
<a href="./guide/engines.html">
<h3>选择定价引擎 <span aria-hidden="true">↗</span></h3>
<p>从解析公式到 CUDA 加速的蒙特卡洛模拟，找到适合产品的定价方法。</p>
</a>
<a href="./reference/python.html">
<h3>了解 API 结构 <span aria-hidden="true">↗</span></h3>
<p>熟悉金融工具、市场输入和定价引擎对应的三个 Python 模块。</p>
</a>
<a href="./cpp/building.html">
<h3>直接使用 C++ <span aria-hidden="true">↗</span></h3>
<p>通过 CMake 构建原生库，并使用导出的目标将其链接到应用程序。</p>
</a>
</div>
</section>

<p class="home-note">Kiyosi 仍处于 Alpha 阶段，API 可能发生变化。选择引擎前，请先了解<a href="./guide/introduction.html#model-scope">模型适用范围</a>。</p>
</main>
