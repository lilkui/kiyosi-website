---
description: Python API reference for kiyosi.
outline: [2, 4]
---

# `kiyosi`

Python API for the kiyosi derivatives pricing core.

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

### Values

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

## `KiyosiError`

Core domain validation or pricing error.

#### Parameters

- **`message`** (`str`) — Human-readable diagnostic message. Callers should branch on ``category`` rather than parse this text.
#### Attributes

- **`category`** (`ErrorCategory`) — Stable machine-readable error category.

## `PricingResult`

Read-only mapping over the fixed risk-measure vocabulary.

Price uses instrument value units. Delta, gamma, and speed are per one spot unit,
squared spot unit, and cubed spot unit. Vega, vanna, and zomma are price, delta,
and gamma changes per one volatility percentage point (an absolute change of
0.01). Rho is per one interest-rate percentage point. Theta, charm, and color
are price, delta, and gamma changes per calendar day as valuation time moves
forward. Undefined or unsupported measures are None, never a zero sentinel.

#### Attributes

- **`price, delta, gamma, speed`** (`float or None`) — Price and first three spot derivatives.
- **`theta, charm, color`** (`float or None`) — Daily changes in price, delta, and gamma.
- **`vega, vanna, zomma`** (`float or None`) — Volatility-point changes in price, delta, and gamma.
- **`rho`** (`float or None`) — Price change per interest-rate percentage point.

### `__len__`

```python
__len__(self) -> int
```

### `__iter__`

```python
__iter__(self) -> collections.abc.Iterator[str]
```

### `__contains__`

```python
__contains__(self, arg: str, /) -> bool
```

### `__getitem__`

```python
__getitem__(self, arg: str, /) -> float | None
```

### `get`

```python
get(self, key: str, default: object | None = None) -> object
```

Return a measure by name.

#### Parameters

- **`key`** (`str`) — Lowercase risk-measure name.
- **`default`** (`object, optional`) — Value returned when ``key`` is unknown.
#### Returns

- `float, None, or object` — Measure value, ``None`` when unavailable, or ``default`` for an unknown key.

### `keys`

```python
keys(self) -> tuple
```

Return risk-measure names in stable order.

#### Returns

- `tuple[str, ...]` — Fixed lowercase risk-measure names.

### `values`

```python
values(self) -> tuple
```

Return risk-measure values in stable order.

#### Returns

- `tuple[float or None, ...]` — Values aligned with `keys`.

### `items`

```python
items(self) -> tuple
```

Return name-value pairs in stable order.

#### Returns

- `tuple[tuple[str, float or None], ...]` — Pairs aligned with `keys`.

### `require`

```python
require(self, measure: RiskMeasure) -> float
```

Return a required risk measure.

#### Parameters

- **`measure`** (`RiskMeasure`) — Measure to retrieve.
#### Returns

- `float` — Available measure value.
#### Raises

- `KiyosiError` — If the requested measure is unavailable.

### `price`

Instrument value, or None when unavailable.

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

## `RiskMeasure`

Risk measure stored by `PricingResult`.

#### Attributes

- `PRICE, DELTA, GAMMA, SPEED, THETA, CHARM, COLOR, VEGA, VANNA, ZOMMA, RHO` — Price or a supported first-, second-, or third-order sensitivity.

### Values

- `PRICE` = `0`
- `DELTA` = `1`
- `GAMMA` = `2`
- `SPEED` = `3`
- `THETA` = `4`
- `CHARM` = `5`
- `COLOR` = `6`
- `VEGA` = `7`
- `VANNA` = `8`
- `ZOMMA` = `9`
- `RHO` = `10`

## `__version__`

```python
__version__ = '0.5.0'
```
