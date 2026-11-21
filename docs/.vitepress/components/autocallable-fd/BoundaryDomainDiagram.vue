<template>
  <figure class="fd-diagram" role="img" aria-labelledby="fd-fig-boundary-title">
    <svg viewBox="0 0 860 405" xmlns="http://www.w3.org/2000/svg">
      <title id="fd-fig-boundary-title">离散障碍计算域、仿射边界推进与三对角右端项消元</title>
      <defs>
        <marker id="fd-arr-bd" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 1 1.5 L 8.5 5 L 1 8.5 z" fill="var(--fd-muted)" />
        </marker>
        <marker id="fd-arr-bd-teal" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 1 1.5 L 8.5 5 L 1 8.5 z" fill="var(--fd-teal)" />
        </marker>
      </defs>

      <!-- ================= TOP PANEL: SPATIAL DOMAIN [S_min, S_max] ================= -->
      <text x="430" y="20" text-anchor="middle" font-size="13.5" font-weight="650" fill="var(--fd-ink)">
        （a）现货计算域 [Sₘᵢₙ, Sₘₐₓ] 中的离散监测障碍
      </text>

      <!-- Domain zones along S -->
      <rect x="64" y="42" width="166" height="96" fill="var(--fd-crimson-soft)" opacity="0.45" />
      <rect x="230" y="42" width="206" height="96" fill="var(--fd-panel-alt)" />
      <rect x="436" y="42" width="360" height="96" fill="var(--fd-teal-soft)" opacity="0.45" />

      <!-- Left & Right True Domain Walls -->
      <line x1="64" y1="36" x2="64" y2="146" stroke="var(--fd-ink)" stroke-width="2.6" />
      <line x1="796" y1="36" x2="796" y2="146" stroke="var(--fd-ink)" stroke-width="2.6" />

      <!-- Interior Barrier Interfaces (dashed, permeable between events!) -->
      <line x1="230" y1="42" x2="230" y2="142" stroke="var(--fd-crimson)" stroke-width="1.8" stroke-dasharray="5 3" />
      <line x1="436" y1="42" x2="436" y2="142" stroke="var(--fd-teal)" stroke-width="1.8" stroke-dasharray="5 3" />
      <line x1="504" y1="42" x2="504" y2="142" stroke="var(--fd-muted)" stroke-width="1.2" stroke-dasharray="2 3" />

      <!-- Axis line -->
      <line x1="64" y1="138" x2="814" y2="138" stroke="var(--fd-muted)" stroke-width="1.5" marker-end="url(#fd-arr-bd)" />

      <!-- Core survival region label placed cleanly inside center rectangle -->
      <text x="333" y="60" text-anchor="middle" font-size="10.6" font-weight="600" fill="var(--fd-muted)">
        核心存续区 [Bⁱⁿ, Bᵒᵘᵗₖ)
      </text>

      <!-- Excursion loop arrows across interior barriers -->
      <path d="M 262 84 C 185 68, 185 112, 262 98" fill="none" stroke="var(--fd-crimson)" stroke-width="1.8" marker-end="url(#fd-arr-bd)" />
      <text x="140" y="95" text-anchor="middle" font-size="10.5" fill="var(--fd-crimson)">
        非监测时刻可穿越回弹
      </text>

      <path d="M 404 84 C 484 68, 484 112, 404 98" fill="none" stroke="var(--fd-teal)" stroke-width="1.8" marker-end="url(#fd-arr-bd-teal)" />
      <text x="598" y="92" text-anchor="middle" font-size="10.5" fill="var(--fd-teal)">
        观察日之间允许越过 Bᵒᵘᵗ 再回落
      </text>

      <!-- Far-field brace [H, S_max] -->
      <line x1="504" y1="56" x2="792" y2="56" stroke="var(--fd-muted)" stroke-width="1.2" marker-end="url(#fd-arr-bd)" />
      <text x="648" y="50" text-anchor="middle" font-size="10.6" fill="var(--fd-ink)">
        远场缓冲带：<tspan class="fd-math">S</tspan><tspan dy="2.5" font-size="8.5">max</tspan><tspan dy="-2.5"> = max(4H, H·eʷ)，</tspan><tspan class="fd-math">V</tspan><tspan dy="2.5" font-size="8.5">S</tspan><tspan dy="-2.5"> → 0, </tspan><tspan class="fd-math">V</tspan><tspan dy="2.5" font-size="8.5">SS</tspan><tspan dy="-2.5"> → 0</tspan>
      </text>
      <text x="652" y="124" text-anchor="middle" font-size="10.4" fill="var(--fd-muted)">
        收益不再依赖 S，PDE 渐近退化为 ∂ₜV = r(t)V
      </text>

      <!-- Labels along S axis -->
      <g font-size="11.3" text-anchor="middle">
        <text x="76" y="156" font-weight="650" fill="var(--fd-ink)">Sₘᵢₙ > 0（下边界）</text>
        <text x="76" y="171" font-size="10.2" fill="var(--fd-muted)">局部仿射贴现</text>
        <text x="230" y="156" font-weight="600" fill="var(--fd-crimson)">Bⁱⁿ（内部界面）</text>
        <text x="436" y="156" font-weight="600" fill="var(--fd-teal)">Bᵒᵘᵗₖ（内部界面）</text>
        <text x="504" y="156" fill="var(--fd-muted)" class="fd-math">H</text>
        <text x="774" y="156" font-weight="650" fill="var(--fd-ink)">
          <tspan class="fd-math">S</tspan><tspan dy="3" font-size="8.5">N</tspan><tspan dy="-3"> = </tspan><tspan class="fd-math">S</tspan><tspan dy="3" font-size="8.5">max</tspan><tspan dy="-3">（上边界）</tspan>
        </text>
        <text x="774" y="171" font-size="10.2" fill="var(--fd-muted)">局部仿射贴现</text>
      </g>

      <!-- ================= BOTTOM LEFT: V(t, S_max) TRAJECTORY ================= -->
      <g transform="translate(0, 194)">
        <rect x="34" y="0" width="406" height="194" rx="6" fill="var(--fd-panel-alt)" stroke="var(--fd-grid)" />
        <text x="237" y="22" text-anchor="middle" font-size="12.5" font-weight="650" fill="var(--fd-ink)">
          （b）上边界节点 V(t, <tspan class="fd-math">S</tspan><tspan dy="2.5" font-size="8.5">max</tspan><tspan dy="-2.5">) 的后向贴现与事件重置轨迹</tspan>
        </text>

        <!-- Axes -->
        <line x1="66" y1="158" x2="414" y2="158" stroke="var(--fd-muted)" stroke-width="1.3" marker-end="url(#fd-arr-bd)" />
        <line x1="66" y1="162" x2="66" y2="38" stroke="var(--fd-muted)" stroke-width="1.3" marker-end="url(#fd-arr-bd)" />
        <text x="58" y="46" text-anchor="end" font-size="11" fill="var(--fd-ink)" class="fd-math">V</text>
        <text x="422" y="162" font-size="11" fill="var(--fd-ink)" class="fd-math">t</text>

        <!-- Vertical time lines: t_0=66, t_1(lockout)=150, t_2(KO)=242, t_3(KO)=326, T=396 -->
        <g stroke="var(--fd-grid)" stroke-dasharray="3 3">
          <line x1="150" y1="42" x2="150" y2="158" />
          <line x1="242" y1="42" x2="242" y2="158" />
          <line x1="326" y1="42" x2="326" y2="158" />
          <line x1="396" y1="42" x2="396" y2="158" />
        </g>

        <path d="M 326 92 Q 360 81 396 68" fill="none" stroke="var(--fd-teal)" stroke-width="2.2" />
        <line x1="326" y1="92" x2="326" y2="74" stroke="var(--fd-teal)" stroke-width="1.5" stroke-dasharray="2 2" />
        <path d="M 242 102 Q 284 89 326 74" fill="none" stroke="var(--fd-teal)" stroke-width="2.2" />
        <line x1="242" y1="102" x2="242" y2="80" stroke="var(--fd-teal)" stroke-width="1.5" stroke-dasharray="2 2" />
        <path d="M 150 110 Q 196 96 242 80" fill="none" stroke="var(--fd-teal)" stroke-width="2.2" />
        <line x1="150" y1="110" x2="150" y2="94" stroke="var(--fd-amber)" stroke-width="1.8" stroke-dasharray="2 2" />
        <path d="M 66 120 Q 108 108 150 94" fill="none" stroke="var(--fd-teal)" stroke-width="2.2" />

        <circle cx="396" cy="68" r="3.8" fill="var(--fd-teal)" />
        <circle cx="326" cy="74" r="3.8" fill="var(--fd-teal)" />
        <circle cx="242" cy="80" r="3.8" fill="var(--fd-teal)" />
        <circle cx="150" cy="94" r="4" fill="var(--fd-amber)" />
        <circle cx="66" cy="120" r="3.8" fill="var(--fd-teal)" />

        <text x="358" y="61" text-anchor="middle" font-size="10" fill="var(--fd-teal)">观察日重置为 Qₖ+Cₖ</text>
        <text x="284" y="116" text-anchor="middle" font-size="10" fill="var(--fd-muted)">价值近似常数时乘 e⁻ʳᵐΔᵗ</text>
        <text x="150" y="84" text-anchor="middle" font-size="10" fill="var(--fd-amber)" font-weight="600">锁定期仅叠加 +c</text>

        <g font-size="10.8" fill="var(--fd-muted)" text-anchor="middle">
          <text x="66" y="174">t₀</text>
          <text x="150" y="174" fill="var(--fd-amber)">t₁(锁定)</text>
          <text x="242" y="174">t₂(敲出)</text>
          <text x="326" y="174">t₃(敲出)</text>
          <text x="396" y="174">T</text>
        </g>
      </g>

      <!-- ================= BOTTOM RIGHT: TRIDIAGONAL RHS COUPLING ================= -->
      <g transform="translate(454, 194)">
        <rect x="0" y="0" width="372" height="194" rx="6" fill="var(--fd-panel-alt)" stroke="var(--fd-grid)" />
        <text x="186" y="22" text-anchor="middle" font-size="12.5" font-weight="650" fill="var(--fd-ink)">
          （c）θ 格式中已知边界节点向内部方程组的代入
        </text>

        <!-- Time level m+1 (right column, known) and time level m (left column, solving) -->
        <text x="108" y="45" text-anchor="middle" font-size="11" font-weight="600" fill="var(--fd-teal)">
          待求时刻 <tspan class="fd-math">t</tspan><tspan dy="2.5" font-size="8.5">m</tspan>
        </text>
        <text x="292" y="45" text-anchor="middle" font-size="11" font-weight="600" fill="var(--fd-muted)">
          已知时刻 <tspan class="fd-math">t</tspan><tspan dy="2.5" font-size="8.5">m+1</tspan>
        </text>

        <!-- Boundary node i=0 -->
        <rect x="70" y="54" width="76" height="22" rx="4" fill="var(--fd-crimson-soft)" stroke="var(--fd-crimson)" />
        <text x="108" y="69" text-anchor="middle" font-size="10.5" fill="var(--fd-crimson)" font-weight="600">V₀ᵐ (已知)</text>
        <rect x="254" y="54" width="76" height="22" rx="4" fill="var(--fd-panel)" stroke="var(--fd-muted)" />
        <text x="292" y="69" text-anchor="middle" font-size="10.5" fill="var(--fd-muted)">V₀ᵐ⁺¹</text>
        <line x1="254" y1="65" x2="150" y2="65" stroke="var(--fd-crimson)" stroke-width="1.4" marker-end="url(#fd-arr-bd)" />
        <text x="202" y="59" text-anchor="middle" font-size="9.5" fill="var(--fd-crimson)">仿射推进</text>

        <!-- Interior node i=1 -->
        <rect x="70" y="92" width="76" height="22" rx="4" fill="var(--fd-teal-soft)" stroke="var(--fd-teal)" />
        <text x="108" y="107" text-anchor="middle" font-size="10.5" fill="var(--fd-teal)" font-weight="600">首内部行 i=1</text>
        <rect x="254" y="92" width="76" height="22" rx="4" fill="var(--fd-panel)" stroke="var(--fd-muted)" />
        <text x="292" y="107" text-anchor="middle" font-size="10.5" fill="var(--fd-muted)">V₁ᵐ⁺¹</text>

        <!-- Boundary contributions into i=1 -->
        <path d="M 108 76 L 108 90" stroke="var(--fd-teal)" stroke-width="1.5" marker-end="url(#fd-arr-bd-teal)" />
        <text x="38" y="88" text-anchor="middle" font-size="9.5" fill="var(--fd-teal)">+θΔt·a₁V₀ᵐ</text>
        <path d="M 254 72 L 150 98" stroke="var(--fd-muted)" stroke-width="1.2" stroke-dasharray="3 2" marker-end="url(#fd-arr-bd)" />
        <rect x="166" y="75" width="78" height="14" rx="2" fill="var(--fd-panel-alt)" opacity="0.92" />
        <text x="205" y="85" text-anchor="middle" font-size="9.1" fill="var(--fd-muted)">+(1−θ)Δt·a₁V₀ᵐ⁺¹</text>

        <!-- Interior node i=N-1 -->
        <rect x="70" y="128" width="76" height="22" rx="4" fill="var(--fd-teal-soft)" stroke="var(--fd-teal)" />
        <text x="108" y="143" text-anchor="middle" font-size="10.5" fill="var(--fd-teal)" font-weight="600">末内部行 N−1</text>
        <rect x="254" y="128" width="76" height="22" rx="4" fill="var(--fd-panel)" stroke="var(--fd-muted)" />
        <text x="292" y="143" text-anchor="middle" font-size="10.5" fill="var(--fd-muted)">
          <tspan class="fd-math">V</tspan><tspan dy="2.5" font-size="8">N−1</tspan><tspan dy="-6.5" font-size="8">m+1</tspan>
        </text>

        <!-- Boundary node i=N -->
        <rect x="70" y="164" width="76" height="22" rx="4" fill="var(--fd-crimson-soft)" stroke="var(--fd-crimson)" />
        <text x="108" y="179" text-anchor="middle" font-size="10.5" fill="var(--fd-crimson)" font-weight="600">
          <tspan class="fd-math">V</tspan><tspan dy="2.5" font-size="8">N</tspan><tspan dy="-6.5" font-size="8">m</tspan><tspan dy="4"> (已知)</tspan>
        </text>
        <rect x="254" y="164" width="76" height="22" rx="4" fill="var(--fd-panel)" stroke="var(--fd-muted)" />
        <text x="292" y="179" text-anchor="middle" font-size="10.5" fill="var(--fd-muted)">
          <tspan class="fd-math">V</tspan><tspan dy="2.5" font-size="8">N</tspan><tspan dy="-6.5" font-size="8">m+1</tspan>
        </text>
        <line x1="254" y1="175" x2="150" y2="175" stroke="var(--fd-crimson)" stroke-width="1.4" marker-end="url(#fd-arr-bd)" />
        <text x="202" y="169" text-anchor="middle" font-size="9.5" fill="var(--fd-crimson)">仿射推进</text>

        <!-- Boundary contributions into i=N-1 -->
        <path d="M 108 164 L 108 152" stroke="var(--fd-teal)" stroke-width="1.5" marker-end="url(#fd-arr-bd-teal)" />
        <text x="38" y="160" text-anchor="middle" font-size="9.3" fill="var(--fd-teal)">
          +θΔt·c<tspan dy="2.5" font-size="7.5">N−1</tspan><tspan dy="-2.5">V</tspan><tspan dy="2.5" font-size="7.5">N</tspan><tspan dy="-6" font-size="7.5">m</tspan>
        </text>
        <path d="M 254 168 L 150 144" stroke="var(--fd-muted)" stroke-width="1.2" stroke-dasharray="3 2" marker-end="url(#fd-arr-bd)" />
      </g>
    </svg>
    <figcaption>
      <strong>图 4：计算域与仿射边界推进。</strong>
      （a）正障碍位于 <span class="fd-math">[S<sub>min</sub>, S<sub>max</sub>]</span> 内，现货可以在相邻观察之间越界后返回。（b）上边界价值近似常数时，仿射推进接近纯现金贴现。观察日按端点现货重置敲出支付或叠加当期票息。（c）已知的两端边界值进入三对角系统首末内部行的右端向量。
    </figcaption>
  </figure>
</template>
