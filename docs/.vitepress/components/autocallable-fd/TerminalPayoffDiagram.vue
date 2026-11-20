<template>
  <figure class="fd-diagram" role="img" aria-labelledby="fd-fig-payoff-title">
    <svg viewBox="0 0 860 355" xmlns="http://www.w3.org/2000/svg">
      <title id="fd-fig-payoff-title">标准雪球与凤凰在到期日 T 的未敲入层与已敲入层终端支付对比</title>
      <defs>
        <marker id="fd-arr-payoff" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 1 1.5 L 8.5 5 L 1 8.5 z" fill="var(--fd-muted)" />
        </marker>
      </defs>

      <!-- ================= LEFT PANEL: SNOWBALL ================= -->
      <g transform="translate(0, 0)">
        <text x="225" y="22" text-anchor="middle" font-size="13.5" font-weight="650" fill="var(--fd-ink)">
          （a）标准雪球到期支付 V(T, S)（rₙ = cₘ = 15%, τ = 1）
        </text>

        <!-- Reference grid lines -->
        <!-- y map: value 1.15 -> y=78, value 1.00 -> y=118, value 0.70 -> y=198, value 0.50 -> y=251, value 0.40 -> y=278 -->
        <g stroke="var(--fd-grid)" stroke-width="1" stroke-dasharray="3 3">
          <line x1="68" y1="78" x2="395" y2="78" />
          <line x1="68" y1="118" x2="395" y2="118" />
          <line x1="68" y1="198" x2="395" y2="198" />
          <line x1="162" y1="44" x2="162" y2="288" />
          <line x1="218" y1="44" x2="218" y2="288" />
          <line x1="302" y1="44" x2="302" y2="288" />
        </g>

        <!-- Axes -->
        <line x1="68" y1="288" x2="405" y2="288" stroke="var(--fd-muted)" stroke-width="1.5" marker-end="url(#fd-arr-payoff)" />
        <line x1="68" y1="292" x2="68" y2="40" stroke="var(--fd-muted)" stroke-width="1.5" marker-end="url(#fd-arr-payoff)" />

        <!-- Y labels -->
        <text x="61" y="82" text-anchor="end" font-size="11" fill="var(--fd-teal)" font-weight="600">1.15</text>
        <text x="61" y="122" text-anchor="end" font-size="11" fill="var(--fd-muted)">1.00</text>
        <text x="61" y="202" text-anchor="end" font-size="11" fill="var(--fd-muted)">0.70</text>
        <text x="61" y="255" text-anchor="end" font-size="11" fill="var(--fd-muted)">P−(U−L)/S₀</text>

        <!-- X labels: S=0 at 68, L at 162, B^in=70 at 218, U=B^out=100 at 302 -->
        <g font-size="11.5" fill="var(--fd-muted)" text-anchor="middle">
          <text x="68" y="306">0</text>
          <text x="162" y="306" class="fd-math">L</text>
          <text x="218" y="306" fill="var(--fd-crimson)" font-weight="600">Bⁱⁿ=70</text>
          <text x="302" y="306" fill="var(--fd-teal)" font-weight="600">U=Bᵒᵘᵗ=100</text>
          <text x="406" y="304" class="fd-math">S<tspan dy="3" font-size="9" font-style="normal">T</tspan></text>
        </g>

        <!-- Knocked-in layer V^(1)(T, S): crimson -->
        <!-- [0, L]: flat at y=251; [L, 100): linear from (162,251) through (218,198) to (302,118); [100, inf): jumps to 1.15 (y=78) -->
        <path d="M 68 251 L 162 251 L 302 118" fill="none" stroke="var(--fd-crimson)" stroke-width="2.4" />
        <!-- Optional L=0 extension dashed -->
        <line x1="68" y1="288" x2="162" y2="251" stroke="var(--fd-crimson)" stroke-width="1.3" stroke-dasharray="3 3" opacity="0.55" />
        <line x1="302" y1="78" x2="390" y2="78" stroke="var(--fd-crimson)" stroke-width="2.4" stroke-dasharray="6 3" />

        <!-- Unknocked layer V^(0)(T, S): teal -->
        <!-- [0, 70): coincides with V^(1) (offset slightly by -2px to make overlap visible) -->
        <path d="M 68 248 L 162 248 L 218 195" fill="none" stroke="var(--fd-teal)" stroke-width="2.2" />
        <!-- [70, inf): flat at 1.15 (y=78) -->
        <line x1="218" y1="78" x2="390" y2="78" stroke="var(--fd-teal)" stroke-width="2.6" />

        <!-- Jump callout at B^in = 70 for V^(0) -->
        <line x1="218" y1="194" x2="218" y2="83" stroke="var(--fd-teal)" stroke-width="1.4" stroke-dasharray="2 2" />
        <circle cx="218" cy="195" r="4" fill="var(--fd-panel)" stroke="var(--fd-teal)" stroke-width="2" />
        <circle cx="218" cy="78" r="4.5" fill="var(--fd-teal)" />
        <rect x="110" y="128" width="102" height="36" rx="4" fill="var(--fd-panel-alt)" stroke="var(--fd-teal)" stroke-width="0.9" />
        <text x="161" y="143" text-anchor="middle" font-size="10.5" fill="var(--fd-teal)" font-weight="600">V⁽⁰⁾ 跳跃 = 0.45</text>
        <text x="161" y="157" text-anchor="middle" font-size="9.8" fill="var(--fd-muted)">cₘτ + (U−Bⁱⁿ)/S₀</text>

        <!-- Jump callout at B^out = 100 for V^(1) -->
        <line x1="302" y1="114" x2="302" y2="83" stroke="var(--fd-crimson)" stroke-width="1.4" stroke-dasharray="2 2" />
        <circle cx="302" cy="118" r="4" fill="var(--fd-panel)" stroke="var(--fd-crimson)" stroke-width="2" />
        <circle cx="302" cy="78" r="4.4" fill="var(--fd-crimson)" />
        <text x="348" y="104" text-anchor="middle" font-size="10.5" fill="var(--fd-crimson)" font-weight="600">
          V⁽¹⁾ 敲出跳 +0.15
        </text>
      </g>

      <!-- ================= RIGHT PANEL: PHOENIX ================= -->
      <g transform="translate(442, 0)">
        <text x="215" y="22" text-anchor="middle" font-size="13.5" font-weight="650" fill="var(--fd-ink)">
          （b）凤凰到期支付 V(T, S)（展示一般情形 Bⁱⁿ &lt; Bᶜₙ &lt; U = Bᵒᵘᵗₙ）
        </text>

        <!-- Reference grid lines -->
        <!-- P+c -> y=98, P=1.00 -> y=118, 0.70 -> y=198, L kink -> y=251 -->
        <g stroke="var(--fd-grid)" stroke-width="1" stroke-dasharray="3 3">
          <line x1="58" y1="98" x2="392" y2="98" />
          <line x1="58" y1="118" x2="392" y2="118" />
          <line x1="58" y1="198" x2="392" y2="198" />
          <line x1="150" y1="44" x2="150" y2="288" />
          <line x1="204" y1="44" x2="204" y2="288" />
          <line x1="246" y1="44" x2="246" y2="288" />
          <line x1="296" y1="44" x2="296" y2="288" />
        </g>

        <!-- Axes -->
        <line x1="58" y1="288" x2="402" y2="288" stroke="var(--fd-muted)" stroke-width="1.5" marker-end="url(#fd-arr-payoff)" />
        <line x1="58" y1="292" x2="58" y2="40" stroke="var(--fd-muted)" stroke-width="1.5" marker-end="url(#fd-arr-payoff)" />

        <!-- Y labels -->
        <text x="52" y="101" text-anchor="end" font-size="10.8" fill="var(--fd-amber)" font-weight="600">P+c</text>
        <text x="52" y="122" text-anchor="end" font-size="11" fill="var(--fd-muted)">1.00</text>
        <text x="52" y="202" text-anchor="end" font-size="11" fill="var(--fd-muted)">0.70</text>

        <!-- X labels: 0 at 58, L at 150, B^in at 204, B^c at 246, U=B^out at 296 -->
        <g font-size="11.5" fill="var(--fd-muted)" text-anchor="middle">
          <text x="58" y="306">0</text>
          <text x="150" y="306" class="fd-math">L</text>
          <text x="204" y="306" fill="var(--fd-crimson)" font-weight="600">Bⁱⁿ</text>
          <text x="246" y="306" fill="var(--fd-amber)" font-weight="600">Bᶜₙ</text>
          <text x="304" y="306" fill="var(--fd-teal)" font-weight="600">U=Bᵒᵘᵗₙ</text>
          <text x="403" y="304" class="fd-math">S<tspan dy="3" font-size="9" font-style="normal">T</tspan></text>
        </g>

        <!-- Knocked-in layer V^(1)(T, S): crimson -->
        <!-- [0, L]: flat at 251; [L, B^c): linear (150,251)->(246,162); at B^c jumps up by c=20px to 142, then linear (246,142)->(296,98), then flat at 98! -->
        <path d="M 58 251 L 150 251 L 246 162" fill="none" stroke="var(--fd-crimson)" stroke-width="2.4" />
        <path d="M 246 142 L 296 98 L 388 98" fill="none" stroke="var(--fd-crimson)" stroke-width="2.4" stroke-dasharray="6 3" />
        <circle cx="246" cy="162" r="3.8" fill="var(--fd-panel)" stroke="var(--fd-crimson)" stroke-width="1.8" />
        <circle cx="246" cy="142" r="4" fill="var(--fd-crimson)" />

        <!-- Unknocked layer V^(0)(T, S): teal -->
        <!-- [0, B^in): coincides with V^(1); [B^in, B^c): flat at P=1.00 (y=118); [B^c, inf): flat at P+c (y=98) -->
        <path d="M 58 248 L 150 248 L 204 198" fill="none" stroke="var(--fd-teal)" stroke-width="2.2" />
        <line x1="204" y1="118" x2="246" y2="118" stroke="var(--fd-teal)" stroke-width="2.6" />
        <line x1="246" y1="98" x2="388" y2="98" stroke="var(--fd-teal)" stroke-width="2.6" />

        <!-- Jump at B^in on V^(0): 0.30 -->
        <line x1="204" y1="194" x2="204" y2="123" stroke="var(--fd-teal)" stroke-width="1.4" stroke-dasharray="2 2" />
        <circle cx="204" cy="198" r="4" fill="var(--fd-panel)" stroke="var(--fd-teal)" stroke-width="2" />
        <circle cx="204" cy="118" r="4.5" fill="var(--fd-teal)" />

        <!-- Digital coupon jump +c at B^c -->
        <circle cx="246" cy="118" r="3.8" fill="var(--fd-panel)" stroke="var(--fd-amber)" stroke-width="1.8" />
        <circle cx="246" cy="98" r="4.2" fill="var(--fd-amber)" />

        <rect x="86" y="128" width="110" height="36" rx="4" fill="var(--fd-panel-alt)" stroke="var(--fd-teal)" stroke-width="0.9" />
        <text x="141" y="143" text-anchor="middle" font-size="10.5" fill="var(--fd-teal)" font-weight="600">V⁽⁰⁾ 跳跃 = 0.30</text>
        <text x="141" y="157" text-anchor="middle" font-size="9.8" fill="var(--fd-muted)">(U−Bⁱⁿ)/S₀（无累积息）</text>

        <text x="318" y="84" text-anchor="middle" font-size="10.5" fill="var(--fd-amber)" font-weight="600">
          Bᶜₙ 处数字票息阶跃 +c
        </text>
        <text x="336" y="138" text-anchor="middle" font-size="10.2" fill="var(--fd-muted)">
          U=Bᵒᵘᵗₙ 时 V⁽¹⁾ 连续折平
        </text>
      </g>

      <!-- Shared Legend -->
      <g transform="translate(155, 338)" font-size="11.5" fill="var(--fd-muted)">
        <line x1="0" y1="-4" x2="22" y2="-4" stroke="var(--fd-teal)" stroke-width="2.6" />
        <text x="28" y="0">未敲入层终端支付 V⁽⁰⁾(T, S)</text>

        <line x1="210" y1="-4" x2="232" y2="-4" stroke="var(--fd-crimson)" stroke-width="2.4" stroke-dasharray="6 3" />
        <text x="238" y="0">已敲入层终端支付 V⁽¹⁾(T, S)</text>

        <circle cx="424" cy="-4" r="4" fill="var(--fd-teal)" />
        <text x="433" y="0">含等号右连续端点</text>

        <circle cx="554" cy="-4" r="4" fill="var(--fd-panel)" stroke="var(--fd-teal)" stroke-width="2" />
        <text x="563" y="0">严格不等左极限端点</text>
      </g>
    </svg>
    <figcaption>
      <strong>图 2：标准雪球与凤凰的到期日双层支付剖面对比（展示含下行权价 <span class="fd-math">L</span> 的限亏拐点与 <span class="fd-math">L = 0</span> 虚线延拓）。</strong>
      标准雪球在 <span class="fd-math">S &lt; B<sup>in</sup></span> 时同时损失累计年化到期票息 <span class="fd-math">c<sub>m</sub>τ(T)</span> 与看跌价差本金，导致 <span class="fd-math">V<sup>(0)</sup></span> 在 <span class="fd-math">B<sup>in</sup></span> 处的跳跃幅度（0.45）显著大于凤凰（0.30）；而凤凰在 <span class="fd-math">B<sup>c</sup><sub>n</sub></span> 处对两层同时施加单期数字票息阶跃 <span class="fd-math">+c</span>（基准合约中 <span class="fd-math">B<sup>c</sup><sub>n</sub> = B<sup>in</sup> = 70</span>，两处阶跃合并）。
    </figcaption>
  </figure>
</template>
