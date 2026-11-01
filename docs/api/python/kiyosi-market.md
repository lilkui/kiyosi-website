---
description: kiyosi.market 的 Python API 参考文档。
outline: [2, 4]
---

# `kiyosi.market`

Market snapshots, calendars, and observation schedules.

Rates and volatility use annual decimal units (0.05 means 5%). Rate curves
use Actual/365 Fixed time; a calendar's trading-day basis applies only to
trading-year fractions. ``BusinessDayConvention`` accepts ``"following"``
or ``"preceding"``, including the supplied date when it is open.
LocalVolatilitySurface owns a rectangular table (rows=time, columns=absolute
spot), interpolating sigma bilinearly with flat price tails and no time
extrapolation. Context changes keep these absolute nodes fixed. All FD engines
support LocalVolatilityParameters for price, delta and gamma; Digital FD requires
explicitly flat risk-free and dividend rates. Non-FD engines, other Greeks and
inverse solves reject this model with UnsupportedOperationError.
Model and context ``replace()`` methods expose named keyword-only fields.
Omitted fields, or the displayed default ``...`` (``Ellipsis``), retain their
values; explicit ``None`` is rejected.

## Examples

Build monthly observations from a month-end anchor. February is clamped
without moving the March anchor:

```python
>>> from datetime import date
>>> schedule = monthly_schedule(
...     start=date(2025, 1, 31), end=date(2025, 3, 31),
...     first_observation_month=1, calendar=all_days_calendar(),
... )
>>> list(schedule)
[datetime.date(2025, 2, 28), datetime.date(2025, 3, 31)]
```


Combine a discount curve with a scalar dividend yield:

```python
>>> curve = RateTermStructure(
...     reference_time=date(2025, 1, 1), times=[date(2026, 1, 1)],
...     factors=[0.95],
... )
>>> model = BlackScholesMertonParameters(
...     risk_free_rate=curve, dividend_yield=0.02, volatility=0.2,
... )
>>> context = PricingContext(
...     model_parameters=model, spot_price=100, valuation_time=date(2025, 1, 1),
... )
>>> round(context.model_parameters.risk_free_curve.factor(
...     date(2025, 1, 1), date(2026, 1, 1),
... ), 2)
0.95
```

## `BlackScholesMertonParameters`

```python
BlackScholesMertonParameters(*, risk_free_rate, dividend_yield, volatility)
```

Immutable BSM rates and strictly positive annual volatility.

#### Parameters

- **`risk_free_rate`** (`float or RateTermStructure`) — Continuously compounded risk-free rate or owned rate curve.
- **`dividend_yield`** (`float or RateTermStructure`) — Continuously compounded dividend yield or owned rate curve.
- **`volatility`** (`float`) — Positive finite annual volatility in decimal units.
#### Raises

- `InvalidInputError` — If scalar rates are non-finite or volatility is nonpositive/non-finite.

### `dividend_curve`

Return an owned copy of the dividend curve.

### `dividend_yield`

Return the scalar dividend yield or an owned node curve.

### `replace`

```python
replace(self, /, *, risk_free_rate=Ellipsis, dividend_yield=Ellipsis, volatility=Ellipsis)
```

Return a validated replacement without changing this value.

#### Parameters

- **`risk_free_rate`** (`float or RateTermStructure, optional`) — Continuously compounded risk-free rate or owned rate curve.
- **`dividend_yield`** (`float or RateTermStructure, optional`) — Continuously compounded dividend yield or owned rate curve.
- **`volatility`** (`float, optional`) — Positive finite annual volatility in decimal units.
#### Returns

- `object` — New instance of the same class; omitted fields or Ellipsis retain their values.
#### Raises

- `KiyosiError` — If replacement terms fail domain validation. The original is unchanged.

### `risk_free_curve`

Return an owned copy of the risk-free curve.

### `risk_free_rate`

Return the scalar risk-free rate or an owned node curve.

### `volatility`

Return positive finite annual volatility in decimal units.

## `BusinessDayConvention`

```python
BusinessDayConvention = typing.Literal['following', 'preceding']
```

## `LocalVolatilityParameters`

```python
LocalVolatilityParameters(*, risk_free_rate, dividend_yield, surface)
```

Immutable local-volatility parameters with owned rate curves and surface.

#### Parameters

- **`risk_free_rate, dividend_yield`** (`float or RateTermStructure`) — Finite continuously compounded rates or validated rate curves.
- **`surface`** (`LocalVolatilitySurface`) — Validated surface in absolute time and price coordinates.
#### Raises

- `InvalidInputError` — If a scalar rate is non-finite. Coverage is checked by the context and pricing over required remaining horizons. All FD product families support price, delta and gamma; Digital FD requires flat rates.

### `dividend_curve`

Return an owned copy of the dividend curve.

### `dividend_yield`

Return a scalar dividend yield or an owned node curve.

### `replace`

```python
replace(self, /, *, risk_free_rate=Ellipsis, dividend_yield=Ellipsis, surface=Ellipsis)
```

Return a validated new model; omitted fields or Ellipsis retain their values.

#### Parameters

- **`risk_free_rate, dividend_yield`** (`float or RateTermStructure, optional`) — Replacement continuously compounded rates or curves.
- **`surface`** (`LocalVolatilitySurface, optional`) — Replacement owned surface.
#### Returns

- `LocalVolatilityParameters` — Independent replacement; the original is unchanged on failure.
#### Raises

- `InvalidInputError` — If a replacement scalar rate is non-finite.

### `risk_free_curve`

Return an owned copy of the risk-free curve.

### `risk_free_rate`

Return a scalar risk-free rate or an owned node curve.

### `surface`

Return an owned copy of the fixed surface.

## `LocalVolatilitySurface`

```python
LocalVolatilitySurface(*, times, spots, values)
```

Immutable local-volatility table, with rows=time and columns=absolute spot.

#### Parameters

- **`times`** (`iterable of datetime.date or datetime.datetime`) — At least two strictly increasing instants; the first is the reference.
- **`spots`** (`iterable of float`) — At least two strictly increasing positive finite prices.
- **`values`** (`iterable of iterable of float`) — Rectangular positive finite annual volatilities (20% is 0.2).
#### Raises

- `InvalidInputError` — If the table shape, nodes or values are invalid.
#### Notes

Sigma interpolates bilinearly on time and absolute price using Actual/365
Fixed. Time extrapolation is rejected; price tails use endpoint volatility.
Inputs are copied. Properties return owned copies; spot changes and time
rolls never translate the surface. Native conversion errors reject booleans,
naive datetimes and invalid iterable elements.

### `maximum_volatility`

Return the largest supplied annual volatility.

### `spots`

Return copied absolute price nodes.

### `times`

Return copied absolute time nodes as UTC datetimes.

### `values`

Return copied volatility rows, indexed by time then price.

### `volatility`

```python
volatility(self, /, time, spot)
```

Interpolate sigma at an absolute time and positive spot.

#### Parameters

- **`time`** (`datetime.date or datetime.datetime`) — Covered query instant.
- **`spot`** (`float`) — Positive finite underlying price; price tails are flat.
#### Returns

- `float` — Annual local volatility in decimal units.
#### Raises

- `InvalidInputError` — If time is outside coverage or spot is nonpositive/non-finite.

## `ObservationSchedule`

Immutable ordered observation dates with sequence access.

#### Notes

Use fixed_interval_schedule or monthly_schedule. The dates property
returns a copy; iteration retains the schedule owner. Integer indexing
accepts negative indices and raises IndexError outside the sequence.
Slices are not supported. len(schedule) counts observations.

### `__getitem__`

```python
__getitem__(self, key, /)
```

Return self[key].

### `__iter__`

```python
__iter__(self, /)
```

Implement iter(self).

### `__len__`

```python
__len__(self, /)
```

Return len(self).

### `dates`

Return a copy of the strictly ordered observation dates.

## `PricingContext`

```python
PricingContext(*, model_parameters, spot_price, valuation_time, calendar=Ellipsis)
```

Immutable market snapshot for one valuation instant.

#### Parameters

- **`model_parameters`** (`BlackScholesMertonParameters or LocalVolatilityParameters`) — Validated rates and BSM volatility or a local-volatility surface.
- **`spot_price`** (`float`) — Positive finite underlying spot price.
- **`valuation_time`** (`datetime.date or datetime.datetime`) — Valuation instant. Dates mean midnight; aware datetimes convert to UTC.
- **`calendar`** (`TradingCalendar, optional`) — Trading calendar. Defaults to weekdays with a 252-day basis.
#### Raises

- `InvalidInputError` — If spot_price is nonpositive/non-finite or valuation_time is outside either rate curve or the local-volatility surface. Contract-life and expiry coverage checks occur at pricing.

### `calendar`

Return an owned copy of the trading calendar.

### `model_parameters`

Return an owned copy of the model parameters.

### `replace`

```python
replace(self, /, *, model_parameters=Ellipsis, spot_price=Ellipsis, valuation_time=Ellipsis, calendar=Ellipsis)
```

Return a validated replacement without changing this value.

#### Parameters

- **`model_parameters`** (`BlackScholesMertonParameters or LocalVolatilityParameters, optional`) — Validated rates and BSM volatility or a local-volatility surface.
- **`spot_price`** (`float, optional`) — Positive finite underlying spot price.
- **`valuation_time`** (`datetime.date or datetime.datetime, optional`) — Valuation instant. Dates mean midnight; aware datetimes convert to UTC.
- **`calendar`** (`TradingCalendar, optional`) — Trading calendar. Defaults to weekdays with a 252-day basis.
#### Returns

- `object` — New instance of the same class; omitted fields or Ellipsis retain their values.
#### Raises

- `KiyosiError` — If replacement terms fail domain validation. The original is unchanged.

### `spot_price`

Return positive finite underlying spot price.

### `valuation_date`

Return the date containing the valuation instant.

### `valuation_time`

Return valuation instant. Dates mean midnight; aware datetimes convert to UTC.

## `RateTermStructure`

```python
RateTermStructure(*, reference_time, times, factors)
```

Immutable rate curve with log-linear factors and Actual/365 Fixed time.

#### Parameters

- **`reference_time`** (`datetime.date or datetime.datetime`) — Inclusive curve reference; factors equal one at this instant.
- **`times`** (`iterable of datetime.date or datetime.datetime`) — Strictly increasing nodes after the reference.
- **`factors`** (`iterable of float`) — Positive finite factors at the nodes; log factors interpolate linearly.
#### Raises

- `InvalidInputError` — If nodes or factors are empty or mismatched, times do not increase after the reference, factors are nonpositive/non-finite, or implied forward rates are non-finite.
#### Notes

Dated curves reject times before their reference; node curves also reject
times after the last node. Negative rates are allowed.

### `factor`

```python
factor(self, /, start, end)
```

Return the factor over an ordered, covered interval.

#### Parameters

- **`start, end`** (`datetime.date or datetime.datetime`) — Ordered interval endpoints.
#### Returns

- `float` — Interval factor; underflow to zero is allowed.
#### Raises

- `InvalidInputError` — If endpoints are reversed or outside curve coverage.
- `ComputationFailureError` — If the log factor is non-finite or exponentiation overflows.

### `factors`

Return copied node factors, including any parallel shift.

### `flat`

```python
flat(rate, *, reference_time=None)
```

Create a continuously compounded flat rate curve.

#### Parameters

- **`rate`** (`float`) — Finite annual rate in decimal units; negative rates are allowed.
- **`reference_time`** (`datetime.date or datetime.datetime, optional`) — Inclusive lower coverage bound, or None for an undated curve.
#### Returns

- `RateTermStructure` — Owned flat curve with no upper coverage bound.
#### Raises

- `InvalidInputError` — If the rate is non-finite.

### `forward_rate`

```python
forward_rate(self, /, time)
```

Return the right-hand instantaneous forward rate.

#### Parameters

- **`time`** (`datetime.date or datetime.datetime`) — Query instant. The final node uses its left interval.
#### Returns

- `float` — Annual continuously compounded forward rate in decimal units.
#### Raises

- `InvalidInputError` — If the instant is outside curve coverage.

### `is_flat`

Return whether the rate curve is explicitly flat.

### `log_factor`

```python
log_factor(self, /, start, end)
```

Return the log factor over an ordered, covered interval.

#### Parameters

- **`start, end`** (`datetime.date or datetime.datetime`) — Ordered interval endpoints.
#### Returns

- `float` — Log of the interval factor, using Actual/365 Fixed time.
#### Raises

- `InvalidInputError` — If endpoints are reversed or outside curve coverage.
- `ComputationFailureError` — If the result is non-finite.

### `max_time`

Return the final node time, or None for a flat curve.

### `nodes`

Return a copy of the supplied curve node times.

### `reference_time`

Return the inclusive lower coverage bound, or None if undated.

### `shifted`

```python
shifted(self, /, shift)
```

Create a parallel rate shift without changing this curve.

#### Parameters

- **`shift`** (`float`) — Finite additive rate shift in decimal units.
#### Returns

- `RateTermStructure` — Independent curve with unchanged coverage.
#### Raises

- `InvalidInputError` — If the shift or resulting rates are non-finite.

## `TradingCalendar`

Immutable trading calendar with a fixed annualization basis.

#### Notes

Use the calendar factory functions to construct instances.

### `adjust`

```python
adjust(self, /, nominal, convention)
```

Find a trading date in the selected direction, including the input date.

#### Parameters

- **`nominal`** (`datetime.date`) — Unadjusted date.
- **`convention`** (`{'following', 'preceding'}`) — Direction to search.
#### Returns

- `datetime.date` — First trading date encountered.
#### Raises

- `InvalidInputError` — If the supported date range is exhausted.

### `is_trading_day`

```python
is_trading_day(self, /, value)
```

Return whether a date is open in this calendar.

#### Parameters

- **`value`** (`datetime.date`) — Date to test; datetime values are not accepted.
#### Returns

- `bool` — Whether the date is a trading day, including explicit overrides.

### `trading_days_between`

```python
trading_days_between(self, /, start, end)
```

Count trading dates in the half-open interval [start, end).

#### Parameters

- **`start, end`** (`datetime.date`) — Ordered interval endpoints.
#### Returns

- `int` — Number of trading dates.
#### Raises

- `InvalidInputError` — If end precedes start.

### `trading_days_per_year`

Return the positive calendar annualization basis.

### `trading_year_fraction`

```python
trading_year_fraction(self, /, start, end)
```

Return trading-day count divided by the calendar annualization basis.

#### Parameters

- **`start, end`** (`datetime.date`) — Ordered endpoints of the half-open interval [start, end).
#### Returns

- `float` — Trading-year fraction.
#### Raises

- `InvalidInputError` — If end precedes start.

## `all_days_calendar`

```python
all_days_calendar()
```

Create a calendar with every date open and a 365-day basis.

#### Returns

- `TradingCalendar` — Calendar with the stated annualization basis.

## `custom_calendar`

```python
custom_calendar(*, base, closed_dates=Ellipsis, open_dates=Ellipsis, trading_days_per_year=None)
```

Create open and closed overrides without changing the base calendar.

#### Parameters

- **`base`** (`TradingCalendar`) — Base calendar; the original is unchanged.
- **`closed_dates`** (`iterable of date, optional`) — Dates forced closed; duplicates and unsorted input are accepted.
- **`open_dates`** (`iterable of date, optional`) — Dates forced open, including weekends; must not also be closed.
- **`trading_days_per_year`** (`int or None, optional`) — Positive annualization basis, or None to retain the base basis.
#### Returns

- `TradingCalendar` — Owned result; no input is mutated.
#### Raises

- `InvalidInputError` — If a date is both open and closed, or the annualization basis is nonpositive.

## `fixed_interval_schedule`

```python
fixed_interval_schedule(*, start, end, interval_days, calendar=Ellipsis)
```

Creates adjusted observations at positive fixed calendar-day intervals.

#### Parameters

- **`start`** (`datetime.date`) — First date of the interval.
- **`end`** (`datetime.date`) — Last date of the interval.
- **`interval_days`** (`int`) — Positive calendar-day spacing of unadjusted observations, up to 2**63 - 1.
- **`calendar`** (`TradingCalendar, optional`) — Trading calendar. Defaults to weekdays with a 252-day basis.
#### Returns

- `ObservationSchedule` — Owned result; no input is mutated.
#### Raises

- `InvalidInputError` — If end precedes start or interval_days is nonpositive.
- `TypeError` — If interval_days is not an integer or is bool.
- `OverflowError` — If interval_days is outside the signed 64-bit range.
#### Notes

Exclude start and include candidates through end. Following adjustment
merges collisions and stops before crossing end; end need not appear.

## `monthly_schedule`

```python
monthly_schedule(*, start, end, first_observation_month, calendar=Ellipsis)
```

Create monthly observations anchored to the start day.

#### Parameters

- **`start`** (`datetime.date`) — First date of the interval.
- **`end`** (`datetime.date`) — Last date of the interval.
- **`first_observation_month`** (`int`) — Positive month offset from start to the first observation.
- **`calendar`** (`TradingCalendar, optional`) — Trading calendar. Defaults to weekdays with a 252-day basis.
#### Returns

- `ObservationSchedule` — Owned result; no input is mutated.
#### Raises

- `InvalidInputError` — If end precedes start or first_observation_month is nonpositive.
#### Notes

Clamp each candidate to its month end while retaining the original
start-day anchor for later months.
Exclude start and include candidates through end. Following adjustment
merges collisions and stops before crossing end; end need not appear.

## `sse_calendar`

```python
sse_calendar()
```

Create an SSE weekday-closure calendar with a 243-day basis.

#### Returns

- `TradingCalendar` — Calendar with the stated annualization basis.
#### Notes

Uses recorded and forecast weekday closures for 1991-2099, and weekdays
outside that range. Forecasts omit ad-hoc closures.

## `weekdays_calendar`

```python
weekdays_calendar()
```

Create a Monday-through-Friday calendar with a 252-day basis.

#### Returns

- `TradingCalendar` — Calendar with the stated annualization basis.
