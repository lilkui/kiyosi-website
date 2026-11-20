<template>
  <figure class="fd-diagram" role="img" aria-labelledby="fd-fig-dual-pde-title">
    <svg viewBox="0 0 860 390" xmlns="http://www.w3.org/2000/svg">
      <title id="fd-fig-dual-pde-title">每日敲入自动赎回结构的双层 PDE 后向推进与状态耦合架构</title>
      <defs>
        <marker id="fd-arr-teal" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 1 1.5 L 8.5 5 L 1 8.5 z" fill="var(--fd-teal)" />
        </marker>
        <marker id="fd-arr-crimson" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 1 1.5 L 8.5 5 L 1 8.5 z" fill="var(--fd-crimson)" />
        </marker>
        <marker id="fd-arr-back" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 1 1.5 L 8.5 5 L 1 8.5 z" fill="var(--fd-ink)" />
        </marker>
      </defs>

      <!-- Top Backward Time Banner -->
      <line x1="790" y1="26" x2="188" y2="26" stroke="var(--fd-ink)" stroke-width="1.8" marker-end="url(#fd-arr-back)" />
      <text x="490" y="18" text-anchor="middle" font-size="12" font-weight="650" fill="var(--fd-ink)">
        PDE 后向时间回溯方向：由到期日 <tspan class="fd-math">T</tspan> 逆推至方差起点 <tspan class="fd-math">t</tspan><tspan dy="3" font-size="9">start</tspan><tspan dy="-3">，再经确定性前缀折算至估值时刻 </tspan><tspan class="fd-math">t</tspan><tspan dy="3" font-size="9">val</tspan>
      </text>

      <!-- Deterministic prefix box [t_val, t_start] on far left -->
      <rect x="34" y="54" width="132" height="270" rx="6" fill="var(--fd-panel-alt)" stroke="var(--fd-faint)" stroke-width="1.4" stroke-dasharray="5 3" />
      <text x="100" y="78" text-anchor="middle" font-size="12" font-weight="650" fill="var(--fd-ink)">确定性零方差前缀</text>
      <text x="100" y="96" text-anchor="middle" font-size="11" fill="var(--fd-muted)">
        [<tspan class="fd-math">t</tspan><tspan dy="3" font-size="8.5">val</tspan><tspan dy="-3">, </tspan><tspan class="fd-math">t</tspan><tspan dy="3" font-size="8.5">start</tspan><tspan dy="-3">]</tspan>
      </text>
      <text x="100" y="126" text-anchor="middle" font-size="10.8" fill="var(--fd-muted)">沿远期路径 F(t) 精确</text>
      <text x="100" y="143" text-anchor="middle" font-size="10.8" fill="var(--fd-muted)">判定敲出 / 派息 / 敲入</text>
      <line x1="52" y1="162" x2="148" y2="162" stroke="var(--fd-grid)" />
      <text x="100" y="184" text-anchor="middle" font-size="10.8" fill="var(--fd-teal)" font-weight="600">未敲入 → 取样 V⁽⁰⁾</text>
      <text x="100" y="204" text-anchor="middle" font-size="10.8" fill="var(--fd-crimson)" font-weight="600">已敲入 → 取样 V⁽¹⁾</text>
      <text x="100" y="224" text-anchor="middle" font-size="10.8" fill="var(--fd-muted)">已敲出 → 直接结算</text>
      <line x1="52" y1="242" x2="148" y2="242" stroke="var(--fd-grid)" />
      <text x="100" y="264" text-anchor="middle" font-size="10.5" fill="var(--fd-muted)">三次样条提取延续值</text>
      <text x="100" y="281" text-anchor="middle" font-size="10.5" fill="var(--fd-muted)">+ 贴现缩放现货 Greeks</text>
      <text x="100" y="308" text-anchor="middle" font-size="10.5" fill="var(--fd-ink)" font-weight="600">
        输出 V(<tspan class="fd-math">t</tspan><tspan dy="3" font-size="8.5">val</tspan><tspan dy="-3">, S₀)</tspan>
      </text>

      <!-- ================= LAYER 0 & LAYER 1 BACKGROUNDS ================= -->
      <rect x="186" y="54" width="606" height="112" rx="6" fill="var(--fd-teal-soft)" stroke="var(--fd-teal)" stroke-width="1.5" />
      <rect x="186" y="212" width="606" height="112" rx="6" fill="var(--fd-crimson-soft)" stroke="var(--fd-crimson)" stroke-width="1.5" />

      <!-- Internal barrier horizontal guides inside Layer 0 & Layer 1 -->
      <line x1="186" y1="98" x2="792" y2="98" stroke="var(--fd-teal)" stroke-width="1" stroke-dasharray="4 3" opacity="0.65" />
      <line x1="186" y1="136" x2="792" y2="136" stroke="var(--fd-crimson)" stroke-width="1.1" stroke-dasharray="4 3" opacity="0.75" />
      <line x1="186" y1="256" x2="792" y2="256" stroke="var(--fd-teal)" stroke-width="1" stroke-dasharray="4 3" opacity="0.65" />

      <!-- ================= VERTICAL EVENT SLICES (drawn behind text labels!) ================= -->
      <line x1="776" y1="48" x2="776" y2="332" stroke="var(--fd-ink)" stroke-width="2" />
      <line x1="654" y1="84" x2="654" y2="332" stroke="var(--fd-crimson)" stroke-width="1.6" stroke-dasharray="4 2" />
      <line x1="496" y1="84" x2="496" y2="332" stroke="var(--fd-teal)" stroke-width="2" />
      <line x1="352" y1="100" x2="352" y2="212" stroke="var(--fd-crimson)" stroke-width="1.6" stroke-dasharray="4 2" />
      <line x1="352" y1="262" x2="352" y2="332" stroke="var(--fd-crimson)" stroke-width="1.6" stroke-dasharray="4 2" />
      <line x1="186" y1="48" x2="186" y2="332" stroke="var(--fd-ink)" stroke-width="1.8" />

      <!-- Layer 0 text & PDE operator arrows -->
      <text x="200" y="75" font-size="13" font-weight="700" fill="var(--fd-teal)">
        未敲入价值层 V⁽⁰⁾(t, S)（代码数组 alive）
      </text>
      <text x="200" y="93" font-size="10.2" fill="var(--fd-teal)">S ≥ Bᵒᵘᵗₖ：观察日重置为 Qₖ + Cₖ(S)</text>
      <text x="200" y="156" font-size="10.2" fill="var(--fd-crimson)">S &lt; Bⁱⁿ：监测日覆写为已敲入层 V⁽¹⁾(t⁺, S)</text>

      <g font-size="11" fill="var(--fd-ink)">
        <line x1="760" y1="118" x2="666" y2="118" stroke="var(--fd-teal)" stroke-width="1.8" marker-end="url(#fd-arr-teal)" />
        <text x="713" y="112" text-anchor="middle">∂ₜV⁽⁰⁾ + ℒV⁽⁰⁾ = 0</text>
        <line x1="640" y1="118" x2="510" y2="118" stroke="var(--fd-teal)" stroke-width="1.8" marker-end="url(#fd-arr-teal)" />
        <text x="575" y="112" text-anchor="middle">独立三对角回溯</text>
        <line x1="482" y1="118" x2="366" y2="118" stroke="var(--fd-teal)" stroke-width="1.8" marker-end="url(#fd-arr-teal)" />
        <text x="424" y="112" text-anchor="middle">∂ₜV⁽⁰⁾ + ℒV⁽⁰⁾ = 0</text>
      </g>

      <!-- Layer 1 text & PDE operator arrows -->
      <text x="200" y="233" font-size="13" font-weight="700" fill="var(--fd-crimson)">
        已敲入价值层 V⁽¹⁾(t, S)（代码数组 knocked）
      </text>
      <text x="200" y="251" font-size="10.2" fill="var(--fd-teal)">S ≥ Bᵒᵘᵗₖ：观察日同样敲出终止为 Qₖ + Cₖ(S)（敲入后仍可敲出）</text>
      <text x="200" y="310" font-size="10.2" fill="var(--fd-muted)">S &lt; Bᵒᵘᵗₖ：纯敲入监测日不发生状态跳变，仅在凤凰派息日叠加 +Cₖ(S)</text>

      <g font-size="11" fill="var(--fd-ink)">
        <line x1="760" y1="278" x2="666" y2="278" stroke="var(--fd-crimson)" stroke-width="1.8" marker-end="url(#fd-arr-crimson)" />
        <text x="713" y="272" text-anchor="middle">∂ₜV⁽¹⁾ + ℒV⁽¹⁾ = 0</text>
        <line x1="640" y1="278" x2="510" y2="278" stroke="var(--fd-crimson)" stroke-width="1.8" marker-end="url(#fd-arr-crimson)" />
        <text x="575" y="272" text-anchor="middle">复用同一 Stepper 分解</text>
        <line x1="482" y1="278" x2="366" y2="278" stroke="var(--fd-crimson)" stroke-width="1.8" marker-end="url(#fd-arr-crimson)" />
        <text x="424" y="272" text-anchor="middle">∂ₜV⁽¹⁾ + ℒV⁽¹⁾ = 0</text>
      </g>

      <!-- Coupling arrows & callout pills between Layer 1 and Layer 0 -->
      <path d="M 654 212 L 654 160" fill="none" stroke="var(--fd-crimson)" stroke-width="2.6" marker-end="url(#fd-arr-crimson)" />
      <rect x="578" y="176" width="152" height="25" rx="4" fill="var(--fd-panel)" stroke="var(--fd-crimson)" stroke-width="1.1" />
      <text x="654" y="192" text-anchor="middle" font-size="10.5" font-weight="600" fill="var(--fd-crimson)">
        单向耦合：S &lt; Bⁱⁿ 时 V⁽¹⁾ → V⁽⁰⁾
      </text>

      <path d="M 496 212 L 496 160" fill="none" stroke="var(--fd-crimson)" stroke-width="2.4" marker-end="url(#fd-arr-crimson)" />
      <rect x="404" y="176" width="158" height="25" rx="4" fill="var(--fd-panel)" stroke="var(--fd-teal)" stroke-width="1.1" />
      <text x="483" y="192" text-anchor="middle" font-size="10.5" font-weight="600" fill="var(--fd-teal)">
        敲出重置 + 派息 + 敲入耦合
      </text>

      <path d="M 352 212 L 352 160" fill="none" stroke="var(--fd-crimson)" stroke-width="2.6" marker-end="url(#fd-arr-crimson)" />

      <!-- Prefix handoff arrows -->
      <line x1="186" y1="118" x2="166" y2="180" stroke="var(--fd-teal)" stroke-width="1.6" marker-end="url(#fd-arr-teal)" />
      <line x1="186" y1="278" x2="166" y2="202" stroke="var(--fd-crimson)" stroke-width="1.6" marker-end="url(#fd-arr-crimson)" />

      <!-- Bottom event time labels -->
      <text x="776" y="348" text-anchor="middle" font-size="11.5" font-weight="650" fill="var(--fd-ink)">到期日 <tspan class="fd-math">T</tspan></text>
      <text x="776" y="363" text-anchor="middle" font-size="10.2" fill="var(--fd-muted)">终端投影 Π⁽⁰⁾, Π⁽¹⁾</text>

      <text x="654" y="348" text-anchor="middle" font-size="11.5" font-weight="600" fill="var(--fd-crimson)">
        纯敲入监测日 <tspan class="fd-math">t</tspan><tspan dy="3" font-size="8.5">d</tspan>
      </text>
      <text x="654" y="363" text-anchor="middle" font-size="10.2" fill="var(--fd-muted)">仅更新 V⁽⁰⁾ 的 S &lt; Bⁱⁿ 区</text>

      <text x="496" y="348" text-anchor="middle" font-size="11.5" font-weight="600" fill="var(--fd-teal)">
        观察日 <tspan class="fd-math">t</tspan><tspan dy="3" font-size="8.5">k</tspan>
      </text>
      <text x="496" y="363" text-anchor="middle" font-size="10.2" fill="var(--fd-muted)">两层同步投影跳跃 ΔV</text>

      <text x="352" y="348" text-anchor="middle" font-size="11.5" font-weight="600" fill="var(--fd-crimson)">
        纯敲入监测日 <tspan class="fd-math">t</tspan><tspan dy="3" font-size="8.5">d</tspan><tspan dy="-3">′</tspan>
      </text>

      <text x="186" y="348" text-anchor="middle" font-size="11.5" font-weight="650" fill="var(--fd-ink)">
        <tspan class="fd-math">t</tspan><tspan dy="3" font-size="8.5">start</tspan>
      </text>
      <text x="186" y="363" text-anchor="middle" font-size="10.2" fill="var(--fd-muted)">方差起点</text>
    </svg>
    <figcaption>
      <strong>图 3：双层 PDE 状态扩展与后向回溯耦合架构。</strong>
      在任意两个离散事件之间，未敲入层 <span class="fd-math">V<sup>(0)</sup></span> 与已敲入层 <span class="fd-math">V<sup>(1)</sup></span> 服从完全相同的线性抛物算子，可复用同一套三对角矩阵分解独立推进；两层仅在离散监测时刻通过单向跳跃传递（<span class="fd-math">S &lt; B<sup>in</sup></span> 时由 <span class="fd-math">V<sup>(1)</sup></span> 覆写 <span class="fd-math">V<sup>(0)</sup></span>）耦合。到期敲入、二元雪球或历史已敲入合约自动退化为单层求解。
    </figcaption>
  </figure>
</template>
