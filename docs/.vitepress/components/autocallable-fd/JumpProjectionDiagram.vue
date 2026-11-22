<template>
  <figure class="fd-diagram" role="img" aria-labelledby="fd-fig-proj-title">
    <svg viewBox="0 0 860 395" xmlns="http://www.w3.org/2000/svg">
      <title id="fd-fig-proj-title">对数现货网格的 sinh 加密与控制体积跳跃修正投影</title>
      <defs>
        <marker id="fd-arr-pj" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 1 1.5 L 8.5 5 L 1 8.5 z" fill="var(--fd-muted)" />
        </marker>
      </defs>

      <!-- ================= TOP STRIP: SINH MULTI-LEVEL CONCENTRATED GRID ================= -->
      <text x="430" y="20" text-anchor="middle" font-size="13.2" font-weight="650" fill="var(--fd-ink)">
        （a）对数坐标 x = ln(S/Sₐ) 上的合约水平对齐与 sinh 加密
      </text>

      <rect x="48" y="34" width="764" height="62" rx="5" fill="var(--fd-panel-alt)" stroke="var(--fd-grid)" />
      <line x1="64" y1="70" x2="796" y2="70" stroke="var(--fd-muted)" stroke-width="1.5" />

      <!-- Midpoint splitters m_12, m_23 -->
      <line x1="305" y1="42" x2="305" y2="92" stroke="var(--fd-muted)" stroke-width="1" stroke-dasharray="3 3" />
      <text x="305" y="48" text-anchor="middle" font-size="9.5" fill="var(--fd-muted)">中点分界</text>
      <line x1="455" y1="42" x2="455" y2="92" stroke="var(--fd-muted)" stroke-width="1" stroke-dasharray="3 3" />
      <text x="455" y="48" text-anchor="middle" font-size="9.5" fill="var(--fd-muted)">中点分界</text>

      <!-- Sinh concentrated tick marks around B^in (x=220), B^c (x=390), B^out=U (x=520) -->
      <g stroke="var(--fd-ink)" stroke-width="1.15" opacity="0.8">
        <!-- Left of B^in=220 -->
        <line v-for="dx in [0, 4, 9, 16, 26, 40, 60, 88, 122, 156]" :key="'l1-'+dx" :x1="220 - dx" y1="63" :x2="220 - dx" y2="77" />
        <!-- Between B^in=220 and midpoint 305 -->
        <line v-for="dx in [4, 9, 16, 26, 40, 60, 85]" :key="'r1-'+dx" :x1="220 + dx" y1="63" :x2="220 + dx" y2="77" />
        <!-- Between midpoint 305 and B^c=390 -->
        <line v-for="dx in [0, 4, 9, 16, 26, 40, 60]" :key="'l2-'+dx" :x1="390 - dx" y1="63" :x2="390 - dx" y2="77" />
        <!-- Between B^c=390 and midpoint 455 -->
        <line v-for="dx in [4, 9, 16, 27, 43, 65]" :key="'r2-'+dx" :x1="390 + dx" y1="63" :x2="390 + dx" y2="77" />
        <!-- Between midpoint 455 and B^out=520 -->
        <line v-for="dx in [0, 4, 9, 16, 27, 43]" :key="'l3-'+dx" :x1="520 - dx" y1="63" :x2="520 - dx" y2="77" />
        <!-- Right of B^out=520 out to x_max=796 -->
        <line v-for="dx in [4, 9, 16, 26, 40, 60, 88, 124, 168, 220, 276]" :key="'r3-'+dx" :x1="520 + dx" y1="63" :x2="520 + dx" y2="77" />
      </g>

      <!-- Highlight exact contract level nodes -->
      <circle cx="64" cy="70" r="3.5" fill="var(--fd-ink)" />
      <circle cx="220" cy="70" r="4.5" fill="var(--fd-crimson)" />
      <circle cx="390" cy="70" r="4.5" fill="var(--fd-amber)" />
      <circle cx="520" cy="70" r="4.5" fill="var(--fd-teal)" />
      <circle cx="796" cy="70" r="3.5" fill="var(--fd-ink)" />

      <g font-size="11" text-anchor="middle">
        <text x="64" y="90" fill="var(--fd-muted)">xₘᵢₙ</text>
        <text x="220" y="90" fill="var(--fd-crimson)" font-weight="650">x(Bⁱⁿ)</text>
        <text x="390" y="90" fill="var(--fd-amber)" font-weight="650">x(Bᶜₖ)</text>
        <text x="520" y="90" fill="var(--fd-teal)" font-weight="650">x(Bᵒᵘᵗₖ) = x(U)</text>
        <text x="782" y="90" fill="var(--fd-muted)">
          <tspan class="fd-math">x</tspan><tspan dy="2.5" font-size="8.5">max</tspan>
        </text>
      </g>

      <!-- ================= BOTTOM MAIN: JUMP-CORRECTION PROJECTION ================= -->
      <text x="430" y="126" text-anchor="middle" font-size="13.2" font-weight="650" fill="var(--fd-ink)">
        （b）控制体积 Cᵢ = [<tspan class="fd-math">x</tspan><tspan dy="3" font-size="9">i−1/2</tspan><tspan dy="-3">, </tspan><tspan class="fd-math">x</tspan><tspan dy="3" font-size="9">i+1/2</tspan><tspan dy="-3">] 内的跳跃修正量分段 Gauss–Legendre 投影</tspan>
      </text>

      <!-- Left box: Smooth non-straddling cell -->
      <g transform="translate(48, 142)">
        <rect x="0" y="0" width="236" height="226" rx="6" fill="var(--fd-panel-alt)" stroke="var(--fd-grid)" />
        <text x="118" y="22" text-anchor="middle" font-size="12" font-weight="650" fill="var(--fd-ink)">
          情形 1：不含间断点的普通单元 Cⱼ
        </text>
        <text x="118" y="40" text-anchor="middle" font-size="10.5" fill="var(--fd-muted)">
          breaks ∩ (<tspan class="fd-math">x</tspan><tspan dy="2.5" font-size="8">j−1/2</tspan><tspan dy="-2.5">, </tspan><tspan class="fd-math">x</tspan><tspan dy="2.5" font-size="8">j+1/2</tspan><tspan dy="-2.5">) = ∅</tspan>
        </text>

        <!-- Cell walls -->
        <line x1="42" y1="62" x2="42" y2="162" stroke="var(--fd-faint)" stroke-dasharray="3 3" />
        <line x1="194" y1="62" x2="194" y2="162" stroke="var(--fd-faint)" stroke-dasharray="3 3" />
        <line x1="28" y1="162" x2="208" y2="162" stroke="var(--fd-muted)" stroke-width="1.3" />

        <!-- Smooth V+ curve -->
        <path d="M 32 138 Q 118 96 204 82" fill="none" stroke="var(--fd-teal)" stroke-width="2.3" />
        <circle cx="118" cy="103" r="4.5" fill="var(--fd-teal)" />
        <line x1="118" y1="103" x2="118" y2="162" stroke="var(--fd-teal)" stroke-width="1.2" stroke-dasharray="2 2" />

        <g font-size="10.5" text-anchor="middle" fill="var(--fd-muted)">
          <text x="42" y="177"><tspan class="fd-math">x</tspan><tspan dy="2.5" font-size="8">j−1/2</tspan></text>
          <text x="118" y="177" fill="var(--fd-ink)" font-weight="600"><tspan class="fd-math">x</tspan><tspan dy="2.5" font-size="8">j</tspan></text>
          <text x="194" y="177"><tspan class="fd-math">x</tspan><tspan dy="2.5" font-size="8">j+1/2</tspan></text>
        </g>
        <text x="118" y="198" text-anchor="middle" font-size="10.8" fill="var(--fd-teal)" font-weight="600">
          直接取中心点修正：Vⱼ⁻ = Vⱼ⁺ + ΔV(Sⱼ)
        </text>
        <text x="118" y="215" text-anchor="middle" font-size="10.2" fill="var(--fd-muted)">
          无人工数值耗散，光滑延续价值原样保留
        </text>
      </g>

      <!-- Right zoomed box: Straddling cell C_i containing interior barrier x_b -->
      <g transform="translate(306, 142)">
        <rect x="0" y="0" width="506" height="226" rx="6" fill="var(--fd-panel-alt)" stroke="var(--fd-teal)" stroke-width="1.2" />
        <text x="253" y="22" text-anchor="middle" font-size="11.6" font-weight="650" fill="var(--fd-ink)">
          情形 2：跨越间断点 <tspan class="fd-math">x</tspan><tspan dy="2.5" font-size="8.5">b</tspan><tspan dy="-2.5"> 的界面单元 Cᵢ → 按 {</tspan><tspan class="fd-math">x</tspan><tspan dy="2.5" font-size="8.5">i−1/2</tspan><tspan dy="-2.5">, </tspan><tspan class="fd-math">x</tspan><tspan dy="2.5" font-size="8.5">b</tspan><tspan dy="-2.5">, </tspan><tspan class="fd-math">x</tspan><tspan dy="2.5" font-size="8.5">i</tspan><tspan dy="-2.5">, </tspan><tspan class="fd-math">x</tspan><tspan dy="2.5" font-size="8.5">i+1/2</tspan><tspan dy="-2.5">} 切分子区间求积</tspan>
        </text>

        <!-- Shaded jump area under Delta V on [x_b, x_{i+1/2}] -->
        <polygon
          points="196,148 196,74 284,84 438,98 438,148"
          fill="var(--fd-teal-soft)"
        />

        <!-- Split vertical lines -->
        <line x1="68" y1="48" x2="68" y2="162" stroke="var(--fd-muted)" stroke-width="1.3" stroke-dasharray="4 3" />
        <line x1="196" y1="48" x2="196" y2="162" stroke="var(--fd-crimson)" stroke-width="1.6" stroke-dasharray="4 2" />
        <line x1="284" y1="48" x2="284" y2="162" stroke="var(--fd-indigo)" stroke-width="1.3" stroke-dasharray="3 3" />
        <line x1="438" y1="48" x2="438" y2="162" stroke="var(--fd-muted)" stroke-width="1.3" stroke-dasharray="4 3" />

        <!-- Zero baseline for jump Delta V(S(x)) -->
        <line x1="46" y1="148" x2="466" y2="148" stroke="var(--fd-muted)" stroke-width="1.4" marker-end="url(#fd-arr-pj)" />
        <text x="40" y="152" text-anchor="end" font-size="10.5" fill="var(--fd-muted)">ΔV=0</text>

        <!-- Jump function Delta V(x) -->
        <line x1="68" y1="148" x2="196" y2="148" stroke="var(--fd-teal)" stroke-width="2.6" />
        <circle cx="196" cy="148" r="3.8" fill="var(--fd-panel)" stroke="var(--fd-teal)" stroke-width="2" />
        <circle cx="196" cy="74" r="4.2" fill="var(--fd-teal)" />
        <polyline points="196,74 284,84 438,98" fill="none" stroke="var(--fd-teal)" stroke-width="2.6" />

        <!-- Gauss-Legendre 2-point nodes -->
        <g fill="var(--fd-amber)">
          <circle cx="95" cy="148" r="3.6" />
          <circle cx="169" cy="148" r="3.6" />
          <circle cx="214.6" cy="76.1" r="3.8" />
          <circle cx="265.4" cy="81.9" r="3.8" />
          <circle cx="316.5" cy="87.0" r="3.8" />
          <circle cx="405.5" cy="95.0" r="3.8" />
        </g>

        <!-- Sub-interval labels -->
        <g font-size="10.2" text-anchor="middle" fill="var(--fd-ink)">
          <text x="132" y="136">子区间 I₁</text>
          <text x="240" y="62" fill="var(--fd-teal)" font-weight="600">子区间 I₂</text>
          <text x="361" y="74" fill="var(--fd-teal)" font-weight="600">子区间 I₃（插值斜率折点切分）</text>
        </g>

        <!-- Coordinate labels -->
        <g font-size="10.8" text-anchor="middle">
          <text x="68" y="176" fill="var(--fd-muted)"><tspan class="fd-math">x</tspan><tspan dy="2.5" font-size="8.2">i−1/2</tspan></text>
          <text x="196" y="176" fill="var(--fd-crimson)" font-weight="650">
            <tspan class="fd-math">x</tspan><tspan dy="2.5" font-size="8.2">b</tspan><tspan dy="-2.5"> = x(B)</tspan>
          </text>
          <text x="284" y="176" fill="var(--fd-indigo)" font-weight="600">
            中心 <tspan class="fd-math">x</tspan><tspan dy="2.5" font-size="8.2">i</tspan>
          </text>
          <text x="438" y="176" fill="var(--fd-muted)"><tspan class="fd-math">x</tspan><tspan dy="2.5" font-size="8.2">i+1/2</tspan></text>
        </g>

        <!-- Legend / formula note inside right box -->
        <circle cx="26" cy="204" r="3.8" fill="var(--fd-amber)" />
        <text x="36" y="208" font-size="10.2" fill="var(--fd-muted)">
          两点 Gauss–Legendre 节点 mⱼ ± |Iⱼ|/(2√3)（三次精确），更新 Vᵢ⁻ = Vᵢ⁺ + ∑ (|Iⱼ|/|Cᵢ|)·Δ̄ⱼ
        </text>
      </g>
    </svg>
    <figcaption>
      <strong>图 6：空间网格加密与控制体积增量跳跃投影原理。</strong>
      （a）<code>concentrate</code> 将保留的障碍与行权价映射为对数网格节点，并在两侧按 <span class="fd-math">sinh</span> 规律加密；（b）在含间断的控制体积 <span class="fd-math">C<sub>i</sub></span> 内，<code>project_interval</code> 同时以障碍坐标 <span class="fd-math">x<sub>b</sub></span> 与单元中心 <span class="fd-math">x<sub>i</sub></span> 切分区间（消除 <span class="fd-math">I<sub>lin</sub>[V<sup>+</sup>]</span> 在 <span class="fd-math">x<sub>i</sub></span> 处的折点误差），仅对不连续跳跃量 <span class="fd-math">ΔV = V<sup>−</sup> − V<sup>+</sup></span> 做加权积分平均。
    </figcaption>
  </figure>
</template>
