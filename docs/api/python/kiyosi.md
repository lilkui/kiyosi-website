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
value. Long calculations release the GIL around owned Rust inputs; short
analytic calls may retain it.

`Greek` accepts delta, gamma, speed, theta, charm, color, vega, vanna,
zomma and rho. Spot derivatives use spot units, volatility and rate
derivatives use percentage points, and time derivatives use calendar days
of forward valuation time. `PricingResult` leaves unavailable or
unrequested sensitivities as None; `require` raises if one is absent.

Calls are synchronous, without core cancellation or signal polling. Python
signal handling, including `KeyboardInterrupt`, resumes when control
returns to Python.

## `ComputationFailureError`

Non-finite numerical result or unavailable computation state.

## `Greek`

```python
Greek = typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']
```

## `InvalidInputError`

Invalid parameters, dates, schedules or contract history.

## `KiyosiError`

Base exception for structured domain failures.

## `NonConvergenceError`

Iteration or integration limit reached without convergence.

## `PricingResult`

```python
PricingResult()
```

Finite price and optional finite price sensitivities.

#### Notes

Unavailable or unrequested Greeks are None. Spot derivatives are per spot
unit, volatility/rate derivatives per percentage point, and time
derivatives per calendar day of forward valuation time.

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

### `speed`

Return speed, or None if unrequested or unavailable.

### `charm`

Return charm, or None if unrequested or unavailable.

### `color`

Return color, or None if unrequested or unavailable.

### `rho`

Return rho, or None if unrequested or unavailable.

### `zomma`

Return zomma, or None if unrequested or unavailable.

### `price`

Return the finite price in contract payment units.

### `vanna`

Return vanna, or None if unrequested or unavailable.

### `delta`

Return delta, or None if unrequested or unavailable.

### `gamma`

Return gamma, or None if unrequested or unavailable.

### `vega`

Return vega, or None if unrequested or unavailable.

### `theta`

Return theta, or None if unrequested or unavailable.

## `RootNotBracketedError`

Supplied interval does not bracket a root in the engine's domain.

## `UnsupportedOperationError`

Unsupported pricing combination or unavailable result measure.

## `__version__`

```python
__version__ = '0.14.0'
```
