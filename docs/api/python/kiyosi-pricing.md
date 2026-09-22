---
description: Python API reference for kiyosi.pricing.
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

### Constructor

Create a stateless pricing engine.

#### Returns

- `pricing engine` — Reusable engine with no mutable configuration.

### `price`

```python
price(self, instrument: BarrierOption, context: PricingContext) -> PricingResult
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `PricingResult` — Result containing ``price`` and any analytics produced by the engine.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.

## `AnalyticBinaryBarrierEngine`

```python
AnalyticBinaryBarrierEngine(self) -> None
```

Stateless pricing engine.

The engine has no configuration and may be reused across supported instruments
and contexts. Concurrent calls are safe.

### Constructor

Create a stateless pricing engine.

#### Returns

- `pricing engine` — Reusable engine with no mutable configuration.

### `price`

```python
price(self, instrument: BinaryBarrierOption, context: PricingContext) -> PricingResult
price(self, instrument: TouchOption, context: PricingContext) -> PricingResult
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `PricingResult` — Result containing ``price`` and any analytics produced by the engine.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.

## `AnalyticDigitalEngine`

```python
AnalyticDigitalEngine(self) -> None
```

Stateless pricing engine.

The engine has no configuration and may be reused across supported instruments
and contexts. Concurrent calls are safe.

### Constructor

Create a stateless pricing engine.

#### Returns

- `pricing engine` — Reusable engine with no mutable configuration.

### `price`

```python
price(self, instrument: CashOrNothingOption, context: PricingContext) -> PricingResult
price(self, instrument: AssetOrNothingOption, context: PricingContext) -> PricingResult
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `PricingResult` — Result containing ``price`` and any analytics produced by the engine.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.

## `AnalyticGeometricAveragePriceEngine`

```python
AnalyticGeometricAveragePriceEngine(self) -> None
```

Stateless pricing engine.

The engine has no configuration and may be reused across supported instruments
and contexts. Concurrent calls are safe.

### Constructor

Create a stateless pricing engine.

#### Returns

- `pricing engine` — Reusable engine with no mutable configuration.

### `price`

```python
price(self, instrument: GeometricAveragePriceOption, context: PricingContext) -> PricingResult
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `PricingResult` — Result containing ``price`` and any analytics produced by the engine.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.

## `AnalyticVanillaEngine`

```python
AnalyticVanillaEngine(self) -> None
```

Stateless pricing engine.

The engine has no configuration and may be reused across supported instruments
and contexts. Concurrent calls are safe.

### Constructor

Create a stateless pricing engine.

#### Returns

- `pricing engine` — Reusable engine with no mutable configuration.

### `price`

```python
price(self, instrument: EuropeanOption, context: PricingContext) -> PricingResult
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `PricingResult` — Result containing ``price`` and any analytics produced by the engine.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.

## `BjerksundStenslandVanillaEngine`

```python
BjerksundStenslandVanillaEngine(self) -> None
```

Stateless pricing engine.

The engine has no configuration and may be reused across supported instruments
and contexts. Concurrent calls are safe.

### Constructor

Create a stateless pricing engine.

#### Returns

- `pricing engine` — Reusable engine with no mutable configuration.

### `price`

```python
price(self, instrument: AmericanOption, context: PricingContext) -> PricingResult
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `PricingResult` — Result containing ``price`` and any analytics produced by the engine.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.

## `CouponQuoteConvention`

Coupon component varied by a snowball implied-coupon solve.

#### Attributes

- `SHIFT_MATURITY_COUPON` — Shift the maturity coupon with the quoted knock-out coupons.
- `PRESERVE_MATURITY_COUPON` — Keep the maturity coupon fixed while shifting knock-out coupons.

### Values

- `SHIFT_MATURITY_COUPON` = `0`
- `PRESERVE_MATURITY_COUPON` = `1`

## `CoxRossRubinsteinVanillaEngine`

```python
CoxRossRubinsteinVanillaEngine(self, step_count: int = 256) -> None
```

Cox-Ross-Rubinstein binomial vanilla-option engine.

Configuration is immutable. Settings are stored without domain validation and
are validated when price() is called.

#### Attributes

- **`step_count`** (`int`) — Number of binomial time steps.

### Constructor

Store Cox-Ross-Rubinstein settings.

#### Parameters

- **`step_count`** (`int, optional`) — Number of binomial time steps. Uses the core default when omitted.
#### Raises

- `TypeError` — If ``step_count`` is not an integer.
- `OverflowError` — If ``step_count`` is outside the C++ ``int`` range.
#### Notes

The setting is validated when price() is called.

### `step_count`

Number of binomial time steps.

### `price`

```python
price(self, instrument: EuropeanOption, context: PricingContext) -> PricingResult
price(self, instrument: AmericanOption, context: PricingContext) -> PricingResult
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `PricingResult` — Result containing ``price`` and any analytics produced by the engine.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.

## `FiniteDifferenceAccumulatorEngine`

```python
FiniteDifferenceAccumulatorEngine(self, *, asset_step_count: int = 200, time_step_count: int = 200, scheme: FiniteDifferenceScheme = FiniteDifferenceScheme.CRANK_NICOLSON, asset_upper_boundary: float | None = None) -> None
```

Finite-difference pricing engine with immutable configuration.

Settings are stored without domain validation and are validated when price() is called.

#### Attributes

- **`asset_step_count`** (`int`) — Number of spatial grid steps.
- **`time_step_count`** (`int`) — Number of time grid steps.
- **`scheme`** (`FiniteDifferenceScheme`) — Time-stepping scheme.
- **`asset_upper_boundary`** (`float or None`) — Explicit upper asset-grid boundary, or ``None`` for the core default.

### Constructor

Store finite-difference settings.

Settings are validated when price() is called.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial grid steps. Uses the core default when omitted.
- **`time_step_count`** (`int, optional`) — Number of time grid steps. Uses the core default when omitted.
- **`scheme`** (`FiniteDifferenceScheme, optional`) — Time-stepping scheme. Uses the core default when omitted.
- **`asset_upper_boundary`** (`float or None, optional`) — Explicit upper asset-grid boundary, or ``None`` for the core default.
#### Raises

- `TypeError` — If a setting has an incompatible representation.
- `OverflowError` — If an integer setting is outside the C++ ``int`` range.

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
price(self, instrument: Accumulator, context: PricingContext) -> PricingResult
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `PricingResult` — Result containing ``price`` and any analytics produced by the engine.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.

## `FiniteDifferenceBarrierEngine`

```python
FiniteDifferenceBarrierEngine(self, *, asset_step_count: int = 200, time_step_count: int = 200, scheme: FiniteDifferenceScheme = FiniteDifferenceScheme.CRANK_NICOLSON, asset_upper_boundary: float | None = None) -> None
```

Finite-difference pricing engine with immutable configuration.

Settings are stored without domain validation and are validated when price() is called.

#### Attributes

- **`asset_step_count`** (`int`) — Number of spatial grid steps.
- **`time_step_count`** (`int`) — Number of time grid steps.
- **`scheme`** (`FiniteDifferenceScheme`) — Time-stepping scheme.
- **`asset_upper_boundary`** (`float or None`) — Explicit upper asset-grid boundary, or ``None`` for the core default.

### Constructor

Store finite-difference settings.

Settings are validated when price() is called.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial grid steps. Uses the core default when omitted.
- **`time_step_count`** (`int, optional`) — Number of time grid steps. Uses the core default when omitted.
- **`scheme`** (`FiniteDifferenceScheme, optional`) — Time-stepping scheme. Uses the core default when omitted.
- **`asset_upper_boundary`** (`float or None, optional`) — Explicit upper asset-grid boundary, or ``None`` for the core default.
#### Raises

- `TypeError` — If a setting has an incompatible representation.
- `OverflowError` — If an integer setting is outside the C++ ``int`` range.

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
price(self, instrument: BarrierOption, context: PricingContext) -> PricingResult
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `PricingResult` — Result containing ``price`` and any analytics produced by the engine.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.

## `FiniteDifferenceBinarySnowballEngine`

```python
FiniteDifferenceBinarySnowballEngine(self, *, asset_step_count: int = 200, time_step_count: int = 200, scheme: FiniteDifferenceScheme = FiniteDifferenceScheme.CRANK_NICOLSON, asset_upper_boundary: float | None = None) -> None
```

Finite-difference pricing engine with immutable configuration.

Settings are stored without domain validation and are validated when price() is called.

#### Attributes

- **`asset_step_count`** (`int`) — Number of spatial grid steps.
- **`time_step_count`** (`int`) — Number of time grid steps.
- **`scheme`** (`FiniteDifferenceScheme`) — Time-stepping scheme.
- **`asset_upper_boundary`** (`float or None`) — Explicit upper asset-grid boundary, or ``None`` for the core default.

### Constructor

Store finite-difference settings.

Settings are validated when price() is called.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial grid steps. Uses the core default when omitted.
- **`time_step_count`** (`int, optional`) — Number of time grid steps. Uses the core default when omitted.
- **`scheme`** (`FiniteDifferenceScheme, optional`) — Time-stepping scheme. Uses the core default when omitted.
- **`asset_upper_boundary`** (`float or None, optional`) — Explicit upper asset-grid boundary, or ``None`` for the core default.
#### Raises

- `TypeError` — If a setting has an incompatible representation.
- `OverflowError` — If an integer setting is outside the C++ ``int`` range.

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
price(self, instrument: BinarySnowballOption, context: PricingContext) -> PricingResult
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `PricingResult` — Result containing ``price`` and any analytics produced by the engine.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.

## `FiniteDifferenceDigitalEngine`

```python
FiniteDifferenceDigitalEngine(self, *, asset_step_count: int = 200, time_step_count: int = 200, scheme: FiniteDifferenceScheme = FiniteDifferenceScheme.CRANK_NICOLSON, asset_upper_boundary: float | None = None) -> None
```

Finite-difference pricing engine with immutable configuration.

Settings are stored without domain validation and are validated when price() is called.

#### Attributes

- **`asset_step_count`** (`int`) — Number of spatial grid steps.
- **`time_step_count`** (`int`) — Number of time grid steps.
- **`scheme`** (`FiniteDifferenceScheme`) — Time-stepping scheme.
- **`asset_upper_boundary`** (`float or None`) — Explicit upper asset-grid boundary, or ``None`` for the core default.

### Constructor

Store finite-difference settings.

Settings are validated when price() is called.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial grid steps. Uses the core default when omitted.
- **`time_step_count`** (`int, optional`) — Number of time grid steps. Uses the core default when omitted.
- **`scheme`** (`FiniteDifferenceScheme, optional`) — Time-stepping scheme. Uses the core default when omitted.
- **`asset_upper_boundary`** (`float or None, optional`) — Explicit upper asset-grid boundary, or ``None`` for the core default.
#### Raises

- `TypeError` — If a setting has an incompatible representation.
- `OverflowError` — If an integer setting is outside the C++ ``int`` range.

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
price(self, instrument: CashOrNothingOption, context: PricingContext) -> PricingResult
price(self, instrument: AssetOrNothingOption, context: PricingContext) -> PricingResult
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `PricingResult` — Result containing ``price`` and any analytics produced by the engine.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.

## `FiniteDifferencePhoenixEngine`

```python
FiniteDifferencePhoenixEngine(self, *, asset_step_count: int = 200, time_step_count: int = 200, scheme: FiniteDifferenceScheme = FiniteDifferenceScheme.CRANK_NICOLSON, asset_upper_boundary: float | None = None) -> None
```

Finite-difference pricing engine with immutable configuration.

Settings are stored without domain validation and are validated when price() is called.

#### Attributes

- **`asset_step_count`** (`int`) — Number of spatial grid steps.
- **`time_step_count`** (`int`) — Number of time grid steps.
- **`scheme`** (`FiniteDifferenceScheme`) — Time-stepping scheme.
- **`asset_upper_boundary`** (`float or None`) — Explicit upper asset-grid boundary, or ``None`` for the core default.

### Constructor

Store finite-difference settings.

Settings are validated when price() is called.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial grid steps. Uses the core default when omitted.
- **`time_step_count`** (`int, optional`) — Number of time grid steps. Uses the core default when omitted.
- **`scheme`** (`FiniteDifferenceScheme, optional`) — Time-stepping scheme. Uses the core default when omitted.
- **`asset_upper_boundary`** (`float or None, optional`) — Explicit upper asset-grid boundary, or ``None`` for the core default.
#### Raises

- `TypeError` — If a setting has an incompatible representation.
- `OverflowError` — If an integer setting is outside the C++ ``int`` range.

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
price(self, instrument: PhoenixOption, context: PricingContext) -> PricingResult
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `PricingResult` — Result containing ``price`` and any analytics produced by the engine.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.

## `FiniteDifferenceScheme`

Time-stepping scheme for finite-difference engines.

#### Attributes

- `EXPLICIT_EULER` — Explicit Euler time stepping.
- `IMPLICIT_EULER` — Implicit Euler time stepping.
- `CRANK_NICOLSON` — Crank-Nicolson time stepping.

### Values

- `EXPLICIT_EULER` = `0`
- `IMPLICIT_EULER` = `1`
- `CRANK_NICOLSON` = `2`

## `FiniteDifferenceSnowballEngine`

```python
FiniteDifferenceSnowballEngine(self, *, asset_step_count: int = 200, time_step_count: int = 200, scheme: FiniteDifferenceScheme = FiniteDifferenceScheme.CRANK_NICOLSON, asset_upper_boundary: float | None = None) -> None
```

Finite-difference pricing engine with immutable configuration.

Settings are stored without domain validation and are validated when price() is called.

#### Attributes

- **`asset_step_count`** (`int`) — Number of spatial grid steps.
- **`time_step_count`** (`int`) — Number of time grid steps.
- **`scheme`** (`FiniteDifferenceScheme`) — Time-stepping scheme.
- **`asset_upper_boundary`** (`float or None`) — Explicit upper asset-grid boundary, or ``None`` for the core default.

### Constructor

Store finite-difference settings.

Settings are validated when price() is called.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial grid steps. Uses the core default when omitted.
- **`time_step_count`** (`int, optional`) — Number of time grid steps. Uses the core default when omitted.
- **`scheme`** (`FiniteDifferenceScheme, optional`) — Time-stepping scheme. Uses the core default when omitted.
- **`asset_upper_boundary`** (`float or None, optional`) — Explicit upper asset-grid boundary, or ``None`` for the core default.
#### Raises

- `TypeError` — If a setting has an incompatible representation.
- `OverflowError` — If an integer setting is outside the C++ ``int`` range.

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
price(self, instrument: SnowballOption, context: PricingContext) -> PricingResult
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `PricingResult` — Result containing ``price`` and any analytics produced by the engine.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.

## `FiniteDifferenceTernarySnowballEngine`

```python
FiniteDifferenceTernarySnowballEngine(self, *, asset_step_count: int = 200, time_step_count: int = 200, scheme: FiniteDifferenceScheme = FiniteDifferenceScheme.CRANK_NICOLSON, asset_upper_boundary: float | None = None) -> None
```

Finite-difference pricing engine with immutable configuration.

Settings are stored without domain validation and are validated when price() is called.

#### Attributes

- **`asset_step_count`** (`int`) — Number of spatial grid steps.
- **`time_step_count`** (`int`) — Number of time grid steps.
- **`scheme`** (`FiniteDifferenceScheme`) — Time-stepping scheme.
- **`asset_upper_boundary`** (`float or None`) — Explicit upper asset-grid boundary, or ``None`` for the core default.

### Constructor

Store finite-difference settings.

Settings are validated when price() is called.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial grid steps. Uses the core default when omitted.
- **`time_step_count`** (`int, optional`) — Number of time grid steps. Uses the core default when omitted.
- **`scheme`** (`FiniteDifferenceScheme, optional`) — Time-stepping scheme. Uses the core default when omitted.
- **`asset_upper_boundary`** (`float or None, optional`) — Explicit upper asset-grid boundary, or ``None`` for the core default.
#### Raises

- `TypeError` — If a setting has an incompatible representation.
- `OverflowError` — If an integer setting is outside the C++ ``int`` range.

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
price(self, instrument: TernarySnowballOption, context: PricingContext) -> PricingResult
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `PricingResult` — Result containing ``price`` and any analytics produced by the engine.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.

## `FiniteDifferenceVanillaEngine`

```python
FiniteDifferenceVanillaEngine(self, *, asset_step_count: int = 200, time_step_count: int = 200, scheme: FiniteDifferenceScheme = FiniteDifferenceScheme.CRANK_NICOLSON, asset_upper_boundary: float | None = None) -> None
```

Finite-difference pricing engine with immutable configuration.

Settings are stored without domain validation and are validated when price() is called.

#### Attributes

- **`asset_step_count`** (`int`) — Number of spatial grid steps.
- **`time_step_count`** (`int`) — Number of time grid steps.
- **`scheme`** (`FiniteDifferenceScheme`) — Time-stepping scheme.
- **`asset_upper_boundary`** (`float or None`) — Explicit upper asset-grid boundary, or ``None`` for the core default.

### Constructor

Store finite-difference settings.

Settings are validated when price() is called.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial grid steps. Uses the core default when omitted.
- **`time_step_count`** (`int, optional`) — Number of time grid steps. Uses the core default when omitted.
- **`scheme`** (`FiniteDifferenceScheme, optional`) — Time-stepping scheme. Uses the core default when omitted.
- **`asset_upper_boundary`** (`float or None, optional`) — Explicit upper asset-grid boundary, or ``None`` for the core default.
#### Raises

- `TypeError` — If a setting has an incompatible representation.
- `OverflowError` — If an integer setting is outside the C++ ``int`` range.

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
price(self, instrument: EuropeanOption, context: PricingContext) -> PricingResult
price(self, instrument: AmericanOption, context: PricingContext) -> PricingResult
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `PricingResult` — Result containing ``price`` and any analytics produced by the engine.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.

## `MonteCarloAccumulatorEngine`

```python
MonteCarloAccumulatorEngine(self, *, path_count: int = 20000, seed: int = 1, backend: object = MonteCarloBackend.CPU) -> None
```

Trading-day Monte Carlo engine with immutable configuration.

Settings are stored without domain validation and are validated when price() is called.

#### Attributes

- **`path_count`** (`int`) — Number of simulated paths.
- **`seed`** (`int or None`) — Non-negative random seed.
- **`backend`** (`MonteCarloBackend`) — CPU or CUDA execution backend.

### Constructor

Store Monte Carlo settings.

Settings are validated when price() is called.

#### Parameters

- **`path_count`** (`int, optional`) — Number of simulated paths. Uses the core default when omitted.
- **`seed`** (`int or None, optional`) — Non-negative random seed. Uses the core default when omitted.
- **`backend`** (`MonteCarloBackend, optional`) — CPU or CUDA execution backend.
#### Raises

- `TypeError` — If a setting has an incompatible representation.
- `OverflowError` — If an integer is outside its C++ representation range.

### `path_count`

Number of simulated paths.

### `seed`

Non-negative random seed.

### `backend`

CPU or CUDA execution backend.

### `price`

```python
price(self, instrument: Accumulator, context: PricingContext) -> PricingResult
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `PricingResult` — Result containing ``price`` and any analytics produced by the engine.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.

## `MonteCarloBackend`

Execution backend for Monte Carlo engines.

#### Attributes

- `CPU` — Run on the host processor.
- `CUDA` — Run on a CUDA-capable GPU.

### Values

- `CPU` = `0`
- `CUDA` = `1`

## `MonteCarloBinarySnowballEngine`

```python
MonteCarloBinarySnowballEngine(self, *, path_count: int = 20000, seed: int = 1, backend: object = MonteCarloBackend.CPU) -> None
```

Trading-day Monte Carlo engine with immutable configuration.

Settings are stored without domain validation and are validated when price() is called.

#### Attributes

- **`path_count`** (`int`) — Number of simulated paths.
- **`seed`** (`int or None`) — Non-negative random seed.
- **`backend`** (`MonteCarloBackend`) — CPU or CUDA execution backend.

### Constructor

Store Monte Carlo settings.

Settings are validated when price() is called.

#### Parameters

- **`path_count`** (`int, optional`) — Number of simulated paths. Uses the core default when omitted.
- **`seed`** (`int or None, optional`) — Non-negative random seed. Uses the core default when omitted.
- **`backend`** (`MonteCarloBackend, optional`) — CPU or CUDA execution backend.
#### Raises

- `TypeError` — If a setting has an incompatible representation.
- `OverflowError` — If an integer is outside its C++ representation range.

### `path_count`

Number of simulated paths.

### `seed`

Non-negative random seed.

### `backend`

CPU or CUDA execution backend.

### `price`

```python
price(self, instrument: BinarySnowballOption, context: PricingContext) -> PricingResult
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `PricingResult` — Result containing ``price`` and any analytics produced by the engine.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.

## `MonteCarloPhoenixEngine`

```python
MonteCarloPhoenixEngine(self, *, path_count: int = 20000, seed: int = 1, backend: object = MonteCarloBackend.CPU) -> None
```

Trading-day Monte Carlo engine with immutable configuration.

Settings are stored without domain validation and are validated when price() is called.

#### Attributes

- **`path_count`** (`int`) — Number of simulated paths.
- **`seed`** (`int or None`) — Non-negative random seed.
- **`backend`** (`MonteCarloBackend`) — CPU or CUDA execution backend.

### Constructor

Store Monte Carlo settings.

Settings are validated when price() is called.

#### Parameters

- **`path_count`** (`int, optional`) — Number of simulated paths. Uses the core default when omitted.
- **`seed`** (`int or None, optional`) — Non-negative random seed. Uses the core default when omitted.
- **`backend`** (`MonteCarloBackend, optional`) — CPU or CUDA execution backend.
#### Raises

- `TypeError` — If a setting has an incompatible representation.
- `OverflowError` — If an integer is outside its C++ representation range.

### `path_count`

Number of simulated paths.

### `seed`

Non-negative random seed.

### `backend`

CPU or CUDA execution backend.

### `price`

```python
price(self, instrument: PhoenixOption, context: PricingContext) -> PricingResult
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `PricingResult` — Result containing ``price`` and any analytics produced by the engine.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.

## `MonteCarloSnowballEngine`

```python
MonteCarloSnowballEngine(self, *, path_count: int = 20000, seed: int = 1, backend: object = MonteCarloBackend.CPU) -> None
```

Trading-day Monte Carlo engine with immutable configuration.

Settings are stored without domain validation and are validated when price() is called.

#### Attributes

- **`path_count`** (`int`) — Number of simulated paths.
- **`seed`** (`int or None`) — Non-negative random seed.
- **`backend`** (`MonteCarloBackend`) — CPU or CUDA execution backend.

### Constructor

Store Monte Carlo settings.

Settings are validated when price() is called.

#### Parameters

- **`path_count`** (`int, optional`) — Number of simulated paths. Uses the core default when omitted.
- **`seed`** (`int or None, optional`) — Non-negative random seed. Uses the core default when omitted.
- **`backend`** (`MonteCarloBackend, optional`) — CPU or CUDA execution backend.
#### Raises

- `TypeError` — If a setting has an incompatible representation.
- `OverflowError` — If an integer is outside its C++ representation range.

### `path_count`

Number of simulated paths.

### `seed`

Non-negative random seed.

### `backend`

CPU or CUDA execution backend.

### `price`

```python
price(self, instrument: SnowballOption, context: PricingContext) -> PricingResult
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `PricingResult` — Result containing ``price`` and any analytics produced by the engine.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.

## `MonteCarloTernarySnowballEngine`

```python
MonteCarloTernarySnowballEngine(self, *, path_count: int = 20000, seed: int = 1, backend: object = MonteCarloBackend.CPU) -> None
```

Trading-day Monte Carlo engine with immutable configuration.

Settings are stored without domain validation and are validated when price() is called.

#### Attributes

- **`path_count`** (`int`) — Number of simulated paths.
- **`seed`** (`int or None`) — Non-negative random seed.
- **`backend`** (`MonteCarloBackend`) — CPU or CUDA execution backend.

### Constructor

Store Monte Carlo settings.

Settings are validated when price() is called.

#### Parameters

- **`path_count`** (`int, optional`) — Number of simulated paths. Uses the core default when omitted.
- **`seed`** (`int or None, optional`) — Non-negative random seed. Uses the core default when omitted.
- **`backend`** (`MonteCarloBackend, optional`) — CPU or CUDA execution backend.
#### Raises

- `TypeError` — If a setting has an incompatible representation.
- `OverflowError` — If an integer is outside its C++ representation range.

### `path_count`

Number of simulated paths.

### `seed`

Non-negative random seed.

### `backend`

CPU or CUDA execution backend.

### `price`

```python
price(self, instrument: TernarySnowballOption, context: PricingContext) -> PricingResult
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `PricingResult` — Result containing ``price`` and any analytics produced by the engine.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.

## `MonteCarloVanillaEngine`

```python
MonteCarloVanillaEngine(self, *, path_count: int = 100000, step_count: int = 50, seed: int | None = None, backend: object = MonteCarloBackend.CPU) -> None
```

Monte Carlo vanilla-option engine with immutable configuration.

Settings are stored without domain validation and are validated when price() is called.

#### Attributes

- **`path_count`** (`int`) — Number of simulated paths.
- **`step_count`** (`int`) — Number of time steps per path.
- **`seed`** (`int or None`) — Optional non-negative random seed.
- **`backend`** (`MonteCarloBackend`) — CPU or CUDA execution backend.

### Constructor

Store Monte Carlo settings.

#### Parameters

- **`path_count`** (`int, optional`) — Number of simulated paths. Uses the core default when omitted.
- **`step_count`** (`int, optional`) — Number of time steps per path. Uses the core default when omitted.
- **`seed`** (`int or None, optional`) — Non-negative random seed, or ``None`` for nondeterministic seeding.
- **`backend`** (`MonteCarloBackend, optional`) — CPU or CUDA execution backend.
#### Raises

- `TypeError` — If a setting has an incompatible representation.
- `OverflowError` — If an integer is outside its C++ representation range.
#### Notes

Settings are validated when price() is called.

### `path_count`

Number of simulated paths.

### `step_count`

Number of time steps per path.

### `seed`

Optional non-negative random seed.

### `backend`

CPU or CUDA execution backend.

### `price`

```python
price(self, instrument: EuropeanOption, context: PricingContext) -> PricingResult
price(self, instrument: AmericanOption, context: PricingContext) -> PricingResult
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `PricingResult` — Result containing ``price`` and any analytics produced by the engine.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.

## `NumericalAnalyticsEngine`

```python
NumericalAnalyticsEngine(self, engine, *, spot_shift=None, volatility_shift=None, rate_shift=None, time_shift_days=None)
```

Add numerical risk analytics and implied-value solvers to an engine.

Omitted settings use the defaults owned by the C++ core. Invalid settings
are rejected by the core when an operation is performed. Spot, volatility,
and rate shifts are absolute; time shifts are calendar days. Measures with
no supported stencil inside a model boundary are ``None`` without
discarding a valid price. Failures from feasible bumped valuations are
still raised.

#### Parameters

- **`engine`** (`pricing engine`) — Engine used for every base and bumped valuation.
- **`spot_shift`** (`float, optional`) — Absolute spot change used by spot-based finite differences.
- **`volatility_shift`** (`float, optional`) — Absolute volatility change used by volatility-based finite differences.
- **`rate_shift`** (`float, optional`) — Absolute risk-free-rate change used by rate-based finite differences.
- **`time_shift_days`** (`int, optional`) — Calendar-day step used by time-based finite differences.
#### Raises

- `TypeError` — If a supplied setting cannot be converted to its required type.
- `KiyosiError` — When a supplied setting is rejected by the core during an operation.
#### Notes

The wrapper is immutable only with respect to ``engine`` access: the
property has no setter. It does not copy the wrapped engine.

### `engine`

Return the wrapped pricing engine.

#### Returns

- `pricing engine` — The same engine object passed to the constructor.

### `price`

```python
price(self, instrument, context)
```

Price an instrument and calculate feasible numerical risk measures.

#### Parameters

- **`instrument`** (`instrument`) — Instrument supported by the wrapped engine.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `PricingResult` — Price and each feasible numerical risk measure. An infeasible or unsupported measure is ``None``.
#### Raises

- `TypeError` — If the engine and instrument combination is not supported.
- `KiyosiError` — If the core rejects the inputs or a feasible valuation fails.

### `implied_volatility`

```python
implied_volatility(self, instrument, context, observed_price, *, lower_bound=None, upper_bound=None, tolerance=None, max_iterations=None)
```

Solve for the volatility that matches an observed price.

#### Parameters

- **`instrument`** (`instrument`) — Instrument supported by the wrapped engine.
- **`context`** (`PricingContext`) — Market state whose volatility is varied by the solver.
- **`observed_price`** (`float`) — Target instrument price.
- **`lower_bound`** (`float, optional`) — Lower volatility bound. Uses the core default when omitted.
- **`upper_bound`** (`float, optional`) — Upper volatility bound. Uses the core default when omitted.
- **`tolerance`** (`float, optional`) — Solver convergence tolerance. Uses the core default when omitted.
- **`max_iterations`** (`int, optional`) — Maximum solver iterations. Uses the core default when omitted.
#### Returns

- `float` — Implied volatility as a decimal rate.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the inputs are invalid, the target is not bracketed, or the solver does not converge.

### `implied_coupon`

```python
implied_coupon(self, instrument, context, observed_price, *, quote_convention=None, lower_bound=None, upper_bound=None, tolerance=None, max_iterations=None)
```

Solve for the coupon rate that matches an observed price.

Snowball instruments require an explicit quote_convention. Phoenix
instruments have one unambiguous coupon and require none.

#### Parameters

- **`instrument`** (`SnowballOption, BinarySnowballOption, TernarySnowballOption, or PhoenixOption`) — Coupon-bearing instrument supported by the wrapped engine.
- **`context`** (`PricingContext`) — Market state used by the solver.
- **`observed_price`** (`float`) — Target instrument price.
- **`quote_convention`** (`CouponQuoteConvention, optional`) — Snowball coupon component to shift. Required for snowballs and omitted for Phoenix options.
- **`lower_bound`** (`float, optional`) — Lower coupon-rate bound. Uses the core default when omitted.
- **`upper_bound`** (`float, optional`) — Upper coupon-rate bound. Uses the core default when omitted.
- **`tolerance`** (`float, optional`) — Solver convergence tolerance. Uses the core default when omitted.
- **`max_iterations`** (`int, optional`) — Maximum solver iterations. Uses the core default when omitted.
#### Returns

- `float` — Implied coupon rate as a decimal rate.
#### Raises

- `TypeError` — If the engine/instrument combination or quote convention is not supported, or an argument has an incompatible representation.
- `KiyosiError` — If the inputs are invalid, the target is not bracketed, or the solver does not converge.

## `QuadratureDigitalEngine`

```python
QuadratureDigitalEngine(self) -> None
```

Stateless pricing engine.

The engine has no configuration and may be reused across supported instruments
and contexts. Concurrent calls are safe.

### Constructor

Create a stateless pricing engine.

#### Returns

- `pricing engine` — Reusable engine with no mutable configuration.

### `price`

```python
price(self, instrument: CashOrNothingOption, context: PricingContext) -> PricingResult
price(self, instrument: AssetOrNothingOption, context: PricingContext) -> PricingResult
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `PricingResult` — Result containing ``price`` and any analytics produced by the engine.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.

## `QuadratureVanillaEngine`

```python
QuadratureVanillaEngine(self) -> None
```

Stateless pricing engine.

The engine has no configuration and may be reused across supported instruments
and contexts. Concurrent calls are safe.

### Constructor

Create a stateless pricing engine.

#### Returns

- `pricing engine` — Reusable engine with no mutable configuration.

### `price`

```python
price(self, instrument: EuropeanOption, context: PricingContext) -> PricingResult
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `PricingResult` — Result containing ``price`` and any analytics produced by the engine.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.

## `TurnbullWakemanArithmeticAveragePriceEngine`

```python
TurnbullWakemanArithmeticAveragePriceEngine(self) -> None
```

Stateless pricing engine.

The engine has no configuration and may be reused across supported instruments
and contexts. Concurrent calls are safe.

### Constructor

Create a stateless pricing engine.

#### Returns

- `pricing engine` — Reusable engine with no mutable configuration.

### `price`

```python
price(self, instrument: ArithmeticAveragePriceOption, context: PricingContext) -> PricingResult
```

Price an instrument under a market context.

#### Parameters

- **`instrument`** (`instrument`) — Instrument accepted by this overload.
- **`context`** (`PricingContext`) — Market state and valuation instant.
#### Returns

- `PricingResult` — Result containing ``price`` and any analytics produced by the engine.
#### Raises

- `KiyosiError` — If instrument terms, context, engine settings, backend availability, or the requested valuation are invalid.

## `calculate_numerical_risk_measures`

```python
calculate_numerical_risk_measures(engine: AnalyticVanillaEngine, instrument: EuropeanOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: QuadratureVanillaEngine, instrument: EuropeanOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: CoxRossRubinsteinVanillaEngine, instrument: EuropeanOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: CoxRossRubinsteinVanillaEngine, instrument: AmericanOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: BjerksundStenslandVanillaEngine, instrument: AmericanOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: FiniteDifferenceVanillaEngine, instrument: EuropeanOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: FiniteDifferenceVanillaEngine, instrument: AmericanOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: MonteCarloVanillaEngine, instrument: EuropeanOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: MonteCarloVanillaEngine, instrument: AmericanOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: AnalyticDigitalEngine, instrument: CashOrNothingOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: AnalyticDigitalEngine, instrument: AssetOrNothingOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: QuadratureDigitalEngine, instrument: CashOrNothingOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: QuadratureDigitalEngine, instrument: AssetOrNothingOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: FiniteDifferenceDigitalEngine, instrument: CashOrNothingOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: FiniteDifferenceDigitalEngine, instrument: AssetOrNothingOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: AnalyticBarrierEngine, instrument: BarrierOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: FiniteDifferenceBarrierEngine, instrument: BarrierOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: AnalyticBinaryBarrierEngine, instrument: BinaryBarrierOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: AnalyticBinaryBarrierEngine, instrument: TouchOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: AnalyticGeometricAveragePriceEngine, instrument: GeometricAveragePriceOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: TurnbullWakemanArithmeticAveragePriceEngine, instrument: ArithmeticAveragePriceOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: FiniteDifferenceAccumulatorEngine, instrument: Accumulator, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: MonteCarloAccumulatorEngine, instrument: Accumulator, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: FiniteDifferenceSnowballEngine, instrument: SnowballOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: MonteCarloSnowballEngine, instrument: SnowballOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: FiniteDifferenceBinarySnowballEngine, instrument: BinarySnowballOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: MonteCarloBinarySnowballEngine, instrument: BinarySnowballOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: FiniteDifferenceTernarySnowballEngine, instrument: TernarySnowballOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: MonteCarloTernarySnowballEngine, instrument: TernarySnowballOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: FiniteDifferencePhoenixEngine, instrument: PhoenixOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
calculate_numerical_risk_measures(engine: MonteCarloPhoenixEngine, instrument: PhoenixOption, context: PricingContext, *, spot_shift: float = 0.01, volatility_shift: float = 0.0001, rate_shift: float = 0.0001, time_shift_days: int = 1) -> PricingResult
```

Compute price and every feasible numerical risk measure.

Shifts are absolute. Omitted shifts use core-owned defaults. A measure with no
valid finite-difference stencil inside a model boundary is ``None`` while other
valid results are preserved.

#### Parameters

- **`engine`** (`pricing engine`) — Engine used for every base and bumped valuation.
- **`instrument`** (`instrument`) — Instrument supported by the engine.
- **`context`** (`PricingContext`) — Market state and valuation instant.
- **`spot_shift`** (`float, optional`) — Absolute spot change for spot-based sensitivities.
- **`volatility_shift`** (`float, optional`) — Absolute volatility change for volatility-based sensitivities.
- **`rate_shift`** (`float, optional`) — Absolute risk-free-rate change for rate-based sensitivities.
- **`time_shift_days`** (`int, optional`) — Calendar-day step for time-based sensitivities.
#### Returns

- `PricingResult` — Price and each feasible numerical sensitivity.
#### Raises

- `TypeError` — If the engine/instrument combination or a setting is incompatible.
- `KiyosiError` — If the inputs are invalid or a feasible valuation fails.

## `implied_coupon`

```python
implied_coupon(engine: FiniteDifferenceSnowballEngine, instrument: SnowballOption, context: PricingContext, observed_price: float, *, quote_convention: CouponQuoteConvention, lower_bound: float = 0.0, upper_bound: float = 2.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_coupon(engine: MonteCarloSnowballEngine, instrument: SnowballOption, context: PricingContext, observed_price: float, *, quote_convention: CouponQuoteConvention, lower_bound: float = 0.0, upper_bound: float = 2.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_coupon(engine: FiniteDifferenceBinarySnowballEngine, instrument: BinarySnowballOption, context: PricingContext, observed_price: float, *, quote_convention: CouponQuoteConvention, lower_bound: float = 0.0, upper_bound: float = 2.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_coupon(engine: MonteCarloBinarySnowballEngine, instrument: BinarySnowballOption, context: PricingContext, observed_price: float, *, quote_convention: CouponQuoteConvention, lower_bound: float = 0.0, upper_bound: float = 2.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_coupon(engine: FiniteDifferenceTernarySnowballEngine, instrument: TernarySnowballOption, context: PricingContext, observed_price: float, *, quote_convention: CouponQuoteConvention, lower_bound: float = 0.0, upper_bound: float = 2.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_coupon(engine: MonteCarloTernarySnowballEngine, instrument: TernarySnowballOption, context: PricingContext, observed_price: float, *, quote_convention: CouponQuoteConvention, lower_bound: float = 0.0, upper_bound: float = 2.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_coupon(engine: FiniteDifferencePhoenixEngine, instrument: PhoenixOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0, upper_bound: float = 2.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_coupon(engine: MonteCarloPhoenixEngine, instrument: PhoenixOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0, upper_bound: float = 2.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
```

Overloaded function.

1. ``implied_coupon(engine: kiyosi._native.FiniteDifferenceSnowballEngine, instrument: kiyosi._native.SnowballOption, context: kiyosi._native.PricingContext, observed_price: float, *, quote_convention: kiyosi._native.CouponQuoteConvention, lower_bound: float = 0.0, upper_bound: float = 2.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float``

Solve for a snowball coupon rate that matches an observed price.

#### Parameters

- **`engine`** (`pricing engine`) — Engine used for trial valuations.
- **`instrument`** (`SnowballOption, BinarySnowballOption, or TernarySnowballOption`) — Snowball instrument supported by the engine.
- **`context`** (`PricingContext`) — Market state used by the solver.
- **`observed_price`** (`float`) — Target instrument price.
- **`quote_convention`** (`CouponQuoteConvention`) — Whether the maturity coupon shifts with quoted knock-out coupons.
- **`lower_bound, upper_bound`** (`float, optional`) — Coupon-rate search interval. Omitted values use core defaults.
- **`tolerance`** (`float, optional`) — Solver convergence tolerance.
- **`max_iterations`** (`int, optional`) — Maximum solver iterations.
#### Returns

- `float` — Implied annualized quoted coupon rate.
#### Raises

- `TypeError` — If the engine/instrument combination or an argument is incompatible.
- `KiyosiError` — If inputs are invalid, the target is not bracketed, or the solver fails.
2. ``implied_coupon(engine: kiyosi._native.MonteCarloSnowballEngine, instrument: kiyosi._native.SnowballOption, context: kiyosi._native.PricingContext, observed_price: float, *, quote_convention: kiyosi._native.CouponQuoteConvention, lower_bound: float = 0.0, upper_bound: float = 2.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float``

Solve for a snowball coupon rate that matches an observed price.

#### Parameters

- **`engine`** (`pricing engine`) — Engine used for trial valuations.
- **`instrument`** (`SnowballOption, BinarySnowballOption, or TernarySnowballOption`) — Snowball instrument supported by the engine.
- **`context`** (`PricingContext`) — Market state used by the solver.
- **`observed_price`** (`float`) — Target instrument price.
- **`quote_convention`** (`CouponQuoteConvention`) — Whether the maturity coupon shifts with quoted knock-out coupons.
- **`lower_bound, upper_bound`** (`float, optional`) — Coupon-rate search interval. Omitted values use core defaults.
- **`tolerance`** (`float, optional`) — Solver convergence tolerance.
- **`max_iterations`** (`int, optional`) — Maximum solver iterations.
#### Returns

- `float` — Implied annualized quoted coupon rate.
#### Raises

- `TypeError` — If the engine/instrument combination or an argument is incompatible.
- `KiyosiError` — If inputs are invalid, the target is not bracketed, or the solver fails.
3. ``implied_coupon(engine: kiyosi._native.FiniteDifferenceBinarySnowballEngine, instrument: kiyosi._native.BinarySnowballOption, context: kiyosi._native.PricingContext, observed_price: float, *, quote_convention: kiyosi._native.CouponQuoteConvention, lower_bound: float = 0.0, upper_bound: float = 2.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float``

Solve for a snowball coupon rate that matches an observed price.

#### Parameters

- **`engine`** (`pricing engine`) — Engine used for trial valuations.
- **`instrument`** (`SnowballOption, BinarySnowballOption, or TernarySnowballOption`) — Snowball instrument supported by the engine.
- **`context`** (`PricingContext`) — Market state used by the solver.
- **`observed_price`** (`float`) — Target instrument price.
- **`quote_convention`** (`CouponQuoteConvention`) — Whether the maturity coupon shifts with quoted knock-out coupons.
- **`lower_bound, upper_bound`** (`float, optional`) — Coupon-rate search interval. Omitted values use core defaults.
- **`tolerance`** (`float, optional`) — Solver convergence tolerance.
- **`max_iterations`** (`int, optional`) — Maximum solver iterations.
#### Returns

- `float` — Implied annualized quoted coupon rate.
#### Raises

- `TypeError` — If the engine/instrument combination or an argument is incompatible.
- `KiyosiError` — If inputs are invalid, the target is not bracketed, or the solver fails.
4. ``implied_coupon(engine: kiyosi._native.MonteCarloBinarySnowballEngine, instrument: kiyosi._native.BinarySnowballOption, context: kiyosi._native.PricingContext, observed_price: float, *, quote_convention: kiyosi._native.CouponQuoteConvention, lower_bound: float = 0.0, upper_bound: float = 2.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float``

Solve for a snowball coupon rate that matches an observed price.

#### Parameters

- **`engine`** (`pricing engine`) — Engine used for trial valuations.
- **`instrument`** (`SnowballOption, BinarySnowballOption, or TernarySnowballOption`) — Snowball instrument supported by the engine.
- **`context`** (`PricingContext`) — Market state used by the solver.
- **`observed_price`** (`float`) — Target instrument price.
- **`quote_convention`** (`CouponQuoteConvention`) — Whether the maturity coupon shifts with quoted knock-out coupons.
- **`lower_bound, upper_bound`** (`float, optional`) — Coupon-rate search interval. Omitted values use core defaults.
- **`tolerance`** (`float, optional`) — Solver convergence tolerance.
- **`max_iterations`** (`int, optional`) — Maximum solver iterations.
#### Returns

- `float` — Implied annualized quoted coupon rate.
#### Raises

- `TypeError` — If the engine/instrument combination or an argument is incompatible.
- `KiyosiError` — If inputs are invalid, the target is not bracketed, or the solver fails.
5. ``implied_coupon(engine: kiyosi._native.FiniteDifferenceTernarySnowballEngine, instrument: kiyosi._native.TernarySnowballOption, context: kiyosi._native.PricingContext, observed_price: float, *, quote_convention: kiyosi._native.CouponQuoteConvention, lower_bound: float = 0.0, upper_bound: float = 2.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float``

Solve for a snowball coupon rate that matches an observed price.

#### Parameters

- **`engine`** (`pricing engine`) — Engine used for trial valuations.
- **`instrument`** (`SnowballOption, BinarySnowballOption, or TernarySnowballOption`) — Snowball instrument supported by the engine.
- **`context`** (`PricingContext`) — Market state used by the solver.
- **`observed_price`** (`float`) — Target instrument price.
- **`quote_convention`** (`CouponQuoteConvention`) — Whether the maturity coupon shifts with quoted knock-out coupons.
- **`lower_bound, upper_bound`** (`float, optional`) — Coupon-rate search interval. Omitted values use core defaults.
- **`tolerance`** (`float, optional`) — Solver convergence tolerance.
- **`max_iterations`** (`int, optional`) — Maximum solver iterations.
#### Returns

- `float` — Implied annualized quoted coupon rate.
#### Raises

- `TypeError` — If the engine/instrument combination or an argument is incompatible.
- `KiyosiError` — If inputs are invalid, the target is not bracketed, or the solver fails.
6. ``implied_coupon(engine: kiyosi._native.MonteCarloTernarySnowballEngine, instrument: kiyosi._native.TernarySnowballOption, context: kiyosi._native.PricingContext, observed_price: float, *, quote_convention: kiyosi._native.CouponQuoteConvention, lower_bound: float = 0.0, upper_bound: float = 2.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float``

Solve for a snowball coupon rate that matches an observed price.

#### Parameters

- **`engine`** (`pricing engine`) — Engine used for trial valuations.
- **`instrument`** (`SnowballOption, BinarySnowballOption, or TernarySnowballOption`) — Snowball instrument supported by the engine.
- **`context`** (`PricingContext`) — Market state used by the solver.
- **`observed_price`** (`float`) — Target instrument price.
- **`quote_convention`** (`CouponQuoteConvention`) — Whether the maturity coupon shifts with quoted knock-out coupons.
- **`lower_bound, upper_bound`** (`float, optional`) — Coupon-rate search interval. Omitted values use core defaults.
- **`tolerance`** (`float, optional`) — Solver convergence tolerance.
- **`max_iterations`** (`int, optional`) — Maximum solver iterations.
#### Returns

- `float` — Implied annualized quoted coupon rate.
#### Raises

- `TypeError` — If the engine/instrument combination or an argument is incompatible.
- `KiyosiError` — If inputs are invalid, the target is not bracketed, or the solver fails.
7. ``implied_coupon(engine: kiyosi._native.FiniteDifferencePhoenixEngine, instrument: kiyosi._native.PhoenixOption, context: kiyosi._native.PricingContext, observed_price: float, *, lower_bound: float = 0.0, upper_bound: float = 2.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float``

Solve for a Phoenix coupon rate that matches an observed price.

#### Parameters

- **`engine`** (`pricing engine`) — Engine used for trial valuations.
- **`instrument`** (`PhoenixOption`) — Phoenix option supported by the engine.
- **`context`** (`PricingContext`) — Market state used by the solver.
- **`observed_price`** (`float`) — Target instrument price.
- **`lower_bound, upper_bound`** (`float, optional`) — Coupon-rate search interval. Omitted values use core defaults.
- **`tolerance`** (`float, optional`) — Solver convergence tolerance.
- **`max_iterations`** (`int, optional`) — Maximum solver iterations.
#### Returns

- `float` — Implied annualized coupon rate.
#### Raises

- `TypeError` — If the engine/instrument combination or an argument is incompatible.
- `KiyosiError` — If inputs are invalid, the target is not bracketed, or the solver fails.
8. ``implied_coupon(engine: kiyosi._native.MonteCarloPhoenixEngine, instrument: kiyosi._native.PhoenixOption, context: kiyosi._native.PricingContext, observed_price: float, *, lower_bound: float = 0.0, upper_bound: float = 2.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float``

Solve for a Phoenix coupon rate that matches an observed price.

#### Parameters

- **`engine`** (`pricing engine`) — Engine used for trial valuations.
- **`instrument`** (`PhoenixOption`) — Phoenix option supported by the engine.
- **`context`** (`PricingContext`) — Market state used by the solver.
- **`observed_price`** (`float`) — Target instrument price.
- **`lower_bound, upper_bound`** (`float, optional`) — Coupon-rate search interval. Omitted values use core defaults.
- **`tolerance`** (`float, optional`) — Solver convergence tolerance.
- **`max_iterations`** (`int, optional`) — Maximum solver iterations.
#### Returns

- `float` — Implied annualized coupon rate.
#### Raises

- `TypeError` — If the engine/instrument combination or an argument is incompatible.
- `KiyosiError` — If inputs are invalid, the target is not bracketed, or the solver fails.

## `implied_volatility`

```python
implied_volatility(engine: AnalyticVanillaEngine, instrument: EuropeanOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: QuadratureVanillaEngine, instrument: EuropeanOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: CoxRossRubinsteinVanillaEngine, instrument: EuropeanOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: CoxRossRubinsteinVanillaEngine, instrument: AmericanOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: BjerksundStenslandVanillaEngine, instrument: AmericanOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: FiniteDifferenceVanillaEngine, instrument: EuropeanOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: FiniteDifferenceVanillaEngine, instrument: AmericanOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: MonteCarloVanillaEngine, instrument: EuropeanOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: MonteCarloVanillaEngine, instrument: AmericanOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: AnalyticDigitalEngine, instrument: CashOrNothingOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: AnalyticDigitalEngine, instrument: AssetOrNothingOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: QuadratureDigitalEngine, instrument: CashOrNothingOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: QuadratureDigitalEngine, instrument: AssetOrNothingOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: FiniteDifferenceDigitalEngine, instrument: CashOrNothingOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: FiniteDifferenceDigitalEngine, instrument: AssetOrNothingOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: AnalyticBarrierEngine, instrument: BarrierOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: FiniteDifferenceBarrierEngine, instrument: BarrierOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: AnalyticBinaryBarrierEngine, instrument: BinaryBarrierOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: AnalyticBinaryBarrierEngine, instrument: TouchOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: AnalyticGeometricAveragePriceEngine, instrument: GeometricAveragePriceOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: TurnbullWakemanArithmeticAveragePriceEngine, instrument: ArithmeticAveragePriceOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: FiniteDifferenceAccumulatorEngine, instrument: Accumulator, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: MonteCarloAccumulatorEngine, instrument: Accumulator, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: FiniteDifferenceSnowballEngine, instrument: SnowballOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: MonteCarloSnowballEngine, instrument: SnowballOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: FiniteDifferenceBinarySnowballEngine, instrument: BinarySnowballOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: MonteCarloBinarySnowballEngine, instrument: BinarySnowballOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: FiniteDifferenceTernarySnowballEngine, instrument: TernarySnowballOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: MonteCarloTernarySnowballEngine, instrument: TernarySnowballOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: FiniteDifferencePhoenixEngine, instrument: PhoenixOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
implied_volatility(engine: MonteCarloPhoenixEngine, instrument: PhoenixOption, context: PricingContext, observed_price: float, *, lower_bound: float = 0.0001, upper_bound: float = 4.0, tolerance: float = 1e-08, max_iterations: int = 100) -> float
```

Solve for the volatility that matches an observed price.

#### Parameters

- **`engine`** (`pricing engine`) — Engine used for trial valuations.
- **`instrument`** (`instrument`) — Instrument supported by the engine.
- **`context`** (`PricingContext`) — Market state whose volatility is varied.
- **`observed_price`** (`float`) — Target instrument price.
- **`lower_bound, upper_bound`** (`float, optional`) — Volatility search interval. Omitted values use core defaults.
- **`tolerance`** (`float, optional`) — Solver convergence tolerance.
- **`max_iterations`** (`int, optional`) — Maximum solver iterations.
#### Returns

- `float` — Implied volatility as a decimal rate.
#### Raises

- `TypeError` — If the engine/instrument combination or an argument is incompatible.
- `KiyosiError` — If inputs are invalid, the target is not bracketed, or the solver fails.
