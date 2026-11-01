---
description: kiyosi.pricing 的 Python API 参考文档。
outline: [2, 4]
---

# `kiyosi.pricing`

Price contracts, compute sensitivities, and solve implied parameters.

Finite-difference engines support local volatility for European and American
vanilla options, digitals, single and double barriers, binary barriers, touch
and no-touch options, autocallable notes and accumulators. They provide price,
delta and gamma, holding the absolute surface fixed. Other Greeks (including
"all"), non-FD engines and inverse solves raise UnsupportedOperationError for
this model. Digital FD requires explicitly flat risk-free and dividend rates.
Delta/gamma are absent at expiry and unavailable event-crossing stencils.
Surface coverage follows remaining stochastic evolution; rates must cover
required discounting. Automatic domains use the maximum interpolated local
volatility over the remaining stochastic horizon. Check time, space and boundary
convergence for local-volatility domains, including automatically selected domains.

``FiniteDifferenceScheme`` selects ``"explicit_euler"``, ``"implicit_euler"``,
``"crank_nicolson"`` (without time-step damping), or ``"rannacher"`` (the default).
Rannacher replaces each of the first two time intervals with two implicit Euler
half-steps and restarts after scheduled barrier, accumulator and autocallable
observations. Payoff averaging and spatial discretization apply independently
of the time scheme. ``MonteCarloSampling`` selects
``"pseudo_random"`` or scrambled ``"sobol"``; a fixed seed reproduces draws
across thread counts in the same build. Sobol estimates omit sampling error.
Autocallable and accumulator ``price`` calls return the sample mean;
``price_with_statistics`` also computes and validates sampling uncertainty.

Pricing raises ``ComputationFailureError`` for materially negative option
prices; only rounding-sized negative results may be clipped to zero.
Coarse numerical grids may require refinement before pricing succeeds.
American Monte Carlo also rejects non-finite continuation regressions;
finite fits with insufficient independent samples use a lower polynomial degree.

``AnalyticEuropeanEngine``, ``CoxRossRubinsteinDigitalEngine``,
``CoxRossRubinsteinBarrierEngine``, ``MonteCarloDigitalEngine`` and
``MonteCarloAsianEngine`` compute native Greeks without numerical bumps;
their ``price_with_greeks`` methods accept only ``greeks`` as a request
control. Engines that use numerical differences also accept bump
settings.
``volatility_shift`` controls the volatility bump for vega and volga;
``rate_shift`` controls parallel bumps of both the risk-free and dividend-yield
curves for rho and dividend_rho. Numerical volga requires a strictly positive
lower volatility leg. Monte Carlo volga can amplify sampling and exercise noise;
check convergence across bump sizes and simulation settings.

``MonteCarloBarrierEngine`` and ``MonteCarloDoubleBarrierEngine`` return only
delta and gamma. Their only bump control is ``spot_shift``, used for barrier
availability checks and numerical derivatives of continuous at-hit rebates.

Pass ``greeks="all"`` to request every measure, a Greek name for one measure,
or an iterable of names for a selection. The ``greeks`` argument is required;
unavailable measures remain None.

Pricing controls are explicit keyword-only parameters, available through
``inspect.signature``. Instrument conversion and supported-family checks
precede Greek-name parsing. Monte Carlo vanilla spot bumps default by product:
0.01 for European options and 8% of spot for American options. Explicit
``None`` selects the automatic bump for either product.

``CouponQuoteConvention`` controls whether a snowball's maturity coupon
shifts with observation coupons (``"shift_maturity_coupon"``) or stays fixed
(``"preserve_maturity_coupon"``). Phoenix coupon solves omit this choice;
the displayed default ``...`` (``Ellipsis``) also means omitted.
Unsupported coupon-solver instruments are rejected before checking this choice.
Phoenix solves preserve the contract's coupon units: annual rate for annual
coupons, fixed per-period proportion for FCN/DCN. Bounds, parameter tolerance
and the returned value use the same units.

## Examples

Price a European call and request its delta and vega:

```python
>>> from datetime import date
>>> from kiyosi.instruments import EuropeanOption
>>> from kiyosi.market import BlackScholesMertonParameters, PricingContext
>>> from kiyosi.pricing import AnalyticEuropeanEngine
>>> option = EuropeanOption(
...     option_type="call", strike=100,
...     effective_date=date(2025, 1, 1), expiry_date=date(2026, 1, 1),
... )
>>> context = PricingContext(
...     model_parameters=BlackScholesMertonParameters(
...         risk_free_rate=0.05, dividend_yield=0.02, volatility=0.2,
...     ),
...     spot_price=100, valuation_time=date(2025, 1, 1),
... )
>>> result = AnalyticEuropeanEngine().price_with_greeks(
...     option, context, greeks=["delta", "vega"],
... )
>>> round(result.price, 6)
9.227006
>>> result.require("delta") > 0
True
>>> sensitivities = AnalyticEuropeanEngine().price_with_greeks(
...     option, context, greeks="all",
... )
>>> sensitivities.require("gamma") > 0
True
>>> round(sensitivities.require("volga"), 8)
0.00023688
>>> round(sensitivities.require("dividend_rho"), 6)
-0.586851
```


Recover the model volatility from its price using a chosen bracket:

```python
>>> sigma = implied_volatility(
...     AnalyticEuropeanEngine(), option, context, result.price,
...     lower_bound=0.1, upper_bound=0.3,
... )
>>> round(sigma, 6)
0.2
```

## `AnalyticBarrierEngine`

```python
AnalyticBarrierEngine()
```

Flat-rate single-barrier analytics with BGK scheduled monitoring.

#### See Also

BarrierOption : Supported contract.

### `price`

```python
price(self, /, instrument, context)
```

Returns the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks, *, spot_shift=Ellipsis, volatility_shift=Ellipsis, rate_shift=Ellipsis, time_shift_days=Ellipsis)
```

Returns the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

## `AnalyticBinaryBarrierEngine`

```python
AnalyticBinaryBarrierEngine()
```

Flat-rate binary-barrier and single-touch analytics.

#### See Also

BinaryBarrierOption : Supported contract.
TouchOption : Supported contract.

### `price`

```python
price(self, /, instrument, context)
```

Return the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks, *, spot_shift=Ellipsis, volatility_shift=Ellipsis, rate_shift=Ellipsis, time_shift_days=Ellipsis)
```

Returns the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

## `AnalyticDigitalEngine`

```python
AnalyticDigitalEngine()
```

Analytic European digital pricing with deterministic rate curves.

#### See Also

CashOrNothingOption : Supported contract.
AssetOrNothingOption : Supported contract.

### `price`

```python
price(self, /, instrument, context)
```

Return the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks, *, spot_shift=Ellipsis, volatility_shift=Ellipsis, rate_shift=Ellipsis, time_shift_days=Ellipsis)
```

Returns the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

## `AnalyticDoubleBarrierEngine`

```python
AnalyticDoubleBarrierEngine()
```

Flat-rate continuous double-barrier analytics.

#### See Also

DoubleBarrierOption : Supported contract.

### `price`

```python
price(self, /, instrument, context)
```

Returns the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks, *, spot_shift=Ellipsis, volatility_shift=Ellipsis, rate_shift=Ellipsis, time_shift_days=Ellipsis)
```

Returns the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

## `AnalyticDoubleTouchEngine`

```python
AnalyticDoubleTouchEngine()
```

Prices continuous cash double-touch and double-no-touch contracts with flat rates.

Either inclusive barrier triggers a touch. Supports expiry payments and
double-touch at-hit payments; past at-hit payments have zero remaining value.
Uses image/spectral series and adaptive first-exit integration for at-hit payments.
Node curves are always rejected; unresolved scheduled monitoring is unsupported.
Resolved scheduled cashflows are priced after calendar and history validation.
Greeks use numerical differences; expiry and current barrier equality without
a prior touch omit Greeks. Stencils crossing a barrier omit affected measures.

#### See Also

DoubleTouchOption : Supported cash contract.
cash_double_touch : Double one-touch constructor.
cash_double_no_touch : Double no-touch constructor.
FiniteDifferenceDoubleTouchEngine : Supports schedules and node curves.

### `price`

```python
price(self, /, instrument, context)
```

Returns the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks, *, spot_shift=Ellipsis, volatility_shift=Ellipsis, rate_shift=Ellipsis, time_shift_days=Ellipsis)
```

Returns the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

## `AnalyticEuropeanEngine`

```python
AnalyticEuropeanEngine()
```

Analytic European vanilla pricing with deterministic rate curves.

#### See Also

EuropeanOption : Supported contract.

### `price`

```python
price(self, /, instrument, context)
```

Return the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, pricing or requested derivatives fail.

## `AnalyticGeometricAveragePriceEngine`

```python
AnalyticGeometricAveragePriceEngine()
```

Prices geometric continuous-average contracts with deterministic rate curves.

#### See Also

GeometricAveragePriceOption : Supported contract.

### `price`

```python
price(self, /, instrument, context)
```

Returns the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks, *, spot_shift=Ellipsis, volatility_shift=Ellipsis, rate_shift=Ellipsis, time_shift_days=Ellipsis)
```

Returns the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

## `AnalyticRangeAccrualEngine`

```python
AnalyticRangeAccrualEngine()
```

Exact BSM range-coupon marginals with deterministic rate curves.

#### See Also

RangeAccrualOption : Supported contract.

### `price`

```python
price(self, /, instrument, context)
```

Returns the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks, *, spot_shift=Ellipsis, volatility_shift=Ellipsis, rate_shift=Ellipsis, time_shift_days=Ellipsis)
```

Returns the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

## `BjerksundStenslandVanillaEngine`

```python
BjerksundStenslandVanillaEngine()
```

Bjerksund-Stensland 2002 American approximation with flat rates.

#### See Also

AmericanOption : Supported contract.

### `price`

```python
price(self, /, instrument, context)
```

Return the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks, *, spot_shift=Ellipsis, volatility_shift=Ellipsis, rate_shift=Ellipsis, time_shift_days=Ellipsis)
```

Returns the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

## `CouponQuoteConvention`

```python
CouponQuoteConvention = typing.Literal['shift_maturity_coupon', 'preserve_maturity_coupon']
```

## `CoxRossRubinsteinBarrierEngine`

```python
CoxRossRubinsteinBarrierEngine(*, step_count=Ellipsis)
```

Flat-rate Cox-Ross-Rubinstein tree pricing.

#### Parameters

- **`step_count`** (`int, optional`) — Number of tree time steps, from 1 through 1,000,000; defaults to 256.
#### Raises

- `InvalidInputError` — If step_count is outside 1 through 1,000,000.
#### Notes

Provides node delta/gamma for its product family; other Greeks are absent.

#### See Also

BarrierOption : Supported contract.

### `price`

```python
price(self, /, instrument, context)
```

Return the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If request validation or pricing fails.

### `step_count`

Return the configured grid size.

## `CoxRossRubinsteinDigitalEngine`

```python
CoxRossRubinsteinDigitalEngine(*, step_count=Ellipsis)
```

Flat-rate Cox-Ross-Rubinstein tree pricing.

#### Parameters

- **`step_count`** (`int, optional`) — Number of tree time steps, from 1 through 1,000,000; defaults to 256.
#### Raises

- `InvalidInputError` — If step_count is outside 1 through 1,000,000.
#### Notes

Provides node delta/gamma for its product family; other Greeks are absent.

#### See Also

CashOrNothingOption : Supported contract.
AssetOrNothingOption : Supported contract.

### `price`

```python
price(self, /, instrument, context)
```

Return the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If request validation or pricing fails.

### `step_count`

Return the configured grid size.

## `CoxRossRubinsteinVanillaEngine`

```python
CoxRossRubinsteinVanillaEngine(*, step_count=Ellipsis)
```

Flat-rate Cox-Ross-Rubinstein tree pricing.

#### Parameters

- **`step_count`** (`int, optional`) — Number of tree time steps, from 1 through 1,000,000; defaults to 256.
#### Raises

- `InvalidInputError` — If step_count is outside 1 through 1,000,000.
#### Notes

Accepts EuropeanOption and AmericanOption.

### `price`

```python
price(self, /, instrument, context)
```

Return the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks, *, spot_shift=Ellipsis, volatility_shift=Ellipsis, rate_shift=Ellipsis, time_shift_days=Ellipsis)
```

Returns the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

### `step_count`

Return the configured grid size.

## `FiniteDifferenceAccumulatorEngine`

```python
FiniteDifferenceAccumulatorEngine(*, asset_step_count=Ellipsis, time_step_count=Ellipsis, scheme=Ellipsis, asset_upper_boundary=None)
```

Finite-difference pricing with immutable grid settings.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial steps, at least 3; defaults to 800.
- **`time_step_count`** (`int, optional`) — Positive time-step budget; event dates and curve knots are added. Read `FiniteDifferenceAccumulatorEngine().time_step_count` for the engine's default.
- **`scheme`** (`FiniteDifferenceScheme, optional`) — Time-marching scheme; defaults to "rannacher" (damped Crank-Nicolson). "crank_nicolson" uses standard Crank-Nicolson without time-step damping.
- **`asset_upper_boundary`** (`float or None, optional`) — Finite positive upper spot boundary, or None (default) for the automatic domain. Must exceed spot, strike and barriers at pricing.
#### Raises

- `InvalidInputError` — If asset_step_count is below 3, time_step_count is below 1, or an explicit upper boundary is nonpositive or non-finite. Boundary coverage and explicit-Euler stability are checked during pricing.
#### Notes

The engine name selects its product family. The vanilla engine accepts
EuropeanOption and AmericanOption. The digital engine accepts
CashOrNothingOption and AssetOrNothingOption. The binary-barrier engine
also accepts TouchOption. The autocallable engine accepts all snowball
variants and PhoenixOption. Other engines accept their named product.
Digital pricing requires explicitly flat rates; other families accept
deterministic rate curves. All FD product families support local-volatility
price, delta and gamma, including American exercise. Other Greeks (including
"all") and inverse solves raise UnsupportedOperationError. Sigma uses
fixed absolute surface coordinates; Greeks are absent at expiry or where
their stencils cross product events. Surface coverage follows remaining
stochastic evolution; rate coverage follows required future discounting.
Automatic local-volatility domains require convergence checks.

### `asset_step_count`

Return the configured spatial grid budget.

### `asset_upper_boundary`

Return the explicit upper spot boundary, or None for automatic selection.

### `price`

```python
price(self, /, instrument, context)
```

Return the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks, *, spot_shift=Ellipsis, volatility_shift=Ellipsis, rate_shift=Ellipsis, time_shift_days=Ellipsis)
```

Returns the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

### `scheme`

Return the configured time-marching choice string.

### `time_step_count`

Return the configured time-step budget before event insertion.

## `FiniteDifferenceAutocallableEngine`

```python
FiniteDifferenceAutocallableEngine(*, asset_step_count=Ellipsis, time_step_count=Ellipsis, scheme=Ellipsis, asset_upper_boundary=None)
```

Finite-difference pricing with immutable grid settings.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial steps, at least 3; defaults to 800.
- **`time_step_count`** (`int, optional`) — Positive time-step budget; event dates and curve knots are added. Read `FiniteDifferenceAutocallableEngine().time_step_count` for the engine's default.
- **`scheme`** (`FiniteDifferenceScheme, optional`) — Time-marching scheme; defaults to "rannacher" (damped Crank-Nicolson). "crank_nicolson" uses standard Crank-Nicolson without time-step damping.
- **`asset_upper_boundary`** (`float or None, optional`) — Finite positive upper spot boundary, or None (default) for the automatic domain. Must exceed spot, strike and barriers at pricing.
#### Raises

- `InvalidInputError` — If asset_step_count is below 3, time_step_count is below 1, or an explicit upper boundary is nonpositive or non-finite. Boundary coverage and explicit-Euler stability are checked during pricing.
#### Notes

The engine name selects its product family. The vanilla engine accepts
EuropeanOption and AmericanOption. The digital engine accepts
CashOrNothingOption and AssetOrNothingOption. The binary-barrier engine
also accepts TouchOption. The autocallable engine accepts all snowball
variants and PhoenixOption. Other engines accept their named product.
Digital pricing requires explicitly flat rates; other families accept
deterministic rate curves. All FD product families support local-volatility
price, delta and gamma, including American exercise. Other Greeks (including
"all") and inverse solves raise UnsupportedOperationError. Sigma uses
fixed absolute surface coordinates; Greeks are absent at expiry or where
their stencils cross product events. Surface coverage follows remaining
stochastic evolution; rate coverage follows required future discounting.
Automatic local-volatility domains require convergence checks.

### `asset_step_count`

Return the configured spatial grid budget.

### `asset_upper_boundary`

Return the explicit upper spot boundary, or None for automatic selection.

### `price`

```python
price(self, /, instrument, context)
```

Return the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks, *, spot_shift=Ellipsis, volatility_shift=Ellipsis, rate_shift=Ellipsis, time_shift_days=Ellipsis)
```

Returns the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

### `scheme`

Return the configured time-marching choice string.

### `time_step_count`

Return the configured time-step budget before event insertion.

## `FiniteDifferenceBarrierEngine`

```python
FiniteDifferenceBarrierEngine(*, asset_step_count=Ellipsis, time_step_count=Ellipsis, scheme=Ellipsis, asset_upper_boundary=None)
```

Finite-difference pricing with immutable grid settings.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial steps, at least 3; defaults to 800.
- **`time_step_count`** (`int, optional`) — Positive time-step budget; event dates and curve knots are added. Read `FiniteDifferenceBarrierEngine().time_step_count` for the engine's default.
- **`scheme`** (`FiniteDifferenceScheme, optional`) — Time-marching scheme; defaults to "rannacher" (damped Crank-Nicolson). "crank_nicolson" uses standard Crank-Nicolson without time-step damping.
- **`asset_upper_boundary`** (`float or None, optional`) — Finite positive upper spot boundary, or None (default) for the automatic domain. Must exceed spot, strike and barriers at pricing.
#### Raises

- `InvalidInputError` — If asset_step_count is below 3, time_step_count is below 1, or an explicit upper boundary is nonpositive or non-finite. Boundary coverage and explicit-Euler stability are checked during pricing.
#### Notes

The engine name selects its product family. The vanilla engine accepts
EuropeanOption and AmericanOption. The digital engine accepts
CashOrNothingOption and AssetOrNothingOption. The binary-barrier engine
also accepts TouchOption. The autocallable engine accepts all snowball
variants and PhoenixOption. Other engines accept their named product.
Digital pricing requires explicitly flat rates; other families accept
deterministic rate curves. All FD product families support local-volatility
price, delta and gamma, including American exercise. Other Greeks (including
"all") and inverse solves raise UnsupportedOperationError. Sigma uses
fixed absolute surface coordinates; Greeks are absent at expiry or where
their stencils cross product events. Surface coverage follows remaining
stochastic evolution; rate coverage follows required future discounting.
Automatic local-volatility domains require convergence checks.

### `asset_step_count`

Return the configured spatial grid budget.

### `asset_upper_boundary`

Return the explicit upper spot boundary, or None for automatic selection.

### `price`

```python
price(self, /, instrument, context)
```

Return the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks, *, spot_shift=Ellipsis, volatility_shift=Ellipsis, rate_shift=Ellipsis, time_shift_days=Ellipsis)
```

Returns the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

### `scheme`

Return the configured time-marching choice string.

### `time_step_count`

Return the configured time-step budget before event insertion.

## `FiniteDifferenceBinaryBarrierEngine`

```python
FiniteDifferenceBinaryBarrierEngine(*, asset_step_count=Ellipsis, time_step_count=Ellipsis, scheme=Ellipsis, asset_upper_boundary=None)
```

Finite-difference pricing with immutable grid settings.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial steps, at least 3; defaults to 800.
- **`time_step_count`** (`int, optional`) — Positive time-step budget; event dates and curve knots are added. Read `FiniteDifferenceBinaryBarrierEngine().time_step_count` for the engine's default.
- **`scheme`** (`FiniteDifferenceScheme, optional`) — Time-marching scheme; defaults to "rannacher" (damped Crank-Nicolson). "crank_nicolson" uses standard Crank-Nicolson without time-step damping.
- **`asset_upper_boundary`** (`float or None, optional`) — Finite positive upper spot boundary, or None (default) for the automatic domain. Must exceed spot, strike and barriers at pricing.
#### Raises

- `InvalidInputError` — If asset_step_count is below 3, time_step_count is below 1, or an explicit upper boundary is nonpositive or non-finite. Boundary coverage and explicit-Euler stability are checked during pricing.
#### Notes

The engine name selects its product family. The vanilla engine accepts
EuropeanOption and AmericanOption. The digital engine accepts
CashOrNothingOption and AssetOrNothingOption. The binary-barrier engine
also accepts TouchOption. The autocallable engine accepts all snowball
variants and PhoenixOption. Other engines accept their named product.
Digital pricing requires explicitly flat rates; other families accept
deterministic rate curves. All FD product families support local-volatility
price, delta and gamma, including American exercise. Other Greeks (including
"all") and inverse solves raise UnsupportedOperationError. Sigma uses
fixed absolute surface coordinates; Greeks are absent at expiry or where
their stencils cross product events. Surface coverage follows remaining
stochastic evolution; rate coverage follows required future discounting.
Automatic local-volatility domains require convergence checks.

### `asset_step_count`

Return the configured spatial grid budget.

### `asset_upper_boundary`

Return the explicit upper spot boundary, or None for automatic selection.

### `price`

```python
price(self, /, instrument, context)
```

Return the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks, *, spot_shift=Ellipsis, volatility_shift=Ellipsis, rate_shift=Ellipsis, time_shift_days=Ellipsis)
```

Returns the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

### `scheme`

Return the configured time-marching choice string.

### `time_step_count`

Return the configured time-step budget before event insertion.

## `FiniteDifferenceDigitalEngine`

```python
FiniteDifferenceDigitalEngine(*, asset_step_count=Ellipsis, time_step_count=Ellipsis, scheme=Ellipsis, asset_upper_boundary=None)
```

Finite-difference pricing with immutable grid settings.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial steps, at least 3; defaults to 800.
- **`time_step_count`** (`int, optional`) — Positive time-step budget; event dates and curve knots are added. Read `FiniteDifferenceDigitalEngine().time_step_count` for the engine's default.
- **`scheme`** (`FiniteDifferenceScheme, optional`) — Time-marching scheme; defaults to "rannacher" (damped Crank-Nicolson). "crank_nicolson" uses standard Crank-Nicolson without time-step damping.
- **`asset_upper_boundary`** (`float or None, optional`) — Finite positive upper spot boundary, or None (default) for the automatic domain. Must exceed spot, strike and barriers at pricing.
#### Raises

- `InvalidInputError` — If asset_step_count is below 3, time_step_count is below 1, or an explicit upper boundary is nonpositive or non-finite. Boundary coverage and explicit-Euler stability are checked during pricing.
#### Notes

The engine name selects its product family. The vanilla engine accepts
EuropeanOption and AmericanOption. The digital engine accepts
CashOrNothingOption and AssetOrNothingOption. The binary-barrier engine
also accepts TouchOption. The autocallable engine accepts all snowball
variants and PhoenixOption. Other engines accept their named product.
Digital pricing requires explicitly flat rates; other families accept
deterministic rate curves. All FD product families support local-volatility
price, delta and gamma, including American exercise. Other Greeks (including
"all") and inverse solves raise UnsupportedOperationError. Sigma uses
fixed absolute surface coordinates; Greeks are absent at expiry or where
their stencils cross product events. Surface coverage follows remaining
stochastic evolution; rate coverage follows required future discounting.
Automatic local-volatility domains require convergence checks.

### `asset_step_count`

Return the configured spatial grid budget.

### `asset_upper_boundary`

Return the explicit upper spot boundary, or None for automatic selection.

### `price`

```python
price(self, /, instrument, context)
```

Return the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks, *, spot_shift=Ellipsis, volatility_shift=Ellipsis, rate_shift=Ellipsis, time_shift_days=Ellipsis)
```

Returns the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

### `scheme`

Return the configured time-marching choice string.

### `time_step_count`

Return the configured time-step budget before event insertion.

## `FiniteDifferenceDoubleBarrierEngine`

```python
FiniteDifferenceDoubleBarrierEngine(*, asset_step_count=Ellipsis, time_step_count=Ellipsis, scheme=Ellipsis, asset_upper_boundary=None)
```

Finite-difference pricing with immutable grid settings.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial steps, at least 3; defaults to 800.
- **`time_step_count`** (`int, optional`) — Positive time-step budget; event dates and curve knots are added. Read `FiniteDifferenceDoubleBarrierEngine().time_step_count` for the engine's default.
- **`scheme`** (`FiniteDifferenceScheme, optional`) — Time-marching scheme; defaults to "rannacher" (damped Crank-Nicolson). "crank_nicolson" uses standard Crank-Nicolson without time-step damping.
- **`asset_upper_boundary`** (`float or None, optional`) — Finite positive upper spot boundary, or None (default) for the automatic domain. Must exceed spot, strike and barriers at pricing.
#### Raises

- `InvalidInputError` — If asset_step_count is below 3, time_step_count is below 1, or an explicit upper boundary is nonpositive or non-finite. Boundary coverage and explicit-Euler stability are checked during pricing.
#### Notes

The engine name selects its product family. The vanilla engine accepts
EuropeanOption and AmericanOption. The digital engine accepts
CashOrNothingOption and AssetOrNothingOption. The binary-barrier engine
also accepts TouchOption. The autocallable engine accepts all snowball
variants and PhoenixOption. Other engines accept their named product.
Digital pricing requires explicitly flat rates; other families accept
deterministic rate curves. All FD product families support local-volatility
price, delta and gamma, including American exercise. Other Greeks (including
"all") and inverse solves raise UnsupportedOperationError. Sigma uses
fixed absolute surface coordinates; Greeks are absent at expiry or where
their stencils cross product events. Surface coverage follows remaining
stochastic evolution; rate coverage follows required future discounting.
Automatic local-volatility domains require convergence checks.

### `asset_step_count`

Return the configured spatial grid budget.

### `asset_upper_boundary`

Return the explicit upper spot boundary, or None for automatic selection.

### `price`

```python
price(self, /, instrument, context)
```

Return the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks, *, spot_shift=Ellipsis, volatility_shift=Ellipsis, rate_shift=Ellipsis, time_shift_days=Ellipsis)
```

Returns the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

### `scheme`

Return the configured time-marching choice string.

### `time_step_count`

Return the configured time-step budget before event insertion.

## `FiniteDifferenceDoubleTouchEngine`

```python
FiniteDifferenceDoubleTouchEngine(*, asset_step_count=Ellipsis, time_step_count=Ellipsis, scheme=Ellipsis, asset_upper_boundary=None)
```

Finite-difference pricing with immutable grid settings.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial steps, at least 3; defaults to 800.
- **`time_step_count`** (`int, optional`) — Positive time-step budget; event dates and curve knots are added. Read `FiniteDifferenceDoubleTouchEngine().time_step_count` for the engine's default.
- **`scheme`** (`FiniteDifferenceScheme, optional`) — Time-marching scheme; defaults to "rannacher" (damped Crank-Nicolson). "crank_nicolson" uses standard Crank-Nicolson without time-step damping.
- **`asset_upper_boundary`** (`float or None, optional`) — Finite positive upper spot boundary, or None (default) for the automatic domain. Must exceed spot, strike and barriers at pricing.
#### Raises

- `InvalidInputError` — If asset_step_count is below 3, time_step_count is below 1, or an explicit upper boundary is nonpositive or non-finite. Boundary coverage and explicit-Euler stability are checked during pricing.
#### Notes

The engine name selects its product family. The vanilla engine accepts
EuropeanOption and AmericanOption. The digital engine accepts
CashOrNothingOption and AssetOrNothingOption. The binary-barrier engine
also accepts TouchOption. The autocallable engine accepts all snowball
variants and PhoenixOption. Other engines accept their named product.
Digital pricing requires explicitly flat rates; other families accept
deterministic rate curves. All FD product families support local-volatility
price, delta and gamma, including American exercise. Other Greeks (including
"all") and inverse solves raise UnsupportedOperationError. Sigma uses
fixed absolute surface coordinates; Greeks are absent at expiry or where
their stencils cross product events. Surface coverage follows remaining
stochastic evolution; rate coverage follows required future discounting.
Automatic local-volatility domains require convergence checks.

### `asset_step_count`

Return the configured spatial grid budget.

### `asset_upper_boundary`

Return the explicit upper spot boundary, or None for automatic selection.

### `price`

```python
price(self, /, instrument, context)
```

Return the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks, *, spot_shift=Ellipsis, volatility_shift=Ellipsis, rate_shift=Ellipsis, time_shift_days=Ellipsis)
```

Returns the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

### `scheme`

Return the configured time-marching choice string.

### `time_step_count`

Return the configured time-step budget before event insertion.

## `FiniteDifferenceScheme`

```python
FiniteDifferenceScheme = typing.Literal['explicit_euler', 'implicit_euler', 'crank_nicolson', 'rannacher']
```

## `FiniteDifferenceVanillaEngine`

```python
FiniteDifferenceVanillaEngine(*, asset_step_count=Ellipsis, time_step_count=Ellipsis, scheme=Ellipsis, asset_upper_boundary=None)
```

Finite-difference pricing with immutable grid settings.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial steps, at least 3; defaults to 800.
- **`time_step_count`** (`int, optional`) — Positive time-step budget; event dates and curve knots are added. Read `FiniteDifferenceVanillaEngine().time_step_count` for the engine's default.
- **`scheme`** (`FiniteDifferenceScheme, optional`) — Time-marching scheme; defaults to "rannacher" (damped Crank-Nicolson). "crank_nicolson" uses standard Crank-Nicolson without time-step damping.
- **`asset_upper_boundary`** (`float or None, optional`) — Finite positive upper spot boundary, or None (default) for the automatic domain. Must exceed spot, strike and barriers at pricing.
#### Raises

- `InvalidInputError` — If asset_step_count is below 3, time_step_count is below 1, or an explicit upper boundary is nonpositive or non-finite. Boundary coverage and explicit-Euler stability are checked during pricing.
#### Notes

The engine name selects its product family. The vanilla engine accepts
EuropeanOption and AmericanOption. The digital engine accepts
CashOrNothingOption and AssetOrNothingOption. The binary-barrier engine
also accepts TouchOption. The autocallable engine accepts all snowball
variants and PhoenixOption. Other engines accept their named product.
Digital pricing requires explicitly flat rates; other families accept
deterministic rate curves. All FD product families support local-volatility
price, delta and gamma, including American exercise. Other Greeks (including
"all") and inverse solves raise UnsupportedOperationError. Sigma uses
fixed absolute surface coordinates; Greeks are absent at expiry or where
their stencils cross product events. Surface coverage follows remaining
stochastic evolution; rate coverage follows required future discounting.
Automatic local-volatility domains require convergence checks.

### `asset_step_count`

Return the configured spatial grid budget.

### `asset_upper_boundary`

Return the explicit upper spot boundary, or None for automatic selection.

### `price`

```python
price(self, /, instrument, context)
```

Return the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks, *, spot_shift=Ellipsis, volatility_shift=Ellipsis, rate_shift=Ellipsis, time_shift_days=Ellipsis)
```

Returns the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

### `scheme`

Return the configured time-marching choice string.

### `time_step_count`

Return the configured time-step budget before event insertion.

## `MonteCarloAccumulatorEngine`

```python
MonteCarloAccumulatorEngine(*, path_count=Ellipsis, seed=None, thread_count=Ellipsis, sampling=Ellipsis, antithetic=Ellipsis)
```

Flat-rate CPU Monte Carlo pricing for accumulators.

#### Parameters

- **`path_count`** (`int, optional`) — Exact path count, 1 through 10,000,000; defaults to 100,000. Sobol sampling requires a power of two.
- **`seed`** (`int or None, optional`) — Unsigned 64-bit seed, or None (default) to use system entropy.
- **`thread_count`** (`int, optional`) — Nonnegative worker cap per call: zero (default) is automatic, one is serial.
- **`sampling`** (`MonteCarloSampling, optional`) — Sampling method; defaults to pseudo_random.
- **`antithetic`** (`bool, optional`) — Pair opposite normal draws; defaults to False. An odd path count leaves one unpaired path.
#### Raises

- `InvalidInputError` — If paths are outside 1 through 10,000,000, thread_count is negative, or Sobol paths are not a power of two.
#### See Also

Accumulator : Supported contract.

#### Notes

Fixed seeds reproduce results across thread counts in the same build.
Calls own their samples and share a library-owned Rayon pool. A worker cap
does not reserve workers. Greeks and solves pin a seed per
request; solver tolerances do not measure sampling error.
Simulation uses the future trading dates. A current knock-out settles
before any purchase.

### `antithetic`

Return whether opposite normal draws are paired.

### `path_count`

Return the exact number of sampled paths.

### `price`

```python
price(self, /, instrument, context)
```

Return the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.
- `OSError` — If system entropy or worker creation fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks, *, spot_shift=Ellipsis, volatility_shift=Ellipsis, rate_shift=Ellipsis, time_shift_days=Ellipsis)
```

Returns the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.
- `OSError` — If system entropy or worker creation fails.

### `price_with_statistics`

```python
price_with_statistics(self, /, instrument, context)
```

Return the price and estimated sampling uncertainty.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `MonteCarloEstimate` — Mean, optional standard error and asymptotic 95% confidence interval.
#### Raises

- `KiyosiError` — If domain validation or numerical pricing fails.
- `OSError` — If system entropy or worker creation fails.

### `sampling`

Return the sampling choice string: pseudo_random or sobol.

### `seed`

Return the unsigned 64-bit seed, or None for system entropy.

### `thread_count`

Return the per-call worker cap; zero selects automatic sizing.

## `MonteCarloAsianEngine`

```python
MonteCarloAsianEngine(*, path_count=Ellipsis, step_count=Ellipsis, seed=None, thread_count=Ellipsis, sampling=Ellipsis, antithetic=Ellipsis)
```

Flat-rate CPU Monte Carlo pricing for continuous average-price options.

#### Parameters

- **`path_count`** (`int, optional`) — Exact path count, 1 through 10,000,000; defaults to 100,000. Sobol sampling requires a power of two.
- **`step_count`** (`int, optional`) — Grid size, 2 through 10,000; defaults to 50. Validated even when unused; see Notes for product-specific use.
- **`seed`** (`int or None, optional`) — Unsigned 64-bit seed, or None (default) to use system entropy.
- **`thread_count`** (`int, optional`) — Nonnegative worker cap per call: zero (default) is automatic, one is serial.
- **`sampling`** (`MonteCarloSampling, optional`) — Sampling method; defaults to pseudo_random.
- **`antithetic`** (`bool, optional`) — Pair opposite normal draws; defaults to False. An odd path count leaves one unpaired path.
#### Raises

- `InvalidInputError` — If paths are outside 1 through 10,000,000, steps outside 2 through 10,000, thread_count is negative, or Sobol paths are not a power of two.
#### See Also

GeometricAveragePriceOption : Supported contract.
ArithmeticAveragePriceOption : Supported contract.

#### Notes

Fixed seeds reproduce results across thread counts in the same build.
Calls own their samples and share a library-owned Rayon pool. A worker cap
does not reserve workers. Greeks and solves pin a seed per
request; solver tolerances do not measure sampling error.
Geometric averages and single fixings sample exact distributions.
Arithmetic averages use step_count trapezoidal intervals with the first
interval integrated conditionally.

### `antithetic`

Return whether opposite normal draws are paired.

### `path_count`

Return the exact number of sampled paths.

### `price`

```python
price(self, /, instrument, context)
```

Return the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.
#### Notes

System entropy and worker-creation failures raise OSError.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, pricing or requested derivatives fail.
#### Notes

System entropy and worker-creation failures raise OSError.

### `sampling`

Return the sampling choice string: pseudo_random or sobol.

### `seed`

Return the unsigned 64-bit seed, or None for system entropy.

### `step_count`

Return the configured grid size.

### `thread_count`

Return the per-call worker cap; zero selects automatic sizing.

## `MonteCarloAutocallableEngine`

```python
MonteCarloAutocallableEngine(*, path_count=Ellipsis, seed=None, thread_count=Ellipsis, sampling=Ellipsis, antithetic=Ellipsis)
```

Flat-rate CPU Monte Carlo pricing for snowball and Phoenix notes.

#### Parameters

- **`path_count`** (`int, optional`) — Exact path count, 1 through 10,000,000; defaults to 100,000. Sobol sampling requires a power of two.
- **`seed`** (`int or None, optional`) — Unsigned 64-bit seed, or None (default) to use system entropy.
- **`thread_count`** (`int, optional`) — Nonnegative worker cap per call: zero (default) is automatic, one is serial.
- **`sampling`** (`MonteCarloSampling, optional`) — Sampling method; defaults to pseudo_random.
- **`antithetic`** (`bool, optional`) — Pair opposite normal draws; defaults to False. An odd path count leaves one unpaired path.
#### Raises

- `InvalidInputError` — If paths are outside 1 through 10,000,000, thread_count is negative, or Sobol paths are not a power of two.
#### See Also

SnowballOption : Supported contract.
BinarySnowballOption : Supported contract.
TernarySnowballOption : Supported contract.
PhoenixOption : Supported contract.

#### Notes

Fixed seeds reproduce results across thread counts in the same build.
Calls own their samples and share a library-owned Rayon pool. A worker cap
does not reserve workers. Greeks and solves pin a seed per
request; solver tolerances do not measure sampling error.
Simulation uses trading days when knock-in matters, or observation
dates and expiry otherwise.

### `antithetic`

Return whether opposite normal draws are paired.

### `path_count`

Return the exact number of sampled paths.

### `price`

```python
price(self, /, instrument, context)
```

Return the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.
- `OSError` — If system entropy or worker creation fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks, *, spot_shift=Ellipsis, volatility_shift=Ellipsis, rate_shift=Ellipsis, time_shift_days=Ellipsis)
```

Returns the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.
- `OSError` — If system entropy or worker creation fails.

### `price_with_statistics`

```python
price_with_statistics(self, /, instrument, context)
```

Return the price and estimated sampling uncertainty.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `MonteCarloEstimate` — Mean, optional standard error and asymptotic 95% confidence interval.
#### Raises

- `KiyosiError` — If domain validation or numerical pricing fails.
- `OSError` — If system entropy or worker creation fails.

### `sampling`

Return the sampling choice string: pseudo_random or sobol.

### `seed`

Return the unsigned 64-bit seed, or None for system entropy.

### `thread_count`

Return the per-call worker cap; zero selects automatic sizing.

## `MonteCarloBarrierEngine`

```python
MonteCarloBarrierEngine(*, path_count=Ellipsis, seed=None, thread_count=Ellipsis, sampling=Ellipsis, antithetic=Ellipsis)
```

Flat-rate CPU Monte Carlo pricing for single-barrier vanilla options.

#### Parameters

- **`path_count`** (`int, optional`) — Exact path count, 1 through 10,000,000; defaults to 100,000. Sobol sampling requires a power of two.
- **`seed`** (`int or None, optional`) — Unsigned 64-bit seed, or None (default) to use system entropy.
- **`thread_count`** (`int, optional`) — Nonnegative worker cap per call: zero (default) is automatic, one is serial.
- **`sampling`** (`MonteCarloSampling, optional`) — Sampling method; defaults to pseudo_random.
- **`antithetic`** (`bool, optional`) — Pair opposite normal draws; defaults to False. An odd path count leaves one unpaired path.
#### Raises

- `InvalidInputError` — If paths are outside 1 through 10,000,000, thread_count is negative, or Sobol paths are not a power of two.
#### See Also

BarrierOption : Supported contract.

#### Notes

Fixed seeds reproduce results across thread counts in the same build.
Calls own their samples and share a library-owned Rayon pool. A worker cap
does not reserve workers. Greeks and solves pin a seed per
request; solver tolerances do not measure sampling error.
Monitoring uses continuous survival or the original fixing dates.
Only delta and gamma are returned.

### `antithetic`

Return whether opposite normal draws are paired.

### `path_count`

Return the exact number of sampled paths.

### `price`

```python
price(self, /, instrument, context)
```

Return the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.
- `OSError` — If system entropy or worker creation fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks, *, spot_shift=Ellipsis)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.
- `OSError` — If system entropy or worker creation fails.

### `sampling`

Return the sampling choice string: pseudo_random or sobol.

### `seed`

Return the unsigned 64-bit seed, or None for system entropy.

### `thread_count`

Return the per-call worker cap; zero selects automatic sizing.

## `MonteCarloDigitalEngine`

```python
MonteCarloDigitalEngine(*, path_count=Ellipsis, seed=None, thread_count=Ellipsis, sampling=Ellipsis, antithetic=Ellipsis)
```

Flat-rate CPU Monte Carlo pricing for European digitals.

#### Parameters

- **`path_count`** (`int, optional`) — Exact path count, 1 through 10,000,000; defaults to 100,000. Sobol sampling requires a power of two.
- **`seed`** (`int or None, optional`) — Unsigned 64-bit seed, or None (default) to use system entropy.
- **`thread_count`** (`int, optional`) — Nonnegative worker cap per call: zero (default) is automatic, one is serial.
- **`sampling`** (`MonteCarloSampling, optional`) — Sampling method; defaults to pseudo_random.
- **`antithetic`** (`bool, optional`) — Pair opposite normal draws; defaults to False. An odd path count leaves one unpaired path.
#### Raises

- `InvalidInputError` — If paths are outside 1 through 10,000,000, thread_count is negative, or Sobol paths are not a power of two.
#### See Also

CashOrNothingOption : Supported contract.
AssetOrNothingOption : Supported contract.

#### Notes

Fixed seeds reproduce results across thread counts in the same build.
Calls own their samples and share a library-owned Rayon pool. A worker cap
does not reserve workers. Greeks and solves pin a seed per
request; solver tolerances do not measure sampling error.
Only native delta and gamma are returned; other requested Greeks remain absent.

### `antithetic`

Return whether opposite normal draws are paired.

### `path_count`

Return the exact number of sampled paths.

### `price`

```python
price(self, /, instrument, context)
```

Return the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.
#### Notes

System entropy and worker-creation failures raise OSError.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, pricing or requested derivatives fail.
#### Notes

System entropy and worker-creation failures raise OSError.

### `sampling`

Return the sampling choice string: pseudo_random or sobol.

### `seed`

Return the unsigned 64-bit seed, or None for system entropy.

### `thread_count`

Return the per-call worker cap; zero selects automatic sizing.

## `MonteCarloDoubleBarrierEngine`

```python
MonteCarloDoubleBarrierEngine(*, path_count=Ellipsis, seed=None, thread_count=Ellipsis, sampling=Ellipsis, antithetic=Ellipsis)
```

Flat-rate CPU Monte Carlo pricing for double-barrier vanilla options.

#### Parameters

- **`path_count`** (`int, optional`) — Exact path count, 1 through 10,000,000; defaults to 100,000. Sobol sampling requires a power of two.
- **`seed`** (`int or None, optional`) — Unsigned 64-bit seed, or None (default) to use system entropy.
- **`thread_count`** (`int, optional`) — Nonnegative worker cap per call: zero (default) is automatic, one is serial.
- **`sampling`** (`MonteCarloSampling, optional`) — Sampling method; defaults to pseudo_random.
- **`antithetic`** (`bool, optional`) — Pair opposite normal draws; defaults to False. An odd path count leaves one unpaired path.
#### Raises

- `InvalidInputError` — If paths are outside 1 through 10,000,000, thread_count is negative, or Sobol paths are not a power of two.
#### See Also

DoubleBarrierOption : Supported contract.

#### Notes

Fixed seeds reproduce results across thread counts in the same build.
Calls own their samples and share a library-owned Rayon pool. A worker cap
does not reserve workers. Greeks and solves pin a seed per
request; solver tolerances do not measure sampling error.
Monitoring uses continuous survival or the original fixing dates.
Only delta and gamma are returned.

### `antithetic`

Return whether opposite normal draws are paired.

### `path_count`

Return the exact number of sampled paths.

### `price`

```python
price(self, /, instrument, context)
```

Return the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.
- `OSError` — If system entropy or worker creation fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks, *, spot_shift=Ellipsis)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.
- `OSError` — If system entropy or worker creation fails.

### `sampling`

Return the sampling choice string: pseudo_random or sobol.

### `seed`

Return the unsigned 64-bit seed, or None for system entropy.

### `thread_count`

Return the per-call worker cap; zero selects automatic sizing.

## `MonteCarloEstimate`

Monte Carlo price with optional sampling uncertainty.

#### Notes

Standard error uses independent pseudorandom observations or even
antithetic pair means. The interval is an asymptotic 95% normal interval.
Uncertainty is absent for Sobol, insufficient independent samples and odd
antithetic counts; known pseudorandom settlements have zero uncertainty.

### `confidence_interval`

Return the asymptotic 95% interval, or None when unavailable.

### `price`

Return the finite price in contract payment units.

### `standard_error`

Return sampling standard error, or None when unavailable.

## `MonteCarloSampling`

```python
MonteCarloSampling = typing.Literal['pseudo_random', 'sobol']
```

## `MonteCarloVanillaEngine`

```python
MonteCarloVanillaEngine(*, path_count=Ellipsis, step_count=Ellipsis, seed=None, thread_count=Ellipsis, sampling=Ellipsis, antithetic=Ellipsis)
```

Flat-rate CPU Monte Carlo pricing for European and American vanilla
options.

#### Parameters

- **`path_count`** (`int, optional`) — Exact path count, 1 through 10,000,000; defaults to 100,000. Sobol sampling requires a power of two.
- **`step_count`** (`int, optional`) — Grid size, 2 through 10,000; defaults to 50. Validated even when unused; see Notes for product-specific use.
- **`seed`** (`int or None, optional`) — Unsigned 64-bit seed, or None (default) to use system entropy.
- **`thread_count`** (`int, optional`) — Nonnegative worker cap per call: zero (default) is automatic, one is serial.
- **`sampling`** (`MonteCarloSampling, optional`) — Sampling method; defaults to pseudo_random.
- **`antithetic`** (`bool, optional`) — Pair opposite normal draws; defaults to False. An odd path count leaves one unpaired path.
#### Raises

- `InvalidInputError` — If paths are outside 1 through 10,000,000, steps outside 2 through 10,000, thread_count is negative, or Sobol paths are not a power of two.
#### See Also

EuropeanOption : Supported contract.
AmericanOption : Supported contract.

#### Notes

Fixed seeds reproduce results across thread counts in the same build.
Calls own their samples and share a library-owned Rayon pool. A worker cap
does not reserve workers. Greeks and solves pin a seed per
request; solver tolerances do not measure sampling error.
European pricing samples the exact terminal distribution and ignores
step_count. Near-strike payoffs preserve small movements even when the
terminal spot rounds to the strike. American exercise grids use step_count
points and require at least three before expiry.

### `antithetic`

Return whether opposite normal draws are paired.

### `path_count`

Return the exact number of sampled paths.

### `price`

```python
price(self, /, instrument, context)
```

Return the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.
#### Notes

System entropy and worker-creation failures raise OSError.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks, *, spot_shift=None, volatility_shift=Ellipsis, rate_shift=Ellipsis, time_shift_days=Ellipsis)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
- **`spot_shift`** (`float or None, optional`) — Positive finite absolute spot bump. European default: 0.01 spot units. American default: 8% of spot. None selects the product's default.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.
#### Notes

System entropy and worker-creation failures raise OSError.
Omitted or None `spot_shift` uses the product's default; other bumps
use the shared core defaults.

### `price_with_statistics`

```python
price_with_statistics(self, /, instrument, context)
```

Return the price and estimated sampling uncertainty.

#### Parameters

- **`instrument`** (`EuropeanOption`) — European vanilla contract; American statistics are not exposed.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `MonteCarloEstimate` — Mean, optional standard error and asymptotic 95% confidence interval.
#### Raises

- `KiyosiError` — If domain validation or numerical pricing fails.
- `OSError` — If system entropy or worker creation fails.

### `sampling`

Return the sampling choice string: pseudo_random or sobol.

### `seed`

Return the unsigned 64-bit seed, or None for system entropy.

### `step_count`

Return the configured grid size.

### `thread_count`

Return the per-call worker cap; zero selects automatic sizing.

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

## `QuadratureAccumulatorEngine`

```python
QuadratureAccumulatorEngine(*, asset_step_count=Ellipsis, integration_standard_deviations=Ellipsis)
```

Flat-rate quadrature pricing with immutable integration settings.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Spatial grid budget, at least 4; defaults to 512.
- **`integration_standard_deviations`** (`float, optional`) — Positive finite integration extent in standard deviations; defaults to 8.
#### Raises

- `InvalidInputError` — If asset_step_count is below 4 or integration_standard_deviations is nonpositive or non-finite.
#### See Also

Accumulator : Supported contract.

### `asset_step_count`

Returns the configured spatial grid budget.

### `integration_standard_deviations`

Returns the integration extent in standard deviations.

### `price`

```python
price(self, /, instrument, context)
```

Returns the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks, *, spot_shift=Ellipsis, volatility_shift=Ellipsis, rate_shift=Ellipsis, time_shift_days=Ellipsis)
```

Returns the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

## `QuadratureAutocallableEngine`

```python
QuadratureAutocallableEngine(*, asset_step_count=Ellipsis, integration_standard_deviations=Ellipsis)
```

Flat-rate quadrature pricing with immutable integration settings.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Spatial grid budget, at least 4; defaults to 512.
- **`integration_standard_deviations`** (`float, optional`) — Positive finite integration extent in standard deviations; defaults to 8.
#### Raises

- `InvalidInputError` — If asset_step_count is below 4 or integration_standard_deviations is nonpositive or non-finite.
#### See Also

SnowballOption : Supported contract.
BinarySnowballOption : Supported contract.
TernarySnowballOption : Supported contract.
PhoenixOption : Supported contract.

#### Notes

Preserves cash and asset payments below the spatial grid, including
zero-lower-strike losses after large spot declines.

### `asset_step_count`

Returns the configured spatial grid budget.

### `integration_standard_deviations`

Returns the integration extent in standard deviations.

### `price`

```python
price(self, /, instrument, context)
```

Returns the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks, *, spot_shift=Ellipsis, volatility_shift=Ellipsis, rate_shift=Ellipsis, time_shift_days=Ellipsis)
```

Returns the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

## `QuadratureBarrierEngine`

```python
QuadratureBarrierEngine(*, asset_step_count=Ellipsis, integration_standard_deviations=Ellipsis)
```

Flat-rate quadrature pricing with immutable integration settings.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Spatial grid budget, at least 4; defaults to 512.
- **`integration_standard_deviations`** (`float, optional`) — Positive finite integration extent in standard deviations; defaults to 8.
#### Raises

- `InvalidInputError` — If asset_step_count is below 4 or integration_standard_deviations is nonpositive or non-finite.
#### See Also

BarrierOption : Supported contract.

### `asset_step_count`

Returns the configured spatial grid budget.

### `integration_standard_deviations`

Returns the integration extent in standard deviations.

### `price`

```python
price(self, /, instrument, context)
```

Returns the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks, *, spot_shift=Ellipsis, volatility_shift=Ellipsis, rate_shift=Ellipsis, time_shift_days=Ellipsis)
```

Returns the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

## `TurnbullWakemanArithmeticAveragePriceEngine`

```python
TurnbullWakemanArithmeticAveragePriceEngine()
```

Approximates arithmetic continuous-average prices with flat rates before expiry.

Uses Levy-compatible moments.

#### See Also

ArithmeticAveragePriceOption : Supported contract.

### `price`

```python
price(self, /, instrument, context)
```

Returns the price without changing the instrument or context.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
#### Returns

- `float` — Present value of remaining contractual payments.
#### Raises

- `KiyosiError` — If domain validation, engine applicability or numerical pricing fails.

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks, *, spot_shift=Ellipsis, volatility_shift=Ellipsis, rate_shift=Ellipsis, time_shift_days=Ellipsis)
```

Returns the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str`) — Greek names or "all" to request every measure; duplicates are ignored.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

## `implied_coupon`

```python
implied_coupon(engine, instrument, context, observed_price, *, quote_convention=Ellipsis, lower_bound=Ellipsis, upper_bound=Ellipsis, price_tolerance=Ellipsis, parameter_tolerance=Ellipsis, max_iterations=Ellipsis)
```

Solve the coupon that reproduces an observed price in the contract's units.

#### Parameters

- **`engine`** (`object`) — QuadratureAutocallableEngine, FiniteDifferenceAutocallableEngine or MonteCarloAutocallableEngine.
- **`instrument`** (`object`) — SnowballOption, BinarySnowballOption, TernarySnowballOption or PhoenixOption; the original is unchanged.
- **`context`** (`PricingContext`) — Market snapshot; the original is unchanged.
- **`observed_price`** (`float`) — Finite target price in the engine's payment units.
- **`quote_convention`** (`CouponQuoteConvention`) — Required for snowballs: shift_maturity_coupon shifts the maturity coupon with observation coupons; preserve_maturity_coupon keeps it fixed. Omit this keyword for Phoenix, or pass Ellipsis (the displayed default).
- **`lower_bound`** (`float, optional`) — Finite lower coupon in the contract's units; defaults to 0. Signed bounds are accepted when the resulting contract terms are valid.
- **`upper_bound`** (`float, optional`) — Finite upper coupon in the same units, above lower_bound; defaults to 2.
- **`price_tolerance`** (`float, optional`) — Positive finite absolute price residual tolerance; defaults to 1e-8.
- **`parameter_tolerance`** (`float, optional`) — Positive finite bracket-width tolerance in the contract's coupon units; defaults to 1e-8. Either tolerance can stop iteration.
- **`max_iterations`** (`int, optional`) — Positive iteration budget; defaults to 100. Endpoint and affine-interpolation evaluations do not use this budget.
#### Returns

- `float` — Annual coupon rate, or fixed per-period proportion for FCN/DCN and other per-period Phoenix contracts.
#### Raises

- `InvalidInputError` — If the quote, settings or repriced terms are invalid.
- `UnsupportedOperationError` — If the combination is unsupported or the parameter is not identifiable.
- `RootNotBracketedError` — If the supplied endpoints do not bracket the target.
- `NonConvergenceError` — If the iteration budget is exhausted.
- `ComputationFailureError` — If a price, residual or numerical evaluation is non-finite.
#### Notes

Pricing failures propagate. Monte Carlo solves pin one seed per request;
tolerances constrain the sampled price curve, not its sampling error.
Snowballs shift all observation coupons relative to the first one,
including past observations. The maturity convention controls the final
coupon; the ternary minimum remains fixed. Phoenix replaces its
conditional coupon without changing its units. Bounds, parameter tolerance
and result use the same units. Trials use affine interpolation, then bisection.

## `implied_volatility`

```python
implied_volatility(engine, instrument, context, observed_price, *, lower_bound=Ellipsis, upper_bound=Ellipsis, price_tolerance=Ellipsis, parameter_tolerance=Ellipsis, max_iterations=Ellipsis)
```

Solve the annual volatility that reproduces an observed price.

#### Parameters

- **`engine`** (`object`) — Supported pricing engine for the instrument.
- **`instrument`** (`object`) — Contract to reprice; the original is unchanged.
- **`context`** (`PricingContext`) — Market snapshot; the original is unchanged.
- **`observed_price`** (`float`) — Finite target price in the engine's payment units.
- **`lower_bound`** (`float, optional`) — Positive finite lower annual volatility in decimal units; defaults to 0.0001.
- **`upper_bound`** (`float, optional`) — Finite upper annual volatility, above lower_bound; defaults to 4.
- **`price_tolerance`** (`float, optional`) — Positive finite absolute price residual tolerance; defaults to 1e-8.
- **`parameter_tolerance`** (`float, optional`) — Positive finite bracket-width tolerance in decimal units; defaults to 1e-8. Either tolerance can stop iteration.
- **`max_iterations`** (`int, optional`) — Positive iteration budget; defaults to 100.
#### Returns

- `float` — Annual parameter in decimal units.
#### Raises

- `InvalidInputError` — If the quote, settings or repriced terms are invalid.
- `UnsupportedOperationError` — If the combination is unsupported or the parameter is not identifiable.
- `RootNotBracketedError` — If the supplied endpoints do not bracket the target.
- `NonConvergenceError` — If the iteration budget is exhausted.
- `ComputationFailureError` — If a price, residual or numerical evaluation is non-finite.
#### Notes

Pricing failures propagate. Monte Carlo solves pin one seed per request;
tolerances constrain the sampled price curve, not its sampling error.
Digital prices can have several volatility roots. The supplied bracket
selects a root; CRR engines restrict it to their admissible tree domain.
