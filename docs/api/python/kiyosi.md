---
description: kiyosi 的 Python API 参考文档。
outline: [2, 4]
---

# `kiyosi`

Python API for the kiyosi derivatives pricing core.

## Failures and cancellation

Representation and signature errors use Python's built-in exceptions. Core domain
rejections and reported backend failures raise KiyosiError; inspect its category.
CUDA unavailability and execution failures use BACKEND_UNAVAILABLE and
BACKEND_FAILURE, and invalid numerical results use INVALID_RESULT.

Allocation failures, including CUDA device-memory exhaustion, raise MemoryError.
Other native runtime/internal exceptions use the binding's built-in exception
mappings; for example, entropy-source runtime failures raise RuntimeError.
Valid settings do not guarantee sufficient memory or other resources.

Pricing, Greeks and implied-value solves are synchronous. Scalar prices from the
AnalyticVanilla, AnalyticDigital, AnalyticBarrier, AnalyticBinaryBarrier,
AnalyticGeometricAveragePrice and TurnbullWakemanArithmeticAveragePrice engines
keep the GIL to avoid thread handoff overhead for short formulas, except that
scheduled AnalyticBarrier and AnalyticBinaryBarrier prices release it while
validating and pricing their observation schedules. AnalyticVanilla and
AnalyticDigital Greek requests also keep the GIL, as do delta-only requests for
the two Asian engines. Other scalar prices, Greek requests and implied-value
solves release it during core computation.
These calls provide no cancellation interface or signal polling within the core.
When they run on the main thread, Python signal handling, including
Ctrl-C/KeyboardInterrupt, is deferred until control returns to Python. It does not
stop an in-progress core computation or become a KiyosiError.

## `ErrorCategory`

Stable category for a core domain error.

#### Attributes

- `INVALID_OPTION` — Invalid or internally inconsistent instrument terms.
- `INVALID_STRIKE` — Invalid strike value.
- `INVALID_VOLATILITY` — Invalid volatility value.
- `INVALID_RISK_FREE_RATE` — Invalid risk-free rate.
- `INVALID_DIVIDEND_YIELD` — Invalid dividend yield.
- `INVALID_SPOT_PRICE` — Invalid spot price.
- `INVALID_DATE` — Invalid calendar date.
- `INVALID_TIME_RANGE` — Invalid or reversed time range.
- `INVALID_RESULT` — Missing or invalid pricing result.
- `INVALID_SCHEDULE` — Invalid observation schedule.
- `INVALID_CALENDAR` — Invalid trading calendar.
- `INVALID_PARAMETER` — Invalid numerical or engine parameter.
- `UNBRACKETED_VOLATILITY` — Observed price is not bracketed by the volatility bounds.
- `SOLVER_NON_CONVERGENCE` — A numerical solver exhausted its iteration limit.
- `SOLVER_NON_FINITE` — A numerical solver encountered a non-finite value.
- `UNBRACKETED_COUPON` — Observed price is not bracketed by the coupon bounds.
- `BACKEND_UNAVAILABLE` — Requested computation backend is unavailable.
- `BACKEND_FAILURE` — Requested computation backend failed.
- `UNSUPPORTED_OPERATION` — Engine or instrument does not support the requested operation.

### 枚举值

- `INVALID_OPTION` = `1`
- `INVALID_STRIKE` = `2`
- `INVALID_VOLATILITY` = `3`
- `INVALID_RISK_FREE_RATE` = `4`
- `INVALID_DIVIDEND_YIELD` = `5`
- `INVALID_SPOT_PRICE` = `6`
- `INVALID_DATE` = `7`
- `INVALID_TIME_RANGE` = `8`
- `INVALID_RESULT` = `9`
- `INVALID_SCHEDULE` = `10`
- `INVALID_CALENDAR` = `11`
- `INVALID_PARAMETER` = `12`
- `UNBRACKETED_VOLATILITY` = `13`
- `SOLVER_NON_CONVERGENCE` = `14`
- `SOLVER_NON_FINITE` = `15`
- `UNBRACKETED_COUPON` = `16`
- `BACKEND_UNAVAILABLE` = `17`
- `BACKEND_FAILURE` = `18`
- `UNSUPPORTED_OPERATION` = `19`

## `Greek`

```python
Greek = typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']
```

## `KiyosiError`

Core domain validation or pricing error.

#### Parameters

- **`message`** (`str`) — Human-readable diagnostic message. Callers should branch on ``category`` rather than parse this text.
#### Attributes

- **`category`** (`ErrorCategory`) — Stable machine-readable error category.

## `PricingResult`

Read-only price and Greek result.

Price uses instrument value units. Delta, gamma, and speed are per one spot unit,
squared spot unit, and cubed spot unit. Vega, vanna, and zomma are price, delta,
and gamma changes per one volatility percentage point (an absolute change of
0.01). Rho is per one interest-rate percentage point. Theta, charm, and color
are price, delta, and gamma changes per calendar day as valuation time moves
forward. Undefined or unsupported Greeks are None, never a zero sentinel.

#### Attributes

- **`price`** (`float`) — Instrument value.
- **`delta, gamma, speed`** (`float or None`) — First three spot derivatives.
- **`theta, charm, color`** (`float or None`) — Daily changes in price, delta, and gamma.
- **`vega, vanna, zomma`** (`float or None`) — Volatility-point changes in price, delta, and gamma.
- **`rho`** (`float or None`) — Price change per interest-rate percentage point.

### `require`

```python
require(self, measure: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']) -> float
```

Return a required Greek.

#### Parameters

- **`measure`** (`{'delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'}`) — Greek to retrieve.
#### Returns

- `float` — Available Greek value.
#### Raises

- `KiyosiError` — If the requested Greek is unavailable.

### `price`

Instrument value.

### `delta`

First spot derivative, or None when unavailable.

### `gamma`

Second spot derivative, or None when unavailable.

### `speed`

Third spot derivative, or None when unavailable.

### `theta`

Daily price decay, or None when unavailable.

### `charm`

Daily change in delta, or None when unavailable.

### `color`

Daily change in gamma, or None when unavailable.

### `vega`

Price change per volatility percentage point, or None.

### `vanna`

Delta change per volatility percentage point, or None.

### `zomma`

Gamma change per volatility percentage point, or None.

### `rho`

Price change per interest-rate percentage point, or None.

## `__version__`

```python
__version__ = '0.10.0'
```
