---
description: Python API reference for kiyosi.market.
outline: [2, 4]
---

# `kiyosi.market`

Market snapshots, calendars, and observation schedules.

## `BlackScholesMertonParameters`

```python
BlackScholesMertonParameters(self, *, risk_free_rate: float, dividend_yield: float, volatility: float) -> None
```

Validated Black-Scholes-Merton market parameters.

Parameters are continuously compounded decimal rates and an annualized decimal
volatility. Instances are immutable value objects.

#### Attributes

- **`risk_free_rate`** (`float`) — Continuously compounded annual risk-free rate.
- **`dividend_yield`** (`float`) — Continuously compounded annual dividend yield.
- **`volatility`** (`float`) — Positive annualized volatility.

### Constructor

Create validated Black-Scholes-Merton parameters.

#### Parameters

- **`risk_free_rate`** (`float`) — Continuously compounded annual risk-free rate.
- **`dividend_yield`** (`float`) — Continuously compounded annual dividend yield.
- **`volatility`** (`float`) — Positive annualized volatility.
#### Raises

- `TypeError` — If a value is not a real number.
- `OverflowError` — If a value cannot be represented as a C++ ``double``.
- `KiyosiError` — If a value is non-finite or volatility is not positive.

### `risk_free_rate`

Continuously compounded annual risk-free rate.

### `dividend_yield`

Continuously compounded annual dividend yield.

### `volatility`

Positive annualized volatility.

## `ObservationSchedule`

Immutable ordered observation dates.

The sequence supports ``len(schedule)``, integer indexing, negative indexing,
and iteration.

#### Attributes

- **`dates`** (`list[datetime.date]`) — Copy of the ordered observation dates.

### `__len__`

```python
__len__(self) -> int
```

### `__getitem__`

```python
__getitem__(self, arg: int, /) -> datetime.date
```

### `__iter__`

```python
__iter__(self) -> collections.abc.Iterator[datetime.date]
```

### `dates`

Copy of the ordered observation dates.

## `PricingContext`

```python
PricingContext(self, *, model_parameters: BlackScholesMertonParameters, spot_price: float, valuation_time: datetime.date | datetime.datetime, calendar: TradingCalendar = TradingCalendar(trading_days_per_year=252)) -> None
```

Validated market state for a valuation instant.

#### Attributes

- **`model_parameters`** (`BlackScholesMertonParameters`) — Read-only parameters view tied to this context's lifetime.
- **`spot_price`** (`float`) — Positive underlying spot price.
- **`valuation_date`** (`datetime.date`) — UTC calendar date containing the valuation instant.
- **`valuation_time`** (`datetime.datetime`) — Timezone-aware valuation timestamp normalized to UTC.
- **`calendar`** (`TradingCalendar`) — Read-only calendar view tied to this context's lifetime.

### Constructor

Create a validated pricing context.

#### Parameters

- **`model_parameters`** (`BlackScholesMertonParameters`) — Black-Scholes-Merton market parameters.
- **`spot_price`** (`float`) — Positive underlying spot price.
- **`valuation_time`** (`datetime.date or datetime.datetime`) — Valuation instant. Dates denote midnight UTC; datetimes must be timezone aware and are normalized to UTC.
- **`calendar`** (`TradingCalendar, optional`) — Trading calendar. Defaults to `weekdays_calendar`.
#### Raises

- `TypeError` — If an argument has an incompatible representation or a datetime is naive.
- `KiyosiError` — If the core rejects the spot price or valuation state.

### `model_parameters`

Read-only parameters view that keeps this context alive; concurrent reads are safe.

### `spot_price`

Positive underlying spot price.

### `valuation_date`

UTC date containing the valuation instant.

### `valuation_time`

Timezone-aware valuation timestamp normalized to UTC.

### `calendar`

Read-only calendar view that keeps this context alive; concurrent reads are safe.

## `TradingCalendar`

Read-only trading-day calendar.

Instances are created by `all_days_calendar`, `weekdays_calendar`,
or `sse_calendar`.

#### Attributes

- **`trading_days_per_year`** (`int`) — Annualization denominator used for trading-year fractions.

### `is_trading_day`

```python
is_trading_day(self, value: datetime.date) -> bool
```

Return whether a date is a trading day.

#### Parameters

- **`value`** (`datetime.date`) — Calendar date to inspect.
#### Returns

- `bool` — ``True`` when the date is open for trading.
#### Raises

- `TypeError` — If ``value`` is not a `datetime.date`.

### `trading_days_between`

```python
trading_days_between(self, start: datetime.date, end: datetime.date) -> int
```

Count trading days in the half-open interval ``[start, end)``.

#### Parameters

- **`start`** (`datetime.date`) — First date included in the interval.
- **`end`** (`datetime.date`) — Exclusive interval end.
#### Returns

- `int` — Number of trading days.
#### Raises

- `TypeError` — If either argument is not a `datetime.date`.
- `KiyosiError` — If the range is reversed.

### `trading_year_fraction`

```python
trading_year_fraction(self, start: datetime.date, end: datetime.date) -> float
```

Return the trading-year fraction for ``[start, end)``.

#### Parameters

- **`start`** (`datetime.date`) — First date included in the interval.
- **`end`** (`datetime.date`) — Exclusive interval end.
#### Returns

- `float` — Trading-day count divided by `trading_days_per_year`.
#### Raises

- `TypeError` — If either argument is not a `datetime.date`.
- `KiyosiError` — If the range is reversed.

### `trading_days_per_year`

Annualization denominator for trading-year fractions.

## `all_days_calendar`

```python
all_days_calendar() -> TradingCalendar
```

Return a calendar in which every day is a trading day.

#### Returns

- `TradingCalendar` — Calendar with 365 annual trading days.

## `fixed_interval_schedule`

```python
fixed_interval_schedule(*, start: datetime.date, end: datetime.date, interval_days: int, calendar: TradingCalendar = TradingCalendar(trading_days_per_year=252)) -> ObservationSchedule
```

Build a fixed-calendar-day observation schedule.

Candidates are ``start + n * interval_days`` for positive ``n``. start is excluded
and ``end`` is an inclusive bound. Candidates use following
trading-day adjustment, duplicate adjusted dates are removed, and generation
stops rather than crossing ``end``; ``end`` is not guaranteed.

#### Parameters

- **`start`** (`datetime.date`) — Anchor date, excluded from the result.
- **`end`** (`datetime.date`) — Inclusive upper bound for adjusted dates.
- **`interval_days`** (`int`) — Positive number of calendar days between candidates.
- **`calendar`** (`TradingCalendar, optional`) — Adjustment calendar. Defaults to `weekdays_calendar`.
#### Returns

- `ObservationSchedule` — Immutable adjusted observation dates.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `OverflowError` — If ``interval_days`` is outside the C++ ``int`` range.
- `KiyosiError` — If the dates, interval, calendar, or resulting schedule are invalid.
#### Examples

With the weekdays calendar, 2025-01-03 through 2025-01-07 at a one-day
interval produces 2025-01-06 and 2025-01-07. Supply explicit
``observation_dates`` to an instrument constructor for bespoke terminal dates.

## `monthly_schedule`

```python
monthly_schedule(*, start: datetime.date, end: datetime.date, lock_up_months: int, calendar: TradingCalendar = TradingCalendar(trading_days_per_year=252)) -> ObservationSchedule
```

Build a monthly observation schedule after a lock-up period.

Monthly candidates begin at ``start + lock_up_months``. ``start`` is excluded
and ``end`` is an inclusive bound. The start day is clamped to each target
month's last day, then candidates use following trading-day adjustment.
Generation stops rather than crossing ``end``, so ``end`` is not guaranteed.

#### Parameters

- **`start`** (`datetime.date`) — Anchor date, excluded from the result.
- **`end`** (`datetime.date`) — Inclusive upper bound for adjusted dates.
- **`lock_up_months`** (`int`) — Positive number of months before the first candidate.
- **`calendar`** (`TradingCalendar, optional`) — Adjustment calendar. Defaults to `weekdays_calendar`.
#### Returns

- `ObservationSchedule` — Immutable adjusted observation dates.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `OverflowError` — If ``lock_up_months`` is outside the C++ ``int`` range.
- `KiyosiError` — If the dates, lock-up, calendar, or resulting schedule are invalid.
#### Examples

With the weekdays calendar, 2025-01-01 through 2025-03-01 with one lock-up
month produces only 2025-02-03; adjusting the Saturday end candidate would
cross the bound. Supply explicit ``observation_dates`` to an instrument
constructor for bespoke terminal dates.

## `sse_calendar`

```python
sse_calendar() -> TradingCalendar
```

Return the Shanghai Stock Exchange holiday calendar.

#### Returns

- `TradingCalendar` — Exchange calendar with 252 annual trading days.

## `weekdays_calendar`

```python
weekdays_calendar() -> TradingCalendar
```

Return a holiday-unaware weekdays calendar.

#### Returns

- `TradingCalendar` — Monday-to-Friday calendar with 252 annual trading days.
