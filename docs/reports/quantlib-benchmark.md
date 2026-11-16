---
description: 基于 59 个原生评测场景、51 个语义单元与 20 类定价引擎的 Kiyosi 0.19.0 与 QuantLib C++ 1.44 精度与延迟对比分析。
---

# Kiyosi vs QuantLib 基准测试分析报告

> **适用版本**：Kiyosi `0.19.0`（提交 `32613360`） vs QuantLib C++ `1.44`（`libQuantLib.so.1.44.0`）
> **评测时间**：2026-11-16 01:38:47 UTC（总墙钟耗时 358.72 s）
> **数据来源**：`benchmarks/quantlib/report.json`（Schema v1，状态 `passed`）

---

## 1. 执行摘要

本报告基于 `benchmarks/quantlib/report.json` 的实测数据，评估 Kiyosi（Rust 原生核心）与 QuantLib C++ 1.44 在衍生品定价精度与单线程执行延迟上的表现。测试覆盖 **20 类合格定价引擎**、**51 个必测语义单元（Semantic Cells）** 及 **59 个评测场景**。所有场景均以独立高精度参考解设置先验误差预算（Error Budget），仅当双端同时通过精度门禁后才计入延迟对比。

### 核心结论

- **100% 通过精度门禁**：全部 59 个场景均通过先验误差预算校验（$|\text{Price} - \text{Reference}| + u_{\text{ref}} \le \text{Budget}$）；5 个蒙特卡洛场景在 32 组独立验证种子（$1009 + 97i,\ i=0\dots 31$）下同时通过均方根误差（RMSE）、有符号偏差（Signed Bias）与样本标准差门禁。
- **整体延迟优势显著**：定义加速比为 $Q / K = \text{Median}(\text{QuantLib}) / \text{Median}(\text{Kiyosi})$。在全部 59 个场景中，Kiyosi 取得 **5.05× 的几何平均加速比**与 **4.26× 的中位数加速比**（区间 **0.91× – 113.35×**），在 **58 / 59** 个场景中延迟低于 QuantLib。
- **唯一低于 1.0× 的场景**：Heston 欧式看涨解析积分（`heston-analytic-call`）中，Kiyosi 耗时 $72.59\ \mu\text{s}$，QuantLib 耗时 $66.23\ \mu\text{s}$（比值 **0.91×**），两者绝对误差均在 $2\times 10^{-14}$ 量级。
- **同等网格／路径下的纯粹算子性能**：剔除因精度门禁导致网格或路径配置不同的场景后，Kiyosi 在 BSM 解析引擎上快 **2.20× – 24.83×**（几何平均 **6.95×**），在同网格一维有限差分上快 **2.88× – 3.68×**（BSM，几何平均 **3.04×**）与 **1.29× – 2.31×**（局部波动率，几何平均 **1.98×**），在同路径欧式／障碍蒙特卡洛上快 **2.95× – 5.54×**。

### 分模块汇总

| 算法类别 | 场景数 | 误差预算 | 最大绝对误差（Kiyosi / QuantLib） | 中位数延迟范围（Kiyosi vs QuantLib） | 几何平均加速比 | 中位数加速比 | 加速比区间（$Q/K$） |
| --- | ---: | ---: | --- | --- | ---: | ---: | --- |
| BSM 解析法 | 23 | $1.0\times 10^{-9}$ | $4.97\times 10^{-14}$ / $7.43\times 10^{-12}$ | $24.88\ \text{ns} - 1.67\ \mu\text{s}$ vs $255.76\ \text{ns} - 8.31\ \mu\text{s}$ | **6.95×** | 5.03× | 2.20× – 24.83× |
| Heston 解析积分 | 1 | $1.0\times 10^{-7}$ | $2.31\times 10^{-14}$ / $1.95\times 10^{-14}$ | $72.59\ \mu\text{s}$ vs $66.23\ \mu\text{s}$ | **0.91×** | 0.91× | 0.91× |
| BSM 数值积分 | 3 | $10^{-5} - 0.2$ | $1.34\times 10^{-8}$ / $1.82\times 10^{-2}$ | $1.96\ \mu\text{s} - 9.21\ \mu\text{s}$ vs $30.66\ \mu\text{s} - 31.58\ \mu\text{s}$ | **9.44×** | 15.51× | 3.36× – 16.13× |
| CRR 二叉树 | 3 | $5\times 10^{-3} - 2\times 10^{-2}$ | $5.19\times 10^{-3}$ / $5.18\times 10^{-3}$ | $8.35\ \mu\text{s} - 3.58\ \text{ms}$ vs $64.96\ \mu\text{s} - 5.85\ \text{ms}$ | **4.00×** | 5.05× | 1.64× – 7.78× |
| 一维有限差分（BSM） | 11 | $3.0\times 10^{-3}$ | $1.20\times 10^{-3}$ / $1.82\times 10^{-3}$ | $2.05\ \text{ms} - 4.23\ \text{ms}$ vs $6.10\ \text{ms} - 234.47\ \text{ms}$ | **4.75×** | 2.97× | 2.88× – 113.35× |
| 一维有限差分（局部波动率） | 11 | $5.0\times 10^{-3}$ | $1.12\times 10^{-3}$ / $2.04\times 10^{-3}$ | $6.58\ \text{ms} - 13.10\ \text{ms}$ vs $13.47\ \text{ms} - 531.72\ \text{ms}$ | **3.15×** | 2.06× | 1.29× – 79.71× |
| 二维有限差分（Heston） | 2 | $5.0\times 10^{-3}$ | $1.12\times 10^{-3}$ / $3.54\times 10^{-3}$ | $94.08\ \text{ms} - 96.09\ \text{ms}$ vs $212.05\ \text{ms} - 233.22\ \text{ms}$ | **2.34×** | 2.34× | 2.21× – 2.48× |
| BSM 蒙特卡洛 | 5 | $0.10 - 0.15$ | $9.38\times 10^{-2}$ / $5.58\times 10^{-2}$ | $1.40\ \text{ms} - 135.71\ \text{ms}$ vs $7.73\ \text{ms} - 664.45\ \text{ms}$ | **5.62×** | 5.54× | 2.95× – 11.37× |
| **全部场景合计** | **59** | — | — | $24.88\ \text{ns} - 135.71\ \text{ms}$ vs $255.76\ \text{ns} - 664.45\ \text{ms}$ | **5.05×** | **4.26×** | **0.91× – 113.35×** |

---

## 2. 测试环境与评测协议

### 2.1 硬件与编译工具链

| 维度 | 配置详情 |
| --- | --- |
| 操作系统 | `Linux-6.18.58.1-microsoft-standard-WSL2-x86_64-with-glibc2.43` |
| 处理器 | Intel(R) Core(TM) Ultra 9 285（24 核 24 线程，L1d 1.1 MiB / L1i 1.5 MiB / L2 72 MiB / L3 36 MiB） |
| 并发限制 | 单工作线程（`workers_per_backend = 1`），无多线程并行加速 |
| Kiyosi 编译 | `rustc 1.99.1 (58cf8f9c3 2026-10-13)`，`cargo build --release --locked -p kiyosi --example quantlib_bench`（Cargo release，thin LTO，`RUSTFLAGS` 未额外指定） |
| QuantLib 编译 | `c++ (Ubuntu 15.2.0-16ubuntu1) 15.2.0`，`-std=c++17 -O3 -DNDEBUG`，动态链接 `/usr/local/lib/libQuantLib.so.1.44.0` |
| 调度与校验环境 | Python `3.14.4`（负责独立参考解生成、精度门禁校验与配对计时调度） |

### 2.2 评测方法论

1. **精度门禁优先（Accuracy-First Gating）**：
   每个场景均配备独立于被测引擎的参考解 $V_{\text{ref}}$ 及参考不确定度 $u_{\text{ref}}$。两侧实现必须满足：
   $$
   |V_{\text{backend}} - V_{\text{ref}}| + u_{\text{ref}} \le \text{error\_budget}
   $$
   对于数值方法（有限差分、蒙特卡洛等），各后端分别采用能稳定通过共同精度门禁的最小离散配置（Committed Profile）。
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
| `european-bsm-atm-call` | `european_bsm` | `AnalyticEuropeanEngine` | 9.22700550815 | $1.07\times 10^{-14}$ | $1.42\times 10^{-14}$ | 24.88 ns (1.07 ns) | 617.70 ns (16.24 ns) | **24.83×** |
| `european-bsm-itm-call` | `european_bsm` | `AnalyticEuropeanEngine` | 23.9825202131 | $0.00$ | $0.00$ | 27.92 ns (1.53 ns) | 641.11 ns (13.68 ns) | **22.96×** |
| `european-bsm-otm-put` | `european_bsm` | `AnalyticEuropeanEngine` | 3.26238340389 | $8.88\times 10^{-16}$ | $6.22\times 10^{-15}$ | 27.13 ns (0.46 ns) | 622.46 ns (9.35 ns) | **22.95×** |
| `digital-bsm-cash-call` | `digital_bsm` | `AnalyticDigitalEngine` | 4.99551713655 | $0.00$ | $1.78\times 10^{-15}$ | 25.53 ns (0.66 ns) | 618.11 ns (37.13 ns) | **24.21×** |
| `digital-bsm-asset-put` | `digital_bsm` | `AnalyticDigitalEngine` | 34.2714509893 | $0.00$ | $1.42\times 10^{-14}$ | 27.12 ns (0.32 ns) | 624.47 ns (32.03 ns) | **23.03×** |
| `geometric-asian-bsm-call` | `geometric_asian_bsm` | `AnalyticGeometricAveragePriceEngine` | 5.03586754652 | $7.11\times 10^{-15}$ | $6.22\times 10^{-15}$ | 44.79 ns (1.65 ns) | 401.36 ns (4.16 ns) | **8.96×** |
| `geometric-asian-bsm-put` | `geometric_asian_bsm` | `AnalyticGeometricAveragePriceEngine` | 2.35569361785 | $2.66\times 10^{-15}$ | $8.88\times 10^{-15}$ | 47.74 ns (3.10 ns) | 408.96 ns (19.27 ns) | **8.57×** |
| `arithmetic-asian-bsm-call` | `arithmetic_asian_bsm` | `TurnbullWakemanArithmeticAveragePriceEngine` | 5.24650186036 | $3.38\times 10^{-14}$ | $7.43\times 10^{-12}$ | 69.13 ns (2.09 ns) | 311.33 ns (6.61 ns) | **4.50×** |
| `arithmetic-asian-bsm-put` | `arithmetic_asian_bsm` | `TurnbullWakemanArithmeticAveragePriceEngine` | 2.27632052827 | $3.42\times 10^{-14}$ | $6.74\times 10^{-12}$ | 69.52 ns (3.12 ns) | 317.96 ns (16.36 ns) | **4.57×** |
| `barrier-down-out-call-rebate` | `single_barrier_bsm` | `AnalyticBarrierEngine` | 9.71405147606 | $5.33\times 10^{-15}$ | $1.78\times 10^{-15}$ | 148.32 ns (3.25 ns) | 1125.82 ns (64.84 ns) | **7.59×** |
| `barrier-up-in-put-rebate` | `single_barrier_bsm` | `AnalyticBarrierEngine` | 1.42695867059 | $2.22\times 10^{-16}$ | $3.33\times 10^{-15}$ | 118.57 ns (4.48 ns) | 1196.66 ns (69.08 ns) | **10.09×** |
| `binary-down-out-cash-call` | `binary_barrier_bsm` | `AnalyticBinaryBarrierEngine` | 4.87026073135 | $1.78\times 10^{-15}$ | $8.88\times 10^{-16}$ | 68.57 ns (1.75 ns) | 275.04 ns (3.38 ns) | **4.01×** |
| `binary-up-in-asset-put` | `binary_barrier_bsm` | `AnalyticBinaryBarrierEngine` | 2.97920242858 | $4.44\times 10^{-16}$ | $4.44\times 10^{-16}$ | 65.63 ns (1.23 ns) | 276.91 ns (12.70 ns) | **4.22×** |
| `touch-up-in-cash-hit` | `touch_bsm` | `AnalyticBinaryBarrierEngine` | 3.71214659048 | $2.22\times 10^{-15}$ | $1.78\times 10^{-15}$ | 44.69 ns (2.66 ns) | 277.80 ns (7.84 ns) | **6.22×** |
| `touch-up-in-cash-expiry` | `touch_bsm` | `AnalyticBinaryBarrierEngine` | 3.63775609357 | $8.88\times 10^{-16}$ | $1.33\times 10^{-15}$ | 59.75 ns (3.28 ns) | 256.12 ns (12.28 ns) | **4.29×** |
| `touch-up-out-cash-expiry` | `touch_bsm` | `AnalyticBinaryBarrierEngine` | 5.97013829796 | $1.78\times 10^{-15}$ | $2.66\times 10^{-15}$ | 60.04 ns (1.05 ns) | 255.76 ns (14.87 ns) | **4.26×** |
| `touch-up-in-asset-hit` | `touch_bsm` | `AnalyticBinaryBarrierEngine` | 44.5457590858 | $1.42\times 10^{-14}$ | $2.13\times 10^{-14}$ | 44.99 ns (1.03 ns) | 276.81 ns (11.92 ns) | **6.15×** |
| `touch-up-in-asset-expiry` | `touch_bsm` | `AnalyticBinaryBarrierEngine` | 44.3204945036 | $3.55\times 10^{-14}$ | $1.42\times 10^{-14}$ | 60.46 ns (4.33 ns) | 255.89 ns (12.40 ns) | **4.23×** |
| `touch-up-out-asset-expiry` | `touch_bsm` | `AnalyticBinaryBarrierEngine` | 54.6844888713 | $4.97\times 10^{-14}$ | $1.42\times 10^{-14}$ | 61.22 ns (2.52 ns) | 262.26 ns (25.36 ns) | **4.28×** |
| `double-barrier-out-call` | `double_barrier_bsm` | `AnalyticDoubleBarrierEngine` | 1.08388145926 | $3.40\times 10^{-14}$ | $4.77\times 10^{-14}$ | 1.67 $\mu\text{s}$ (95.63 ns) | 7.95 $\mu\text{s}$ (192.81 ns) | **4.76×** |
| `double-barrier-in-put` | `double_barrier_bsm` | `AnalyticDoubleBarrierEngine` | 4.81765548074 | $3.73\times 10^{-14}$ | $2.22\times 10^{-14}$ | 1.65 $\mu\text{s}$ (98.90 ns) | 8.31 $\mu\text{s}$ (243.56 ns) | **5.03×** |
| `double-touch-in-cash-expiry` | `double_touch_bsm` | `AnalyticDoubleTouchEngine` | 5.99318208860 | $8.88\times 10^{-16}$ | $8.88\times 10^{-16}$ | 795.77 ns (31.39 ns) | 1.83 $\mu\text{s}$ (94.42 ns) | **2.30×** |
| `double-touch-out-cash-expiry` | `double_touch_bsm` | `AnalyticDoubleTouchEngine` | 3.61471230292 | $8.88\times 10^{-16}$ | $4.44\times 10^{-16}$ | 809.78 ns (6.94 ns) | 1.78 $\mu\text{s}$ (43.80 ns) | **2.20×** |

**技术要点**：

- **纯值计算与对象开销**：Kiyosi 解析引擎仅计算价格标量，无观察者通知链与动态多态分发，欧式与数字期权单次调用仅需 $25\text{–}28\ \text{ns}$；QuantLib `AnalyticEuropeanEngine` 在 `recalculate()` 中同时求值 Greeks，耗时约 $620\text{–}640\ \text{ns}$（加速比 **23×–25×**）。而在 QuantLib 同样只计算价值不计算 Greeks 的到期型单触碰（`AnalyticDigitalAmericanKOEngine` / 到期分支）与双触碰（`AnalyticDoubleBarrierBinaryEngine`）场景中，Kiyosi 依然保持 **4.23×–4.29×** 与 **2.20×–2.30×** 的速度优势。
- **级数展开策略**：双障碍与双触碰场景中，Kiyosi 自适应切换吸收镜像级数与谱级数（内部上限 64 / 256 项，动态收敛判据），而 QuantLib 双障碍使用显式 `series = 5`、双触碰固定上限 99 项 Hui 级数（末项阈值 $10^{-8}$），Kiyosi 在保持 $10^{-14}\text{–}10^{-16}$ 精度的同时取得 **2.20×–5.03×** 加速。

---

### 3.2 数值积分与 CRR 二叉树引擎（6 个场景）

| 场景 ID | 引擎 (`engine`) | 配置对比（Kiyosi vs QuantLib） | 误差预算 | Kiyosi 绝对误差 | QuantLib 绝对误差 | Kiyosi 中位数 (IQR) | QuantLib 中位数 (IQR) | 加速比 ($Q/K$) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `quadrature-bsm-european-call` | `QuadratureVanillaEngine` | 512 步复合 Simpson（行权价分段） vs 5000 步固定梯形法则 | $1.0\times 10^{-5}$ | $8.30\times 10^{-9}$ | $5.05\times 10^{-6}$ | 9.21 $\mu\text{s}$ (0.27 $\mu\text{s}$) | 30.91 $\mu\text{s}$ (1.43 $\mu\text{s}$) | **3.36×** |
| `quadrature-bsm-cash-call` | `QuadratureDigitalEngine` | 512 步复合 Simpson（行权价分段） vs 5000 步固定梯形法则 | $2.0\times 10^{-2}$ | $6.77\times 10^{-10}$ | $1.73\times 10^{-3}$ | 1.96 $\mu\text{s}$ (0.02 $\mu\text{s}$) | 31.58 $\mu\text{s}$ (0.30 $\mu\text{s}$) | **16.13×** |
| `quadrature-bsm-asset-put` | `QuadratureDigitalEngine` | 512 步复合 Simpson（行权价分段） vs 5000 步固定梯形法则 | $2.0\times 10^{-1}$ | $1.34\times 10^{-8}$ | $1.82\times 10^{-2}$ | 1.98 $\mu\text{s}$ (0.10 $\mu\text{s}$) | 30.66 $\mu\text{s}$ (0.18 $\mu\text{s}$) | **15.51×** |
| `crr-bsm-european-call` | `CoxRossRubinsteinVanillaEngine` | `step_count = 512` vs `step_count = 512` | $5.0\times 10^{-3}$ | $3.80\times 10^{-3}$ | $3.83\times 10^{-3}$ | 8.35 $\mu\text{s}$ (0.11 $\mu\text{s}$) | 64.96 $\mu\text{s}$ (1.93 $\mu\text{s}$) | **7.78×** |
| `crr-bsm-american-put` | `CoxRossRubinsteinVanillaEngine` | `step_count = 512` vs `step_count = 512` | $5.0\times 10^{-3}$ | $1.82\times 10^{-3}$ | $1.80\times 10^{-3}$ | 110.71 $\mu\text{s}$ (6.86 $\mu\text{s}$) | 558.74 $\mu\text{s}$ (16.19 $\mu\text{s}$) | **5.05×** |
| `crr-bsm-down-out-call` | `CoxRossRubinsteinBarrierEngine` | `step_count = 2048` vs `step_count = 2048`（纯离散树） | $2.0\times 10^{-2}$ | $5.19\times 10^{-3}$ | $5.18\times 10^{-3}$ | 3.58 ms (0.05 ms) | 5.85 ms (0.06 ms) | **1.64×** |

**技术要点**：

- **数值积分在间断点处的精度跨越**：QuantLib `IntegralEngine` 采用不可调参的 5000 区间梯形积分，跨过数字期权行权价阶跃间断时退化为一阶收敛（绝对误差达 $1.73\times 10^{-3}$ 与 $1.82\times 10^{-2}$）；Kiyosi 在行权价处精确切分积分区间并使用 512 步复合 Simpson 法则（$\pm 8\sigma$），不仅速度提升 **15.51×–16.13×**，还将数字期权积分误差降低 6 个数量级至 $10^{-10}\text{–}10^{-8}$。
- **CRR 二叉树**：在完全相同的步数（512 步或 2048 步）与树离散误差下，Kiyosi 凭借紧凑的一维数组回推实现 **1.64×–7.78×** 加速。

---

### 3.3 一维有限差分引擎：BSM 与局部波动率（22 个场景）

涵盖 BSM（`fd_bsm`，11 个场景，误差预算 $3.0\times 10^{-3}$）与外部给定非恒定局部波动率曲面（`fd_local_vol`，11 个场景，误差预算 $5.0\times 10^{-3}$）。局部波动率曲面在时间（`2025-01-01` 至 `2026-01-01`，Act/365F）与现货（$[80, 120]$，节点矩阵 `[[0.30, 0.15], [0.35, 0.20]]`）上作双线性插值并在边界外常数外推。

- **Kiyosi 配置**：全部 22 个场景统一采用 `space = 800`、`time = 400`、`upper = 400`、`scheme = "rannacher"`（前两个时间步用隐式 Euler 半步阻尼平滑）。
- **QuantLib 配置**：采用 `space = 800` 对数空间自动网格（局部波动率下 `mesher_vol = 0.5` 仅用于网格定界）与 Crank–Nicolson（`damping = 2`）。在 9 个场景中使用 `time = 400`；但在向上触碰（`up-one-touch-cash-hit`）与向上不触碰（`up-no-touch-asset-expiry`）中，`time = 400` 因终端／边界一阶误差超出共同误差预算（BSM 下初始误差分别为 $0.00589$ 与 $0.0696$），需分别加密至 `time = 1600` 与 `time = 16000` 方可通过门禁。

#### 3.3.1 BSM 一维有限差分（`fd_bsm`，误差预算 $3.0\times 10^{-3}$）

| 场景 ID | Kiyosi 引擎 | 时间步（K / Q） | 参考价格 | Kiyosi 绝对误差 | QuantLib 绝对误差 | Kiyosi 中位数 (IQR) | QuantLib 中位数 (IQR) | 加速比 ($Q/K$) |
| --- | --- | :---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `fd-bsm-european-call` | `FiniteDifferenceVanillaEngine` | 400 / 400 | 9.22700550815 | $6.05\times 10^{-4}$ | $7.08\times 10^{-5}$ | 2.08 ms (0.02 ms) | 6.11 ms (0.11 ms) | **2.94×** |
| `fd-bsm-american-put` | `FiniteDifferenceVanillaEngine` | 400 / 400 | 6.66068454589 | $1.20\times 10^{-3}$ | $1.20\times 10^{-3}$ | 2.17 ms (0.07 ms) | 7.99 ms (0.29 ms) | **3.68×** |
| `fd-bsm-cash-digital-call` | `FiniteDifferenceDigitalEngine` | 400 / 400 | 4.94581091053 | $4.45\times 10^{-5}$ | $6.84\times 10^{-5}$ | 2.15 ms (0.08 ms) | 6.25 ms (0.36 ms) | **2.91×** |
| `fd-bsm-asset-digital-put` | `FiniteDifferenceDigitalEngine` | 400 / 400 | 48.7733863768 | $1.42\times 10^{-4}$ | $8.01\times 10^{-4}$ | 2.09 ms (0.04 ms) | 6.20 ms (0.22 ms) | **2.97×** |
| `fd-bsm-down-out-call` | `FiniteDifferenceBarrierEngine` | 400 / 400 | 9.13330643650 | $4.36\times 10^{-4}$ | $1.61\times 10^{-6}$ | 2.10 ms (0.04 ms) | 6.10 ms (0.06 ms) | **2.90×** |
| `fd-bsm-terminal-down-out-cash` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 400 | 4.82180082739 | $3.57\times 10^{-5}$ | $1.47\times 10^{-4}$ | 2.10 ms (0.13 ms) | 6.12 ms (0.22 ms) | **2.92×** |
| `fd-bsm-terminal-up-in-asset` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 400 | 2.94955886912 | $1.04\times 10^{-5}$ | $5.60\times 10^{-5}$ | 4.23 ms (0.29 ms) | 13.63 ms (0.41 ms) | **3.22×** |
| `fd-bsm-down-no-touch-cash-expiry` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 400 | 7.13408843096 | $8.33\times 10^{-5}$ | $1.49\times 10^{-4}$ | 2.12 ms (0.16 ms) | 6.11 ms (0.21 ms) | **2.88×** |
| `fd-bsm-down-one-touch-asset-hit` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 400 | 19.4492167646 | $7.73\times 10^{-4}$ | $1.82\times 10^{-3}$ | 2.05 ms (0.03 ms) | 6.13 ms (0.24 ms) | **2.99×** |
| `fd-bsm-up-one-touch-cash-hit` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 1600 | 3.69391182061 | $1.15\times 10^{-5}$ | $1.48\times 10^{-3}$ | 2.08 ms (0.04 ms) | 23.20 ms (1.14 ms) | **11.17×** |
| `fd-bsm-up-no-touch-asset-expiry` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 16000 | 54.1403691157 | $1.43\times 10^{-4}$ | $1.77\times 10^{-3}$ | 2.07 ms (0.12 ms) | 234.47 ms (3.49 ms) | **113.35×** |

#### 3.3.2 局部波动率一维有限差分（`fd_local_vol`，误差预算 $5.0\times 10^{-3}$）

| 场景 ID | Kiyosi 引擎 | 时间步（K / Q） | 参考价格 | Kiyosi 绝对误差 | QuantLib 绝对误差 | Kiyosi 中位数 (IQR) | QuantLib 中位数 (IQR) | 加速比 ($Q/K$) |
| --- | --- | :---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `fd-local-vol-european-call` | `FiniteDifferenceVanillaEngine` | 400 / 400 | 11.0017427062 | $4.79\times 10^{-4}$ | $1.02\times 10^{-4}$ | 6.63 ms (0.25 ms) | 13.69 ms (1.04 ms) | **2.06×** |
| `fd-local-vol-american-put` | `FiniteDifferenceVanillaEngine` | 400 / 400 | 8.36106642823 | $1.12\times 10^{-3}$ | $1.24\times 10^{-3}$ | 12.09 ms (0.19 ms) | 15.63 ms (1.00 ms) | **1.29×** |
| `fd-local-vol-cash-digital-call` | `FiniteDifferenceDigitalEngine` | 400 / 400 | 5.39093949985 | $1.23\times 10^{-5}$ | $1.22\times 10^{-4}$ | 6.67 ms (0.21 ms) | 13.48 ms (0.31 ms) | **2.02×** |
| `fd-local-vol-asset-digital-put` | `FiniteDifferenceDigitalEngine` | 400 / 400 | 40.5303971416 | $5.96\times 10^{-4}$ | $1.95\times 10^{-3}$ | 6.61 ms (0.28 ms) | 13.47 ms (0.24 ms) | **2.04×** |
| `fd-local-vol-down-out-call` | `FiniteDifferenceBarrierEngine` | 400 / 400 | 10.3817423850 | $3.06\times 10^{-4}$ | $1.40\times 10^{-4}$ | 6.84 ms (0.23 ms) | 13.76 ms (0.57 ms) | **2.01×** |
| `fd-local-vol-terminal-down-out-cash` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 400 | 4.83462680702 | $2.12\times 10^{-6}$ | $2.48\times 10^{-4}$ | 6.62 ms (0.21 ms) | 13.64 ms (0.62 ms) | **2.06×** |
| `fd-local-vol-terminal-up-in-asset` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 400 | 3.48032683172 | $3.67\times 10^{-5}$ | $1.48\times 10^{-5}$ | 13.10 ms (0.25 ms) | 30.25 ms (2.54 ms) | **2.31×** |
| `fd-local-vol-down-no-touch-cash-expiry` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 400 | 5.90771262187 | $3.29\times 10^{-5}$ | $2.35\times 10^{-4}$ | 6.61 ms (0.16 ms) | 13.74 ms (0.78 ms) | **2.08×** |
| `fd-local-vol-down-one-touch-asset-hit` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 400 | 29.6031381560 | $2.33\times 10^{-4}$ | $1.03\times 10^{-3}$ | 6.58 ms (0.10 ms) | 14.35 ms (1.59 ms) | **2.18×** |
| `fd-local-vol-up-one-touch-cash-hit` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 1600 | 4.51261775417 | $1.55\times 10^{-5}$ | $1.83\times 10^{-3}$ | 6.59 ms (0.09 ms) | 53.43 ms (2.21 ms) | **8.11×** |
| `fd-local-vol-up-no-touch-asset-expiry` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 16000 | 44.3991225309 | $1.94\times 10^{-4}$ | $2.04\times 10^{-3}$ | 6.67 ms (0.24 ms) | 531.72 ms (4.76 ms) | **79.71×** |

**技术要点**：

- **同规模网格（$800 \times 400$）下的求解器吞吐**：在 9 个时间步相同的场景中，Kiyosi 在 BSM 下稳定耗时约 $2.05\text{–}2.17\ \text{ms}$（敲入型 `terminal-up-in-asset` 需两次 PDE 求解，耗时 $4.23\ \text{ms}$ vs QuantLib $13.63\ \text{ms}$），几何平均加速 **3.04×**；在局部波动率下稳定耗时 $6.58\text{–}13.10\ \text{ms}$，几何平均加速 **1.98×**。
- **边界条件与时间步收敛效率**：在向上触碰／不触碰场景中，Kiyosi 凭借跳跃修正与边界处理在 $400$ 时间步下即达到 $10^{-5}\text{–}10^{-4}$ 精度；QuantLib 需将时间步加密 $4\times$（1600 步）与 $40\times$（16000 步）才能将终端边界误差压入同一预算，从而产生 **8.11×–113.35×** 的实测耗时差距。

---

### 3.4 Heston 随机波动率引擎（3 个场景）

共用市场与模型参数：$S = K = 100,\ r = 0.05,\ q = 0.02,\ v_0 = \theta = 0.04,\ \kappa = 1.5,\ \xi = 0.3,\ \rho = -0.7$，期限 1 年（`2025-01-01` 至 `2026-01-01`）。

| 场景 ID | 引擎 (`engine`) | 算法与配置对比（Kiyosi vs QuantLib） | 误差预算 | Kiyosi 绝对误差 | QuantLib 绝对误差 | Kiyosi 中位数 (IQR) | QuantLib 中位数 (IQR) | 加速比 ($Q/K$) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `heston-analytic-call` | `AnalyticHestonEuropeanEngine` | 自适应 Fourier + 确定性方差控制变量（$\text{tol}=10^{-9}$） vs Gatheral 自适应 Lobatto（$\text{rel\_tol}=10^{-9}$） | $1.0\times 10^{-7}$ | $2.31\times 10^{-14}$ | $1.95\times 10^{-14}$ | 72.59 $\mu\text{s}$ (4.04 $\mu\text{s}$) | 66.23 $\mu\text{s}$ (0.98 $\mu\text{s}$) | **0.91×** |
| `heston-fd-european-call` | `FiniteDifferenceHestonVanillaEngine` | MCS ADI ($\theta=1/3$), $200\times 50\times 200$ 区间 vs Hundsdorfer ADI, $200\times 100\times 200$ 节点 | $5.0\times 10^{-3}$ | $4.89\times 10^{-4}$ | $9.05\times 10^{-4}$ | 96.09 ms (3.25 ms) | 212.05 ms (3.88 ms) | **2.21×** |
| `heston-fd-american-put` | `FiniteDifferenceHestonVanillaEngine` | MCS ADI + Ikonen–Toivanen 分裂, $200\times 50\times 200$ vs Hundsdorfer + 投影, $200\times 100\times 200$ | $5.0\times 10^{-3}$ | $1.12\times 10^{-3}$ | $3.54\times 10^{-3}$ | 94.08 ms (2.32 ms) | 233.22 ms (3.22 ms) | **2.48×** |

**技术要点**：

- **Heston Fourier 积分**：`heston-analytic-call` 是全套基准中唯一 $Q/K < 1$ 的场景（差距 $6.36\ \mu\text{s}$）。Kiyosi 采用带确定性方差控制变量的半无限区间映射与显式尾部界估计，双方均达到 $2\times 10^{-14}$ 精度。
- **Heston 二维有限差分**：Kiyosi 采用 Modified Craig–Sneyd（MCS，$\theta=1/3$）ADI 格式并在美式行权中应用 Ikonen–Toivanen 算子分裂，在 $200\times 50\times 200$ 网格（计算域 $[0, 400]\times[0, 0.6]$）下的绝对误差（欧式 $4.89\times 10^{-4}$、美式 $1.12\times 10^{-3}$）反而优于 QuantLib 在 $200\times 100\times 200$ 网格下的误差（欧式 $9.05\times 10^{-4}$、美式 $3.54\times 10^{-3}$），同时实现 **2.21×–2.48×** 加速。

---

### 3.5 BSM 蒙特卡洛引擎（5 个场景）

全部场景采用单线程伪随机抽样，关闭对偶变量（`antithetic = false`）与控制变量（`control_variate = false`）。Kiyosi 使用块流式 PCG32 + Box–Muller；QuantLib 使用 MT19937 + 逆正态分布。除计时种子 `seed = 1729` 外，双方均在 32 个预设验证种子（$1009 + 97i,\ i=0\dots 31$）上检验样本统计量。

#### 3.5.1 计时种子精度与延迟表现（`seed = 1729`）

| 场景 ID | 引擎 (`engine`) | 物理路径数（K / Q） | 误差预算 | 参考价格 | Kiyosi 计时误差 | QuantLib 计时误差 | Kiyosi 中位数 (IQR) | QuantLib 中位数 (IQR) | 加速比 ($Q/K$) |
| --- | --- | :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `mc-european-call` | `MonteCarloVanillaEngine` | 131,072 / 262,144 | $0.10$ | 9.22700550815 | $6.38\times 10^{-2}$ | $3.14\times 10^{-2}$ | 2.77 ms (0.05 ms) | 31.47 ms (0.52 ms) | **11.37×** |
| `mc-european-put` | `MonteCarloVanillaEngine` | 65,536 / 65,536 | $0.10$ | 6.33008062755 | $1.58\times 10^{-2}$ | $4.47\times 10^{-2}$ | 1.40 ms (0.02 ms) | 7.73 ms (0.13 ms) | **5.54×** |
| `mc-barrier-down-out-call` | `MonteCarloBarrierEngine` | 65,536 / 131,072 | $0.10$ | 7.58695396974 | $9.38\times 10^{-2}$ | $3.13\times 10^{-2}$ | 3.30 ms (0.12 ms) | 20.40 ms (0.66 ms) | **6.19×** |
| `mc-barrier-up-in-put` | `MonteCarloBarrierEngine` | 65,536 / 65,536 | $0.10$ | 0.23061330871 | $2.17\times 10^{-3}$ | $3.01\times 10^{-5}$ | 3.57 ms (0.21 ms) | 10.54 ms (0.89 ms) | **2.95×** |
| `mc-american-put` | `MonteCarloVanillaEngine` | 65,536 / 65,536 (+32,768 校准) | $0.15$ | 6.66068454589 | $3.18\times 10^{-3}$ | $5.58\times 10^{-2}$ | 135.71 ms (5.28 ms) | 664.45 ms (5.73 ms) | **4.90×** |

#### 3.5.2 32 种子集合验证统计量（Seed Ensemble Validation）

| 场景 ID | 门禁上限（RMSE / \|Bias\| / StdDev） | Kiyosi RMSE | QuantLib RMSE | Kiyosi 有符号偏差 | QuantLib 有符号偏差 | Kiyosi 样本标准差 (SE) | QuantLib 样本标准差 (SE) | 最大绝对误差（K / Q） |
| --- | :---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `mc-european-call` | $0.05$ / $0.025$ / $0.05$ | $3.11\times 10^{-2}$ | $2.88\times 10^{-2}$ | $+2.85\times 10^{-3}$ | $-2.53\times 10^{-3}$ | $3.14\times 10^{-2}$ ($5.56\times 10^{-3}$) | $2.92\times 10^{-2}$ ($5.16\times 10^{-3}$) | $8.39\times 10^{-2}$ / $6.07\times 10^{-2}$ |
| `mc-european-put` | $0.05$ / $0.025$ / $0.05$ | $2.70\times 10^{-2}$ | $3.52\times 10^{-2}$ | $-3.28\times 10^{-3}$ | $+1.85\times 10^{-2}$ | $2.72\times 10^{-2}$ ($4.81\times 10^{-3}$) | $3.04\times 10^{-2}$ ($5.37\times 10^{-3}$) | $4.49\times 10^{-2}$ / $8.08\times 10^{-2}$ |
| `mc-barrier-down-out-call` | $0.05$ / $0.025$ / $0.05$ | $3.45\times 10^{-2}$ | $3.66\times 10^{-2}$ | $+1.13\times 10^{-3}$ | $-7.45\times 10^{-3}$ | $3.51\times 10^{-2}$ ($6.20\times 10^{-3}$) | $3.64\times 10^{-2}$ ($6.43\times 10^{-3}$) | $6.64\times 10^{-2}$ / $9.87\times 10^{-2}$ |
| `mc-barrier-up-in-put` | $0.05$ / $0.025$ / $0.05$ | $1.08\times 10^{-3}$ | $7.32\times 10^{-3}$ | $-5.32\times 10^{-5}$ | $+5.01\times 10^{-3}$ | $1.09\times 10^{-3}$ ($1.93\times 10^{-4}$) | $5.41\times 10^{-3}$ ($9.57\times 10^{-4}$) | $2.66\times 10^{-3}$ / $1.41\times 10^{-2}$ |
| `mc-american-put` | $0.075$ / $0.05$ / $0.075$ | $4.05\times 10^{-2}$ | $4.02\times 10^{-2}$ | $-2.41\times 10^{-2}$ | $-2.54\times 10^{-2}$ | $3.31\times 10^{-2}$ ($5.84\times 10^{-3}$) | $3.16\times 10^{-2}$ ($5.58\times 10^{-3}$) | $7.95\times 10^{-2}$ / $9.57\times 10^{-2}$ |

**技术要点**：

- **连续障碍桥接存活率 vs 辅助随机数抽样**：在单步终值演化的连续障碍期权中，Kiyosi 直接计算 Brownian Bridge 条件存活概率期望（无额外抽样噪声），而 QuantLib `MCBarrierEngine` 使用固定种子（`seed = 5`）的辅助均匀随机数对桥穿越做伯努利抽样。在同为 $65{,}536$ 条路径的 `mc-barrier-up-in-put` 中，Kiyosi 不仅快 **2.95×**，其 32 种子 RMSE（$1.08\times 10^{-3}$）也比 QuantLib（$7.32\times 10^{-3}$）低 **6.8 倍**；在 `mc-barrier-down-out-call` 中，QuantLib 需翻倍至 $131{,}072$ 条路径才能达到与 Kiyosi $65{,}536$ 条路径相当的 RMSE（$0.0366$ vs $0.0345$），从而带来 **6.19×** 的实测耗时比。
- **美式最小二乘蒙特卡洛（LSM）**：在 `mc-american-put`（65,536 条定价路径、50 个行权时间步、二次单项式基）中，Kiyosi 在实值（ITM）定价路径上直接做样本内回归拟合（基函数 $1, S/K, (S/K)^2$），而 QuantLib 在每次 `recalculate()` 中先独立模拟 32,768 条校准路径再模拟 65,536 条定价路径。根据 `report.json` 记录的 LSM 细化实验（`lsm_refinement`）：
  - 将定价路径翻倍至 $131{,}072$ 时，Kiyosi 与 QuantLib 的 32 种子 RMSE 分别降至 $0.0332$ 与 $0.0315$；
  - 在 $131{,}072$ 路径下将行权步从 50 加密至 100，Kiyosi 与 QuantLib 的种子均值变化仅为 $-0.00141$（$\text{SE}=0.00340$）与 $+0.00075$（$\text{SE}=0.00297$）；
  - 将 QuantLib 校准路径从 $32{,}768$ 翻倍至 $65{,}536$ 时，均值变化仅 $+4.56\times 10^{-5}$（$\text{SE}=7.16\times 10^{-4}$）。
  在基线配置下，双端集合精度高度一致（RMSE $0.0405$ vs $0.0402$），而 Kiyosi 延迟仅为 $135.71\ \text{ms}$（QuantLib 为 $664.45\ \text{ms}$，加速 **4.90×**）。

---

## 4. 覆盖范围、局限与解读说明

1. **严格语义对齐与排除边界**：
   本基准仅纳入在合约条款、市场模型与数值算法三个维度上与 QuantLib 原生引擎严格等价的 **20 类引擎（51 个语义单元）**。Kiyosi 其余 14 类引擎因缺乏直接等价的 QuantLib 原生实现而未纳入对比，包括：
   - 近似公式版本不同：`BjerksundStenslandVanillaEngine`（Kiyosi 实现 2002 版，QuantLib 为 1993 版）；
   - 结构化奇异产品无内置对应引擎：自动赎回（`Autocallable`）、累购累沽（`Accumulator`）的积分、有限差分与蒙特卡洛引擎，以及区间累计解析引擎（`AnalyticRangeAccrualEngine`）；
   - 离散／连续监控或算法语义差异：数字期权与连续平均亚式蒙特卡洛、双障碍／双触碰有限差分、障碍期权数值积分及数字期权 CRR 二叉树。
2. **加速比解读注意事项**：
   - **同工作量对比 vs 精度门禁驱动对比**：大部分场景（如 BSM 解析法、CRR 二叉树、18 个同步数一维 FD、2 个同路径 MC）属于固定相同离散规模或解析公式的对比；而 `fd-bsm-up-no-touch-asset-expiry`（**113.35×**）、`fd-local-vol-up-no-touch-asset-expiry`（**79.71×**）、`mc-european-call`（**11.37×**）等高加速比则反映了“达到相同先验精度门禁所需的计算成本差异”。
   - **接口固有附加计算**：QuantLib 原生 `recalculate()` 在部分解析引擎和有限差分引擎中会同步计算灵敏度指标，在蒙特卡洛中会累计样本方差；Kiyosi 的 `price()` 仅计算价格标量（Greeks 由 `price_with_greeks()` 按需调用）。
   - **单核基准**：所有测量均固定 `workers = 1`，反映单核指令与内存布局效率，不包含 Kiyosi 蒙特卡洛引擎在多线程 Rayon 池下的并行扩展加速。
