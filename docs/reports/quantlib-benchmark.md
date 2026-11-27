# Kiyosi vs QuantLib 基准测试分析报告

> **评测版本**　Kiyosi `v0.23.0`（`9231574344cbc2173d3ccdea1e52f4cf749504ed`）与 QuantLib C++ `1.44`（`libQuantLib.so.1.44.0`）。[Kiyosi v0.23.0](https://github.com/lilkui/kiyosi/commit/9231574344cbc2173d3ccdea1e52f4cf749504ed)
>
> **基准套件**　在 Kiyosi v0.23.0 的检出上应用 `8ad163b88abc5d32e4b854fc2d96e45b45167ccd` 中 `benchmarks/quantlib/` 的变更。[基准套件与运行方式](https://github.com/lilkui/kiyosi/blob/8ad163b88abc5d32e4b854fc2d96e45b45167ccd/benchmarks/quantlib/README.md#运行方式)
>
> **评测时间**　2026-11-27 12:56:08 UTC+8，整次运行耗时 493.83 s。
>
> **数据来源**　基准运行器生成的 JSON 报告（默认路径 `benchmarks/quantlib/report.json`，Schema v1，状态 `passed`）。

---

## 1. 执行摘要

本报告对比 Kiyosi 与 QuantLib C++ 1.44 的衍生品定价精度和延迟，覆盖 **20 类定价引擎**、**51 个必测语义单元（Semantic Cells）** 和 **62 个评测场景**。其中 59 个场景双方各用 1 个工作线程，另有 3 个蒙特卡洛场景使用 Kiyosi 的 8 个工作线程与 QuantLib 的 1 个工作线程。双端通过精度门禁后再计时。

### 核心结论

- **62 个场景均通过精度门禁**。8 个蒙特卡洛场景在 32 个预设验证种子下的均方根误差（RMSE）、有符号偏差的绝对值和样本标准差均满足门限。
- Kiyosi 在 62 个场景中的中位数延迟均低于 QuantLib。全量中位数延迟比 $Q/K$ 的几何平均值为 **9.87×**，中位数为 **7.04×**，范围为 **2.16×–230.97×**。
- 在各后端的路径数、时间步数和随机种子固定的条件下，Kiyosi 从 1 个工作线程扩展到 8 个工作线程时，欧式看涨、下敲出看涨和美式看跌的加速比分别为 **4.89×**、**5.08×**、**4.58×**。
- $Q/K$ 最低的是双障碍到期现金不触碰解析场景（`double-touch-out-cash-expiry`，**2.16×**）。最高的是 BSM 向上资产不触碰有限差分场景（`fd-bsm-up-no-touch-asset-expiry`，**230.97×**）。在后者中，为满足共同误差预算，Kiyosi 使用 400 个时间步，QuantLib 使用 16,000 个时间步。
- 在双方均用 $800\times 400$ 网格的 9 个 BSM 一维有限差分场景中，$Q/K$ 的几何平均值为 **6.12×**。在双方均用 65,536 条路径、各用 1 个工作线程的欧式看跌和障碍敲入看跌蒙特卡洛场景中，$Q/K$ 分别为 **5.44×** 和 **3.07×**。在各自按误差预算选择时间步数的 11 个局部波动率一维有限差分场景中，$Q/K$ 的几何平均值为 **15.83×**。

### 分模块汇总

| 算法类别 | 场景数 | 误差预算 | 计时配置最大绝对误差（Kiyosi / QuantLib） | 中位数延迟范围（Kiyosi vs QuantLib） | 几何平均加速比 | 中位数加速比 | 加速比区间（$Q/K$） |
| --- | ---: | ---: | --- | --- | ---: | ---: | --- |
| BSM 解析法 | 23 | $1.0\times 10^{-9}$ | $3.55\times 10^{-14}$ / $7.43\times 10^{-12}$ | 27.65 ns – 1.80 $\mu\text{s}$ vs 255.03 ns – 8.24 $\mu\text{s}$ | **6.15×** | 5.08× | 2.16× – 22.58× |
| Heston 解析积分 | 1 | $1.0\times 10^{-7}$ | $2.31\times 10^{-14}$ / $1.95\times 10^{-14}$ | 13.46 $\mu\text{s}$ vs 66.09 $\mu\text{s}$ | **4.91×** | 4.91× | 4.91× |
| BSM 数值积分 | 3 | $10^{-5} - 0.2$ | $1.34\times 10^{-8}$ / $1.82\times 10^{-2}$ | 1.98 $\mu\text{s}$ – 5.28 $\mu\text{s}$ vs 31.08 $\mu\text{s}$ – 31.76 $\mu\text{s}$ | **11.41×** | 15.72× | 5.93× – 15.95× |
| CRR 二叉树 | 3 | $5\times 10^{-3} - 2\times 10^{-2}$ | $5.19\times 10^{-3}$ / $5.18\times 10^{-3}$ | 1.08 $\mu\text{s}$ – 109.34 $\mu\text{s}$ vs 65.22 $\mu\text{s}$ – 5.98 ms | **37.12×** | 60.13× | 5.05× – 168.41× |
| 一维有限差分（BSM） | 11 | $3.0\times 10^{-3}$ | $1.11\times 10^{-3}$ / $1.82\times 10^{-3}$ | 998.74 $\mu\text{s}$ – 2.04 ms vs 6.04 ms – 234.20 ms | **9.62×** | 6.10× | 5.71× – 230.97× |
| 一维有限差分（局部波动率） | 11 | $5.0\times 10^{-3}$ | $2.16\times 10^{-3}$ / $2.04\times 10^{-3}$ | 1.22 ms – 2.58 ms vs 13.60 ms – 536.40 ms | **15.83×** | 11.31× | 6.27× – 222.82× |
| 二维有限差分（Heston） | 2 | $5.0\times 10^{-3}$ | $1.06\times 10^{-3}$ / $3.54\times 10^{-3}$ | 14.35 ms – 16.10 ms vs 209.86 ms – 233.14 ms | **14.55×** | 14.55× | 14.48× – 14.62× |
| BSM 蒙特卡洛（1 / 1 工作线程） | 5 | $0.10 - 0.15$ | $9.38\times 10^{-2}$ / $5.58\times 10^{-2}$ | 1.46 ms – 102.54 ms vs 7.95 ms – 669.65 ms | **5.92×** | 6.35× | 3.07× – 10.47× |
| BSM 蒙特卡洛（8 / 1 工作线程） | 3 | $0.10 - 0.15$ | $9.38\times 10^{-2}$ / $5.58\times 10^{-2}$ | 617.45 $\mu\text{s}$ – 22.40 ms vs 21.22 ms – 666.35 ms | **37.73×** | 33.59× | 29.74× – 53.75× |
| **全部场景合计** | **62** | — | — | 27.65 ns – 102.54 ms vs 255.03 ns – 669.65 ms | **9.87×** | 7.04× | 2.16× – 230.97× |

---

## 2. 测试环境与评测协议

### 2.1 硬件与编译工具链

| 维度 | 配置详情 |
| --- | --- |
| 操作系统 | `Linux-6.18.58.1-microsoft-standard-WSL2-x86_64-with-glibc2.43` |
| 处理器 | Intel(R) Core(TM) Ultra 9 285（24 核 24 线程，L1d 1.1 MiB / L1i 1.5 MiB / L2 72 MiB / L3 36 MiB） |
| 工作线程 | 蒙特卡洛场景按 `profiles.kiyosi.workers` 与 `profiles.quantlib.workers` 配置，其余场景双方各用 1 个工作线程。8 线程场景要求至少 8 个可用逻辑 CPU |
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
   合约、市场上下文、模型及引擎对象均在计时循环外预先构造，计时仅覆盖单次公开定价调用（Kiyosi `price()` vs QuantLib `recalculate() + NPV()`）。每个批次预热 3 次。8 线程场景在首次并行预热时创建 Kiyosi 专用 Rayon 线程池，批次内的定价调用复用该线程池。运行器自适应调整单批迭代次数以达到目标阈值（`target_ms = 20`），再按 `[kiyosi, quantlib]` 与 `[quantlib, kiyosi]` 交替采集 **15 组配对样本**，以减轻系统热漂移与背景噪声的影响。分位数（`q1_ns`、`median_ns`、`q3_ns`、`iqr_ns`）采用包含端点的线性插值计算。
3. **工作量透明度**：
   测试直接调用双端公开原生定价接口，保留引擎固有开销。例如 QuantLib 部分解析与有限差分引擎在 `recalculate()` 时会附带计算部分 Greeks，蒙特卡洛引擎会累加样本方差；这些实际计算均计入测量时间，并在各模块说明中标注。

---

## 3. 分模块精度与性能分析

### 3.1 BSM 解析引擎（23 个场景）

涵盖欧式普通期权、现金／资产数字期权、连续几何／算术平均亚式期权、单障碍期权、二元障碍期权、单触碰／不触碰期权及双障碍／双触碰期权。所有场景共享 $1.0\times 10^{-9}$ 的绝对误差预算，参考解由 Python `Decimal`（50–110 位有效数字）通过高斯幂级数积分、镜像法吸收密度积分及首达时间 Laplace 变换独立计算（$u_{\text{ref}} \in [10^{-13}, 10^{-12}]$）。

| 场景 ID | 家族 (`family`) | Kiyosi 引擎 | 参考价格 | Kiyosi 绝对误差 | QuantLib 绝对误差 | Kiyosi 中位数 (IQR) | QuantLib 中位数 (IQR) | 加速比 ($Q/K$) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `european-bsm-atm-call` | `european_bsm` | `AnalyticEuropeanEngine` | 9.22700550815 | $1.07\times 10^{-14}$ | $1.42\times 10^{-14}$ | 27.88 ns (0.62 ns) | 627.67 ns (22.34 ns) | **22.51×** |
| `european-bsm-itm-call` | `european_bsm` | `AnalyticEuropeanEngine` | 23.9825202131 | $0.00$ | $0.00$ | 35.44 ns (0.65 ns) | 627.20 ns (30.72 ns) | **17.70×** |
| `european-bsm-otm-put` | `european_bsm` | `AnalyticEuropeanEngine` | 3.26238340389 | $8.88\times 10^{-16}$ | $6.22\times 10^{-15}$ | 35.78 ns (0.44 ns) | 625.53 ns (9.22 ns) | **17.48×** |
| `digital-bsm-cash-call` | `digital_bsm` | `AnalyticDigitalEngine` | 4.99551713655 | $0.00$ | $1.78\times 10^{-15}$ | 27.65 ns (0.30 ns) | 624.33 ns (15.66 ns) | **22.58×** |
| `digital-bsm-asset-put` | `digital_bsm` | `AnalyticDigitalEngine` | 34.2714509893 | $0.00$ | $1.42\times 10^{-14}$ | 35.38 ns (0.74 ns) | 628.31 ns (14.81 ns) | **17.76×** |
| `geometric-asian-bsm-call` | `geometric_asian_bsm` | `AnalyticGeometricAveragePriceEngine` | 5.03586754652 | $7.11\times 10^{-15}$ | $6.22\times 10^{-15}$ | 56.23 ns (0.90 ns) | 405.29 ns (6.24 ns) | **7.21×** |
| `geometric-asian-bsm-put` | `geometric_asian_bsm` | `AnalyticGeometricAveragePriceEngine` | 2.35569361785 | $2.66\times 10^{-15}$ | $8.88\times 10^{-15}$ | 56.70 ns (1.36 ns) | 410.89 ns (10.77 ns) | **7.25×** |
| `arithmetic-asian-bsm-call` | `arithmetic_asian_bsm` | `TurnbullWakemanArithmeticAveragePriceEngine` | 5.24650186036 | $3.38\times 10^{-14}$ | $7.43\times 10^{-12}$ | 72.02 ns (3.46 ns) | 310.90 ns (5.44 ns) | **4.32×** |
| `arithmetic-asian-bsm-put` | `arithmetic_asian_bsm` | `TurnbullWakemanArithmeticAveragePriceEngine` | 2.27632052827 | $3.42\times 10^{-14}$ | $6.74\times 10^{-12}$ | 71.98 ns (2.11 ns) | 311.91 ns (4.17 ns) | **4.33×** |
| `barrier-down-out-call-rebate` | `single_barrier_bsm` | `AnalyticBarrierEngine` | 9.71405147606 | $5.33\times 10^{-15}$ | $1.78\times 10^{-15}$ | 160.30 ns (8.59 ns) | 1.12 $\mu\text{s}$ (0.05 $\mu\text{s}$) | **6.99×** |
| `barrier-up-in-put-rebate` | `single_barrier_bsm` | `AnalyticBarrierEngine` | 1.42695867059 | $2.22\times 10^{-16}$ | $3.33\times 10^{-15}$ | 121.09 ns (2.45 ns) | 1.16 $\mu\text{s}$ (0.02 $\mu\text{s}$) | **9.58×** |
| `binary-down-out-cash-call` | `binary_barrier_bsm` | `AnalyticBinaryBarrierEngine` | 4.87026073135 | $1.78\times 10^{-15}$ | $8.88\times 10^{-16}$ | 76.99 ns (1.01 ns) | 277.46 ns (4.22 ns) | **3.60×** |
| `binary-up-in-asset-put` | `binary_barrier_bsm` | `AnalyticBinaryBarrierEngine` | 2.97920242858 | $4.44\times 10^{-16}$ | $4.44\times 10^{-16}$ | 72.04 ns (4.21 ns) | 278.34 ns (10.55 ns) | **3.86×** |
| `touch-up-in-cash-hit` | `touch_bsm` | `AnalyticBinaryBarrierEngine` | 3.71214659048 | $2.22\times 10^{-15}$ | $1.78\times 10^{-15}$ | 51.21 ns (0.95 ns) | 279.17 ns (5.91 ns) | **5.45×** |
| `touch-up-in-cash-expiry` | `touch_bsm` | `AnalyticBinaryBarrierEngine` | 3.63775609357 | $8.88\times 10^{-16}$ | $1.33\times 10^{-15}$ | 61.51 ns (2.38 ns) | 259.20 ns (15.12 ns) | **4.21×** |
| `touch-up-out-cash-expiry` | `touch_bsm` | `AnalyticBinaryBarrierEngine` | 5.97013829796 | $0.00$ | $2.66\times 10^{-15}$ | 82.54 ns (1.85 ns) | 255.03 ns (4.59 ns) | **3.09×** |
| `touch-up-in-asset-hit` | `touch_bsm` | `AnalyticBinaryBarrierEngine` | 44.5457590858 | $1.42\times 10^{-14}$ | $2.13\times 10^{-14}$ | 51.72 ns (1.47 ns) | 277.69 ns (5.64 ns) | **5.37×** |
| `touch-up-in-asset-expiry` | `touch_bsm` | `AnalyticBinaryBarrierEngine` | 44.3204945036 | $3.55\times 10^{-14}$ | $1.42\times 10^{-14}$ | 62.25 ns (1.98 ns) | 258.97 ns (8.28 ns) | **4.16×** |
| `touch-up-out-asset-expiry` | `touch_bsm` | `AnalyticBinaryBarrierEngine` | 54.6844888713 | $0.00$ | $1.42\times 10^{-14}$ | 82.58 ns (0.57 ns) | 257.25 ns (7.01 ns) | **3.11×** |
| `double-barrier-out-call` | `double_barrier_bsm` | `AnalyticDoubleBarrierEngine` | 1.08388145926 | $3.40\times 10^{-14}$ | $4.77\times 10^{-14}$ | 1.80 $\mu\text{s}$ (0.11 $\mu\text{s}$) | 8.05 $\mu\text{s}$ (0.39 $\mu\text{s}$) | **4.46×** |
| `double-barrier-in-put` | `double_barrier_bsm` | `AnalyticDoubleBarrierEngine` | 4.81765548074 | $3.38\times 10^{-14}$ | $2.22\times 10^{-14}$ | 1.62 $\mu\text{s}$ (0.04 $\mu\text{s}$) | 8.24 $\mu\text{s}$ (0.42 $\mu\text{s}$) | **5.08×** |
| `double-touch-in-cash-expiry` | `double_touch_bsm` | `AnalyticDoubleTouchEngine` | 5.99318208860 | $8.88\times 10^{-16}$ | $8.88\times 10^{-16}$ | 816.01 ns (10.67 ns) | 1.82 $\mu\text{s}$ (0.03 $\mu\text{s}$) | **2.23×** |
| `double-touch-out-cash-expiry` | `double_touch_bsm` | `AnalyticDoubleTouchEngine` | 3.61471230292 | $8.88\times 10^{-16}$ | $4.44\times 10^{-16}$ | 836.71 ns (46.05 ns) | 1.81 $\mu\text{s}$ (0.05 $\mu\text{s}$) | **2.16×** |

**技术要点**：

- 欧式普通期权与到期数字期权的中位数延迟为 Kiyosi 27.65 ns – 35.78 ns、QuantLib 624.33 ns – 628.31 ns，加速比为 **17.48×–22.58×**。Kiyosi 的 `price()` 返回价格标量，QuantLib 的 `AnalyticEuropeanEngine` 在 `recalculate()` 中也计算 Greeks。到期结算的单触碰与单不触碰场景加速比为 **3.09×–4.21×**，双触碰与双不触碰场景为 **2.16×–2.23×**。
- Kiyosi 的双障碍与双触碰引擎在吸收镜像级数与谱级数之间自适应选择（内部上限分别为 64 项和 256 项）。QuantLib 双障碍使用 `series = 5`，双触碰采用最多 99 项的 Hui 级数（末项阈值 $10^{-8}$）。这四个场景的加速比为 **2.16×–5.08×**，双端绝对误差均在 $10^{-16}\text{–}10^{-14}$ 之间。

---

### 3.2 数值积分与 CRR 二叉树引擎（6 个场景）

| 场景 ID | 引擎 (`engine`) | 配置对比（Kiyosi vs QuantLib） | 误差预算 | Kiyosi 绝对误差 | QuantLib 绝对误差 | Kiyosi 中位数 (IQR) | QuantLib 中位数 (IQR) | 加速比 ($Q/K$) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `quadrature-bsm-european-call` | `QuadratureVanillaEngine` | 512 步复合 Simpson（行权价分段） vs 5000 步固定梯形法则 | $1.00\times 10^{-5}$ | $8.30\times 10^{-9}$ | $5.05\times 10^{-6}$ | 5.28 $\mu\text{s}$ (0.10 $\mu\text{s}$) | 31.31 $\mu\text{s}$ (0.81 $\mu\text{s}$) | **5.93×** |
| `quadrature-bsm-cash-call` | `QuadratureDigitalEngine` | 512 步复合 Simpson（行权价分段） vs 5000 步固定梯形法则 | $2.00\times 10^{-2}$ | $6.77\times 10^{-10}$ | $1.73\times 10^{-3}$ | 1.99 $\mu\text{s}$ (0.12 $\mu\text{s}$) | 31.76 $\mu\text{s}$ (0.33 $\mu\text{s}$) | **15.95×** |
| `quadrature-bsm-asset-put` | `QuadratureDigitalEngine` | 512 步复合 Simpson（行权价分段） vs 5000 步固定梯形法则 | $2.00\times 10^{-1}$ | $1.34\times 10^{-8}$ | $1.82\times 10^{-2}$ | 1.98 $\mu\text{s}$ (0.02 $\mu\text{s}$) | 31.08 $\mu\text{s}$ (0.50 $\mu\text{s}$) | **15.72×** |
| `crr-bsm-european-call` | `CoxRossRubinsteinVanillaEngine` | `step_count = 512` vs `step_count = 512` | $5.00\times 10^{-3}$ | $3.80\times 10^{-3}$ | $3.83\times 10^{-3}$ | 1.08 $\mu\text{s}$ (0.05 $\mu\text{s}$) | 65.22 $\mu\text{s}$ (0.44 $\mu\text{s}$) | **60.13×** |
| `crr-bsm-american-put` | `CoxRossRubinsteinVanillaEngine` | `step_count = 512` vs `step_count = 512` | $5.00\times 10^{-3}$ | $1.82\times 10^{-3}$ | $1.80\times 10^{-3}$ | 109.34 $\mu\text{s}$ (1.46 $\mu\text{s}$) | 552.31 $\mu\text{s}$ (10.10 $\mu\text{s}$) | **5.05×** |
| `crr-bsm-down-out-call` | `CoxRossRubinsteinBarrierEngine` | `step_count = 2048` vs `step_count = 2048`（纯离散树） | $2.00\times 10^{-2}$ | $5.19\times 10^{-3}$ | $5.18\times 10^{-3}$ | 35.53 $\mu\text{s}$ (1.58 $\mu\text{s}$) | 5.98 ms (0.15 ms) | **168.41×** |

**技术要点**：

- 在两个数字期权积分场景中，Kiyosi 在行权价处切分积分区间，使用 512 步复合 Simpson 法（$\pm 8\sigma$），绝对误差分别为 $6.77\times 10^{-10}$ 和 $1.34\times 10^{-8}$。QuantLib `IntegralEngine` 使用 5000 区间的固定梯形法，对应误差为 $1.73\times 10^{-3}$ 和 $1.82\times 10^{-2}$。Kiyosi 在这两个场景的加速比为 **15.72×–15.95×**。
- CRR 场景中双方步数相同，绝对误差接近。Kiyosi 对 512 步欧式看涨直接按二项分布权重求到期收益期望，对 2048 步下敲出看涨用反射法计算逐步监控下的格点权重，加速比分别为 **60.13×** 和 **168.41×**；512 步美式看跌需逐层回推处理提前行权，加速比为 **5.05×**。

---

### 3.3 一维有限差分引擎：BSM 与局部波动率（22 个场景）

涵盖 BSM（`fd_bsm`，11 个场景，误差预算 $3.0\times 10^{-3}$）与外部给定的非恒定局部波动率曲面（`fd_local_vol`，11 个场景，误差预算 $5.0\times 10^{-3}$）。局部波动率曲面在时间（`2025-01-01` 至 `2026-01-01`，Act/365F）与现货（$[80,120]$，节点矩阵 `[[0.30, 0.15], [0.35, 0.20]]`）上作双线性插值，现货超出区间时取相应端点值。

- Kiyosi 在 22 个场景中均使用 800 个空间步、对数现货网格和 Rannacher 格式。BSM 场景使用 400 个时间步。局部波动率场景中，美式看跌和向上资产不触碰使用 200 步，其余 9 个场景使用 100 步。两个普通欧式场景自动选择求解域并在行权价附近加密节点，其余场景显式设置 `upper = 400`。
- QuantLib 使用 `space = 800` 的自动对数网格与 Crank–Nicolson 格式（`damping = 2`），局部波动率场景以 `mesher_vol = 0.5` 定界网格。BSM 与局部波动率中各有 9 个场景使用 400 个时间步；为满足共同误差预算，向上现金单触碰（`up-one-touch-cash-hit`）使用 1600 步，向上资产不触碰（`up-no-touch-asset-expiry`）使用 16000 步。

#### 3.3.1 BSM 一维有限差分（`fd_bsm`，误差预算 $3.0\times 10^{-3}$）

| 场景 ID | Kiyosi 引擎 | 时间步（K / Q） | 参考价格 | Kiyosi 绝对误差 | QuantLib 绝对误差 | Kiyosi 中位数 (IQR) | QuantLib 中位数 (IQR) | 加速比 ($Q/K$) |
| --- | --- | :---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `fd-bsm-european-call` | `FiniteDifferenceVanillaEngine` | 400 / 400 | 9.22700550815 | $4.83\times 10^{-5}$ | $7.08\times 10^{-5}$ | 1.07 ms (0.03 ms) | 6.18 ms (0.38 ms) | **5.81×** |
| `fd-bsm-american-put` | `FiniteDifferenceVanillaEngine` | 400 / 400 | 6.66068454589 | $1.11\times 10^{-3}$ | $1.20\times 10^{-3}$ | 1.14 ms (0.08 ms) | 8.04 ms (0.24 ms) | **7.08×** |
| `fd-bsm-cash-digital-call` | `FiniteDifferenceDigitalEngine` | 400 / 400 | 4.94581091053 | $8.78\times 10^{-6}$ | $6.84\times 10^{-5}$ | 1.05 ms (0.02 ms) | 6.23 ms (0.14 ms) | **5.92×** |
| `fd-bsm-asset-digital-put` | `FiniteDifferenceDigitalEngine` | 400 / 400 | 48.7733863768 | $3.19\times 10^{-5}$ | $8.01\times 10^{-4}$ | 1.06 ms (0.05 ms) | 6.04 ms (0.11 ms) | **5.71×** |
| `fd-bsm-down-out-call` | `FiniteDifferenceBarrierEngine` | 400 / 400 | 9.13330643650 | $2.32\times 10^{-5}$ | $1.61\times 10^{-6}$ | 1.06 ms (0.02 ms) | 6.12 ms (0.18 ms) | **5.80×** |
| `fd-bsm-terminal-down-out-cash` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 400 | 4.82180082739 | $1.42\times 10^{-5}$ | $1.47\times 10^{-4}$ | 1.02 ms (0.01 ms) | 6.13 ms (0.13 ms) | **6.00×** |
| `fd-bsm-terminal-up-in-asset` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 400 | 2.94955886912 | $3.56\times 10^{-5}$ | $5.60\times 10^{-5}$ | 2.04 ms (0.16 ms) | 13.71 ms (0.28 ms) | **6.73×** |
| `fd-bsm-down-no-touch-cash-expiry` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 400 | 7.13408843096 | $2.66\times 10^{-6}$ | $1.49\times 10^{-4}$ | 1.03 ms (0.05 ms) | 6.26 ms (0.19 ms) | **6.10×** |
| `fd-bsm-down-one-touch-asset-hit` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 400 | 19.4492167646 | $4.10\times 10^{-6}$ | $1.82\times 10^{-3}$ | 998.74 $\mu\text{s}$ (14.09 $\mu\text{s}$) | 6.10 ms (0.07 ms) | **6.11×** |
| `fd-bsm-up-one-touch-cash-hit` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 1600 | 3.69391182061 | $7.81\times 10^{-6}$ | $1.48\times 10^{-3}$ | 1.00 ms (0.01 ms) | 23.45 ms (0.48 ms) | **23.45×** |
| `fd-bsm-up-no-touch-asset-expiry` | `FiniteDifferenceBinaryBarrierEngine` | 400 / 16000 | 54.1403691157 | $1.01\times 10^{-4}$ | $1.77\times 10^{-3}$ | 1.01 ms (0.05 ms) | 234.20 ms (3.60 ms) | **230.97×** |

#### 3.3.2 局部波动率一维有限差分（`fd_local_vol`，误差预算 $5.0\times 10^{-3}$）

| 场景 ID | Kiyosi 引擎 | 时间步（K / Q） | 参考价格 | Kiyosi 绝对误差 | QuantLib 绝对误差 | Kiyosi 中位数 (IQR) | QuantLib 中位数 (IQR) | 加速比 ($Q/K$) |
| --- | --- | :---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `fd-local-vol-european-call` | `FiniteDifferenceVanillaEngine` | 100 / 400 | 11.0017427062 | $2.21\times 10^{-4}$ | $1.02\times 10^{-4}$ | 1.27 ms (0.03 ms) | 13.65 ms (0.25 ms) | **10.77×** |
| `fd-local-vol-american-put` | `FiniteDifferenceVanillaEngine` | 200 / 400 | 8.36106642823 | $2.16\times 10^{-3}$ | $1.24\times 10^{-3}$ | 2.50 ms (0.05 ms) | 15.71 ms (0.29 ms) | **6.27×** |
| `fd-local-vol-cash-digital-call` | `FiniteDifferenceDigitalEngine` | 100 / 400 | 5.39093949985 | $7.30\times 10^{-5}$ | $1.22\times 10^{-4}$ | 1.23 ms (0.05 ms) | 13.60 ms (0.47 ms) | **11.05×** |
| `fd-local-vol-asset-digital-put` | `FiniteDifferenceDigitalEngine` | 100 / 400 | 40.5303971416 | $1.67\times 10^{-3}$ | $1.95\times 10^{-3}$ | 1.23 ms (0.03 ms) | 13.97 ms (0.77 ms) | **11.34×** |
| `fd-local-vol-down-out-call` | `FiniteDifferenceBarrierEngine` | 100 / 400 | 10.3817423850 | $2.21\times 10^{-4}$ | $1.40\times 10^{-4}$ | 1.27 ms (0.03 ms) | 14.27 ms (1.03 ms) | **11.27×** |
| `fd-local-vol-terminal-down-out-cash` | `FiniteDifferenceBinaryBarrierEngine` | 100 / 400 | 4.83462680702 | $4.58\times 10^{-5}$ | $2.48\times 10^{-4}$ | 1.23 ms (0.04 ms) | 13.94 ms (0.71 ms) | **11.31×** |
| `fd-local-vol-terminal-up-in-asset` | `FiniteDifferenceBinaryBarrierEngine` | 100 / 400 | 3.48032683172 | $9.48\times 10^{-4}$ | $1.48\times 10^{-5}$ | 2.58 ms (0.15 ms) | 30.09 ms (1.88 ms) | **11.68×** |
| `fd-local-vol-down-no-touch-cash-expiry` | `FiniteDifferenceBinaryBarrierEngine` | 100 / 400 | 5.90771262187 | $1.27\times 10^{-4}$ | $2.35\times 10^{-4}$ | 1.22 ms (0.03 ms) | 13.77 ms (0.16 ms) | **11.25×** |
| `fd-local-vol-down-one-touch-asset-hit` | `FiniteDifferenceBinaryBarrierEngine` | 100 / 400 | 29.6031381560 | $9.64\times 10^{-4}$ | $1.03\times 10^{-3}$ | 1.22 ms (0.06 ms) | 13.90 ms (0.31 ms) | **11.41×** |
| `fd-local-vol-up-one-touch-cash-hit` | `FiniteDifferenceBinaryBarrierEngine` | 100 / 1600 | 4.51261775417 | $1.94\times 10^{-4}$ | $1.83\times 10^{-3}$ | 1.24 ms (0.08 ms) | 53.70 ms (1.72 ms) | **43.30×** |
| `fd-local-vol-up-no-touch-asset-expiry` | `FiniteDifferenceBinaryBarrierEngine` | 200 / 16000 | 44.3991225309 | $5.54\times 10^{-4}$ | $2.04\times 10^{-3}$ | 2.41 ms (0.11 ms) | 536.40 ms (5.22 ms) | **222.82×** |

**技术要点**：

- 在双方均采用 $800\times 400$ 网格的 9 个 BSM 场景中，加速比为 **5.71×–7.08×**。在 QuantLib 采用 400 个时间步（Kiyosi 为 100 或 200 步）的 9 个局部波动率场景中，加速比为 **6.27×–11.68×**。网格节点分布和时间推进方式也会影响误差与延迟。
- 为通过共同精度门禁，QuantLib 在向上现金单触碰与向上资产不触碰场景中分别使用 1600 和 16000 个时间步。此时向上现金单触碰在 BSM 与局部波动率下的加速比分别为 **23.45×** 和 **43.30×**，向上资产不触碰分别为 **230.97×** 和 **222.82×**。

---

### 3.4 Heston 随机波动率引擎（3 个场景）

共用市场与模型参数：$S = K = 100,\ r = 0.05,\ q = 0.02,\ v_0 = \theta = 0.04,\ \kappa = 1.5,\ \xi = 0.3,\ \rho = -0.7$，期限 1 年（`2025-01-01` 至 `2026-01-01`）。

| 场景 ID | 引擎 (`engine`) | 算法与配置对比（Kiyosi vs QuantLib） | 误差预算 | Kiyosi 绝对误差 | QuantLib 绝对误差 | Kiyosi 中位数 (IQR) | QuantLib 中位数 (IQR) | 加速比 ($Q/K$) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `heston-analytic-call` | `AnalyticHestonEuropeanEngine` | 自适应 Fourier + 确定性方差控制变量（$\text{tol}=10^{-9}$） vs Gatheral 自适应 Lobatto（$\text{rel\_tol}=10^{-9}$） | $1.00\times 10^{-7}$ | $2.31\times 10^{-14}$ | $1.95\times 10^{-14}$ | 13.46 $\mu\text{s}$ (0.73 $\mu\text{s}$) | 66.09 $\mu\text{s}$ (1.65 $\mu\text{s}$) | **4.91×** |
| `heston-fd-european-call` | `FiniteDifferenceHestonVanillaEngine` | MCS ADI ($\theta=1/3$), $200\times 50\times 200$ 区间 vs Hundsdorfer ADI, $200\times 100\times 200$ 节点 | $5.00\times 10^{-3}$ | $5.70\times 10^{-4}$ | $9.05\times 10^{-4}$ | 14.35 ms (0.44 ms) | 209.86 ms (2.18 ms) | **14.62×** |
| `heston-fd-american-put` | `FiniteDifferenceHestonVanillaEngine` | MCS ADI + Ikonen–Toivanen 分裂, $200\times 50\times 200$ vs Hundsdorfer + 投影, $200\times 100\times 200$ | $5.00\times 10^{-3}$ | $1.06\times 10^{-3}$ | $3.54\times 10^{-3}$ | 16.10 ms (1.08 ms) | 233.14 ms (3.32 ms) | **14.48×** |

**技术要点**：

- Heston 欧式场景的参考值由 Gatheral–Lobatto 与独立 exp-sinh Fourier 积分交叉校验，参考不确定度为 $10^{-11}$。两个被测解析引擎相对该参考值的绝对误差均约为 $2\times 10^{-14}$。
- Heston 二维有限差分中，Kiyosi 以对数现货和方差为坐标，现货上界为 400，方差范围为 $[0,0.6]$。时间推进使用 Modified Craig–Sneyd ADI 格式（$\theta=1/3$），美式行权采用 Ikonen–Toivanen 算子分裂。QuantLib 使用自动求解域、Hundsdorfer 格式与原生美式收益投影。所测配置下，Kiyosi 在欧式和美式场景中的绝对误差均更小，加速比分别为 **14.62×** 和 **14.48×**。

---

### 3.5 BSM 蒙特卡洛引擎（8 个场景）

全部场景采用伪随机抽样，关闭对偶变量（`antithetic = false`）与控制变量（`control_variate = false`）。Kiyosi 使用块流式 PCG32 + Box–Muller；QuantLib 使用 MT19937 + 逆正态分布。除计时种子 `seed = 1729` 外，双方均在 32 个预设验证种子（$1009 + 97i,\ i=0\dots 31$）上检验样本统计量。

欧式看涨、下敲出看涨和美式看跌分别运行 Kiyosi 的 1 线程和 8 线程配置。每一对场景只调整 Kiyosi 的工作线程数，沿用路径数、时间步数、种子、参考价格和误差门限。QuantLib 原生引擎在全部蒙特卡洛场景中以 1 个工作线程逐条处理路径。[QuantLib 1.44 路径采样循环](https://github.com/lballabio/QuantLib/blob/v1.44/ql/methods/montecarlo/montecarlomodel.hpp#L82-L113)

#### 3.5.1 计时种子精度与延迟表现（`seed = 1729`）

| 场景 ID | 引擎 (`engine`) | 工作线程（K / Q） | 物理路径数（K / Q） | 误差预算 | 参考价格 | Kiyosi 计时误差 | QuantLib 计时误差 | Kiyosi 中位数 (IQR) | QuantLib 中位数 (IQR) | 加速比 ($Q/K$) |
| --- | --- | :---: | :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `mc-european-call` | `MonteCarloVanillaEngine` | 1 / 1 | 131,072 / 262,144 | $0.10$ | 9.22700550815 | $6.38\times 10^{-2}$ | $3.14\times 10^{-2}$ | 3.02 ms (0.03 ms) | 31.60 ms (2.36 ms) | **10.47×** |
| `mc-european-call-8-workers` | `MonteCarloVanillaEngine` | 8 / 1 | 131,072 / 262,144 | $0.10$ | 9.22700550815 | $6.38\times 10^{-2}$ | $3.14\times 10^{-2}$ | 617.45 $\mu\text{s}$ (124.49 $\mu\text{s}$) | 33.19 ms (1.32 ms) | **53.75×** |
| `mc-european-put` | `MonteCarloVanillaEngine` | 1 / 1 | 65,536 / 65,536 | $0.10$ | 6.33008062755 | $1.58\times 10^{-2}$ | $4.47\times 10^{-2}$ | 1.46 ms (0.06 ms) | 7.95 ms (0.60 ms) | **5.44×** |
| `mc-barrier-down-out-call` | `MonteCarloBarrierEngine` | 1 / 1 | 65,536 / 131,072 | $0.10$ | 7.58695396974 | $9.38\times 10^{-2}$ | $3.13\times 10^{-2}$ | 3.21 ms (0.08 ms) | 20.35 ms (0.36 ms) | **6.35×** |
| `mc-barrier-down-out-call-8-workers` | `MonteCarloBarrierEngine` | 8 / 1 | 65,536 / 131,072 | $0.10$ | 7.58695396974 | $9.38\times 10^{-2}$ | $3.13\times 10^{-2}$ | 631.64 $\mu\text{s}$ (118.97 $\mu\text{s}$) | 21.22 ms (1.37 ms) | **33.59×** |
| `mc-barrier-up-in-put` | `MonteCarloBarrierEngine` | 1 / 1 | 65,536 / 65,536 | $0.10$ | 0.230613308713 | $2.17\times 10^{-3}$ | $3.01\times 10^{-5}$ | 3.34 ms (0.13 ms) | 10.27 ms (0.17 ms) | **3.07×** |
| `mc-american-put` | `MonteCarloVanillaEngine` | 1 / 1 | 65,536 / 65,536 (+32,768 校准) | $0.15$ | 6.66068454589 | $3.18\times 10^{-3}$ | $5.58\times 10^{-2}$ | 102.54 ms (1.79 ms) | 669.65 ms (12.63 ms) | **6.53×** |
| `mc-american-put-8-workers` | `MonteCarloVanillaEngine` | 8 / 1 | 65,536 / 65,536 (+32,768 校准) | $0.15$ | 6.66068454589 | $3.18\times 10^{-3}$ | $5.58\times 10^{-2}$ | 22.40 ms (2.98 ms) | 666.35 ms (7.49 ms) | **29.74×** |

#### 3.5.2 32 种子集合验证统计量（Seed Ensemble Validation）

每个线程配置独立验证。各验证种子的绝对误差、种子集合的 RMSE 以及有符号偏差的绝对值均加上参考不确定度后与对应门限比较。样本标准差直接与门限比较，括号内为种子均值的标准误（SE）。

| 场景 ID | 门禁上限（RMSE / \|Bias\| / StdDev） | Kiyosi RMSE | QuantLib RMSE | Kiyosi 有符号偏差 | QuantLib 有符号偏差 | Kiyosi 样本标准差 (SE) | QuantLib 样本标准差 (SE) | 最大绝对误差（K / Q） |
| --- | :---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `mc-european-call` | $0.05$ / $0.025$ / $0.05$ | $3.11\times 10^{-2}$ | $2.88\times 10^{-2}$ | $+2.85\times 10^{-3}$ | $-2.53\times 10^{-3}$ | $3.14\times 10^{-2}$ ($5.56\times 10^{-3}$) | $2.92\times 10^{-2}$ ($5.16\times 10^{-3}$) | $8.39\times 10^{-2}$ / $6.07\times 10^{-2}$ |
| `mc-european-call-8-workers` | $0.05$ / $0.025$ / $0.05$ | $3.11\times 10^{-2}$ | $2.88\times 10^{-2}$ | $+2.85\times 10^{-3}$ | $-2.53\times 10^{-3}$ | $3.14\times 10^{-2}$ ($5.56\times 10^{-3}$) | $2.92\times 10^{-2}$ ($5.16\times 10^{-3}$) | $8.39\times 10^{-2}$ / $6.07\times 10^{-2}$ |
| `mc-european-put` | $0.05$ / $0.025$ / $0.05$ | $2.70\times 10^{-2}$ | $3.52\times 10^{-2}$ | $-3.28\times 10^{-3}$ | $+1.85\times 10^{-2}$ | $2.72\times 10^{-2}$ ($4.81\times 10^{-3}$) | $3.04\times 10^{-2}$ ($5.37\times 10^{-3}$) | $4.49\times 10^{-2}$ / $8.08\times 10^{-2}$ |
| `mc-barrier-down-out-call` | $0.05$ / $0.025$ / $0.05$ | $3.45\times 10^{-2}$ | $3.66\times 10^{-2}$ | $+1.13\times 10^{-3}$ | $-7.45\times 10^{-3}$ | $3.51\times 10^{-2}$ ($6.20\times 10^{-3}$) | $3.64\times 10^{-2}$ ($6.43\times 10^{-3}$) | $6.64\times 10^{-2}$ / $9.87\times 10^{-2}$ |
| `mc-barrier-down-out-call-8-workers` | $0.05$ / $0.025$ / $0.05$ | $3.45\times 10^{-2}$ | $3.66\times 10^{-2}$ | $+1.13\times 10^{-3}$ | $-7.45\times 10^{-3}$ | $3.51\times 10^{-2}$ ($6.20\times 10^{-3}$) | $3.64\times 10^{-2}$ ($6.43\times 10^{-3}$) | $6.64\times 10^{-2}$ / $9.87\times 10^{-2}$ |
| `mc-barrier-up-in-put` | $0.05$ / $0.025$ / $0.05$ | $1.08\times 10^{-3}$ | $7.32\times 10^{-3}$ | $-5.32\times 10^{-5}$ | $+5.01\times 10^{-3}$ | $1.09\times 10^{-3}$ ($1.93\times 10^{-4}$) | $5.41\times 10^{-3}$ ($9.57\times 10^{-4}$) | $2.66\times 10^{-3}$ / $1.41\times 10^{-2}$ |
| `mc-american-put` | $0.075$ / $0.05$ / $0.075$ | $4.05\times 10^{-2}$ | $4.02\times 10^{-2}$ | $-2.41\times 10^{-2}$ | $-2.54\times 10^{-2}$ | $3.31\times 10^{-2}$ ($5.84\times 10^{-3}$) | $3.16\times 10^{-2}$ ($5.58\times 10^{-3}$) | $7.95\times 10^{-2}$ / $9.57\times 10^{-2}$ |
| `mc-american-put-8-workers` | $0.075$ / $0.05$ / $0.075$ | $4.05\times 10^{-2}$ | $4.02\times 10^{-2}$ | $-2.41\times 10^{-2}$ | $-2.54\times 10^{-2}$ | $3.31\times 10^{-2}$ ($5.84\times 10^{-3}$) | $3.16\times 10^{-2}$ ($5.58\times 10^{-3}$) | $7.95\times 10^{-2}$ / $9.57\times 10^{-2}$ |

**技术要点**：

- Kiyosi 直接计算布朗桥条件存活概率，QuantLib `MCBarrierEngine` 用固定种子（`seed = 5`）的辅助随机流抽样障碍穿越。在 `mc-barrier-up-in-put` 中，双方均用 65,536 条路径，Kiyosi 的加速比为 **3.07×**，32 种子 RMSE 分别为 Kiyosi $1.08\times 10^{-3}$、QuantLib $7.32\times 10^{-3}$。在 `mc-barrier-down-out-call` 中，Kiyosi 用 65,536 条路径得到 RMSE $0.0345$，QuantLib 用 131,072 条路径得到 RMSE $0.0366$，双方各用 1 个工作线程时，$Q/K$ 为 **6.35×**。
- **美式最小二乘蒙特卡洛（LSM）**：在 `mc-american-put`（65,536 条定价路径、50 个行权时间步、二次单项式基）中，Kiyosi 在实值（ITM）定价路径上直接做样本内回归拟合（基函数 $1, S/K, (S/K)^2$），而 QuantLib 在每次 `recalculate()` 中先独立模拟 32,768 条校准路径再模拟 65,536 条定价路径。根据 `report.json` 记录的 LSM 细化实验（`lsm_refinement`）：
  - 将定价路径翻倍至 $131{,}072$ 时，Kiyosi 与 QuantLib 的 32 种子 RMSE 分别降至 $0.0332$ 与 $0.0315$；
  - 在 $131{,}072$ 路径下将行权步从 50 加密至 100，Kiyosi 与 QuantLib 的种子均值变化仅为 $-0.00141$（$\text{SE}=0.00340$）与 $+0.00075$（$\text{SE}=0.00297$）；
  - 将 QuantLib 校准路径从 $32{,}768$ 翻倍至 $65{,}536$ 时，均值变化仅为 $+4.56\times 10^{-5}$（$\text{SE}=7.16\times 10^{-4}$）。
  双方各用 1 个工作线程时，32 种子 RMSE 分别为 Kiyosi $0.0405$、QuantLib $0.0402$，中位数延迟分别为 102.54 ms 和 669.65 ms，$Q/K$ 为 **6.53×**。

#### 3.5.3 Kiyosi 的 8 线程并行加速

并行加速比 $K_1/K_8$ 为同一合约及路径配置下，Kiyosi 使用 1 个工作线程和 8 个工作线程的中位数延迟之比。

| 场景 | Kiyosi 1 线程 | Kiyosi 8 线程 | 并行加速比（$K_1/K_8$） |
| --- | ---: | ---: | ---: |
| `mc-european-call` | 3.02 ms | 617.45 $\mu\text{s}$ | **4.89×** |
| `mc-barrier-down-out-call` | 3.21 ms | 631.64 $\mu\text{s}$ | **5.08×** |
| `mc-american-put` | 102.54 ms | 22.40 ms | **4.58×** |

---

## 4. 覆盖范围、局限与解读说明

1. **严格语义对齐与排除边界**：
   本基准覆盖 **20 类引擎（51 个语义单元）**，每类都能在相同合约条款、市场模型与算法类别下与 QuantLib 原生引擎对照。Kiyosi 其余 14 类引擎因缺乏直接等价的 QuantLib 原生实现而未纳入对比，包括：
   - 近似公式版本不同：`BjerksundStenslandVanillaEngine`（Kiyosi 实现 2002 版，QuantLib 为 1993 版）；
   - 结构化奇异产品无内置对应引擎：自动赎回（`Autocallable`）、累购累沽（`Accumulator`）的积分、有限差分与蒙特卡洛引擎，以及区间累计解析引擎（`AnalyticRangeAccrualEngine`）；
   - 离散／连续监控或算法语义差异：数字期权与连续平均亚式蒙特卡洛、双障碍／双触碰有限差分、障碍期权数值积分及数字期权 CRR 二叉树。
2. **加速比解读注意事项**：
   - **离散步数与路径数差异**：3 个 CRR 场景步数相同，9 个 BSM 一维有限差分场景空间与时间步数均相同；11 个局部波动率场景时间步数均有差异（其中向上资产不触碰为 200 步 vs 16,000 步，加速比 **222.82×**）。8 个蒙特卡洛场景中有 4 个场景的定价路径数相同，其中包括美式看跌的两种线程配置。QuantLib 在这两个场景中均另用 32,768 条独立校准路径。
   - **接口固有附加计算**：QuantLib 原生 `recalculate()` 在部分解析引擎和有限差分引擎中会同步计算 Greeks，在蒙特卡洛中会累计样本方差；Kiyosi 的 `price()` 仅计算价格标量（Greeks 由 `price_with_greeks()` 按需调用）。
   - 全量汇总同时包含 1 / 1 和 8 / 1 两种工作线程配置。8 / 1 场景的 $Q/K$ 衡量各后端按所列配置完成一次定价的延迟差异。Kiyosi 的并行扩展由同一场景的 $K_1/K_8$ 衡量，结果受合约、路径数和可用 CPU 影响。
