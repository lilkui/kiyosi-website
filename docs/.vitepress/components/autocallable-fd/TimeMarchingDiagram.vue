<template>
  <figure class="fd-diagram" role="img" aria-labelledby="fd-fig-time-title">
    <svg viewBox="0 0 860 365" xmlns="http://www.w3.org/2000/svg">
      <title id="fd-fig-time-title">时间网格事件插点、近估值段加密与观察日后 Rannacher 阻尼重启机制</title>
      <defs>
        <marker id="fd-arr-tm" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 1 1.5 L 8.5 5 L 1 8.5 z" fill="var(--fd-muted)" />
        </marker>
        <marker id="fd-arr-tm-ink" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 1 1.5 L 8.5 5 L 1 8.5 z" fill="var(--fd-ink)" />
        </marker>
      </defs>

      <!-- ================= TOP PANEL: TIME GRID & RANNACHER RESTARTS ================= -->
      <text x="430" y="20" text-anchor="middle" font-size="13.2" font-weight="650" fill="var(--fd-ink)">
        （a）后向时间推进网格：事件精确插点、Rannacher 半步阻尼重启与近估值段加密
      </text>

      <!-- Backward direction arrow -->
      <line x1="794" y1="40" x2="66" y2="40" stroke="var(--fd-ink)" stroke-width="1.5" marker-end="url(#fd-arr-tm-ink)" />
      <text x="430" y="35" text-anchor="middle" font-size="10.8" fill="var(--fd-muted)">
        后向步进顺序（step = M′ − 1 … 0）
      </text>

      <!-- Near-valuation dense refinement zone [0, tau_near]: x=64..216 -->
      <rect x="64" y="66" width="152" height="58" rx="4" fill="var(--fd-indigo-soft)" stroke="var(--fd-indigo)" stroke-width="1.2" />
      <g stroke="var(--fd-indigo)" stroke-width="0.9" opacity="0.7">
        <line v-for="k in 18" :key="'nv-'+k" :x1="64 + k * 8" y1="86" :x2="64 + k * 8" y2="116" />
      </g>
      <text x="140" y="79" text-anchor="middle" font-size="10" font-weight="600" fill="var(--fd-indigo)">
        近估值段加密 (≥128 / 64 步)
      </text>

      <!-- CN zone 1: x=216..404 -->
      <rect x="216" y="66" width="188" height="58" fill="var(--fd-teal-soft)" stroke="var(--fd-teal)" stroke-width="1.1" />
      <g stroke="var(--fd-teal)" stroke-width="1.2">
        <line v-for="x in [254, 292, 330, 368]" :key="'cn1-'+x" :x1="x" y1="86" :x2="x" y2="116" />
      </g>
      <text x="310" y="79" text-anchor="middle" font-size="10" font-weight="600" fill="var(--fd-teal)">
        Crank–Nicolson (θ = 1/2，复用 LU 缓存)
      </text>

      <!-- Rannacher damping zone after Event t_k: x=404..492 (2 intervals = 4 half-steps) -->
      <rect x="404" y="66" width="88" height="58" fill="var(--fd-amber-soft)" stroke="var(--fd-amber)" stroke-width="1.3" />
      <line x1="448" y1="70" x2="448" y2="120" stroke="var(--fd-amber)" stroke-width="1.4" />
      <line x1="426" y1="82" x2="426" y2="112" stroke="var(--fd-amber)" stroke-width="1.1" stroke-dasharray="2 2" />
      <line x1="470" y1="82" x2="470" y2="112" stroke="var(--fd-amber)" stroke-width="1.1" stroke-dasharray="2 2" />
      <text x="448" y="57" text-anchor="middle" font-size="9.8" font-weight="650" fill="var(--fd-amber)">
        阻尼重启：4 个 IE 半步
      </text>

      <!-- CN zone 2: x=492..706 -->
      <rect x="492" y="66" width="214" height="58" fill="var(--fd-teal-soft)" stroke="var(--fd-teal)" stroke-width="1.1" />
      <g stroke="var(--fd-teal)" stroke-width="1.2">
        <line v-for="x in [535, 578, 621, 664]" :key="'cn2-'+x" :x1="x" y1="86" :x2="x" y2="116" />
      </g>
      <text x="599" y="79" text-anchor="middle" font-size="10" font-weight="600" fill="var(--fd-teal)">
        Crank–Nicolson (θ = 1/2，均匀 Δt)
      </text>

      <!-- Rannacher damping zone at Expiry T: x=706..794 (2 intervals = 4 half-steps) -->
      <rect x="706" y="66" width="88" height="58" fill="var(--fd-amber-soft)" stroke="var(--fd-amber)" stroke-width="1.3" />
      <line x1="750" y1="70" x2="750" y2="120" stroke="var(--fd-amber)" stroke-width="1.4" />
      <line x1="728" y1="82" x2="728" y2="112" stroke="var(--fd-amber)" stroke-width="1.1" stroke-dasharray="2 2" />
      <line x1="772" y1="82" x2="772" y2="112" stroke="var(--fd-amber)" stroke-width="1.1" stroke-dasharray="2 2" />
      <text x="748" y="57" text-anchor="middle" font-size="9.8" font-weight="650" fill="var(--fd-amber)">
        终端阻尼：4 个 IE 半步
      </text>

      <!-- Event t_k, Expiry T, and Valuation 0 vertical bars (start at y=62 below top labels!) -->
      <line x1="492" y1="62" x2="492" y2="134" stroke="var(--fd-crimson)" stroke-width="2.6" />
      <line x1="794" y1="62" x2="794" y2="134" stroke="var(--fd-ink)" stroke-width="2.6" />
      <line x1="64" y1="62" x2="64" y2="134" stroke="var(--fd-ink)" stroke-width="2.4" />
      <line x1="216" y1="62" x2="216" y2="132" stroke="var(--fd-indigo)" stroke-width="1.6" stroke-dasharray="3 2" />

      <g font-size="11" text-anchor="middle">
        <text x="64" y="148" font-weight="650" fill="var(--fd-ink)">t = 0（估值点）</text>
        <text x="216" y="148" font-weight="600" fill="var(--fd-indigo)">
          <tspan class="fd-math">τ</tspan><tspan dy="2.5" font-size="8.5">near</tspan><tspan dy="-2.5">（首个事件/节点）</tspan>
        </text>
        <text x="492" y="148" font-weight="650" fill="var(--fd-crimson)">事件点 tₖ（投影跳跃 + damping=2）</text>
        <text x="774" y="148" font-weight="650" fill="var(--fd-ink)">
          <tspan class="fd-math">τ</tspan><tspan dy="2.5" font-size="8.5">T</tspan><tspan dy="-2.5">（到期终端投影）</tspan>
        </text>
      </g>

      <!-- ================= BOTTOM LEFT: AMPLIFICATION FACTOR R(z) ================= -->
      <g transform="translate(48, 170)">
        <rect x="0" y="0" width="388" height="178" rx="6" fill="var(--fd-panel-alt)" stroke="var(--fd-grid)" />
        <text x="194" y="21" text-anchor="middle" font-size="12.2" font-weight="650" fill="var(--fd-ink)">
          （b）模态放大因子 R(z) 随刚度 z = λΔt 的渐近行为
        </text>

        <!-- R=+1 at y=46, R=0 at y=98, R=-1 at y=150 -->
        <line x1="56" y1="46" x2="362" y2="46" stroke="var(--fd-grid)" stroke-dasharray="3 3" />
        <line x1="56" y1="98" x2="368" y2="98" stroke="var(--fd-muted)" stroke-width="1.3" marker-end="url(#fd-arr-tm)" />
        <line x1="56" y1="150" x2="362" y2="150" stroke="var(--fd-crimson)" stroke-width="1" stroke-dasharray="4 3" opacity="0.7" />
        <line x1="56" y1="158" x2="56" y2="34" stroke="var(--fd-muted)" stroke-width="1.3" marker-end="url(#fd-arr-tm)" />

        <text x="48" y="50" text-anchor="end" font-size="10.5" fill="var(--fd-muted)">+1</text>
        <text x="48" y="102" text-anchor="end" font-size="10.5" fill="var(--fd-muted)">0</text>
        <text x="48" y="154" text-anchor="end" font-size="10.5" fill="var(--fd-crimson)" font-weight="600">−1</text>
        <text x="372" y="102" font-size="11" fill="var(--fd-ink)" class="fd-math">z</text>

        <!-- Crank-Nicolson R(z) = (1 - z/2)/(1 + z/2) -> approaches -1 -->
        <path
          d="M 56 46 C 84 96, 124 138, 356 147"
          fill="none"
          stroke="var(--fd-crimson)"
          stroke-width="2.2"
          stroke-dasharray="6 3"
        />
        <text x="272" y="123" text-anchor="middle" font-size="10" fill="var(--fd-crimson)" font-weight="600">
          无阻尼 CN：R(∞) → −1（逐步反号振荡）
        </text>

        <!-- Two Implicit Euler half-steps: R_damp(z) = 1 / (1 + z/4)^2 -> approaches 0 rapidly! -->
        <path
          d="M 56 46 C 90 80, 146 95, 356 97.5"
          fill="none"
          stroke="var(--fd-teal)"
          stroke-width="2.4"
        />
        <text x="248" y="72" text-anchor="middle" font-size="10.3" fill="var(--fd-teal)" font-weight="600">
          一对 IE 半步 [1/(1+z/4)]² → 0（L-稳定消振）
        </text>
      </g>

      <!-- ================= BOTTOM RIGHT: GAMMA SPURIOUS OSCILLATION CONTRAST ================= -->
      <g transform="translate(454, 170)">
        <rect x="0" y="0" width="358" height="178" rx="6" fill="var(--fd-panel-alt)" stroke="var(--fd-grid)" />
        <text x="179" y="21" text-anchor="middle" font-size="12.2" font-weight="650" fill="var(--fd-ink)">
          （c）距敲出观察日 2 天时敲出线附近的二阶导数 Γ(S)
        </text>

        <line x1="32" y1="104" x2="334" y2="104" stroke="var(--fd-muted)" stroke-width="1.2" marker-end="url(#fd-arr-tm)" />
        <line x1="146" y1="38" x2="146" y2="152" stroke="var(--fd-faint)" stroke-dasharray="3 3" />

        <!-- Undamped CN spurious sawtooth wave around B^out (centered at x=146 so right side is wide open for labels!) -->
        <polyline
          points="38,107 84,106 108,101 120,117 129,78 138,142 146,44 154,144 163,76 172,115 186,102 214,106 322,105"
          fill="none"
          stroke="var(--fd-crimson)"
          stroke-width="1.8"
        />
        <!-- Rannacher smooth Gamma curve -->
        <path
          d="M 38 107 Q 104 114 146 126 Q 194 114 322 105"
          fill="none"
          stroke="var(--fd-teal)"
          stroke-width="2.6"
        />

        <text x="256" y="64" text-anchor="middle" font-size="10.3" fill="var(--fd-crimson)" font-weight="600">
          无阻尼 CN：Γ 放大 k² 倍
        </text>
        <text x="256" y="79" text-anchor="middle" font-size="10.1" fill="var(--fd-crimson)">
          失真达 +10³ 量级
        </text>
        <text x="260" y="138" text-anchor="middle" font-size="10.3" fill="var(--fd-teal)" font-weight="600">
          Rannacher 重启：恢复光滑 Γ
        </text>
        <text x="146" y="166" text-anchor="middle" font-size="10.8" fill="var(--fd-ink)" font-weight="600">
          S = Bᵒᵘᵗₖ（阶跃间断源）
        </text>
      </g>
    </svg>
    <figcaption>
      <strong>图 7：时间离散网格与观察日后 Rannacher 阻尼重启的数值机理。</strong>
      （a）每次跨越终端或中间事件点后，计数器重置 <code>damping = 2</code>，将紧随其后的两个时间步各拆分为两个隐式 Euler 半步，随后切回 Crank–Nicolson；（b–c）无阻尼 CN 对阶跃激发的高波数模态放大因子趋于 <span class="fd-math">−1</span>，求二阶导数 <span class="fd-math">Γ = ∂<sub>SS</sub>V</span> 时误差按波数平方 <span class="fd-math">k<sup>2</sup></span> 放大而失真（见第 8.7、9.7 节实测），L-稳定半步阻尼则在保持整体二阶时间精度的同时迅速滤除高频伪振荡。
    </figcaption>
  </figure>
</template>
