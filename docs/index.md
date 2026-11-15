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
<h2>广泛的产品覆盖</h2>
<p>支持普通期权、数字期权、亚式期权和障碍期权，以及国内市场常见的雪球、凤凰、累购和累沽等奇异期权结构。</p>

</article>
<article>
<h2>多种定价方法</h2>
<p>提供解析法、二叉树、数值积分、有限差分和蒙特卡洛方法，便于对同一合约交叉验证价格与 Greeks。</p>

</article>
<article>
<h2>Rust 核心，Python 接口</h2>
<p>通过 Python 构建合约、配置市场输入，由 Rust 核心完成定价。核心库也可直接接入 Rust 应用。</p>

</article>
</section>

</main>
