<template>
  <figure class="fd-diagram" role="img" aria-labelledby="fd-fig-step-title">
    <svg viewBox="0 0 860 375" xmlns="http://www.w3.org/2000/svg">
      <title id="fd-fig-step-title">观察日阶跃条件在雪球与凤凰中的分区映射逻辑</title>
      <defs>
        <marker id="fd-arr-st" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 1 1.5 L 8.5 5 L 1 8.5 z" fill="var(--fd-muted)" />
        </marker>
        <marker id="fd-arr-st-crim" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 1 1.5 L 8.5 5 L 1 8.5 z" fill="var(--fd-crimson)" />
        </marker>
        <marker id="fd-arr-st-amb" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 1 1.5 L 8.5 5 L 1 8.5 z" fill="var(--fd-amber)" />
        </marker>
        <marker id="fd-arr-st-teal" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 1 1.5 L 8.5 5 L 1 8.5 z" fill="var(--fd-teal)" />
        </marker>
      </defs>

      <!-- ================= LEFT PANEL: SNOWBALL STEP CONDITION ================= -->
      <g transform="translate(0, 0)">
        <text x="220" y="20" text-anchor="middle" font-size="13.2" font-weight="650" fill="var(--fd-ink)">
          （a）雪球观察日 tₖ &lt; T：三区映射（χₖ = 1, κₖ = 1）
        </text>

        <!-- Zone tints: Zone I [56, 176], Zone II [176, 296], Zone III [296, 396] -->
        <rect x="56" y="38" width="120" height="252" fill="var(--fd-crimson-soft)" opacity="0.38" />
        <rect x="176" y="38" width="120" height="252" fill="var(--fd-panel-alt)" opacity="0.65" />
        <rect x="296" y="38" width="100" height="252" fill="var(--fd-teal-soft)" opacity="0.38" />

        <g font-size="10.2" text-anchor="middle" font-weight="600">
          <text x="116" y="54" fill="var(--fd-crimson)">Ⅰ 敲入切换区</text>
          <text x="236" y="54" fill="var(--fd-muted)">Ⅱ 原层续存区</text>
          <text x="346" y="54" fill="var(--fd-teal)">Ⅲ 敲出终止区</text>
        </g>

        <!-- Vertical barrier lines -->
        <line x1="176" y1="38" x2="176" y2="290" stroke="var(--fd-crimson)" stroke-width="1.4" stroke-dasharray="4 3" />
        <line x1="296" y1="38" x2="296" y2="290" stroke="var(--fd-teal)" stroke-width="1.4" stroke-dasharray="4 3" />

        <!-- Axes -->
        <line x1="56" y1="290" x2="404" y2="290" stroke="var(--fd-muted)" stroke-width="1.5" marker-end="url(#fd-arr-st)" />
        <line x1="56" y1="294" x2="56" y2="34" stroke="var(--fd-muted)" stroke-width="1.5" marker-end="url(#fd-arr-st)" />
        <text x="48" y="42" text-anchor="end" font-size="11.5" fill="var(--fd-ink)" class="fd-math">V</text>

        <!-- Post-event smooth curve V^(0)(t_k^+, S) (dashed muted teal) -->
        <path
          d="M 56 266 Q 116 210 176 160 Q 236 116 296 98 Q 346 86 394 82"
          fill="none"
          stroke="var(--fd-teal)"
          stroke-width="1.6"
          stroke-dasharray="4 4"
          opacity="0.55"
        />
        <!-- Post-event smooth curve V^(1)(t_k^+, S) (dashed muted crimson) -->
        <path
          d="M 56 266 Q 116 240 176 206 Q 236 164 296 126 Q 346 98 394 86"
          fill="none"
          stroke="var(--fd-crimson)"
          stroke-width="1.6"
          stroke-dasharray="4 4"
          opacity="0.6"
        />

        <!-- Pre-event V^(0)(t_k^-, S) SOLID BOLD:
             [S_min, B^in): follows V^(1)+ from (56,266) to (176,206)
             [B^in, B^out): follows V^(0)+ from (176,160) to (296,98)
             [B^out, S_max]: flat at Q_k (y=74) -->
        <path d="M 56 266 Q 116 240 176 206" fill="none" stroke="var(--fd-teal)" stroke-width="2.8" />
        <path d="M 176 160 Q 236 116 296 98" fill="none" stroke="var(--fd-teal)" stroke-width="2.8" />
        <line x1="296" y1="74" x2="394" y2="74" stroke="var(--fd-teal)" stroke-width="2.8" />

        <!-- Open / Filled Endpoint Markers -->
        <!-- At B^in (x=176): S < B^in goes to V^(1)+ (open at 206), S >= B^in stays V^(0)+ (filled at 160) -->
        <circle cx="176" cy="206" r="4" fill="var(--fd-panel)" stroke="var(--fd-teal)" stroke-width="2" />
        <circle cx="176" cy="160" r="4.4" fill="var(--fd-teal)" />
        <!-- At B^out (x=296): S < B^out stays V^(0)+ (open at 98), S >= B^out jumps to Q_k (filled at 74) -->
        <circle cx="296" cy="98" r="4" fill="var(--fd-panel)" stroke="var(--fd-teal)" stroke-width="2" />
        <circle cx="296" cy="74" r="4.4" fill="var(--fd-teal)" />

        <!-- Coupling / Reset Arrows -->
        <line x1="126" y1="205" x2="126" y2="231" stroke="var(--fd-crimson)" stroke-width="1.8" marker-end="url(#fd-arr-st-crim)" />
        <text x="118" y="196" text-anchor="middle" font-size="10" fill="var(--fd-crimson)" font-weight="600">拉取 V⁽¹⁾(tₖ⁺)</text>

        <line x1="334" y1="108" x2="334" y2="79" stroke="var(--fd-teal)" stroke-width="1.8" marker-end="url(#fd-arr-st-teal)" />
        <text x="348" y="68" text-anchor="middle" font-size="10.5" fill="var(--fd-teal)" font-weight="600">Qₖ = P+R+rₖτₖ</text>
        <text x="348" y="128" text-anchor="middle" font-size="9.8" fill="var(--fd-muted)">两层均终止于 Qₖ</text>

        <!-- X-axis labels -->
        <g font-size="11.2" text-anchor="middle" fill="var(--fd-muted)">
          <text x="56" y="308">Sₘᵢₙ</text>
          <text x="176" y="308" fill="var(--fd-crimson)" font-weight="600">Bⁱⁿ (&lt;)</text>
          <text x="296" y="308" fill="var(--fd-teal)" font-weight="600">Bᵒᵘᵗₖ (≥)</text>
          <text x="404" y="306" class="fd-math">S</text>
        </g>
      </g>

      <!-- ================= RIGHT PANEL: PHOENIX STEP CONDITION ================= -->
      <g transform="translate(442, 0)">
        <text x="210" y="20" text-anchor="middle" font-size="13.2" font-weight="650" fill="var(--fd-ink)">
          （b）凤凰观察日 tₖ &lt; T：四区映射（Bⁱⁿ &lt; Bᶜₖ &lt; Bᵒᵘᵗₖ）
        </text>

        <!-- 4 Zone tints: [48,136], [136,214], [214,302], [302,394] -->
        <rect x="48" y="38" width="88" height="252" fill="var(--fd-crimson-soft)" opacity="0.38" />
        <rect x="136" y="38" width="78" height="252" fill="var(--fd-panel-alt)" opacity="0.65" />
        <rect x="214" y="38" width="88" height="252" fill="var(--fd-amber-soft)" opacity="0.38" />
        <rect x="302" y="38" width="92" height="252" fill="var(--fd-teal-soft)" opacity="0.38" />

        <g font-size="10" text-anchor="middle" font-weight="600">
          <text x="92" y="54" fill="var(--fd-crimson)">Ⅰ 敲入无息</text>
          <text x="175" y="54" fill="var(--fd-muted)">Ⅱ 续存无息</text>
          <text x="258" y="54" fill="var(--fd-amber)">Ⅲ 续存+派息 c</text>
          <text x="348" y="54" fill="var(--fd-teal)">Ⅳ 敲出+派息 c</text>
        </g>

        <!-- Vertical barrier lines -->
        <line x1="136" y1="38" x2="136" y2="290" stroke="var(--fd-crimson)" stroke-width="1.4" stroke-dasharray="4 3" />
        <line x1="214" y1="38" x2="214" y2="290" stroke="var(--fd-amber)" stroke-width="1.4" stroke-dasharray="4 3" />
        <line x1="302" y1="38" x2="302" y2="290" stroke="var(--fd-teal)" stroke-width="1.4" stroke-dasharray="4 3" />

        <!-- Axes -->
        <line x1="48" y1="290" x2="402" y2="290" stroke="var(--fd-muted)" stroke-width="1.5" marker-end="url(#fd-arr-st)" />
        <line x1="48" y1="294" x2="48" y2="34" stroke="var(--fd-muted)" stroke-width="1.5" marker-end="url(#fd-arr-st)" />

        <!-- Post-event smooth curves V^(0)+ and V^(1)+ -->
        <path
          d="M 48 266 Q 92 222 136 184 Q 175 154 214 132 Q 258 112 302 100 Q 348 90 392 86"
          fill="none"
          stroke="var(--fd-teal)"
          stroke-width="1.6"
          stroke-dasharray="4 4"
          opacity="0.55"
        />
        <path
          d="M 48 266 Q 92 244 136 220 Q 175 196 214 172 Q 258 146 302 124 Q 348 102 392 92"
          fill="none"
          stroke="var(--fd-crimson)"
          stroke-width="1.6"
          stroke-dasharray="4 4"
          opacity="0.6"
        />

        <!-- Pre-event V^(0)(t_k^-, S) SOLID BOLD:
             Zone I [48,136): follows V^(1)+ to (136,220)
             Zone II [136,214): follows V^(0)+ from (136,184) to (214,132)
             Zone III [214,302): shifted UP by -20px (+c): from (214,112) to (302,80)
             Zone IV [302,392]: flat at P+R+c (y=70) -->
        <path d="M 48 266 Q 92 244 136 220" fill="none" stroke="var(--fd-teal)" stroke-width="2.8" />
        <path d="M 136 184 Q 175 154 214 132" fill="none" stroke="var(--fd-teal)" stroke-width="2.8" />
        <path d="M 214 112 Q 258 92 302 80" fill="none" stroke="var(--fd-teal)" stroke-width="2.8" />
        <line x1="302" y1="70" x2="392" y2="70" stroke="var(--fd-teal)" stroke-width="2.8" />

        <!-- Open / Filled Markers -->
        <circle cx="136" cy="220" r="3.8" fill="var(--fd-panel)" stroke="var(--fd-teal)" stroke-width="2" />
        <circle cx="136" cy="184" r="4.2" fill="var(--fd-teal)" />

        <circle cx="214" cy="132" r="3.8" fill="var(--fd-panel)" stroke="var(--fd-amber)" stroke-width="2" />
        <circle cx="214" cy="112" r="4.2" fill="var(--fd-amber)" />

        <circle cx="302" cy="80" r="3.8" fill="var(--fd-panel)" stroke="var(--fd-teal)" stroke-width="2" />
        <circle cx="302" cy="70" r="4.2" fill="var(--fd-teal)" />

        <!-- Arrows -->
        <line x1="96" y1="215" x2="96" y2="236" stroke="var(--fd-crimson)" stroke-width="1.7" marker-end="url(#fd-arr-st-crim)" />
        <line x1="258" y1="114" x2="258" y2="95" stroke="var(--fd-amber)" stroke-width="1.8" marker-end="url(#fd-arr-st-amb)" />
        <text x="258" y="86" text-anchor="middle" font-size="10.2" fill="var(--fd-amber)" font-weight="600">+c 平移</text>
        <text x="352" y="138" text-anchor="middle" font-size="10.2" fill="var(--fd-teal)" font-weight="600">兑付 P + R + c</text>
        <line x1="352" y1="124" x2="352" y2="75" stroke="var(--fd-teal)" stroke-width="1.5" marker-end="url(#fd-arr-st-teal)" />

        <!-- X-axis labels -->
        <g font-size="11.2" text-anchor="middle" fill="var(--fd-muted)">
          <text x="48" y="308">Sₘᵢₙ</text>
          <text x="136" y="308" fill="var(--fd-crimson)" font-weight="600">Bⁱⁿ (&lt;)</text>
          <text x="214" y="308" fill="var(--fd-amber)" font-weight="600">Bᶜₖ (≥)</text>
          <text x="302" y="308" fill="var(--fd-teal)" font-weight="600">Bᵒᵘᵗₖ (≥)</text>
          <text x="402" y="306" class="fd-math">S</text>
        </g>
      </g>

      <!-- Shared Legend -->
      <g transform="translate(88, 348)" font-size="11.3" fill="var(--fd-muted)">
        <line x1="0" y1="-4" x2="22" y2="-4" stroke="var(--fd-teal)" stroke-width="1.6" stroke-dasharray="4 4" />
        <text x="28" y="0">事件后未敲入延续值 V⁽⁰⁾(tₖ⁺, S)</text>

        <line x1="236" y1="-4" x2="258" y2="-4" stroke="var(--fd-crimson)" stroke-width="1.6" stroke-dasharray="4 4" />
        <text x="264" y="0">事件后已敲入延续值 V⁽¹⁾(tₖ⁺, S)</text>

        <line x1="472" y1="-4" x2="494" y2="-4" stroke="var(--fd-teal)" stroke-width="2.8" />
        <text x="500" y="0">施加阶跃后的事件前价值 V⁽⁰⁾(tₖ⁻, S)</text>
      </g>
    </svg>
    <figcaption>
      <strong>图 5：观察日后向阶跃映射 <span class="fd-math">V(t<sub>k</sub><sup>+</sup>, S) ↦ V(t<sub>k</sub><sup>−</sup>, S)</span> 对比。</strong>
      虚线为从 <span class="fd-math">(t<sub>k</sub>, T]</span> 回溯抵达 <span class="fd-math">t<sub>k</sub><sup>+</sup></span> 时的光滑延续价值，粗实线为施加观察日条款后的 <span class="fd-math">V<sup>(0)</sup>(t<sub>k</sub><sup>−</sup>, S)</span>。在敲出锁定期或仅派息日（<span class="fd-math">χ<sub>k</sub> = 0</span>），第 Ⅳ 区并入第 Ⅲ 区；在纯每日敲入监测日（无派息、无敲出），仅保留第 Ⅰ 区的层间切换，其余区间恒等不变。
    </figcaption>
  </figure>
</template>
