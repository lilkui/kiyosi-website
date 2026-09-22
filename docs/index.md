---
layout: page
sidebar: false
title: Derivatives pricing, clearly expressed
description: A native C++23 core, a Python-first API, and a consistent approach to derivatives pricing.
---

<main class="kiyosi-home">
<section class="home-hero" aria-labelledby="hero-title">
<div>
<p class="eyebrow">Derivatives pricing library</p>
<h1 id="hero-title">Quantitative finance.<br><span>Clearly expressed.</span></h1>
<p class="hero-description">Price vanilla options, exotic instruments, and structured products with a C++23 core and a Python-first API.</p>
<div class="hero-actions">

[Get started](./guide/installation){.primary}
[Explore the API](./reference/python)

</div>
</div>
<div class="code-example vp-doc">
<p class="example-title">One interface, different engines</p>

```python
from kiyosi.pricing import (
    AnalyticVanillaEngine,
    MonteCarloVanillaEngine,
)

# Use the same option and market context.
analytic = AnalyticVanillaEngine()
result = analytic.price(option, context)

monte_carlo = MonteCarloVanillaEngine()
estimate = monte_carlo.price(option, context)
```

[See the complete pricing example →](./guide/first-price){.example-link}

</div>
</section>

<section class="home-start vp-doc" aria-label="Install kiyosi">
<div>
<h2>Start with Python.</h2>
<p>Python 3.11+ · Prebuilt x64 wheels for Windows and Linux</p>
</div>

```sh
python -m pip install kiyosi
```

</section>

<section class="home-paths" aria-labelledby="explore-title">
<h2 id="explore-title">From your first price to your next model.</h2>
<div class="path-grid">
<a href="./guide/first-price.html">
<h3>Price a European option <span aria-hidden="true">↗</span></h3>
<p>Define an instrument, set the market context, and calculate a price with the analytic Black-Scholes engine.</p>
</a>
<a href="./guide/engines.html">
<h3>Choose a pricing engine <span aria-hidden="true">↗</span></h3>
<p>Find the available methods for your instrument, from analytic formulas to CUDA-accelerated Monte Carlo.</p>
</a>
<a href="./reference/python.html">
<h3>Find your way around the API <span aria-hidden="true">↗</span></h3>
<p>Explore the three Python modules for instruments, market inputs, and pricing engines.</p>
</a>
<a href="./cpp/building.html">
<h3>Work directly in C++ <span aria-hidden="true">↗</span></h3>
<p>Build the native library with CMake and link it into your application through the exported target.</p>
</a>
</div>
</section>

<p class="home-note">Kiyosi is alpha software; APIs may change. Read about <a href="./guide/introduction.html#model-scope">model scope</a> before choosing an engine.</p>
</main>
