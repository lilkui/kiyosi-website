# Kiyosi vs QuantLib 基准测试分析报告

> **适用版本**：Kiyosi `0.21.0`（提交 `95dc9115`） vs QuantLib C++ `1.44`（`libQuantLib.so.1.44.0`）
> **评测时间**：2026-11-20 19:16:20 UTC+8（总墙钟耗时 352.86 s）
> **数据来源**：`benchmarks/quantlib/report.json`（Schema v1，状态 `passed`）

---

## 1. 执行摘要

本报告基于 `benchmarks/quantlib/report.json` 的实测数据，评估 Kiyosi 原生核心与 QuantLib C++ 1.44 的衍生品定价精度和单线程延迟。测试覆盖 **20 类定价引擎**、**51 个必测语义单元（Semantic Cells）** 和 **59 个评测场景**。每个场景预先指定参考值及误差预算，双端均通过精度门禁后才比较延迟。

### 核心结论

- 全部 **59 个场景**均通过误差预算校验（$|\text{Price} - \text{Reference}| + u_{\text{ref}} \le \text{Budget}$）。5 个蒙特卡洛场景使用 32 个预设验证种子（$1009 + 97i,\ i=0\dots 31$），均方根误差（RMSE）、有符号偏差的绝对值和样本标准差均在门限内。
- Kiyosi 在 **59 个场景**中的中位数延迟均低于 QuantLib。按 $Q/K = \text{Median}(\text{QuantLib}) / \text{Median}(\text{Kiyosi})$ 计算，几何平均加速比为 **4.93×**，中位数加速比为 **4.07×**，区间为 **1.16×–113.18×**。
- Heston 欧式看涨解析积分（`heston-analytic-call`）的加速比最小，为 **1.16×**。Kiyosi 和 QuantLib 的中位数延迟分别为 $57.83\ \mu\text{s}$ 和 $66.90\ \mu\text{s}$，绝对误差均约为 $2\times 10^{-14}$。
- BSM 解析引擎的加速比为 **2.13×–22.63×**（几何平均 **6.13×**）。采用相同空间规模和时间步数的一维有限差分场景中，BSM 的加速比为 **2.91×–3.55×**（几何平均 **3.03×**），局部波动率为 **1.27×–2.38×**（几何平均 **2.00×**）。路径数相同的欧式与障碍蒙特卡洛场景的加速比分别为 **7.11×** 和 **2.91×**。

### 分模块汇总

| 算法类别 | 场景数 | 误差预算 | 最大绝对误差（Kiyosi / QuantLib） | 中位数延迟范围（Kiyosi vs QuantLib） | 几何平均加速比 | 中位数加速比 | 加速比区间（$Q/K$） |
| --- | ---: | ---: | --- | --- | ---: | ---: | --- |
| BSM 解析法 | 23 | $1.0\times 10^{-9}$ | $3.55\times 10^{-14}$ / $7.43\times 10^{-12}$ | 27.37 ns – 1.70 $\mu\text{s}$ vs 253.07 ns – 8.24 $\mu\text{s}$ | **6.13×** | 5.05× | 2.13× – 22.63× |
| Heston 解析积分 | 1 | $1.0\times 10^{-7}$ | $2.31\times 10^{-14}$ / $1.95\times 10^{-14}$ | 57.83 $\mu\text{s}$ vs 66.90 $\mu\text{s}$ | **1.16×** | 1.16× | 1.16× |
| BSM 数值积分 | 3 | $10^{-5} - 0.2$ | $1.34\times 10^{-8}$ / $1.82\times 10^{-2}$ | 1.97 $\mu\text{s}$ – 5.03 $\mu\text{s}$ vs 30.78 $\mu\text{s}$ – 31.63 $\mu\text{s}$ | **11.50×** | 15.48× | 6.14× – 16.02× |
| CRR 二叉树 | 3 | $5\times 10^{-3} - 2\times 10^{-2}$ | $5.19\times 10^{-3}$ / $5.18\times 10^{-3}$ | 8.16 $\mu\text{s}$ – 3.01 ms vs 64.93 $\mu\text{s}$ – 5.86 ms | **4.32×** | 5.19× | 1.95× – 7.95× |
| 一维有限差分（BSM） | 11 | $3.0\times 10^{-3}$ | $1.20\times 10^{-3}$ / $1.82\times 10^{-3}$ | 2.08 ms – 4.16 ms vs 6.08 ms – 235.04 ms | **4.75×** | 2.94× | 2.91× – 113.18× |
| 一维有限差分（局部波动率） | 11 | $5.0\times 10^{-3}$ | $1.12\times 10^{-3}$ / $2.04\times 10^{-3}$ | 6.60 ms – 13.18 ms vs 13.55 ms – 535.71 ms | **3.17×** | 2.09× | 1.27× – 78.43× |
| 二维有限差分（Heston） | 2 | $5.0\times 10^{-3}$ | $1.12\times 10^{-3}$ / $3.54\times 10^{-3}$ | 91.62 ms – 95.15 ms vs 210.92 ms – 231.48 ms | **2.37×** | 2.37× | 2.22× – 2.53× |
| BSM 蒙特卡洛 | 5 | $0.10 - 0.15$ | $9.38\times 10^{-2}$ / $5.58\times 10^{-2}$ | 1.10 ms – 136.92 ms vs 7.82 ms – 662.51 ms | **6.06×** | 6.28× | 2.91× – 12.99× |
| **全部场景合计** | **59** | — | — | 27.37 ns – 136.92 ms vs 253.07 ns – 662.51 ms | **4.93×** | **4.07×** | **1.16× – 113.18×** |

---

## 2. 测试环境与评测协议

### 2.1 硬件与编译工具链

| 维度 | 配置详情 |
| --- | --- |
| 操作系统 | `Linux-6.18.58.1-microsoft-standard-WSL2-x86_64-with-glibc2.43` |
| 处理器 | Intel(R) Core(TM) Ultra 9 285（24 核 24 线程，L1d 1.1 MiB / L1i 1.5 MiB / L2 72 MiB / L3 36 MiB） |
| 并发限制 | 单工作线程（`workers_per_backend = 1`），无多线程并行加速 |
| Kiyosi 编译 | `rustc 1.99.1 (58cf8f9c3 2026-10-13)`，`cargo build --release --locked -p kiyosi-quantlib-bench --bin quantlib_bench --message-format=json-render-diagnostics`（Cargo release，thin LTO，`RUSTFLAGS` 未额外指定） |
| QuantLib 基准程序 | `c++ (Ubuntu 15.2.0-16ubuntu1) 15.2.0`，`-std=c++17 -O3 -DNDEBUG`，动态链接 `/usr/local/lib/libQuantLib.so.1.44.0` |
| 调度与校验环境 | Python `3.14.4`（负责独立参考解生成、精度门禁校验与配对计时调度） |

### 2.2 评测方法论

1. **精度门禁优先（Accuracy-First Gating）**：
   每个场景均使用预先生成的参考值 $V_{\text{ref}}$ 和参考不确定度 $u_{\text{ref}}$。双端均须满足以下条件。
   $$
   |V_{\text{backend}} - V_{\text{ref}}| + u_{\text{ref}} \le \text{error\_budget}
   $$
   有限差分和蒙特卡洛等数值方法使用各后端预先指定的离散配置，并遵循同一误差预算。
2. **配对交替采样（Paired Alternating Sampling）**：
   合约、市场上下文、模型及引擎对象均在计时循环外预先构造，计时仅测量单次公开定价调用（Kiyosi `price()` vs QuantLib `recalculate() + NPV()`）。每个场景执行 3 次预热，随后自适应调整单批迭代次数使单批耗时达到目标阈值（`target_ms = 20`），并按 `[kiyosi, quantlib]` 与 `[quantlib, kiyosi]` 交替顺序采集 **15 组配对样本**，抵消系统热漂移与背景噪声。分位数（`q1_ns`、`median_ns`、`q3_ns`、`iqr_ns`）采用包含端点的线性插值计算。
3. **工作量透明度**：
   测试直接调用双端公开原生定价接口，不人为剥离引擎内部固有开销。例如 QuantLib 部分解析与有限差分引擎在 `recalculate()` 时会附带计算部分 Greeks，其蒙特卡洛引擎会累加样本方差；这些实际发生的计算均保留在测量时间内，并在各模块分析中明确说明。

---

## 3. 分模块精度与性能分析

### 3.1 BSM 解析引擎（23 个场景）

涵盖欧式普通期权、现金／资产数字期权、连续几何／算术平均亚式期权、单障碍期权、二元障碍期权、单触碰／不触碰期权及双障碍／双触碰期权。所有场景共享 $1.0\times 10^{-9}$ 的绝对误差预算，参考解由 Python `Decimal`（50–110 位有效数字）通过高斯幂级数积分、镜像法吸收密度积分及首达时间 Laplace 变换独立计算（$u_{\text{ref}} \in [10^{-13}, 10^{-12}]$）。

| 场景 ID | 家族 (`family`) | Kiyosi 引擎 | 参考价格 | Kiyosi 绝对误差 | QuantLib 绝对误差 | Kiyosi 中位数 (IQR) | QuantLib 中位数 (IQR) | 加速比 ($Q/K$) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `european-bsm-atm-call` | `european_bsm` | `AnalyticEuropeanEngine` | 9.22700550815 | $1.07\times 10^{-14}$ | $1.42\times 10^{-14}$ | 27.37 ns (0.66 ns) | 619.25 ns (12.67 ns) | **22.63×** |
| `european-bsm-itm-call` | `european_bsm` | `AnalyticEuropeanEngine` | 23.9825202131 | $0.00$ | $0.00$ | 35.21 ns (0.56 ns) | 619.96 ns (5.97 ns) | **17.61×** |
| `european-bsm-otm-put` | `european_bsm` | `AnalyticEuropeanEngine` | 3.26238340389 | $8.88\times 10^{-16}$ | $6.22\times 10^{-15}$ | 35.50 ns (0.57 ns) | 620.86 ns (15.66 ns) | **17.49×** |
| `digital-bsm-cash-call` | `digital_bsm` | `AnalyticDigitalEngine` | 4.99551713655 | $0.00$ | $1.78\times 10^{-15}$ | 27.77 ns (1.01 ns) | 623.48 ns (24.37 ns) | **22.45×** |
| `digital-bsm-asset-put` | `digital_bsm` | `AnalyticDigitalEngine` | 34.2714509893 | $0.00$ | $1.42\times 10^{-14}$ | 35.56 ns (2.13 ns) | 621.81 ns (8.02 ns) | **17.49×** |
| `geometric-asian-bsm-call` | `geometric_asian_bsm` | `AnalyticGeometricAveragePriceEngine` | 5.03586754652 | $7.11\times 10^{-15}$ | $6.22\times 10^{-15}$ | 56.74 ns (1.50 ns) | 401.84 ns (13.38 ns) | **7.08×** |
| `geometric-asian-bsm-put` | `geometric_asian_bsm` | `AnalyticGeometricAveragePriceEngine` | 2.35569361785 | $2.66\times 10^{-15}$ | $8.88\times 10^{-15}$ | 55.94 ns (0.91 ns) | 403.51 ns (9.46 ns) | **7.21×** |
| `arithmetic-asian-bsm-call` | `arithmetic_asian_bsm` | `TurnbullWakemanArithmeticAveragePriceEngine` | 5.24650186036 | $3.38\times 10^{-14}$ | $7.43\times 10^{-12}$ | 73.24 ns (3.46 ns) | 313.93 ns (17.54 ns) | **4.29×** |
| `arithmetic-asian-bsm-put` | `arithmetic_asian_bsm` | `TurnbullWakemanArithmeticAveragePriceEngine` | 2.27632052827 | $3.42\times 10^{-14}$ | $6.74\times 10^{-12}$ | 71.49 ns (0.85 ns) | 314.81 ns (10.83 ns) | **4.40×** |
| `barrier-down-out-call-rebate` | `single_barrier_bsm` | `AnalyticBarrierEngine` | 9.71405147606 | $5.33\times 10^{-15}$ | $1.78\times 10^{-15}$ | 161.00 ns (8.92 ns) | 1.17 $\mu\text{s}$ (85.44 ns) | **7.30×** |
| `barrier-up-in-put-rebate` | `single_barrier_bsm` | `AnalyticBarrierEngine` | 1.42695867059 | $2.22\times 10^{-16}$ | $3.33\times 10^{-15}$ | 120.18 ns (2.50 ns) | 1.16 $\mu\text{s}$ (42.87 ns) | **9.65×** |
| `binary-down-out-cash-call` | `binary_barrier_bsm` | `AnalyticBinaryBarrierEngine` | 4.87026073135 | $1.78\times 10^{-15}$ | $8.88\times 10^{-16}$ | 76.20 ns (1.16 ns) | 274.60 ns (7.91 ns) | **3.60×** |
| `binary-up-in-asset-put` | `binary_barrier_bsm` | `AnalyticBinaryBarrierEngine` | 2.97920242858 | $4.44\times 10^{-16}$ | $4.44\times 10^{-16}$ | 73.22 ns (2.22 ns) | 279.17 ns (15.89 ns) | **3.81×** |
| `touch-up-in-cash-hit` | `touch_bsm` | `AnalyticBinaryBarrierEngine` | 3.71214659048 | $2.22\times 10^{-15}$ | $1.78\times 10^{-15}$ | 52.02 ns (2.91 ns) | 281.02 ns (11.82 ns) | **5.40×** |
| `touch-up-in-cash-expiry` | `touch_bsm` | `AnalyticBinaryBarrierEngine` | 3.63775609357 | $8.88\times 10^{-16}$ | $1.33\times 10^{-15}$ | 61.55 ns (2.23 ns) | 253.99 ns (6.21 ns) | **4.13×** |
| `touch-up-out-cash-expiry` | `touch_bsm` | `AnalyticBinaryBarrierEngine` | 5.97013829796 | $0.00$ | $2.66\times 10^{-15}$ | 82.25 ns (0.85 ns) | 254.42 ns (6.63 ns) | **3.09×** |
| `touch-up-in-asset-hit` | `touch_bsm` | `AnalyticBinaryBarrierEngine` | 44.5457590858 | $1.42\times 10^{-14}$ | $2.13\times 10^{-14}$ | 51.44 ns (1.59 ns) | 276.07 ns (3.23 ns) | **5.37×** |
| `touch-up-in-asset-expiry` | `touch_bsm` | `AnalyticBinaryBarrierEngine` | 44.3204945036 | $3.55\times 10^{-14}$ | $1.42\times 10^{-14}$ | 62.16 ns (0.97 ns) | 253.07 ns (3.43 ns) | **4.07×** |
| `touch-up-out-asset-expiry` | `touch_bsm` | `AnalyticBinaryBarrierEngine` | 54.6844888713 | $0.00$ | $1.42\times 10^{-14}$ | 82.05 ns (2.12 ns) | 254.61 ns (5.17 ns) | **3.10×** |
| `double-barrier-out-call` | `double_barrier_bsm` | `AnalyticDoubleBarrierEngine` | 1.08388145926 | $3.40\times 10^{-14}$ | $4.77\times 10^{-14}$ | 1.70 $\mu\text{s}$ (24.75 ns) | 7.83 $\mu\text{s}$ (273.00 ns) | **4.62×** |
| `double-barrier-in-put` | `double_barrier_bsm` | `AnalyticDoubleBarrierEngine` | 4.81765548074 | $3.38\times 10^{-14}$ | $2.22\times 10^{-14}$ | 1.63 $\mu\text{s}$ (31.96 ns) | 8.24 $\mu\text{s}$ (208.93 ns) | **5.05×** |
| `double-touch-in-cash-expiry` | `double_touch_bsm` | `AnalyticDoubleTouchEngine` | 5.99318208860 | $8.88\times 10^{-16}$ | $8.88\times 10^{-16}$ | 832.52 ns (56.77 ns) | 1.81 $\mu\text{s}$ (66.39 ns) | **2.17×** |
| `double-touch-out-cash-expiry` | `double_touch_bsm` | `AnalyticDoubleTouchEngine` | 3.61471230292 | $8.88\times 10^{-16}$ | $4.44\times 10^{-16}$ | 833.73 ns (38.99 ns) | 1.78 $\mu\text{s}$ (46.30 ns) | **2.13×** |

**技术要点**：

- 欧式与数字期权的中位数延迟为 Kiyosi $27.37\text{–}35.56\ \text{ns}$、QuantLib $619.25\text{–}623.48\ \text{ns}$，加速比为 **17.49×–22.63×**。Kiyosi 的 `price()` 返回价格标量，QuantLib 的 `AnalyticEuropeanEngine` 在 `recalculate()` 中也计算 Greeks。QuantLib 的到期型单触碰和双触碰引擎仅计算价格，对应场景的加速比分别为 **3.09×–4.13×** 和 **2.13×–2.17×**。
- Kiyosi 的双障碍与双触碰引擎在吸收镜像级数与谱级数之间自适应选择（内部上限分别为 64 项和 256 项）。QuantLib 双障碍使用 `series = 5`，双触碰采用最多 99 项的 Hui 级数，末项阈值为 $10^{-8}$。这些场景的加速比为 **2.13×–5.05×**，两端的绝对误差范围约为 $10^{-16}\text{–}10^{-14}$。

---

### 3.2 数值积分与 CRR 二叉树引擎（6 个场景）

| 场景 ID | 引擎 (`engine`) | 配置对比（Kiyosi vs QuantLib） | 误差预算 | Kiyosi 绝对误差 | QuantLib 绝对误差 | Kiyosi 中位数 (IQR) | QuantLib 中位数 (IQR) | 加速比 ($Q/K$) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `quadrature-bsm-european-call` | `QuadratureVanillaEngine` | 512 步复合 Simpson（行权价分段） vs 5000 步固定梯形法则 | $1.0\times 10^{-5}$ | $8.30\times 10^{-9}$ | $5.05\times 10^{-6}$ | 5.03 $\mu\text{s}$ (0.09 $\mu\text{s}$) | 30.89 $\mu\text{s}$ (0.28 $\mu\text{s}$) | **6.14×** |
| `quadrature-bsm-cash-call` | `QuadratureDigitalEngine` | 512 步复合 Simpson（行权价分段） vs 5000 步固定梯形法则 | $2.0\times 10^{-2}$ | $6.77\times 10^{-10}$ | $1.73\times 10^{-3}$ | 1.97 $\mu\text{s}$ (0.08 $\mu\text{s}$) | 31.63 $\mu\text{s}$ (0.86 $\mu\text{s}$) | **16.02×** |
| `quadrature-bsm-asset-put` | `QuadratureDigitalEngine` | 512 步复合 Simpson（行权价分段） vs 5000 步固定梯形法则 | $2.0\times 10^{-1}$ | $1.34\times 10^{-8}$ | $1.82\times 10^{-2}$ | 1.99 $\mu\text{s}$ (0.11 $\mu\text{s}$) | 30.78 $\mu\text{s}$ (0.36 $\mu\text{s}$) | **15.48×** |
| `crr-bsm-european-call` | `CoxRossRubinsteinVanillaEngine` | `step_count = 512` vs `step_count = 512` | $5.0\times 10^{-3}$ | $3.80\times 10^{-3}$ | $3.83\times 10^{-3}$ | 8.16 $\mu\text{s}$ (0.05 $\mu\text{s}$) | 64.93 $\mu\text{s}$ (1.75 $\mu\text{s}$) | **7.95×** |
| `crr-bsm-american-put` | `CoxRossRubinsteinVanillaEngine` | `step_count = 512` vs `step_count = 512` | $5.0\times 10^{-3}$ | $1.82\times 10^{-3}$ | $1.80\times 10^{-3}$ | 105.72 $\mu\text{s}$ (2.59 $\mu\text{s}$) | 549.15 $\mu\text{s}$ (5.98 $\mu\text{s}$) | **5.19×** |
| `crr-bsm-down-out-call` | `CoxRossRubinsteinBarrierEngine` | `step_count = 2048` vs `step_count = 2048`（纯离散树） | $2.0\times 10^{-2}$ | $5.19\times 10^{-3}$ | $5.18\times 10^{-3}$ | 3.01 ms (0.02 ms) | 5.86 ms (0.07 ms) | **1.95×** |

**技术要点**：

- Kiyosi 在数字期权的行权价处切分积分区间，使用 512 步复合 Simpson 法（$\pm 8\sigma$）。两个场景的绝对误差分别为 $6.77\times 10^{-10}$ 和 $1.34\times 10^{-8}$。QuantLib `IntegralEngine` 使用 5000 区间的固定梯形法，对应误差为 $1.73\times 10^{-3}$ 和 $1.82\times 10^{-2}$。Kiyosi 在这两个场景的加速比为 **15.48×–16.02×**。
- CRR 二叉树采用相同的 512 或 2048 个时间步。双端绝对误差接近，Kiyosi 的加速比为 **1.95×–7.95×**。

---

### 3.3 一维有限差分引擎：BSM 与局部波动率（22 个场景）

涵盖 BSM（`fd_bsm`，11 个场景，误差预算 $3.0\times 10^{-3}$）与外部给定的非恒定局部波动率曲面（`fd_local_vol`，11 个场景，误差预算 $5.0\times 10^{-3}$）。局部波动率曲面在时间（`2025-01-01` 至 `2026-01-01`，Act/365F）与现货（$[80,120]$，节点矩阵 `[[0.30, 0.15], [0.35, 0.20]]`）上作双线性插值，现货超出区间时取相应端点值。

- Kiyosi 在 22 个场景中均使用 `space = 800`、`time = 400` 和 Rannacher 格式（前两个时间步采用隐式 Euler 半步阻尼）。两个普通欧式场景自动选择求解域，并在行权价附近加密节点。其余场景显式设置 `upper = 400`。
- QuantLib 使用 `space = 800` 的自动对数网格与 Crank–Nicolson 格式（`damping = 2`）。局部波动率场景的 `mesher_vol = 0.5` 用于网格定界。两组模型各有 9 个场景使用 400 个时间步。为满足共同误差预算，向上现金单触碰（`up-one-touch-cash-hit`）使用 1600 步，向上资产不触碰（`up-no-touch-asset-expiry`）使用 16000 步。

#### 3.3.1 BSM 一维有限差分（`fd_bsm`，误差预算 $3.0\times 10^{-3}$）

| 场景 ID | Kiyosi 引擎 | 时间步（K / Q） | 参考价格 | Kiyosi 绝对误差 | QuantLib 绝对误差 | Kiyosi 中位数 (IQR) | QuantLib 中位数 (IQR) | 加速比 ($Q/K$) |
| --- | --- | :---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `fd-bsm-european-call` | `FiniteDifferenceVanillaEngine` | 400 / 400 | 9.22700550815 | $8.64\times 10^{-5}$ | $7.08\times 10^{-5}$ | 2.10 ms (0.05 ms) | 6.19 ms (0.29 ms) | **2.94×** |
| `fd-bsm-american-put` | `FiniteDifferenceVanillaEngine` | 400 / 400 | 6.66068454589 | $1.20\times 10^{-3}$ | $1.20\times 10^{-3}$ | 2.24 ms (0.15 ms) | 7.94 ms (0.33 ms) | **3.55×** |
| `fd-bsm-cash-digital-call` | `FiniteDifferenceDigitalEngine` | 400 / 400 | 4.94581091053 | $4.45\times 10^{-5}$ | $6.84\times 10^{-5}$ | 2.09 ms (0.14 ms) | 6.10 ms (0.34 ms) | **2.92×** |
| `fd-bsm-asset-digital-put` | `FiniteDifferenceDigitalEngine` | 400 / 400 | 48.7733863768 | $1.42\times 10^{-4}$ | $8.01\times 10^{-4}$ | 2.09 ms (0.12 ms) | 6.08 ms (0.26 ms) | **2.91×** |
| `fd-bsm-down-out-call` | `FiniteDifferenceBarrierEngine` | 400 / 400 | 9.13330643650 | $8.87\times 10^{-5}$ | $1.61\times 10^{-6}$ | 2.11 ms (0.04 ms) | 6.19 ms (0.17 ms) | **2.94×** |
| `fd-bsm-terminal-down-out-cash` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 400 | 4.82180082739 | $3.57\times 10^{-5}$ | $1.47\times 10^{-4}$ | 2.10 ms (0.03 ms) | 6.13 ms (0.10 ms) | **2.93×** |
| `fd-bsm-terminal-up-in-asset` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 400 | 2.94955886912 | $1.04\times 10^{-5}$ | $5.60\times 10^{-5}$ | 4.16 ms (0.17 ms) | 13.68 ms (0.71 ms) | **3.29×** |
| `fd-bsm-down-no-touch-cash-expiry` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 400 | 7.13408843096 | $8.33\times 10^{-5}$ | $1.49\times 10^{-4}$ | 2.08 ms (0.08 ms) | 6.11 ms (0.12 ms) | **2.93×** |
| `fd-bsm-down-one-touch-asset-hit` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 400 | 19.4492167646 | $7.73\times 10^{-4}$ | $1.82\times 10^{-3}$ | 2.08 ms (0.02 ms) | 6.11 ms (0.17 ms) | **2.94×** |
| `fd-bsm-up-one-touch-cash-hit` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 1600 | 3.69391182061 | $1.15\times 10^{-5}$ | $1.48\times 10^{-3}$ | 2.09 ms (0.04 ms) | 23.45 ms (0.94 ms) | **11.24×** |
| `fd-bsm-up-no-touch-asset-expiry` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 16000 | 54.1403691157 | $1.43\times 10^{-4}$ | $1.77\times 10^{-3}$ | 2.08 ms (0.08 ms) | 235.04 ms (4.15 ms) | **113.18×** |

#### 3.3.2 局部波动率一维有限差分（`fd_local_vol`，误差预算 $5.0\times 10^{-3}$）

| 场景 ID | Kiyosi 引擎 | 时间步（K / Q） | 参考价格 | Kiyosi 绝对误差 | QuantLib 绝对误差 | Kiyosi 中位数 (IQR) | QuantLib 中位数 (IQR) | 加速比 ($Q/K$) |
| --- | --- | :---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `fd-local-vol-european-call` | `FiniteDifferenceVanillaEngine` | 400 / 400 | 11.0017427062 | $1.03\times 10^{-4}$ | $1.02\times 10^{-4}$ | 6.62 ms (0.18 ms) | 13.55 ms (0.62 ms) | **2.05×** |
| `fd-local-vol-american-put` | `FiniteDifferenceVanillaEngine` | 400 / 400 | 8.36106642823 | $1.12\times 10^{-3}$ | $1.24\times 10^{-3}$ | 12.25 ms (0.28 ms) | 15.62 ms (1.09 ms) | **1.27×** |
| `fd-local-vol-cash-digital-call` | `FiniteDifferenceDigitalEngine` | 400 / 400 | 5.39093949985 | $1.23\times 10^{-5}$ | $1.22\times 10^{-4}$ | 6.71 ms (0.17 ms) | 13.63 ms (0.57 ms) | **2.03×** |
| `fd-local-vol-asset-digital-put` | `FiniteDifferenceDigitalEngine` | 400 / 400 | 40.5303971416 | $5.96\times 10^{-4}$ | $1.95\times 10^{-3}$ | 6.61 ms (0.14 ms) | 13.63 ms (0.49 ms) | **2.06×** |
| `fd-local-vol-down-out-call` | `FiniteDifferenceBarrierEngine` | 400 / 400 | 10.3817423850 | $1.04\times 10^{-4}$ | $1.40\times 10^{-4}$ | 6.60 ms (0.19 ms) | 13.65 ms (0.19 ms) | **2.07×** |
| `fd-local-vol-terminal-down-out-cash` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 400 | 4.83462680702 | $2.12\times 10^{-6}$ | $2.48\times 10^{-4}$ | 6.68 ms (0.40 ms) | 14.44 ms (1.19 ms) | **2.16×** |
| `fd-local-vol-terminal-up-in-asset` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 400 | 3.48032683172 | $3.67\times 10^{-5}$ | $1.48\times 10^{-5}$ | 13.18 ms (0.74 ms) | 31.35 ms (2.60 ms) | **2.38×** |
| `fd-local-vol-down-no-touch-cash-expiry` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 400 | 5.90771262187 | $3.29\times 10^{-5}$ | $2.35\times 10^{-4}$ | 6.71 ms (0.29 ms) | 14.01 ms (0.91 ms) | **2.09×** |
| `fd-local-vol-down-one-touch-asset-hit` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 400 | 29.6031381560 | $2.33\times 10^{-4}$ | $1.03\times 10^{-3}$ | 6.60 ms (0.17 ms) | 13.96 ms (0.76 ms) | **2.11×** |
| `fd-local-vol-up-one-touch-cash-hit` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 1600 | 4.51261775417 | $1.55\times 10^{-5}$ | $1.83\times 10^{-3}$ | 6.65 ms (0.51 ms) | 53.77 ms (2.51 ms) | **8.09×** |
| `fd-local-vol-up-no-touch-asset-expiry` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 16000 | 44.3991225309 | $1.94\times 10^{-4}$ | $2.04\times 10^{-3}$ | 6.83 ms (0.45 ms) | 535.71 ms (4.85 ms) | **78.43×** |

**技术要点**：

- 在两组模型各自的 9 个 $800\times 400$ 场景中，Kiyosi 的中位数延迟范围为 BSM **2.08–4.16 ms**、局部波动率 **6.60–13.18 ms**，几何平均加速比分别为 **3.03×** 和 **2.00×**。两端的网格坐标、节点分布和时间推进方式均有差异。
- 向上触碰与不触碰场景中，Kiyosi 使用 400 个时间步，绝对误差约为 $10^{-5}\text{–}10^{-4}$。在满足同一误差预算的配置下，现金单触碰场景的加速比为 BSM **11.24×**、局部波动率 **8.09×**，资产不触碰场景分别为 **113.18×** 和 **78.43×**。

---

### 3.4 Heston 随机波动率引擎（3 个场景）

共用市场与模型参数：$S = K = 100,\ r = 0.05,\ q = 0.02,\ v_0 = \theta = 0.04,\ \kappa = 1.5,\ \xi = 0.3,\ \rho = -0.7$，期限 1 年（`2025-01-01` 至 `2026-01-01`）。

| 场景 ID | 引擎 (`engine`) | 算法与配置对比（Kiyosi vs QuantLib） | 误差预算 | Kiyosi 绝对误差 | QuantLib 绝对误差 | Kiyosi 中位数 (IQR) | QuantLib 中位数 (IQR) | 加速比 ($Q/K$) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `heston-analytic-call` | `AnalyticHestonEuropeanEngine` | 自适应 Fourier + 确定性方差控制变量（$\text{tol}=10^{-9}$） vs Gatheral 自适应 Lobatto（$\text{rel\_tol}=10^{-9}$） | $1.0\times 10^{-7}$ | $2.31\times 10^{-14}$ | $1.95\times 10^{-14}$ | 57.83 $\mu\text{s}$ (1.03 $\mu\text{s}$) | 66.90 $\mu\text{s}$ (2.70 $\mu\text{s}$) | **1.16×** |
| `heston-fd-european-call` | `FiniteDifferenceHestonVanillaEngine` | MCS ADI ($\theta=1/3$), $200\times 50\times 200$ 区间 vs Hundsdorfer ADI, $200\times 100\times 200$ 节点 | $5.0\times 10^{-3}$ | $4.89\times 10^{-4}$ | $9.05\times 10^{-4}$ | 95.15 ms (2.21 ms) | 210.92 ms (4.88 ms) | **2.22×** |
| `heston-fd-american-put` | `FiniteDifferenceHestonVanillaEngine` | MCS ADI + Ikonen–Toivanen 分裂, $200\times 50\times 200$ vs Hundsdorfer + 投影, $200\times 100\times 200$ | $5.0\times 10^{-3}$ | $1.12\times 10^{-3}$ | $3.54\times 10^{-3}$ | 91.62 ms (3.08 ms) | 231.48 ms (2.83 ms) | **2.53×** |

**技术要点**：

- Heston 欧式场景的参考值由 Gatheral–Lobatto 与独立 exp-sinh Fourier 积分交叉校验，参考不确定度为 $10^{-11}$。两个被测解析引擎相对该参考值的绝对误差均约为 $2\times 10^{-14}$。
- Heston 二维有限差分中，Kiyosi 在 $[0,400]\times[0,0.6]$ 上使用 Modified Craig–Sneyd ADI 格式（$\theta=1/3$），美式行权采用 Ikonen–Toivanen 算子分裂。QuantLib 使用自动求解域、Hundsdorfer 格式与原生美式收益投影。所测配置下，Kiyosi 在欧式和美式场景中的绝对误差均更小，加速比分别为 **2.22×** 和 **2.53×**。

---

### 3.5 BSM 蒙特卡洛引擎（5 个场景）

全部场景采用单线程伪随机抽样，关闭对偶变量（`antithetic = false`）与控制变量（`control_variate = false`）。Kiyosi 使用块流式 PCG32 + Box–Muller；QuantLib 使用 MT19937 + 逆正态分布。除计时种子 `seed = 1729` 外，双方均在 32 个预设验证种子（$1009 + 97i,\ i=0\dots 31$）上检验样本统计量。

#### 3.5.1 计时种子精度与延迟表现（`seed = 1729`）

| 场景 ID | 引擎 (`engine`) | 物理路径数（K / Q） | 误差预算 | 参考价格 | Kiyosi 计时误差 | QuantLib 计时误差 | Kiyosi 中位数 (IQR) | QuantLib 中位数 (IQR) | 加速比 ($Q/K$) |
| --- | --- | :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `mc-european-call` | `MonteCarloVanillaEngine` | 131,072 / 262,144 | $0.10$ | 9.22700550815 | $6.38\times 10^{-2}$ | $3.14\times 10^{-2}$ | 2.44 ms (0.08 ms) | 31.65 ms (1.46 ms) | **12.99×** |
| `mc-european-put` | `MonteCarloVanillaEngine` | 65,536 / 65,536 | $0.10$ | 6.33008062755 | $1.58\times 10^{-2}$ | $4.47\times 10^{-2}$ | 1.10 ms (0.05 ms) | 7.82 ms (0.22 ms) | **7.11×** |
| `mc-barrier-down-out-call` | `MonteCarloBarrierEngine` | 65,536 / 131,072 | $0.10$ | 7.58695396974 | $9.38\times 10^{-2}$ | $3.13\times 10^{-2}$ | 3.29 ms (0.03 ms) | 20.64 ms (1.14 ms) | **6.28×** |
| `mc-barrier-up-in-put` | `MonteCarloBarrierEngine` | 65,536 / 65,536 | $0.10$ | 0.23061330871 | $2.17\times 10^{-3}$ | $3.01\times 10^{-5}$ | 3.50 ms (0.24 ms) | 10.20 ms (0.67 ms) | **2.91×** |
| `mc-american-put` | `MonteCarloVanillaEngine` | 65,536 / 65,536 (+32,768 校准) | $0.15$ | 6.66068454589 | $3.18\times 10^{-3}$ | $5.58\times 10^{-2}$ | 136.92 ms (1.68 ms) | 662.51 ms (10.47 ms) | **4.84×** |

#### 3.5.2 32 种子集合验证统计量（Seed Ensemble Validation）

| 场景 ID | 门禁上限（RMSE / \|Bias\| / StdDev） | Kiyosi RMSE | QuantLib RMSE | Kiyosi 有符号偏差 | QuantLib 有符号偏差 | Kiyosi 样本标准差 (SE) | QuantLib 样本标准差 (SE) | 最大绝对误差（K / Q） |
| --- | :---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `mc-european-call` | $0.05$ / $0.025$ / $0.05$ | $3.11\times 10^{-2}$ | $2.88\times 10^{-2}$ | $+2.85\times 10^{-3}$ | $-2.53\times 10^{-3}$ | $3.14\times 10^{-2}$ ($5.56\times 10^{-3}$) | $2.92\times 10^{-2}$ ($5.16\times 10^{-3}$) | $8.39\times 10^{-2}$ / $6.07\times 10^{-2}$ |
| `mc-european-put` | $0.05$ / $0.025$ / $0.05$ | $2.70\times 10^{-2}$ | $3.52\times 10^{-2}$ | $-3.28\times 10^{-3}$ | $+1.85\times 10^{-2}$ | $2.72\times 10^{-2}$ ($4.81\times 10^{-3}$) | $3.04\times 10^{-2}$ ($5.37\times 10^{-3}$) | $4.49\times 10^{-2}$ / $8.08\times 10^{-2}$ |
| `mc-barrier-down-out-call` | $0.05$ / $0.025$ / $0.05$ | $3.45\times 10^{-2}$ | $3.66\times 10^{-2}$ | $+1.13\times 10^{-3}$ | $-7.45\times 10^{-3}$ | $3.51\times 10^{-2}$ ($6.20\times 10^{-3}$) | $3.64\times 10^{-2}$ ($6.43\times 10^{-3}$) | $6.64\times 10^{-2}$ / $9.87\times 10^{-2}$ |
| `mc-barrier-up-in-put` | $0.05$ / $0.025$ / $0.05$ | $1.08\times 10^{-3}$ | $7.32\times 10^{-3}$ | $-5.32\times 10^{-5}$ | $+5.01\times 10^{-3}$ | $1.09\times 10^{-3}$ ($1.93\times 10^{-4}$) | $5.41\times 10^{-3}$ ($9.57\times 10^{-4}$) | $2.66\times 10^{-3}$ / $1.41\times 10^{-2}$ |
| `mc-american-put` | $0.075$ / $0.05$ / $0.075$ | $4.05\times 10^{-2}$ | $4.02\times 10^{-2}$ | $-2.41\times 10^{-2}$ | $-2.54\times 10^{-2}$ | $3.31\times 10^{-2}$ ($5.84\times 10^{-3}$) | $3.16\times 10^{-2}$ ($5.58\times 10^{-3}$) | $7.95\times 10^{-2}$ / $9.57\times 10^{-2}$ |

**技术要点**：

- Kiyosi 直接计算布朗桥条件存活概率，QuantLib `MCBarrierEngine` 用固定种子（`seed = 5`）的辅助随机流抽样障碍穿越。在 `mc-barrier-up-in-put` 中，双方均用 65,536 条路径，Kiyosi 的加速比为 **2.91×**，32 种子 RMSE 分别为 Kiyosi $1.08\times 10^{-3}$、QuantLib $7.32\times 10^{-3}$。在 `mc-barrier-down-out-call` 中，Kiyosi 用 65,536 条路径得到 RMSE $0.0345$，QuantLib 用 131,072 条路径得到 RMSE $0.0366$，加速比为 **6.28×**。
- **美式最小二乘蒙特卡洛（LSM）**：在 `mc-american-put`（65,536 条定价路径、50 个行权时间步、二次单项式基）中，Kiyosi 在实值（ITM）定价路径上直接做样本内回归拟合（基函数 $1, S/K, (S/K)^2$），而 QuantLib 在每次 `recalculate()` 中先独立模拟 32,768 条校准路径再模拟 65,536 条定价路径。根据 `report.json` 记录的 LSM 细化实验（`lsm_refinement`）：
  - 将定价路径翻倍至 $131{,}072$ 时，Kiyosi 与 QuantLib 的 32 种子 RMSE 分别降至 $0.0332$ 与 $0.0315$；
  - 在 $131{,}072$ 路径下将行权步从 50 加密至 100，Kiyosi 与 QuantLib 的种子均值变化仅为 $-0.00141$（$\text{SE}=0.00340$）与 $+0.00075$（$\text{SE}=0.00297$）；
  - 将 QuantLib 校准路径从 $32{,}768$ 翻倍至 $65{,}536$ 时，均值变化仅 $+4.56\times 10^{-5}$（$\text{SE}=7.16\times 10^{-4}$）。
  基线配置的 32 种子 RMSE 为 Kiyosi $0.0405$、QuantLib $0.0402$，中位数延迟分别为 $136.92\ \text{ms}$ 和 $662.51\ \text{ms}$，加速比为 **4.84×**。

---

## 4. 覆盖范围、局限与解读说明

1. **严格语义对齐与排除边界**：
   本基准覆盖 **20 类引擎（51 个语义单元）**，每类都能在相同合约条款、市场模型与算法类别下使用 QuantLib 原生引擎进行对照。Kiyosi 其余 14 类引擎因缺乏直接等价的 QuantLib 原生实现而未纳入对比，包括：
   - 近似公式版本不同：`BjerksundStenslandVanillaEngine`（Kiyosi 实现 2002 版，QuantLib 为 1993 版）；
   - 结构化奇异产品无内置对应引擎：自动赎回（`Autocallable`）、累购累沽（`Accumulator`）的积分、有限差分与蒙特卡洛引擎，以及区间累计解析引擎（`AnalyticRangeAccrualEngine`）；
   - 离散／连续监控或算法语义差异：数字期权与连续平均亚式蒙特卡洛、双障碍／双触碰有限差分、障碍期权数值积分及数字期权 CRR 二叉树。
2. **加速比解读注意事项**：
   - CRR 二叉树的步数、18 个一维有限差分场景的空间规模与时间步数，以及 2 个蒙特卡洛场景的定价与校准路径数，在双端均相同。`fd-bsm-up-no-touch-asset-expiry`（**113.18×**）、`fd-local-vol-up-no-touch-asset-expiry`（**78.43×**）和 `mc-european-call`（**12.99×**）的加速比包含通过共同精度门禁所用的时间步数或路径数差异。
   - **接口固有附加计算**：QuantLib 原生 `recalculate()` 在部分解析引擎和有限差分引擎中会同步计算灵敏度指标，在蒙特卡洛中会累计样本方差；Kiyosi 的 `price()` 仅计算价格标量（Greeks 由 `price_with_greeks()` 按需调用）。
   - **单核基准**：所有测量均固定 `workers = 1`，反映单核指令与内存布局效率，不包含 Kiyosi 蒙特卡洛引擎在多线程 Rayon 池下的并行扩展加速。
