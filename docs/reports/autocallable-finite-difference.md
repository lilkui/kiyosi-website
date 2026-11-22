---
description: 面向具备高等数学、概率论与线性代数基础的读者，系统阐述 Kiyosi 运用一维有限差分法为雪球与凤凰结构化票据定价的数学建模、偏微分方程推导、离散障碍计算域与边界设置、观察日阶跃投影及独立验证结果。
---

<script setup>
import AutocallPathDiagram from '../.vitepress/components/autocallable-fd/AutocallPathDiagram.vue'
import TerminalPayoffDiagram from '../.vitepress/components/autocallable-fd/TerminalPayoffDiagram.vue'
import DualLayerPdeDiagram from '../.vitepress/components/autocallable-fd/DualLayerPdeDiagram.vue'
import BoundaryDomainDiagram from '../.vitepress/components/autocallable-fd/BoundaryDomainDiagram.vue'
import ObservationStepDiagram from '../.vitepress/components/autocallable-fd/ObservationStepDiagram.vue'
import JumpProjectionDiagram from '../.vitepress/components/autocallable-fd/JumpProjectionDiagram.vue'
import TimeMarchingDiagram from '../.vitepress/components/autocallable-fd/TimeMarchingDiagram.vue'
import MathTerm from '../.vitepress/components/autocallable-fd/MathTerm.vue'
</script>

# Kiyosi 自动赎回结构（雪球、凤凰）有限差分定价：原理、实现与验证报告

> 适用版本：Kiyosi 0.22.0（提交 `d8413d1`）。  
> 验证环境：Ubuntu 26.04 x86_64，Rust release 构建，Python 3.15.2，QuantLib 1.44，NumPy 2.5.5。

::: tip 阅读与交互提示
本文假定读者具备高等数学、概率论与线性代数基础，无需预先修读金融工程或随机过程课程。文中带有虚线下划线的专业名词（如 <MathTerm id="feynman-kac">Feynman–Kac 偏微分方程</MathTerm>）均支持**点击弹出释义卡片**，再次点击、按 `Esc` 或点击空白处即可关闭。
:::

## 目录

1. [摘要](#_1-摘要)
2. [产品定义与支付结构](#_2-产品定义与支付结构)
3. [有限差分定价基本原理与数学模型](#_3-有限差分定价基本原理与数学模型)
4. [边界条件的设置方法与计算域构造](#_4-边界条件的设置方法与计算域构造)
5. [观察日阶跃条件的应用逻辑](#_5-观察日阶跃条件的应用逻辑)
6. [空间时间离散化、阻尼格式与算法实现](#_6-空间时间离散化、阻尼格式与算法实现)
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

雪球（Snowball）与凤凰（Phoenix）是金融市场中常见的自动赎回结构化票据（Autocallable Note）。从数学角度看，可以把它们理解为一份与标的资产价格 $S_t$（例如某只股票或股票指数的实时价格，以下简称“现货”）挂钩的分段现金流规则：在合约存续期内的一系列约定日期，系统检查资产价格是否越过预设门槛，从而决定**提前结束合约并兑付本息**（称为“敲出”）、**发放当期利息**（称为“派息”），或**激活到期下跌亏损条款**（称为“敲入”）。为这类合约定价，本质上是计算未来所有可能价格轨迹下现金流折算到今天的数学期望。`FiniteDifferenceAutocallableEngine` 在统一的合约抽象下，为雪球、二元雪球、三元雪球和凤凰四类产品提供基于偏微分方程（PDE）的一维有限差分定价，同时支持 <MathTerm id="bsm-gbm">Black–Scholes–Merton 模型</MathTerm>（BSM，含确定性利率与股息期限结构）与 <MathTerm id="local-volatility">局部波动率</MathTerm>（Local Volatility）模型。

初学者常有一个直觉疑问：既然最终收益取决于过去两百多个交易日里价格有没有跌破敲入线、十几个观察日里有没有越过敲出线，定价岂不是要做两百多维的路径积分？之所以仍能用一维空间网格高效求解，关键在于合约状态的跳变只发生在有限个离散时刻。在任意两个相邻事件时刻之间的开区间内，没有任何条款触发，资产价格未来的涨跌分布只取决于当前价格而与更早的历史无关（即具备 <MathTerm id="piecewise-markov">分段马尔可夫性</MathTerm>），合约的期望延续价值满足确定性的一维 <MathTerm id="feynman-kac">后向 Feynman–Kac 偏微分方程</MathTerm>；至于跨期传递的历史路径记忆，只需一个二值状态标记 $j\in\{0,1\}$（$0$ 表示“尚未敲入”，$1$ 表示“已经敲入”）即可无损记录。求解器据此采用五项核心数值设计：

- **双层耦合与单层退化 PDE**：对于每个交易日监测敲入且敲入会改变到期收益的合约，在同一空间网格上从到期日逆向同步回推“未敲入层” $V^{(0)}$ 与“已敲入层” $V^{(1)}$，每逢监测时刻在敲入线下方将 $V^{(0)}$ 单向切换为 $V^{(1)}$；若合约仅在到期日观察敲入、不含敲入（二元雪球）或估值前早已敲入，则自动退化为单层求解以节省一半算力。
- **正现货截断域与仿射边界**：数值求解将无限价格半轴 $(0,+\infty)$ 截断为有限区间 $[S_{\min},S_{\max}]$，使所有正的敲出、敲入与派息门槛均处于区间内部。每个时间子步在上下端点按 <MathTerm id="dirichlet-affine">局部仿射边界条件</MathTerm>（把边界附近的价值局部近似为关于价格的一次函数 $A+BS$ 并分别折现）推进，并在事件时刻按端点价格执行合约条款。
- **增量跳跃修正的控制体积投影**：在观察日与监测日将更新后的价值拆成“原有光滑网格解 + 局部跳跃增量” $V^- = V^+ + \Delta V$，仅在跨越价格门槛的 <MathTerm id="control-volume">对偶控制体积</MathTerm> 上用分段 <MathTerm id="gauss-legendre">两点 Gauss–Legendre 求积</MathTerm> 计算平均跳跃量 $\overline{\Delta}_i$。这样既消除了门槛落在两格点之间造成的 $O(h)$ 阶梯抖动误差，又避免了在两百多个每日监测点上反复对光滑函数做积分平均而抹平曲线。
- **对数现货网格与 Rannacher 阻尼**：基础网格在对数坐标 $x=\ln(S/S_{\mathrm a})$ 上等距划分，隐式与半隐式格式进一步在合约关键价位两侧按 <MathTerm id="sinh-grid">双曲正弦（sinh）规律加密</MathTerm>。时间推进默认采用 <MathTerm id="rannacher-damping">Rannacher 阻尼格式</MathTerm>：在到期日及每次事件跳变后先走两对隐式 Euler 半步滤除高频锯齿伪影，随后切回二阶精度的 Crank–Nicolson 格式推进。
- **独立时间约定与固定时刻可复用解**：控制波动率累积速度的方差时钟可选自然日（Act/365F）或交易日（`"business"`），与合约观察日历、Act/365F 票息计息以及利率、股息曲线彼此独立。`solve` 接口支持一次逆向回推生成只读样条解，供多现货场景批量提取价格与各阶偏导数（<MathTerm id="greeks">Greeks</MathTerm>）。

第 8、9 节在单位名义本金（本金设为 $1$）假设下，使用 QuantLib <MathTerm id="static-replication">静态复制</MathTerm>、障碍对齐的 <MathTerm id="gaussian-convolution-fft">高斯转移密度卷积</MathTerm> 和独立 Monte Carlo 抽样对上述设计进行了基准验证。在默认 800×400 网格下，凤凰与雪球的到期敲入误差分别为 $4.9\times10^{-7}$ 和 $7.7\times10^{-7}$；每日敲入误差分别为 $6.3\times10^{-5}$ 和 $1.04\times10^{-4}$，网格加密至 3200×3200 后分别降至 $1.4\times10^{-6}$ 和 $2.3\times10^{-6}$。第 10 节汇总了仓库测试结果，附录 B 提供定价与复现脚本。

---

## 2. 产品定义与支付结构

### 2.1 统一的合约模型

阅读后续方程前，先明确自动赎回合约的三个核心动作（设名义本金归一化为 $1$，标的资产在时刻 $t$ 的价格记为 $S_t$）：

- **敲出（Knock-Out，提前赎回）**：在一组预先约定的观察时刻（通常每月一次），若资产价格涨到或超过敲出门槛 $B^{\text{out}}_k$（即 $S_{t_k}\ge B^{\text{out}}_k$），合约当场提前结束，向持有人返还本金与约定收益，后续日程全部作废。
- **敲入（Knock-In，激活下跌风险）**：在约定的敲入监测时刻（每个交易日收盘或仅在到期日），若资产价格严格跌破敲入门槛 $B^{\text{in}}$（即 $S < B^{\text{in}}$），合约就会被打上“已敲入”标记。敲入发生当下并不扣钱，但如果直到到期日合约都没能靠涨回敲出线提前赎回，持有人在到期时就要按标的跌幅承担本金亏损（或只拿保底低息）。
- **票息（Coupon，利息给付）**：合约向持有人支付的收益，既可以像存款计息一样按持有天数折算并在结束时一次性结清（雪球模式），也可以在每个观察日达到门槛时单独发放（凤凰模式）。

四类产品在 Rust 核心库中统一表示为泛型结构 `AutocallableNote<T>`，其中类型参数 `T` 分别对应 `SnowballTerms`、`BinarySnowballTerms`、`TernarySnowballTerms` 和 `PhoenixTerms`。定价引擎通过内部只读视图提取合约要素，在同一条时间轴上统一编排敲出观察、期间派息、敲入监测与到期结算。

| 符号 | Python 字段 | 含义 |
|---|---|---|
| $t_0,T$ | `effective_time`、`expiry_time` | 生效和到期时刻，精确到日内时分秒及微秒 |
| $P$ | `principal_redemption_ratio` | 单位名义本金对应的赎回本金比例，默认 1 |
| $\rho_0,\rho_a$ | `rebate_rate`、`annual_rebate_rate` | 终止时支付的固定返还率与年化返还率，均非负，默认 0 |
| — | `barrier_state` | 严格早于估值时刻的历史状态，取 `no_event`、`knocked_in`、`knocked_out` 或 `None`（未知） |
| — | `calendar` | 合约观察日历，决定每日敲入监测落在哪些交易日 |
| $B^{\text{in}}$ | `knock_in_level` | 敲入水平，严格低于该水平（$S < B^{\text{in}}$）时触发敲入；二元雪球无敲入 |
| — | `knock_in_observation` | 每个交易日指定时钟时刻观察（`every_trading_day`），或仅在到期时刻观察（`at_expiry`） |

雪球系列与凤凰在日程组织和票息语义上各有侧重：

- **雪球、三元雪球与二元雪球**：通过 `autocall_observations` 存放一组严格递增的敲出观察记录，第 $k$ 期记录包含观察时刻 $t_k$、敲出水平 $B^{\text{out}}_k$ 及年化敲出票息率 $r_k$。存续期间中途不派息；若直至到期均未敲出且未敲入，到期支付年化到期票息率 $c_m$（`maturity_coupon_rate`）。若发生过敲入且最终未敲出，标准雪球按参考价 $S_{\text{ref}}$（`initial_spot`）和上下行权价 $U,L$（`upper_strike`、`lower_strike`）承担下跌亏损；三元雪球不扣减本金，改为支付较低的年化保底票息 $c_{\min}$（`minimum_coupon_rate`，$c_{\min}\le c_m$）；二元雪球不设敲入障碍，只要未敲出，到期固定支付 $c_m$。
- **凤凰（Phoenix）**：分别使用 `knock_out_observations` 与 `coupon_observations` 两份独立日程存放 `KnockOutObservation` 和 `CouponObservation`。两份日程各自非空且严格递增，观察时刻均位于存续期内，既可以完全重合，也可以错开在不同日期或同一天的不同时点。每期票息率 $c$（`coupon_per_period`，允许为负）是固定单期比例，不按持有期长短年化折算，只要派息观察时刻满足含等号条件 $S_{t_k}\ge B^c_k$ 即当期发放；当 $B^c_k=0$ 时因正价格恒满足条件，退化为无条件固定派息（FCN）。未达派息线而漏付的票息不向后累计（无记忆效应）。预设参数 `lockout_periods` 在展开日程时直接略去前若干期敲出观察，锁定期内的派息与每日敲入监测照常执行。

<AutocallPathDiagram />

### 2.2 雪球与凤凰的现金流机制对比

记 $\tau(t)=\operatorname{Act/365F}(t_0,t)$ 为从生效时刻 $t_0$ 到时刻 $t$ 按“实际相隔秒数除以 365 天”折算的年化时间长度。四类产品在提前敲出或未敲出到期时，均以原始名义本金为基准支付一次终止返还 $R(t)=\rho_0+\rho_a\tau(t)$；雪球系列的年化敲出票息与到期票息同样按整个持有期 $\tau(t)$ 线性计息。

设 $t_k$ 为合约事件时刻，用示性变量 $\chi_k\in\{0,1\}$ 标记 $t_k$ 是否存在生效的敲出观察（存在取 $1$，否则取 $0$），用示性函数 $\mathbf 1_{\{S\ge B^c_k\}}$ 表示条件满足时取 $1$、不满足时取 $0$。记 $Q_k$ 为敲出兑付金额（不含凤凰当期票息），$C_k(S)$ 为观察时刻票息（仅在凤凰的派息观察时刻取下表值，其余时刻恒为 $0$），$\Pi^{(0)}(S)$ 与 $\Pi^{(1)}(S)$ 分别为未敲出条件下“未敲入”与“已敲入”两种状态对应的到期结算金额：

| 产品 | 敲出兑付 $Q_k$ | 期间票息 $C_k(S)$ | 未敲入到期支付 $\Pi^{(0)}(S)$ | 已敲入到期支付 $\Pi^{(1)}(S)$ |
|---|---|---|---|---|
| 雪球 | $P+R(t_k)+r_k\tau(t_k)$ | $0$ | $P+R(T)+c_m\tau(T)$ | $P+R(T)+\dfrac{\min(U,\max(L,S))-U}{S_{\text{ref}}}$ |
| 三元雪球 | $P+R(t_k)+r_k\tau(t_k)$ | $0$ | $P+R(T)+c_m\tau(T)$ | $P+R(T)+c_{\min}\tau(T)$ |
| 二元雪球 | $P+R(t_k)+r_k\tau(t_k)$ | $0$ | $P+R(T)+c_m\tau(T)$ | — |
| 凤凰 | $P+R(t_k)$ | $c\,\mathbf 1_{\{S\ge B^c_k\}}$ | $P+R(T)$ | $P+R(T)+\dfrac{\min(U,\max(L,S))-U}{S_{\text{ref}}}$ |

表中标准雪球与凤凰在已敲入到期时的亏损项 $\frac{\min(U,\max(L,S))-U}{S_{\text{ref}}}$ 是一个分段线性函数（金融上称为“看跌价差”空头损益）：当到期价 $S\ge U$ 时该项为 $0$（不亏本金）；当 $L\le S < U$ 时亏损为 $-(U-S)/S_{\text{ref}}$，随到期价下跌线性扩大（常见设置 $U=S_{\text{ref}}, L=0$ 下，资产从期初跌去多少比例，本金就亏掉多少比例）；当 $S < L$ 时被截断在最大亏损 $-(U-L)/S_{\text{ref}}$。

两类结构在结算与建模上的主要差异体现在以下四个环节：

1. **提前敲出与当期派息的叠加关系**。当 $\chi_k=1$ 且 $S_{t_k}\ge B^{\text{out}}_k$（含等号）时，合约立即终止。雪球将截至 $t_k$ 累积的年化票息 $r_k\tau(t_k)$ 随本金一次性结清；凤凰则支付本金与返还 $Q_k=P+R(t_k)$，若该时刻同时为派息观察时刻且 $S_{t_k}\ge B^c_k$，则一并支付当期票息 $c$（合计 $Q_k+C_k(S_{t_k})$），此后所有未来派息日程随即作废。
2. **敲入的状态不可逆性与“敲入后敲出获救”**。在任意敲入监测时刻，只要标的现货严格低于敲入线（$S<B^{\text{in}}$），合约状态即从 $j=0$ 不可逆地切换至 $j=1$。敲入本身不触发即时现金流；即便此前或当期已经敲入，只要在后续敲出观察日回升至 $S_{t_k}\ge B^{\text{out}}_k$，合约仍按全额敲出款 $Q_k+C_k(S_{t_k})$ 终止兑付，从而免除到期亏损。在已敲入但尚未敲出的存续期内，凤凰只要在派息观察日满足 $S_{t_k}\ge B^c_k$，仍正常支付当期票息（见图 1 路径 ③ 在 $t_3$ 处的派息点）。
3. **到期结算与敲入跳变幅度的差异**。若存续至到期日 $T$ 仍未敲出（当 $T$ 本身带有敲出观察且 $S_T\ge B^{\text{out}}_n$ 时，优先按敲出兑付），合约按最终敲入状态支付 $\Pi^{(0)}(S_T)$ 或 $\Pi^{(1)}(S_T)$，并加上当期符合条件的凤凰末期票息 $C_n(S_T)$。如图 2 所示，标准雪球一旦在 $B^{\text{in}}$ 处触发敲入，不仅要承担本金下跌亏损 $(U-B^{\text{in}})/S_{\text{ref}}$，还会同时失去整段持有期累积的到期红利票息 $c_m\tau(T)$；凤凰由于票息已在各期独立发放，未敲入到期仅返还本金与返还 $P+R(T)$，因此在 $B^{\text{in}}$ 处的到期支付跳变幅度明显小于同参数雪球。
4. **估值时刻的精确分界**。严格早于估值时刻 $t_{\text{val}}$ 的历史票息视为已落袋现金，不再计入当前现值；严格早于 $t_{\text{val}}$ 的敲入、敲出记录通过 `barrier_state` 传入。若估值时刻恰好落在某个观察或监测时点上，引擎以精确的当前现货 $S_0$ 判定一次当期事件，保证同日估值不遗漏、不重计。

有限差分、高斯求积和 Monte Carlo 三个引擎共用同一套底层结算函数（`observation_coupon`、`knock_out_payment`、`terminal`、`below_knock_in` 和 `expiry_payment`），确保等号方向、计息基准与锁定期语义完全一致。参见[合约条款](https://github.com/lilkui/kiyosi/blob/d8413d14ab2f7a53ecc3df145d394bd3c5ba783e/crates/kiyosi/src/instruments/autocallable.rs)和[事件结算](https://github.com/lilkui/kiyosi/blob/d8413d14ab2f7a53ecc3df145d394bd3c5ba783e/crates/kiyosi/src/instruments/autocallable/pricing.rs)。

<TerminalPayoffDiagram />

### 2.3 预设结构

市场上常见的雪球和凤凰变体均由预设构造器（Preset）展开为基础合约条款，求解器无需为特定商业名称编写专门分支，直接对展开后的观察序列与行权参数求解：

| 预设 | 展开结果 |
|---|---|
| 雪球 `Standard` / `European` | 常数敲出水平与票息；每日敲入 / 仅到期敲入 |
| 雪球 `StepDown`、`BothDown` | 敲出水平（以及票息）逐期递减（降敲 / 双降） |
| 雪球 `DualCoupon` | 到期票息 $c_m$ 与敲出票息 $r_k$ 独立设定 |
| 雪球 `Parachute` | 仅替换最后一期的敲出水平（通常大幅下调末期敲出线） |
| 雪球 `Otm`、`LossCapped` | 调整看跌起算上行权价 $U$；设定正的下行权价 $L$ 封顶最大本金亏损 |
| 雪球 `EarlyProfit`、`Butterfly` | 按观察时间分两段或三段设定阶梯年化票息，到期票息取末段水平 |
| 凤凰 `Standard`、`StepDown` | 常数或逐期递减敲出水平，配条件数字票息障碍 |
| 凤凰 `FixedCouponNote`、`DigitalCouponNote` | 无条件固定派息票据（FCN，$B^c=0$）或无提前敲出的数字派息票据（DCN） |

因此，本报告对雪球与凤凰基础条款的数学推导与数值验证覆盖了上述全部变体所需的支付原语；第 8.5 与 9.5 节还分别核验了降敲、双票息、降落伞、限亏及锁定期等结构的精度。

---

## 3. 有限差分定价基本原理与数学模型

### 3.1 分段马尔可夫性与最小状态空间约简

如果未来时刻 $t_{\text{pay}}$ 有一笔确定的现金 $X$，在连续复利无风险利率 $r(u)$ 下，它折算到当前时刻 $t$ 的现值为 $X\exp(-\int_t^{t_{\text{pay}}} r(u)\,du)$（其中的指数因子称为**贴现因子**）。当未来现金流取决于随机变化的价格路径时，衍生品无套利定价理论指出：只需在一个消除了风险溢价的等价概率分布——即 <MathTerm id="risk-neutral">风险中性测度</MathTerm> $\mathbb Q$——下，对未来全部未决现金流的贴现值求**条件数学期望**，所得期望值就是合约在时刻 $t$ 的理论公允价格。

表面上看，雪球和凤凰具有很强的路径依赖性：最终支付不仅取决于到期现货 $S_T$，还取决于存续期内每个月度观察日是否曾达到敲出线、每个派息日是否越过派息线，以及两百多个交易日内是否曾跌破敲入线。为什么我们不需要把这几百个时间点的价格都当作自变量，而是只靠一维空间网格就能严格求解？根源在于**离散事件的 <MathTerm id="piecewise-markov">分段马尔可夫性</MathTerm>** 与**历史信息的最小 <MathTerm id="sufficient-statistic">充分统计量</MathTerm> 约简**。

将全部未来敲出观察时刻、凤凰派息时刻与每日敲入监测时刻合并去重并按升序排列，记为 $t_{\text{val}} < \tau_1 < \tau_2 < \dots < \tau_K = T$。利用概率论中的**全期望公式（迭代期望定律）**，我们可以从终值 $\tau_K=T$ 出发，按区间一段一段往回求条件期望：

1. **开区间内的无记忆连续演化**。在任意两个相邻事件时刻之间的开区间 $(\tau_{m-1}, \tau_m)$ 内，没有任何合约条款被观察或触发：既不会发生敲出终止，也不会产生票息支付或敲入状态翻转。因此，在 $(\tau_{m-1}, \tau_m)$ 内部，给定当前时刻 $t$、当前现货 $S_t=S$ 以及进入该区间时的离散状态，合约的期望延续价值 $V(t,S)$ 只随当前价格的随机波动而平滑变化，由下一节即将推导的 <MathTerm id="feynman-kac">Feynman–Kac 方程</MathTerm> 转化为一维 <MathTerm id="parabolic-pde">线性抛物型偏微分方程</MathTerm>。
2. **三类路径依赖的解耦压缩**。再看跨越事件时刻 $\tau_m$ 时，可能影响后续现金流的三类历史信息各自如何处理：
   - **是否已敲出**：一旦在某个观察日触发敲出，持有人当场拿到确定金额 $Q_k+C_k(S)$，后续现金流恒为 $0$。敲出态在概率模型中是一个 <MathTerm id="absorbing-state">终止吸收态</MathTerm>，无需为它单独维护网格，只需在该观察日把 $S\ge B^{\text{out}}_k$ 区域的价值直接截断替换为即时兑付额。
   - **历史已付凤凰票息**：由于凤凰票息按期独立结算且漏付不补（无记忆效应），过去某期是否拿过票息，丝毫不改变未来任何一期的派息门槛或敲出门槛。根据期望的线性性质，每期凤凰票息只是在对应观察时刻叠加到存续价值上的一个局部增量 $+C_k(S)$，不增加任何状态变量。
   - **是否曾发生敲入**：这是唯一需要跨期保留到到期日 $T$ 的历史记忆。由于敲入规则只问“存续期内是否**至少有一次**在监测时刻满足 $S<B^{\text{in}}$”，而不关心跌破过几次或最低跌到多少，整条历史路径对未来的影响可无损压缩为一个**一比特布尔状态变量** $j\in\{0,1\}$，其中 $j=0$ 表示“截至当前尚未敲入”，$j=1$ 表示“截至当前已经敲入”。

经过这三步约简，原本依赖整条路径的高维期望计算，等价转化为**耦合的一维分段初边值问题**：至多在同一组空间网格上维护两个二元函数 $V^{(0)}(t,S)$ 与 $V^{(1)}(t,S)$，从到期日 $T$ 逆着时间轴向估值时刻 $t_{\text{val}}$ 交替执行“开区间内求解 PDE 逆推期望”与“事件点上按合约条款代数更新”。

### 3.2 标的资产动力学与方差时钟

为了写出开区间内的偏微分方程，需要先刻画标的资产价格 $S_t$ 在极短时间步 $\Delta t$ 内的随机变化规律。以 Act/365F 自然时间 $t$ 度量日历流逝，记 $u(t)$ 为从起算时刻累积的有效方差时间（Variance Time），其瞬时累积速率记为 $a(t)=du/dt\ge 0$。

先从本科概率论熟悉的离散小步长 $\Delta t > 0$ 来看：在 <MathTerm id="risk-neutral">风险中性测度</MathTerm> $\mathbb Q$ 下，资产在 $[t, t+\Delta t]$ 内的相对涨跌幅 $\Delta S_t / S_t$ 由“确定性平均漂移”和“零均值高斯随机扰动”两部分相加而成：

$$
\frac{\Delta S_t}{S_t}\approx \big(r(t)-q(t)\big)\,\Delta t + \sigma(t,S_t)\sqrt{a(t)\Delta t}\,Z,\qquad Z\sim\mathcal N(0,1).
$$

这里为什么随机项乘的是 $\sqrt{\Delta t}$ 而不是 $\Delta t$？原因来自概率论中**独立随机变量方差的可加性**：把一段有限时间拆成许多互不重叠的独立小步时，总方差等于各小步方差之和，即区间方差必须与时间长度 $\Delta t$ 成正比（等于 $\sigma^2 a(t)\Delta t$）；对它开平方后，**标准差自然就与 $\sqrt{\Delta t}$ 成正比**。令 $\Delta t\to 0$，将累积的正态随机扰动记作 <MathTerm id="brownian-motion">标准布朗运动</MathTerm> $W_t$（其无穷小增量 $dW_t$ 服从均值为 $0$、方差为 $dt$ 的正态分布，形式上可记为 $\sqrt{dt}\,Z$），上述离散关系在连续时间极限下就写作随机微分方程：

$$
\frac{dS_t}{S_t}=\big(r(t)-q(t)\big)\,dt+\sigma(t,S_t)\sqrt{a(t)}\,dW_t ,
$$

其中 $r(t)$ 为瞬时无风险利率，$q(t)$ 为瞬时连续股息率（或融券贴水率；因为股票分红会除息使股价自然下调，风险中性下股价自身的平均增长率为 $r-q$，加上股息 $q$ 后总期望收益率仍等于 $r$）。模型层面的各项输入约定相互独立：

- **波动率函数 $\sigma(t,S)$**：度量单位时间内价格随机摆动的剧烈程度。在 <MathTerm id="bsm-gbm">BSM 模型</MathTerm>（`BlackScholesMertonParameters`）下取常数年化波动率 $\sigma$；在 <MathTerm id="local-volatility">局部波动率</MathTerm> 模型（`LocalVolatilityParameters`）下由二维网格 `LocalVolatilitySurface` 给出，时间轴按距曲面首节点的 Act/365F 年数线性插值，现货轴按绝对价格线性插值，超出曲面现货端点时采用水平常数外推（Flat Extrapolation）。
- **方差时钟 $a(t)$**：默认 `variance_time_convention="actual_365_fixed"` 时假定自然日全天均匀波动，恒有 $a(t)=1$。当设为 `"business"` 时需绑定模型交易日历：设该日历每年的交易日基准天数为 $B$（例如 `weekdays_calendar()` 扣除双休日后 $B=261$），则在开市交易日内速率放大为 $a(t)=365/B$，而在周末及节假日闭市期间停止随机波动（$a(t)=0$），从而使一整年 $B$ 个交易日累加的总方差恰好仍为 $\sigma^2$。
- **曲线与合约计息独立性**：无风险利率与股息率由各自的 `RateTermStructure` 独立决定（支持连续复利常数利率或分段期限结构节点）；合约观察日遵循合约自身的 `calendar`；雪球年化票息与终止返还固定按 Act/365F 自然年折算。切换模型方差时钟不会改变票息计息天数或贴现因子。

### 3.3 事件区间内的后向 Feynman–Kac 方程

直接在现货 $S$ 上建网格时，由于波动幅度 $\sigma S$ 与 $S$ 成正比，高价区的随机扩散步幅远大于低价区。为此，求解器做对数坐标变换 $x=\ln(S/S_{\mathrm a})$（等价于 $S=S_{\mathrm a}e^x$），其中 $S_{\mathrm a}$ 为固定的网格参考水平（定义见第 6.2 节）。记变换后的各层价值函数为 $W^{(j)}(t,x)=V^{(j)}(t,S_{\mathrm a}e^x)$，有效瞬时方差率为 $\nu(t,x)=a(t)\sigma^2(t,S_{\mathrm a}e^x)$。

我们可以用高等数学的**泰勒展开**配合概率论求期望，分两步直观导出 $W^{(j)}(t,x)$ 满足的偏微分方程：

1. **对数价格增量 $\Delta x$ 的均值与方差（<MathTerm id="ito-lemma">Itô 引理</MathTerm> 的直观推导）**。对 $x+\Delta x = \ln(S+\Delta S)-\ln S_{\mathrm a}$ 在 $S$ 处按 $\ln(1+u)=u-\tfrac12 u^2+O(u^3)$ 做二阶泰勒展开：
   $$
   \Delta x = \ln\!\left(1+\frac{\Delta S_t}{S_t}\right) \approx \frac{\Delta S_t}{S_t} - \frac{1}{2}\left(\frac{\Delta S_t}{S_t}\right)^2.
   $$
   在普通微积分中，二阶项 $(\Delta t)^2$ 是高阶无穷小，除以 $\Delta t$ 取极限后会消失；但在这里，$\Delta S_t/S_t$ 含有量级为 $\sqrt{\nu\Delta t}\,Z$ 的随机项，平方后得到 $\big(\Delta S_t/S_t\big)^2 = \nu\Delta t\,Z^2 + O(\Delta t^{3/2})$——它与一阶时间步 $\Delta t$ **同阶**！由于标准正态变量满足 $\mathbb E[Z]=0$、$\mathbb E[Z^2]=\operatorname{Var}(Z)=1$，两边对条件分布取期望与方差并略去高阶项，就得到对数价格在 $\Delta t$ 内的平均漂移与方差：
   $$
   \mathbb E[\Delta x]\approx \underbrace{\Big(r(t)-q(t)-\tfrac{1}{2}\nu(t,x)\Big)}_{\mu(t,x)}\Delta t,\qquad
   \mathbb E\big[(\Delta x)^2\big]\approx \nu(t,x)\,\Delta t.
   $$
   漂移率 $\mu(t,x)$ 中多出来的 $-\tfrac12\nu(t,x)$ 修正项，正是随机波动在二阶泰勒项上留下的平均贡献（随机微积分中称为 <MathTerm id="ito-lemma">Itô 引理</MathTerm>）。
2. **由贴现条件期望导出偏微分方程（<MathTerm id="feynman-kac">后向 Feynman–Kac 方程</MathTerm>）**。在两次合约事件之间的开区间内，当前时刻 $t$ 的价值等于极短时间 $\Delta t$ 之后价值的贴现条件期望：
   $$
   W^{(j)}(t,x)=e^{-r(t)\Delta t}\,\mathbb E\!\Big[W^{(j)}(t+\Delta t,\,x+\Delta x)\,\Big|\,x_t=x\Big].
   $$
   将等式右端的 $e^{-r\Delta t}\approx 1-r\Delta t$ 与 $W^{(j)}(t+\Delta t, x+\Delta x)$ 的二元泰勒展开 $W^{(j)} + \partial_t W^{(j)}\Delta t + \partial_x W^{(j)}\Delta x + \tfrac12\partial_{xx}W^{(j)}(\Delta x)^2 + \cdots$ 相乘并取条件期望，代入刚才算出的 $\mathbb E[\Delta x]\approx \mu\Delta t$ 与 $\mathbb E[(\Delta x)^2]\approx \nu\Delta t$，消去两侧的 $W^{(j)}(t,x)$ 后同除以 $\Delta t$ 并令 $\Delta t\to 0$，即得两次合约事件之间的控制方程：

$$
\partial_t W^{(j)}+\tfrac12\nu(t,x)\,\partial_{xx}W^{(j)}
+\mu(t,x)\,\partial_x W^{(j)}-r(t)W^{(j)}=0,
\qquad j\in\{0,1\}.
$$

利用复合函数求导法则 $\partial_x W=S\partial_S V$ 和 $\partial_{xx}W=S^2\partial_{SS}V+S\partial_S V$ 可以验证，原本现货坐标扩散项中随股价平方剧烈变化的 $S^2\partial_{SS}V$ 因子已被对数坐标变换完全吸收（在常数波动率 BSM 下，$\nu$ 与 $\mu$ 甚至关于空间坐标 $x$ 完全是常数！）。未敲入与已敲入两层共享同一个微分算子和同一组空间网格。每个时间子步在步中点读取 $r$、$q$、方差时钟速率 $a$ 以及各空间节点现货 $S_i=S_{\mathrm a}e^{x_i}$ 处的局部波动率。交易日方差时钟的开闭市切换点被精确选入时间网格；闭市子步内 $\nu=0$，二阶扩散项消失，方程退化为一阶确定性漂移贴现方程 $\partial_t W+(r-q)\partial_x W-rW=0$。

### 3.4 敲入状态分层与双层／单层自动判别

如图 3 所示，在每日敲入模式下，未敲入层 $V^{(0)}$（代码中记作 `alive`）与已敲入层 $V^{(1)}$（代码中记作 `knocked`）沿时间反向同步回推。由于敲入状态一旦触发便不可逆转，两层之间的信息流向是严格单向的：$V^{(1)}$ 完全自洽演化，不依赖 $V^{(0)}$ 的任何数值；而 $V^{(0)}$ 在每个敲入监测时点只需将 $S<B^{\text{in}}$ 区域的函数值覆写为同点的 $V^{(1)}$。

并非所有包含敲入字样的合约都需要同时算两层 PDE。若合约仅在到期日 $T$ 观察敲入（欧式敲入），存续期内根本不会发生状态切换，$V^{(1)}$ 仅在 $T$ 时刻用于拼接 $S<B^{\text{in}}$ 区间的终值，回推全程只需维护单层网格。此外，即便条款声明了每日敲入，若起算前历史状态已处于敲入，或者合约参数使得“敲入与否完全不改变到期支付”，两层价值函数在数学上恒等（$V^{(0)}\equiv V^{(1)}$）。求解器通过布尔条件 `layered = daily && !starting_knocked && note.knock_in_affects_payoff()` 自动判别是否启用双层网格，其中 `knock_in_affects_payoff()` 的充要条件如下：

| 产品 | `knock_in_affects_payoff()` 为真的充要条件 | 条件不成立时的退化结果 |
|---|---|---|
| 雪球 | $L\ne U$ 或 $c_m\ne 0$ | $L=U$ 且 $c_m=0$ 时，无论是否敲入均有 $\Pi^{(0)}(S)=\Pi^{(1)}(S)=P+R(T)$ |
| 三元雪球 | $c_{\min}\ne c_m$ | 保底票息等于到期票息时，两层到期支付恒等 |
| 二元雪球 | 永不成立（条款无敲入障碍） | 始终单层求解 |
| 凤凰 | $L\ne U$ | 凤凰无到期累积红利票息，$L=U$ 时敲入后亏损项恒为 0，两层支付均为 $P+R(T)$ |

当判定无需分层（`layered == false`）时，引擎不仅节省一半的空间内存与线性方程组回代计算量，在隐式 Euler、Crank–Nicolson 及 Rannacher 格式下还能省去将两百余个纯每日敲入交易日插入时间网格的步骤，显著减少时间步数并避免不必要的阻尼重启。

<DualLayerPdeDiagram />

### 3.5 零方差确定性前缀与历史状态衔接

当估值时刻 $t_{\text{val}}$ 恰好落在一段零方差窗口的开头——常见例子是在周六、周日或长假期间使用 `"business"` 交易日方差时钟估值，或者在 BSM 模型中传入极端参数 $\sigma=0$——随机波动直到窗口末端 $t_{\text{start}}=\operatorname{variance\_start}(t_{\text{val}}, T)$ 才真正开始。在 $[t_{\text{val}}, t_{\text{start}}]$ 这一段内，因为随机项消失（$\nu\equiv 0$），价格变化退化为普通微积分中的一阶常微分方程 $dS_t/dt = (r(t)-q(t))S_t$，可直接积分出精确解。若硬把这段零方差区间塞进空间网格做有限差分，一阶导数的离散误差反而会把期间可能发生的观察跳变抹模糊，同时白白消耗时间步。

因此，Kiyosi 采用**确定性前缀剥离 + 随机延续回溯**的两阶段精确分解（`AutocallableState::evaluate`）：

1. **确定性远期前缀结算 $[t_{\text{val}}, t_{\text{start}}]$**：在 $a(t)\equiv 0$ 的区间内，标的现货严格沿常微分方程的指数积分曲线（称为确定性**远期价格轨迹**）运动：
   $$
   F(t)=S_0\exp\!\left(\int_{t_{\text{val}}}^{t}\big(r(u)-q(u)\big)\,du\right).
   $$
   引擎按时间顺序逐一检查 $[t_{\text{val}}, t_{\text{start}}]$ 内的每一个敲出、派息与敲入事件（含 $t_{\text{val}}$ 当期事件），直接拿精确值 $F(t)$ 与各门槛比较：记录是否已变为敲入态 `state.knocked_in`，累加窗口内触发并折现回 $t_{\text{val}}$ 的凤凰票息 `state.coupon`（记为 $C_{\text{prefix}}$），一旦触发敲出或已抵达终点 $T$ 则立即返回精确折现结算值 `state.settlement`。
2. **随机网格延续与链式求导缩放**：若走完确定性前缀到达 $t_{\text{start}}$ 时合约仍存续且未来支付尚未完全锁定（`fixed_value_at(...) == None`），引擎才以 $t_{\text{start}}$ 为起点建立有限差分网格，求出 $[t_{\text{start}}, T]$ 的延续价值函数 $V_{\text{grid}}(t_{\text{start}}, S)$。记 $\gamma=\int_{t_{\text{val}}}^{t_{\text{start}}}(r-q)\,du$ 为对数持有收益（Carry），$\delta=-\int_{t_{\text{val}}}^{t_{\text{start}}}r\,du$ 为对数贴现指数，则 $t_{\text{start}}$ 处的起点价格与初始现货成正比：$S_{\text{start}}=S_0 e^{\gamma}$。由高等数学的复合函数求导法则（每次对 $S_0$ 求导都会多乘一个内层导数 $dS_{\text{start}}/dS_0 = e^{\gamma}$），估值时刻的价格与前 3 阶现货偏导数精确还原为：
   $$
   V(t_{\text{val}},S_0)=C_{\text{prefix}}+e^{\delta}\,V_{\text{grid}}(t_{\text{start}},S_{\text{start}}),\qquad
   \frac{\partial^p V}{\partial S_0^p}(t_{\text{val}},S_0)=e^{\delta+p\gamma}\,\frac{\partial^p V_{\text{grid}}}{\partial S^p}(t_{\text{start}},S_{\text{start}}),\quad p=1,2,3.
   $$

### 3.6 静态复制恒等式（用于理论检验）

为了在后文检验有限差分求解器的代码正确性，我们需要一组完全不依赖网格离散的**精确解析解**。当自动赎回结构退化为“中途不设提前敲出、仅在到期日观察敲出与敲入”时，路径依赖完全消失，最终收益只取决于单个时刻的价格分布。此时利用数学期望的线性性质，可以把复杂的分段到期支付函数拆解为三类拥有初等闭式定价公式（由标准正态分布累积函数 $\Phi(\cdot)$ 表达）的基础合约的线性组合，这种方法在金融数学中称为 <MathTerm id="static-replication">静态复制</MathTerm>：

- **零息债贴现因子 $D(T)=e^{-\int_{t_0}^T r(u)\,du}$**：对应在到期日 $T$ 无条件确定支付 $1$ 元现金的现值。
- **欧式现金或无二元期权 $\mathrm{CoN}^{\text{call}}(K,t)$ 与 $\mathrm{CoN}^{\text{put}}(K,t)$**：对应在时刻 $t$ 按阶跃示性函数 $\mathbf 1_{\{S_t\ge K\}}$（看涨数字）或 $\mathbf 1_{\{S_t < K\}}$（看跌数字）支付 $1$ 元现金的现值。
- **欧式普通看跌期权 $\mathrm{Put}(K,T)$**：对应在到期日 $T$ 按折线函数 $(K-S_T)^+ = \max(K-S_T, 0)$ 支付的现值。

对仅在到期敲出且到期敲入的凤凰，当参数满足 $L\le B^{\text{in}}\le\min(U,B^{\text{out}})$ 时，考察敲入区的分段线性亏损项，容易逐段验证初等代数恒等式 $\mathbf 1_{\{S<B^{\text{in}}\}}(\max(S,L)-U)=-(U-B^{\text{in}})\mathbf 1_{\{S<B^{\text{in}}\}}-\big[(B^{\text{in}}-S)^+-(L-S)^+\big]$（分别代入 $S\ge B^{\text{in}}$、$L\le S<B^{\text{in}}$ 和 $S<L$ 三段即可核对左右恒等）。由于中途不会提前终止，各期派息观察时刻 $t_k$ 与到期亏损完全解耦，两边取贴现期望立得精确初值 $V_0$：

$$
V_0=(P+R(T))\,D(T)+\sum_{k=1}^{n}c\,\mathrm{CoN}^{\text{call}}(B^c_k,t_k)-\frac{(U-B^{\text{in}})\,\mathrm{CoN}^{\text{put}}(B^{\text{in}},T)+\mathrm{Put}(B^{\text{in}},T)-\mathrm{Put}(L,T)}{S_{\text{ref}}}.
$$

同理，对单个敲出观察日 $t_1=T$、仅在到期敲入且满足 $B^{\text{in}}\le B^{\text{out}}$（标准雪球另需 $L\le B^{\text{in}}\le U$）的雪球系列产品，记到期票息额 $A=c_m\tau(T)$、敲出与到期票息差 $\Delta=(r_1-c_m)\tau(T)$，静态复制公式分别为：

$$
\begin{aligned}
V_0^{\text{雪球}}&=(P+R(T)+A)D(T)+\Delta\,\mathrm{CoN}^{\text{call}}(B^{\text{out}},T)-A\,\mathrm{CoN}^{\text{put}}(B^{\text{in}},T)-\frac{(U-B^{\text{in}})\,\mathrm{CoN}^{\text{put}}(B^{\text{in}},T)+\mathrm{Put}(B^{\text{in}},T)-\mathrm{Put}(L,T)}{S_{\text{ref}}},\\
V_0^{\text{三元}}&=(P+R(T)+A)D(T)+\Delta\,\mathrm{CoN}^{\text{call}}(B^{\text{out}},T)-(c_m-c_{\min})\tau(T)\,\mathrm{CoN}^{\text{put}}(B^{\text{in}},T),\\
V_0^{\text{二元}}&=(P+R(T)+A)D(T)+\Delta\,\mathrm{CoN}^{\text{call}}(B^{\text{out}},T).
\end{aligned}
$$

上述闭式恒等式完全独立于 Kiyosi 的任何实现，第 8.1 和 9.1 节直接调用外部库 QuantLib 计算这组公式，作为检验有限差分终端投影、空间加密和贴现逻辑的解析基准。

---

## 4. 边界条件的设置方法与计算域构造

从理论上讲，资产价格 $S$ 可以取 $(0,+\infty)$ 上的任意正实数；但计算机上的有限差分网格只能在有限区间 $[S_{\min}, S_{\max}]$ 内布置有限个节点。在哪里截断计算区间、如何在左右两个端点给定边界条件，直接决定了远场截断误差的大小，以及锁定期、阶梯降敲、无条件派息等条款下的自洽性。

### 4.1 核心前提：离散监测障碍是内部界面而非计算域边界

如果一份合约规定“在存续期内**任意连续时刻** $t\in[t_0,T]$，只要价格一碰到 $B^{\text{out}}$ 就立刻终止”（即连续监测障碍期权），那么价格一旦到达 $B^{\text{out}}$ 就再无后续演化，PDE 计算区间可以直接取 $[S_{\min}, B^{\text{out}}]$，并在右端点 $S=B^{\text{out}}$ 上全时段固定函数值 $V(t, B^{\text{out}})=Q(t)$（偏微分方程中称为 <MathTerm id="dirichlet-affine">第一类吸收边界条件</MathTerm>）。

然而，雪球与凤凰的敲出和敲入均为**离散时点监测**（Discrete Monitoring），门槛绝对不能当成网格截断边界：

- **敲出仅在月度或季度观察时刻 $t_k$ 判定**：在两个观察日之间的开区间 $(t_{k-1}, t_k)$ 内，即便价格大幅冲高至 $S_t > B^{\text{out}}_k$，只要在 $t_k$ 观察时刻到来前回落到 $B^{\text{out}}_k$ 下方，合约就**不会敲出**（见图 1 路径 ② 与图 4a 右侧回弹轨迹）。如果错误地在 $B^{\text{out}}_k$ 处截断网格并强加吸收边界，就会把所有“中途越界但观察日前回落”的路径全部误判为提前敲出，造成严重的系统性偏差。此外，降敲结构（Step-Down）各期的 $B^{\text{out}}_k$ 随时间变化，凤凰锁定期内甚至完全关闭敲出，根本不存在一条全时段固定的截断线。
- **每日敲入同样存在日内与跨日回弹**：每日敲入仅在每个交易日的指定钟点（如收盘 15:00）检查一次。在相邻两次检查之间（含盘中波动及周末休市前后），价格跌破 $B^{\text{in}}$ 后若在观察钟点前拉回 $B^{\text{in}}$ 之上，并不触发敲入（见图 4a 左侧回弹轨迹）；即便已经敲入，价格也仍需在更低区域继续演化，以准确计算到期亏损金额以及日后反弹至 $B^{\text{out}}_k$ 敲出获救的概率。

因此，求解器的现货计算域必须向两侧留足缓冲，取 $[S_{\min},S_{\max}]$（$S_{\min}>0$），将所有正的敲入、敲出、派息和行权价全部包络在**区间内部**，仅在对应事件时刻施加阶跃更新；取值为 $0$ 的下行权价或零派息门槛位于正现货域外，仍作为代数参数参与收益结算。

<BoundaryDomainDiagram />

### 4.2 自动上边界 $S_{\max}$ 的扩散跨度构造

那么上边界 $S_{\max}$ 究竟要推到多远，才能让边界截断对中心区域价格的影响忽略不计？若未显式指定 `asset_upper_boundary`，`diffusion_upper` 利用正态分布尾部快速衰减的性质，按剩余期限内的随机扩散标准差与最大漂移跨度自动估算远场上界。

首先收集所有与剩余随机演化相关的参考价格水平，取其与回溯起点现货的最大值作为特征尺度 $H$：

$$
H=\max\!\Big(\{S_{\text{start}}\}\cup\mathcal L_{\text{contract}}\Big),
$$

其中 $\mathcal L_{\text{contract}}$ 包含严格晚于回溯起点的生效敲出水平 $B^{\text{out}}_k$ 与凤凰票息障碍 $B^c_k$，并按合约条款并入敲入水平 $B^{\text{in}}$、参考价 $S^\ast$ 以及亏损结算的上下行权价 $U,L$（二元雪球仅取剩余敲出水平）。随后在对数价格空间估算剩余期限 $\tau_T$ 内的“4 倍最大扩散标准差 + 最大累积对数漂移幅度”（标准正态分布超出 4 个标准差的单侧概率不足 $3.2\times 10^{-5}$）：

$$
w=4\,\bar\sigma\sqrt{\tau_T}+\max_{e}\Big|\!-\!\ln D_r(0,e)+\ln D_q(0,e)-\tfrac12\bar\sigma^2e\Big|,\qquad
S_{\max}=\begin{cases}4H,&w\le\ln4,\\ H\,e^{w},&w>\ln4.\end{cases}
$$

上述构造通过三项细节保证不同市场环境下的稳健性：

1. **最大波动率包络 $\bar\sigma$**：BSM 下取常数 $\sigma$；局部波动率下，由于双线性插值函数的极值必在矩形网格顶点或截断时间边界上取得，`diffusion_upper` 扫描回溯区间 $[t_{\text{start}}, T]$ 内的全部曲面节点与两端时间切片取精确最大值。若启用 `"business"` 交易日方差时钟，再将 $\bar\sigma$ 乘以 $\sqrt{365/B}$ 换算为自然时间尺度下的有效波动率。
2. **分段曲线节点的漂移极值检查**：公式中的 $-\ln D_r(0,t)+\ln D_q(0,t)=\int_0^t (r(u)-q(u))\,du$ 是累积净漂移。当利率曲线 $r(t)$ 或股息曲线 $q(t)$ 非平坦且正负交替时，对数漂移未必在终点 $T$ 达到最大绝对值。遍历两条曲线在 $(0,\tau_T]$ 内的全部节点 $e$ 取最大值，可防止中途出现大幅正向漂移把价格分布推近 $S_{\max}$。
3. **最低四倍缓冲下限 $4H$**：即便在极短期限（$\tau_T\to 0$）或极低波动率（$\bar\sigma\to 0$）场景下，$w\le\ln 4$ 分支仍强制保证 $S_{\max}\ge 4H$（例如基准合约 $H=100$ 时自动给出 $S_{\max}=400$）。若用户显式传入 `asset_upper_boundary`，引擎在需要建立数值网格时强制校验 $S_{\max}>H$，拒绝任何截断有效合约水平的非法输入。

### 4.3 自动正下边界 $S_{\min}$

因为对数坐标 $x=\ln(S/S_{\mathrm a})$ 在 $S\to 0^+$ 时趋向 $-\infty$，下边界同样需要取一个足够小的严格正数 $S_{\min}>0$。记 $L_+$ 为合约水平中最小的正值（若没有正水平则取回溯起点现货），记 $S_{\text{query,min}}$ 为回溯起点的最低查询现货（单点定价取 $S_{\text{start}}$，批量解取查询区间下端经确定性前缀推进后的现货）。引擎复用第 4.2 节的对数扩散跨度 $w$，取

$$
m=\max(1.5w,\ln 2),\qquad
S_{\min}=\max\!\left(s_{\mathrm{tiny}},\,\min\!\left(L_+e^{-m},\ S_{\text{query,min}}e^{-m/4}\right)\right),
$$

其中 $s_{\mathrm{tiny}}$ 为双精度浮点数 `f64` 可表示的最小正数。两项指数缓冲分别覆盖合约低价区与最低查询点。对于采用 Act/365F 方差时钟、无敲入且只有到期事件的单层 BSM 合约，如果最低查询现货远高于最高合约水平，求解器会在低尾概率可忽略时将下界收至二者的几何中点以集中有效网格分辨率。

### 4.4 边界节点的仿射贴现与事件重置

确定了区间端点 $S_0=S_{\min}$ 和 $S_N=S_{\max}$ 后，如何在每个逆向时间子步 $\Delta t$ 上更新这两个边界节点的价值？

观察图 2 的到期支付曲线可以发现：在极高价区（$S\to S_{\max}$）和极低价区（$S\to S_{\min}$），远离内部门槛后，合约价值关于现货 $S$ 都十分接近一条直线（即 <MathTerm id="dirichlet-affine">仿射函数</MathTerm>）$V(S)\approx A + B S$——高价区几乎是水平常数（$B\approx 0$），而已敲入层的低价未封顶亏损区则是斜率为 $1/S_{\text{ref}}$ 的直线。在金融含义上，$A + B S$ 相当于一个由“现金 $A$”与“$B$ 份标的资产”组成的静态组合：从较晚时刻 $t^+$ 逆推 $\Delta t$ 回到较早时刻 $t^-$ 时，现金项按无风险利率折现为 $A e^{-r_m\Delta t}$，而标的资产项（因持有期间除息率为 $q_m$）按风险中性现值折算为 $B S e^{-q_m\Delta t}$。

具体实现中，引擎在每个子步开始前，利用边界节点 $b$ 与紧邻内部节点 $n$ 在较晚时刻的已知值 $V_b^+, V_n^+$，联立 $V_b^+ = A + B S_b$ 与 $V_n^+ = A + B S_n$ 解出斜率项 $B S_b = \frac{V_n^+ - V_b^+}{(S_n/S_b)-1}$ 与截距 $A = V_b^+ - B S_b$，代入 $V_b^- = A e^{-r_m\Delta t} + B S_b e^{-q_m\Delta t}$ 并利用对数坐标关系 $S_n/S_b = e^{x_n - x_b}$，即得到 `SpatialGrid::discount_affine_edges` 的精确递推式：

$$
V_b^-=V_b^+e^{-r_m\Delta t}
+\frac{V_n^+-V_b^+}{e^{x_n-x_b}-1}
\left(e^{-q_m\Delta t}-e^{-r_m\Delta t}\right).
$$

当低价区价值随现货呈线性变化时，上式第二项准确保留了斜率项在 $r_m\ne q_m$ 下的折现修正；而在远场上边界处 $V_n^+\approx V_b^+$，第二项自动趋零，平滑退化为纯现金贴现 $V_b^+ e^{-r_m\Delta t}$。

在到期时刻及后续每个合约事件时刻，上下两端均直接代入端点价格 $S_{\min}, S_{\max}$ 执行合约支付或阶跃更新：下边界按 $S_{\min}$ 判定敲入、派息与到期损益；上边界在敲出观察日重置为 $Q_k+C_k(S_{\max})$，在仅派息日叠加 $C_k(S_{\max})$。图 4b 展示了上边界近似常值时的逆向贴现与事件重置轨迹，第 8.3 和 9.3 节验证了价格对上边界位置的极低敏感性。

### 4.5 边界条件在三对角线性系统中的消元代入

将空间区间划分为 $N$ 段，共有 $N+1$ 个网格节点，对应现货 $S_{\min}=S_0<S_1<\dots<S_N=S_{\max}$。从线性代数的角度看，在从已知时刻 $t_{m+1}$ 逆推待求时刻 $t_m$（步长 $\Delta t = t_{m+1}-t_m$）之前，首尾两个边界值 $V^m_0$ 与 $V^m_N$ 已经由 4.4 节的公式提前算出，因此真正的未知量只有中间 $N-1$ 个内部节点 $(V^m_1, \dots, V^m_{N-1})^\top$。

在任意内部节点 $i\in\{1,\dots,N-1\}$ 上，第 3.3 节偏微分方程中的空间导数项经相邻三点差分离散后，可写成线性组合 $(\mathcal A V)_i = a_i V_{i-1} + b_i V_i + c_i V_{i+1}$（具体系数见第 6.3 节）。对时间导数 $\big(V^{m+1}_i - V^m_i\big)/\Delta t$ 搭配权重参数 $\theta\in[0,1]$ 对两端时刻的空间算子做加权平均（$\theta=0$ 为完全用已知时刻计算的显式 Euler，$\theta=1$ 为完全用待求时刻联立的隐式 Euler，$\theta=\tfrac12$ 为两端对半平均的 Crank–Nicolson），整理出把待求时刻 $V^m$ 放左边、已知时刻 $V^{m+1}$ 放右边的线性方程（见图 4c 及 `Stepper::apply`）：

$$
-\theta\Delta t\,a_i V^m_{i-1}+\big(1-\theta\Delta t\,b_i\big)V^m_i-\theta\Delta t\,c_i V^m_{i+1}
=V^{m+1}_i+(1-\theta)\Delta t\big(a_i V^{m+1}_{i-1}+b_i V^{m+1}_i+c_i V^{m+1}_{i+1}\big).
$$

由于第 $i$ 个方程只牵涉 $i-1, i, i+1$ 三个相邻未知数，只需在第一行（$i=1$）和最后一行（$i=N-1$）中把已知边界项 $\theta\Delta t\,a_1 V^m_0$ 与 $\theta\Delta t\,c_{N-1} V^m_N$ 移到等号右端向量（RHS），左端系数矩阵就严格保持 $(N-1)\times(N-1)$ <MathTerm id="tridiagonal-thomas">三对角矩阵</MathTerm> 结构：

$$
\begin{aligned}
\mathrm{rhs}_1 &= V^{m+1}_1 + (1-\theta)\Delta t\big(a_1 V^{m+1}_0 + b_1 V^{m+1}_1 + c_1 V^{m+1}_2\big) + \theta\Delta t\,a_1 V^m_0, \\[4pt]
\mathrm{rhs}_{N-1} &= V^{m+1}_{N-1} + (1-\theta)\Delta t\big(a_{N-1} V^{m+1}_{N-2} + b_{N-1} V^{m+1}_{N-1} + c_{N-1} V^{m+1}_N\big) + \theta\Delta t\,c_{N-1} V^m_N.
\end{aligned}
$$

实现中当 $\theta=1$（隐式 Euler 及 Rannacher 阻尼半步）时直接略去右端的 $(1-\theta)$ 显式组合项，仅保留 $V^{m+1}_i$ 与两端隐式边界补偿项，既节省浮点乘加，又避免极端粗网格下未使用的显式项发生大数溢出。

### 4.6 计算域与工作量有效性检查

定价前及回溯过程中，求解器执行以下完备性校验，以防数值失真或资源耗尽：

- **边界覆盖与网格可表性**。边界须有限且满足 $0<S_{\min}<S_{\max}$，上边界须严格大于关注水平 $H$，相邻对数节点及其对应现货在双精度浮点下须严格可区分。校验失败时返回 `InvalidInput`。
- **事件时刻浮点分辨率**：相邻事件换算为年化时间后若在双精度浮点下无法区分，返回 `ComputationFailure`（`validate_event_resolution`）。
- **显式格式 <MathTerm id="cfl-condition">CFL 稳定性条件</MathTerm> 校验**。选择显式格式 `explicit_euler`（$\theta=0$）时，时间步过大会导致中心点权重变负而引起误差指数爆炸，故强制要求 $\Delta t\cdot\max_i(-b_i)\le 1$。Act/365F 方差时钟下的 BSM 网格预检全部时间步，推进时也检查当前系数；条件不满足时返回 `InvalidInput`。
- **内存与计算预算护栏**：预计工作区内存超过 1 GiB（`validate_workspace`，计入三对角缓存、双层向量与曲线节点开销），或预计总网格节点更新次数超过 $10^9$（`validate_work`，计入事件插点、Rannacher 阻尼分裂半步与状态层数）时，提前返回 `InvalidInput`。
- **运行时数值健康检查**：局部波动率逐步矩阵消元或回代过程中若出现 `NaN`、`Inf` 或消元主元为零，立即中止并返回 `ComputationFailure`（`unstable`）。

---

## 5. 观察日阶跃条件的应用逻辑

开区间内的偏微分方程刻画了无事件期间资产价格的连续随机波动，而**观察日与监测日的阶跃条件（Step / Jump Conditions）**则负责把雪球和凤凰的合约条款镶嵌进逆向递推链条。无论是提前敲出终止、凤凰条件派息，还是每日敲入引发的层间切换，在逆向时间网格上都表现为跨越事件时刻 $t_k$ 前后无穷小邻域 $[t_k^-, t_k^+]$ 的瞬时分段映射。

### 5.1 后向时间记号 $t_k^+ \to t_k^-$ 与条款触发优先级

初学者阅读逆向 PDE 文献时，最容易混淆的是高等数学左极限 $t_k^-$、右极限 $t_k^+$ 与算法计算先后顺序之间的对应关系。记住一条准则即可：**日历时间从左往右走（$t_k^- \to t_k^+$），而求解器逆着时间从右往左推（$t_k^+ \to t_k^-$）**：

- **事件后极限 $t_k^+$（右极限，$\lim_{\epsilon\downarrow 0} (t_k+\epsilon)$）**：按日历顺序看，位于 $t_k$ 观察动作刚刚结束之后。对逆向求解器而言，$V^{(j)}(t_k^+, S)$ 是从后一段区间 $(t_k, t_{k+1})$ 完成 PDE 求解后**已经拿到手的输入函数**（仅反映未来延续价值，尚未计入 $t_k$ 当期任何现金流或状态切换）。
- **事件前极限 $t_k^-$（左极限，$\lim_{\epsilon\downarrow 0} (t_k-\epsilon)$）**：按日历顺序看，位于即将踏入 $t_k$ 观察判定之前。$V^{(j)}(t_k^-, S)$ 是把 $t_k$ 当期的敲出、派息与敲入规则施加到 $V^{(j)}(t_k^+, S)$ 上之后**新算出的输出函数**，随后作为前一段区间 $(t_{k-1}, t_k)$ 继续往回求解的起始条件。

在通用合约下，同一个时间戳 $t_k$ 可能同时挂载至多三项条款：敲出观察（$\chi_k=1$）、凤凰派息观察（存在 $B^c_k$）以及每日敲入监测（$\kappa_k=1$）。Kiyosi 严格按照合约结算规则执行以下**触发优先级与不等号方向**：

1. **不等号方向非对称性**：敲出条件 $S\ge B^{\text{out}}_k$ 与凤凰派息条件 $S\ge B^c_k$ 均**包含等号**（向上触及门槛即生效，使价值函数在 $B^{\text{out}}_k$ 与 $B^c_k$ 处保持右连续）；敲入条件 $S < B^{\text{in}}$ 则为**严格小于号**（现货恰好等于 $B^{\text{in}}$ 时不触发敲入，同样使函数在 $B^{\text{in}}$ 处保持右连续）。
2. **敲出终止具有最高优先级**：只要 $\chi_k=1$ 且 $S\ge B^{\text{out}}_k$，无论当前处于未敲入层（$j=0$）还是已敲入层（$j=1$），合约均当即终止赎回，后续延续价值 $V^{(j)}(t_k^+,S)$ 被直接舍弃并替换为敲出兑付额 $Q_k$。
3. **同日派息与敲出累加、与存续叠加**：凤凰在同一时刻若既满足派息条件 $S\ge B^c_k$ 又满足敲出条件 $S\ge B^{\text{out}}_k$，持有人**同时获得当期票息与敲出本金返还**（即 $Q_k + c$）；若未触发敲出（$S < B^{\text{out}}_k$ 或处于锁定期 $\chi_k=0$），当期合资格票息 $C_k(S)$ 直接加在延续价值之上。
4. **未敲出前提下的单向敲入层切换**：仅当当期未发生敲出（$\chi_k=0$ 或 $S < B^{\text{out}}_k$），且当前位于未敲入层（$j=0$）、该时刻为敲入监测点（$\kappa_k=1$）并满足 $S < B^{\text{in}}$ 时，后续延续价值由 $V^{(0)}(t_k^+,S)$ 切换为已敲入层的延续价值 $V^{(1)}(t_k^+,S)$，再叠加当期可能存在的无条件或低门槛凤凰票息 $C_k(S)$（例如 FCN 的 $B^c_k=0 < B^{\text{in}}$ 时，即使敲入当期仍照付票息 $c$）。

### 5.2 终端条件与各类事件日的阶跃映射公式

综合上述优先级，记下标 $n$ 对应到期时刻 $T$（若 $T$ 无派息观察则 $C_n(S)\equiv 0$，若 $T$ 无敲出观察则 $\chi_n=0$），四类产品在所有事件节点上的状态更新可统一写为如下分段函数。

**(1) 到期时刻 $T$ 的终端初值条件**（`pricing::expiry_payment`）：

$$
\begin{aligned}
V^{(1)}(T,S)&=C_n(S)+\begin{cases}
Q_n,&\chi_n=1,\ S\ge B^{\text{out}}_n,\\[3pt]
\Pi^{(1)}(S),&\text{否则},
\end{cases}\\[6pt]
V^{(0)}(T,S)&=C_n(S)+\begin{cases}
Q_n,&\chi_n=1,\ S\ge B^{\text{out}}_n,\\[3pt]
\Pi^{(1)}(S),&\big(\chi_n=0\ \text{或}\ S<B^{\text{out}}_n\big)\ \text{且}\ \kappa_n=1,\ S<B^{\text{in}},\\[3pt]
\Pi^{(0)}(S),&\text{否则}.
\end{cases}
\end{aligned}
$$

**(2) 存续期内一般观察时刻 $t_k\in(t_{\text{val}}, T)$ 的后向阶跃条件**（如图 5 所示）：

$$
\begin{aligned}
V^{(1)}(t_k^-,S)&=C_k(S)+\begin{cases}
Q_k,&\chi_k=1,\ S\ge B^{\text{out}}_k,\\[3pt]
V^{(1)}(t_k^+,S),&\text{否则},
\end{cases}\\[6pt]
V^{(0)}(t_k^-,S)&=C_k(S)+\begin{cases}
Q_k,&\chi_k=1,\ S\ge B^{\text{out}}_k,\\[3pt]
V^{(1)}(t_k^+,S),&\big(\chi_k=0\ \text{或}\ S<B^{\text{out}}_k\big)\ \text{且}\ \kappa_k=1,\ S<B^{\text{in}},\\[3pt]
V^{(0)}(t_k^+,S),&\text{否则}.
\end{cases}
\end{aligned}
$$

<ObservationStepDiagram />

对照图 5 的函数图像，这一映射在不同日程类型下的几何形态一目了然：

- **雪球月度观察日（图 5a，$\chi_k=1,\ C_k\equiv 0$，通常与当日敲入监测同刻 $\kappa_k=1$）**：横轴被 $B^{\text{in}}$ 与 $B^{\text{out}}_k$ 切成三段。在右侧敲出区 $[B^{\text{out}}_k, S_{\max}]$，$V^{(0)}$ 与 $V^{(1)}$ 均被拉平为水平常数 $Q_k=P+R(t_k)+r_k\tau(t_k)$；在中间安全存续区 $[B^{\text{in}}, B^{\text{out}}_k)$，$V^{(0)}$ 原封不动保留光滑延续曲线；在左侧敲入区 $[S_{\min}, B^{\text{in}})$，$V^{(0)}$ 向下跌落贴合到已敲入层曲线 $V^{(1)}(t_k^+,S)$ 上，在 $B^{\text{in}}$ 处形成高度为 $V^{(1)}(t_k^+,B^{\text{in}})-V^{(0)}(t_k^+,B^{\text{in}})<0$ 的向下垂直断层。
- **凤凰完整观察日（图 5b，$\chi_k=1,\ \kappa_k=1$，典型参数满足 $B^{\text{in}}\le B^c_k < B^{\text{out}}_k$）**：横轴细分为四段。相较于雪球，在 $[B^c_k, B^{\text{out}}_k)$ 区间内，$V^{(0)}$ 与 $V^{(1)}$ 两条延续曲线同时向上刚性平移一个固定票息高度 $+c$；在 $[B^{\text{out}}_k, S_{\max}]$ 敲出区，兑付平台高度定格在 $P+R(t_k)+c$。若合约设定 $B^c_k=B^{\text{in}}$（如第 7.4 节凤凰基准），则第 Ⅱ 区宽度收缩为零，敲入切换跳变与数字派息跳变在 $S=B^{\text{in}}$ 同一点叠加。
- **凤凰锁定期或独立派息日（$\chi_k=0$）与独立敲出日（$C_k\equiv 0$）**：当凤凰敲出日程与票息日程错开，或处于前若干期敲出锁定期时，令 $\chi_k=0$ 即得纯派息日阶跃——全区间不发生敲出拉平，仅在 $[B^c_k, S_{\max}]$ 上整体抬升 $+c$（若同刻含每日敲入则叠加左侧层切换）；反之在无派息的纯敲出日令 $C_k\equiv 0$，即与雪球三区映射完全一致。
- **纯每日敲入监测日（非观察普通交易日，$\chi_k=0,\ C_k\equiv 0,\ \kappa_k=1$）**：已敲入层 $V^{(1)}(t^-,S)=V^{(1)}(t^+,S)$ 原样穿过、不受任何扰动；未敲入层仅执行单侧替换：
  $$
  V^{(0)}(t^-,S)=\begin{cases}
  V^{(1)}(t^+,S),&S<B^{\text{in}},\\
  V^{(0)}(t^+,S),&S\ge B^{\text{in}}.
  \end{cases}
  $$

### 5.3 雪球与凤凰的空间间断谱对比

数值偏微分方程的收敛速度与稳定性难点，直接取决于终端条件和各观察日映射在空间方向制造的非光滑点——按高等数学术语，分为函数值本身突变的 <MathTerm id="c0-c1-discontinuity">第一类跳跃间断与斜率折角</MathTerm>（即 $C^0$ 跳跃与连续不可导的 $C^1$ 拐点）。下表以第 7.4 节的一年期基准合约（$\tau(T)=1, S_{\text{ref}}=U=B^{\text{out}}=100, B^{\text{in}}=B^c=70, L=0, c_m=r_k=15\%, c=0.8\%$）为例，对比四类产品在各关键价位上的间断强度（若同一时刻多个门槛重合，跳跃量代数相加）：

| 空间位置 | 凤凰基准 | 雪球基准 | 三元雪球 | 二元雪球 |
|---|---|---|---|---|
| 到期 $B^{\text{in}}$ 处（未敲入层 $V^{(0)}$） | 敲入跳跃 $(U-B^{\text{in}})/S_{\text{ref}}=0.30$（重合 $B^c_n$ 时再加 $c=0.008$） | 跳跃 $c_m\tau(T)+(U-B^{\text{in}})/S_{\text{ref}}=0.45$ | 跳跃 $(c_m-c_{\min})\tau(T)=0.12$ | 无 |
| 到期 $B^{\text{out}}_n$ 处 | 已敲入层跳跃 $(U-\max(L,B^{\text{out}}_n))^+/S_{\text{ref}}$（基准 $U=B^{\text{out}}_n$ 为 0，仅折角） | 未敲入层在 $r_n=c_m$ 时连续；已敲入层跳跃 $r_n\tau(T)+(U-B^{\text{out}}_n)^+/S_{\text{ref}}=0.15$ | 未敲入层同雪球；已敲入层跳跃 $(r_n-c_{\min})\tau(T)=0.12$ | $r_n\ne c_m$ 时跳跃 $(r_n-c_m)\tau(T)$ |
| 存续期观察日 $B^{\text{out}}_k$ 处 | $Q_k+C_k(B^{\text{out}}_k)-V^{(j)}(t_k^+,B^{\text{out}}_k)$ | $Q_k-V^{(j)}(t_k^+,B^{\text{out}}_k)$，随累积计息期 $\tau(t_k)$ 递增 | 同雪球 | 同雪球 |
| 存续期观察日 $B^c_k$ 处 | 数字票息正跳跃 $+c=0.008$ | 无 | 无 | 无 |
| 每日监测日 $B^{\text{in}}$ 处（未敲入层） | 层差跳跃 $V^{(1)}(t^+,B^{\text{in}})-V^{(0)}(t^+,B^{\text{in}})$ | 层差跳跃 $V^{(1)}(t^+,B^{\text{in}})-V^{(0)}(t^+,B^{\text{in}})$ | 层差跳跃 $V^{(1)}-V^{(0)}$ | 无 |
| 行权价 $U$、$L$ 处 | 斜率折角（$C^0$ 连续，$C^1$ 间断） | 斜率折角（$C^0$ 连续，$C^1$ 间断） | 无 | 无 |

从概率直觉上可以理解一个有趣现象：在每日敲入合约中，存续期早期的单日敲入层差 $|V^{(0)}(t^+,B^{\text{in}})-V^{(1)}(t^+,B^{\text{in}})|$ 其实非常小（基准参数下仅约 $0.002\sim 0.004$）。因为当股价已经贴着 $B^{\text{in}}$ 上沿走时，即便今天侥幸没破线，后面还有两百多个交易日要过，未来某天跌破 $B^{\text{in}}$ 的条件概率极高，所以 $V^{(0)}$ 在 $B^{\text{in}}$ 右侧的值早已被拉近 $V^{(1)}$；但越临近到期日 $T$，剩下的监测天数屈指可数，“再撑一两天不破线就能全额保住本金和到期票息”的概率陡增，两层之间的落差随之急剧拉大，直至在 $T$ 时刻达到 $0.308$（凤凰）或 $0.45$（标准雪球）。标准雪球在到期敲入线上的跳变高度比凤凰大出近一半，正是雪球在默认网格下对时间阻尼与空间投影精度更为敏感的原因。

### 5.4 控制体积跳跃修正投影：为什么只投影增量 $\Delta V$

要把 5.2 节含跳跃的分段函数离散到对数网格节点 $\{x_i\}_{i=0}^N$（对应现货 $S_i=S_{\mathrm a}e^{x_i}$）上，最朴素的做法是**逐节点直接代值**：令 $V_i^- = V^-(S_i)$。但这种做法和传统的整值积分平均各有明显缺陷：

1. **逐点采样引发 $O(h)$ 阶梯抖动误差**：当某个观察日的敲出水平 $B^{\text{out}}_k$ 或票息门槛 $B^c_k$（例如多期降敲中有十几个不同水平，或与别的水平相距极近而未能全部对齐格点）落在两个网格节点 $(S_{i-1}, S_i)$ 中间时，只要门槛没跨过节点，所有 $V^-(S_i)$ 的采样值都纹丝不动，一旦跨过节点又突然跳变。这会导致算出的期权价格随门槛微调呈锯齿状跳动，空间收敛阶从二阶跌落为一阶。
2. **整值单元平均在高频监测下造成人工模糊（数值耗散）**：如果换一种思路，围绕每个节点 $x_i$ 取左右相邻中点围成的小区间 $C_i=[x_{i-1/2}, x_{i+1/2}]$（称为 <MathTerm id="control-volume">对偶控制体积</MathTerm>），每次事件都用区间定积分均值 $V_i^- = \frac{1}{|C_i|}\int_{C_i} V^-(S(x))\,dx$ 更新节点值，虽然消除了锯齿，但在一年约 250 个每日敲入监测日上，哪怕在根本没有发生跳跃的光滑区域，每次积分重算都会像均值滤波一样把光滑曲线额外抹平一点，累计产生高达 $O(M_{\text{events}} h^2)$ 的人工耗散误差。

为兼顾两侧优势，Kiyosi 在 `autocallable.rs` 与 `grid::project_in_coordinates` 中设计了**控制体积增量跳跃修正投影（Incremental Jump-Correction Projection）**。做法非常直观——先把更新后的价值恒等拆成“已知光滑网格解 + 局部跳跃修正量”：

$$
V^{(j)}(t_k^-, S) = V^{(j)}(t_k^+, S) + \Delta V^{(j)}(S),\qquad j\in\{0,1\},
$$

其中增量跳跃函数 $\Delta V^{(0)}(S)$ 与 $\Delta V^{(1)}(S)$ 只在发生敲出、派息或敲入层切换的区域非零：

$$
\begin{aligned}
\Delta V^{(0)}(S) &= \begin{cases}
Q_k + C_k(S) - I_{\text{lin}}[V^{(0)+}](S), & \chi_k=1,\ S\ge B^{\text{out}}_k, \\[4pt]
\big(I_{\text{lin}}[V^{(1)+}](S) - I_{\text{lin}}[V^{(0)+}](S)\big)\mathbf 1_{\{\kappa_k=1,\,S<B^{\text{in}}\}} + C_k(S), & \text{否则},
\end{cases} \\[6pt]
\Delta V^{(1)}(S) &= \begin{cases}
Q_k + C_k(S) - I_{\text{lin}}[V^{(1)+}](S), & \chi_k=1,\ S\ge B^{\text{out}}_k, \\[4pt]
C_k(S), & \text{否则}.
\end{cases}
\end{aligned}
$$

这里 $I_{\text{lin}}[V^{(j)+}](S)$ 表示在对数坐标 $x=\ln(S/S_{\mathrm a})$ 上对离散节点向量 $V^{(j)+}$ 做分段线性插值（`SpatialGrid::linear`）。对每个内部节点 $i\in\{1,\dots,N-1\}$，取其对偶控制体积 $C_i=[x_{i-1/2}, x_{i+1/2}]$，其中左右界面为相邻节点中点 $x_{i-1/2}=\tfrac12(x_{i-1}+x_i)$、$x_{i+1/2}=\tfrac12(x_i+x_{i+1})$。如图 6b 所示，投影算法分四步只对增量 $\Delta V$ 求单元平均：

1. **收集当期精确间断切分点 `breaks`**：终端时刻 $T$ 收集 $\{B^{\text{in}}, L, U, B^{\text{out}}_n, B^c_n\}$（含看跌价差折角点 $L,U$，此时尚无先验网格解，直接对终值函数 `expiry_payment` 做单元积分平均）；存续期事件时刻 $t_k<T$ 收集当期实际生效的 $\{B^{\text{out}}_k, B^c_k\}$，若当期含分层敲入监测则并入 $B^{\text{in}}$。所有正切分水平 $B$ 都精确映射为 $\ln(B/S_{\mathrm a})$，包括因间距过近未成为网格节点的水平；零水平位于正现货域外，无需加入切分。
2. **非跨界光滑单元直接放行（图 6b 左）**：检查是否有间断点严格落在开区间 $(x_{i-1/2}, x_{i+1/2})$ 内部。若没有（绝大多数网格单元都属于此类），完全不做数值积分，直接取中心节点值 $\overline{\Delta}_i = \Delta V(S_i)$。因为线性插值在网格节点上恒满足 $I_{\text{lin}}[V^+](S_i) \equiv V^+_i$，所以在无当期票息、无状态切换、无敲出的区域恒有 $\Delta V(S_i)=0$，即 $V^-_i = V^+_i$ 原样保留，零平滑损耗；而在 $S_i < B^{\text{in}}$ 的纯敲入区内部单元，也有 $V^{(0)-}_i = V^{(0)+}_i + (V^{(1)+}_i - V^{(0)+}_i) = V^{(1)+}_i$，实现精确逐点赋值。
3. **跨障碍界面单元的子区间精确切分（图 6b 右）**：若 $(x_{i-1/2}, x_{i+1/2})$ 内部包含一个或多个间断点，算法将单元左右端点、内部间断点坐标**以及节点中心坐标 $x_i$** 合并排序去重，把 $C_i$ 切成若干互不重叠的子区间 $I_m=[p_m, p_{m+1}]$。把中心 $x_i$ 也作为切分点是关键细节：因为分段线性插值函数 $I_{\text{lin}}[V^+]$ 恰好在节点 $x_i$ 处拐弯（左右斜率不同），显式在 $x_i$ 切开后，$\Delta V(S(x))$ 在每个开子区间 $(p_m, p_{m+1})$ 上都变成光滑无拐点的函数。
4. **子区间 <MathTerm id="gauss-legendre">两点 Gauss–Legendre 求积</MathTerm> 合成**：在每个光滑子区间 $I_m$（中点 $c_m=\tfrac12(p_m+p_{m+1})$，长度 $|I_m|=p_{m+1}-p_m$）上取对称高斯求积节点 $c_m\pm\rho_m$（其中 $\rho_m=\frac{|I_m|}{2\sqrt 3}$，对任意三次及以下多项式定积分精确成立），代回 $S(x)=S_{\mathrm a}e^x$ 计算跳跃修正量，再按子区间长度占比加权求和，得到定积分均值 $\overline{\Delta}_i=|C_i|^{-1}\int_{C_i}\Delta V(S(x))\,dx$ 的高精度近似并更新节点值：
   $$
   \overline{\Delta}_i=\sum_{m}\frac{|I_m|}{|C_i|}\cdot\frac{\Delta V\big(S(c_m-\rho_m)\big)+\Delta V\big(S(c_m+\rho_m)\big)}{2},\qquad
   V^{(j)-}_i = V^{(j)+}_i + \overline{\Delta}^{(j)}_i .
   $$

在分层模式下，$V^{(0)}$ 与 $V^{(1)}$ 共享同一组切分点与高斯求积节点，单次循环同步完成积分。第 8.8 与 9.8 节检验了相距仅约 $0.1\%$ 的合约水平在不同网格下的价格误差。

<JumpProjectionDiagram />

### 5.5 估值时刻当期事件的精确点值处理

需要特别区分概率含义：**控制体积积分投影只用于未来事件时刻 $t > t_{\text{val}}$**（在 PDE 回溯网格中对应 `time > 0.0`），绝不用于估值时刻 $t = t_{\text{val}}$ 本身。原因来自随机变量与已知常数的本质区别：未来时刻的价格 $S_{t_k}$ 是具有连续概率密度的随机变量，跨门槛单元内有一部分概率落在线上、一部分落在线下，因而需要按区间长度积分求平均；而在当前估值时刻 $t_{\text{val}}$，市场现货 $S_0$ 是一个**已经观测到的确定实数**，没有任何分布不确定性，触发与否非黑即白。

因此，`pricing::initial` 与确定性路径在 $t_{\text{val}}$ 处严格按已知标量 $S_0$ 做一次性点值判定：

- 若历史状态 `barrier_state == "knocked_out"`：合约早已终止，直接返回现值 $0$。
- 若 $t_{\text{val}}$ 恰好落在每日敲入监测钟点且 $S_0 < B^{\text{in}}$：立即将当前状态置为已敲入（此后若仍需 PDE 回溯，直接切换为单层已敲入求解）。
- 若 $t_{\text{val}}$ 恰好是派息或敲出观察时刻：按 $S_0\ge B^c_0$ 计入一次当期凤凰票息；若同时满足 $\chi_0=1$ 且 $S_0\ge B^{\text{out}}_0$，直接返回敲出兑付额加当期票息，无需启动 PDE。
- 若 $t_{\text{val}} = T$：直接调用 `expiry_payment` 返回精确到期结算额。

---

## 6. 空间时间离散化、阻尼格式与算法实现

### 6.1 求解总体流程

`FiniteDifferenceAutocallableEngine::price` 与 `price_with_greeks` 通过内部入口 `native` 串联起三步计算流程：

1. **前置校验与确定性分流**：校验模型适用性、合约存续期、历史状态自洽性及利率股息曲线覆盖范围；识别零方差前缀 $[t_{\text{val}}, t_{\text{start}}]$ 并沿确定性远期轨迹结算该前缀内的事件。若合约已终止、剩余现金流已完全确定（`fixed_value_at` 命中，例如无敲入、无条件派息且敲出支付贴现值恒等于到期贴现值的退化情形），或整段剩余期限均为零方差，则直接返回精确解析贴现值。
2. **网格构造与双层回溯（`solve_grid`）**：以 $t_{\text{start}}$ 为起点构造插入全部未来事件与模型节点的时间网格（并加密近估值首段），生成向各合约门槛聚集的对数现货网格，通过控制体积投影初始化 $T$ 时刻终值，再逆着时间步进求解三对角方程组，每遇事件点执行增量跳跃修正投影并重启 Rannacher 阻尼。BSM 与局部波动率通过 Rust 编译期单态化的 `Diffusion` trait 共享同一套回溯循环，省去内层循环的动态虚函数调用开销。
3. **样条提取与敏感度合成**：在回溯终点构建带过冲保护的对数现货三次样条，提取延续价值及对现货的一、二、三阶偏导数（原生 Delta、Gamma、Speed），合并前缀票息与贴现缩放因子；若请求了对波动率、利率或时间的偏导数（Vega、Rho、Theta），则在固定中心网格上界 $S_{\max}$ 的前提下通过微扰重算补全。参见[有限差分入口](https://github.com/lilkui/kiyosi/blob/d8413d14ab2f7a53ecc3df145d394bd3c5ba783e/crates/kiyosi/src/engines/finite_difference/autocallable.rs)。

### 6.2 空间网格：均匀对数坐标与分段 $\sinh$ 加密

在总节点数 $N+1$ 固定的情况下，把网格点均匀撒在全区间并不划算——在远离门槛的高价区和极低价区，价值曲线几乎是平直的，稀疏几个点就够用；而在敲入线、敲出线和派息线附近，价值函数存在剧烈跳跃与弯曲，需要密集排布节点才能看清细节。

`SpatialGrid` 以最高合约水平（无合约水平时取回溯起点现货）作为参考价 $S_{\mathrm a}$，并将其限制在 $[S_{\min},S_{\max}]$ 内。基础网格先在对数区间 $[x_{\min},x_{\max}]$ 上等距划分为 $N$ 段（`asset_step_count`，默认 800），其中 $x_{\min}=\ln(S_{\min}/S_{\mathrm a})$、$x_{\max}=\ln(S_{\max}/S_{\mathrm a})$，对应的现货节点 $S_i=S_{\mathrm a}e^{x_i}$ 呈等比数列排列。显式 Euler 格式直接使用这组均匀对数节点。

其余隐式与半隐式时间格式通过 `grid::concentrate` 执行 <MathTerm id="sinh-grid">双曲正弦（sinh）分段加密</MathTerm>（图 6a）。双曲正弦函数 $\sinh(u)=(e^u-e^{-u})/2$ 在原点附近斜率最小（$\sinh u\approx u$）、向远处指数增大，非常适合生成“锚点旁极细、向远端平滑拉宽”的非均匀坐标。候选锚点收集剩余生效敲出水平、凤凰派息水平，以及条款适用的敲入水平、参考价和上下行权价。对数坐标的加密尺度参数取

$$
s_c=\max\!\left(
0.001\sqrt{\min(365\tau_{\text{near}},1)},\
0.01\,\sigma(t_{\text{start}},H_{\text{levels}})\sqrt{\tau_{\text{near}}},\
64\varepsilon
\right),
$$

其中 $H_{\text{levels}}$ 是加密前取的最高合约水平（无合约水平时取回溯起点现货），$\tau_{\text{near}}$ 是距回溯起点最近的未来事件、曲线节点、局部波动率时间切片或方差时钟切换点的时间间隔，$\varepsilon\approx 2.22\times 10^{-16}$ 为双精度机器精度。具体生成分三步：

1. **筛选保留锚点**：将域内正水平映射为对数坐标、排序并去重。若某候选点距前一个已保留坐标（首点从 $x_{\min}$ 起算）或距右端点 $x_{\max}$ 小于最小间距阈值 $g=s_c\operatorname{asinh}((x_{\max}-x_{\min})/s_c)/N$，则跳过该候选点，防止极近水平挤占过多微步（被跳过的水平仍会在 5.4 节的控制体积积分中被精确切分）。
2. **中点切段与步数分配**：在每对相邻保留锚点的对数中点（对应现货的几何平均数 $\sqrt{S_a S_b}$）处切分，使每个单调子段恰好有一端是锚点。若子段数超过 $N$ 则回退到基础均匀网格；否则每段先保底分配 1 步，剩余步数按反双曲正弦伸缩权重 $w(a,b)=\operatorname{asinh}((b-a)/s_c)$ 比例分配，并按最大余数法补齐总步数 $N$。
3. **按 $\sinh$ 映射生成节点**：左端 $a$ 为锚点的子段取 $x=a+s_c\sinh(j\Delta\xi)$，右端 $b$ 为锚点的子段取 $x=b-s_c\sinh((n-j)\Delta\xi)$（$j=0,\dots,n$）。其中 $n$ 为该段步数，参数步长 $\Delta\xi$ 取总伸缩宽度除以 $N$ 与各多步子段 $w(a,b)/(n-0.5)$ 中的最小值。各子段终点精确对齐 $b$，保留锚点处的现货坐标直接存入原始合约水平浮点值，杜绝 $\exp(\ln B)$ 往返转换带来的末位舍入误差。

### 6.3 对数网格三点算子与漂移占优处理

非均匀对数网格建好后，需要在每个内部节点 $x_i$ 上用左、中、右三个相邻节点 $(W_{i-1}, W_i, W_{i+1})$ 近似第 3.3 节 PDE 中的空间导数项 $\tfrac12\nu\partial_{xx}W + \mu\partial_x W - rW$。记左步长 $h_-=x_i-x_{i-1}$、右步长 $h_+=x_{i+1}-x_i$，现货相对间距 $d_-=1-e^{-h_-}$、$d_+=e^{h_+}-1$，现货持有收益率 $\lambda=r-q$，对数漂移率 $\mu=\lambda-\nu/2$。空间离散算子统一写成：

$$
(\mathcal A W)_i=a_i(W_{i-1}-W_i)+c_i(W_{i+1}-W_i)-rW_i .
$$

如何确定左右权重 $a_i$ 和 $c_i$？从概率论视角看，若把离散算子视作节点间的瞬时随机跳变，$a_i\Delta t$ 和 $c_i\Delta t$ 分别对应向左跳 $-h_-$ 和向右跳 $+h_+$ 的局部转移权重。`LogStencil` 采用 <MathTerm id="moment-upwind">一阶矩匹配与迎风非负约束</MathTerm>：要求离散跳变同时精确匹配**对数坐标的一阶矩（期望漂移率 $\mu$）**与**现货坐标的一阶矩（期望收益率 $\lambda$）**，这就给出关于 $(a_i, c_i)$ 的二元一次方程组：

$$
-a_i h_- + c_i h_+ = \mu,\qquad -a_i d_- + c_i d_+ = \lambda.
$$

（注意到由泰勒展开 $d_\pm \approx h_\pm \pm \tfrac12 h_\pm^2$，两式相减除以 $\tfrac12$ 自动蕴含了对数二阶矩 $a_i h_-^2 + c_i h_+^2 \approx 2(\lambda-\mu)=\nu$，即自动匹配了扩散方差！）令 $\eta_-=d_-/h_-$、$\eta_+=d_+/h_+$，解上述二元一次方程组并对负值截断，取：

$$
a_i=\max\!\left(\frac{\lambda-\mu\eta_+}{h_-(\eta_+-\eta_-)},\ -\frac{\lambda}{d_-},\ 0\right),
\qquad
c_i=\max\!\left(\frac{\lambda+a_i d_-}{d_+},\ 0\right).
$$

为什么要加 $\max(\cdot, 0)$ 非负保护？当波动率 $\sigma$ 极小而利率与股息差 $|\lambda|$ 很大（即“漂移占优”或周末闭市 $\nu=0$）时，无约束二元方程组解出的某一侧系数会变成负数——负的转移权重违背概率非负性，在线性方程组中会破坏对角占优并诱发非物理锯齿振荡。上式中的 $\max$ 约束会自动把背风侧的负权重归零，保留现货期望关系 $-a_i d_- + c_i d_+ = \lambda$ 并蜕化为顺着漂移方向的**迎风单侧差分**。当步长极细导致分母 $\eta_+-\eta_-\le 8\varepsilon$ 或极端网格使 $d_+$ 溢出时，则平滑回退到附加人工方差下限 $\tilde\nu=\max(\nu,\mu h_+,-\mu h_-)$ 的非均匀中心差分：

$$
a_i=\frac{\tilde\nu-\mu h_+}{h_-(h_-+h_+)},\qquad
c_i=\frac{\tilde\nu+\mu h_-}{h_+(h_-+h_+)} .
$$

两种分支都严格保证非对角权重 $a_i\ge 0,\ c_i\ge 0$（浮点舍入精度内），主对角系数为 $b_i=-a_i-c_i-r$。均匀对数网格在所有内部节点复用同一组步长几何量，局部波动率则按各节点对应的真实绝对价格 $S_i$ 取值。

### 6.4 时间离散、近估值段加密与观察日后 Rannacher 阻尼重启

<TimeMarchingDiagram />

如图 7a 所示，时间轴的构造与推进格式围绕三个目标协同设计：让所有合约观察时刻严丝合缝落在时间节点上、尽可能复用线性方程组的消元结果、彻底消除跳跃初值引起的高频振荡。

**(1) 事件精确插点时间网格（`TimeGrid::with_events`）**：
- 在逆推总跨度 $[0,\tau_T]$ 上先铺设 $M$（`time_step_count`，默认 400）个均匀基准时间点。
- 并入全部未来敲出观察、凤凰派息观察、需要分层或显式推进时的每日敲入监测点、无风险利率与股息曲线内部节点、局部波动率曲面时间切片，以及交易日方差时钟的开闭市切换点。
- **近邻吸收防碎步**：若某个均匀基准点与任意精确事件点的距离不超过 $4\varepsilon\tau_T$，直接丢弃该均匀点而保留精确事件点，避免产生接近机器精度的病态极小时间步。
- **均匀步宽精确保持**：未被内部事件打断的相邻均匀基准点之间，步宽直接赋为同一个双精度常量 $\Delta t=\tau_T/M$（而非用 `end - start` 现场相减），保证浮点数的二进制位完全一致，以便直接命中后文的矩阵分解缓存。

**(2) 近估值首段自适应加密**：
记 $\tau_{\text{near}}$ 为距回溯起点最近的第一个事件或模型节点。若首段 $[0, \tau_{\text{near}}]$ 内的现有时间步数少于 `near_steps`（单层模式为 **128 步**，双层模式为 **64 步**），求解器将该段整体替换为 `near_steps` 个等距细步，保留 $\tau_{\text{near}}$ 右侧网格不变。因为逆推的最后一段直接决定最终输出的价格和二阶导数（Gamma），当估值时刻离下一个观察日非常近（例如只剩一两天甚至几小时，$\tau_{\text{near}}\ll \tau_T/M$）时，这一局部加密能以很小的总计算代价大幅提升近门槛估值精度。

**(3) 用线性代数特征值理解 Crank–Nicolson 伪振荡与 <MathTerm id="rannacher-damping">Rannacher 阻尼重启</MathTerm>**：
引擎提供四种时间格式（`scheme`）：显式 Euler（$\theta=0$）、隐式 Euler（$\theta=1$）、标准 Crank–Nicolson（$\theta=\tfrac12$）以及默认的 **Rannacher 格式**。为什么金融工程里看似具备二阶时间精度的标准 Crank–Nicolson（CN）在观察日附近会让二阶导数彻底算崩，而必须改用带事件重启的 Rannacher 格式？我们可以用线性代数中的**特征值与特征向量展开**把机理看个通透（见图 7b–c）：

把空间离散矩阵 $\mathcal A$ 的特征值记为 $-\lambda_k < 0$，把网格上的函数按对应的特征向量 $v_k$ 展开。空间变化平缓的光滑分量对应很小的 $\lambda_k$；而在网格相邻节点间上下剧烈跳动的**高频锯齿分量**（高波数 $k$），对应的特征值绝对值极大（$\lambda_k \propto h^{-2}$）。观察 4.5 节的时间推进方程：每逆推一个时间步 $\Delta t$，第 $k$ 个特征向量分量的系数就会乘以一个标量**模态放大因子**（令无量纲刚度 $z=\lambda_k\Delta t > 0$）：

$$
R_\theta(z)=\frac{1-(1-\theta)z}{1+\theta z}.
$$

现在对比不同 $\theta$ 在极高频锯齿分量（$z\to\infty$）上的表现：
- 在标准 Crank–Nicolson（$\theta=\tfrac12$）下，虽然对一切 $z>0$ 都有 $|R_{1/2}(z)|=\big|\frac{1-z/2}{1+z/2}\big|<1$（误差不会发散，称为 **A-稳定**），但当 $z\to\infty$ 时极限却是 $\lim_{z\to\infty} R_{1/2}(z) = -1$（**非 L-稳定**）！正如第 5 节所示，雪球与凤凰在到期日以及每一个敲出、派息和每日敲入事件点，都会向网格注入垂直阶跃或折角；就像傅里叶级数展开阶梯函数必然包含大量高频正弦波一样，每次阶跃都会激发出大量 $z\gg 1$ 的高频模态。在无阻尼 CN 下，这些锯齿分量每走一步乘上约 $-1$——幅值几乎不衰减，只是每步正负交替翻转 $(-1)^m$。对价格本身，锯齿振幅也许只有 $10^{-3}$ 量级；但一旦对空间求两次导数计算 $\Gamma = \partial_{SS}V$，每次求导都会给波数为 $k$ 的高频锯齿再乘一次 $k$，二阶导把锯齿误差剧烈放大 $k^2$ 倍，直接导致观察日前两天的敲出线 Gamma 畸变为 $+1321.9$（凤凰，第 8.7 节）与 $+2344.4$（雪球，第 9.7 节），不仅正负号颠倒，数值更暴涨了六个数量级！
- 反观隐式 Euler（$\theta=1$），其放大因子为 $R_1(z)=\frac{1}{1+z}$，当 $z\to\infty$ 时迅速趋于 $0$（称为 **L-稳定**），能强力压灭高频毛刺，但全程使用隐式 Euler 只有一阶时间精度 $O(\Delta t)$。

Kiyosi 的 `TimeGrid::substeps` 采用**事件驱动的 Rannacher 半步阻尼重启**，将两者的优点结合起来：

- 初始化阻尼计数器 `damping = 2`（对应到期日 $T$ 的终值间断），并且每当逆向推进跨过一个观察或敲入事件、施加完跳跃修正后，立即把计数器**重新置为 `damping = 2`**。
- 当 `damping > 0` 时，将当前时间步宽 $\Delta t$ 对半拆成 **2 个步长为 $\Delta t/2$ 的隐式 Euler（$\theta=1$）半步**，并将 `damping` 减 1；紧跟在每次事件后的两个时间区间共执行 $2\times 2 = 4$ 个隐式半步。单个区间内一对隐式半步的组合放大因子为 $R_{\text{damp}}(z)=(1+z/2)^{-2}$，当 $z\to\infty$ 时按 $O(z^{-2})$ 急速衰减（四个半步累积按 $O(z^{-4})$ 归零），像低通滤波器一样把刚注入的高频锯齿瞬间抹平。
- 当 `damping == 0` 后，后续已恢复光滑的区间自动切回标准 Crank–Nicolson（$\theta=\tfrac12$）单步推进。由于每次事件只改写固定常数个（2 个）时间步，当加密网格令 $\Delta t\to 0$ 时，整体时间截断误差依然保持二阶收敛 $O(\Delta t^2)$。

### 6.5 线性代数求解与三对角分解缓存

每个隐式或半隐式时间子步，归结为求解一个 $(N-1)\times(N-1)$ 的 <MathTerm id="tridiagonal-thomas">三对角线性方程组，采用 Thomas 追赶法</MathTerm>（即针对三对角稀疏矩阵定制的无主元高斯消元 / $LU$ 分解）。因为每行至多三个非零元，消元与回代各扫一遍一维数组即可完成，单步时间与空间复杂度均为严格的 $O(N)$：

- **BSM 分解缓存（`Stepper`）**：在常数波动率 BSM 模型下，空间网格固定后，左端三对角系数矩阵完全由五元组 $(\Delta t,\ \theta,\ r_m,\ q_m,\ \sigma\sqrt{a_m})$ 唯一决定。`Stepper` 内部维护一个容量为 **3 槽**的循环分解缓存（`FACTOR_CACHE_LEN = 3`），保存消元阶段算好的乘子 `multipliers`、上对角元 `upper` 以及消元后主对角元的倒数 `inverse`（把内层回代循环里耗时的浮点除法预先转成乘法）。为什么恰好设 3 个槽位？因为在同一段常数利率区间内，1 号槽存“均匀 CN 整步 $(\Delta t, \tfrac12)$”，2 号槽存“Rannacher 隐式半步 $(\Delta t/2, 1)$”，3 号槽应付事件插点切割出的非均匀过渡步，使绝大多数时间子步（以及同一子步内的 `alive` 与 `knocked` 两层）完全省去矩阵分解，只做一次轻量级的向量前代与回代扫描。
- **局部波动率逐步分解（`advance_local`）**：在局部波动率模型下，由于 $\sigma(t_m, S_i)$ 随时间中点和空间位置同时变化，每个时间子步动态更新三对角系数并原地完成消元分解，未敲入与已敲入两层共享同一算子推进。

### 6.6 样条提取、Greeks 可用性判定与可复用解 `FiniteDifferenceSolution`

逆推抵达终点后，我们拿到了离散网格节点上的函数值向量；但在实际定价与风险管理中，不仅需要查询任意现货 $S_0$（未必恰好落在网格点上）的价格，还需要计算价格对各个市场输入参数的偏导数——金融上统称为 <MathTerm id="greeks">Greeks（希腊字母风险敏感度）</MathTerm>，其中最核心的现货敏感度是一阶偏导 $\Delta = \partial V/\partial S$、二阶偏导 $\Gamma = \partial^2 V/\partial S^2$ 与三阶偏导 $\mathrm{Speed} = \partial^3 V/\partial S^3$。

**(1) <MathTerm id="cubic-spline-bezier">带 Bézier 过冲保护的对数现货三次样条</MathTerm>（`SpatialGrid::spline` / `sample`）**。
回溯结束后，引擎在对数网格上构造分段三次样条插值函数 $W(x)$。若网格某端相邻两步的长度比在 $[0.25,4]$ 之间，使用同一三次多项式衔接这两个区间（非扭结端条件）；否则将该端二阶导数设为零（自然样条端条件）。将查询现货 $S$ 映射为 $x=\ln(S/S_{\mathrm a})$ 求出样条的一阶导 $W_x = \partial_x W$ 和二阶导 $W_{xx} = \partial_{xx} W$ 后，由高等数学的复合函数求导法则（$W(x)=V(S_{\mathrm a}e^x) \implies \partial_S V = \partial_x W \cdot \frac{dx}{dS} = \frac{W_x}{S}$，再对 $S$ 用商的求导法则求导一次）直接换算现货一阶与二阶偏导数：

$$
\Delta=\frac{W_x}{S},\qquad
\Gamma=\frac{W_{xx}-W_x}{S^2}.
$$

若局部节点在现货坐标上已高度接近同一直线，直接按该直线采样以避免浮点微扰弯曲；其余单元将三次多项式转换为四控制点 Bézier 形式，利用凸包性质检测样条是否在拐点旁产生局部“过冲”，视网格与包络检查结果做钳制或回退到线性插值。若对称微扰点 $S\pm h$ 严格位于网格内部，三阶偏导 `Speed` 取两点现货 Gamma 的中心差商。

**(2) 跨越当期不连续点的 Greeks 屏蔽（`at_spot_discontinuity`）**：
当估值时刻 $t_{\text{val}}$（或零方差前缀内的确定性观察时刻）恰好存在观察事件，且现货对称微扰区间 $[S_0-h, S_0+h]$ 跨越了生效的敲出线 $B^{\text{out}}$、非零凤凰派息线 $B^c$ 或影响支付的敲入线 $B^{\text{in}}$ 时，真实价值函数在该点发生垂直阶跃，高等数学意义下的导数不存在（广义函数意义下含 <MathTerm id="dirac-delta">Dirac δ 奇异项</MathTerm>）。引擎通过精确远期比较主动检测此类跨界情形：保留精确标量价格，同时将不可微的现货 Greeks 诚实地标记为不可用（Python 中返回 `None`），绝不输出横跨断层算出的虚假差商。BSM 模型的跨参数偏导数 Vega（$\partial V/\partial\sigma$）、Rho（$\partial V/\partial r$）与 Theta（$\partial V/\partial t$）通过核心数值微扰重定价计算，且在微扰重算时固定锁定中心定价所用的上边界 $S_{\max}$，消除计算域随波动率或利率微移引起的网格抖动噪声。局部波动率模型支持固定绝对曲面下的原生 Delta 与 Gamma。

**(3) 固定估值时刻的多现货可复用解（`engine.solve`）**：
有限差分的一大结构优势是：一次从 $T$ 到 $t_{\text{start}}$ 的网格逆推，天然同时算出了整个价格区间 $[S_{\min}, S_{\max}]$ 上的价值函数曲线！在绘制现货损益与 Greeks 曲线或执行现货压力测试时，合约条款、市场模型、历史状态与估值时刻均固定，仅查询现货 $S_0$ 在闭区间 $[S_{\text{low}}, S_{\text{high}}]$ 内变化。调用 `engine.solve(note, context, spot_range=(low, high))` 时：
- 引擎将查询区间两端沿确定性前缀推进至回溯起点，用上端确定自动上界的尺度，用下端计算正下界，确保单张网格完整覆盖全部查询现货。
- 若存在当期或零方差前缀内的敲入监测，查询区间低端可能已当期敲入而高端尚未敲入；`solve` 利用正双精度浮点数 IEEE-754 整数位模式单调保序的性质，在 $[S_{\text{low}}, S_{\text{high}}]$ 上执行最多 64 步二分查找，准确判断区间内是否存在任何需要未敲入层 $V^{(0)}$ 的查询点，从而决定单次 `solve_grid` 是否保留双层样条。
- 返回的 `FiniteDifferenceSolution` 内部以只读引用计数持有双层（或单层）样条，后续调用 `price_many` 或 `price_many_with_greeks` 时完全无需重解 PDE，仅对每个查询现货执行微秒级的确定性当期事件判定与样条求值（完整示例见附录 B.3）。参见[有限差分解](https://github.com/lilkui/kiyosi/blob/d8413d14ab2f7a53ecc3df145d394bd3c5ba783e/crates/kiyosi/src/engines/finite_difference/solution.rs)。

### 6.7 各项数值设计解决的核心问题汇总

| 数值方法 | 解决的核心数值或金融问题 | 本报告实测证据 |
|---|---|---|
| 双层状态 PDE 与自动单层退化 | 精确刻画每日敲入的不可逆状态传递，同时避免到期敲入与二元雪球的冗余开销 | 第 7.4 节基准中，每日敲入使凤凰和雪球价格分别比到期敲入低约 $0.00863$ 和 $0.01455$ |
| 合约水平对齐与分段 `sinh` 加密 | 使保留障碍精确落在网格节点上，并将节点集中于间断与高曲率邻域 | 到期敲入基准在同步加密的前三级误差约按二阶下降。相近水平的误差随网格配置变化（第 8.2、8.8、9.2、9.8 节） |
| 对数漂移与现货矩匹配 | 控制漂移占优时的非对角权重，并保留通常分支的现货矩 | 波动率 $10\%$ 的扫描场景在 1600×3200 网格上绝对误差低于 $3\times10^{-7}$（第 8.5、9.5 节） |
| 事件后 Rannacher 半步阻尼重启 | 滤除每次敲出、派息、敲入阶跃重新激发的高波数模态，防止二阶导数爆炸 | 距观察日两天、现货在敲出线时，Gamma 与参考相差低于 $10^{-6}$，而无阻尼 CN 失真至 $+10^3$ 量级（第 8.7、9.7 节） |
| 事件精确插点与近估值首段加密 | 杜绝观察时刻的时间舍入漂移，精细解析紧邻估值点的短期扩散过渡层 | 每日敲入基准在时间步加密后恢复清晰的二阶时间收敛率（第 8.2、9.2 节） |
| 控制体积增量跳跃修正投影 | 消除亚网格障碍引发的 $O(h)$ 锯齿误差，且不在高频每日监测中耗散光滑延续值 | 固定时间步数时，两组基准的到期敲入误差随空间加密下降（第 8.2、9.2 节） |
| 仿射 Dirichlet 边界与事件重置 | 分别贴现现金与现货敞口，并在事件时刻取端点支付点值 | 上边界取 250、400、1000 时，四组基准价格最大变动小于 $8\times10^{-9}$（第 8.3、9.3 节） |
| 带过冲保护的三次样条与间断检测 | 在非节点现货处稳定提取光滑价格与原生 Delta、Gamma，屏蔽跨跳变伪导数 | 多现货水平下的 Delta 与 Gamma 相对独立中心差分高度吻合（第 8.6、9.6 节及附录 B.3） |

---

## 7. 验证方法论与独立参考解

为排除同源实现可能带来的系统性盲区，以下三套外部参考解均脱离 Kiyosi 独立编写，基于同一组数值条款交叉核对有限差分结果。基准测试采用 Act/365F 方差时间、固定利率与股息、零返还；第 10 节和附录 B.3 补充检验独立观察日程、返还与交易日方差时钟。

### 7.1 参考 A：QuantLib 静态复制（解析）

按第 3.6 节导出的代数恒等式，直接调用开源量化库 QuantLib 1.44 的 `BlackCalculator` 计算零息本金（及雪球到期票息）贴现、现金或无（Cash-or-Nothing）数字看涨／看跌期权以及欧式普通看跌期权的线性组合。这套参考解完全由正态分布累积函数构成，不含任何网格或时间离散误差（仅含机器浮点舍入误差），适用于“仅在到期允许敲出且到期敲入”的凤凰，以及单观察日、到期敲入的雪球、三元雪球和二元雪球。

### 7.2 参考 B：障碍对齐的转移密度卷积（半解析）

当存续期内包含多次观察或每日敲入时，已不存在初等闭式解；但在常系数 BSM 模型下，任意两个相邻事件之间间隔 $\Delta t$ 时，对数价格增量 $x_{t+\Delta t}-x_t$ 严格服从正态分布 $\mathcal N(\nu\Delta t,\,\sigma^2\Delta t)$（其中 $\nu=r-q-\tfrac{\sigma^2}{2}$），无需做小时间步偏微分方程近似！

据此在 $x=\ln(S/70)$ 坐标上构造等宽小单元，单元宽度取 $h=H_0/m$，其中基准格距 $H_0=\ln(100/70)/20$。所有由该方法检验的场景均将正的门槛和行权价选在整数倍格点 $70\,e^{kH_0}$（$k\in\mathbb Z$）上，使所有跳跃间断点和斜率拐点恰好落在单元分界线上。由概率论正态分布积分，从单元中心 $x_i$ 出发经过 $\Delta t$ 落入第 $j$ 个单元 $[x_j-h/2, x_j+h/2]$ 的精确转移概率等于标准正态分布函数 $\Phi(\cdot)$ 在两端点之差，一步逆向期望递推即写成离散 <MathTerm id="gaussian-convolution-fft">高斯转移密度卷积</MathTerm>：

$$
V_i(t)=e^{-r\Delta t}\sum_j\Big[\Phi\Big(\tfrac{x_j+h/2-x_i-\nu\Delta t}{\sigma\sqrt{\Delta t}}\Big)-\Phi\Big(\tfrac{x_j-h/2-x_i-\nu\Delta t}{\sigma\sqrt{\Delta t}}\Big)\Big]V_j(t+\Delta t),\qquad \nu=r-q-\tfrac{\sigma^2}{2}.
$$

实现中，窄卷积核采用直接求和，宽卷积核利用快速傅里叶变换（FFT）加速；核半宽覆盖约 12 个标准差，计算域以初始现货为中心向两侧各扩展 10 个标准差并留出漂移余量，合约支付和事件更新由纯 Python 独立编写。由于单元中心中点求积对光滑正态密度具有 $O(h^2)$ 二阶精度，每将细分倍数 $m$ 翻倍（即单元宽度 $h$ 减半），误差应缩小为原来的 $\tfrac14$。下表中相邻两级差值之比高度贴近 $4$，印证了严格的二阶空间收敛：

| $m$ | 凤凰，到期敲入 | 凤凰，每日敲入 | 雪球，到期敲入 | 雪球，每日敲入 |
|---|---|---|---|---|
| 5 | 1.0009196819 | 0.9921525814 | 1.0132142484 | 0.9984899542 |
| 10 | 1.0009237023 | 0.9922559951 | 1.0132184291 | 0.9986236166 |
| 20 | 1.0009247074 | 0.9922818899 | 1.0132194742 | 0.9986570970 |
| 40 | 1.0009249586 | 0.9922883661 | 1.0132197355 | 0.9986654712 |
| 相邻差值之比 | 4.000, 4.000 | 3.994, 3.998 | 4.000, 4.000 | 3.992, 3.998 |

最终高精度参考值取 $m=40,80,160$（每日敲入取 $80,160,320$），对最细两级做 <MathTerm id="richardson-extrapolation">Richardson 外推</MathTerm>（利用 $V_{\text{ext}} = V(2m) + \frac{V(2m)-V(m)}{3}$ 消去 $O(h^2)$ 主误差项）。附录脚本以相邻两次外推之差及最后一次外推修正量中的较大者保守估计参考解自身残余误差。

### 7.3 参考 C：事件日精确抽样的 Monte Carlo

根据概率论中的大数定律，大量独立随机模拟路径的贴现收益算术平均值依概率收敛于真实数学期望。在常数波动率 BSM 下，由于离散监测只关心事件时刻的价格，模拟程序直接按精确对数正态增量 $\ln S_{t+\Delta}=\ln S_t+\nu\Delta+\sigma\sqrt\Delta Z$（$Z\sim\mathcal N(0,1)$）在相邻事件日之间一步跳转抽样，并配合 <MathTerm id="antithetic-variates">对偶变量</MathTerm> $(Z, -Z)$ 成对抵消一阶抽样波动。这种抽样在 BSM 下**完全没有时间步离散偏差**，只含样本有限带来的统计抽样误差（由样本标准误 $\mathrm{SE}$ 度量）。局部波动率场景无法一步精确抽样，改用对数 Euler 格式推进，强制最大子步不超过 $1/4$ 天；表中所列标准误仅度量随机抽样误差。

### 7.4 基准合约

除非另有说明，凤凰和雪球各使用一份“标准一年期月度”合约，两者共用日期、价格门槛和市场参数：

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

三元雪球和二元雪球基准与雪球基准相同，仅分别改为敲入后支付最低年化票息 $c_{\min}=3\%$，以及去掉敲入条款。

由卷积加密得到的 Richardson 外推参考价格如下（四舍五入至小数点后九位）：

| 合约 | 到期敲入 | 每日敲入 |
|---|---|---|
| 凤凰 | 1.000925042 | 0.992290525 |
| 雪球 | 1.013219823 | 0.998668263 |
| 三元雪球 | 1.033151508 | 1.028417875 |
| 二元雪球 | 1.038992508（无敲入） | — |

---

## 8. 验证结果：凤凰

### 8.1 理论检验：静态复制解析基准

比较单期与 12 期凤凰。两种合约均设为仅在到期允许敲出且仅在到期观察敲入，分别测试三组参数 $(c,L)=(0.8\%,0)、(-2\%,50)、(5\%,60)$，遍历波动率 15%、30%、50% 与初始现货 55、70、75、90、100、120、150（每类 $3\times 3\times 7 = 63$ 个算例）。参考价格由第 3.6 节的静态复制组合经 QuantLib 算出，表中报告绝对误差 $|V_{\text{FD}}-V_{\text{QL}}|$。

| 合约 | 例数 | 默认网格最大误差 | 默认网格平均误差 | 3200×3200 最大误差 |
| --- | --- | --- | --- | --- |
| 单期凤凰 | 63 | 1.45e-05 | 3.51e-06 | 1.00e-06 |
| 12 期凤凰 | 63 | 6.76e-05 | 7.01e-06 | 3.19e-06 |

### 8.2 空间与时间收敛性

下表列出空间步数 $N$ 与时间步数 $M$（记为 $N\times M$）同步加密时，有限差分价格相对第 7.4 节卷积外推参考值的有符号误差（`FD - 参考值`）。

| 网格 | 到期敲入误差 | 每日敲入误差 |
| --- | --- | --- |
| 400×200 | 2.05e-06 | 1.11e-04 |
| 800×400 | 4.86e-07 | 6.26e-05 |
| 1600×800 | 1.29e-07 | 2.37e-05 |
| 1600×1600 | -8.51e-09 | 5.60e-06 |
| 3200×3200 | -2.14e-09 | 1.38e-06 |
| 6400×3200 | 7.89e-09 | 1.38e-06 |

固定时间步数 $M=3200$、单独增加空间步数 $N$ 的结果如下。其中每日敲入列以 6400×3200 网格的价格作对照基准，以便剥离共同的时间离散残差、单独观察空间收敛。

| 空间步数 | 到期敲入误差 | 每日敲入空间差异 |
| --- | --- | --- |
| 200 | -3.24e-06 | -1.81e-06 |
| 400 | -8.93e-07 | -1.46e-07 |
| 800 | -2.13e-07 | -3.87e-08 |
| 1600 | -4.29e-08 | -1.63e-08 |
| 3200 | -2.14e-09 | -2.12e-09 |

再固定空间步数 $N=3200$，对比三种时间推进格式随时间步数 $M$ 增加的表现（每个单元格依次列出“到期敲入误差 / 每日敲入误差”）。

| 时间步数 | Rannacher | Crank–Nicolson | 隐式 Euler |
| --- | --- | --- | --- |
| 200 | 2.94e-06 / 1.11e-04 | 9.58e-04 / -9.43e-04 | 8.11e-05 / 2.25e-04 |
| 400 | 6.98e-07 / 6.26e-05 | -6.25e-04 / 3.17e-04 | 4.15e-05 / 1.55e-04 |
| 800 | 1.70e-07 / 2.38e-05 | 4.62e-04 / 3.09e-03 | 2.15e-05 / 9.12e-05 |
| 1600 | 3.22e-08 / 5.61e-06 | 1.19e-03 / -1.05e-03 | 1.12e-05 / 4.93e-05 |
| 3200 | -2.14e-09 / 1.38e-06 | -1.63e-03 / 1.90e-05 | 5.62e-06 / 2.56e-05 |

可以看到：到期敲入时，Rannacher 每把时间步数翻倍，误差就缩小约 4 倍（二阶收敛 $O(\Delta t^2)$），而隐式 Euler 仅缩小为一半（一阶收敛 $O(\Delta t)$）。每日敲入因存续期内有约 261 个未来监测日，当总时间步数 $M$ 较小时（如 $M=200,400$），大部分时间区间都处于事件后的隐式半步阻尼状态，因而初期收敛略缓；一旦时间步数增至 1600 并翻倍到 3200，平滑 CN 步占比恢复主导，Rannacher 的每日敲入误差即从 $5.61\times10^{-6}$ 降至 $1.38\times10^{-6}$（精确缩小为四分之一，恢复二阶收敛）。相比之下，无阻尼 CN 因高频锯齿分量正负翻转，误差停留在 $10^{-3}$ 量级且随加密上下震荡。

### 8.3 计算域敏感性

固定 1600×1600 网格，测试人为改变上边界 $S_{\max}$（自动上边界为 400）对结果的影响：

| 上边界 | 到期敲入价格 | 每日敲入价格 |
| --- | --- | --- |
| 250 | 1.0009250341 | 0.9922961291 |
| 400 | 1.0009250339 | 0.9922961229 |
| 1000 | 1.0009250319 | 0.9922961222 |

跨度从 250 拉大至 1000，两种敲入方式的最大价格变动仅为 $6.87\times10^{-9}$，说明自动边界留出的远场缓冲已足够充分。

### 8.4 多方法交叉验证

独立 Monte Carlo 使用 400 万条对偶路径，表内 `±` 后为一个统计标准误。求积（`QuadratureAutocallableEngine`）与有限差分（FD）均使用 Kiyosi 0.22.0。

| 方法 | 到期敲入价格 | 每日敲入价格 |
| --- | --- | --- |
| 卷积外推 | 1.000925042 | 0.992290525 |
| 独立 Monte Carlo | 1.000860418 ± 4.09e-05 | 0.992310796 ± 4.34e-05 |
| FD 800×400 | 1.000925529 | 0.992353113 |
| FD 1600×1600 | 1.000925034 | 0.992296123 |
| FD 3200×3200 | 1.000925040 | 0.992291905 |
| 求积（默认） | 1.000925010 | 0.992286727 |

### 8.5 参数扫描

改变市场波动率、负利率、近敲入线现货及典型条款变体，每个单元格依次列出“到期敲入 / 每日敲入”相对卷积参考的有符号误差。逐期降敲的水平取 `70 * exp(k * H0)`，$k$ 从 20 逐期递减到 9。

| 场景 | 800×400 | 1600×3200 |
| --- | --- | --- |
| 波动率 10% | -2.33e-07 / 8.93e-07 | -1.40e-07 / -1.46e-07 |
| 波动率 60% | 5.30e-06 / 3.92e-05 | 1.21e-06 / 2.43e-06 |
| $r=-1\%,q=0$ | 3.82e-07 / 7.21e-05 | -1.17e-07 / 1.55e-06 |
| 现货 72 | 8.56e-07 / 1.11e-04 | 7.07e-08 / 2.10e-06 |
| 逐期降敲 | 6.82e-07 / 3.89e-05 | -5.17e-08 / 1.74e-06 |
| 每期票息 −1% | 1.55e-06 / 6.00e-05 | 4.78e-07 / 1.79e-06 |
| 锁定前三期敲出 | 2.98e-07 / 8.85e-05 | -9.17e-08 / 1.86e-06 |
| 无条件票息 | 6.26e-07 / 6.21e-05 | -6.58e-10 / 1.39e-06 |

### 8.6 Greeks 验证

比较 800×1600 网格输出的偏导数 <MathTerm id="greeks">Delta、Gamma 与 Vega</MathTerm>。独立参考值通过对高精度卷积外推价格做中心差商获得（现货微扰步长 $0.05$，波动率微扰步长 $0.001$）。每格依次给出“FD 值 / 参考值”。

| 敲入 | 现货 | Delta | Gamma | Vega |
| --- | --- | --- | --- | --- |
| 到期 | 72 | 0.013153 / 0.0131529 | -0.000481814 / -0.000481832 | -0.485648 / -0.485613 |
| 到期 | 80 | 0.00865516 / 0.00865518 | -0.000559131 / -0.000559098 | -0.656184 / -0.656148 |
| 到期 | 90 | 0.0038793 / 0.00387938 | -0.000391666 / -0.000391689 | -0.546164 / -0.546158 |
| 到期 | 100 | 0.000987177 / 0.000987093 | -0.000178182 / -0.000178182 | -0.239416 / -0.239426 |
| 到期 | 110 | 9.3941e-05 / 9.39753e-05 | -2.7577e-05 / -2.75688e-05 | -0.0408191 / -0.0408397 |
| 每日 | 72 | 0.0149091 / 0.0149066 | -0.000335013 / -0.000333958 | -0.271262 / -0.27117 |
| 每日 | 80 | 0.0109736 / 0.0109734 | -0.000556175 / -0.00055608 | -0.618141 / -0.618061 |
| 每日 | 90 | 0.0059051 / 0.00590577 | -0.000441906 / -0.000441895 | -0.612205 / -0.612177 |
| 每日 | 100 | 0.00222508 / 0.0022256 | -0.000284718 / -0.000284736 | -0.302441 / -0.302483 |
| 每日 | 110 | 0.000402469 / 0.000402802 | -8.74527e-05 / -8.74797e-05 | -0.0645404 / -0.0645838 |

### 8.7 临近观察日的数值稳定性

将估值时刻推进到 2025-06-30（距离下一次敲出观察日 2025-07-02 仅剩两天），在每日敲入与默认 800×400 网格下，对比敲出线正上方 $S_0=100$ 及靠近敲入线的 $S_0=72$ 处的价格与二阶导数 Gamma（参考 Gamma 中心差商步长取 $0.02$）：

| 计算方法 | 价格（现货 100） | Gamma（现货 100） | 价格（现货 72） | Gamma（现货 72） |
| --- | --- | --- | --- | --- |
| 卷积外推 | 1.00904195 | -0.00026692462 | 0.77085590 | -0.0015915183 |
| Rannacher | 1.00905383 | -0.00026712346 | 0.77097618 | -0.0016118689 |
| Crank–Nicolson | 1.00705019 | 1321.8516 | 0.77068833 | -0.0016133527 |
| 隐式 Euler | 1.00908408 | -0.00026811167 | 0.77128680 | -0.0016214348 |

这组数据直观印证了第 6.4 节的特征值放大分析：无阻尼 Crank–Nicolson 在敲出线阶跃附近残留高频锯齿，求二阶导数后 Gamma 失真至 $+1321.85$；而 Rannacher 阻尼重启将该点的 Gamma 稳稳恢复至参考值 $-0.000267$ 附近。此外，当现货恰好等于 $70$ 且处于当期每日敲入观察时刻时，因为微小扰动会直接跨过敲入跳跃点，Rannacher 按设计将不可微的 Gamma 返回为 `None`。

### 8.8 相近合约水平的网格误差

保持参考价和上行权价为 $100$，同时将各期敲出水平微调至 $100$ 附近（相距仅 $0.1\%\sim 0.5\%$）。下表列出到期敲入 FD 价格与 2048 步高斯求积结果的绝对差值：

| 敲出水平 | 800×400 | 800×1600 | 1600×400 | 3200×1600 |
| --- | --- | --- | --- | --- |
| 99.5 | 4.62e-07 | 1.70e-07 | 6.28e-07 | 3.01e-08 |
| 99.9 | 5.12e-07 | 1.47e-07 | 1.34e-06 | 1.71e-07 |
| 100.1 | 5.19e-07 | 1.53e-07 | 1.32e-06 | 2.09e-07 |
| 100.5 | 3.67e-07 | 3.32e-07 | 7.09e-07 | 3.07e-08 |

当两个关键价格水平靠得非常近时，改变空间步数 $N$ 会改变筛选阈值与两水平周围的局部格距分布，因此表中的微小误差随网格配置呈非单调起伏，整体保持在 $10^{-6}$ 及更低量级。

### 8.9 局部波动率

先将局部波动率曲面设为常数 $25\%$，两种敲入方式的 FD 价格均与 BSM 结果逐位一致。再构造随价格下跌波动率抬升的偏斜曲面：现货节点取 50、70、100、130、160，生效时波动率为 40%、32%、25%、21%、19%，到期时为 36%、30%、24%、21%、20%。独立对数 Euler Monte Carlo 使用 100 万条对偶路径，最大时间步长 $1/4$ 天（最后一列 `SE` 表示相差几个抽样标准误）：

| 敲入 | 400² | 800² | 1600² | 3200² | 独立 MC ± 标准误 | FD − MC |
| --- | --- | --- | --- | --- | --- | --- |
| 到期 | 0.9959754 | 0.9959743 | 0.9959740 | 0.9959739 | 0.9959356 ± 9.31e-05 | +0.41 SE |
| 每日 | 0.9870459 | 0.9870068 | 0.9869890 | 0.9869848 | 0.9868897 ± 9.67e-05 | +0.98 SE |

FD 自身随网格从 $400^2$ 加密至 $3200^2$ 稳定收敛，与独立 MC 的差值落在 $1$ 个抽样标准误以内（该对比的精度上限主要由 MC 的抽样噪声与 Euler 离散误差决定）。

---

## 9. 验证结果：雪球

### 9.1 理论检验：静态复制解析基准

雪球各变体均设为仅在到期允许敲出，含敲入障碍的合约仅在到期观察敲入，敲出年化票息取 15%。遍历波动率 15%、30%、50% 与现货 55、70、75、90、100、120、150（每类 $3\times 7 = 21$ 个算例），与第 3.6 节 QuantLib 静态复制解析解对比绝对误差：

| 合约 | 例数 | 默认网格最大误差 | 默认网格平均误差 | 3200×3200 最大误差 |
| --- | --- | --- | --- | --- |
| 标准雪球，$c_m=15\%$，$L=0$ | 21 | 8.93e-06 | 2.90e-06 | 5.52e-07 |
| 双票息，$c_m=5\%$ | 21 | 1.01e-05 | 3.34e-06 | 6.29e-07 |
| 限亏，$L=60$ | 21 | 1.78e-05 | 5.42e-06 | 1.23e-06 |
| 三元雪球，$c_m=10\%$，$c_{\min}=2\%$ | 21 | 2.44e-06 | 1.06e-06 | 1.51e-07 |
| 二元雪球，$c_m=3\%$ | 21 | 1.72e-06 | 5.66e-07 | 1.06e-07 |

### 9.2 空间与时间收敛性

同步加密时相对第 7.4 节卷积外推参考值的有符号价格误差如下：

| 网格 | 到期敲入误差 | 每日敲入误差 |
| --- | --- | --- |
| 400×200 | 3.31e-06 | 1.83e-04 |
| 800×400 | 7.67e-07 | 1.04e-04 |
| 1600×800 | 1.88e-07 | 3.94e-05 |
| 1600×1600 | -1.18e-08 | 9.33e-06 |
| 3200×3200 | -5.20e-09 | 2.30e-06 |
| 6400×3200 | 1.01e-08 | 2.29e-06 |

固定 $M=3200$ 单独加密空间步数 $N$ 的结果如下（每日敲入列同样以 6400×3200 的价格为基准以剥离共同的时间误差）：

| 空间步数 | 到期敲入误差 | 每日敲入空间差异 |
| --- | --- | --- |
| 200 | -2.82e-06 | 2.74e-06 |
| 400 | -1.43e-06 | 4.95e-07 |
| 800 | -3.41e-07 | 1.23e-07 |
| 1600 | -6.11e-08 | 2.91e-08 |
| 3200 | -5.20e-09 | 6.15e-09 |

固定 $N=3200$ 对比三种时间推进格式（每格依次列出“到期敲入误差 / 每日敲入误差”）：

| 时间步数 | Rannacher | Crank–Nicolson | 隐式 Euler |
| --- | --- | --- | --- |
| 200 | 4.74e-06 / 1.83e-04 | 1.12e-03 / -2.60e-03 | 1.31e-04 / 3.70e-04 |
| 400 | 1.10e-06 / 1.04e-04 | 1.11e-03 / 1.89e-03 | 6.55e-05 / 2.56e-04 |
| 800 | 2.44e-07 / 3.94e-05 | 1.18e-04 / 3.61e-03 | 3.21e-05 / 1.51e-04 |
| 1600 | 4.41e-08 / 9.31e-06 | 2.69e-03 / -2.01e-03 | 1.54e-05 / 8.17e-05 |
| 3200 | -5.20e-09 / 2.30e-06 | -4.93e-03 / 4.06e-04 | 7.70e-06 / 4.24e-05 |

收敛规律与凤凰一致：到期敲入下 Rannacher 呈现标准二阶收敛，隐式 Euler 呈现一阶收敛；每日敲入下当时间步数从 1600 增至 3200 时，Rannacher 误差由 $9.31\times10^{-6}$ 降至 $2.30\times10^{-6}$（缩小为四分之一）；无阻尼 CN 则因阶跃高频振荡产生显著的非单调误差。

### 9.3 计算域敏感性

固定 1600×1600 网格（自动上边界为 400）：

| 上边界 | 到期敲入价格 | 每日敲入价格 |
| --- | --- | --- |
| 250 | 1.0132198035 | 0.9986775920 |
| 400 | 1.0132198107 | 0.9986775927 |
| 1000 | 1.0132198081 | 0.9986775939 |

两种敲入方式的最大价格变动仅为 $7.22\times10^{-9}$。

### 9.4 多方法交叉验证

独立 Monte Carlo 使用 400 万条对偶路径，表内 `±` 后为一个标准误。求积与 FD 均使用 Kiyosi 0.22.0。

| 方法 | 到期敲入价格 | 每日敲入价格 |
| --- | --- | --- |
| 卷积外推 | 1.013219823 | 0.998668263 |
| 独立 Monte Carlo | 1.013143688 ± 5.11e-05 | 0.998704648 ± 5.58e-05 |
| FD 800×400 | 1.013220589 | 0.998772565 |
| FD 1600×1600 | 1.013219811 | 0.998677593 |
| FD 3200×3200 | 1.013219817 | 0.998670563 |
| 求积（默认） | 1.013219768 | 0.998661687 |

三元雪球与二元雪球基准的 FD 有符号误差如下：

| 合约 | 卷积参考价格 | 800×400 | 1600×1600 | 3200×3200 |
| --- | --- | --- | --- | --- |
| 三元雪球，到期敲入 | 1.033151508 | -1.46e-07 | -1.80e-07 | -4.95e-08 |
| 三元雪球，每日敲入 | 1.028417875 | 3.44e-05 | 2.93e-06 | 7.24e-07 |
| 二元雪球 | 1.038992508 | 5.06e-07 | -1.33e-08 | -6.30e-09 |

正如第 5.3 节间断谱所预示的，三元雪球在敲入线处的跳变幅度（$0.12$）远小于标准雪球（$0.45$），因此其默认网格下的每日敲入误差也缩小为标准雪球的约三分之一。

### 9.5 参数扫描

每格依次给出“到期敲入 / 每日敲入”相对卷积参考的有符号误差。逐期降敲的水平取 `70 * exp(k * H0)`，$k$ 从 20 逐期递减到 9；末一行对应降落伞雪球（仅下调最后一期敲出线至约 $83.67$）。

| 场景 | 800×400 | 1600×3200 |
| --- | --- | --- |
| 波动率 10% | -3.26e-07 / 1.74e-06 | -2.28e-07 / -2.28e-07 |
| 波动率 60% | 4.94e-06 / 3.43e-05 | 1.16e-06 / 2.47e-06 |
| $r=-1\%,q=0$ | 7.95e-07 / 1.20e-04 | -1.12e-07 / 2.70e-06 |
| 现货 72 | -8.82e-07 / 1.95e-04 | -3.61e-07 / 3.77e-06 |
| 逐期降敲 | -1.79e-06 / 5.63e-05 | -8.16e-07 / 2.06e-06 |
| $r=2\%,q=8\%$ | 1.19e-06 / 1.40e-04 | -5.35e-08 / 3.36e-06 |
| 到期票息 5% | 1.59e-06 / 7.65e-05 | 2.64e-07 / 1.98e-06 |
| 末期敲出水平约 83.67 | -3.16e-07 / 8.85e-05 | -3.44e-07 / 2.02e-06 |

### 9.6 Greeks 验证

比较 800×1600 网格的 Delta、Gamma 与 Vega（参考值使用卷积外推中心差商，现货步长 $0.05$，波动率步长 $0.001$；每格依次为“FD 值 / 参考值”）：

| 敲入 | 现货 | Delta | Gamma | Vega |
| --- | --- | --- | --- | --- |
| 到期 | 72 | 0.0127674 / 0.0127675 | -0.000445881 / -0.000445894 | -0.532519 / -0.532484 |
| 到期 | 80 | 0.00870708 / 0.00870687 | -0.000542322 / -0.000542363 | -0.742098 / -0.742068 |
| 到期 | 90 | 0.00344619 / 0.00344627 | -0.000476166 / -0.000476154 | -0.65865 / -0.65863 |
| 到期 | 100 | 0.000144416 / 0.000144389 | -0.00015218 / -0.000152178 | -0.278576 / -0.278584 |
| 到期 | 110 | -0.000196521 / -0.000196501 | 2.35969e-05 / 2.3586e-05 | -0.0347379 / -0.034761 |
| 每日 | 72 | 0.0161433 / 0.0161395 | -0.000206924 / -0.000204938 | -0.18057 / -0.180403 |
| 每日 | 80 | 0.0128934 / 0.0128928 | -0.000560414 / -0.000560339 | -0.709895 / -0.709778 |
| 每日 | 90 | 0.00694829 / 0.00694939 | -0.000574445 / -0.000574365 | -0.79498 / -0.794941 |
| 每日 | 100 | 0.00223887 / 0.00224002 | -0.000334892 / -0.000334948 | -0.393831 / -0.393896 |
| 每日 | 110 | 0.000322077 / 0.000322517 | -7.72216e-05 / -7.72843e-05 | -0.0759789 / -0.0760388 |

注意表中一个很能体现雪球收益结构的现象：当到期敲入且初始现货高达 $110$（已明显高于敲出线 $100$）时，一阶导数 Delta 变为**负数**（$-0.000197$）、二阶导数 Gamma 变为正数。原因很直观：在这份年化票息高达 $15\%$（远高于无风险利率 $3\%$）的合约中，价格涨得太高会使合约大概率在第一个月观察日就早早敲出结清，反而让持有人少赚了后续十一个月的丰厚高息。

### 9.7 临近观察日的数值稳定性

估值设为 2025-06-30（距下一次敲出观察日两天），取每日敲入与默认网格，观察敲出线处 $S_0=100$ 及靠近敲入线的 $S_0=72$（参考 Gamma 中心差商步长取 $0.02$）：

| 计算方法 | 价格（现货 100） | Gamma（现货 100） | 价格（现货 72） | Gamma（现货 72） |
| --- | --- | --- | --- | --- |
| 卷积外推 | 1.07914278 | -0.00029403305 | 0.76133309 | -0.0009710343 |
| Rannacher | 1.07916140 | -0.00029338627 | 0.76154116 | -0.0010154396 |
| Crank–Nicolson | 1.07562233 | 2344.3605 | 0.76102223 | -0.00099749011 |
| 隐式 Euler | 1.07920872 | -0.00029197225 | 0.76208532 | -0.0010790829 |

无阻尼 CN 在敲出线附近的 Gamma 再次因高频振荡暴涨至 $+2344.36$，而 Rannacher 将其恢复到参考值 $-0.000294$ 附近；当现货恰好为 $70$ 且处于当期每日敲入观察时刻时，Rannacher 同样因扰动跨越敲入跳跃而返回 `None`。

### 9.8 相近合约水平的网格误差

保持参考价和上行权价为 $100$，同时微调各期敲出水平。下表为到期敲入 FD 价格与 2048 步求积的绝对差值：

| 敲出水平 | 800×400 | 800×1600 | 1600×400 | 3200×1600 |
| --- | --- | --- | --- | --- |
| 99.5 | 7.96e-07 | 2.00e-07 | 1.03e-06 | 4.05e-08 |
| 99.9 | 1.00e-06 | 4.08e-08 | 6.25e-06 | 1.04e-06 |
| 100.1 | 1.15e-06 | 7.95e-08 | 6.20e-06 | 1.35e-06 |
| 100.5 | 6.76e-07 | 4.45e-07 | 1.50e-06 | 8.14e-08 |

调整空间步数会改变相近水平之间及两侧的局部节点间距，表中的价格误差随网格配置呈非单调变化。

### 9.9 局部波动率

常数曲面设为 $25\%$ 时，两种敲入方式的 FD 价格均与 BSM 相同。使用与第 8.9 节相同的偏斜波动率曲面（现货节点 50、70、100、130、160，生效波动率 40%、32%、25%、21%、19%，到期波动率 36%、30%、24%、21%、20%）及 100 万条对偶路径、最大步长 $1/4$ 天的对数 Euler MC 对比如下：

| 敲入 | 400² | 800² | 1600² | 3200² | 独立 MC ± 标准误 | FD − MC |
| --- | --- | --- | --- | --- | --- | --- |
| 到期 | 1.0074204 | 1.0074194 | 1.0074191 | 1.0074191 | 1.0073858 ± 1.13e-04 | +0.30 SE |
| 每日 | 0.9919096 | 0.9918434 | 0.9918134 | 0.9918063 | 0.9916904 ± 1.20e-04 | +0.97 SE |

差异同样处于 1 个抽样标准误以内，对比精度上限受限于抽样误差与对数 Euler 时间离散误差。

---

## 10. 仓库测试套件

在该版本源码和 release 构建的 Python wheel 上运行相关测试，Rust 共 111 项通过，Python 共 320 项通过，另有 952 个子测试通过。

| 测试范围 | Rust 测试 | Python 测试 |
|---|---|---|
| 凤凰、雪球、变体与预设 | `phoenix`、`snowball`、`snowball_variants`、`autocallable_presets` | `test_phoenix.py`、`test_snowball.py`、`test_snowball_variants.py`、`test_autocallable_presets.py` |
| FD 精度、边界、历史与 Greeks | `autocallable_finite_difference` | `test_autocallable_finite_difference.py`、`test_autocallable_fd_accuracy.py`、`test_autocallable_fd_regressions.py`、`test_autocallable_fd_validation.py` |
| 局部波动率、模型参考与隐含票息 | `local_volatility_structured`、`implied_coupon`、`autocallable_monte_carlo` | `test_local_volatility_structured.py`、`test_quantlib_profiles.py`、`test_implied_coupon.py` |
| 终止返还、方差时钟、可复用解 | `autocallable_rebate`、`variance_time_conventions`、`finite_difference_solution` | `test_autocallable_rebate.py`、`test_variance_time_conventions.py`、`test_finite_difference_solution.py` |

独立凤凰日程测试覆盖了仅敲出、仅派息及同一时刻两项观察重合的情形；返还测试覆盖提前敲出与未敲出到期；可复用解测试覆盖查询现货跨越当期障碍，以及在零方差区间内逐一按远期轨迹结算观察事件。

---

## 11. 误差预算、局限与使用建议

| 用途 | 基准网格 | 第 7.4 节合约上的绝对误差 |
|---|---|---|
| 到期敲入基础定价 | 800×400 | 凤凰约 $4.9\times10^{-7}$，雪球约 $7.7\times10^{-7}$ |
| 每日敲入基础定价 | 800×400 | 凤凰约 $6.3\times10^{-5}$，雪球约 $1.04\times10^{-4}$ |
| 每日敲入，降低时间误差 | 1600×1600 | 凤凰约 $5.6\times10^{-6}$，雪球约 $9.3\times10^{-6}$ |
| 每日敲入，进一步加密 | 3200×3200 | 凤凰约 $1.4\times10^{-6}$，雪球约 $2.3\times10^{-6}$ |

- **空间误差诊断**。当敲出水平与行权价相距极近时，局部网格分辨率变化会引起微小的非单调波动；分别固定时间步加密空间、固定空间步加密时间，即可将这类空间离散误差与每日敲入的时间离散误差清晰剥离开。
- **时间误差调优**。每日敲入包含两百余个监测点，每次事件都会触发隐式半步阻尼重启。若每日敲入合约需要更高精度，应优先增加时间步数 `time_step_count`，并用相邻两级网格比对价格与 Greeks 的收敛幅度。
- **计算域核查**。上边界截断测试应与空间步数加密分开独立验证；局部波动率曲面绑定在绝对现货坐标上，在极端偏斜曲面上仍建议核查自动边界下的收敛稳定性。
- **模型适用边界**。引擎支持 BSM 与局部波动率模型，不支持随机波动率 Heston 模型（会在适用性校验阶段主动拒绝，因 Heston 需额外引入方差维构成二维 PDE）。局部波动率下支持固定绝对曲面的原生 Delta、Gamma 及隐含票息反解；隐含波动率反解因曲面非单一标量而返回 `UnsupportedOperation`。当期观察事件处的现货 Greeks 是否存在，严格取决于支付函数在该点的局部连续性。
- **参考解精度边界**。局部波动率下对数 Euler Monte Carlo 的统计标准误并不包含有限时间步的离散偏差；第 8.9、9.9 节的 MC 对比主要用于核验价格所处量级无误，更高位数的精度评估应以偏微分方程自身的网格加密收敛为准。

---

## 12. 结论

通过分段马尔可夫性质与一比特敲入状态标记，雪球、二元雪球、三元雪球和凤凰四类路径依赖自动赎回票据均可归结为同一套对数坐标一维偏微分方程组求解。在本报告的 BSM 基准测试中，结合控制体积增量跳跃投影、分段 `sinh` 空间加密与事件后 Rannacher 半步阻尼重启，有限差分解随空间与时间网格加密稳定收敛至 QuantLib 静态复制解析解和高精度高斯卷积参考值。默认网格下的主要残差来自每日高频敲入监测引起的时间阻尼重启；相近的敲出水平与行权价则可通过不同空间步数交叉核对。四类产品共享的底层结算逻辑完整覆盖独立凤凰观察日程、终止返还与当期事件，附录 B.3 展示了如何在给定方差时钟和估值时刻下一次求解、批量复用于多现货查询。

---

## 附录 A：源码索引

| 组件 | 文件 |
|---|---|
| 引擎入口、事件与层处理 | [`engines/finite_difference/autocallable.rs`](https://github.com/lilkui/kiyosi/blob/d8413d14ab2f7a53ecc3df145d394bd3c5ba783e/crates/kiyosi/src/engines/finite_difference/autocallable.rs) |
| 设置、格式、上边界、Greeks 补全 | [`engines/finite_difference.rs`](https://github.com/lilkui/kiyosi/blob/d8413d14ab2f7a53ecc3df145d394bd3c5ba783e/crates/kiyosi/src/engines/finite_difference.rs) |
| 对数现货网格、加密、矩匹配算子、投影、样条、时间网格 | [`engines/finite_difference/grid.rs`](https://github.com/lilkui/kiyosi/blob/d8413d14ab2f7a53ecc3df145d394bd3c5ba783e/crates/kiyosi/src/engines/finite_difference/grid.rs) |
| θ 格式、Thomas 求解、分解缓存 | [`engines/finite_difference/step.rs`](https://github.com/lilkui/kiyosi/blob/d8413d14ab2f7a53ecc3df145d394bd3c5ba783e/crates/kiyosi/src/engines/finite_difference/step.rs) |
| BSM 与局部波动率的单态化扩散 | [`engines/finite_difference/diffusion.rs`](https://github.com/lilkui/kiyosi/blob/d8413d14ab2f7a53ecc3df145d394bd3c5ba783e/crates/kiyosi/src/engines/finite_difference/diffusion.rs) |
| 交易日方差规则 | [`time/convention.rs`](https://github.com/lilkui/kiyosi/blob/d8413d14ab2f7a53ecc3df145d394bd3c5ba783e/crates/kiyosi/src/time/convention.rs) |
| 保存解与现货查询 | [`engines/finite_difference/solution.rs`](https://github.com/lilkui/kiyosi/blob/d8413d14ab2f7a53ecc3df145d394bd3c5ba783e/crates/kiyosi/src/engines/finite_difference/solution.rs) |
| 雪球、二元雪球、三元雪球与凤凰的条款、统一视图和支付语义 | [`instruments/autocallable.rs`](https://github.com/lilkui/kiyosi/blob/d8413d14ab2f7a53ecc3df145d394bd3c5ba783e/crates/kiyosi/src/instruments/autocallable.rs)、[`instruments/autocallable/pricing.rs`](https://github.com/lilkui/kiyosi/blob/d8413d14ab2f7a53ecc3df145d394bd3c5ba783e/crates/kiyosi/src/instruments/autocallable/pricing.rs) |
| 雪球与凤凰预设 | [`instruments/autocallable/presets.rs`](https://github.com/lilkui/kiyosi/blob/d8413d14ab2f7a53ecc3df145d394bd3c5ba783e/crates/kiyosi/src/instruments/autocallable/presets.rs) |
| 仓库测试 | [`tests/phoenix.rs`](https://github.com/lilkui/kiyosi/blob/d8413d14ab2f7a53ecc3df145d394bd3c5ba783e/crates/kiyosi/tests/phoenix.rs)、[`tests/snowball.rs`](https://github.com/lilkui/kiyosi/blob/d8413d14ab2f7a53ecc3df145d394bd3c5ba783e/crates/kiyosi/tests/snowball.rs)、[`tests/snowball_variants.rs`](https://github.com/lilkui/kiyosi/blob/d8413d14ab2f7a53ecc3df145d394bd3c5ba783e/crates/kiyosi/tests/snowball_variants.rs)、[`tests/autocallable_finite_difference.rs`](https://github.com/lilkui/kiyosi/blob/d8413d14ab2f7a53ecc3df145d394bd3c5ba783e/crates/kiyosi/tests/autocallable_finite_difference.rs)、[`test_autocallable_fd_accuracy.py`](https://github.com/lilkui/kiyosi/blob/d8413d14ab2f7a53ecc3df145d394bd3c5ba783e/python/tests/test_autocallable_fd_accuracy.py)、[`quantlib_reference/structured.py`](https://github.com/lilkui/kiyosi/blob/d8413d14ab2f7a53ecc3df145d394bd3c5ba783e/python/tests/quantlib_reference/structured.py) |

## 附录 B：复现脚本

使用 `kiyosi==0.22.0`、`QuantLib==1.44` 和 `numpy==2.5.5`。把 B.1 的两个代码块依次保存为 `phoenix_report.py`，把 B.2 的两个代码块保存为 `snowball_report.py`。B.4 演示如何用这些模块复算基准、参数扫描、静态复制和局部波动率比较。

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
