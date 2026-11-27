# Kiyosi vs QuantLib 基准测试分析报告

> **评测版本**：Kiyosi `0.23.0`（提交 `92315743`） vs QuantLib C++ `1.44`（`libQuantLib.so.1.44.0`）
> **评测时间**：2026-11-27 10:01:59 UTC+8（总墙钟耗时 343.98 s）
> **数据来源**：`benchmarks/quantlib/report.json`（Schema v1，状态 `passed`）

---

## 1. 执行摘要

本报告基于 `benchmarks/quantlib/report.json`，对比 Kiyosi 原生核心与 QuantLib C++ 1.44 在衍生品定价上的精度和单线程延迟。测试覆盖 **20 类定价引擎**、**51 个必测语义单元（Semantic Cells）** 和 **59 个评测场景**。每个场景均预设参考值与误差预算，双端通过精度门禁后再比较延迟。

### 核心结论

- **全量通过精度门禁**：全部 **59 个场景**均满足误差预算。5 个蒙特卡洛场景在 32 个预设验证种子下的均方根误差（RMSE）、有符号偏差绝对值和样本标准差均在门限内。
- **全场景延迟领先**：Kiyosi 在全部 **59 个场景**的中位数延迟均低于 QuantLib。以中位数延迟比（$Q/K$）衡量，几何平均加速比为 **9.23×**，中位数加速比为 **6.74×**，区间为 **2.17×–233.84×**。
- **极值分布**：加速比最低为双障碍到期现金不触碰解析场景（`double-touch-out-cash-expiry`，**2.17×**）；最高为 BSM 向上资产不触碰有限差分场景（`fd-bsm-up-no-touch-asset-expiry`，**233.84×**，Kiyosi 使用 400 个时间步，QuantLib 需 16,000 个时间步以满足共同误差预算）。
- **同配置与按精度选配对比**：在双方网格或路径数一致的典型场景中，9 个 $800\times 400$ BSM 一维有限差分场景的几何平均加速比为 **6.14×**，同为 65,536 条路径的欧式看跌和障碍敲入看跌蒙特卡洛场景分别为 **5.40×** 和 **3.09×**；在各自按误差预算选配时间步数的 11 个局部波动率一维有限差分场景中，几何平均加速比为 **15.91×**。

### 分模块汇总

| 算法类别 | 场景数 | 误差预算 | 最大绝对误差（Kiyosi / QuantLib） | 中位数延迟范围（Kiyosi vs QuantLib） | 几何平均加速比 | 中位数加速比 | 加速比区间（$Q/K$） |
| --- | ---: | ---: | --- | --- | ---: | ---: | --- |
| BSM 解析法 | 23 | $1.0\times 10^{-9}$ | $3.55\times 10^{-14}$ / $7.43\times 10^{-12}$ | 27.81 ns – 1.70 $\mu\text{s}$ vs 254.27 ns – 8.19 $\mu\text{s}$ | **6.15×** | 5.06× | 2.17× – 22.37× |
| Heston 解析积分 | 1 | $1.0\times 10^{-7}$ | $2.31\times 10^{-14}$ / $1.95\times 10^{-14}$ | 13.49 $\mu\text{s}$ vs 65.66 $\mu\text{s}$ | **4.87×** | 4.87× | 4.87× |
| BSM 数值积分 | 3 | $10^{-5} - 0.2$ | $1.34\times 10^{-8}$ / $1.82\times 10^{-2}$ | 1.98 $\mu\text{s}$ – 5.18 $\mu\text{s}$ vs 31.19 $\mu\text{s}$ – 31.81 $\mu\text{s}$ | **11.50×** | 15.79× | 6.02× – 16.02× |
| CRR 二叉树 | 3 | $5\times 10^{-3} - 2\times 10^{-2}$ | $5.19\times 10^{-3}$ / $5.18\times 10^{-3}$ | 1.08 $\mu\text{s}$ – 108.70 $\mu\text{s}$ vs 65.85 $\mu\text{s}$ – 5.95 ms | **37.16×** | 61.25× | 5.05× – 165.77× |
| 一维有限差分（BSM） | 11 | $3.0\times 10^{-3}$ | $1.11\times 10^{-3}$ / $1.82\times 10^{-3}$ | 1.00 ms – 2.02 ms vs 6.09 ms – 234.86 ms | **9.66×** | 6.11× | 5.76× – 233.84× |
| 一维有限差分（局部波动率） | 11 | $5.0\times 10^{-3}$ | $2.16\times 10^{-3}$ / $2.04\times 10^{-3}$ | 1.21 ms – 2.50 ms vs 13.68 ms – 532.54 ms | **15.91×** | 11.30× | 6.24× – 219.32× |
| 二维有限差分（Heston） | 2 | $5.0\times 10^{-3}$ | $1.06\times 10^{-3}$ / $3.54\times 10^{-3}$ | 14.45 ms – 15.88 ms vs 210.77 ms – 231.95 ms | **14.60×** | 14.60× | 14.59× – 14.60× |
| BSM 蒙特卡洛 | 5 | $0.10 - 0.15$ | $9.38\times 10^{-2}$ / $5.58\times 10^{-2}$ | 1.45 ms – 103.90 ms vs 7.83 ms – 667.68 ms | **5.91×** | 6.43× | 3.09× – 10.43× |
| **全部场景合计** | **59** | — | — | 27.81 ns – 103.90 ms vs 254.27 ns – 667.68 ms | **9.23×** | **6.74×** | **2.17× – 233.84×** |

---

## 2. 测试环境与评测协议

### 2.1 硬件与编译工具链

| 维度 | 配置详情 |
| --- | --- |
| 操作系统 | `Linux-6.18.58.1-microsoft-standard-WSL2-x86_64-with-glibc2.43` |
| 处理器 | Intel(R) Core(TM) Ultra 9 285（24 核 24 线程，L1d 1.1 MiB / L1i 1.5 MiB / L2 72 MiB / L3 36 MiB） |
| 并发限制 | 单工作线程（`workers_per_backend = 1`），无多线程并行加速 |
| Kiyosi 编译 | `rustc 1.100.0 (0ef1bc386 2026-11-09)`，`cargo build --release --locked -p kiyosi-quantlib-bench --bin quantlib_bench --message-format=json-render-diagnostics`（Cargo release，thin LTO，`RUSTFLAGS` 未额外指定） |
| QuantLib 基准程序 | `c++ (Ubuntu 15.2.0-16ubuntu1) 15.2.0`，`-std=c++17 -O3 -DNDEBUG`，动态链接 `/usr/local/lib/libQuantLib.so.1.44.0` |
| 调度与校验环境 | Python `3.14.4`（加载预先生成的参考值、校验精度门禁与调度配对计时） |

### 2.2 评测方法论

1. **精度门禁优先（Accuracy-First Gating）**：
   每个场景均使用预先生成的参考值 $V_{\text{ref}}$ 和参考不确定度 $u_{\text{ref}}$。双端均须满足：
   $$
   |V_{\text{backend}} - V_{\text{ref}}| + u_{\text{ref}} \le \text{error\_budget}
   $$
   有限差分和蒙特卡洛等数值方法使用各后端预先指定的离散配置，并遵循同一误差预算。
2. **配对交替采样（Paired Alternating Sampling）**：
   合约、市场上下文、模型及引擎对象均在计时循环外预先构造，计时仅覆盖单次公开定价调用（Kiyosi `price()` vs QuantLib `recalculate() + NPV()`）。每个场景预热 3 次后，自适应调整单批迭代次数以达到目标阈值（`target_ms = 20`），再按 `[kiyosi, quantlib]` 与 `[quantlib, kiyosi]` 交替采集 **15 组配对样本**，以抵消系统热漂移与背景噪声。分位数（`q1_ns`、`median_ns`、`q3_ns`、`iqr_ns`）采用包含端点的线性插值计算。
3. **工作量透明度**：
   测试直接调用双端公开原生定价接口，保留引擎固有开销。例如 QuantLib 部分解析与有限差分引擎在 `recalculate()` 时会附带计算部分 Greeks，蒙特卡洛引擎会累加样本方差；这些实际计算均计入测量时间，并在各模块说明中标注。

---

## 3. 分模块精度与性能分析

### 3.1 BSM 解析引擎（23 个场景）

涵盖欧式普通期权、现金／资产数字期权、连续几何／算术平均亚式期权、单障碍期权、二元障碍期权、单触碰／不触碰期权及双障碍／双触碰期权。所有场景共享 $1.0\times 10^{-9}$ 的绝对误差预算，参考解由 Python `Decimal`（50–110 位有效数字）通过高斯幂级数积分、镜像法吸收密度积分及首达时间 Laplace 变换独立计算（$u_{\text{ref}} \in [10^{-13}, 10^{-12}]$）。

| 场景 ID | 家族 (`family`) | Kiyosi 引擎 | 参考价格 | Kiyosi 绝对误差 | QuantLib 绝对误差 | Kiyosi 中位数 (IQR) | QuantLib 中位数 (IQR) | 加速比 ($Q/K$) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `european-bsm-atm-call` | `european_bsm` | `AnalyticEuropeanEngine` | 9.22700550815 | $1.07\times 10^{-14}$ | $1.42\times 10^{-14}$ | 29.03 ns (1.77 ns) | 625.19 ns (17.47 ns) | **21.54×** |
| `european-bsm-itm-call` | `european_bsm` | `AnalyticEuropeanEngine` | 23.9825202131 | $0.00$ | $0.00$ | 35.46 ns (0.79 ns) | 623.54 ns (10.15 ns) | **17.58×** |
| `european-bsm-otm-put` | `european_bsm` | `AnalyticEuropeanEngine` | 3.26238340389 | $8.88\times 10^{-16}$ | $6.22\times 10^{-15}$ | 36.48 ns (1.89 ns) | 631.63 ns (36.72 ns) | **17.31×** |
| `digital-bsm-cash-call` | `digital_bsm` | `AnalyticDigitalEngine` | 4.99551713655 | $0.00$ | $1.78\times 10^{-15}$ | 27.81 ns (0.65 ns) | 621.92 ns (11.31 ns) | **22.37×** |
| `digital-bsm-asset-put` | `digital_bsm` | `AnalyticDigitalEngine` | 34.2714509893 | $0.00$ | $1.42\times 10^{-14}$ | 35.31 ns (1.43 ns) | 635.40 ns (25.31 ns) | **18.00×** |
| `geometric-asian-bsm-call` | `geometric_asian_bsm` | `AnalyticGeometricAveragePriceEngine` | 5.03586754652 | $7.11\times 10^{-15}$ | $6.22\times 10^{-15}$ | 56.13 ns (2.20 ns) | 404.07 ns (19.30 ns) | **7.20×** |
| `geometric-asian-bsm-put` | `geometric_asian_bsm` | `AnalyticGeometricAveragePriceEngine` | 2.35569361785 | $2.66\times 10^{-15}$ | $8.88\times 10^{-15}$ | 55.95 ns (0.45 ns) | 405.84 ns (11.55 ns) | **7.25×** |
| `arithmetic-asian-bsm-call` | `arithmetic_asian_bsm` | `TurnbullWakemanArithmeticAveragePriceEngine` | 5.24650186036 | $3.38\times 10^{-14}$ | $7.43\times 10^{-12}$ | 72.41 ns (1.76 ns) | 311.54 ns (7.20 ns) | **4.30×** |
| `arithmetic-asian-bsm-put` | `arithmetic_asian_bsm` | `TurnbullWakemanArithmeticAveragePriceEngine` | 2.27632052827 | $3.42\times 10^{-14}$ | $6.74\times 10^{-12}$ | 71.49 ns (1.56 ns) | 312.89 ns (2.97 ns) | **4.38×** |
| `barrier-down-out-call-rebate` | `single_barrier_bsm` | `AnalyticBarrierEngine` | 9.71405147606 | $5.33\times 10^{-15}$ | $1.78\times 10^{-15}$ | 156.27 ns (4.39 ns) | 1.12 $\mu\text{s}$ (24.49 ns) | **7.19×** |
| `barrier-up-in-put-rebate` | `single_barrier_bsm` | `AnalyticBarrierEngine` | 1.42695867059 | $2.22\times 10^{-16}$ | $3.33\times 10^{-15}$ | 121.29 ns (2.53 ns) | 1.15 $\mu\text{s}$ (29.93 ns) | **9.49×** |
| `binary-down-out-cash-call` | `binary_barrier_bsm` | `AnalyticBinaryBarrierEngine` | 4.87026073135 | $1.78\times 10^{-15}$ | $8.88\times 10^{-16}$ | 76.46 ns (1.38 ns) | 278.46 ns (4.89 ns) | **3.64×** |
| `binary-up-in-asset-put` | `binary_barrier_bsm` | `AnalyticBinaryBarrierEngine` | 2.97920242858 | $4.44\times 10^{-16}$ | $4.44\times 10^{-16}$ | 72.05 ns (2.68 ns) | 284.99 ns (15.99 ns) | **3.96×** |
| `touch-up-in-cash-hit` | `touch_bsm` | `AnalyticBinaryBarrierEngine` | 3.71214659048 | $2.22\times 10^{-15}$ | $1.78\times 10^{-15}$ | 51.31 ns (0.69 ns) | 280.19 ns (12.24 ns) | **5.46×** |
| `touch-up-in-cash-expiry` | `touch_bsm` | `AnalyticBinaryBarrierEngine` | 3.63775609357 | $8.88\times 10^{-16}$ | $1.33\times 10^{-15}$ | 61.60 ns (0.96 ns) | 254.27 ns (4.68 ns) | **4.13×** |
| `touch-up-out-cash-expiry` | `touch_bsm` | `AnalyticBinaryBarrierEngine` | 5.97013829796 | $0.00$ | $2.66\times 10^{-15}$ | 82.35 ns (3.88 ns) | 257.47 ns (6.45 ns) | **3.13×** |
| `touch-up-in-asset-hit` | `touch_bsm` | `AnalyticBinaryBarrierEngine` | 44.5457590858 | $1.42\times 10^{-14}$ | $2.13\times 10^{-14}$ | 51.25 ns (0.91 ns) | 277.40 ns (3.98 ns) | **5.41×** |
| `touch-up-in-asset-expiry` | `touch_bsm` | `AnalyticBinaryBarrierEngine` | 44.3204945036 | $3.55\times 10^{-14}$ | $1.42\times 10^{-14}$ | 62.46 ns (0.97 ns) | 254.89 ns (7.28 ns) | **4.08×** |
| `touch-up-out-asset-expiry` | `touch_bsm` | `AnalyticBinaryBarrierEngine` | 54.6844888713 | $0.00$ | $1.42\times 10^{-14}$ | 83.04 ns (2.02 ns) | 255.30 ns (4.68 ns) | **3.07×** |
| `double-barrier-out-call` | `double_barrier_bsm` | `AnalyticDoubleBarrierEngine` | 1.08388145926 | $3.40\times 10^{-14}$ | $4.77\times 10^{-14}$ | 1.70 $\mu\text{s}$ (34.73 ns) | 7.90 $\mu\text{s}$ (180.32 ns) | **4.64×** |
| `double-barrier-in-put` | `double_barrier_bsm` | `AnalyticDoubleBarrierEngine` | 4.81765548074 | $3.38\times 10^{-14}$ | $2.22\times 10^{-14}$ | 1.62 $\mu\text{s}$ (23.24 ns) | 8.19 $\mu\text{s}$ (166.86 ns) | **5.06×** |
| `double-touch-in-cash-expiry` | `double_touch_bsm` | `AnalyticDoubleTouchEngine` | 5.99318208860 | $8.88\times 10^{-16}$ | $8.88\times 10^{-16}$ | 824.11 ns (25.64 ns) | 1.82 $\mu\text{s}$ (32.86 ns) | **2.21×** |
| `double-touch-out-cash-expiry` | `double_touch_bsm` | `AnalyticDoubleTouchEngine` | 3.61471230292 | $8.88\times 10^{-16}$ | $4.44\times 10^{-16}$ | 831.48 ns (25.09 ns) | 1.81 $\mu\text{s}$ (44.03 ns) | **2.17×** |

**技术要点**：

- 欧式普通期权与到期数字期权的中位数延迟为 Kiyosi $27.81\text{–}36.48\ \text{ns}$、QuantLib $621.92\text{–}635.40\ \text{ns}$，加速比为 **17.31×–22.37×**。Kiyosi 的 `price()` 返回价格标量，QuantLib 的 `AnalyticEuropeanEngine` 在 `recalculate()` 中也计算 Greeks。到期结算的单触碰与单不触碰场景加速比为 **3.07×–4.13×**，双触碰与双不触碰场景为 **2.17×–2.21×**。
- Kiyosi 的双障碍与双触碰引擎在吸收镜像级数与谱级数之间自适应选择（内部上限分别为 64 项和 256 项）。QuantLib 双障碍使用 `series = 5`，双触碰采用最多 99 项的 Hui 级数（末项阈值 $10^{-8}$）。这四个场景的加速比为 **2.17×–5.06×**，双端绝对误差均在 $10^{-16}\text{–}10^{-14}$ 之间。

---

### 3.2 数值积分与 CRR 二叉树引擎（6 个场景）

| 场景 ID | 引擎 (`engine`) | 配置对比（Kiyosi vs QuantLib） | 误差预算 | Kiyosi 绝对误差 | QuantLib 绝对误差 | Kiyosi 中位数 (IQR) | QuantLib 中位数 (IQR) | 加速比 ($Q/K$) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `quadrature-bsm-european-call` | `QuadratureVanillaEngine` | 512 步复合 Simpson（行权价分段） vs 5000 步固定梯形法则 | $1.00\times 10^{-5}$ | $8.30\times 10^{-9}$ | $5.05\times 10^{-6}$ | 5.18 $\mu\text{s}$ (0.05 $\mu\text{s}$) | 31.19 $\mu\text{s}$ (0.20 $\mu\text{s}$) | **6.02×** |
| `quadrature-bsm-cash-call` | `QuadratureDigitalEngine` | 512 步复合 Simpson（行权价分段） vs 5000 步固定梯形法则 | $2.00\times 10^{-2}$ | $6.77\times 10^{-10}$ | $1.73\times 10^{-3}$ | 1.99 $\mu\text{s}$ (0.02 $\mu\text{s}$) | 31.81 $\mu\text{s}$ (0.30 $\mu\text{s}$) | **16.02×** |
| `quadrature-bsm-asset-put` | `QuadratureDigitalEngine` | 512 步复合 Simpson（行权价分段） vs 5000 步固定梯形法则 | $2.00\times 10^{-1}$ | $1.34\times 10^{-8}$ | $1.82\times 10^{-2}$ | 1.98 $\mu\text{s}$ (0.06 $\mu\text{s}$) | 31.25 $\mu\text{s}$ (0.77 $\mu\text{s}$) | **15.79×** |
| `crr-bsm-european-call` | `CoxRossRubinsteinVanillaEngine` | `step_count = 512` vs `step_count = 512` | $5.00\times 10^{-3}$ | $3.80\times 10^{-3}$ | $3.83\times 10^{-3}$ | 1.08 $\mu\text{s}$ (0.02 $\mu\text{s}$) | 65.85 $\mu\text{s}$ (2.35 $\mu\text{s}$) | **61.25×** |
| `crr-bsm-american-put` | `CoxRossRubinsteinVanillaEngine` | `step_count = 512` vs `step_count = 512` | $5.00\times 10^{-3}$ | $1.82\times 10^{-3}$ | $1.80\times 10^{-3}$ | 108.70 $\mu\text{s}$ (0.87 $\mu\text{s}$) | 549.35 $\mu\text{s}$ (9.61 $\mu\text{s}$) | **5.05×** |
| `crr-bsm-down-out-call` | `CoxRossRubinsteinBarrierEngine` | `step_count = 2048` vs `step_count = 2048`（纯离散树） | $2.00\times 10^{-2}$ | $5.19\times 10^{-3}$ | $5.18\times 10^{-3}$ | 35.86 $\mu\text{s}$ (1.37 $\mu\text{s}$) | 5.95 ms (0.14 ms) | **165.77×** |

**技术要点**：

- 在两个数字期权积分场景中，Kiyosi 在行权价处切分积分区间，使用 512 步复合 Simpson 法（$\pm 8\sigma$），绝对误差分别为 $6.77\times 10^{-10}$ 和 $1.34\times 10^{-8}$。QuantLib `IntegralEngine` 使用 5000 区间的固定梯形法，对应误差为 $1.73\times 10^{-3}$ 和 $1.82\times 10^{-2}$。Kiyosi 在这两个场景的加速比为 **15.79×–16.02×**。
- CRR 场景中双方步数相同，绝对误差接近。Kiyosi 对 512 步欧式看涨直接按二项分布权重求到期收益期望，对 2048 步下敲出看涨用反射法计算逐步监控下的格点权重，加速比分别为 **61.25×** 和 **165.77×**；512 步美式看跌需逐层回推处理提前行权，加速比为 **5.05×**。

---

### 3.3 一维有限差分引擎：BSM 与局部波动率（22 个场景）

涵盖 BSM（`fd_bsm`，11 个场景，误差预算 $3.0\times 10^{-3}$）与外部给定的非恒定局部波动率曲面（`fd_local_vol`，11 个场景，误差预算 $5.0\times 10^{-3}$）。局部波动率曲面在时间（`2025-01-01` 至 `2026-01-01`，Act/365F）与现货（$[80,120]$，节点矩阵 `[[0.30, 0.15], [0.35, 0.20]]`）上作双线性插值，现货超出区间时取相应端点值。

- Kiyosi 在 22 个场景中均使用 800 个空间步、对数现货网格和 Rannacher 格式。BSM 场景使用 400 个时间步。局部波动率场景中，美式看跌和向上资产不触碰使用 200 步，其余 9 个场景使用 100 步。两个普通欧式场景自动选择求解域并在行权价附近加密节点，其余场景显式设置 `upper = 400`。
- QuantLib 使用 `space = 800` 的自动对数网格与 Crank–Nicolson 格式（`damping = 2`），局部波动率场景以 `mesher_vol = 0.5` 定界网格。BSM 与局部波动率中各有 9 个场景使用 400 个时间步；为满足共同误差预算，向上现金单触碰（`up-one-touch-cash-hit`）使用 1600 步，向上资产不触碰（`up-no-touch-asset-expiry`）使用 16000 步。

#### 3.3.1 BSM 一维有限差分（`fd_bsm`，误差预算 $3.0\times 10^{-3}$）

| 场景 ID | Kiyosi 引擎 | 时间步（K / Q） | 参考价格 | Kiyosi 绝对误差 | QuantLib 绝对误差 | Kiyosi 中位数 (IQR) | QuantLib 中位数 (IQR) | 加速比 ($Q/K$) |
| --- | --- | :---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `fd-bsm-european-call` | `FiniteDifferenceVanillaEngine` | 400 / 400 | 9.22700550815 | $4.83\times 10^{-5}$ | $7.08\times 10^{-5}$ | 1.07 ms (0.02 ms) | 6.17 ms (0.15 ms) | **5.76×** |
| `fd-bsm-american-put` | `FiniteDifferenceVanillaEngine` | 400 / 400 | 6.66068454589 | $1.11\times 10^{-3}$ | $1.20\times 10^{-3}$ | 1.13 ms (0.08 ms) | 8.12 ms (0.15 ms) | **7.19×** |
| `fd-bsm-cash-digital-call` | `FiniteDifferenceDigitalEngine` | 400 / 400 | 4.94581091053 | $8.78\times 10^{-6}$ | $6.84\times 10^{-5}$ | 1.05 ms (0.06 ms) | 6.10 ms (0.14 ms) | **5.78×** |
| `fd-bsm-asset-digital-put` | `FiniteDifferenceDigitalEngine` | 400 / 400 | 48.7733863768 | $3.19\times 10^{-5}$ | $8.01\times 10^{-4}$ | 1.08 ms (0.04 ms) | 6.27 ms (0.25 ms) | **5.82×** |
| `fd-bsm-down-out-call` | `FiniteDifferenceBarrierEngine` | 400 / 400 | 9.13330643650 | $2.32\times 10^{-5}$ | $1.61\times 10^{-6}$ | 1.05 ms (0.02 ms) | 6.14 ms (0.35 ms) | **5.84×** |
| `fd-bsm-terminal-down-out-cash` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 400 | 4.82180082739 | $1.42\times 10^{-5}$ | $1.47\times 10^{-4}$ | 1.02 ms (0.02 ms) | 6.17 ms (0.31 ms) | **6.04×** |
| `fd-bsm-terminal-up-in-asset` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 400 | 2.94955886912 | $3.56\times 10^{-5}$ | $5.60\times 10^{-5}$ | 2.02 ms (0.02 ms) | 13.61 ms (0.68 ms) | **6.74×** |
| `fd-bsm-down-no-touch-cash-expiry` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 400 | 7.13408843096 | $2.66\times 10^{-6}$ | $1.49\times 10^{-4}$ | 1.01 ms (0.02 ms) | 6.19 ms (0.12 ms) | **6.15×** |
| `fd-bsm-down-one-touch-asset-hit` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 400 | 19.4492167646 | $4.10\times 10^{-6}$ | $1.82\times 10^{-3}$ | 1.00 ms (0.03 ms) | 6.09 ms (0.07 ms) | **6.11×** |
| `fd-bsm-up-one-touch-cash-hit` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 1600 | 3.69391182061 | $7.81\times 10^{-6}$ | $1.48\times 10^{-3}$ | 1.00 ms (0.02 ms) | 23.56 ms (0.31 ms) | **23.55×** |
| `fd-bsm-up-no-touch-asset-expiry` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 16000 | 54.1403691157 | $1.01\times 10^{-4}$ | $1.77\times 10^{-3}$ | 1.00 ms (0.04 ms) | 234.86 ms (4.79 ms) | **233.84×** |

#### 3.3.2 局部波动率一维有限差分（`fd_local_vol`，误差预算 $5.0\times 10^{-3}$）

| 场景 ID | Kiyosi 引擎 | 时间步（K / Q） | 参考价格 | Kiyosi 绝对误差 | QuantLib 绝对误差 | Kiyosi 中位数 (IQR) | QuantLib 中位数 (IQR) | 加速比 ($Q/K$) |
| --- | --- | :---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `fd-local-vol-european-call` | `FiniteDifferenceVanillaEngine` | 100 / 400 | 11.0017427062 | $2.21\times 10^{-4}$ | $1.02\times 10^{-4}$ | 1.24 ms (0.02 ms) | 13.68 ms (0.38 ms) | **11.00×** |
| `fd-local-vol-american-put` | `FiniteDifferenceVanillaEngine` | 200 / 400 | 8.36106642823 | $2.16\times 10^{-3}$ | $1.24\times 10^{-3}$ | 2.50 ms (0.12 ms) | 15.62 ms (0.48 ms) | **6.24×** |
| `fd-local-vol-cash-digital-call` | `FiniteDifferenceDigitalEngine` | 100 / 400 | 5.39093949985 | $7.30\times 10^{-5}$ | $1.22\times 10^{-4}$ | 1.21 ms (0.01 ms) | 13.81 ms (0.77 ms) | **11.42×** |
| `fd-local-vol-asset-digital-put` | `FiniteDifferenceDigitalEngine` | 100 / 400 | 40.5303971416 | $1.67\times 10^{-3}$ | $1.95\times 10^{-3}$ | 1.22 ms (0.05 ms) | 13.71 ms (0.61 ms) | **11.21×** |
| `fd-local-vol-down-out-call` | `FiniteDifferenceBarrierEngine` | 100 / 400 | 10.3817423850 | $2.21\times 10^{-4}$ | $1.40\times 10^{-4}$ | 1.24 ms (0.02 ms) | 13.88 ms (0.10 ms) | **11.18×** |
| `fd-local-vol-terminal-down-out-cash` | `FiniteDifferenceBinaryBarrierEngine` | 100 / 400 | 4.83462680702 | $4.58\times 10^{-5}$ | $2.48\times 10^{-4}$ | 1.22 ms (0.02 ms) | 13.81 ms (0.36 ms) | **11.30×** |
| `fd-local-vol-terminal-up-in-asset` | `FiniteDifferenceBinaryBarrierEngine` | 100 / 400 | 3.48032683172 | $9.48\times 10^{-4}$ | $1.48\times 10^{-5}$ | 2.49 ms (0.03 ms) | 30.34 ms (1.01 ms) | **12.20×** |
| `fd-local-vol-down-no-touch-cash-expiry` | `FiniteDifferenceBinaryBarrierEngine` | 100 / 400 | 5.90771262187 | $1.27\times 10^{-4}$ | $2.35\times 10^{-4}$ | 1.23 ms (0.02 ms) | 13.86 ms (0.44 ms) | **11.24×** |
| `fd-local-vol-down-one-touch-asset-hit` | `FiniteDifferenceBinaryBarrierEngine` | 100 / 400 | 29.6031381560 | $9.64\times 10^{-4}$ | $1.03\times 10^{-3}$ | 1.23 ms (0.04 ms) | 14.15 ms (0.59 ms) | **11.54×** |
| `fd-local-vol-up-one-touch-cash-hit` | `FiniteDifferenceBinaryBarrierEngine` | 100 / 1600 | 4.51261775417 | $1.94\times 10^{-4}$ | $1.83\times 10^{-3}$ | 1.23 ms (0.07 ms) | 53.12 ms (1.62 ms) | **43.04×** |
| `fd-local-vol-up-no-touch-asset-expiry` | `FiniteDifferenceBinaryBarrierEngine` | 200 / 16000 | 44.3991225309 | $5.54\times 10^{-4}$ | $2.04\times 10^{-3}$ | 2.43 ms (0.07 ms) | 532.54 ms (4.87 ms) | **219.32×** |

**技术要点**：

- 在双方均采用 $800\times 400$ 网格的 9 个 BSM 场景中，加速比为 **5.76×–7.19×**。在 QuantLib 采用 400 个时间步（Kiyosi 为 100 或 200 步）的 9 个局部波动率场景中，加速比为 **6.24×–12.20×**。网格节点分布和时间推进方式也会影响误差与延迟。
- 为通过共同精度门禁，QuantLib 在向上现金单触碰与向上资产不触碰场景中分别使用 1600 和 16000 个时间步。此时向上现金单触碰在 BSM 与局部波动率下的加速比分别为 **23.55×** 和 **43.04×**，向上资产不触碰分别为 **233.84×** 和 **219.32×**。

---

### 3.4 Heston 随机波动率引擎（3 个场景）

共用市场与模型参数：$S = K = 100,\ r = 0.05,\ q = 0.02,\ v_0 = \theta = 0.04,\ \kappa = 1.5,\ \xi = 0.3,\ \rho = -0.7$，期限 1 年（`2025-01-01` 至 `2026-01-01`）。

| 场景 ID | 引擎 (`engine`) | 算法与配置对比（Kiyosi vs QuantLib） | 误差预算 | Kiyosi 绝对误差 | QuantLib 绝对误差 | Kiyosi 中位数 (IQR) | QuantLib 中位数 (IQR) | 加速比 ($Q/K$) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `heston-analytic-call` | `AnalyticHestonEuropeanEngine` | 自适应 Fourier + 确定性方差控制变量（$\text{tol}=10^{-9}$） vs Gatheral 自适应 Lobatto（$\text{rel\_tol}=10^{-9}$） | $1.00\times 10^{-7}$ | $2.31\times 10^{-14}$ | $1.95\times 10^{-14}$ | 13.49 $\mu\text{s}$ (0.22 $\mu\text{s}$) | 65.66 $\mu\text{s}$ (1.09 $\mu\text{s}$) | **4.87×** |
| `heston-fd-european-call` | `FiniteDifferenceHestonVanillaEngine` | MCS ADI ($\theta=1/3$), $200\times 50\times 200$ 区间 vs Hundsdorfer ADI, $200\times 100\times 200$ 节点 | $5.00\times 10^{-3}$ | $5.70\times 10^{-4}$ | $9.05\times 10^{-4}$ | 14.45 ms (0.56 ms) | 210.77 ms (1.52 ms) | **14.59×** |
| `heston-fd-american-put` | `FiniteDifferenceHestonVanillaEngine` | MCS ADI + Ikonen–Toivanen 分裂, $200\times 50\times 200$ vs Hundsdorfer + 投影, $200\times 100\times 200$ | $5.00\times 10^{-3}$ | $1.06\times 10^{-3}$ | $3.54\times 10^{-3}$ | 15.88 ms (0.44 ms) | 231.95 ms (4.77 ms) | **14.60×** |

**技术要点**：

- Heston 欧式场景的参考值由 Gatheral–Lobatto 与独立 exp-sinh Fourier 积分交叉校验，参考不确定度为 $10^{-11}$。两个被测解析引擎相对该参考值的绝对误差均约为 $2\times 10^{-14}$。
- Heston 二维有限差分中，Kiyosi 以对数现货和方差为坐标，现货上界为 400，方差范围为 $[0,0.6]$。时间推进使用 Modified Craig–Sneyd ADI 格式（$\theta=1/3$），美式行权采用 Ikonen–Toivanen 算子分裂。QuantLib 使用自动求解域、Hundsdorfer 格式与原生美式收益投影。所测配置下，Kiyosi 在欧式和美式场景中的绝对误差均更小，加速比分别为 **14.59×** 和 **14.60×**。

---

### 3.5 BSM 蒙特卡洛引擎（5 个场景）

全部场景采用单线程伪随机抽样，关闭对偶变量（`antithetic = false`）与控制变量（`control_variate = false`）。Kiyosi 使用块流式 PCG32 + Box–Muller；QuantLib 使用 MT19937 + 逆正态分布。除计时种子 `seed = 1729` 外，双方均在 32 个预设验证种子（$1009 + 97i,\ i=0\dots 31$）上检验样本统计量。

#### 3.5.1 计时种子精度与延迟表现（`seed = 1729`）

| 场景 ID | 引擎 (`engine`) | 物理路径数（K / Q） | 误差预算 | 参考价格 | Kiyosi 计时误差 | QuantLib 计时误差 | Kiyosi 中位数 (IQR) | QuantLib 中位数 (IQR) | 加速比 ($Q/K$) |
| --- | --- | :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `mc-european-call` | `MonteCarloVanillaEngine` | 131,072 / 262,144 | $0.10$ | 9.22700550815 | $6.38\times 10^{-2}$ | $3.14\times 10^{-2}$ | 3.03 ms (0.06 ms) | 31.60 ms (1.14 ms) | **10.43×** |
| `mc-european-put` | `MonteCarloVanillaEngine` | 65,536 / 65,536 | $0.10$ | 6.33008062755 | $1.58\times 10^{-2}$ | $4.47\times 10^{-2}$ | 1.45 ms (0.02 ms) | 7.83 ms (0.32 ms) | **5.40×** |
| `mc-barrier-down-out-call` | `MonteCarloBarrierEngine` | 65,536 / 131,072 | $0.10$ | 7.58695396974 | $9.38\times 10^{-2}$ | $3.13\times 10^{-2}$ | 3.17 ms (0.03 ms) | 20.41 ms (0.37 ms) | **6.44×** |
| `mc-barrier-up-in-put` | `MonteCarloBarrierEngine` | 65,536 / 65,536 | $0.10$ | 0.230613308713 | $2.17\times 10^{-3}$ | $3.01\times 10^{-5}$ | 3.35 ms (0.24 ms) | 10.36 ms (0.31 ms) | **3.09×** |
| `mc-american-put` | `MonteCarloVanillaEngine` | 65,536 / 65,536 (+32,768 校准) | $0.15$ | 6.66068454589 | $3.18\times 10^{-3}$ | $5.58\times 10^{-2}$ | 103.90 ms (2.06 ms) | 667.68 ms (10.19 ms) | **6.43×** |

#### 3.5.2 32 种子集合验证统计量（Seed Ensemble Validation）

| 场景 ID | 门禁上限（RMSE / \|Bias\| / StdDev） | Kiyosi RMSE | QuantLib RMSE | Kiyosi 有符号偏差 | QuantLib 有符号偏差 | Kiyosi 样本标准差 (SE) | QuantLib 样本标准差 (SE) | 最大绝对误差（K / Q） |
| --- | :---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `mc-european-call` | $0.05$ / $0.025$ / $0.05$ | $3.11\times 10^{-2}$ | $2.88\times 10^{-2}$ | $+2.85\times 10^{-3}$ | $-2.53\times 10^{-3}$ | $3.14\times 10^{-2}$ ($5.56\times 10^{-3}$) | $2.92\times 10^{-2}$ ($5.16\times 10^{-3}$) | $8.39\times 10^{-2}$ / $6.07\times 10^{-2}$ |
| `mc-european-put` | $0.05$ / $0.025$ / $0.05$ | $2.70\times 10^{-2}$ | $3.52\times 10^{-2}$ | $-3.28\times 10^{-3}$ | $+1.85\times 10^{-2}$ | $2.72\times 10^{-2}$ ($4.81\times 10^{-3}$) | $3.04\times 10^{-2}$ ($5.37\times 10^{-3}$) | $4.49\times 10^{-2}$ / $8.08\times 10^{-2}$ |
| `mc-barrier-down-out-call` | $0.05$ / $0.025$ / $0.05$ | $3.45\times 10^{-2}$ | $3.66\times 10^{-2}$ | $+1.13\times 10^{-3}$ | $-7.45\times 10^{-3}$ | $3.51\times 10^{-2}$ ($6.20\times 10^{-3}$) | $3.64\times 10^{-2}$ ($6.43\times 10^{-3}$) | $6.64\times 10^{-2}$ / $9.87\times 10^{-2}$ |
| `mc-barrier-up-in-put` | $0.05$ / $0.025$ / $0.05$ | $1.08\times 10^{-3}$ | $7.32\times 10^{-3}$ | $-5.32\times 10^{-5}$ | $+5.01\times 10^{-3}$ | $1.09\times 10^{-3}$ ($1.93\times 10^{-4}$) | $5.41\times 10^{-3}$ ($9.57\times 10^{-4}$) | $2.66\times 10^{-3}$ / $1.41\times 10^{-2}$ |
| `mc-american-put` | $0.075$ / $0.05$ / $0.075$ | $4.05\times 10^{-2}$ | $4.02\times 10^{-2}$ | $-2.41\times 10^{-2}$ | $-2.54\times 10^{-2}$ | $3.31\times 10^{-2}$ ($5.84\times 10^{-3}$) | $3.16\times 10^{-2}$ ($5.58\times 10^{-3}$) | $7.95\times 10^{-2}$ / $9.57\times 10^{-2}$ |

**技术要点**：

- Kiyosi 直接计算布朗桥条件存活概率，QuantLib `MCBarrierEngine` 用固定种子（`seed = 5`）的辅助随机流抽样障碍穿越。在 `mc-barrier-up-in-put` 中，双方均用 65,536 条路径，Kiyosi 的加速比为 **3.09×**，32 种子 RMSE 分别为 Kiyosi $1.08\times 10^{-3}$、QuantLib $7.32\times 10^{-3}$。在 `mc-barrier-down-out-call` 中，Kiyosi 用 65,536 条路径得到 RMSE $0.0345$，QuantLib 用 131,072 条路径得到 RMSE $0.0366$，加速比为 **6.44×**。
- **美式最小二乘蒙特卡洛（LSM）**：在 `mc-american-put`（65,536 条定价路径、50 个行权时间步、二次单项式基）中，Kiyosi 在实值（ITM）定价路径上直接做样本内回归拟合（基函数 $1, S/K, (S/K)^2$），而 QuantLib 在每次 `recalculate()` 中先独立模拟 32,768 条校准路径再模拟 65,536 条定价路径。根据 `report.json` 记录的 LSM 细化实验（`lsm_refinement`）：
  - 将定价路径翻倍至 $131{,}072$ 时，Kiyosi 与 QuantLib 的 32 种子 RMSE 分别降至 $0.0332$ 与 $0.0315$；
  - 在 $131{,}072$ 路径下将行权步从 50 加密至 100，Kiyosi 与 QuantLib 的种子均值变化仅为 $-0.00141$（$\text{SE}=0.00340$）与 $+0.00075$（$\text{SE}=0.00297$）；
  - 将 QuantLib 校准路径从 $32{,}768$ 翻倍至 $65{,}536$ 时，均值变化仅为 $+4.56\times 10^{-5}$（$\text{SE}=7.16\times 10^{-4}$）。
  基线配置的 32 种子 RMSE 为 Kiyosi $0.0405$、QuantLib $0.0402$，中位数延迟分别为 $103.90\ \text{ms}$ 和 $667.68\ \text{ms}$，加速比为 **6.43×**。

---

## 4. 覆盖范围、局限与解读说明

1. **严格语义对齐与排除边界**：
   本基准覆盖 **20 类引擎（51 个语义单元）**，每类都能在相同合约条款、市场模型与算法类别下与 QuantLib 原生引擎对照。Kiyosi 其余 14 类引擎因缺乏直接等价的 QuantLib 原生实现而未纳入对比，包括：
   - 近似公式版本不同：`BjerksundStenslandVanillaEngine`（Kiyosi 实现 2002 版，QuantLib 为 1993 版）；
   - 结构化奇异产品无内置对应引擎：自动赎回（`Autocallable`）、累购累沽（`Accumulator`）的积分、有限差分与蒙特卡洛引擎，以及区间累计解析引擎（`AnalyticRangeAccrualEngine`）；
   - 离散／连续监控或算法语义差异：数字期权与连续平均亚式蒙特卡洛、双障碍／双触碰有限差分、障碍期权数值积分及数字期权 CRR 二叉树。
2. **加速比解读注意事项**：
   - **离散步数与路径数差异**：3 个 CRR 场景步数相同，9 个 BSM 一维有限差分场景空间与时间步数均相同；11 个局部波动率场景时间步数均有差异（其中向上资产不触碰为 200 步 vs 16,000 步，加速比 **219.32×**）。5 个蒙特卡洛场景中有 3 个定价路径数相同，其中美式看跌还包含 QuantLib 的 32,768 条独立校准路径。
   - **接口固有附加计算**：QuantLib 原生 `recalculate()` 在部分解析引擎和有限差分引擎中会同步计算 Greeks，在蒙特卡洛中会累计样本方差；Kiyosi 的 `price()` 仅计算价格标量（Greeks 由 `price_with_greeks()` 按需调用）。
   - **单核基准**：所有测量均固定 `workers = 1`，仅反映单核指令与内存布局效率，不包含 Kiyosi 蒙特卡洛引擎在多线程 Rayon 池下的并行扩展加速。
