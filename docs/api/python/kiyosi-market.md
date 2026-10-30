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

## Examples

Build monthly observations from a month-end anchor. February is clamped
without moving the March anchor:

```python
>>> from datetime import date
>>> schedule = monthly_schedule(
...     start=date(2025, 1, 31), end=date(2025, 3, 31),
...     first_observation_month=1, calendar=all_days_calendar(),
... )
>>> schedule.dates
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

### `replace`

```python
replace(self, /, **changes)
```

Return a validated replacement without changing this value.

#### Parameters

- **`risk_free_rate`** (`float or RateTermStructure, optional`) — Continuously compounded risk-free rate or owned rate curve.
- **`dividend_yield`** (`float or RateTermStructure, optional`) — Continuously compounded dividend yield or owned rate curve.
- **`volatility`** (`float, optional`) — Positive finite annual volatility in decimal units.
#### Returns

- `object` — New instance of the same class; omitted fields retain their values.
#### Raises

- `KiyosiError` — If replacement terms fail domain validation. The original is unchanged.

### `risk_free_rate`

Return the scalar risk-free rate or an owned node curve.

### `dividend_curve`

Return an owned copy of the dividend curve.

### `risk_free_curve`

Return an owned copy of the risk-free curve.

### `dividend_yield`

Return the scalar dividend yield or an owned node curve.

### `volatility`

Return positive finite annual volatility in decimal units.

## `BusinessDayConvention`

```python
BusinessDayConvention = typing.Literal['following', 'preceding']
```

## `ObservationSchedule`

```python
ObservationSchedule()
```

Immutable ordered observation dates with sequence access.

#### Notes

Use fixed_interval_schedule or monthly_schedule. The dates property
returns a copy; iteration retains the schedule owner. Integer indexing
accepts negative indices and raises IndexError outside the sequence.
Slices are not supported. len(schedule) counts observations.

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

### `__getitem__`

```python
__getitem__(self, key, /)
```

Return self[key].

### `dates`

Return a copy of the strictly ordered observation dates.

## `PricingContext`

```python
PricingContext(*, model_parameters, spot_price, valuation_time, calendar=Ellipsis)
```

Immutable market snapshot for one valuation instant.

#### Parameters

- **`model_parameters`** (`BlackScholesMertonParameters`) — Validated BSM rates and volatility.
- **`spot_price`** (`float`) — Positive finite underlying spot price.
- **`valuation_time`** (`datetime.date or datetime.datetime`) — Valuation instant. Dates mean midnight; aware datetimes convert to UTC.
- **`calendar`** (`TradingCalendar, optional`) — Trading calendar. Defaults to weekdays with a 252-day basis.
#### Raises

- `InvalidInputError` — If spot_price is nonpositive/non-finite or valuation_time is outside either rate curve. Contract-life checks occur at pricing.

### `replace`

```python
replace(self, /, **changes)
```

Return a validated replacement without changing this value.

#### Parameters

- **`model_parameters`** (`BlackScholesMertonParameters, optional`) — Validated BSM rates and volatility.
- **`spot_price`** (`float, optional`) — Positive finite underlying spot price.
- **`valuation_time`** (`datetime.date or datetime.datetime, optional`) — Valuation instant. Dates mean midnight; aware datetimes convert to UTC.
- **`calendar`** (`TradingCalendar, optional`) — Trading calendar. Defaults to weekdays with a 252-day basis.
#### Returns

- `object` — New instance of the same class; omitted fields retain their values.
#### Raises

- `KiyosiError` — If replacement terms fail domain validation. The original is unchanged.

### `valuation_time`

Return valuation instant. Dates mean midnight; aware datetimes convert to UTC.

### `calendar`

Return an owned copy of the trading calendar.

### `valuation_date`

Return the date containing the valuation instant.

### `spot_price`

Return positive finite underlying spot price.

### `model_parameters`

Return an owned copy of the model parameters.

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

### `is_flat`

Return whether the rate curve is explicitly flat.

### `reference_time`

Return the inclusive lower coverage bound, or None if undated.

### `nodes`

Return a copy of the supplied curve node times.

### `max_time`

Return the final node time, or None for a flat curve.

### `factors`

Return copied node factors, including any parallel shift.

## `TradingCalendar`

```python
TradingCalendar()
```

Immutable trading calendar with a fixed annualization basis.

#### Notes

Use the calendar factory functions to construct instances.

### `is_trading_day`

```python
is_trading_day(self, /, value)
```

Return whether a date is open in this calendar.

#### Parameters

- **`value`** (`datetime.date`) — Date to test; datetime values are not accepted.
#### Returns

- `bool` — Whether the date is a trading day, including explicit overrides.

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

### `trading_days_per_year`

Return the positive calendar annualization basis.

## `all_days_calendar`

```python
all_days_calendar()
```

Create a calendar with every date open and a 365-day basis.

#### Returns

- `TradingCalendar` — Calendar with the stated annualization basis.

## `custom_calendar`

```python
custom_calendar(*, base, **overrides)
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
