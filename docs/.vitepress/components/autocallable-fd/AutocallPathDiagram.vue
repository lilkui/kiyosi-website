<template>
  <figure class="fd-diagram" role="img" aria-labelledby="fd-fig-paths-title">
    <svg viewBox="0 0 860 365" xmlns="http://www.w3.org/2000/svg">
      <title id="fd-fig-paths-title">雪球与凤凰在时间-价格平面上的离散监测与典型路径</title>
      <defs>
        <marker id="fd-arr-ink" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 1 1.5 L 8.5 5 L 1 8.5 z" fill="var(--fd-muted)" />
        </marker>
      </defs>

      <!-- Lockout shaded band (Phoenix early KO lockout) -->
      <rect x="82" y="34" width="196" height="266" fill="var(--fd-amber-soft)" opacity="0.55" rx="2" />
      <text x="180" y="52" text-anchor="middle" font-size="11.5" fill="var(--fd-amber)" font-weight="600">
        凤凰敲出锁定期（仅观察票息与敲入）
      </text>

      <!-- Knock-in danger zone tint -->
      <rect x="82" y="232" width="688" height="68" fill="var(--fd-crimson-soft)" opacity="0.45" />

      <!-- Monthly observation vertical lines -->
      <g stroke="var(--fd-grid)" stroke-width="1.2" stroke-dasharray="4 4">
        <line x1="180" y1="34" x2="180" y2="300" />
        <line x1="278" y1="34" x2="278" y2="300" />
        <line x1="376" y1="34" x2="376" y2="300" />
        <line x1="474" y1="34" x2="474" y2="300" />
        <line x1="572" y1="34" x2="572" y2="300" />
        <line x1="670" y1="34" x2="670" y2="300" />
      </g>
      <line x1="770" y1="34" x2="770" y2="300" stroke="var(--fd-muted)" stroke-width="1.4" stroke-dasharray="3 3" />

      <!-- Barrier horizontal lines -->
      <!-- Knock-out barrier B^out (active from t_2 onward if lockout=1, or all t_k for Snowball) -->
      <line x1="82" y1="112" x2="278" y2="112" stroke="var(--fd-teal)" stroke-width="1.5" stroke-dasharray="2 5" opacity="0.55" />
      <line x1="278" y1="112" x2="770" y2="112" stroke="var(--fd-teal)" stroke-width="2" stroke-dasharray="7 4" />
      <!-- Initial spot / reference S_0 = U -->
      <line x1="82" y1="146" x2="770" y2="146" stroke="var(--fd-faint)" stroke-width="1.1" />
      <!-- Phoenix coupon barrier B^c -->
      <line x1="82" y1="194" x2="770" y2="194" stroke="var(--fd-amber)" stroke-width="1.6" stroke-dasharray="5 4" />
      <!-- Knock-in barrier B^in with daily trading-day ticks -->
      <line x1="82" y1="232" x2="770" y2="232" stroke="var(--fd-crimson)" stroke-width="1.8" />
      <g stroke="var(--fd-crimson)" stroke-width="1" opacity="0.75">
        <line v-for="n in 42" :key="n" :x1="82 + n * 16.3" y1="228" :x2="82 + n * 16.3" y2="236" />
      </g>

      <!-- Axes -->
      <line x1="82" y1="300" x2="792" y2="300" stroke="var(--fd-muted)" stroke-width="1.5" marker-end="url(#fd-arr-ink)" />
      <line x1="82" y1="304" x2="82" y2="24" stroke="var(--fd-muted)" stroke-width="1.5" marker-end="url(#fd-arr-ink)" />

      <!-- Y-axis labels -->
      <text x="74" y="28" text-anchor="end" font-size="12.5" fill="var(--fd-ink)" class="fd-math">S<tspan dy="3" font-size="9.5" font-style="normal">t</tspan></text>
      <text x="74" y="116" text-anchor="end" font-size="12" fill="var(--fd-teal)" font-weight="600">
        <tspan class="fd-math">B</tspan><tspan dy="-5" font-size="9">out</tspan><tspan dy="5"> (≥)</tspan>
      </text>
      <text x="74" y="150" text-anchor="end" font-size="11.5" fill="var(--fd-muted)">
        <tspan class="fd-math">S</tspan><tspan dy="3" font-size="9">0</tspan><tspan dy="-3"> = </tspan><tspan class="fd-math">U</tspan>
      </text>
      <text x="74" y="198" text-anchor="end" font-size="12" fill="var(--fd-amber)" font-weight="600">
        <tspan class="fd-math">B</tspan><tspan dy="-5" font-size="9">c</tspan><tspan dy="5"> (≥)</tspan>
      </text>
      <text x="74" y="236" text-anchor="end" font-size="12" fill="var(--fd-crimson)" font-weight="600">
        <tspan class="fd-math">B</tspan><tspan dy="-5" font-size="9">in</tspan><tspan dy="5"> (&lt;)</tspan>
      </text>
      <text x="74" y="304" text-anchor="end" font-size="11.5" fill="var(--fd-muted)">0</text>

      <!-- X-axis labels -->
      <g font-size="12" fill="var(--fd-muted)" text-anchor="middle">
        <text x="82" y="320" class="fd-math">t<tspan dy="3" font-size="9" font-style="normal">0</tspan></text>
        <text x="180" y="320" class="fd-math">t<tspan dy="3" font-size="9" font-style="normal">1</tspan></text>
        <text x="278" y="320" class="fd-math">t<tspan dy="3" font-size="9" font-style="normal">2</tspan></text>
        <text x="376" y="320" class="fd-math">t<tspan dy="3" font-size="9" font-style="normal">3</tspan></text>
        <text x="474" y="320" class="fd-math">t<tspan dy="3" font-size="9" font-style="normal">4</tspan></text>
        <text x="572" y="320" class="fd-math">t<tspan dy="3" font-size="9" font-style="normal">5</tspan></text>
        <text x="670" y="320" class="fd-math">t<tspan dy="3" font-size="9" font-style="normal">6</tspan></text>
        <text x="770" y="320" font-weight="600" fill="var(--fd-ink)" class="fd-math">T</text>
        <text x="802" y="304" class="fd-math">t</text>
      </g>

      <!-- Path 1: Early Knock-Out at t_3 (passes above B^out inside lockout at t_1 without KO for Phoenix, KOs at t_3) -->
      <path
        d="M 82 146 L 125 128 L 180 96 L 232 134 L 278 128 L 330 118 L 376 84"
        fill="none"
        stroke="var(--fd-teal)"
        stroke-width="2.4"
        stroke-linejoin="round"
      />
      <!-- Lockout point at t_1: open circle for Phoenix KO, coupon paid -->
      <circle cx="180" cy="96" r="4.2" fill="var(--fd-panel)" stroke="var(--fd-amber)" stroke-width="2" />
      <!-- Knock-out termination at t_3 -->
      <circle cx="376" cy="84" r="5" fill="var(--fd-teal)" />
      <text x="376" y="68" text-anchor="middle" font-size="11.5" fill="var(--fd-teal)" font-weight="600">
        路径 ①：t₃ 触发敲出终止（付 Q₃ + C₃）
      </text>

      <!-- Path 2: Survives unknocked (briefly crosses B^out BETWEEN t_4 and t_5 without KO!) -->
      <path
        d="M 82 146 L 142 162 L 180 170 L 240 154 L 278 164 L 340 182 L 376 175 L 430 142 L 474 132 L 526 96 L 572 138 L 625 166 L 670 158 L 724 176 L 770 162"
        fill="none"
        stroke="var(--fd-indigo)"
        stroke-width="2.1"
        stroke-linejoin="round"
      />
      <!-- Non-observation excursion above B^out between t_4 and t_5 -->
      <circle cx="526" cy="96" r="3.6" fill="var(--fd-panel)" stroke="var(--fd-indigo)" stroke-width="1.8" />
      <text x="596" y="92" text-anchor="start" font-size="10.8" fill="var(--fd-indigo)">
        ← 非观察日越过敲出线不触发
      </text>
      <circle cx="770" cy="162" r="4.8" fill="var(--fd-indigo)" />
      <text x="760" y="138" text-anchor="end" font-size="11.5" fill="var(--fd-indigo)" font-weight="600">
        路径 ②：未敲入到期 Π⁽⁰⁾(<tspan class="fd-math">S</tspan><tspan dy="3" font-size="8.5">T</tspan><tspan dy="-3">)</tspan>
      </text>

      <!-- Path 3: Daily Knock-In on trading day between t_2 and t_3, never knocks out -->
      <path
        d="M 82 146 L 135 178 L 180 206 L 236 218 L 278 214 L 311 248 L 352 222 L 376 184 L 435 198 L 474 212 L 535 242 L 572 224 L 635 256 L 670 246 L 725 268 L 770 258"
        fill="none"
        stroke="var(--fd-crimson)"
        stroke-width="2.2"
        stroke-linejoin="round"
      />
      <!-- Exact daily knock-in point at x=311 -->
      <circle cx="311" cy="248" r="4.8" fill="var(--fd-crimson)" />
      <text x="311" y="268" text-anchor="middle" font-size="11" fill="var(--fd-crimson)" font-weight="600">
        交易日 S &lt; Bⁱⁿ → 状态切换 j: 0 → 1
      </text>
      <!-- At t_3 (x=376, y=184 < 194 meaning S > B^c!), Phoenix still pays coupon c! -->
      <circle cx="376" cy="184" r="4" fill="var(--fd-amber)" />
      <circle cx="770" cy="258" r="4.8" fill="var(--fd-crimson)" />
      <text x="760" y="286" text-anchor="end" font-size="11.5" fill="var(--fd-crimson)" font-weight="600">
        路径 ③：已敲入到期 Π⁽¹⁾(<tspan class="fd-math">S</tspan><tspan dy="3" font-size="8.5">T</tspan><tspan dy="-3">)（承担下跌亏损）</tspan>
      </text>

      <!-- Bottom legend strip -->
      <g transform="translate(46, 345)" font-size="11.2" fill="var(--fd-muted)">
        <line x1="0" y1="-4" x2="18" y2="-4" stroke="var(--fd-crimson)" stroke-width="2" />
        <line x1="9" y1="-8" x2="9" y2="0" stroke="var(--fd-crimson)" stroke-width="1.3" />
        <text x="24" y="0">每日敲入监测点（严格不等 S &lt; Bⁱⁿ）</text>

        <circle cx="242" cy="-4" r="4" fill="var(--fd-amber)" />
        <text x="252" y="0">凤凰观察日派息（S ≥ Bᶜ，敲入后仍可派息）</text>

        <circle cx="520" cy="-4" r="4.2" fill="var(--fd-teal)" />
        <text x="530" y="0">敲出观察日终止（S ≥ Bᵒᵘᵗ，敲入后亦可敲出）</text>
      </g>
    </svg>
    <figcaption>
      <strong>图 1：雪球与凤凰在 <span class="fd-math">(t, S<sub>t</sub>)</span> 平面上的离散事件触发机制。</strong>
      敲出与凤凰派息仅在离散观察时刻 <span class="fd-math">t<sub>k</sub></span> 判定（路径 ② 在 <span class="fd-math">t<sub>4</sub></span> 与 <span class="fd-math">t<sub>5</sub></span> 之间短暂越过 <span class="fd-math">B<sup>out</sup></span> 并不触发敲出）；每日敲入则在每个交易日的约定观察时点判定（<span class="fd-math">B<sup>in</sup></span> 上的短竖线），一旦 <span class="fd-math">S &lt; B<sup>in</sup></span> 即不可逆地转入已敲入状态 <span class="fd-math">j = 1</span>。
    </figcaption>
  </figure>
</template>
