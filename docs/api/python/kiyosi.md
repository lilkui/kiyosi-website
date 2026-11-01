---
description: kiyosi 的 Python API 参考文档。
outline: [2, 4]
---

# `kiyosi`

Price derivatives with validated Rust contracts and engines.

## Notes

Domain failures raise a specific `KiyosiError` subclass:
`InvalidInputError`, `UnsupportedOperationError`, `ComputationFailureError`,
`RootNotBracketedError` or `NonConvergenceError`. Catch a subclass for one
failure category or `KiyosiError` for any domain failure. Representation
and signature errors use native Python exceptions; reported operational
failures use `OSError`. Internal Rust panics are separate from domain
exceptions; allocation exhaustion may terminate the process.

Contract and calendar dates require `datetime.date`, excluding datetime
instances. Instant inputs accept dates at midnight UTC or timezone-aware
datetimes normalized to UTC; naive datetimes are rejected. Numeric inputs
reject booleans and unintended lossy conversions.

Values own their data and expose read-only properties. Shared and distinct
instances support concurrent reads and pricing. Replacement creates a new
value. Long calculations release the GIL while borrowing immutable Rust
inputs for the duration of the call; short analytic calls may retain it.
Parallel Monte Carlo calls share a library-owned Rayon worker pool and keep
their own simulation buffers. The pool is sized from available CPUs on first
use and retained until process exit; it ignores `RAYON_NUM_THREADS` and leaves
the application's global Rayon pool unchanged. `thread_count` caps workers per
call without reserving them; one runs on the calling thread and zero selects
automatic sizing. Worker-creation failures raise `OSError` during pricing;
failed initialization can be retried by a later call.
For multiprocessing, use the `spawn` start method. Forking after the worker
pool has initialized leaves it unusable in the child process.

`Greek` accepts delta, gamma, speed, theta, charm, color, vega, volga, vanna,
zomma, rho and dividend_rho. Spot derivatives use spot units, volatility and rate
derivatives use percentage points (squared for volga), and time derivatives use calendar days
of forward valuation time. `PricingResult` leaves unavailable or
unrequested sensitivities as None; `require` raises if one is absent.
Volga is the second volatility derivative divided by 10000. Dividend rho is
the sensitivity to a parallel shift of the continuous dividend-yield curve,
divided by 100, holding other market inputs fixed.

Calls are synchronous, without core cancellation or signal polling. Python
signal handling, including `KeyboardInterrupt`, resumes when control
returns to Python.

## `ComputationFailureError`

Non-finite numerical result or unavailable computation state.

## `Greek`

```python
Greek = typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'volga', 'vanna', 'zomma', 'rho', 'dividend_rho']
```

## `InvalidInputError`

Invalid parameters, dates, schedules or contract history.

## `KiyosiError`

Base exception for structured domain failures.

## `NonConvergenceError`

Iteration or integration limit reached without convergence.

## `PricingResult`

Finite price and optional finite price sensitivities.

#### Notes

Unavailable or unrequested Greeks are None. Spot derivatives are per spot
unit, volatility/rate derivatives per percentage point (squared for volga), and time
derivatives per calendar day of forward valuation time.

### `charm`

Return charm, or None if unrequested or unavailable.

### `color`

Return color, or None if unrequested or unavailable.

### `delta`

Return delta, or None if unrequested or unavailable.

### `dividend_rho`

Return dividend rho per yield percentage point, or None if unavailable.

### `gamma`

Return gamma, or None if unrequested or unavailable.

### `price`

Return the finite price in contract payment units.

### `require`

```python
require(self, /, measure)
```

Return a requested Greek or raise when it is unavailable.

#### Parameters

- **`measure`** (`str`) — Greek name, such as delta or vega.
#### Returns

- `float` — Finite sensitivity in PricingResult reporting units.
#### Raises

- `UnsupportedOperationError` — If the measure was not requested or is undefined at this valuation.

### `rho`

Return rho, or None if unrequested or unavailable.

### `speed`

Return speed, or None if unrequested or unavailable.

### `theta`

Return theta, or None if unrequested or unavailable.

### `vanna`

Return vanna, or None if unrequested or unavailable.

### `vega`

Return vega, or None if unrequested or unavailable.

### `volga`

Return volga per squared volatility percentage point, or None if unavailable.

### `zomma`

Return zomma, or None if unrequested or unavailable.

## `RootNotBracketedError`

Supplied interval does not bracket a root in the engine's domain.

## `UnsupportedOperationError`

Unsupported pricing combination or unavailable result measure.

## `__version__`

```python
__version__ = '0.16.0'
```
