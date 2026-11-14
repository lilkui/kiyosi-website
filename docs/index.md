---
layout: page
sidebar: false
title: 开源衍生品定价库
description: kiyosi 是以 Rust 为核心、提供 Python 接口的开源衍生品定价库，支持普通期权、奇异期权和结构化产品的定价与风险计算。
---

<main class="kiyosi-home">
<section class="home-hero" aria-labelledby="hero-title">
<h1 id="hero-title">kiyosi</h1>
<p class="hero-description">开源衍生品定价库</p>
<div class="hero-actions">

[开始使用](./guide/installation){.primary}
[API 参考](./api/){.secondary}

</div>
</section>

<section id="features" class="home-features" aria-label="核心特性">
<article>
<h2>多种定价方法</h2>
<p>支持解析法、二叉树、有限差分、积分与蒙特卡洛，可按产品与模型条件选择引擎。</p>

[了解定价引擎](./guide/engines)

</article>
<article>
<h2>价格与风险敏感度</h2>
<p>按需计算 Greeks 与数值敏感度，求解隐含波动率和隐含票息。</p>

[查阅 Python API](./reference/python)

</article>
<article>
<h2>Rust 核心，Python 接口</h2>
<p>通过 Python 定义合约、提供市场输入，由 Rust 执行计算。原生核心也可独立接入 Rust 应用。</p>

[构建 Rust 核心](./rust/building)

</article>
</section>

</main>
