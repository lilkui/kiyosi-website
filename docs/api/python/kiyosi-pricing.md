---
description: kiyosi.pricing 的 Python API 参考文档。
outline: [2, 4]
---

# `kiyosi.pricing`

Pricing engines, analytics, and implied-value solvers.

## `AnalyticBarrierEngine`

```python
AnalyticBarrierEngine(self) -> None
```

Stateless pricing engine.

The engine has no configuration and may be reused across supported instruments
and contexts. Concurrent calls are safe.

Scheduled monitoring is approximated with a BGK barrier shift. Untouched contracts
with future observations require a final observation at expiry; shorter monitoring
windows raise KiyosiError with category UNSUPPORTED_OPERATION. Spot must lie strictly
on the unbreached side of the shifted barrier; otherwise the approximation raises
the same error. Resolved settlements remain supported.

### 构造函数

Create a stateless pricing engine.

#### Returns

- `pricing engine` — Reusable engine with no mutable configuration.

### `price`

```python
price(self, instrument: BarrierOption, context: PricingContext) -> float
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `float` — Instrument price. No Greeks are calculated.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

### `price_with_greeks`

```python
price_with_greeks(self, instrument: BarrierOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
```

Compute price and the explicitly selected Greeks.

Pass one lowercase Greek name or an iterable of them, or set ``all_greeks=True`` to
request all ten. These forms are mutually exclusive. Native values are reused;
missing feasible measures use numerical price differences. Unrequested or
undefined measures are None, never zero sentinels. At expiry or a monitored
barrier hit-state boundary, only price is available. Feasible bumped valuation
failures fail the entire operation.
At current autocallable-product event thresholds, undefined spot and time
sensitivities remain None while feasible rate and volatility sensitivities survive.

Shift keyword arguments are absolute and use core-owned defaults. Spot shifts
use asset-price units, volatility and rate shifts use decimal units, and time
shifts use calendar days. Collapsed or asymmetric stencils leave affected
numerical Greeks unavailable. Monte Carlo valuations share one seed per request
without changing the engine. Concurrent calls are safe.
For American Monte Carlo, omitted or None spot_shift uses 8% of spot to reduce
exercise-decision sampling noise. Explicit shifts remain absolute. Sampling error
and bump-size bias remain; check convergence for the valuation.

#### Returns

- `PricingResult` — Price and requested available Greeks, with Greek units.
#### Raises

- `TypeError` — If a Greek representation, engine/instrument pairing, or shift representation is incompatible.
- `OverflowError` — If time_shift_days is outside the C++ int range.
- `KiyosiError` — If the Greek request or settings are invalid, or a required valuation fails.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

## `AnalyticBinaryBarrierEngine`

```python
AnalyticBinaryBarrierEngine(self) -> None
```

Stateless pricing engine.

The engine has no configuration and may be reused across supported instruments
and contexts. Concurrent calls are safe.

Scheduled monitoring is approximated with a BGK barrier shift. Untouched contracts
with future observations require a final observation at expiry; shorter monitoring
windows raise KiyosiError with category UNSUPPORTED_OPERATION. Spot must lie strictly
on the unbreached side of the shifted barrier; otherwise the approximation raises
the same error. Resolved settlements remain supported.

### 构造函数

Create a stateless pricing engine.

#### Returns

- `pricing engine` — Reusable engine with no mutable configuration.

### `price`

```python
price(self, instrument: BinaryBarrierOption, context: PricingContext) -> float
price(self, instrument: TouchOption, context: PricingContext) -> float
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `float` — Instrument price. No Greeks are calculated.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

### `price_with_greeks`

```python
price_with_greeks(self, instrument: BinaryBarrierOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
price_with_greeks(self, instrument: TouchOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
```

Compute price and the explicitly selected Greeks.

Pass one lowercase Greek name or an iterable of them, or set ``all_greeks=True`` to
request all ten. These forms are mutually exclusive. Native values are reused;
missing feasible measures use numerical price differences. Unrequested or
undefined measures are None, never zero sentinels. At expiry or a monitored
barrier hit-state boundary, only price is available. Feasible bumped valuation
failures fail the entire operation.
At current autocallable-product event thresholds, undefined spot and time
sensitivities remain None while feasible rate and volatility sensitivities survive.

Shift keyword arguments are absolute and use core-owned defaults. Spot shifts
use asset-price units, volatility and rate shifts use decimal units, and time
shifts use calendar days. Collapsed or asymmetric stencils leave affected
numerical Greeks unavailable. Monte Carlo valuations share one seed per request
without changing the engine. Concurrent calls are safe.
For American Monte Carlo, omitted or None spot_shift uses 8% of spot to reduce
exercise-decision sampling noise. Explicit shifts remain absolute. Sampling error
and bump-size bias remain; check convergence for the valuation.

#### Returns

- `PricingResult` — Price and requested available Greeks, with Greek units.
#### Raises

- `TypeError` — If a Greek representation, engine/instrument pairing, or shift representation is incompatible.
- `OverflowError` — If time_shift_days is outside the C++ int range.
- `KiyosiError` — If the Greek request or settings are invalid, or a required valuation fails.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

## `AnalyticDigitalEngine`

```python
AnalyticDigitalEngine(self) -> None
```

Stateless pricing engine.

The engine has no configuration and may be reused across supported instruments
and contexts. Concurrent calls are safe.

### 构造函数

Create a stateless pricing engine.

#### Returns

- `pricing engine` — Reusable engine with no mutable configuration.

### `price`

```python
price(self, instrument: CashOrNothingOption, context: PricingContext) -> float
price(self, instrument: AssetOrNothingOption, context: PricingContext) -> float
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `float` — Instrument price. No Greeks are calculated.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

### `price_with_greeks`

```python
price_with_greeks(self, instrument: CashOrNothingOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
price_with_greeks(self, instrument: AssetOrNothingOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
```

Compute price and the explicitly selected Greeks.

Pass one lowercase Greek name or an iterable of them, or set ``all_greeks=True`` to
request all ten. These forms are mutually exclusive. Native values are reused;
missing feasible measures use numerical price differences. Unrequested or
undefined measures are None, never zero sentinels. At expiry or a monitored
barrier hit-state boundary, only price is available. Feasible bumped valuation
failures fail the entire operation.
At current autocallable-product event thresholds, undefined spot and time
sensitivities remain None while feasible rate and volatility sensitivities survive.

Shift keyword arguments are absolute and use core-owned defaults. Spot shifts
use asset-price units, volatility and rate shifts use decimal units, and time
shifts use calendar days. Collapsed or asymmetric stencils leave affected
numerical Greeks unavailable. Monte Carlo valuations share one seed per request
without changing the engine. Concurrent calls are safe.
For American Monte Carlo, omitted or None spot_shift uses 8% of spot to reduce
exercise-decision sampling noise. Explicit shifts remain absolute. Sampling error
and bump-size bias remain; check convergence for the valuation.

#### Returns

- `PricingResult` — Price and requested available Greeks, with Greek units.
#### Raises

- `TypeError` — If a Greek representation, engine/instrument pairing, or shift representation is incompatible.
- `OverflowError` — If time_shift_days is outside the C++ int range.
- `KiyosiError` — If the Greek request or settings are invalid, or a required valuation fails.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

## `AnalyticGeometricAveragePriceEngine`

```python
AnalyticGeometricAveragePriceEngine(self) -> None
```

Stateless pricing engine.

The engine has no configuration and may be reused across supported instruments
and contexts. Concurrent calls are safe.

### 构造函数

Create a stateless pricing engine.

#### Returns

- `pricing engine` — Reusable engine with no mutable configuration.

### `price`

```python
price(self, instrument: GeometricAveragePriceOption, context: PricingContext) -> float
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `float` — Instrument price. No Greeks are calculated.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

### `price_with_greeks`

```python
price_with_greeks(self, instrument: GeometricAveragePriceOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
```

Compute price and the explicitly selected Greeks.

Pass one lowercase Greek name or an iterable of them, or set ``all_greeks=True`` to
request all ten. These forms are mutually exclusive. Native values are reused;
missing feasible measures use numerical price differences. Unrequested or
undefined measures are None, never zero sentinels. At expiry or a monitored
barrier hit-state boundary, only price is available. Feasible bumped valuation
failures fail the entire operation.
At current autocallable-product event thresholds, undefined spot and time
sensitivities remain None while feasible rate and volatility sensitivities survive.

Shift keyword arguments are absolute and use core-owned defaults. Spot shifts
use asset-price units, volatility and rate shifts use decimal units, and time
shifts use calendar days. Collapsed or asymmetric stencils leave affected
numerical Greeks unavailable. Monte Carlo valuations share one seed per request
without changing the engine. Concurrent calls are safe.
For American Monte Carlo, omitted or None spot_shift uses 8% of spot to reduce
exercise-decision sampling noise. Explicit shifts remain absolute. Sampling error
and bump-size bias remain; check convergence for the valuation.

#### Returns

- `PricingResult` — Price and requested available Greeks, with Greek units.
#### Raises

- `TypeError` — If a Greek representation, engine/instrument pairing, or shift representation is incompatible.
- `OverflowError` — If time_shift_days is outside the C++ int range.
- `KiyosiError` — If the Greek request or settings are invalid, or a required valuation fails.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

## `AnalyticVanillaEngine`

```python
AnalyticVanillaEngine(self) -> None
```

Stateless pricing engine.

The engine has no configuration and may be reused across supported instruments
and contexts. Concurrent calls are safe.

### 构造函数

Create a stateless pricing engine.

#### Returns

- `pricing engine` — Reusable engine with no mutable configuration.

### `price`

```python
price(self, instrument: EuropeanOption, context: PricingContext) -> float
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `float` — Instrument price. No Greeks are calculated.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

### `price_with_greeks`

```python
price_with_greeks(self, instrument: EuropeanOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
```

Compute price and the explicitly selected Greeks.

Pass one lowercase Greek name or an iterable of them, or set ``all_greeks=True`` to
request all ten. These forms are mutually exclusive. Native values are reused;
missing feasible measures use numerical price differences. Unrequested or
undefined measures are None, never zero sentinels. At expiry or a monitored
barrier hit-state boundary, only price is available. Feasible bumped valuation
failures fail the entire operation.
At current autocallable-product event thresholds, undefined spot and time
sensitivities remain None while feasible rate and volatility sensitivities survive.

Shift keyword arguments are absolute and use core-owned defaults. Spot shifts
use asset-price units, volatility and rate shifts use decimal units, and time
shifts use calendar days. Collapsed or asymmetric stencils leave affected
numerical Greeks unavailable. Monte Carlo valuations share one seed per request
without changing the engine. Concurrent calls are safe.
For American Monte Carlo, omitted or None spot_shift uses 8% of spot to reduce
exercise-decision sampling noise. Explicit shifts remain absolute. Sampling error
and bump-size bias remain; check convergence for the valuation.

#### Returns

- `PricingResult` — Price and requested available Greeks, with Greek units.
#### Raises

- `TypeError` — If a Greek representation, engine/instrument pairing, or shift representation is incompatible.
- `OverflowError` — If time_shift_days is outside the C++ int range.
- `KiyosiError` — If the Greek request or settings are invalid, or a required valuation fails.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

## `BjerksundStenslandVanillaEngine`

```python
BjerksundStenslandVanillaEngine(self) -> None
```

Stateless pricing engine.

The engine has no configuration and may be reused across supported instruments
and contexts. Concurrent calls are safe.

### 构造函数

Create a stateless pricing engine.

#### Returns

- `pricing engine` — Reusable engine with no mutable configuration.

### `price`

```python
price(self, instrument: AmericanOption, context: PricingContext) -> float
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `float` — Instrument price. No Greeks are calculated.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

### `price_with_greeks`

```python
price_with_greeks(self, instrument: AmericanOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
```

Compute price and the explicitly selected Greeks.

Pass one lowercase Greek name or an iterable of them, or set ``all_greeks=True`` to
request all ten. These forms are mutually exclusive. Native values are reused;
missing feasible measures use numerical price differences. Unrequested or
undefined measures are None, never zero sentinels. At expiry or a monitored
barrier hit-state boundary, only price is available. Feasible bumped valuation
failures fail the entire operation.
At current autocallable-product event thresholds, undefined spot and time
sensitivities remain None while feasible rate and volatility sensitivities survive.

Shift keyword arguments are absolute and use core-owned defaults. Spot shifts
use asset-price units, volatility and rate shifts use decimal units, and time
shifts use calendar days. Collapsed or asymmetric stencils leave affected
numerical Greeks unavailable. Monte Carlo valuations share one seed per request
without changing the engine. Concurrent calls are safe.
For American Monte Carlo, omitted or None spot_shift uses 8% of spot to reduce
exercise-decision sampling noise. Explicit shifts remain absolute. Sampling error
and bump-size bias remain; check convergence for the valuation.

#### Returns

- `PricingResult` — Price and requested available Greeks, with Greek units.
#### Raises

- `TypeError` — If a Greek representation, engine/instrument pairing, or shift representation is incompatible.
- `OverflowError` — If time_shift_days is outside the C++ int range.
- `KiyosiError` — If the Greek request or settings are invalid, or a required valuation fails.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

## `CouponQuoteConvention`

```python
CouponQuoteConvention = typing.Literal['shift_maturity_coupon', 'preserve_maturity_coupon']
```

## `CoxRossRubinsteinVanillaEngine`

```python
CoxRossRubinsteinVanillaEngine(self, step_count: int = 256) -> None
```

Cox-Ross-Rubinstein binomial vanilla-option engine.

Configuration is immutable and validated at construction. Market-dependent tree
constraints are checked when pricing.

### 构造函数

Create an engine with validated Cox-Ross-Rubinstein settings.

#### Parameters

- **`step_count`** (`int, optional`) — Number of binomial time steps. Uses the core default when omitted.
#### Raises

- `TypeError` — If ``step_count`` is not an integer.
- `OverflowError` — If ``step_count`` is outside the C++ ``int`` range.
- `KiyosiError` — INVALID_PARAMETER if the step count is outside 1..1,000,000.
#### Notes

The step count is validated at construction; accepted range is 1..1,000,000.

### `step_count`

Number of binomial time steps.

### `price`

```python
price(self, instrument: EuropeanOption, context: PricingContext) -> float
price(self, instrument: AmericanOption, context: PricingContext) -> float
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `float` — Instrument price. No Greeks are calculated.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

### `price_with_greeks`

```python
price_with_greeks(self, instrument: EuropeanOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
price_with_greeks(self, instrument: AmericanOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
```

Compute price and the explicitly selected Greeks.

Pass one lowercase Greek name or an iterable of them, or set ``all_greeks=True`` to
request all ten. These forms are mutually exclusive. Native values are reused;
missing feasible measures use numerical price differences. Unrequested or
undefined measures are None, never zero sentinels. At expiry or a monitored
barrier hit-state boundary, only price is available. Feasible bumped valuation
failures fail the entire operation.
At current autocallable-product event thresholds, undefined spot and time
sensitivities remain None while feasible rate and volatility sensitivities survive.

Shift keyword arguments are absolute and use core-owned defaults. Spot shifts
use asset-price units, volatility and rate shifts use decimal units, and time
shifts use calendar days. Collapsed or asymmetric stencils leave affected
numerical Greeks unavailable. Monte Carlo valuations share one seed per request
without changing the engine. Concurrent calls are safe.
For American Monte Carlo, omitted or None spot_shift uses 8% of spot to reduce
exercise-decision sampling noise. Explicit shifts remain absolute. Sampling error
and bump-size bias remain; check convergence for the valuation.

#### Returns

- `PricingResult` — Price and requested available Greeks, with Greek units.
#### Raises

- `TypeError` — If a Greek representation, engine/instrument pairing, or shift representation is incompatible.
- `OverflowError` — If time_shift_days is outside the C++ int range.
- `KiyosiError` — If the Greek request or settings are invalid, or a required valuation fails.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

## `FiniteDifferenceAccumulatorEngine`

```python
FiniteDifferenceAccumulatorEngine(self, *, asset_step_count: int = 200, time_step_count: int = 200, scheme: typing.Literal['explicit_euler', 'implicit_euler', 'crank_nicolson'] = 'crank_nicolson', asset_upper_boundary: float | None = None) -> None
```

Finite-difference pricing engine with immutable configuration.

Configuration is validated at construction. Contract, market, and backend availability
are checked when pricing.
Vanilla, digital, and barrier engines accept 3..10,000 asset steps and 1..100,000
time steps. Accumulator and autocallable engines accept 3..2,000 asset steps and
1..2,000 time steps.

### 构造函数

Create an engine with validated finite-difference settings.

Settings are validated at construction.
The engine-specific ranges are listed in the engine class documentation.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial grid steps. Uses the core default when omitted.
- **`time_step_count`** (`int, optional`) — Number of time grid steps. Uses the core default when omitted.
- **`scheme`** (`{'explicit_euler', 'implicit_euler', 'crank_nicolson'}, optional`) — Time-stepping scheme. Uses the core default when omitted.
- **`asset_upper_boundary`** (`float or None, optional`) — Explicit upper asset-grid boundary, or ``None`` for the core default.
#### Raises

- `TypeError` — If a setting has an incompatible representation.
- `OverflowError` — If an integer setting is outside the C++ ``int`` range.
- `KiyosiError` — INVALID_PARAMETER if the core rejects the configuration.

### `asset_step_count`

Number of spatial grid steps.

### `time_step_count`

Number of time grid steps.

### `scheme`

Finite-difference time-stepping scheme.

### `asset_upper_boundary`

Explicit upper asset-grid boundary, or None for the core default.

### `price`

```python
price(self, instrument: Accumulator, context: PricingContext) -> float
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `float` — Instrument price. No Greeks are calculated.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

### `price_with_greeks`

```python
price_with_greeks(self, instrument: Accumulator, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
```

Compute price and the explicitly selected Greeks.

Pass one lowercase Greek name or an iterable of them, or set ``all_greeks=True`` to
request all ten. These forms are mutually exclusive. Native values are reused;
missing feasible measures use numerical price differences. Unrequested or
undefined measures are None, never zero sentinels. At expiry or a monitored
barrier hit-state boundary, only price is available. Feasible bumped valuation
failures fail the entire operation.
At current autocallable-product event thresholds, undefined spot and time
sensitivities remain None while feasible rate and volatility sensitivities survive.

Shift keyword arguments are absolute and use core-owned defaults. Spot shifts
use asset-price units, volatility and rate shifts use decimal units, and time
shifts use calendar days. Collapsed or asymmetric stencils leave affected
numerical Greeks unavailable. Monte Carlo valuations share one seed per request
without changing the engine. Concurrent calls are safe.
For American Monte Carlo, omitted or None spot_shift uses 8% of spot to reduce
exercise-decision sampling noise. Explicit shifts remain absolute. Sampling error
and bump-size bias remain; check convergence for the valuation.

#### Returns

- `PricingResult` — Price and requested available Greeks, with Greek units.
#### Raises

- `TypeError` — If a Greek representation, engine/instrument pairing, or shift representation is incompatible.
- `OverflowError` — If time_shift_days is outside the C++ int range.
- `KiyosiError` — If the Greek request or settings are invalid, or a required valuation fails.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

## `FiniteDifferenceAutocallableEngine`

```python
FiniteDifferenceAutocallableEngine(self, *, asset_step_count: int = 200, time_step_count: int = 200, scheme: typing.Literal['explicit_euler', 'implicit_euler', 'crank_nicolson'] = 'crank_nicolson', asset_upper_boundary: float | None = None) -> None
```

Finite-difference pricing engine with immutable configuration.

Configuration is validated at construction. Contract, market, and backend availability
are checked when pricing.
Vanilla, digital, and barrier engines accept 3..10,000 asset steps and 1..100,000
time steps. Accumulator and autocallable engines accept 3..2,000 asset steps and
1..2,000 time steps.

### 构造函数

Create an engine with validated finite-difference settings.

Settings are validated at construction.
The engine-specific ranges are listed in the engine class documentation.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial grid steps. Uses the core default when omitted.
- **`time_step_count`** (`int, optional`) — Number of time grid steps. Uses the core default when omitted.
- **`scheme`** (`{'explicit_euler', 'implicit_euler', 'crank_nicolson'}, optional`) — Time-stepping scheme. Uses the core default when omitted.
- **`asset_upper_boundary`** (`float or None, optional`) — Explicit upper asset-grid boundary, or ``None`` for the core default.
#### Raises

- `TypeError` — If a setting has an incompatible representation.
- `OverflowError` — If an integer setting is outside the C++ ``int`` range.
- `KiyosiError` — INVALID_PARAMETER if the core rejects the configuration.

### `asset_step_count`

Number of spatial grid steps.

### `time_step_count`

Number of time grid steps.

### `scheme`

Finite-difference time-stepping scheme.

### `asset_upper_boundary`

Explicit upper asset-grid boundary, or None for the core default.

### `price`

```python
price(self, instrument: SnowballOption, context: PricingContext) -> float
price(self, instrument: BinarySnowballOption, context: PricingContext) -> float
price(self, instrument: TernarySnowballOption, context: PricingContext) -> float
price(self, instrument: PhoenixOption, context: PricingContext) -> float
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `float` — Instrument price. No Greeks are calculated.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

### `price_with_greeks`

```python
price_with_greeks(self, instrument: SnowballOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
price_with_greeks(self, instrument: BinarySnowballOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
price_with_greeks(self, instrument: TernarySnowballOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
price_with_greeks(self, instrument: PhoenixOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
```

Compute price and the explicitly selected Greeks.

Pass one lowercase Greek name or an iterable of them, or set ``all_greeks=True`` to
request all ten. These forms are mutually exclusive. Native values are reused;
missing feasible measures use numerical price differences. Unrequested or
undefined measures are None, never zero sentinels. At expiry or a monitored
barrier hit-state boundary, only price is available. Feasible bumped valuation
failures fail the entire operation.
At current autocallable-product event thresholds, undefined spot and time
sensitivities remain None while feasible rate and volatility sensitivities survive.

Shift keyword arguments are absolute and use core-owned defaults. Spot shifts
use asset-price units, volatility and rate shifts use decimal units, and time
shifts use calendar days. Collapsed or asymmetric stencils leave affected
numerical Greeks unavailable. Monte Carlo valuations share one seed per request
without changing the engine. Concurrent calls are safe.
For American Monte Carlo, omitted or None spot_shift uses 8% of spot to reduce
exercise-decision sampling noise. Explicit shifts remain absolute. Sampling error
and bump-size bias remain; check convergence for the valuation.

#### Returns

- `PricingResult` — Price and requested available Greeks, with Greek units.
#### Raises

- `TypeError` — If a Greek representation, engine/instrument pairing, or shift representation is incompatible.
- `OverflowError` — If time_shift_days is outside the C++ int range.
- `KiyosiError` — If the Greek request or settings are invalid, or a required valuation fails.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

## `FiniteDifferenceBarrierEngine`

```python
FiniteDifferenceBarrierEngine(self, *, asset_step_count: int = 200, time_step_count: int = 200, scheme: typing.Literal['explicit_euler', 'implicit_euler', 'crank_nicolson'] = 'crank_nicolson', asset_upper_boundary: float | None = None) -> None
```

Finite-difference pricing engine with immutable configuration.

Configuration is validated at construction. Contract, market, and backend availability
are checked when pricing.
Vanilla, digital, and barrier engines accept 3..10,000 asset steps and 1..100,000
time steps. Accumulator and autocallable engines accept 3..2,000 asset steps and
1..2,000 time steps.

### 构造函数

Create an engine with validated finite-difference settings.

Settings are validated at construction.
The engine-specific ranges are listed in the engine class documentation.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial grid steps. Uses the core default when omitted.
- **`time_step_count`** (`int, optional`) — Number of time grid steps. Uses the core default when omitted.
- **`scheme`** (`{'explicit_euler', 'implicit_euler', 'crank_nicolson'}, optional`) — Time-stepping scheme. Uses the core default when omitted.
- **`asset_upper_boundary`** (`float or None, optional`) — Explicit upper asset-grid boundary, or ``None`` for the core default.
#### Raises

- `TypeError` — If a setting has an incompatible representation.
- `OverflowError` — If an integer setting is outside the C++ ``int`` range.
- `KiyosiError` — INVALID_PARAMETER if the core rejects the configuration.

### `asset_step_count`

Number of spatial grid steps.

### `time_step_count`

Number of time grid steps.

### `scheme`

Finite-difference time-stepping scheme.

### `asset_upper_boundary`

Explicit upper asset-grid boundary, or None for the core default.

### `price`

```python
price(self, instrument: BarrierOption, context: PricingContext) -> float
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `float` — Instrument price. No Greeks are calculated.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

### `price_with_greeks`

```python
price_with_greeks(self, instrument: BarrierOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
```

Compute price and the explicitly selected Greeks.

Pass one lowercase Greek name or an iterable of them, or set ``all_greeks=True`` to
request all ten. These forms are mutually exclusive. Native values are reused;
missing feasible measures use numerical price differences. Unrequested or
undefined measures are None, never zero sentinels. At expiry or a monitored
barrier hit-state boundary, only price is available. Feasible bumped valuation
failures fail the entire operation.
At current autocallable-product event thresholds, undefined spot and time
sensitivities remain None while feasible rate and volatility sensitivities survive.

Shift keyword arguments are absolute and use core-owned defaults. Spot shifts
use asset-price units, volatility and rate shifts use decimal units, and time
shifts use calendar days. Collapsed or asymmetric stencils leave affected
numerical Greeks unavailable. Monte Carlo valuations share one seed per request
without changing the engine. Concurrent calls are safe.
For American Monte Carlo, omitted or None spot_shift uses 8% of spot to reduce
exercise-decision sampling noise. Explicit shifts remain absolute. Sampling error
and bump-size bias remain; check convergence for the valuation.

#### Returns

- `PricingResult` — Price and requested available Greeks, with Greek units.
#### Raises

- `TypeError` — If a Greek representation, engine/instrument pairing, or shift representation is incompatible.
- `OverflowError` — If time_shift_days is outside the C++ int range.
- `KiyosiError` — If the Greek request or settings are invalid, or a required valuation fails.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

## `FiniteDifferenceDigitalEngine`

```python
FiniteDifferenceDigitalEngine(self, *, asset_step_count: int = 200, time_step_count: int = 200, scheme: typing.Literal['explicit_euler', 'implicit_euler', 'crank_nicolson'] = 'crank_nicolson', asset_upper_boundary: float | None = None) -> None
```

Finite-difference pricing engine with immutable configuration.

Configuration is validated at construction. Contract, market, and backend availability
are checked when pricing.
Vanilla, digital, and barrier engines accept 3..10,000 asset steps and 1..100,000
time steps. Accumulator and autocallable engines accept 3..2,000 asset steps and
1..2,000 time steps.

### 构造函数

Create an engine with validated finite-difference settings.

Settings are validated at construction.
The engine-specific ranges are listed in the engine class documentation.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial grid steps. Uses the core default when omitted.
- **`time_step_count`** (`int, optional`) — Number of time grid steps. Uses the core default when omitted.
- **`scheme`** (`{'explicit_euler', 'implicit_euler', 'crank_nicolson'}, optional`) — Time-stepping scheme. Uses the core default when omitted.
- **`asset_upper_boundary`** (`float or None, optional`) — Explicit upper asset-grid boundary, or ``None`` for the core default.
#### Raises

- `TypeError` — If a setting has an incompatible representation.
- `OverflowError` — If an integer setting is outside the C++ ``int`` range.
- `KiyosiError` — INVALID_PARAMETER if the core rejects the configuration.

### `asset_step_count`

Number of spatial grid steps.

### `time_step_count`

Number of time grid steps.

### `scheme`

Finite-difference time-stepping scheme.

### `asset_upper_boundary`

Explicit upper asset-grid boundary, or None for the core default.

### `price`

```python
price(self, instrument: CashOrNothingOption, context: PricingContext) -> float
price(self, instrument: AssetOrNothingOption, context: PricingContext) -> float
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `float` — Instrument price. No Greeks are calculated.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

### `price_with_greeks`

```python
price_with_greeks(self, instrument: CashOrNothingOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
price_with_greeks(self, instrument: AssetOrNothingOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
```

Compute price and the explicitly selected Greeks.

Pass one lowercase Greek name or an iterable of them, or set ``all_greeks=True`` to
request all ten. These forms are mutually exclusive. Native values are reused;
missing feasible measures use numerical price differences. Unrequested or
undefined measures are None, never zero sentinels. At expiry or a monitored
barrier hit-state boundary, only price is available. Feasible bumped valuation
failures fail the entire operation.
At current autocallable-product event thresholds, undefined spot and time
sensitivities remain None while feasible rate and volatility sensitivities survive.

Shift keyword arguments are absolute and use core-owned defaults. Spot shifts
use asset-price units, volatility and rate shifts use decimal units, and time
shifts use calendar days. Collapsed or asymmetric stencils leave affected
numerical Greeks unavailable. Monte Carlo valuations share one seed per request
without changing the engine. Concurrent calls are safe.
For American Monte Carlo, omitted or None spot_shift uses 8% of spot to reduce
exercise-decision sampling noise. Explicit shifts remain absolute. Sampling error
and bump-size bias remain; check convergence for the valuation.

#### Returns

- `PricingResult` — Price and requested available Greeks, with Greek units.
#### Raises

- `TypeError` — If a Greek representation, engine/instrument pairing, or shift representation is incompatible.
- `OverflowError` — If time_shift_days is outside the C++ int range.
- `KiyosiError` — If the Greek request or settings are invalid, or a required valuation fails.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

## `FiniteDifferenceScheme`

```python
FiniteDifferenceScheme = typing.Literal['explicit_euler', 'implicit_euler', 'crank_nicolson']
```

## `FiniteDifferenceVanillaEngine`

```python
FiniteDifferenceVanillaEngine(self, *, asset_step_count: int = 200, time_step_count: int = 200, scheme: typing.Literal['explicit_euler', 'implicit_euler', 'crank_nicolson'] = 'crank_nicolson', asset_upper_boundary: float | None = None) -> None
```

Finite-difference pricing engine with immutable configuration.

Configuration is validated at construction. Contract, market, and backend availability
are checked when pricing.
Vanilla, digital, and barrier engines accept 3..10,000 asset steps and 1..100,000
time steps. Accumulator and autocallable engines accept 3..2,000 asset steps and
1..2,000 time steps.

### 构造函数

Create an engine with validated finite-difference settings.

Settings are validated at construction.
The engine-specific ranges are listed in the engine class documentation.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial grid steps. Uses the core default when omitted.
- **`time_step_count`** (`int, optional`) — Number of time grid steps. Uses the core default when omitted.
- **`scheme`** (`{'explicit_euler', 'implicit_euler', 'crank_nicolson'}, optional`) — Time-stepping scheme. Uses the core default when omitted.
- **`asset_upper_boundary`** (`float or None, optional`) — Explicit upper asset-grid boundary, or ``None`` for the core default.
#### Raises

- `TypeError` — If a setting has an incompatible representation.
- `OverflowError` — If an integer setting is outside the C++ ``int`` range.
- `KiyosiError` — INVALID_PARAMETER if the core rejects the configuration.

### `asset_step_count`

Number of spatial grid steps.

### `time_step_count`

Number of time grid steps.

### `scheme`

Finite-difference time-stepping scheme.

### `asset_upper_boundary`

Explicit upper asset-grid boundary, or None for the core default.

### `price`

```python
price(self, instrument: EuropeanOption, context: PricingContext) -> float
price(self, instrument: AmericanOption, context: PricingContext) -> float
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `float` — Instrument price. No Greeks are calculated.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

### `price_with_greeks`

```python
price_with_greeks(self, instrument: EuropeanOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
price_with_greeks(self, instrument: AmericanOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
```

Compute price and the explicitly selected Greeks.

Pass one lowercase Greek name or an iterable of them, or set ``all_greeks=True`` to
request all ten. These forms are mutually exclusive. Native values are reused;
missing feasible measures use numerical price differences. Unrequested or
undefined measures are None, never zero sentinels. At expiry or a monitored
barrier hit-state boundary, only price is available. Feasible bumped valuation
failures fail the entire operation.
At current autocallable-product event thresholds, undefined spot and time
sensitivities remain None while feasible rate and volatility sensitivities survive.

Shift keyword arguments are absolute and use core-owned defaults. Spot shifts
use asset-price units, volatility and rate shifts use decimal units, and time
shifts use calendar days. Collapsed or asymmetric stencils leave affected
numerical Greeks unavailable. Monte Carlo valuations share one seed per request
without changing the engine. Concurrent calls are safe.
For American Monte Carlo, omitted or None spot_shift uses 8% of spot to reduce
exercise-decision sampling noise. Explicit shifts remain absolute. Sampling error
and bump-size bias remain; check convergence for the valuation.

#### Returns

- `PricingResult` — Price and requested available Greeks, with Greek units.
#### Raises

- `TypeError` — If a Greek representation, engine/instrument pairing, or shift representation is incompatible.
- `OverflowError` — If time_shift_days is outside the C++ int range.
- `KiyosiError` — If the Greek request or settings are invalid, or a required valuation fails.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

## `MonteCarloAccumulatorEngine`

```python
MonteCarloAccumulatorEngine(self, *, path_count: int = 20000, seed: int | None = 1, backend: typing.Literal['cpu', 'cuda'] = 'cpu', thread_count: int = 0) -> None
```

Trading-day Monte Carlo engine with immutable configuration.

Configuration is validated at construction. Contract, market, and backend availability
are checked when pricing.
Accumulator and autocallable engines accept 1..10,000,000 paths.

### 构造函数

Create an engine with validated Monte Carlo settings.

Settings are validated at construction.

#### Parameters

- **`path_count`** (`int, optional`) — Number of simulated paths. Uses the core default when omitted.
- **`seed`** (`int or None, optional`) — Non-negative random seed. Uses the core default when omitted. CPU paths have separate random streams; early knock-out does not shift later paths' draws.
- **`backend`** (`{'cpu', 'cuda'}, optional`) — CPU or CUDA execution backend.
- **`thread_count`** (`int, optional`) — Per-call CPU concurrency cap: 0 automatic, 1 serial. CUDA requires 0. Seeded CPU results are identical across thread counts in the same build.
#### Raises

- `TypeError` — If a setting has an incompatible representation.
- `OverflowError` — If an integer is outside its C++ representation range.
- `KiyosiError` — INVALID_PARAMETER if the core rejects the configuration.

### `path_count`

Number of simulated paths.

### `seed`

Non-negative random seed.

### `backend`

CPU or CUDA execution backend.

### `thread_count`

Per-call CPU concurrency cap; 0 automatic, 1 serial.

### `price`

```python
price(self, instrument: Accumulator, context: PricingContext) -> float
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `float` — Instrument price. No Greeks are calculated.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

### `price_with_greeks`

```python
price_with_greeks(self, instrument: Accumulator, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
```

Compute price and the explicitly selected Greeks.

Pass one lowercase Greek name or an iterable of them, or set ``all_greeks=True`` to
request all ten. These forms are mutually exclusive. Native values are reused;
missing feasible measures use numerical price differences. Unrequested or
undefined measures are None, never zero sentinels. At expiry or a monitored
barrier hit-state boundary, only price is available. Feasible bumped valuation
failures fail the entire operation.
At current autocallable-product event thresholds, undefined spot and time
sensitivities remain None while feasible rate and volatility sensitivities survive.

Shift keyword arguments are absolute and use core-owned defaults. Spot shifts
use asset-price units, volatility and rate shifts use decimal units, and time
shifts use calendar days. Collapsed or asymmetric stencils leave affected
numerical Greeks unavailable. Monte Carlo valuations share one seed per request
without changing the engine. Concurrent calls are safe.
For American Monte Carlo, omitted or None spot_shift uses 8% of spot to reduce
exercise-decision sampling noise. Explicit shifts remain absolute. Sampling error
and bump-size bias remain; check convergence for the valuation.

#### Returns

- `PricingResult` — Price and requested available Greeks, with Greek units.
#### Raises

- `TypeError` — If a Greek representation, engine/instrument pairing, or shift representation is incompatible.
- `OverflowError` — If time_shift_days is outside the C++ int range.
- `KiyosiError` — If the Greek request or settings are invalid, or a required valuation fails.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

## `MonteCarloAutocallableEngine`

```python
MonteCarloAutocallableEngine(self, *, path_count: int = 20000, seed: int | None = 1, backend: typing.Literal['cpu', 'cuda'] = 'cpu', thread_count: int = 0) -> None
```

Trading-day Monte Carlo engine with immutable configuration.

Configuration is validated at construction. Contract, market, and backend availability
are checked when pricing.
Accumulator and autocallable engines accept 1..10,000,000 paths.

### 构造函数

Create an engine with validated Monte Carlo settings.

Settings are validated at construction.

#### Parameters

- **`path_count`** (`int, optional`) — Number of simulated paths. Uses the core default when omitted.
- **`seed`** (`int or None, optional`) — Non-negative random seed. Uses the core default when omitted. CPU paths have separate random streams; early knock-out does not shift later paths' draws.
- **`backend`** (`{'cpu', 'cuda'}, optional`) — CPU or CUDA execution backend.
- **`thread_count`** (`int, optional`) — Per-call CPU concurrency cap: 0 automatic, 1 serial. CUDA requires 0. Seeded CPU results are identical across thread counts in the same build.
#### Raises

- `TypeError` — If a setting has an incompatible representation.
- `OverflowError` — If an integer is outside its C++ representation range.
- `KiyosiError` — INVALID_PARAMETER if the core rejects the configuration.

### `path_count`

Number of simulated paths.

### `seed`

Non-negative random seed.

### `backend`

CPU or CUDA execution backend.

### `thread_count`

Per-call CPU concurrency cap; 0 automatic, 1 serial.

### `price`

```python
price(self, instrument: SnowballOption, context: PricingContext) -> float
price(self, instrument: BinarySnowballOption, context: PricingContext) -> float
price(self, instrument: TernarySnowballOption, context: PricingContext) -> float
price(self, instrument: PhoenixOption, context: PricingContext) -> float
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `float` — Instrument price. No Greeks are calculated.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

### `price_with_greeks`

```python
price_with_greeks(self, instrument: SnowballOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
price_with_greeks(self, instrument: BinarySnowballOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
price_with_greeks(self, instrument: TernarySnowballOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
price_with_greeks(self, instrument: PhoenixOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
```

Compute price and the explicitly selected Greeks.

Pass one lowercase Greek name or an iterable of them, or set ``all_greeks=True`` to
request all ten. These forms are mutually exclusive. Native values are reused;
missing feasible measures use numerical price differences. Unrequested or
undefined measures are None, never zero sentinels. At expiry or a monitored
barrier hit-state boundary, only price is available. Feasible bumped valuation
failures fail the entire operation.
At current autocallable-product event thresholds, undefined spot and time
sensitivities remain None while feasible rate and volatility sensitivities survive.

Shift keyword arguments are absolute and use core-owned defaults. Spot shifts
use asset-price units, volatility and rate shifts use decimal units, and time
shifts use calendar days. Collapsed or asymmetric stencils leave affected
numerical Greeks unavailable. Monte Carlo valuations share one seed per request
without changing the engine. Concurrent calls are safe.
For American Monte Carlo, omitted or None spot_shift uses 8% of spot to reduce
exercise-decision sampling noise. Explicit shifts remain absolute. Sampling error
and bump-size bias remain; check convergence for the valuation.

#### Returns

- `PricingResult` — Price and requested available Greeks, with Greek units.
#### Raises

- `TypeError` — If a Greek representation, engine/instrument pairing, or shift representation is incompatible.
- `OverflowError` — If time_shift_days is outside the C++ int range.
- `KiyosiError` — If the Greek request or settings are invalid, or a required valuation fails.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

## `MonteCarloBackend`

```python
MonteCarloBackend = typing.Literal['cpu', 'cuda']
```

## `MonteCarloVanillaEngine`

```python
MonteCarloVanillaEngine(self, *, path_count: int = 100000, step_count: int = 50, seed: int | None = None, backend: typing.Literal['cpu', 'cuda'] = 'cpu', thread_count: int = 0) -> None
```

Monte Carlo vanilla-option engine with immutable configuration.

Configuration is validated at construction. Contract, market, and backend availability
are checked when pricing.
Accepts 1..10,000,000 paths and 2..10,000 steps; American pricing before
expiry requires at least 3 steps.
European prices sample the exact terminal distribution; valid step counts do not affect them.
American calls with nonpositive dividends and nonnegative rates use that distribution
with an immediate-exercise lower bound. Rate stencils crossing zero retain exercise-grid
simulations on both sides.

### 构造函数

Create an engine with validated Monte Carlo settings.

#### Parameters

- **`path_count`** (`int, optional`) — Number of simulated paths. Uses the core default when omitted.
- **`step_count`** (`int, optional`) — American time grid points; validated but unused for European pricing. Uses the core default when omitted.
- **`seed`** (`int or None, optional`) — Non-negative random seed, or ``None`` for nondeterministic seeding.
- **`backend`** (`{'cpu', 'cuda'}, optional`) — CPU or CUDA execution backend.
- **`thread_count`** (`int, optional`) — Per-call CPU concurrency cap: 0 automatic, 1 serial. CUDA requires 0. Seeded CPU results are identical across thread counts in the same build.
#### Raises

- `TypeError` — If a setting has an incompatible representation.
- `OverflowError` — If an integer is outside its C++ representation range.
- `KiyosiError` — INVALID_PARAMETER if the core rejects the configuration.
#### Notes

Settings are validated at construction.

### `path_count`

Number of simulated paths.

### `step_count`

American time grid points; validated but unused for European pricing.

### `seed`

Optional non-negative random seed.

### `backend`

CPU or CUDA execution backend.

### `thread_count`

Per-call CPU concurrency cap; 0 automatic, 1 serial.

### `price`

```python
price(self, instrument: EuropeanOption, context: PricingContext) -> float
price(self, instrument: AmericanOption, context: PricingContext) -> float
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `float` — Instrument price. No Greeks are calculated.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

### `price_with_greeks`

```python
price_with_greeks(self, instrument: EuropeanOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
price_with_greeks(self, instrument: AmericanOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None | None = None, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
```

Compute price and the explicitly selected Greeks.

Pass one lowercase Greek name or an iterable of them, or set ``all_greeks=True`` to
request all ten. These forms are mutually exclusive. Native values are reused;
missing feasible measures use numerical price differences. Unrequested or
undefined measures are None, never zero sentinels. At expiry or a monitored
barrier hit-state boundary, only price is available. Feasible bumped valuation
failures fail the entire operation.
At current autocallable-product event thresholds, undefined spot and time
sensitivities remain None while feasible rate and volatility sensitivities survive.

Shift keyword arguments are absolute and use core-owned defaults. Spot shifts
use asset-price units, volatility and rate shifts use decimal units, and time
shifts use calendar days. Collapsed or asymmetric stencils leave affected
numerical Greeks unavailable. Monte Carlo valuations share one seed per request
without changing the engine. Concurrent calls are safe.
For American Monte Carlo, omitted or None spot_shift uses 8% of spot to reduce
exercise-decision sampling noise. Explicit shifts remain absolute. Sampling error
and bump-size bias remain; check convergence for the valuation.

#### Returns

- `PricingResult` — Price and requested available Greeks, with Greek units.
#### Raises

- `TypeError` — If a Greek representation, engine/instrument pairing, or shift representation is incompatible.
- `OverflowError` — If time_shift_days is outside the C++ int range.
- `KiyosiError` — If the Greek request or settings are invalid, or a required valuation fails.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

## `QuadratureDigitalEngine`

```python
QuadratureDigitalEngine(self) -> None
```

Stateless pricing engine.

The engine has no configuration and may be reused across supported instruments
and contexts. Concurrent calls are safe.

### 构造函数

Create a stateless pricing engine.

#### Returns

- `pricing engine` — Reusable engine with no mutable configuration.

### `price`

```python
price(self, instrument: CashOrNothingOption, context: PricingContext) -> float
price(self, instrument: AssetOrNothingOption, context: PricingContext) -> float
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `float` — Instrument price. No Greeks are calculated.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

### `price_with_greeks`

```python
price_with_greeks(self, instrument: CashOrNothingOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
price_with_greeks(self, instrument: AssetOrNothingOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
```

Compute price and the explicitly selected Greeks.

Pass one lowercase Greek name or an iterable of them, or set ``all_greeks=True`` to
request all ten. These forms are mutually exclusive. Native values are reused;
missing feasible measures use numerical price differences. Unrequested or
undefined measures are None, never zero sentinels. At expiry or a monitored
barrier hit-state boundary, only price is available. Feasible bumped valuation
failures fail the entire operation.
At current autocallable-product event thresholds, undefined spot and time
sensitivities remain None while feasible rate and volatility sensitivities survive.

Shift keyword arguments are absolute and use core-owned defaults. Spot shifts
use asset-price units, volatility and rate shifts use decimal units, and time
shifts use calendar days. Collapsed or asymmetric stencils leave affected
numerical Greeks unavailable. Monte Carlo valuations share one seed per request
without changing the engine. Concurrent calls are safe.
For American Monte Carlo, omitted or None spot_shift uses 8% of spot to reduce
exercise-decision sampling noise. Explicit shifts remain absolute. Sampling error
and bump-size bias remain; check convergence for the valuation.

#### Returns

- `PricingResult` — Price and requested available Greeks, with Greek units.
#### Raises

- `TypeError` — If a Greek representation, engine/instrument pairing, or shift representation is incompatible.
- `OverflowError` — If time_shift_days is outside the C++ int range.
- `KiyosiError` — If the Greek request or settings are invalid, or a required valuation fails.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

## `QuadratureVanillaEngine`

```python
QuadratureVanillaEngine(self) -> None
```

Stateless pricing engine.

The engine has no configuration and may be reused across supported instruments
and contexts. Concurrent calls are safe.

### 构造函数

Create a stateless pricing engine.

#### Returns

- `pricing engine` — Reusable engine with no mutable configuration.

### `price`

```python
price(self, instrument: EuropeanOption, context: PricingContext) -> float
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `float` — Instrument price. No Greeks are calculated.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

### `price_with_greeks`

```python
price_with_greeks(self, instrument: EuropeanOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
```

Compute price and the explicitly selected Greeks.

Pass one lowercase Greek name or an iterable of them, or set ``all_greeks=True`` to
request all ten. These forms are mutually exclusive. Native values are reused;
missing feasible measures use numerical price differences. Unrequested or
undefined measures are None, never zero sentinels. At expiry or a monitored
barrier hit-state boundary, only price is available. Feasible bumped valuation
failures fail the entire operation.
At current autocallable-product event thresholds, undefined spot and time
sensitivities remain None while feasible rate and volatility sensitivities survive.

Shift keyword arguments are absolute and use core-owned defaults. Spot shifts
use asset-price units, volatility and rate shifts use decimal units, and time
shifts use calendar days. Collapsed or asymmetric stencils leave affected
numerical Greeks unavailable. Monte Carlo valuations share one seed per request
without changing the engine. Concurrent calls are safe.
For American Monte Carlo, omitted or None spot_shift uses 8% of spot to reduce
exercise-decision sampling noise. Explicit shifts remain absolute. Sampling error
and bump-size bias remain; check convergence for the valuation.

#### Returns

- `PricingResult` — Price and requested available Greeks, with Greek units.
#### Raises

- `TypeError` — If a Greek representation, engine/instrument pairing, or shift representation is incompatible.
- `OverflowError` — If time_shift_days is outside the C++ int range.
- `KiyosiError` — If the Greek request or settings are invalid, or a required valuation fails.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

## `TurnbullWakemanArithmeticAveragePriceEngine`

```python
TurnbullWakemanArithmeticAveragePriceEngine(self) -> None
```

Stateless pricing engine.

The engine has no configuration and may be reused across supported instruments
and contexts. Concurrent calls are safe.

### 构造函数

Create a stateless pricing engine.

#### Returns

- `pricing engine` — Reusable engine with no mutable configuration.

### `price`

```python
price(self, instrument: ArithmeticAveragePriceOption, context: PricingContext) -> float
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `float` — Instrument price. No Greeks are calculated.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

### `price_with_greeks`

```python
price_with_greeks(self, instrument: ArithmeticAveragePriceOption, context: PricingContext, greeks: typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho'] | collections.abc.Iterable[typing.Literal['delta', 'gamma', 'speed', 'theta', 'charm', 'color', 'vega', 'vanna', 'zomma', 'rho']] | None = None, *, all_greeks: bool = False, spot_shift: float | None = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
```

Compute price and the explicitly selected Greeks.

Pass one lowercase Greek name or an iterable of them, or set ``all_greeks=True`` to
request all ten. These forms are mutually exclusive. Native values are reused;
missing feasible measures use numerical price differences. Unrequested or
undefined measures are None, never zero sentinels. At expiry or a monitored
barrier hit-state boundary, only price is available. Feasible bumped valuation
failures fail the entire operation.
At current autocallable-product event thresholds, undefined spot and time
sensitivities remain None while feasible rate and volatility sensitivities survive.

Shift keyword arguments are absolute and use core-owned defaults. Spot shifts
use asset-price units, volatility and rate shifts use decimal units, and time
shifts use calendar days. Collapsed or asymmetric stencils leave affected
numerical Greeks unavailable. Monte Carlo valuations share one seed per request
without changing the engine. Concurrent calls are safe.
For American Monte Carlo, omitted or None spot_shift uses 8% of spot to reduce
exercise-decision sampling noise. Explicit shifts remain absolute. Sampling error
and bump-size bias remain; check convergence for the valuation.

#### Returns

- `PricingResult` — Price and requested available Greeks, with Greek units.
#### Raises

- `TypeError` — If a Greek representation, engine/instrument pairing, or shift representation is incompatible.
- `OverflowError` — If time_shift_days is outside the C++ int range.
- `KiyosiError` — If the Greek request or settings are invalid, or a required valuation fails.
#### Notes

Operational exceptions and cancellation follow the package-level contract in
`kiyosi`: allocation failures raise MemoryError, and Python signal handling
is deferred until the synchronous core computation returns.

## `implied_coupon`

```python
implied_coupon(engine: FiniteDifferenceAutocallableEngine, instrument: SnowballOption, context: PricingContext, observed_price: float, *, quote_convention: typing.Literal['shift_maturity_coupon', 'preserve_maturity_coupon'], lower_bound: float = 0.0, upper_bound: float = 2.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_coupon(engine: MonteCarloAutocallableEngine, instrument: SnowballOption, context: PricingContext, observed_price: float, *, quote_convention: typing.Literal['shift_maturity_coupon', 'preserve_maturity_coupon'], lower_bound: float = 0.0, upper_bound: float = 2.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_coupon(engine: FiniteDifferenceAutocallableEngine, instrument: BinarySnowballOption, context: PricingContext, observed_price: float, *, quote_convention: typing.Literal['shift_maturity_coupon', 'preserve_maturity_coupon'], lower_bound: float = 0.0, upper_bound: float = 2.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_coupon(engine: MonteCarloAutocallableEngine, instrument: BinarySnowballOption, context: PricingContext, observed_price: float, *, quote_convention: typing.Literal['shift_maturity_coupon', 'preserve_maturity_coupon'], lower_bound: float = 0.0, upper_bound: float = 2.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_coupon(engine: FiniteDifferenceAutocallableEngine, instrument: TernarySnowballOption, context: PricingContext, observed_price: float, *, quote_convention: typing.Literal['shift_maturity_coupon', 'preserve_maturity_coupon'], lower_bound: float = 0.0, upper_bound: float = 2.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_coupon(engine: MonteCarloAutocallableEngine, instrument: TernarySnowballOption, context: PricingContext, observed_price: float, *, quote_convention: typing.Literal['shift_maturity_coupon', 'preserve_maturity_coupon'], lower_bound: float = 0.0, upper_bound: float = 2.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_coupon(engine: FiniteDifferenceAutocallableEngine, instrument: PhoenixOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0, upper_bound: float = 2.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_coupon(engine: MonteCarloAutocallableEngine, instrument: PhoenixOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0, upper_bound: float = 2.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
```

Solve for a coupon rate that matches an observed price.

#### Parameters

- **`engine`** (`pricing engine`) — Engine used for trial valuations.
- **`instrument`** (`SnowballOption, BinarySnowballOption, TernarySnowballOption, or PhoenixOption`) — Instrument supported by the engine.
- **`context`** (`PricingContext`) — Market state used by the solver.
- **`observed_price`** (`float`) — Target instrument price.
- **`quote_convention`** (`{'shift_maturity_coupon', 'preserve_maturity_coupon'}`) — Required for snowball instruments: whether the maturity coupon shifts with quoted knock-out coupons. Omit this argument for Phoenix instruments.
- **`lower_bound, upper_bound`** (`float, optional`) — Finite coupon-rate search interval, which may include negative rates. Omitted values use core defaults.
- **`price_tolerance`** (`float, optional`) — Absolute price-error tolerance; Monte Carlo sampling error is not bounded.
- **`parameter_tolerance`** (`float, optional`) — Absolute search-interval tolerance in volatility or coupon-rate units. The solver stops when either tolerance is met.
- **`max_iterations`** (`int, optional`) — Maximum solver iterations.
#### Returns

- `float` — Implied annualized coupon rate.
An unseeded Monte Carlo engine uses one random seed throughout this solve.
Monte Carlo and finite-difference engines first try interpolation and verify its
price residual. If the price tolerance is not met, the solver uses bisection.

#### Raises

- `TypeError` — If the engine/instrument combination or an argument is incompatible.
- `KiyosiError` — If inputs are invalid, the target is not bracketed, or the solver fails.

## `implied_volatility`

```python
implied_volatility(engine: AnalyticVanillaEngine, instrument: EuropeanOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: QuadratureVanillaEngine, instrument: EuropeanOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: CoxRossRubinsteinVanillaEngine, instrument: EuropeanOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: CoxRossRubinsteinVanillaEngine, instrument: AmericanOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: BjerksundStenslandVanillaEngine, instrument: AmericanOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: FiniteDifferenceVanillaEngine, instrument: EuropeanOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: FiniteDifferenceVanillaEngine, instrument: AmericanOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: MonteCarloVanillaEngine, instrument: EuropeanOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: MonteCarloVanillaEngine, instrument: AmericanOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: AnalyticDigitalEngine, instrument: CashOrNothingOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: AnalyticDigitalEngine, instrument: AssetOrNothingOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: QuadratureDigitalEngine, instrument: CashOrNothingOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: QuadratureDigitalEngine, instrument: AssetOrNothingOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: FiniteDifferenceDigitalEngine, instrument: CashOrNothingOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: FiniteDifferenceDigitalEngine, instrument: AssetOrNothingOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: AnalyticBarrierEngine, instrument: BarrierOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: FiniteDifferenceBarrierEngine, instrument: BarrierOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: AnalyticBinaryBarrierEngine, instrument: BinaryBarrierOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: AnalyticBinaryBarrierEngine, instrument: TouchOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: AnalyticGeometricAveragePriceEngine, instrument: GeometricAveragePriceOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: TurnbullWakemanArithmeticAveragePriceEngine, instrument: ArithmeticAveragePriceOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: FiniteDifferenceAccumulatorEngine, instrument: Accumulator, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: MonteCarloAccumulatorEngine, instrument: Accumulator, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: FiniteDifferenceAutocallableEngine, instrument: SnowballOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: FiniteDifferenceAutocallableEngine, instrument: BinarySnowballOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: FiniteDifferenceAutocallableEngine, instrument: TernarySnowballOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: FiniteDifferenceAutocallableEngine, instrument: PhoenixOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: MonteCarloAutocallableEngine, instrument: SnowballOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: MonteCarloAutocallableEngine, instrument: BinarySnowballOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: MonteCarloAutocallableEngine, instrument: TernarySnowballOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: MonteCarloAutocallableEngine, instrument: PhoenixOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, price_tolerance: float = 1e-08, parameter_tolerance: float = 1e-08, max_iterations: int = 100) -> float
```

Solve for the volatility that matches an observed price.

Uses safeguarded Brent interpolation, with bisection when needed to retain the bracket.

#### Parameters

- **`engine`** (`pricing engine`) — Engine used for trial valuations.
- **`instrument`** (`instrument`) — Instrument supported by the engine.
- **`context`** (`PricingContext`) — Market state whose volatility is varied.
- **`observed_price`** (`float`) — Target instrument price.
- **`lower_bound, upper_bound`** (`float, optional`) — Volatility search interval. Omitted values use core defaults. CRR searches intersect this interval with the tree's admissible volatility range.
- **`price_tolerance`** (`float, optional`) — Absolute price-error tolerance; Monte Carlo sampling error is not bounded.
- **`parameter_tolerance`** (`float, optional`) — Absolute search-interval tolerance in volatility or coupon-rate units. The solver stops when either tolerance is met.
- **`max_iterations`** (`int, optional`) — Maximum solver iterations.
#### Returns

- `float` — Implied volatility as a decimal rate.
An unseeded Monte Carlo engine uses one random seed throughout this solve.
Known volatility-independent payments raise ``KiyosiError`` with category
``UNSUPPORTED_OPERATION``.

#### Raises

- `TypeError` — If the engine/instrument combination or an argument is incompatible.
- `KiyosiError` — If inputs are invalid, the target is not bracketed, or the solver fails.
