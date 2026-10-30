---
description: kiyosi.pricing 的 Python API 参考文档。
outline: [2, 4]
---

# `kiyosi.pricing`

Price contracts, compute sensitivities, and solve implied parameters.

``FiniteDifferenceScheme`` selects ``"explicit_euler"``, ``"implicit_euler"``
or ``"crank_nicolson"`` (with initial damping). ``MonteCarloSampling`` selects
``"pseudo_random"`` or scrambled ``"sobol"``; a fixed seed reproduces draws
across thread counts in the same build. Sobol estimates omit sampling error.

``CouponQuoteConvention`` controls whether a snowball's maturity coupon
shifts with observation coupons (``"shift_maturity_coupon"``) or stays fixed
(``"preserve_maturity_coupon"``). Phoenix coupon solves omit this choice.

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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
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

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

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

## `AnalyticGeometricAveragePriceEngine`

```python
AnalyticGeometricAveragePriceEngine()
```

Analytic continuous average-price pricing.

#### Notes

AnalyticGeometricAveragePriceEngine accepts geometric averages and
deterministic curves. TurnbullWakemanArithmeticAveragePriceEngine uses
a Levy-compatible moment approximation and requires flat rates before
expiry. It accepts arithmetic averages.

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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
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
CoxRossRubinsteinBarrierEngine(**fields)
```

Flat-rate Cox-Ross-Rubinstein tree pricing.

#### Parameters

- **`step_count`** (`int, optional`) — Number of tree time steps, from 1 through 1,000,000; defaults to 256.
#### Raises

- `InvalidInputError` — If step_count is outside 1 through 1,000,000.
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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
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

## `CoxRossRubinsteinDigitalEngine`

```python
CoxRossRubinsteinDigitalEngine(**fields)
```

Flat-rate Cox-Ross-Rubinstein tree pricing.

#### Parameters

- **`step_count`** (`int, optional`) — Number of tree time steps, from 1 through 1,000,000; defaults to 256.
#### Raises

- `InvalidInputError` — If step_count is outside 1 through 1,000,000.
#### Notes

The vanilla engine accepts EuropeanOption and AmericanOption; the
digital engine accepts CashOrNothingOption and AssetOrNothingOption.

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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
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

## `CoxRossRubinsteinVanillaEngine`

```python
CoxRossRubinsteinVanillaEngine(**fields)
```

Flat-rate Cox-Ross-Rubinstein tree pricing.

#### Parameters

- **`step_count`** (`int, optional`) — Number of tree time steps, from 1 through 1,000,000; defaults to 256.
#### Raises

- `InvalidInputError` — If step_count is outside 1 through 1,000,000.
#### Notes

The vanilla engine accepts EuropeanOption and AmericanOption; the
digital engine accepts CashOrNothingOption and AssetOrNothingOption.

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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
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
FiniteDifferenceAccumulatorEngine(**fields)
```

Finite-difference pricing with immutable grid settings.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial steps, at least 3; defaults to 800.
- **`time_step_count`** (`int, optional`) — Positive time-step budget, default 200; event dates and curve knots are added.
- **`scheme`** (`FiniteDifferenceScheme, optional`) — Time-marching scheme; defaults to damped Crank-Nicolson.
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
deterministic rate curves.

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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

### `asset_upper_boundary`

Return the explicit upper spot boundary, or None for automatic selection.

### `time_step_count`

Return the configured time-step budget before event insertion.

### `scheme`

Return the configured time-marching choice string.

### `asset_step_count`

Return the configured spatial grid budget.

## `FiniteDifferenceAutocallableEngine`

```python
FiniteDifferenceAutocallableEngine(**fields)
```

Finite-difference pricing with immutable grid settings.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial steps, at least 3; defaults to 800.
- **`time_step_count`** (`int, optional`) — Positive time-step budget, default 200; event dates and curve knots are added.
- **`scheme`** (`FiniteDifferenceScheme, optional`) — Time-marching scheme; defaults to damped Crank-Nicolson.
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
deterministic rate curves.

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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
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

### `asset_step_count`

Return the configured spatial grid budget.

### `asset_upper_boundary`

Return the explicit upper spot boundary, or None for automatic selection.

## `FiniteDifferenceBarrierEngine`

```python
FiniteDifferenceBarrierEngine(**fields)
```

Finite-difference pricing with immutable grid settings.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial steps, at least 3; defaults to 800.
- **`time_step_count`** (`int, optional`) — Positive time-step budget, default 200; event dates and curve knots are added.
- **`scheme`** (`FiniteDifferenceScheme, optional`) — Time-marching scheme; defaults to damped Crank-Nicolson.
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
deterministic rate curves.

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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

### `time_step_count`

Return the configured time-step budget before event insertion.

### `asset_upper_boundary`

Return the explicit upper spot boundary, or None for automatic selection.

### `scheme`

Return the configured time-marching choice string.

### `asset_step_count`

Return the configured spatial grid budget.

## `FiniteDifferenceBinaryBarrierEngine`

```python
FiniteDifferenceBinaryBarrierEngine(**fields)
```

Finite-difference pricing with immutable grid settings.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial steps, at least 3; defaults to 800.
- **`time_step_count`** (`int, optional`) — Positive time-step budget, default 200; event dates and curve knots are added.
- **`scheme`** (`FiniteDifferenceScheme, optional`) — Time-marching scheme; defaults to damped Crank-Nicolson.
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
deterministic rate curves.

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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

### `asset_step_count`

Return the configured spatial grid budget.

### `asset_upper_boundary`

Return the explicit upper spot boundary, or None for automatic selection.

### `scheme`

Return the configured time-marching choice string.

### `time_step_count`

Return the configured time-step budget before event insertion.

## `FiniteDifferenceDigitalEngine`

```python
FiniteDifferenceDigitalEngine(**fields)
```

Finite-difference pricing with immutable grid settings.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial steps, at least 3; defaults to 800.
- **`time_step_count`** (`int, optional`) — Positive time-step budget, default 200; event dates and curve knots are added.
- **`scheme`** (`FiniteDifferenceScheme, optional`) — Time-marching scheme; defaults to damped Crank-Nicolson.
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
deterministic rate curves.

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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

### `asset_step_count`

Return the configured spatial grid budget.

### `time_step_count`

Return the configured time-step budget before event insertion.

### `asset_upper_boundary`

Return the explicit upper spot boundary, or None for automatic selection.

### `scheme`

Return the configured time-marching choice string.

## `FiniteDifferenceDoubleBarrierEngine`

```python
FiniteDifferenceDoubleBarrierEngine(**fields)
```

Finite-difference pricing with immutable grid settings.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial steps, at least 3; defaults to 800.
- **`time_step_count`** (`int, optional`) — Positive time-step budget, default 200; event dates and curve knots are added.
- **`scheme`** (`FiniteDifferenceScheme, optional`) — Time-marching scheme; defaults to damped Crank-Nicolson.
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
deterministic rate curves.

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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
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

### `asset_step_count`

Return the configured spatial grid budget.

### `asset_upper_boundary`

Return the explicit upper spot boundary, or None for automatic selection.

## `FiniteDifferenceDoubleTouchEngine`

```python
FiniteDifferenceDoubleTouchEngine(**fields)
```

Finite-difference pricing with immutable grid settings.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial steps, at least 3; defaults to 800.
- **`time_step_count`** (`int, optional`) — Positive time-step budget, default 200; event dates and curve knots are added.
- **`scheme`** (`FiniteDifferenceScheme, optional`) — Time-marching scheme; defaults to damped Crank-Nicolson.
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
deterministic rate curves.

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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

### `time_step_count`

Return the configured time-step budget before event insertion.

### `asset_step_count`

Return the configured spatial grid budget.

### `scheme`

Return the configured time-marching choice string.

### `asset_upper_boundary`

Return the explicit upper spot boundary, or None for automatic selection.

## `FiniteDifferenceScheme`

```python
FiniteDifferenceScheme = typing.Literal['explicit_euler', 'implicit_euler', 'crank_nicolson']
```

## `FiniteDifferenceVanillaEngine`

```python
FiniteDifferenceVanillaEngine(**fields)
```

Finite-difference pricing with immutable grid settings.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Number of spatial steps, at least 3; defaults to 800.
- **`time_step_count`** (`int, optional`) — Positive time-step budget, default 200; event dates and curve knots are added.
- **`scheme`** (`FiniteDifferenceScheme, optional`) — Time-marching scheme; defaults to damped Crank-Nicolson.
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
deterministic rate curves.

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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

### `asset_step_count`

Return the configured spatial grid budget.

### `scheme`

Return the configured time-marching choice string.

### `time_step_count`

Return the configured time-step budget before event insertion.

### `asset_upper_boundary`

Return the explicit upper spot boundary, or None for automatic selection.

## `MonteCarloAccumulatorEngine`

```python
MonteCarloAccumulatorEngine(**fields)
```

Flat-rate CPU Monte Carlo pricing for accumulators.

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

Accumulator : Supported contract.

#### Notes

Fixed seeds reproduce results across thread counts in the same build.
Each call owns its workers and samples. Greeks and solves pin a seed per
request; solver tolerances do not measure sampling error.
Simulation uses the future trading dates; step_count is validated but
unused. A current knock-out settles before any purchase.

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

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.
#### Notes

System entropy and worker-creation failures raise OSError.

### `antithetic`

Return whether opposite normal draws are paired.

### `path_count`

Return the exact number of sampled paths.

### `thread_count`

Return the per-call worker cap; zero selects automatic sizing.

### `sampling`

Return the sampling choice string: pseudo_random or sobol.

### `step_count`

Return the configured grid size.

### `seed`

Return the unsigned 64-bit seed, or None for system entropy.

## `MonteCarloAsianEngine`

```python
MonteCarloAsianEngine(**fields)
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
Each call owns its workers and samples. Greeks and solves pin a seed per
request; solver tolerances do not measure sampling error.
Geometric averages and single fixings sample exact distributions.
Arithmetic averages use step_count trapezoidal intervals with the first
interval integrated conditionally.

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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.
#### Notes

System entropy and worker-creation failures raise OSError.

### `path_count`

Return the exact number of sampled paths.

### `seed`

Return the unsigned 64-bit seed, or None for system entropy.

### `step_count`

Return the configured grid size.

### `thread_count`

Return the per-call worker cap; zero selects automatic sizing.

### `antithetic`

Return whether opposite normal draws are paired.

### `sampling`

Return the sampling choice string: pseudo_random or sobol.

## `MonteCarloAutocallableEngine`

```python
MonteCarloAutocallableEngine(**fields)
```

Flat-rate CPU Monte Carlo pricing for snowball and Phoenix notes.

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

SnowballOption : Supported contract.
BinarySnowballOption : Supported contract.
TernarySnowballOption : Supported contract.
PhoenixOption : Supported contract.

#### Notes

Fixed seeds reproduce results across thread counts in the same build.
Each call owns its workers and samples. Greeks and solves pin a seed per
request; solver tolerances do not measure sampling error.
Simulation uses trading days when knock-in matters, or observation
dates and expiry otherwise. step_count is validated but unused.

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

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.
#### Notes

System entropy and worker-creation failures raise OSError.

### `step_count`

Return the configured grid size.

### `seed`

Return the unsigned 64-bit seed, or None for system entropy.

### `antithetic`

Return whether opposite normal draws are paired.

### `sampling`

Return the sampling choice string: pseudo_random or sobol.

### `path_count`

Return the exact number of sampled paths.

### `thread_count`

Return the per-call worker cap; zero selects automatic sizing.

## `MonteCarloBarrierEngine`

```python
MonteCarloBarrierEngine(**fields)
```

Flat-rate CPU Monte Carlo pricing for single-barrier vanilla options.

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

BarrierOption : Supported contract.

#### Notes

Fixed seeds reproduce results across thread counts in the same build.
Each call owns its workers and samples. Greeks and solves pin a seed per
request; solver tolerances do not measure sampling error.
Monitoring uses continuous survival or the original fixing dates;
step_count is validated but unused. Only delta and gamma are returned.

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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.
#### Notes

System entropy and worker-creation failures raise OSError.

### `sampling`

Return the sampling choice string: pseudo_random or sobol.

### `path_count`

Return the exact number of sampled paths.

### `seed`

Return the unsigned 64-bit seed, or None for system entropy.

### `step_count`

Return the configured grid size.

### `thread_count`

Return the per-call worker cap; zero selects automatic sizing.

### `antithetic`

Return whether opposite normal draws are paired.

## `MonteCarloDigitalEngine`

```python
MonteCarloDigitalEngine(**fields)
```

Flat-rate CPU Monte Carlo pricing for European digitals.

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

CashOrNothingOption : Supported contract.
AssetOrNothingOption : Supported contract.

#### Notes

Fixed seeds reproduce results across thread counts in the same build.
Each call owns its workers and samples. Greeks and solves pin a seed per
request; solver tolerances do not measure sampling error.
Terminal sampling ignores step_count. Only native delta and gamma are
returned; other requested Greeks remain absent.

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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.
#### Notes

System entropy and worker-creation failures raise OSError.

### `path_count`

Return the exact number of sampled paths.

### `thread_count`

Return the per-call worker cap; zero selects automatic sizing.

### `seed`

Return the unsigned 64-bit seed, or None for system entropy.

### `antithetic`

Return whether opposite normal draws are paired.

### `sampling`

Return the sampling choice string: pseudo_random or sobol.

### `step_count`

Return the configured grid size.

## `MonteCarloDoubleBarrierEngine`

```python
MonteCarloDoubleBarrierEngine(**fields)
```

Flat-rate CPU Monte Carlo pricing for double-barrier vanilla options.

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

DoubleBarrierOption : Supported contract.

#### Notes

Fixed seeds reproduce results across thread counts in the same build.
Each call owns its workers and samples. Greeks and solves pin a seed per
request; solver tolerances do not measure sampling error.
Monitoring uses continuous survival or the original fixing dates;
step_count is validated but unused. Only delta and gamma are returned.

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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.
#### Notes

System entropy and worker-creation failures raise OSError.

### `sampling`

Return the sampling choice string: pseudo_random or sobol.

### `path_count`

Return the exact number of sampled paths.

### `seed`

Return the unsigned 64-bit seed, or None for system entropy.

### `step_count`

Return the configured grid size.

### `antithetic`

Return whether opposite normal draws are paired.

### `thread_count`

Return the per-call worker cap; zero selects automatic sizing.

## `MonteCarloEstimate`

```python
MonteCarloEstimate()
```

Monte Carlo price with optional sampling uncertainty.

#### Notes

Standard error uses independent pseudorandom observations or even
antithetic pair means. The interval is an asymptotic 95% normal interval.
Uncertainty is absent for Sobol, insufficient independent samples and odd
antithetic counts; known pseudorandom settlements have zero uncertainty.

### `price`

Return the finite price in contract payment units.

### `standard_error`

Return sampling standard error, or None when unavailable.

### `confidence_interval`

Return the asymptotic 95% interval, or None when unavailable.

## `MonteCarloSampling`

```python
MonteCarloSampling = typing.Literal['pseudo_random', 'sobol']
```

## `MonteCarloVanillaEngine`

```python
MonteCarloVanillaEngine(**fields)
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
Each call owns its workers and samples. Greeks and solves pin a seed per
request; solver tolerances do not measure sampling error.
European pricing samples the exact terminal distribution and ignores
step_count. American exercise grids use step_count points and require at
least three before expiry.

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

### `price_with_greeks`

```python
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
- **`spot_shift`** (`float or None, optional`) — Positive finite absolute spot bump. European default: 0.01 spot units. American default: 8% of spot; None also selects this American default.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.
#### Notes

System entropy and worker-creation failures raise OSError.
For American vanilla options, omitted or None `spot_shift` uses 8% of
spot; other bumps use the shared core defaults.

### `sampling`

Return the sampling choice string: pseudo_random or sobol.

### `antithetic`

Return whether opposite normal draws are paired.

### `seed`

Return the unsigned 64-bit seed, or None for system entropy.

### `path_count`

Return the exact number of sampled paths.

### `thread_count`

Return the per-call worker cap; zero selects automatic sizing.

### `step_count`

Return the configured grid size.

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

## `QuadratureAccumulatorEngine`

```python
QuadratureAccumulatorEngine(**fields)
```

Flat-rate quadrature pricing with immutable integration settings.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Spatial grid budget, at least 4; defaults to 512.
- **`integration_standard_deviations`** (`float, optional`) — Positive finite integration extent in standard deviations; defaults to 8.
#### Raises

- `InvalidInputError` — If asset_step_count is below 4 or integration_standard_deviations is nonpositive or non-finite.
#### See Also

Accumulator : Supported contract.

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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

### `asset_step_count`

Return the configured spatial grid budget.

### `integration_standard_deviations`

Return the integration extent in standard deviations.

## `QuadratureAutocallableEngine`

```python
QuadratureAutocallableEngine(**fields)
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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

### `asset_step_count`

Return the configured spatial grid budget.

### `integration_standard_deviations`

Return the integration extent in standard deviations.

## `QuadratureBarrierEngine`

```python
QuadratureBarrierEngine(**fields)
```

Flat-rate quadrature pricing with immutable integration settings.

#### Parameters

- **`asset_step_count`** (`int, optional`) — Spatial grid budget, at least 4; defaults to 512.
- **`integration_standard_deviations`** (`float, optional`) — Positive finite integration extent in standard deviations; defaults to 8.
#### Raises

- `InvalidInputError` — If asset_step_count is below 4 or integration_standard_deviations is nonpositive or non-finite.
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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

### `asset_step_count`

Return the configured spatial grid budget.

### `integration_standard_deviations`

Return the integration extent in standard deviations.

## `QuadratureDigitalEngine`

```python
QuadratureDigitalEngine()
```

Flat-rate terminal quadrature with a fixed 2,048-panel Simpson rule.

#### Notes

The vanilla engine accepts EuropeanOption; the digital engine accepts
CashOrNothingOption and AssetOrNothingOption.

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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
- **`spot_shift`** (`float, optional`) — Positive finite absolute spot bump; defaults to 0.01 spot units.
- **`volatility_shift`** (`float, optional`) — Positive finite volatility bump in decimal units; defaults to 0.0001.
- **`rate_shift`** (`float, optional`) — Positive finite parallel risk-free-rate bump in decimal units; defaults to 0.0001.
- **`time_shift_days`** (`int, optional`) — Positive forward/backward time bump in calendar days; defaults to 1. All bumps are validated even when analytic Greeks are available.
#### Returns

- `PricingResult` — Price and requested Greeks. Unsupported or undefined Greeks are None, including every Greek at expiry. Units follow PricingResult.
#### Raises

- `KiyosiError` — If requests, shifts, pricing or a feasible bumped valuation fails.

## `QuadratureVanillaEngine`

```python
QuadratureVanillaEngine()
```

Flat-rate terminal quadrature with a fixed 2,048-panel Simpson rule.

#### Notes

The vanilla engine accepts EuropeanOption; the digital engine accepts
CashOrNothingOption and AssetOrNothingOption.

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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
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

Analytic continuous average-price pricing.

#### Notes

AnalyticGeometricAveragePriceEngine accepts geometric averages and
deterministic curves. TurnbullWakemanArithmeticAveragePriceEngine uses
a Levy-compatible moment approximation and requires flat rates before
expiry. It accepts arithmetic averages.

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
price_with_greeks(self, /, instrument, context, greeks=None, **settings)
```

Return the price and selected sensitivities.

#### Parameters

- **`instrument`** (`object`) — Supported contract; see the engine class for accepted types.
- **`context`** (`PricingContext`) — Market snapshot and valuation instant.
- **`greeks`** (`str or iterable of str, optional`) — Greek names. Required unless `all_greeks=True`; duplicates are ignored.
- **`all_greeks`** (`bool, optional`) — Request every measure; omit `greeks` when True. Defaults to False.
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
implied_coupon(engine, instrument, context, observed_price, **settings)
```

Solve the annual coupon that reproduces an observed price.

#### Parameters

- **`engine`** (`object`) — QuadratureAutocallableEngine, FiniteDifferenceAutocallableEngine or MonteCarloAutocallableEngine.
- **`instrument`** (`object`) — SnowballOption, BinarySnowballOption, TernarySnowballOption or PhoenixOption; the original is unchanged.
- **`context`** (`PricingContext`) — Market snapshot; the original is unchanged.
- **`observed_price`** (`float`) — Finite target price in the engine's payment units.
- **`quote_convention`** (`CouponQuoteConvention`) — Required for snowballs: shift_maturity_coupon shifts the maturity coupon with observation coupons; preserve_maturity_coupon keeps it fixed. Omit this keyword for Phoenix.
- **`lower_bound`** (`float, optional`) — Finite lower annual coupon in decimal units; defaults to 0. Signed bounds are accepted when the resulting contract terms are valid.
- **`upper_bound`** (`float, optional`) — Finite upper annual coupon, above lower_bound; defaults to 2.
- **`price_tolerance`** (`float, optional`) — Positive finite absolute price residual tolerance; defaults to 1e-8.
- **`parameter_tolerance`** (`float, optional`) — Positive finite bracket-width tolerance in decimal units; defaults to 1e-8. Either tolerance can stop iteration.
- **`max_iterations`** (`int, optional`) — Positive iteration budget; defaults to 100. Endpoint and affine-interpolation evaluations do not use this budget.
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
Snowballs shift all observation coupons relative to the first one,
including past observations. The maturity convention controls the final
coupon; the ternary minimum remains fixed. Phoenix replaces its
conditional annual coupon. Trials use affine interpolation, then bisection.

## `implied_volatility`

```python
implied_volatility(engine, instrument, context, observed_price, **settings)
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
