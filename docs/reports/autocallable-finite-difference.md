# Kiyosi 自动赎回结构（雪球、凤凰）有限差分定价：原理、实现与验证报告

> 适用版本：Kiyosi 0.21.0（提交 `95dc9115`）。
> 验证环境：Ubuntu 26.04 x86_64，Rust release 构建，Python 3.15.2，QuantLib 1.44，NumPy 2.5.5。

## 目录

1. [摘要](#_1-摘要)
2. [产品定义与支付结构](#_2-产品定义与支付结构)
3. [数学模型](#_3-数学模型)
4. [边界条件与计算域](#_4-边界条件与计算域)
5. [数值离散化与算法实现](#_5-数值离散化与算法实现)
6. [各项数值方法解决的问题及必要性](#_6-各项数值方法解决的问题及必要性)
7. [验证方法论与独立参考解](#_7-验证方法论与独立参考解)
8. [验证结果：凤凰](#_8-验证结果-凤凰)
9. [验证结果：雪球](#_9-验证结果-雪球)
10. [仓库测试套件](#_10-仓库测试套件)
11. [误差预算、局限与使用建议](#_11-误差预算、局限与使用建议)
12. [结论](#_12-结论)
13. [附录 A：源码索引](#附录-a-源码索引)
14. [附录 B：复现脚本](#附录-b-复现脚本)

---

## 1. 摘要

`FiniteDifferenceAutocallableEngine` 为雪球、二元雪球、三元雪球和凤凰定价，支持 Black–Scholes–Merton（BSM）与局部波动率模型。求解器在一维现货网格上回溯，在需要区分每日敲入状态时使用双层 PDE。观察时刻精确插入时间网格，间断支付用控制体积投影，默认采用带 Rannacher 阻尼的 Crank–Nicolson 格式。

凤凰分别指定敲出和票息日程。四类合约都可在终止时支付固定返还和按 Act/365F 折算的年化返还。模型可使用 Act/365F 或交易日方差时钟，合约观察、返还计息、利率与股息曲线仍按各自约定处理。`solve` 可复用固定估值时刻的网格，批量查询现货价格及现货 Greeks。

第 8、9 节在单位名义本金下用 QuantLib 静态复制、障碍对齐的高斯卷积和独立 Monte Carlo 检验结果。默认 800×400 网格下，凤凰和雪球的到期敲入误差分别为 $5.6\times10^{-7}$ 和 $7.4\times10^{-7}$。每日敲入分别为 $6.3\times10^{-5}$ 和 $1.04\times10^{-4}$，加密至 3200×3200 后降为 $1.4\times10^{-6}$ 和 $2.3\times10^{-6}$。第 10 节给出仓库测试结果，附录 B 给出定价与复现代码。

---

## 2. 产品定义与支付结构

### 2.1 统一的合约模型

四类产品在 Rust 中都是 `AutocallableNote<T>`，`T` 分别为 `SnowballTerms`、`BinarySnowballTerms`、`TernarySnowballTerms` 和 `PhoenixTerms`。求解器通过内部视图读取合同条款，并在同一时间轴上处理敲出、票息和敲入。

| 符号 | Python 字段 | 含义 |
|---|---|---|
| $t_0,T$ | `effective_time`、`expiry_time` | 生效和到期时刻，含日内时分秒 |
| $P$ | `principal_redemption_ratio` | 单位名义本金对应的赎回本金，默认 1 |
| $\rho_0,\rho_a$ | `rebate_rate`、`annual_rebate_rate` | 固定返还率与年化返还率，均非负，默认 0 |
| — | `barrier_state` | 严格早于估值时刻的历史，取 `no_event`、`knocked_in`、`knocked_out` 或 `None`（未知） |
| — | `calendar` | 合约观察日历 |
| $B^{\text{in}}$ | `knock_in_level` | 严格低于该水平时敲入，二元雪球无敲入 |
| — | `knock_in_observation` | 指定时钟时刻的每日交易日观察，或仅在到期观察 |

雪球、三元雪球和二元雪球用 `autocall_observations` 存放带年化敲出票息 $r_k$ 的敲出记录，未敲入到期的年化票息由 `maturity_coupon_rate` 给出。三元雪球敲入后到期改付 `minimum_coupon_rate`（$c_{\min}\le c_m$）。雪球与凤凰通过 `initial_spot`、`upper_strike`、`lower_strike` 定义亏损参与的参考价 $S_{\text{ref}}$ 和上下行权价 $U,L$。

凤凰分别用 `knock_out_observations` 和 `coupon_observations` 存放 `KnockOutObservation` 与 `CouponObservation`。两份日程各自非空且严格递增，观察时刻均在合约存续期内，可以重合，也可以在不同日期或同一天的不同时刻。每期票息 `coupon_per_period` 可以为负，通过含等号的票息障碍判断是否支付。障碍为 0 时无条件派息。凤凰票息按期给付，不累计未支付的票息。预设的 `lockout_periods` 用于展开日程，从敲出日程中省去前几期，票息和敲入照常观察。

### 2.2 现金流

记 $\tau(t)=\operatorname{Act/365F}(t_0,t)$。四类产品在敲出或未敲出到期时都支付一次返还 $R(t)=\rho_0+\rho_a\tau(t)$，以原始名义本金计。雪球年化票息也按 $\tau(t)$ 折算。设 $t_k$ 为敲出、票息或敲入事件时刻，$\chi_k$ 表示该时刻有敲出观察。$C_k(S)$ 只在凤凰的票息观察时刻取表中的值，在其他时刻为 0。记 $\Pi^{(0)}$ 和 $\Pi^{(1)}$ 分别为未敲入和已敲入且未敲出时的到期支付。

| 产品 | 敲出支付 $Q_k$ | 票息 $C_k(S)$ | $\Pi^{(0)}(S)$ | $\Pi^{(1)}(S)$ |
|---|---|---|---|---|
| 雪球 | $P+R(t_k)+r_k\tau(t_k)$ | 0 | $P+R(T)+c_m\tau(T)$ | $P+R(T)+\dfrac{\min(U,\max(L,S))-U}{S_{\text{ref}}}$ |
| 三元雪球 | $P+R(t_k)+r_k\tau(t_k)$ | 0 | $P+R(T)+c_m\tau(T)$ | $P+R(T)+c_{\min}\tau(T)$ |
| 二元雪球 | $P+R(t_k)+r_k\tau(t_k)$ | 0 | $P+R(T)+c_m\tau(T)$ | — |
| 凤凰 | $P+R(t_k)$ | $c\,\mathbf 1_{\{S\ge B^c_k\}}$ | $P+R(T)$ | $P+R(T)+\dfrac{\min(U,\max(L,S))-U}{S_{\text{ref}}}$ |

- **敲出与票息**。若 $t_k$ 有敲出观察且 $S_{t_k}\ge B^{\text{out}}_k$，支付 $Q_k$ 并终止合约。凤凰同一时刻的合资格票息与敲出款一并支付，敲出后所有票息观察失效。
- **敲入**。在敲入监测时刻，若 $S<B^{\text{in}}$，不可逆地转为已敲入。敲入本身不支付现金流。
- **到期**。若未敲出，按敲入状态支付 $\Pi^{(0)}$ 或 $\Pi^{(1)}$，并加上当期合资格的凤凰票息。到期日有敲出观察且触发时，敲出支付替代到期支付。
- **估值时刻**。历史票息已结算。当期事件按估值时刻的现货精确判断并只计入一次。

FD、求积和 Monte Carlo 引擎共用这些支付规则，见 `observation_coupon`、`knock_out_payment`、`terminal`、`below_knock_in` 和 `expiry_payment`。参见[合约条款](https://github.com/lilkui/kiyosi/blob/95dc91155223b9095d06cbbf7ba4bda5bc72b7c1/crates/kiyosi/src/instruments/autocallable.rs)和[事件结算](https://github.com/lilkui/kiyosi/blob/95dc91155223b9095d06cbbf7ba4bda5bc72b7c1/crates/kiyosi/src/instruments/autocallable/pricing.rs)。

### 2.3 预设结构

市场上常见的雪球和凤凰变体由预设展开为普通合约，引擎看到的只是展开后的条款：

| 预设 | 展开结果 |
|---|---|
| 雪球 `Standard` / `European` | 常数敲出水平与票息；每日敲入 / 仅到期敲入 |
| 雪球 `StepDown`、`BothDown` | 敲出水平（以及票息）逐期递减 |
| 雪球 `DualCoupon` | 到期票息 $c_m$ 与敲出票息 $r_k$ 分开设定 |
| 雪球 `Parachute` | 只替换最后一期的敲出水平（通常调低） |
| 雪球 `Otm`、`LossCapped` | 改变上行权价 $U$；设定下行权价 $L$ 以限制亏损 |
| 雪球 `EarlyProfit`、`Butterfly` | 按观察时间分两段或三段设定年化票息，到期票息取最后一段 |
| 凤凰 `Standard`、`StepDown` | 常数或递减敲出水平，带票息障碍 |
| 凤凰 `FixedCouponNote`、`DigitalCouponNote` | 无条件票息（FCN，$B^c=0$）或数字票息 |

因此本报告对“雪球”和“凤凰”的验证覆盖了这些预设所用的全部支付要素；第 9.5 节对其中多个变体单独做了检验。

---

## 3. 数学模型

### 3.1 标的动力学

以 Act/365F 自然时间 $t$ 表示模型日期，记 $u(t)$ 为累积方差时间，$a(t)=du/dt$。风险中性动力学为

$$
\frac{dS_t}{S_t}=\big(r(t)-q(t)\big)\,dt+
\sigma(t,S_t)\sqrt{a(t)}\,dW_t .
$$

- BSM 使用常数年化波动率 $\sigma$。局部波动率使用 `LocalVolatilitySurface`，按 Act/365F 和绝对现货做双线性插值，现货方向超出曲面时取最近端点。
- `variance_time_convention="actual_365_fixed"`（默认）有 $a(t)=1$。`"business"` 需要指定模型日历；若年化基准为 $B$ 个交易日，则交易日全天均匀累积方差时间（$a(t)=365/B$），闭市日 $a(t)=0$。`weekdays_calendar()` 的 $B$ 为 261。
- 利率与股息仍由各自的 `RateTermStructure` 决定，可以用连续复利常数或带节点的期限结构。合约观察遵循合约日历，返还与雪球票息继续按 Act/365F 计息。方差时钟与这两类约定独立。

### 3.2 分段 PDE

在两个相邻事件时刻之间，价值函数满足 Feynman–Kac 后向方程

$$
\frac{\partial V}{\partial t}+\tfrac12 a(t)\sigma^2(t,S)S^2\frac{\partial^2V}{\partial S^2}
+\big(r(t)-q(t)\big)S\frac{\partial V}{\partial S}-r(t)V=0 .
$$

求解器在每个子步中点读取 $r$、$q$、$a$ 和局部波动率。方差时钟切换点进入时间网格，使每个子步内 $a$ 恒定。若从估值时刻起有一段零方差窗口，引擎先沿确定性远期逐一结算窗口内的观察事件，若仍需随机定价，再求窗口末端以后的延续价值。

### 3.3 路径依赖的状态扩展

自动赎回产品的路径依赖有两个来源：

1. **离散敲出与票息**。在各自观察时刻施加跳跃条件。敲出支付 $Q_k$ 可以随观察时刻变化，其金额由该观察时刻的合约条款确定。
2. **敲入状态**：敲入后到期支付不同，需要一个二值状态 $j\in\{0,1\}$（0 为未敲入，1 为已敲入）。

因此，每日敲入合约求解两个价值函数 $V^{(0)}$ 和 $V^{(1)}$。它们服从同一个微分算子，只在事件时刻耦合。到期敲入合约只在 $T$ 观察敲入，此时 $V^{(1)}$ 只在终端条件中出现，单层求解即可。代码中的条件为 `daily && !starting_knocked && note.knock_in_affects_payoff()`，其中“敲入会改变支付”按产品判断：

| 产品 | `knock_in_affects_payoff()` 为真的条件 | 不成立时 |
|---|---|---|
| 雪球 | $L\ne U$ 或 $c_m\ne0$ | $\Pi^{(0)}=\Pi^{(1)}=P+R(T)$ |
| 三元雪球 | $c_{\min}\ne c_m$ | 两层到期支付相同 |
| 二元雪球 | 永不成立（没有敲入） | 始终单层 |
| 凤凰 | $L\ne U$ | $\Pi^{(0)}=\Pi^{(1)}=P+R(T)$ |

敲入不改变支付或在开始 PDE 回溯前已敲入时，引擎只建立一层。隐式及 CN 类格式也省去这类合约的每日监测节点。

### 3.4 终端与跳跃条件

记 $t^{+}$ 为事件之后（时间上更晚一侧），$t^{-}$ 为事件之前；后向求解从 $t^{+}$ 推到 $t^{-}$。以下用第 2.2 节的 $Q_k$、$C_k$、$\Pi^{(0)}$、$\Pi^{(1)}$ 统一表示四类产品；$\kappa=1$ 表示该时刻也是敲入监测日。

**终端条件**。用下标 $n$ 表示 $T$ 时刻。若到期日无票息观察，则 $C_n=0$；若无敲出观察，则 $\chi_n=0$。

$$
\begin{aligned}
V^{(1)}(T,S)&=C_n(S)+\begin{cases}Q_n,&\chi_n=1,\ S\ge B^{\text{out}}_n\\ \Pi^{(1)}(S),&\text{否则}\end{cases}\\[4pt]
V^{(0)}(T,S)&=C_n(S)+\begin{cases}Q_n,&\chi_n=1,\ S\ge B^{\text{out}}_n\\ \Pi^{(1)}(S),&\kappa=1,\ S<B^{\text{in}}\\ \Pi^{(0)}(S),&\text{否则}\end{cases}
\end{aligned}
$$

**观察日 $t_k<T$**：

$$
\begin{aligned}
V^{(1)}(t_k^-,S)&=C_k(S)+\begin{cases}Q_k,&\chi_k=1,\ S\ge B^{\text{out}}_k\\ V^{(1)}(t_k^+,S),&\text{否则}\end{cases}\\
V^{(0)}(t_k^-,S)&=C_k(S)+\begin{cases}Q_k,&\chi_k=1,\ S\ge B^{\text{out}}_k\\ V^{(1)}(t_k^+,S),&\kappa=1,\ S<B^{\text{in}}\\ V^{(0)}(t_k^+,S),&\text{否则}\end{cases}
\end{aligned}
$$

**纯敲入监测日**（每日敲入的非观察交易日）：$V^{(0)}(t^-,S)=V^{(1)}(t^+,S)$（当 $S<B^{\text{in}}$），其余情况保持不变。

**估值时刻处理**（`pricing::initial` 与确定性路径共用结算规则）：

- 已敲出：价值为 0。
- 估值时刻是每日监测时刻且 $S_0<B^{\text{in}}$：立即视为已敲入。
- 估值时刻是观察日：用 $S_0$ 计入当期票息，若敲出则直接结算。
- 估值时刻是到期日：直接返回终端支付。

### 3.5 各产品的间断结构

下表按第 7.4 节的基准条款列出各事件对间断的贡献（$\tau(T)=1$）。若同一时刻的障碍重合，应合并对应的贡献。

| 位置 | 凤凰基准 | 雪球基准 | 三元雪球 | 二元雪球 |
|---|---|---|---|---|
| 到期 $B^{\text{in}}$ 处（未敲入层） | 跳跃 $(U-B^{\text{in}})/S_{\text{ref}}=0.30$ | 跳跃 $c_m\tau(T)+(U-B^{\text{in}})/S_{\text{ref}}\approx0.45$ | 跳跃 $(c_m-c_{\min})\tau(T)\approx0.12$ | 无 |
| 到期 $B^{\text{out}}_n$ 处 | 已敲入层跳跃 $(U-\max(L,B^{\text{out}}_n))^+/S_{\text{ref}}$（基准中为 0） | 未敲入层在 $r_n=c_m$ 时连续；已敲入层跳跃 $r_n\tau(T)+(U-B^{\text{out}}_n)^+/S_{\text{ref}}\approx0.15$ | 未敲入层同雪球；已敲入层跳跃 $(r_n-c_{\min})\tau(T)$ | $r_n\ne c_m$ 时跳跃 $(r_n-c_m)\tau(T)$ |
| 观察日 $B^{\text{out}}_k$ 处 | $Q_k$ 与续存价值之差 | $Q_k$ 与续存价值之差 | 同雪球 | 同雪球 |
| 观察日 $B^c_k$ 处 | 数字票息跳跃 $c$ | 无 | 无 | 无 |
| 每日监测日 $B^{\text{in}}$ 处 | $V^{(0)}-V^{(1)}$ | $V^{(0)}-V^{(1)}$ | $V^{(0)}-V^{(1)}$ | 无 |
| $U$、$L$ 处 | 拐点 | 拐点 | 无 | 无 |

每日监测日的跳跃由两层价值的差决定，临近到期时通常增大。标准雪球的到期敲入跳跃比凤凰约高出 50%，年化到期票息越高，跳跃越显著。第 5 节的节点对齐、跳跃投影和 Rannacher 阻尼用于解析这些事件附近的价值变化。

### 3.6 静态复制恒等式（用于理论检验）

若凤凰仅有到期敲出与到期敲入，且 $L\le B^{\text{in}}\le\min(U,B^{\text{out}})$，可将价格分解为欧式产品的组合。$t_k$ 表示各票息观察时刻。

$$
V_0=(P+R(T))\,D(T)+\sum_{k=1}^{n}c\,\mathrm{CoN}^{\text{call}}(B^c_k,t_k)-\frac{(U-B^{\text{in}})\,\mathrm{CoN}^{\text{put}}(B^{\text{in}},T)+\mathrm{Put}(B^{\text{in}},T)-\mathrm{Put}(L,T)}{S_{\text{ref}}},
$$

其中 $\mathrm{CoN}$ 是现金或无（cash-or-nothing）二元期权，$D$ 为贴现因子。这里用到 $\mathbf 1_{\{S<B^{\text{in}}\}}(\max(S,L)-U)=-(U-B^{\text{in}})\mathbf 1_{\{S<B^{\text{in}}\}}-\big[(B^{\text{in}}-S)^+-(L-S)^+\big]$。

雪球类产品的下列组合取单个敲出观察日 $t_1=T$，带敲入障碍时仅在到期敲入且 $B^{\text{in}}\le B^{\text{out}}$。标准雪球还需 $L\le B^{\text{in}}\le U$。记 $A=c_m\tau(T)$、$\Delta=(r_1-c_m)\tau(T)$。

$$
\begin{aligned}
V_0^{\text{雪球}}&=(P+R(T)+A)D(T)+\Delta\,\mathrm{CoN}^{\text{call}}(B^{\text{out}},T)-A\,\mathrm{CoN}^{\text{put}}(B^{\text{in}},T)-\frac{(U-B^{\text{in}})\,\mathrm{CoN}^{\text{put}}(B^{\text{in}},T)+\mathrm{Put}(B^{\text{in}},T)-\mathrm{Put}(L,T)}{S_{\text{ref}}},\\
V_0^{\text{三元}}&=(P+R(T)+A)D(T)+\Delta\,\mathrm{CoN}^{\text{call}}(B^{\text{out}},T)-(c_m-c_{\min})\tau(T)\,\mathrm{CoN}^{\text{put}}(B^{\text{in}},T),\\
V_0^{\text{二元}}&=(P+R(T)+A)D(T)+\Delta\,\mathrm{CoN}^{\text{call}}(B^{\text{out}},T).
\end{aligned}
$$

这些恒等式不依赖 Kiyosi 的任何实现，第 8.1 和 9.1 节用 QuantLib 计算它们作为解析基准。

---

## 4. 边界条件与计算域

### 4.1 自动上边界

上边界 $S_{\max}$ 由 `diffusion_upper` 确定。$H$ 取回溯起点现货及参与网格构造的最高合约水平。构造时使用严格晚于回溯起点的敲出水平和票息障碍，并按条款加入敲入和参考水平、亏损结算行权价。二元雪球的水平来自剩余敲出日程。

$$
w=4\,\bar\sigma\sqrt{\tau_T}+\max_{e}\Big|\!-\!\ln D_r(0,e)+\ln D_q(0,e)-\tfrac12\bar\sigma^2e\Big|,\qquad
S_{\max}=\begin{cases}4H,&w\le\ln4\\ H\,e^{w},&w>\ln4.\end{cases}
$$

$\tau_T$ 和 $e$ 是从回溯起点计的 Act/365F 年数，$e$ 遍历利率与股息曲线区间的终点。$\bar\sigma$ 取 BSM 常数波动率或局部曲面在回溯时段内的最大值。方差时钟为 `"business"` 时，构造上界用的 $\bar\sigma$ 再乘 $\sqrt{365/B}$，为交易日上的自然时间波动率。显式指定 `asset_upper_boundary` 时，若需要数值网格，该边界必须大于回溯起点现货和待纳入的合约水平。

### 4.2 下边界 $S=0$

几何布朗运动以 0 为吸收态，PDE 在 $S=0$ 处退化为 $\partial_tV=rV$。实现中令下边界节点：

$$
V(t,0)=e^{-r_m\Delta t}\,V(t+\Delta t,0),
$$

事件修正也作用在 0 节点上，直接读取节点处的支付。零现货路径不会敲出，仅无条件凤凰票息会支付。有后续敲入观察的产品会在下一个监测时刻敲入，到期按第 2.2 节的 $\Pi^{(1)}(0)$ 结算。二元雪球按 $\Pi^{(0)}(0)$ 结算。

### 4.3 上边界 $S=S_{\max}$

在所有合约水平之上，收益（赎回本金、返还及适用票息）不再依赖 $S$，价值函数渐近满足 $V_S\to0$、$V_{SS}\to0$，PDE 退化为 $\partial_tV=rV$。上边界采用同样的“贴现 Dirichlet”条件，并在事件时刻施加同样的跳跃修正。第 8.3 和 9.3 节用固定空间节点数改变上边界，检验价格对计算域的敏感性。

### 4.4 有效性检查

- 上边界非有限、不大于关注水平，或网格间距无效：返回 `InvalidInput`。
- 时间网格中的事件时刻在浮点精度下不可区分：返回 `ComputationFailure`（`validate_event_resolution`）。
- 显式 Euler 不满足稳定性条件 $\Delta t\cdot\max_i|b_i|\le1$：返回 `InvalidInput`（`validate_stability`）。
- 预计工作区超过 1 GiB，或回溯超过十亿次网格更新：返回 `InvalidInput`。工作量估算计入事件和曲线节点、阻尼半步与状态层数。
- 求解过程中出现非有限值或三对角主元为零：返回 `ComputationFailure`（`unstable`）。

---

## 5. 数值离散化与算法实现

### 5.1 总体流程

`native` 先校验合约生命周期、历史状态与模型，处理已结算、已知支付和零方差区间。需要 PDE 回溯时，`solve_grid` 构造时间与空间网格，投影终端支付，再逐步后向求解。在敲出、票息与需要切换状态的敲入事件上施加跳跃修正，并重启 Rannacher 阻尼。最终用样条取延续价值，与确定性区间中已经确定的支付合并。BSM 与局部波动率通过 `Diffusion` trait 共用求解器。参见[有限差分入口](https://github.com/lilkui/kiyosi/blob/95dc91155223b9095d06cbbf7ba4bda5bc72b7c1/crates/kiyosi/src/engines/finite_difference/autocallable.rs)。

### 5.2 空间网格

**(1) 基础坐标。** `SpatialGrid` 采用 $x=\operatorname{asinh}(S/s)$ 坐标。当 $S_{\max}>4H_{\text{levels}}$ 时，$s=H_{\text{levels}}$。其余情形 $s=0$，此时基础网格在 $S$ 上均匀。$H_{\text{levels}}$ 是最高合约水平，若无待纳入的水平则取回溯起点现货。

**(2) 合约水平对齐与加密**（`grid::concentrate`，隐式和 CN 类格式启用）。需要对齐的水平集合为

$$
\mathcal L=\{S^\ast\}\cup\{B^{\text{in}}\}\cup\{L,\,U\}\cup\{B^{\text{out}}_k:\ \text{敲出生效}\}\cup\{B^c_k\},
$$

有敲入时加入参考水平 $S^\ast$ 与 $B^{\text{in}}$，其中三元雪球以敲入水平为参考。有亏损参与时加入 $L,U$。敲出水平与凤凰票息障碍取自回溯起点后的观察日程。处理步骤：

1. 对水平排序、去重，按 $g=s_c\operatorname{asinh}(S_{\max}/s_c)/N$ 筛掉过近的内部水平。
2. 以相邻水平的中点为界，把 $[0,S_{\max}]$ 划分为若干段，每段有一端是合约水平。
3. 每段先分配一个区间，再按各段的 asinh 宽度 $\operatorname{asinh}((b-a)/s_c)$ 比例分配剩余区间，尾数按最大余数法处理。若段数超过 $N$，使用基础网格。
4. 每段内节点从合约水平一侧按 sinh 规律向外展开，保留的合约水平精确落在段端点。

加密尺度为

$$
s_c=H_{\text{levels}}\cdot\max\!\Big(0.001\sqrt{\min(365\,\tau_{\text{near}},1)},\ 64\varepsilon\Big),
$$

其中 $\tau_{\text{near}}$ 取首个未来事件、曲线或曲面节点、方差时钟转折点与到期中的最近距离。

**(3) 非均匀三点算子。** 对内部节点 $S_i$，记 $h_l=S_i-S_{i-1}$、$h_r=S_{i+1}-S_i$、$\mu=r-q$：

$$
a_i=\frac{S_i}{h_l}\Big(\tilde v\,\frac{S_i}{h_l+h_r}-\mu\frac{h_r}{h_l+h_r}\Big),\quad
c_i=\frac{S_i}{h_r}\Big(\tilde v\,\frac{S_i}{h_l+h_r}+\mu\frac{h_l}{h_l+h_r}\Big),\quad
b_i=-a_i-c_i-r ,
$$

$$
\tilde v=\max\!\Big(a(t)\sigma^2,\ \mu^{+}\frac{h_r}{S_i},\ \mu^{-}\frac{h_l}{S_i}\Big).
$$

$\tilde v=a(t)\sigma^2$ 时，这正是二阶中心差分在非均匀网格上的标准形式。只有在漂移相对扩散占优（低波动或粗网格）时才启用下限，相当于加入最小的迎风人工扩散，保证 $a_i,c_i\ge0$。sinh 坐标网格（未加密时）使用同样的“扩散不小于半个漂移”约束：$\max(\tfrac12\hat\sigma^2,\tfrac12|\hat\mu|)$。

### 5.3 时间离散

**(1) 时间网格**（`TimeGrid::with_events`）：

- 在 $[0,\tau_T]$ 上取 $M$（`time_step_count`）个均匀步。
- 插入敲出和票息观察、每日敲入监测（分层模式或显式格式时）、利率和股息曲线节点、局部波动率曲面时间节点以及方差时钟的切换点。
- 与事件时刻距离在 $4\varepsilon\tau_T$ 以内的均匀节点直接替换为事件节点，避免产生微小步长。
- 未被打断的均匀步保留完全相同的 $\Delta t$，使三对角分解缓存可以复用。

**(2) 近估值段加密**：若 $[0,\tau_{\text{near}}]$ 内的步数少于 128（分层时为 64），则将该段替换为 128（或 64）等分，保留区间右端的原有节点。该区间的解直接决定最终输出的价格和 Greeks，在邻近事件估值（如观察日前一两天）时尤为关键。

**(3) θ 格式**：

$$
\big(I-\theta\Delta t\,\mathcal A\big)V^{m}=\big(I+(1-\theta)\Delta t\,\mathcal A\big)V^{m+1}+\text{边界项},
$$

| 方案 | $\theta$ | 说明 |
|---|---|---|
| `explicit_euler` | 0 | 一阶，有条件稳定，定价前做稳定性检查 |
| `implicit_euler` | 1 | 一阶，L-稳定 |
| `crank_nicolson` | ½ | 二阶，A-稳定但非 L-稳定 |
| `rannacher`（默认） | ½ + 阻尼 | 每次事件后的前两个区间各替换为两个隐式 Euler 半步，之后切回 CN |

阻尼计数器 `damping` 在终端以及每个观察和敲入事件之后重置为 2（`TimeGrid::substeps`）。

**(4) 线性代数**：三对角系统用 Thomas 算法求解，复杂度 $O(N)$。BSM 下 `Stepper` 以 $(\Delta t,\theta,r,q,\sigma\sqrt{a})$ 为键缓存最多 3 组三对角分解（前向乘子、上对角和主元倒数），均匀步之间只需前代和回代。局部波动率下系数随 $(t,S)$ 变化，各时间步需重新分解，并检查数值是否有限，遇到零主元或非有限值时报错。

### 5.4 事件处理：跳跃修正的控制体积投影

终端条件和事件跳跃在 $S$ 上不连续（凤凰票息和敲出是数字型支付，敲入会切换状态，雪球的到期票息还会加大敲入线上的跳跃，见第 3.5 节），在 $U$、$L$ 处有拐点。若直接取节点值，误差为 $O(h)$，并随障碍与节点的相对位置呈锯齿状变化。切分点按事件类型选取：终端取 $B^{\text{in}}$、$L$、$U$、生效的 $B^{\text{out}}_n$ 和凤凰的 $B^c_n$；观察日取生效的 $B^{\text{out}}_k$ 和 $B^c_k$；分层模式下的敲入监测日再加上 $B^{\text{in}}$。Kiyosi 的处理方法（`grid::project_in_coordinates`）如下：

1. 每个内部节点 $i$ 的控制体积为 $C_i=[x_{i-1/2},x_{i+1/2}]$，端点取相邻节点在坐标空间的中点。
2. 若 $C_i$ 内没有间断点，直接取中心值。若有，就在间断点处切分 $C_i$，对每个子区间用两点 Gauss–Legendre 求积（节点为 $m\pm\frac{\Delta}{2\sqrt3}$，对三次多项式精确），再按长度加权平均：

$$
\bar f_i=\sum_{\text{子区间}}\frac{|I_j|}{|C_i|}\cdot\frac{f(m_j-\rho_j)+f(m_j+\rho_j)}{2},\qquad \rho_j=\frac{|I_j|}{2\sqrt3}.
$$

3. **只投影跳跃修正量**：事件前的值写成 $V^-_i=V^+_i+\overline{\Delta}_i$，其中 $\Delta(S)=V^-(S)-V^+(S)$。被积函数里的 $V^+$ 由当前网格线性插值得到（`SpatialGrid::linear`）。光滑部分 $V^+$ 保持不变，不会被反复平均抹平；只有真正不连续的部分被单元平均。
4. 分层模式下，两层在同一组切分点上同时投影。

对齐使障碍落在对应控制体积内部。间断修正仍按实际障碍切分，包含空间网格近距离去重的水平。第 8.8 和 9.8 节检验相近水平下的误差。

### 5.5 结果提取与 Greeks

- 自然三次样条从最终网格提取价格、Delta 和 Gamma。样条过冲时会回退插值或钳制结果。Speed 可由两侧 Gamma 差分得到，要求现货扰动点位于网格内。
- 当期观察按实际现货判断。现货扰动跨越不连续的敲出、敲入或派息条件时，相关现货 Greeks 不可用。方差恢复前的确定性观察也适用这一检查；Delta 和 Gamma 按确定性远期映射与贴现因子缩放。
- BSM 的 Vega、Rho、Theta 等通过扰动重定价计算。中心定价有数值网格时，扰动计算固定中心网格上界以减轻计算域变化的影响。局部波动率的可用 Greeks 为固定曲面下的 Delta 和 Gamma。
- `engine.solve(instrument, context, spot_range=(low, high))` 返回 `FiniteDifferenceSolution`，固定合约、估值时刻、历史和市场模型，为闭区间内的现货场景复用回溯结果。`price_many` 和 `price_many_with_greeks` 保留查询顺序；当期票息、敲出与敲入按每个查询现货分别判定。自动网格覆盖查询区间，显式网格上界也须覆盖所需范围。保存解支持现货 Greeks，Vega、Rho、Theta 需要引擎重新定价。附录 B.3 含可运行示例。参见[有限差分解](https://github.com/lilkui/kiyosi/blob/95dc91155223b9095d06cbbf7ba4bda5bc72b7c1/crates/kiyosi/src/engines/finite_difference/solution.rs)。

### 5.6 特殊路径

| 情形 | 处理 |
|---|---|
| 此前已经敲出 | 价格为 0 |
| 估值时刻达到到期，或当期敲出 | 直接返回结算支付，含适用的返还和当期票息 |
| 剩余支付可确定 | 直接计算现金流的贴现值 |
| 整段剩余期限为零方差 | 逐次比较确定性远期与合约水平，按精确观察时刻结算 |
| 已有敲入或敲出观察但缺少所需历史状态，或状态与历史时序矛盾 | 分别报 `MissingHistory` 或 `InvalidInput` |

---

## 6. 各项数值方法解决的问题及必要性

| 方法 | 作用 | 实测 |
|---|---|---|
| 双层状态 | 分开传播未敲入与已敲入价值，在监测时刻切换 | 每日敲入的凤凰和雪球基准分别比到期敲入低约 0.00863 和 0.01455 |
| 水平对齐和 sinh 加密 | 将更多网格分配到障碍与行权价附近 | 到期敲入基准在同步加密下接近二阶收敛。水平相距 0.1% 时可单独加密空间（第 8.8、9.8 节） |
| 迎风扩散下限 | 维持非负非对角系数 | 波动率为 10% 的扫描场景在 1600×3200 网格上误差低于 $3\times10^{-7}$ |
| Rannacher 阻尼 | 消减事件投影引入的高频分量 | 观察日前两天，测试点的 Gamma 与参考相差低于 $10^{-6}$，无阻尼 CN 达到 $10^3$ 量级（第 8.7、9.7 节） |
| 事件插点与近估值段加密 | 在事件时刻施加跳跃条件，解析近估值区间 | 每日敲入基准在足够密的时间网格上接近二阶收敛 |
| 跳跃修正投影 | 单元平均跳跃量，保留平滑延续价值 | 空间加密结果见第 8.2、9.2 节 |
| 贴现 Dirichlet 边界 | 从零现货支付及远场渐近支付生成边界值 | 上边界由 250 调至 1000 时，四组基准价格的变化不超过 $2\times10^{-8}$ |
| 样条插值 | 在节点间直接读取现货敏感度 | 验证样本中 Delta 和 Gamma 的误差见第 8.6、9.6 节 |

---

## 7. 验证方法论与独立参考解

参考解从同一组数值条款独立计算。基准采用 Act/365F 方差时间、固定利率与股息、零返还；第 10 节和附录 B.3 补充检验独立观察日程、返还与交易日方差时钟。

### 7.1 参考 A：QuantLib 静态复制（解析）

按 3.6 节的恒等式，用 QuantLib 1.44 的 `BlackCalculator` 计算本金（及雪球到期票息）贴现、cash-or-nothing 看涨与看跌以及欧式看跌组合。这是解析解，只含浮点舍入误差，适用于“只在到期允许敲出、到期敲入”的凤凰，以及单观察日、到期敲入的雪球、三元雪球和二元雪球。

### 7.2 参考 B：障碍对齐的转移密度卷积（半解析）

在 $x=\ln(S/70)$ 坐标上取单元宽度 $h=H_0/m$，其中 $H_0=\ln(100/70)/20$。用卷积作参考的场景将正的障碍和行权价取为 $70\,e^{kH_0}$（$k$ 为整数），使间断点和拐点落在单元边界上。后向递推用精确的高斯单元概率：

$$
V_i(t)=e^{-r\Delta t}\sum_j\Big[\Phi\Big(\tfrac{x_j+h/2-x_i-\nu\Delta t}{\sigma\sqrt{\Delta t}}\Big)-\Phi\Big(\tfrac{x_j-h/2-x_i-\nu\Delta t}{\sigma\sqrt{\Delta t}}\Big)\Big]V_j(t+\Delta t),\qquad \nu=r-q-\tfrac{\sigma^2}{2},
$$

短卷积核用直接卷积，长卷积核用 FFT。核半宽约 12 个标准差，计算域以现货为中心向两侧各扩展 10 个标准差并留出漂移余量。支付和事件处理由 Python 独立实现。下表中相邻差值之比接近 4，与二阶收敛相符。

| $m$ | 凤凰，到期敲入 | 凤凰，每日敲入 | 雪球，到期敲入 | 雪球，每日敲入 |
|---|---|---|---|---|
| 5 | 1.0009196819 | 0.9921525814 | 1.0132142484 | 0.9984899542 |
| 10 | 1.0009237023 | 0.9922559951 | 1.0132184291 | 0.9986236166 |
| 20 | 1.0009247074 | 0.9922818899 | 1.0132194742 | 0.9986570970 |
| 40 | 1.0009249586 | 0.9922883661 | 1.0132197355 | 0.9986654712 |
| 相邻差值之比 | 4.000, 4.000 | 3.994, 3.998 | 4.000, 4.000 | 3.992, 3.998 |

最终参考值取 $m=40,80,160$（每日敲入取 $80,160,320$），用最细两级结果做 Richardson 外推。附录脚本以两次外推之差及最后一次外推修正量中的较大者估计离散误差。

### 7.3 参考 C：事件日精确抽样的 Monte Carlo

在所有事件日上按 GBM 精确分布 $\ln S_{t+\Delta}=\ln S_t+\nu\Delta+\sigma\sqrt\Delta Z$ 抽样，使用对偶变量。离散监测在事件日上精确抽样，只有统计误差，没有离散化偏差。局部波动率场景使用对数 Euler 格式，子步不超过 1/4 天。所列标准误只量化抽样误差。

### 7.4 基准合约

除非另有说明，凤凰和雪球各使用一份“标准一年期月度”合约，两者共用日期、水平和市场参数：

| 项目 | 凤凰 | 雪球 |
|---|---|---|
| 生效与估值 | 2025-01-02 00:00 | 同左 |
| 敲出与票息观察日 | 2025-02-03、03-03、04-02、05-02、06-02、07-02、08-04、09-02、10-02、11-03、12-02、2026-01-02（均为工作日） | 敲出日程同左，年化观察票息随敲出支付 |
| $S_0=S_{\text{ref}}=U$ | 100 | 100 |
| $B^{\text{out}}$ / $B^{\text{in}}$ | 100 / 70 | 100 / 70 |
| 票息 | $B^c=70$，$c=0.8\%$ 每期 | $r_k=c_m=15\%$ 年化（按 Act/365F 从生效日计息，$\tau_T=1$） |
| $L$, $P$, $\rho_0$, $\rho_a$ | 0, 1, 0, 0 | 同左 |
| 市场 | $r=3\%$，$q=1\%$，$\sigma=25\%$ | 同左 |
| 敲入 | “到期敲入”或“每日敲入”（工作日日历 00:00，共 262 个监测日，与 `knock_in_observation_schedule` 一致） | 同左 |

三元雪球和二元雪球基准与雪球基准相同，只是分别改为敲入后支付最低票息 $c_{\min}=3\%$，以及去掉敲入。

Richardson 外推参考价格（四舍五入至小数点后九位）：

| 合约 | 到期敲入 | 每日敲入 |
|---|---|---|
| 凤凰 | 1.000925042 | 0.992290525 |
| 雪球 | 1.013219823 | 0.998668263 |
| 三元雪球 | 1.033151508 | 1.028417875 |
| 二元雪球 | 1.038992508（无敲入） | — |

---

## 8. 验证结果：凤凰

### 8.1 理论检验：静态复制解析基准

比较单期与 12 期凤凰。两种合约均只在到期敲出和敲入，分别取 $(c,L)=(0.8\%,0)、(-2\%,50)、(5\%,60)$。 波动率依次为 15%、30%、50%，现货为 55、70、75、90、100、120、150。使用第 3.6 节的组合和 QuantLib 计算参考价格，表中为绝对误差。

| 合约 | 例数 | 默认网格最大误差 | 默认网格平均误差 | 3200×3200 最大误差 |
| --- | --- | --- | --- | --- |
| 单期凤凰 | 63 | 3.19e-05 | 6.07e-06 | 1.44e-06 |
| 12 期凤凰 | 63 | 7.78e-05 | 8.67e-06 | 3.79e-06 |

### 8.2 空间与时间收敛性

同步加密的价格误差相对第 7.4 节的卷积外推值计算。

| 网格 | 到期敲入误差 | 每日敲入误差 |
| --- | --- | --- |
| 400×200 | 2.40e-06 | 1.10e-04 |
| 800×400 | 5.63e-07 | 6.25e-05 |
| 1600×800 | 1.47e-07 | 2.37e-05 |
| 1600×1600 | 9.18e-09 | 5.59e-06 |
| 3200×3200 | 2.75e-09 | 1.38e-06 |
| 6400×3200 | 9.04e-09 | 1.38e-06 |

固定 $M=3200$ 增加空间步数的结果如下。每日敲入列以 6400×3200 的价格为基准，以减弱共同的时间误差。

| 空间步数 | 到期敲入误差 | 每日敲入空间差异 |
| --- | --- | --- |
| 200 | -2.50e-06 | -1.17e-06 |
| 400 | -5.41e-07 | -6.13e-07 |
| 800 | -1.36e-07 | -1.08e-07 |
| 1600 | -2.52e-08 | -2.60e-08 |
| 3200 | 2.75e-09 | -5.58e-09 |

固定 $N=3200$ 比较时间格式。每格依次给出到期敲入和每日敲入的有符号误差。

| 时间步数 | Rannacher | Crank–Nicolson | 隐式 Euler |
| --- | --- | --- | --- |
| 200 | 2.95e-06 / 1.11e-04 | 9.58e-04 / -9.43e-04 | 8.11e-05 / 2.25e-04 |
| 400 | 7.02e-07 / 6.26e-05 | -6.25e-04 / 3.17e-04 | 4.15e-05 / 1.55e-04 |
| 800 | 1.74e-07 / 2.37e-05 | 4.63e-04 / 3.09e-03 | 2.15e-05 / 9.12e-05 |
| 1600 | 3.71e-08 / 5.61e-06 | 1.19e-03 / -1.05e-03 | 1.12e-05 / 4.93e-05 |
| 3200 | 2.75e-09 / 1.38e-06 | -1.63e-03 / 1.93e-05 | 5.62e-06 / 2.56e-05 |

到期敲入时，Rannacher 在时间误差占主导的区间接近二阶，隐式 Euler 接近一阶。每日敲入约有 261 个未来监测点，低时间步数下频繁重启阻尼，收敛较慢。将时间步数从 1600 加倍至 3200 后，Rannacher 的每日敲入误差约为原来的四分之一。无阻尼 CN 在这些网格上出现明显的非单调误差。

### 8.3 计算域敏感性

固定 1600×1600 网格。自动边界为 400。

| 上边界 | 到期敲入价格 | 每日敲入价格 |
| --- | --- | --- |
| 250 | 1.0009250545 | 0.9922961092 |
| 400 | 1.0009250516 | 0.9922961122 |
| 1000 | 1.0009250486 | 0.9922961096 |

两种敲入方式的最大价格变动为 5.88e-09。

### 8.4 多方法交叉验证

独立 Monte Carlo 使用 400 万条对偶路径，表内 ± 后为一个标准误。求积与 FD 均使用 Kiyosi 0.21.0。

| 方法 | 到期敲入价格 | 每日敲入价格 |
| --- | --- | --- |
| 卷积外推 | 1.000925042 | 0.992290525 |
| 独立 Monte Carlo | 1.000860418 ± 4.09e-05 | 0.992310796 ± 4.34e-05 |
| FD 800×400 | 1.000925606 | 0.992353044 |
| FD 1600×1600 | 1.000925052 | 0.992296112 |
| FD 3200×3200 | 1.000925045 | 0.992291900 |
| 求积（默认） | 1.000925010 | 0.992286727 |

### 8.5 参数扫描

每格依次给出到期敲入和每日敲入相对卷积参考的有符号误差。逐期降敲的水平取 `70 * exp(k * H0)`，$k$ 从 20 逐期递减到 9。

| 场景 | 800×400 | 1600×3200 |
| --- | --- | --- |
| 波动率 10% | -3.23e-07 / 8.01e-07 | -1.60e-07 / -1.64e-07 |
| 波动率 60% | 7.08e-06 / 3.96e-05 | 1.66e-06 / 2.54e-06 |
| $r=-1\%,q=0$ | 2.17e-07 / 7.17e-05 | -1.64e-07 / 1.46e-06 |
| 现货 72 | 4.69e-06 / 1.13e-04 | 9.63e-07 / 2.49e-06 |
| 逐期降敲 | 1.13e-06 / 3.85e-05 | 1.38e-07 / 1.60e-06 |
| 每期票息 −1% | 2.29e-06 / 6.06e-05 | 6.83e-07 / 1.97e-06 |
| 锁定前三期敲出 | 4.67e-07 / 8.84e-05 | -4.92e-08 / 1.86e-06 |
| 无条件票息 | 6.62e-07 / 6.20e-05 | 3.58e-09 / 1.37e-06 |

### 8.6 Greeks 验证

比较 800×1600 网格的 Delta、Gamma 与 Vega。参考值使用卷积外推的中心差分，现货步长 0.05，波动率步长 0.001。每格依次给出 FD 与参考值。

| 敲入 | 现货 | Delta | Gamma | Vega |
| --- | --- | --- | --- | --- |
| 到期 | 72 | 0.0131531 / 0.0131529 | -0.000481828 / -0.000481832 | -0.485643 / -0.485613 |
| 到期 | 80 | 0.00865499 / 0.00865518 | -0.000559206 / -0.000559098 | -0.656187 / -0.656148 |
| 到期 | 90 | 0.00387911 / 0.00387938 | -0.000391635 / -0.000391689 | -0.546159 / -0.546158 |
| 到期 | 100 | 0.000987166 / 0.000987093 | -0.00017818 / -0.000178182 | -0.23941 / -0.239426 |
| 到期 | 110 | 9.39392e-05 / 9.39753e-05 | -2.75729e-05 / -2.75688e-05 | -0.0408189 / -0.0408397 |
| 每日 | 72 | 0.0149094 / 0.0149066 | -0.000334959 / -0.000333958 | -0.271272 / -0.27117 |
| 每日 | 80 | 0.0109735 / 0.0109734 | -0.000556285 / -0.00055608 | -0.618174 / -0.618061 |
| 每日 | 90 | 0.00590496 / 0.00590577 | -0.000441869 / -0.000441895 | -0.612214 / -0.612177 |
| 每日 | 100 | 0.0022251 / 0.0022256 | -0.000284719 / -0.000284736 | -0.30244 / -0.302483 |
| 每日 | 110 | 0.000402467 / 0.000402802 | -8.74496e-05 / -8.74797e-05 | -0.0645399 / -0.0645838 |

### 8.7 临近观察日的数值稳定性

估值设为 2025-06-30，距下一次敲出观察两天。取每日敲入与默认网格，观察敲出线处 $S_0=100$ 及靠近敲入线的 $S_0=72$。参考 Gamma 使用现货步长 0.02。

| 计算方法 | 价格（现货 100） | Gamma（现货 100） | 价格（现货 72） | Gamma（现货 72） |
| --- | --- | --- | --- | --- |
| 卷积外推 | 1.0090419 | -0.00026692461 | 0.7708559 | -0.0015915183 |
| Rannacher | 1.0090539 | -0.00026712259 | 0.77097806 | -0.0016119176 |
| Crank–Nicolson | 1.00705 | 1322.6726 | 0.77069091 | -0.0016132364 |
| 隐式 Euler | 1.0090841 | -0.00026811117 | 0.77128869 | -0.0016214756 |

无阻尼 CN 在敲出线附近产生高频振荡。Rannacher 将该点的 Gamma 恢复到参考值附近。现货恰好为 70 且处于当期每日敲入观察时刻时，Rannacher 的 Gamma 返回 `None`，因为现货扰动会跨越敲入跳跃。

### 8.8 相近合约水平的网格误差

同时改变各期敲出水平，保持参考价和上行权价为 100。表中为到期敲入 FD 价格与 2048 步求积的绝对差值。

| 敲出水平 | 800×400 | 800×1600 | 1600×400 | 3200×1600 |
| --- | --- | --- | --- | --- |
| 99.5 | 8.12e-07 | 1.80e-07 | 6.65e-07 | 3.86e-08 |
| 99.9 | 4.19e-06 | 3.53e-06 | 7.70e-07 | 3.89e-08 |
| 100.1 | 4.13e-06 | 3.46e-06 | 8.08e-07 | 3.95e-08 |
| 100.5 | 6.78e-07 | 2.01e-08 | 6.76e-07 | 3.09e-08 |

水平越接近，网格空间分辨率越重要。加密空间后，两个相距 0.1% 水平的场景误差均降低。

### 8.9 局部波动率

常数曲面设为 25%，两种敲入方式的 FD 价格均与 BSM 相同。偏斜曲面的现货节点为 50、70、100、130、160，生效时波动率为 40%、32%、25%、21%、19%，到期时为 36%、30%、24%、21%、20%。独立对数 Euler MC 使用 100 万条对偶路径，最大步长 1/4 天。

| 敲入 | 400² | 800² | 1600² | 3200² | 独立 MC ± 标准误 | FD − MC |
| --- | --- | --- | --- | --- | --- | --- |
| 到期 | 0.9959756 | 0.9959743 | 0.9959740 | 0.9959739 | 0.9959356 ± 9.31e-05 | +0.41 SE |
| 每日 | 0.9870447 | 0.9870066 | 0.9869889 | 0.9869848 | 0.9868897 ± 9.67e-05 | +0.98 SE |

差异与本次抽样的标准误同量级。该比较的分辨率受抽样误差和 Euler 时间离散影响。

---

## 9. 验证结果：雪球

### 9.1 理论检验：静态复制解析基准

雪球变体均只在到期敲出。含敲入障碍的合约只在到期敲入，敲出年化票息取 15%。 波动率依次为 15%、30%、50%，现货为 55、70、75、90、100、120、150。使用第 3.6 节的组合和 QuantLib 计算参考价格，表中为绝对误差。

| 合约 | 例数 | 默认网格最大误差 | 默认网格平均误差 | 3200×3200 最大误差 |
| --- | --- | --- | --- | --- |
| 标准雪球，$c_m=15\%$，$L=0$ | 21 | 1.66e-05 | 5.02e-06 | 1.04e-06 |
| 双票息，$c_m=5\%$ | 21 | 2.00e-05 | 6.04e-06 | 1.25e-06 |
| 限亏，$L=60$ | 21 | 3.96e-05 | 8.98e-06 | 1.78e-06 |
| 三元雪球，$c_m=10\%$，$c_{\min}=2\%$ | 21 | 5.12e-06 | 1.54e-06 | 3.20e-07 |
| 二元雪球，$c_m=3\%$ | 21 | 2.51e-06 | 8.66e-07 | 1.55e-07 |

### 9.2 空间与时间收敛性

同步加密的价格误差相对第 7.4 节的卷积外推值计算。

| 网格 | 到期敲入误差 | 每日敲入误差 |
| --- | --- | --- |
| 400×200 | 3.57e-06 | 1.83e-04 |
| 800×400 | 7.44e-07 | 1.04e-04 |
| 1600×800 | 1.71e-07 | 3.94e-05 |
| 1600×1600 | -2.88e-08 | 9.27e-06 |
| 3200×3200 | -6.37e-09 | 2.28e-06 |
| 6400×3200 | 9.56e-09 | 2.29e-06 |

固定 $M=3200$ 增加空间步数的结果如下。每日敲入列以 6400×3200 的价格为基准，以减弱共同的时间误差。

| 空间步数 | 到期敲入误差 | 每日敲入空间差异 |
| --- | --- | --- |
| 200 | -6.99e-06 | -1.79e-06 |
| 400 | -1.17e-06 | -4.17e-07 |
| 800 | -3.63e-07 | -1.13e-07 |
| 1600 | -7.81e-08 | -2.66e-08 |
| 3200 | -6.37e-09 | -5.00e-09 |

固定 $N=3200$ 比较时间格式。每格依次给出到期敲入和每日敲入的有符号误差。

| 时间步数 | Rannacher | Crank–Nicolson | 隐式 Euler |
| --- | --- | --- | --- |
| 200 | 4.74e-06 / 1.83e-04 | 1.12e-03 / -2.60e-03 | 1.31e-04 / 3.70e-04 |
| 400 | 1.10e-06 / 1.04e-04 | 1.11e-03 / 1.89e-03 | 6.55e-05 / 2.56e-04 |
| 800 | 2.43e-07 / 3.94e-05 | 1.18e-04 / 3.62e-03 | 3.21e-05 / 1.51e-04 |
| 1600 | 4.29e-08 / 9.29e-06 | 2.69e-03 / -2.01e-03 | 1.54e-05 / 8.16e-05 |
| 3200 | -6.37e-09 / 2.28e-06 | -4.93e-03 / 4.07e-04 | 7.70e-06 / 4.24e-05 |

到期敲入时，Rannacher 在时间误差占主导的区间接近二阶，隐式 Euler 接近一阶。每日敲入约有 261 个未来监测点，低时间步数下频繁重启阻尼，收敛较慢。将时间步数从 1600 加倍至 3200 后，Rannacher 的每日敲入误差约为原来的四分之一。无阻尼 CN 在这些网格上出现明显的非单调误差。

### 9.3 计算域敏感性

固定 1600×1600 网格。自动边界为 400。

| 上边界 | 到期敲入价格 | 每日敲入价格 |
| --- | --- | --- |
| 250 | 1.0132198057 | 0.9986775346 |
| 400 | 1.0132197937 | 0.9986775332 |
| 1000 | 1.0132197865 | 0.9986775308 |

两种敲入方式的最大价格变动为 1.93e-08。

### 9.4 多方法交叉验证

独立 Monte Carlo 使用 400 万条对偶路径，表内 ± 后为一个标准误。求积与 FD 均使用 Kiyosi 0.21.0。

| 方法 | 到期敲入价格 | 每日敲入价格 |
| --- | --- | --- |
| 卷积外推 | 1.013219823 | 0.998668263 |
| 独立 Monte Carlo | 1.013143688 ± 5.11e-05 | 0.998704648 ± 5.58e-05 |
| FD 800×400 | 1.013220567 | 0.998772328 |
| FD 1600×1600 | 1.013219794 | 0.998677533 |
| FD 3200×3200 | 1.013219816 | 0.998670548 |
| 求积（默认） | 1.013219768 | 0.998661687 |

三元、二元雪球基准的 FD 误差如下。

| 合约 | 卷积参考价格 | 800×400 | 1600×1600 | 3200×3200 |
| --- | --- | --- | --- | --- |
| 三元雪球，到期敲入 | 1.033151508 | -4.59e-07 | -2.74e-07 | -6.90e-08 |
| 三元雪球，每日敲入 | 1.028417875 | 3.40e-05 | 2.82e-06 | 7.01e-07 |
| 二元雪球 | 1.038992508 | 3.74e-07 | -4.62e-08 | -1.45e-08 |

三元雪球的每日敲入跳跃较小，默认误差约为标准雪球的三分之一。

### 9.5 参数扫描

每格依次给出到期敲入和每日敲入相对卷积参考的有符号误差。逐期降敲的水平取 `70 * exp(k * H0)`，$k$ 从 20 逐期递减到 9。

| 场景 | 800×400 | 1600×3200 |
| --- | --- | --- |
| 波动率 10% | -4.85e-07 / 1.58e-06 | -2.64e-07 / -2.62e-07 |
| 波动率 60% | 6.88e-06 / 3.46e-05 | 1.64e-06 / 2.54e-06 |
| $r=-1\%,q=0$ | 4.88e-07 / 1.19e-04 | -2.05e-07 / 2.53e-06 |
| 现货 72 | 3.65e-06 / 1.97e-04 | 7.18e-07 / 4.07e-06 |
| 逐期降敲 | -1.42e-06 / 5.50e-05 | -5.56e-07 / 1.82e-06 |
| $r=2\%,q=8\%$ | 6.70e-07 / 1.39e-04 | -1.59e-07 / 3.14e-06 |
| 到期票息 5% | 1.69e-06 / 7.64e-05 | 2.78e-07 / 1.96e-06 |
| 末期敲出水平约 83.67 | -1.87e-07 / 8.84e-05 | -3.14e-07 / 1.99e-06 |

### 9.6 Greeks 验证

比较 800×1600 网格的 Delta、Gamma 与 Vega。参考值使用卷积外推的中心差分，现货步长 0.05，波动率步长 0.001。每格依次给出 FD 与参考值。

| 敲入 | 现货 | Delta | Gamma | Vega |
| --- | --- | --- | --- | --- |
| 到期 | 72 | 0.0127675 / 0.0127675 | -0.000445896 / -0.000445894 | -0.532517 / -0.532484 |
| 到期 | 80 | 0.00870682 / 0.00870687 | -0.000542409 / -0.000542363 | -0.742108 / -0.742068 |
| 到期 | 90 | 0.00344599 / 0.00344627 | -0.000476167 / -0.000476154 | -0.658642 / -0.65863 |
| 到期 | 100 | 0.000144414 / 0.000144389 | -0.000152179 / -0.000152178 | -0.278568 / -0.278584 |
| 到期 | 110 | -0.000196513 / -0.000196501 | 2.36022e-05 / 2.3586e-05 | -0.034738 / -0.034761 |
| 每日 | 72 | 0.0161436 / 0.0161395 | -0.000206802 / -0.000204938 | -0.18059 / -0.180403 |
| 每日 | 80 | 0.0128932 / 0.0128928 | -0.000560565 / -0.000560339 | -0.709954 / -0.709778 |
| 每日 | 90 | 0.00694815 / 0.00694939 | -0.000574433 / -0.000574365 | -0.794993 / -0.794941 |
| 每日 | 100 | 0.00223891 / 0.00224002 | -0.000334895 / -0.000334948 | -0.393828 / -0.393896 |
| 每日 | 110 | 0.000322084 / 0.000322517 | -7.72178e-05 / -7.72843e-05 | -0.0759785 / -0.0760388 |

到期敲入且现货为 110 时，Delta 为负、Gamma 为正。对这份基准雪球，现货升高会提高提前敲出的概率，缩短按 15% 年化票息计息的持有期。

### 9.7 临近观察日的数值稳定性

估值设为 2025-06-30，距下一次敲出观察两天。取每日敲入与默认网格，观察敲出线处 $S_0=100$ 及靠近敲入线的 $S_0=72$。参考 Gamma 使用现货步长 0.02。

| 计算方法 | 价格（现货 100） | Gamma（现货 100） | 价格（现货 72） | Gamma（现货 72） |
| --- | --- | --- | --- | --- |
| 卷积外推 | 1.0791428 | -0.00029403304 | 0.76133309 | -0.00097103431 |
| Rannacher | 1.0791614 | -0.00029338796 | 0.76154349 | -0.0010155327 |
| Crank–Nicolson | 1.075622 | 2345.827 | 0.76102588 | -0.0009972712 |
| 隐式 Euler | 1.0792087 | -0.00029197403 | 0.76208767 | -0.0010791718 |

无阻尼 CN 在敲出线附近产生高频振荡。Rannacher 将该点的 Gamma 恢复到参考值附近。现货恰好为 70 且处于当期每日敲入观察时刻时，Rannacher 的 Gamma 返回 `None`，因为现货扰动会跨越敲入跳跃。

### 9.8 相近合约水平的网格误差

同时改变各期敲出水平，保持参考价和上行权价为 100。表中为到期敲入 FD 价格与 2048 步求积的绝对差值。

| 敲出水平 | 800×400 | 800×1600 | 1600×400 | 3200×1600 |
| --- | --- | --- | --- | --- |
| 99.5 | 2.45e-06 | 1.45e-06 | 1.10e-06 | 5.47e-08 |
| 99.9 | 4.31e-05 | 4.20e-05 | 1.71e-06 | 5.56e-08 |
| 100.1 | 4.57e-05 | 4.47e-05 | 1.95e-06 | 6.53e-08 |
| 100.5 | 2.15e-06 | 1.02e-06 | 1.05e-06 | 3.63e-08 |

水平越接近，网格空间分辨率越重要。加密空间后，两个相距 0.1% 水平的场景误差均降低。

### 9.9 局部波动率

常数曲面设为 25%，两种敲入方式的 FD 价格均与 BSM 相同。偏斜曲面的现货节点为 50、70、100、130、160，生效时波动率为 40%、32%、25%、21%、19%，到期时为 36%、30%、24%、21%、20%。独立对数 Euler MC 使用 100 万条对偶路径，最大步长 1/4 天。

| 敲入 | 400² | 800² | 1600² | 3200² | 独立 MC ± 标准误 | FD − MC |
| --- | --- | --- | --- | --- | --- | --- |
| 到期 | 1.0074206 | 1.0074193 | 1.0074191 | 1.0074191 | 1.0073858 ± 1.13e-04 | +0.30 SE |
| 每日 | 0.9919075 | 0.9918429 | 0.9918133 | 0.9918063 | 0.9916904 ± 1.20e-04 | +0.97 SE |

差异与本次抽样的标准误同量级。该比较的分辨率受抽样误差和 Euler 时间离散影响。

---

## 10. 仓库测试套件

在该版本源码和 release 构建的 Python wheel 上运行相关测试，Rust 共 106 项通过，Python 共 314 项通过，另有 952 个子测试通过。

| 测试范围 | Rust 测试 | Python 测试 |
|---|---|---|
| 凤凰、雪球、变体与预设 | `phoenix`、`snowball`、`snowball_variants`、`autocallable_presets` | `test_phoenix.py`、`test_snowball.py`、`test_snowball_variants.py`、`test_autocallable_presets.py` |
| FD 精度、边界、历史与 Greeks | `autocallable_finite_difference` | `test_autocallable_finite_difference.py`、`test_autocallable_fd_accuracy.py`、`test_autocallable_fd_regressions.py`、`test_autocallable_fd_validation.py` |
| 局部波动率、模型参考与隐含票息 | `local_volatility_structured`、`implied_coupon`、`autocallable_monte_carlo` | `test_local_volatility_structured.py`、`test_quantlib_profiles.py`、`test_implied_coupon.py` |
| 终止返还、方差时钟、可复用解 | `autocallable_rebate`、`variance_time_conventions`、`finite_difference_solution` | `test_autocallable_rebate.py`、`test_variance_time_conventions.py`、`test_finite_difference_solution.py` |

独立凤凰日程包含仅敲出、仅派息及同一时刻同时发生两项观察的情况。返还测试覆盖提前敲出与未敲出到期，保存解测试覆盖现货跨越当期障碍，以及在零方差区间内逐一处理观察。

---

## 11. 误差预算、局限与使用建议

| 用途 | 基准网格 | 第 7.4 节合约上的绝对误差 |
|---|---|---|
| 到期敲入基础定价 | 800×400 | 凤凰约 $5.6\times10^{-7}$，雪球约 $7.4\times10^{-7}$ |
| 每日敲入基础定价 | 800×400 | 凤凰约 $6.3\times10^{-5}$，雪球约 $1.04\times10^{-4}$ |
| 每日敲入，降低时间误差 | 1600×1600 | 凤凰约 $5.6\times10^{-6}$，雪球约 $9.3\times10^{-6}$ |
| 每日敲入，进一步加密 | 3200×3200 | 凤凰约 $1.4\times10^{-6}$，雪球约 $2.3\times10^{-6}$ |

- **空间误差**。相近敲出水平与行权价会增加局部误差。分方向加密空间、时间网格，可区分这一误差与每日敲入的时间误差。
- **时间误差**。频繁监测会反复重启阻尼。每日敲入若需更高精度，应先增加时间步数，再用相邻两级网格核对价格与 Greeks。
- **计算域**。上边界检验应独立于空间步数检验。局部波动率曲面的绝对现货水平固定，自动边界仍需检查收敛。
- **适用范围**。引擎支持 BSM 与局部波动率。Heston 由适用性校验拒绝。局部波动率支持固定曲面下的 Delta 和 Gamma、隐含票息求解；隐含波动率求解返回 `UnsupportedOperation`。事件处的现货 Greeks 随支付的局部连续性而定。
- **参考精度**。Monte Carlo 的标准误不覆盖 Euler 偏差。第 8.9、9.9 节的结果适合检验局部波动率价格量级，精细误差主要依赖网格收敛分析。

---

## 12. 结论

在本报告的 BSM 基准上，Rannacher 有限差分结果随空间与时间加密趋近 QuantLib 静态复制和高斯卷积参考。每日敲入的时间离散是默认网格的主要误差来源，相近的敲出水平与行权价则需要更细的空间网格。四类产品共享的支付实现覆盖独立凤凰观察日程、终止返还和当期事件。附录 B.3 演示如何在给定方差时钟和估值时刻下，对多个现货复用同一解。

---

## 附录 A：源码索引

| 组件 | 文件 |
|---|---|
| 引擎入口、事件与层处理 | [`engines/finite_difference/autocallable.rs`](https://github.com/lilkui/kiyosi/blob/95dc91155223b9095d06cbbf7ba4bda5bc72b7c1/crates/kiyosi/src/engines/finite_difference/autocallable.rs) |
| 设置、格式、上边界、Greeks 补全 | [`engines/finite_difference.rs`](https://github.com/lilkui/kiyosi/blob/95dc91155223b9095d06cbbf7ba4bda5bc72b7c1/crates/kiyosi/src/engines/finite_difference.rs) |
| 网格、sinh 坐标、加密、投影、样条、时间网格 | [`engines/finite_difference/grid.rs`](https://github.com/lilkui/kiyosi/blob/95dc91155223b9095d06cbbf7ba4bda5bc72b7c1/crates/kiyosi/src/engines/finite_difference/grid.rs) |
| θ 格式、Thomas 求解、分解缓存 | [`engines/finite_difference/step.rs`](https://github.com/lilkui/kiyosi/blob/95dc91155223b9095d06cbbf7ba4bda5bc72b7c1/crates/kiyosi/src/engines/finite_difference/step.rs) |
| BSM 与局部波动率的单态化扩散 | [`engines/finite_difference/diffusion.rs`](https://github.com/lilkui/kiyosi/blob/95dc91155223b9095d06cbbf7ba4bda5bc72b7c1/crates/kiyosi/src/engines/finite_difference/diffusion.rs) |
| 交易日方差规则 | [`time/convention.rs`](https://github.com/lilkui/kiyosi/blob/95dc91155223b9095d06cbbf7ba4bda5bc72b7c1/crates/kiyosi/src/time/convention.rs) |
| 保存解与现货查询 | [`engines/finite_difference/solution.rs`](https://github.com/lilkui/kiyosi/blob/95dc91155223b9095d06cbbf7ba4bda5bc72b7c1/crates/kiyosi/src/engines/finite_difference/solution.rs) |
| 雪球、二元雪球、三元雪球与凤凰的条款、统一视图和支付语义 | [`instruments/autocallable.rs`](https://github.com/lilkui/kiyosi/blob/95dc91155223b9095d06cbbf7ba4bda5bc72b7c1/crates/kiyosi/src/instruments/autocallable.rs)、[`instruments/autocallable/pricing.rs`](https://github.com/lilkui/kiyosi/blob/95dc91155223b9095d06cbbf7ba4bda5bc72b7c1/crates/kiyosi/src/instruments/autocallable/pricing.rs) |
| 雪球与凤凰预设 | [`instruments/autocallable/presets.rs`](https://github.com/lilkui/kiyosi/blob/95dc91155223b9095d06cbbf7ba4bda5bc72b7c1/crates/kiyosi/src/instruments/autocallable/presets.rs) |
| 仓库测试 | [`tests/phoenix.rs`](https://github.com/lilkui/kiyosi/blob/95dc91155223b9095d06cbbf7ba4bda5bc72b7c1/crates/kiyosi/tests/phoenix.rs)、[`tests/snowball.rs`](https://github.com/lilkui/kiyosi/blob/95dc91155223b9095d06cbbf7ba4bda5bc72b7c1/crates/kiyosi/tests/snowball.rs)、[`tests/snowball_variants.rs`](https://github.com/lilkui/kiyosi/blob/95dc91155223b9095d06cbbf7ba4bda5bc72b7c1/crates/kiyosi/tests/snowball_variants.rs)、[`tests/autocallable_finite_difference.rs`](https://github.com/lilkui/kiyosi/blob/95dc91155223b9095d06cbbf7ba4bda5bc72b7c1/crates/kiyosi/tests/autocallable_finite_difference.rs)、[`test_autocallable_fd_accuracy.py`](https://github.com/lilkui/kiyosi/blob/95dc91155223b9095d06cbbf7ba4bda5bc72b7c1/python/tests/test_autocallable_fd_accuracy.py)、[`quantlib_reference/structured.py`](https://github.com/lilkui/kiyosi/blob/95dc91155223b9095d06cbbf7ba4bda5bc72b7c1/python/tests/quantlib_reference/structured.py) |

## 附录 B：复现脚本

使用 `kiyosi==0.21.0`、`QuantLib==1.44` 和 `numpy==2.5.5`。把 B.1 的两个代码块依次保存为 `phoenix_report.py`，把 B.2 的两个代码块保存为 `snowball_report.py`。B.4 演示如何用这些模块复算基准、参数扫描、静态复制和局部波动率比较。

### B.1 凤凰

```python
"""Shared contract definition and independent reference pricers."""

import math
from datetime import datetime, timedelta

import numpy as np
from kiyosi import instruments as ins
from kiyosi import market as mk
from kiyosi import pricing as pr

START = datetime(2025, 1, 2)
OBS = [
    datetime(2025, 2, 3), datetime(2025, 3, 3), datetime(2025, 4, 2),
    datetime(2025, 5, 2), datetime(2025, 6, 2), datetime(2025, 7, 2),
    datetime(2025, 8, 4), datetime(2025, 9, 2), datetime(2025, 10, 2),
    datetime(2025, 11, 3), datetime(2025, 12, 2), datetime(2026, 1, 2),
]
END = OBS[-1]
BASE = dict(s0=100.0, r=0.03, q=0.01, sigma=0.25, ko=100.0, cb=70.0, ki=70.0,
            coupon=0.008, upper=100.0, lower=0.0, principal=1.0, lockout=0)


def yf(t, origin=START):
    return (t - origin).total_seconds() / (365 * 86400)


def weekdays(start, end):
    out, d = [], start
    while d <= end:
        if d.weekday() < 5:
            out.append(d)
        d += timedelta(days=1)
    return out


def note(daily, p=BASE, obs=OBS, ko_levels=None, cb_levels=None):
    ko_levels = ko_levels or [p["ko"]] * len(obs)
    cb_levels = cb_levels or [p["cb"]] * len(obs)
    return ins.PhoenixOption(
        calendar=mk.weekdays_calendar(),
        coupon_per_period=p["coupon"],
        initial_spot=100.0,
        knock_in_level=p["ki"],
        upper_strike=p["upper"],
        lower_strike=p["lower"],
        knock_in_observation=(ins.KnockInObservation.every_trading_day(START.time())
                              if daily else ins.KnockInObservation.at_expiry()),
        barrier_state="no_event",
        effective_time=START,
        expiry_time=obs[-1],
        principal_redemption_ratio=p["principal"],
        knock_out_observations=[
            ins.KnockOutObservation(t, level)
            for t, level in list(zip(obs, ko_levels, strict=True))[p["lockout"]:]
        ],
        coupon_observations=[
            ins.CouponObservation(t, level)
            for t, level in zip(obs, cb_levels, strict=True)
        ],
    )


def context(spot=None, p=BASE, valuation=START):
    return mk.PricingContext(
        model_parameters=mk.BlackScholesMertonParameters(
            risk_free_rate=p["r"], dividend_yield=p["q"], volatility=p["sigma"]),
        spot_price=p["s0"] if spot is None else spot,
        valuation_time=valuation,
    )


def fd(**kw):
    return pr.FiniteDifferenceAutocallableEngine(**kw)


_erf = np.frompyfunc(math.erf, 1, 1)


def ncdf(x):
    return 0.5 * (1.0 + _erf(np.asarray(x) / math.sqrt(2.0)).astype(float))


def events(daily, obs=OBS, valuation=START):
    times = {t: {"obs": i, "ki": False} for i, t in enumerate(obs) if t > valuation}
    if daily:
        for d in weekdays(START, obs[-1]):
            if d > valuation:
                times.setdefault(d, {"obs": None, "ki": False})["ki"] = True
    else:
        times[obs[-1]]["ki"] = True
    return sorted(times.items())


def _layers_event(S, A, K, ev, p, ko_lv, cb_lv, terminal):
    i = ev["obs"]
    coupon = np.where(S >= cb_lv[i], p["coupon"], 0.0) if i is not None else 0.0
    below = S < p["ki"]
    if terminal:
        loss = (np.clip(S, p["lower"], p["upper"]) - p["upper"]) / 100.0
        a = p["principal"] + np.where(below if ev["ki"] else False, loss, 0.0)
        k = p["principal"] + loss
        out = S >= ko_lv[i]
        return (np.where(out, p["principal"], a) + coupon,
                np.where(out, p["principal"], k) + coupon)
    if ev["ki"]:
        A = np.where(below, K, A)
    A, K = A + coupon, K + coupon
    if i is not None and i >= p["lockout"]:
        out = S >= ko_lv[i]
        A = np.where(out, p["principal"] + coupon, A)
        K = np.where(out, p["principal"] + coupon, K)
    return A, K


H0 = math.log(100.0 / 70.0) / 20.0  # every contract level is 70*exp(k*H0)


def on_lattice(level):
    k = math.log(level / 70.0) / H0
    return abs(k - round(k)) < 1e-9


def convolution_price(daily, m=10, width=10.0, p=BASE, obs=OBS, ko_levels=None,
                      cb_levels=None, spot=None, valuation=START):
    """Backward induction with exact Gaussian cell probabilities (second order)."""
    ko_lv = ko_levels or [p["ko"]] * len(obs)
    cb_lv = cb_levels or [p["cb"]] * len(obs)
    for level in [*ko_lv, *[c for c in cb_lv if c > 0], p["ki"], p["upper"]] + (
            [p["lower"]] if p["lower"] > 0 else []):
        assert on_lattice(level), level
    s0 = p["s0"] if spot is None else spot
    T = yf(obs[-1], valuation)
    h = H0 / m
    x0 = math.log(s0 / 70.0)
    W = width * p["sigma"] * math.sqrt(T) + abs(p["r"] - p["q"]) * T
    jlo, jhi = int(math.floor((x0 - W) / h)), int(math.ceil((x0 + W) / h))
    x = (np.arange(jlo, jhi) + 0.5) * h
    S = 70.0 * np.exp(x)
    evs = events(daily, obs, valuation)
    A, K = _layers_event(S, None, None, evs[-1][1], p, ko_lv, cb_lv, True)
    mu_rate = p["r"] - p["q"] - 0.5 * p["sigma"] ** 2

    def step(V, dt):
        s = p["sigma"] * math.sqrt(dt)
        mu = mu_rate * dt
        R = int(math.ceil((12 * s + abs(mu)) / h)) + 1
        d = np.arange(-R, R + 1) * h
        w = ncdf((d + 0.5 * h - mu) / s) - ncdf((d - 0.5 * h - mu) / s)
        Vp = np.pad(V, R, mode="edge")
        if R < 200:
            out = np.convolve(Vp, w[::-1], mode="valid")
        else:
            n = len(Vp) + len(w) - 1
            L = 1 << (n - 1).bit_length()
            full = np.fft.irfft(np.fft.rfft(Vp, L) * np.fft.rfft(w[::-1], L), L)[:n]
            out = full[len(w) - 1:len(Vp)]
        return math.exp(-p["r"] * dt) * out

    for j in range(len(evs) - 2, -1, -1):
        dt = yf(evs[j + 1][0], valuation) - yf(evs[j][0], valuation)
        A, K = step(A, dt), step(K, dt)
        A, K = _layers_event(S, A, K, evs[j][1], p, ko_lv, cb_lv, False)
    t1 = yf(evs[0][0], valuation)
    s = p["sigma"] * math.sqrt(t1)
    c = x0 + mu_rate * t1
    w = ncdf((x + 0.5 * h - c) / s) - ncdf((x - 0.5 * h - c) / s)
    # A daily monitoring instant at valuation knocks in with the current spot.
    current_ki = (daily and valuation.weekday() < 5 and valuation.time() == START.time()
                  and s0 < p["ki"])
    return math.exp(-p["r"] * t1) * float(np.dot(w, K if current_ki else A))


def reference(daily, ms=(20, 40, 80), **kw):
    """Richardson-extrapolated convolution value and a conservative error bound."""
    v = [convolution_price(daily, m=m, **kw) for m in ms]
    r1 = v[1] + (v[1] - v[0]) / 3
    r2 = v[2] + (v[2] - v[1]) / 3
    return r2, max(abs(r2 - r1), abs(v[2] - v[1]) / 3), v


def mc_price(daily, paths=4_000_000, batch=250_000, seed=20251115, p=BASE, obs=OBS,
             ko_levels=None, cb_levels=None, local=None, dtmax=None):
    """Antithetic GBM (exact at events) or log-Euler local-volatility Monte Carlo."""
    ko_lv = ko_levels or [p["ko"]] * len(obs)
    cb_lv = cb_levels or [p["cb"]] * len(obs)
    evs = events(daily, obs)
    rng = np.random.default_rng(seed)
    total, total2, n = 0.0, 0.0, 0
    while n < paths:
        b = min(batch, paths - n) // 2
        logS = np.full(2 * b, math.log(p["s0"]))
        alive = np.ones(2 * b, bool)
        kin = np.zeros(2 * b, bool)
        pv = np.zeros(2 * b)
        t_prev = 0.0
        for t, ev in evs:
            tt = yf(t)
            substeps = 1 if dtmax is None else max(1, math.ceil((tt - t_prev) / dtmax - 1e-9))
            dt = (tt - t_prev) / substeps
            for k in range(substeps):
                z = rng.standard_normal(b)
                z = np.concatenate([z, -z])
                sig = p["sigma"] if local is None else local(t_prev + (k + 0.5) * dt,
                                                             np.exp(logS))
                logS += (p["r"] - p["q"] - 0.5 * sig * sig) * dt + sig * math.sqrt(dt) * z
            t_prev = tt
            S = np.exp(logS)
            df = math.exp(-p["r"] * tt)
            i = ev["obs"]
            if ev["ki"]:
                kin |= alive & (S < p["ki"])
            if i is not None:
                pv += np.where(alive & (S >= cb_lv[i]), p["coupon"] * df, 0.0)
                if i >= p["lockout"]:
                    out = alive & (S >= ko_lv[i])
                    pv += np.where(out, p["principal"] * df, 0.0)
                    alive &= ~out
        loss = (np.clip(S, p["lower"], p["upper"]) - p["upper"]) / 100.0
        pv += np.where(alive, (p["principal"] + np.where(kin, loss, 0.0)) * df, 0.0)
        pair = 0.5 * (pv[:b] + pv[b:])
        total += pair.sum()
        total2 += (pair * pair).sum()
        n += 2 * b
    pairs = n // 2
    mean = total / pairs
    se = math.sqrt(max(total2 / pairs - mean * mean, 0.0) / (pairs - 1))
    return float(mean), se
```

QuantLib 静态复制（第 8.1 节）的核心函数：

```python
import QuantLib as ql


def black(kind, strike, spot, r, q, sigma, t, payout=1.0):
    fwd, df = spot * math.exp((r - q) * t), math.exp(-r * t)
    if kind == "digital":
        payoff = ql.CashOrNothingPayoff(ql.Option.Call, strike, payout)
    elif kind == "digital_put":
        payoff = ql.CashOrNothingPayoff(ql.Option.Put, strike, payout)
    else:
        if strike <= 0:
            return 0.0
        payoff = ql.PlainVanillaPayoff(ql.Option.Put, strike)
    return ql.BlackCalculator(payoff, fwd, sigma * math.sqrt(t), df).value()


def static_value(p, obs, spot):
    """Phoenix with knock-out only at expiry and knock-in observed at expiry."""
    T = yf(obs[-1])
    v = p["principal"] * math.exp(-p["r"] * T)
    for t in obs:
        v += math.copysign(1, p["coupon"]) * black(
            "digital", p["cb"], spot, p["r"], p["q"], p["sigma"], yf(t), abs(p["coupon"]))
    v -= ((p["upper"] - p["ki"]) * black("digital_put", p["ki"], spot, p["r"], p["q"],
                                          p["sigma"], T)
          + black("put", p["ki"], spot, p["r"], p["q"], p["sigma"], T)
          - black("put", p["lower"], spot, p["r"], p["q"], p["sigma"], T)) / 100.0
    return v
```

### B.2 雪球、三元雪球和二元雪球

`kind` 选择产品；`rates` 给出逐期年化敲出票息，`ko_levels` 给出逐期敲出水平，二者缺省时取常数。卷积参考要求所有合约水平落在 $70\,e^{kH_0}$ 格点上，`lattice(k)` 返回这些水平。

```python
"""Shared snowball contract definitions and independent reference pricers."""

import math
from datetime import datetime, timedelta

import numpy as np
from kiyosi import instruments as ins
from kiyosi import market as mk
from kiyosi import pricing as pr

START = datetime(2025, 1, 2)
OBS = [
    datetime(2025, 2, 3), datetime(2025, 3, 3), datetime(2025, 4, 2),
    datetime(2025, 5, 2), datetime(2025, 6, 2), datetime(2025, 7, 2),
    datetime(2025, 8, 4), datetime(2025, 9, 2), datetime(2025, 10, 2),
    datetime(2025, 11, 3), datetime(2025, 12, 2), datetime(2026, 1, 2),
]
H0 = math.log(100.0 / 70.0) / 20.0  # every contract level is 70*exp(k*H0)
BASE = dict(kind="snowball", s0=100.0, r=0.03, q=0.01, sigma=0.25, ko=100.0,
            ki=70.0, coupon=0.15, mat=0.15, minc=0.03, upper=100.0, lower=0.0,
            principal=1.0)


def lattice(k):
    return 70.0 * math.exp(k * H0)


def yf(t, origin=START):
    return (t - origin).total_seconds() / (365 * 86400)


def weekdays(start, end):
    out, d = [], start
    while d <= end:
        if d.weekday() < 5:
            out.append(d)
        d += timedelta(days=1)
    return out


def note(daily, p=BASE, obs=OBS, ko_levels=None, rates=None, state="no_event"):
    ko_levels = ko_levels or [p["ko"]] * len(obs)
    rates = rates or [p["coupon"]] * len(obs)
    records = ins.autocallable_observations(obs, ko_levels, knock_out_coupon_rates=rates)
    common = dict(effective_time=START, expiry_time=obs[-1], autocall_observations=records,
                  barrier_state=state, principal_redemption_ratio=p["principal"],
                  calendar=mk.weekdays_calendar(), maturity_coupon_rate=p["mat"])
    if p["kind"] == "binary":
        return ins.BinarySnowballOption(**common)
    ki_obs = (ins.KnockInObservation.every_trading_day(START.time()) if daily
              else ins.KnockInObservation.at_expiry())
    if p["kind"] == "ternary":
        return ins.TernarySnowballOption(minimum_coupon_rate=p["minc"], knock_in_level=p["ki"],
                                         knock_in_observation=ki_obs, **common)
    return ins.SnowballOption(initial_spot=100.0, knock_in_level=p["ki"], upper_strike=p["upper"],
                              lower_strike=p["lower"], knock_in_observation=ki_obs, **common)


def context(spot=None, p=BASE, valuation=START):
    return mk.PricingContext(
        model_parameters=mk.BlackScholesMertonParameters(
            risk_free_rate=p["r"], dividend_yield=p["q"], volatility=p["sigma"]),
        spot_price=p["s0"] if spot is None else spot,
        valuation_time=valuation,
    )


def fd(**kw):
    return pr.FiniteDifferenceAutocallableEngine(**kw)


_erf = np.frompyfunc(math.erf, 1, 1)


def ncdf(x):
    return 0.5 * (1.0 + _erf(np.asarray(x) / math.sqrt(2.0)).astype(float))


def events(daily, obs=OBS, valuation=START):
    times = {t: {"obs": i, "ki": False} for i, t in enumerate(obs) if t > valuation}
    if daily:
        for d in weekdays(START, obs[-1]):
            if d > valuation:
                times.setdefault(d, {"obs": None, "ki": False})["ki"] = True
    else:
        times[obs[-1]]["ki"] = True
    return sorted(times.items())


class Payoff:
    """Snowball, binary and ternary settlement written independently of Kiyosi."""

    def __init__(self, p, obs, ko_levels, rates):
        self.p, self.obs = p, obs
        self.ko = ko_levels or [p["ko"]] * len(obs)
        self.rates = rates or [p["coupon"]] * len(obs)
        self.life = yf(obs[-1])

    def ko_pay(self, i):
        return self.p["principal"] + self.rates[i] * yf(self.obs[i])

    def intact(self, S):
        return np.full_like(S, self.p["principal"] + self.p["mat"] * self.life)

    def knocked(self, S):
        p = self.p
        if p["kind"] == "ternary":
            return np.full_like(S, p["principal"] + p["minc"] * self.life)
        if p["kind"] == "binary":
            return self.intact(S)
        return p["principal"] + (np.clip(S, p["lower"], p["upper"]) - p["upper"]) / 100.0

    def below(self, S):
        return S < self.p["ki"] if self.p["kind"] != "binary" else np.zeros(S.shape, bool)

    def event(self, S, A, K, ev, terminal):
        i = ev["obs"]
        if terminal:
            A = np.where(self.below(S) & ev["ki"], self.knocked(S), self.intact(S))
            K = self.knocked(S)
        elif ev["ki"]:
            A = np.where(self.below(S), K, A)
        if i is not None:
            out = S >= self.ko[i]
            A = np.where(out, self.ko_pay(i), A)
            K = np.where(out, self.ko_pay(i), K)
        return A, K

    def levels(self):
        p = self.p
        out = list(self.ko)
        if p["kind"] != "binary":
            out.append(p["ki"])
        if p["kind"] == "snowball":
            out.append(p["upper"])
            if p["lower"] > 0:
                out.append(p["lower"])
        return out


def on_lattice(level):
    k = math.log(level / 70.0) / H0
    return abs(k - round(k)) < 1e-9


def convolution_price(daily, m=10, width=10.0, p=BASE, obs=OBS, ko_levels=None, rates=None,
                      spot=None, valuation=START, knocked_in=False):
    """Backward induction with exact Gaussian cell probabilities (second order)."""
    pay = Payoff(p, obs, ko_levels, rates)
    for level in pay.levels():
        assert on_lattice(level), level
    daily = daily and p["kind"] != "binary"
    s0 = p["s0"] if spot is None else spot
    T = yf(obs[-1], valuation)
    h = H0 / m
    x0 = math.log(s0 / 70.0)
    W = width * p["sigma"] * math.sqrt(T) + abs(p["r"] - p["q"]) * T
    jlo, jhi = int(math.floor((x0 - W) / h)), int(math.ceil((x0 + W) / h))
    x = (np.arange(jlo, jhi) + 0.5) * h
    S = 70.0 * np.exp(x)
    evs = events(daily, obs, valuation)
    A, K = pay.event(S, None, None, evs[-1][1], True)
    mu_rate = p["r"] - p["q"] - 0.5 * p["sigma"] ** 2

    def step(V, dt):
        s = p["sigma"] * math.sqrt(dt)
        mu = mu_rate * dt
        R = int(math.ceil((12 * s + abs(mu)) / h)) + 1
        d = np.arange(-R, R + 1) * h
        w = ncdf((d + 0.5 * h - mu) / s) - ncdf((d - 0.5 * h - mu) / s)
        Vp = np.pad(V, R, mode="edge")
        if R < 200:
            out = np.convolve(Vp, w[::-1], mode="valid")
        else:
            n = len(Vp) + len(w) - 1
            L = 1 << (n - 1).bit_length()
            full = np.fft.irfft(np.fft.rfft(Vp, L) * np.fft.rfft(w[::-1], L), L)[:n]
            out = full[len(w) - 1:len(Vp)]
        return math.exp(-p["r"] * dt) * out

    for j in range(len(evs) - 2, -1, -1):
        dt = yf(evs[j + 1][0], valuation) - yf(evs[j][0], valuation)
        A, K = step(A, dt), step(K, dt)
        A, K = pay.event(S, A, K, evs[j][1], False)
    t1 = yf(evs[0][0], valuation)
    s = p["sigma"] * math.sqrt(t1)
    c = x0 + mu_rate * t1
    w = ncdf((x + 0.5 * h - c) / s) - ncdf((x - 0.5 * h - c) / s)
    # A daily monitoring instant at valuation knocks in with the current spot.
    current_ki = daily and valuation.weekday() < 5 and valuation.time() == START.time() \
        and s0 < p["ki"]
    V = K if (knocked_in or current_ki) else A
    return math.exp(-p["r"] * t1) * float(np.dot(w, V))


def reference(daily, ms=(20, 40, 80), **kw):
    """Richardson-extrapolated convolution value and a conservative error bound."""
    v = [convolution_price(daily, m=m, **kw) for m in ms]
    r1 = v[1] + (v[1] - v[0]) / 3
    r2 = v[2] + (v[2] - v[1]) / 3
    return r2, max(abs(r2 - r1), abs(v[2] - v[1]) / 3), v


def mc_price(daily, paths=4_000_000, batch=250_000, seed=20251115, p=BASE, obs=OBS,
             ko_levels=None, rates=None, local=None, dtmax=None):
    """Antithetic GBM (exact at events) or log-Euler local-volatility Monte Carlo."""
    pay = Payoff(p, obs, ko_levels, rates)
    daily = daily and p["kind"] != "binary"
    evs = events(daily, obs)
    rng = np.random.default_rng(seed)
    total, total2, n = 0.0, 0.0, 0
    while n < paths:
        b = min(batch, paths - n) // 2
        logS = np.full(2 * b, math.log(p["s0"]))
        alive = np.ones(2 * b, bool)
        kin = np.zeros(2 * b, bool)
        pv = np.zeros(2 * b)
        t_prev = 0.0
        for t, ev in evs:
            tt = yf(t)
            substeps = 1 if dtmax is None else max(1, math.ceil((tt - t_prev) / dtmax - 1e-9))
            dt = (tt - t_prev) / substeps
            for k in range(substeps):
                z = rng.standard_normal(b)
                z = np.concatenate([z, -z])
                sig = p["sigma"] if local is None else local(t_prev + (k + 0.5) * dt,
                                                             np.exp(logS))
                logS += (p["r"] - p["q"] - 0.5 * sig * sig) * dt + sig * math.sqrt(dt) * z
            t_prev = tt
            S = np.exp(logS)
            df = math.exp(-p["r"] * tt)
            i = ev["obs"]
            if ev["ki"]:
                kin |= alive & pay.below(S)
            if i is not None:
                out = alive & (S >= pay.ko[i])
                pv += np.where(out, pay.ko_pay(i) * df, 0.0)
                alive &= ~out
        pv += np.where(alive, np.where(kin, pay.knocked(S), pay.intact(S)) * df, 0.0)
        pair = 0.5 * (pv[:b] + pv[b:])
        total += pair.sum()
        total2 += (pair * pair).sum()
        n += 2 * b
    pairs = n // 2
    mean = total / pairs
    se = math.sqrt(max(total2 / pairs - mean * mean, 0.0) / (pairs - 1))
    return float(mean), se
```

单观察日雪球类合约的 QuantLib 静态复制（第 9.1 节），沿用 B.1 中的 `black`：

```python
from phoenix_report import black


def snowball_static_value(p, spot, expiry=OBS[-1]):
    """Single-observation snowball, ternary or binary note with knock-in at expiry."""
    T = yf(expiry)
    a = (p["r"], p["q"], p["sigma"], T)
    v = (p["principal"] + p["mat"] * T) * math.exp(-p["r"] * T)
    v += (p["coupon"] - p["mat"]) * T * black("digital", p["ko"], spot, *a)
    if p["kind"] == "binary":
        return v
    if p["kind"] == "ternary":
        return v - (p["mat"] - p["minc"]) * T * black("digital_put", p["ki"], spot, *a)
    return v - (p["mat"] * T * black("digital_put", p["ki"], spot, *a)
                + ((p["upper"] - p["ki"]) * black("digital_put", p["ki"], spot, *a)
                   + black("put", p["ki"], spot, *a) - black("put", p["lower"], spot, *a)) / 100)
```

### B.3 独立日程、返还与批量现货查询

合约在周六观察票息、周一观察敲出、周二到期。合约日历允许周六观察；方差日历在周末暂停扩散。固定返还 2% 与年化返还 5% 在现金流终止日付一次。估值在周六票息观察时刻，查询现货 95 时恰好满足含等号的票息条件。

```python
from datetime import datetime

from kiyosi import instruments as ins
from kiyosi import market as mk
from kiyosi import pricing as pr

start = datetime(2025, 1, 3)
coupon_day = datetime(2025, 1, 4)
knock_out_day = datetime(2025, 1, 6)
expiry = datetime(2025, 1, 7)
note = ins.PhoenixOption(
    coupon_per_period=0.01,
    initial_spot=100,
    knock_in_level=70,
    upper_strike=100,
    lower_strike=0,
    knock_in_observation=ins.KnockInObservation.at_expiry(),
    effective_time=start,
    expiry_time=expiry,
    barrier_state="no_event",
    knock_out_observations=[ins.KnockOutObservation(knock_out_day, 102)],
    coupon_observations=[ins.CouponObservation(coupon_day, 95)],
    rebate_rate=0.02,
    annual_rebate_rate=0.05,
    calendar=mk.all_days_calendar(),
)
context = mk.PricingContext(
    model_parameters=mk.BlackScholesMertonParameters(
        risk_free_rate=0.03,
        dividend_yield=0.01,
        volatility=0.25,
        variance_time_convention="business",
        calendar=mk.weekdays_calendar(),
    ),
    spot_price=100,
    valuation_time=coupon_day,
)
engine = pr.FiniteDifferenceAutocallableEngine()
spots = (94, 95, 100, 105)
solution = engine.solve(note, context, spot_range=(94, 105))
results = solution.price_many_with_greeks(spots, ["delta", "gamma"])
for spot, result in zip(spots, results, strict=True):
    scalar = engine.price(note, context.replace(spot_price=spot))
    assert abs(result.price - scalar) < 1e-5
    print(spot, f"{result.price:.9f}")

assert results[1].price > results[0].price
assert results[1].delta is None and results[1].gamma is None
```

输出价格依次为 `1.020296334`、`1.030296334`、`1.030296334`、`1.030243234`。现货为 95 的查询计入当期票息，Delta 与 Gamma 在支付跳跃处不可用。

### B.4 复算验证结果

以下调用复算两份基准的同步加密、独立 MC 和局部波动率比较。定价格式和计算域分别由 `scheme`、`asset_upper_boundary` 控制；静态复制使用 B.1 的 `static_value` 或 B.2 的 `snowball_static_value`。变体通过 `p` 或 `ko_levels` 同时传给 `note` 与 `reference`，市场参数变化同时传给 `context`。例如 `p=dict(snowball.BASE, kind="ternary")` 选三元雪球。

```python
import numpy as np

import phoenix_report as phoenix
import snowball_report as snowball
from kiyosi import market as mk
from kiyosi import pricing as pr

nodes = [50, 70, 100, 130, 160]
v0 = [0.40, 0.32, 0.25, 0.21, 0.19]
v1 = [0.36, 0.30, 0.24, 0.21, 0.20]
grids = [(400, 200), (800, 400), (1600, 800),
         (1600, 1600), (3200, 3200), (6400, 3200)]


def local(t, spot):
    return (1 - t) * np.interp(spot, nodes, v0) + t * np.interp(spot, nodes, v1)


for module in (phoenix, snowball):
    surface = mk.LocalVolatilitySurface(
        times=[module.START, module.OBS[-1]], spots=nodes, values=[v0, v1],
    )
    context = module.context()
    local_context = context.replace(model_parameters=mk.LocalVolatilityParameters(
        risk_free_rate=module.BASE["r"], dividend_yield=module.BASE["q"], surface=surface,
    ))
    for daily in (False, True):
        ms = (80, 160, 320) if daily else (40, 80, 160)
        ref, _, _ = module.reference(daily, ms=ms)
        note = module.note(daily)
        print(module.__name__, daily, ref)
        for n, m in grids:
            engine = module.fd(asset_step_count=n, time_step_count=m)
            print(n, m, engine.price(note, context) - ref)
        print("quadrature", pr.QuadratureAutocallableEngine().price(note, context))
        print("GBM MC", module.mc_price(daily, paths=4_000_000))
        for n in (400, 800, 1600, 3200):
            engine = module.fd(asset_step_count=n, time_step_count=n)
            print(n, engine.price(note, local_context))
        print("local vol MC", module.mc_price(daily, paths=1_000_000,
                                             local=local, dtmax=0.25 / 365))
```
