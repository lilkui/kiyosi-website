export interface MathTermEntry {
  title: string
  en: string
  html: string
}

export const MATH_TERMS: Record<string, MathTermEntry> = {
  'risk-neutral': {
    title: '风险中性测度',
    en: 'Risk-Neutral Measure, ℚ',
    html: '无套利定价理论构造的等价概率分布。通过买卖标的资产与无风险债券动态对冲随机波动后，衍生品价格不依赖投资者对股票真实涨跌的主观预期，等价于在一个虚拟概率分布 <span class="mt-math">ℚ</span> 下计算未来收益的贴现数学期望——在该分布下，标的资产扣除股息后的平均增长率恰好等于无风险利率 <span class="mt-math">r</span>。',
  },
  'piecewise-markov': {
    title: '分段马尔可夫性',
    en: 'Piecewise Markovian Property',
    html: '概率论中的“无后效性”：在相邻两次观察事件之间的开区间内，给定当前时刻的价格 <span class="mt-math">S<sub>t</sub></span> 与离散状态标记 <span class="mt-math">j</span>，未来价格的条件概率分布只取决于当前值，与历史路径如何走到当前值无关。借此可用全期望公式按时间段逐段倒推，避免对整条历史轨迹做高维积分。',
  },
  'absorbing-state': {
    title: '终止吸收态',
    en: 'Absorbing State',
    html: '马尔可夫过程中的一类特殊状态：一旦系统在某个观察时刻进入该状态（例如触发提前敲出赎回），合约立即结清终止，此后永远停留在该状态、不再产生任何后续随机现金流，因此在偏微分方程中只需直接赋为已知兑付常数。',
  },
  'sufficient-statistic': {
    title: '充分统计量',
    en: 'Sufficient Statistic',
    html: '概率统计概念：把高维样本（如存续期两百多个交易日的历史价格序列）压缩为一个低维变量时，若压缩后的变量保留了决定未来收益分布所需的全部信息，则称为充分统计量。对敲入条款而言，“历史上是否至少跌破过一次敲入线”只需 1 比特布尔值 <span class="mt-math">j ∈ {0, 1}</span> 即可完整记录。',
  },
  'brownian-motion': {
    title: '标准布朗运动',
    en: 'Standard Brownian Motion, Wₜ',
    html: '连续时间随机游走极限，又称维纳过程（Wiener Process）。满足：① <span class="mt-math">W<sub>0</sub> = 0</span> 且路径连续；② 不重叠时间段的增量相互独立；③ 任意时间步 <span class="mt-math">Δt &gt; 0</span> 上的增量服从正态分布 <span class="mt-math">W<sub>t+Δt</sub> − W<sub>t</sub> ∼ 𝒩(0, Δt)</span>。因方差为 <span class="mt-math">Δt</span>，无穷小增量 <span class="mt-math">dW<sub>t</sub></span> 的量级为 <span class="mt-math">√dt</span>，满足二次变差关系 <span class="mt-math">(dW<sub>t</sub>)<sup>2</sup> = dt</span>。',
  },
  'bsm-gbm': {
    title: 'Black–Scholes–Merton 模型',
    en: 'BSM / Geometric Brownian Motion',
    html: '经典期权定价基准模型。假设标的资产的瞬时相对收益率由确定性漂移 <span class="mt-math">(r − q)dt</span> 与常数波动率高斯噪声 <span class="mt-math">σ dW<sub>t</sub></span> 叠加而成（即几何布朗运动）。在该模型下，对数价格 <span class="mt-math">ln(S<sub>T</sub> / S<sub>0</sub>)</span> 严格服从正态分布，从而保证资产价格恒为正数。',
  },
  'local-volatility': {
    title: '局部波动率模型',
    en: 'Dupire Local Volatility, σ(t, S)',
    html: '将 BSM 模型中的常数波动率 <span class="mt-math">σ</span> 推广为时间 <span class="mt-math">t</span> 与当前资产价格 <span class="mt-math">S</span> 的确定性二元函数 <span class="mt-math">σ(t, S)</span>。它无需引入新的随机变量（仍保持一维偏微分方程结构），即可贴合真实市场中不同行权价与到期日呈现的“波动率微笑／偏斜”现象。',
  },
  'ito-lemma': {
    title: 'Itô 引理',
    en: "Itô's Lemma",
    html: '随机微积分中的复合函数求导法则。对光滑函数 <span class="mt-math">f(S<sub>t</sub>)</span> 做二阶泰勒展开：<span class="mt-math">df ≈ f′(S)dS + ½ f″(S)(dS)<sup>2</sup></span>。普通微积分中二阶项是高阶无穷小可舍去；但因随机增量 <span class="mt-math">dS ∼ O(√dt)</span>，其平方 <span class="mt-math">(dS)<sup>2</sup> = σ<sup>2</sup>S<sup>2</sup>dt</span> 与 <span class="mt-math">dt</span> 同阶，故二阶导数项会保留在 <span class="mt-math">dt</span> 漂移项中（如 <span class="mt-math">f(S)=ln S</span> 时产生 <span class="mt-math">−½σ<sup>2</sup>dt</span>）。',
  },
  'feynman-kac': {
    title: '后向 Feynman–Kac 方程',
    en: 'Backward Feynman–Kac PDE',
    html: '连接概率论条件期望与偏微分方程的核心定理。若价值函数定义为未来收益的贴现条件期望 <span class="mt-math">V(t, x) = 𝔼[e<sup>−∫r du</sup> g(X<sub>T</sub>) | X<sub>t</sub> = x]</span>，对极短步长 <span class="mt-math">Δt</span> 应用全期望公式与二元二阶泰勒展开后，随机项取期望归零，从而证明 <span class="mt-math">V(t, x)</span> 满足确定性的二阶线性抛物型偏微分方程，可由终值在 <span class="mt-math">t = T</span> 逆推至 <span class="mt-math">t = 0</span>。',
  },
  'parabolic-pde': {
    title: '线性抛物型偏微分方程',
    en: 'Linear Parabolic PDE',
    html: '对时间含一阶偏导 <span class="mt-math">∂<sub>t</sub>W</span>、对空间含二阶偏导 <span class="mt-math">∂<sub>xx</sub>W</span> 的线性偏微分方程，数学原型为物理学中的热传导／扩散方程。给定终值 <span class="mt-math">W(T, x)</span> 沿时间反向推进时（令剩余时间 <span class="mt-math">τ = T − t</span>，则 <span class="mt-math">∂<sub>τ</sub>W = ½ν ∂<sub>xx</sub>W + …</span>），空间二阶导与时间导数同号，具有抹平局部尖角、保持数值演化的适定性。',
  },
  'static-replication': {
    title: '静态复制与现金或无二元期权',
    en: 'Static Replication & Cash-or-Nothing',
    html: '静态复制指用一组初始建仓后无需中途调仓的基础合约线性拼出目标到期收益。其中“现金或无（Cash-or-Nothing, CoN）”数字看涨／看跌期权的到期支付为示性函数 <span class="mt-math"><b>1</b><sub>{S<sub>T</sub> ≥ K}</sub></span> 或 <span class="mt-math"><b>1</b><sub>{S<sub>T</sub> &lt; K}</sub></span>（跨过门槛付固定现金 1，否则付 0），在 BSM 模型下可直接由正态分布累积函数给出精确初等解析解。',
  },
  'dirichlet-affine': {
    title: 'Dirichlet 边界条件与仿射贴现',
    en: 'Dirichlet & Affine Boundary Condition',
    html: '在有限计算区间两端直接指定待求函数的值称为第一类（Dirichlet）边界条件。“仿射（Affine）函数”即一次函数加常数 <span class="mt-math">V(S) ≈ A + B·S</span>：在经济学上等价于持有 <span class="mt-math">A</span> 份现金和 <span class="mt-math">B</span> 份股票，经过 <span class="mt-math">Δt</span> 后分别乘以各自折现因子 <span class="mt-math">e<sup>−rΔt</sup></span> 与 <span class="mt-math">e<sup>−qΔt</sup></span>，即可准确推算边界节点值。',
  },
  'tridiagonal-thomas': {
    title: '三对角矩阵与 Thomas 追赶法',
    en: 'Tridiagonal System & Thomas Algorithm',
    html: '每个网格内部节点仅与左右紧邻节点耦合时，线性方程组的系数矩阵只有主对角线和紧邻上下两条次对角线非零，称为三对角矩阵。Thomas 追赶法是对三对角矩阵定制的无主元高斯消元（LU 分解）：从第一行到末行顺推消去下对角元（“追”），再从末行倒推回代求解（“赶”），耗时与内存均为最优的 <span class="mt-math">O(N)</span>。',
  },
  'cfl-condition': {
    title: 'CFL 稳定性条件',
    en: 'Courant–Friedrichs–Lewy Condition',
    html: '显式差分格式保持误差不发散的时间步长上限。直觉上，显式一步更新相当于用旧时刻相邻三点做加权平均；若时间步 <span class="mt-math">Δt</span> 相对于空间步长平方 <span class="mt-math">h<sup>2</sup></span> 过大，中心点权重会变为负数，导致微小舍入误差每步翻倍放大。隐式与半隐式格式通过联立方程组消除了这一步长限制。',
  },
  'c0-c1-discontinuity': {
    title: 'C⁰ 跳跃间断与 C¹ 折角',
    en: 'C⁰ Jump & C¹ Kink Singularity',
    html: '按高等数学可微阶数分类：<span class="mt-math">C<sup>0</sup></span> 间断（第一类跳跃间断）指函数值本身在某点左右极限不等，出现垂直断层（如数字票息线与敲出线）；<span class="mt-math">C<sup>1</sup></span> 间断指函数本身连续（属于 <span class="mt-math">C<sup>0</sup></span>），但一阶导数左右极限不等，图像出现尖锐折角（如 <span class="mt-math">max(L, S)</span> 在行权价 <span class="mt-math">L</span> 处），这两类非光滑点是有限差分误差的主要来源。',
  },
  'control-volume': {
    title: '对偶控制体积投影',
    en: 'Dual Control-Volume Projection',
    html: '围绕每个网格节点 <span class="mt-math">x<sub>i</sub></span> 取左右相邻中点围成的小区间 <span class="mt-math">C<sub>i</sub> = [x<sub>i−1/2</sub>, x<sub>i+1/2</sub>]</span> 作为其“管辖单元”（控制体积）。遇到跳跃函数时，不直接取节点单点值，而计算单元上的定积分平均值 <span class="mt-math">|C<sub>i</sub>|<sup>−1</sup>∫<sub>C<sub>i</sub></sub> ΔV dx</span>，使落在格点之间的障碍能按所占长度比例连续反映到离散方程中，消除 <span class="mt-math">O(h)</span> 阶梯抖动。',
  },
  'gauss-legendre': {
    title: '两点 Gauss–Legendre 求积',
    en: '2-Point Gauss–Legendre Quadrature',
    html: '数值计算定积分的高效公式。将区间 <span class="mt-math">[p<sub>m</sub>, p<sub>m+1</sub>]</span>（中点 <span class="mt-math">c<sub>m</sub></span>，长度 <span class="mt-math">L</span>）上的积分近似为对称两点 <span class="mt-math">c<sub>m</sub> ± L/(2√3)</span> 处函数值的算术平均乘以 <span class="mt-math">L</span>。通过精巧选取这两个无理采样位置，仅计算 2 次函数值即可对任意三次及以下多项式做到零误差精确积分。',
  },
  'sinh-grid': {
    title: '双曲正弦（sinh）网格加密',
    en: 'Hyperbolic Sine Grid Stretching',
    html: '利用双曲正弦函数 <span class="mt-math">sinh(u) = (e<sup>u</sup> − e<sup>−u</sup>)/2</span> 在 <span class="mt-math">u = 0</span> 附近斜率平缓（<span class="mt-math">sinh u ≈ u</span>）、向两侧呈指数增大的特性构造光滑非均匀网格。把锚点放在障碍线上，等距参数 <span class="mt-math">jΔξ</span> 经 <span class="mt-math">sinh</span> 映射后，能在障碍近旁排出极细密节点以捕捉剧烈跳变，在平缓远场自动拉宽步长以节省总网格数。',
  },
  'moment-upwind': {
    title: '矩匹配与迎风单侧离散',
    en: 'Moment Matching & Upwind Discretization',
    html: '“一阶矩”即随机变量的数学期望。三点空间算子通过调节左右非对角系数 <span class="mt-math">a<sub>i</sub>, c<sub>i</sub></span>，使离散一步跳变的对数均值与现货均值同时吻合连续扩散模型；当漂移过强、波动极小时，同时匹配两项会导致某侧权重为负（类似出现“负转移概率”并引发振荡），此时将负侧截断为 0、仅保留顺漂移方向的一侧差分，即数值 PDE 中的“迎风（Upwind）”格式。',
  },
  'rannacher-damping': {
    title: 'Crank–Nicolson、A/L-稳定与 Rannacher 阻尼',
    en: 'CN, A/L-Stability & Rannacher Time Stepping',
    html: '按线性代数特征值分析，误差的每个空间频率模态每步乘以放大因子 <span class="mt-math">R<sub>θ</sub>(z)</span>（<span class="mt-math">z = λ<sub>k</sub>Δt &gt; 0</span>）。<b>A-稳定</b>指对一切 <span class="mt-math">z &gt; 0</span> 有 <span class="mt-math">|R(z)| ≤ 1</span>（误差不发散）；<b>L-稳定</b>进一步要求极高频锯齿模态满足 <span class="mt-math">lim<sub>z→∞</sub> R(z) = 0</span>（快速衰减）。CN 格式（<span class="mt-math">θ = ½</span>）虽有二阶精度且 A-稳定，但 <span class="mt-math">R(∞) = −1</span> 非 L-稳定，会让阶跃间断产生持久正负抖动并炸毁二阶导数；<b>Rannacher 阻尼</b>在每次事件间断后先插 4 个 L-稳定的隐式 Euler 半步（<span class="mt-math">θ = 1</span>）滤净高频毛刺，再切回 CN 保持二阶精度。',
  },
  'cubic-spline-bezier': {
    title: '三次样条与 Bézier 过冲保护',
    en: 'Cubic Spline & Bézier Overshoot Guard',
    html: '三次样条在每个网格区间上用三次多项式插值，并令节点处一阶、二阶导数连续，从而直接求出一阶导（Delta）与二阶导（Gamma）。但在剧烈折角旁，光滑样条容易像弹簧一样鼓出超出两端节点值范围的伪波峰（过冲）。将区间三次多项式等价改写为四控制点 Bézier 曲线后，曲线必包络在控制点凸包内，据此可低成本检测并钳制局部过冲。',
  },
  'dirac-delta': {
    title: 'Dirac δ 奇异性',
    en: 'Dirac Delta Singularity',
    html: '广义函数（分布）概念：当价值函数在障碍 <span class="mt-math">S = B</span> 处存在高度为 <span class="mt-math">J</span> 的阶跃跳变时，经典一阶导数在该点趋于无穷大（不存在），在广义导数意义下表现为一个集中在 <span class="mt-math">S = B</span> 处、积分面积等于 <span class="mt-math">J</span> 的脉冲 <span class="mt-math">J·δ(S − B)</span>。此时任何有限步长差商都会随步长趋零而发散，因此引擎直接将跨跳变点的数值导数标记为不可用。',
  },
  'greeks': {
    title: 'Greeks（希腊字母敏感度）',
    en: 'Option Greeks (Partial Derivatives)',
    html: '金融工程中对合约价值多元函数 <span class="mt-math">V(t, S, σ, r)</span> 各阶偏导数的习惯命名，用于度量市场参数微变时的风险敞口与对冲比例：<b>Delta</b> <span class="mt-math">Δ = ∂V/∂S</span>（对价格一阶导）、<b>Gamma</b> <span class="mt-math">Γ = ∂<sup>2</sup>V/∂S<sup>2</sup></span>（对价格二阶导／曲率）、<b>Speed</b> <span class="mt-math">∂<sup>3</sup>V/∂S<sup>3</sup></span>（三阶导）、<b>Vega</b> <span class="mt-math">∂V/∂σ</span>（对波动率偏导）、<b>Rho</b> <span class="mt-math">∂V/∂r</span>（对利率偏导）、<b>Theta</b> <span class="mt-math">∂V/∂t</span>（对时间偏导）。',
  },
  'gaussian-convolution-fft': {
    title: '高斯转移密度卷积与 FFT',
    en: 'Gaussian Transition Convolution & FFT',
    html: '在常系数 BSM 下，相邻事件间对数价格增量 <span class="mt-math">Δx</span> 服从精确正态分布，故条件期望积分在对数均匀格点上表现为离散卷积 <span class="mt-math">∑<sub>j</sub> w<sub>i−j</sub> V<sub>j</sub></span>。当卷积核较宽时，利用离散傅里叶变换性质“数组卷积等价于频域逐点相乘”，通过快速傅里叶变换（FFT）可将单步计算量由 <span class="mt-math">O(N<sup>2</sup>)</span> 降至 <span class="mt-math">O(N log N)</span>。',
  },
  'richardson-extrapolation': {
    title: 'Richardson 外推',
    en: 'Richardson Extrapolation',
    html: '利用已知收敛阶消除主误差项的经典外推法。若网格步长为 <span class="mt-math">h</span> 时数值解满足泰勒渐近展开 <span class="mt-math">V(h) = V<sup>*</sup> + C·h<sup>2</sup> + O(h<sup>4</sup>)</span>，加密一倍得 <span class="mt-math">V(h/2) = V<sup>*</sup> + C·h<sup>2</sup>/4 + O(h<sup>4</sup>)</span>；两式按 <span class="mt-math">[4V(h/2) − V(h)] / 3 = V(h/2) + [V(h/2) − V(h)] / 3</span> 线性组合即可精确抵消 <span class="mt-math">O(h<sup>2</sup>)</span> 主误差项，获得高精度参考基准。',
  },
  'antithetic-variates': {
    title: '对偶变量法',
    en: 'Antithetic Variates',
    html: 'Monte Carlo 模拟中的方差缩减技术。利用标准正态分布的对称性（若 <span class="mt-math">Z ∼ 𝒩(0, 1)</span>，则 <span class="mt-math">−Z ∼ 𝒩(0, 1)</span>），每抽取一组随机数 <span class="mt-math">Z</span>，同时模拟一条正向路径与一条镜像路径 <span class="mt-math">−Z</span> 并取成对均值 <span class="mt-math">½(Y<sub>+</sub> + Y<sub>−</sub>)</span>。因两条路径的收益呈负相关（<span class="mt-math">Cov(Y<sub>+</sub>, Y<sub>−</sub>) &lt; 0</span>），成对均值的方差显著小于独立抽样，在相同路径数下缩小统计标准误。',
  },
}
