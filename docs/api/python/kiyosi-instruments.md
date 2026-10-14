---
description: Python API reference for kiyosi.instruments.
outline: [2, 4]
---

# `kiyosi.instruments`

Validated derivative instruments.

## `Accumulator`

```python
Accumulator(self, *, strike: float, knock_out_level: float, daily_quantity: float, acceleration_factor: float, accumulated_quantity: float = 0.0, effective_date: datetime.date, expiry_date: datetime.date) -> None
```

Immutable validated accumulator contract.

### Constructor

Create a validated accumulator contract.

#### Parameters

- **`strike`** (`float`) — Positive purchase strike.
- **`knock_out_level`** (`float`) — Positive upper knock-out level.
- **`daily_quantity`** (`float`) — Non-negative base quantity accumulated per trading day.
- **`acceleration_factor`** (`float`) — Non-negative quantity multiplier below the strike.
- **`accumulated_quantity`** (`float, optional`) — Non-negative quantity already accumulated at valuation.
- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates, each anchored at 00:00 UTC.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the quantities, levels, or date ordering.

### `strike`

Positive purchase strike.

### `knock_out_level`

Positive upper knock-out level.

### `daily_quantity`

Base quantity accumulated per trading day.

### `acceleration_factor`

Quantity multiplier applied below the strike.

### `accumulated_quantity`

Quantity already accumulated at valuation.

### `effective_date`

First date on which the contract is effective.

### `expiry_date`

Contract expiry at 00:00 UTC.

## `AmericanOption`

```python
AmericanOption(self, *, option_type: typing.Literal['call', 'put'], strike: float, effective_date: datetime.date, expiry_date: datetime.date) -> None
```

Immutable validated American vanilla option.

The payoff may be exercised from the effective date through expiry.

### Constructor

Create a validated American option.

#### Parameters

- **`option_type`** (`{'call', 'put'}`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive strike price.
- **`effective_date`** (`datetime.date`) — First exercise date.
- **`expiry_date`** (`datetime.date`) — Last exercise date.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the strike or date ordering.

### `option_type`

Call or put payoff direction.

### `strike`

Positive strike price.

### `effective_date`

First date on which the contract is effective.

### `expiry_date`

Contract expiry at 00:00 UTC.

## `ArithmeticAveragePriceOption`

```python
ArithmeticAveragePriceOption(self, *, option_type: typing.Literal['call', 'put'], strike: float, averaging_start_date: datetime.date, effective_date: datetime.date, expiry_date: datetime.date, realized_average: float = 0.0) -> None
```

Immutable validated average-price option.

### Constructor

Create a validated average-price option.

#### Parameters

- **`option_type`** (`{'call', 'put'}`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive strike price.
- **`averaging_start_date`** (`datetime.date`) — First date included in the averaging period. Equality with expiry denotes a single fixing.
- **`effective_date`** (`datetime.date`) — First date on which the contract is effective.
- **`expiry_date`** (`datetime.date`) — Contract expiry at 00:00 UTC.
- **`realized_average`** (`float, optional`) — Average realized before valuation time, or zero before averaging begins. Geometric averaging requires a positive value after averaging starts. Defaults to the core-owned pre-averaging value.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the terms or date ordering.

### `averaging_start_date`

First date included in the averaging period; equality with expiry denotes a single fixing.

### `realized_average`

Average realized before valuation, or zero before averaging begins; geometric averaging requires a positive value after averaging starts.

### `option_type`

Call or put payoff direction.

### `strike`

Positive strike price.

### `effective_date`

First date on which the contract is effective.

### `expiry_date`

Contract expiry at 00:00 UTC.

## `AssetOrNothingOption`

```python
AssetOrNothingOption(self, *, option_type: typing.Literal['call', 'put'], strike: float, effective_date: datetime.date, expiry_date: datetime.date) -> None
```

Immutable validated asset-or-nothing digital option.

### Constructor

Create a validated asset-or-nothing option.

#### Parameters

- **`option_type`** (`{'call', 'put'}`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive strike price.
- **`effective_date`** (`datetime.date`) — First date on which the contract is effective.
- **`expiry_date`** (`datetime.date`) — Contract expiry at 00:00 UTC.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the strike or date ordering.

### `option_type`

Call or put payoff direction.

### `strike`

Positive strike price.

### `effective_date`

First date on which the contract is effective.

### `expiry_date`

Contract expiry at 00:00 UTC.

## `AutocallableBarrierState`

```python
AutocallableBarrierState = typing.Literal['none', 'knocked_out', 'knocked_in']
```

## `AutocallableObservation`

```python
AutocallableObservation(self, date: datetime.date, knock_out_level: float, *, coupon_rate: float = 0.0, coupon_barrier_level: float = 0.0) -> None
```

Immutable observation record. Domain validation runs when constructing a note.

### `date`

(self) -> datetime.date

### `knock_out_level`

(self) -> float

### `coupon_rate`

(self) -> float

### `coupon_barrier_level`

(self) -> float

## `BarrierOption`

```python
BarrierOption(self, *, option_type: typing.Literal['call', 'put'], strike: float, effective_date: datetime.date, expiry_date: datetime.date, barrier_level: float, barrier_type: typing.Literal['up_and_in', 'up_and_out', 'down_and_in', 'down_and_out'], rebate: float = 0.0, rebate_timing: typing.Literal['at_hit', 'at_expiry'] = 'at_expiry', observation_mode: typing.Literal['continuous', 'scheduled'] = 'continuous', observation_dates: collections.abc.Iterable[datetime.date] = (), touch_state: typing.Literal['untouched', 'touched'] | None = None) -> None
```

Immutable validated barrier option.

Scheduled barriers are observed only on ``observation_dates``; continuous
barriers require no schedule.

### Constructor

Create a validated barrier option.

#### Parameters

- **`option_type`** (`{'call', 'put'}`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive strike price.
- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates, each anchored at 00:00 UTC.
- **`barrier_level`** (`float`) — Positive barrier level.
- **`barrier_type`** (`{'up_and_in', 'up_and_out', 'down_and_in', 'down_and_out'}`) — Barrier direction and knock-in or knock-out behavior.
- **`rebate`** (`float, optional`) — Rebate amount. Uses the core default when omitted.
- **`rebate_timing`** (`{'at_hit', 'at_expiry'}, optional`) — Time at which the rebate is paid.
- **`observation_mode`** (`{'continuous', 'scheduled'}, optional`) — Continuous or scheduled monitoring.
- **`observation_dates`** (`iterable[datetime.date], optional`) — Required schedule for scheduled monitoring; omitted for continuous monitoring.
- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — History strictly before valuation. Required once prior monitoring was possible.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the payoff, barrier, dates, or observation schedule.

### `barrier_level`

Positive barrier level.

### `barrier_type`

Barrier direction and activation behavior.

### `rebate`

Barrier rebate amount.

### `rebate_timing`

Time at which the rebate is paid.

### `observation_mode`

Continuous or scheduled monitoring mode.

### `touch_state`

Barrier touch history before valuation.

### `observation_dates`

Copy of the scheduled observations at 00:00 UTC.

### `option_type`

Call or put payoff direction.

### `strike`

Positive strike price.

### `effective_date`

First date on which the contract is effective.

### `expiry_date`

Contract expiry at 00:00 UTC.

## `BarrierTouchState`

```python
BarrierTouchState = typing.Literal['untouched', 'touched']
```

## `BarrierType`

```python
BarrierType = typing.Literal['up_and_in', 'up_and_out', 'down_and_in', 'down_and_out']
```

## `BinaryBarrierOption`

Immutable validated strike-based binary barrier option.

Instances are created by `cash_binary_barrier_option` or
`asset_binary_barrier_option`.

### `barrier_level`

Positive barrier level.

### `barrier_type`

Barrier direction and activation behavior.

### `payoff_type`

Cash or asset delivery form.

### `payout`

Cash payout, or None for an asset payoff.

### `observation_mode`

Continuous or scheduled monitoring mode.

### `touch_state`

Barrier touch history before valuation.

### `observation_dates`

Copy of the scheduled observations at 00:00 UTC.

### `option_type`

Call or put payoff direction.

### `strike`

Positive strike price.

### `effective_date`

First date on which the contract is effective.

### `expiry_date`

Contract expiry at 00:00 UTC.

## `BinarySnowballOption`

```python
BinarySnowballOption(self, *, maturity_coupon_rate: float, barrier_state: typing.Literal['none', 'knocked_out', 'knocked_in'] | None = None, principal_ratio: float = 1.0, effective_date: datetime.date, expiry_date: datetime.date, observations: collections.abc.Iterable[AutocallableObservation]) -> None
```

Immutable validated binary snowball option.

### Constructor

Create a validated binary snowball option.

Provide observations as AutocallableObservation records. Use autocallable_observations
to associate parallel sequences before construction. Domain validation runs in the core.

#### Parameters

- **`observations`** (`iterable[AutocallableObservation]`) — Ordered contractual observations at 00:00 UTC.
- **`maturity_coupon_rate`** (`float`) — Annualized coupon rate used at maturity when applicable.
- **`barrier_state`** (`{'none', 'knocked_out', 'knocked_in'} | None, optional`) — State before valuation; required after an observation has occurred.
- **`principal_ratio`** (`float, optional`) — Normalized principal repayment component; coupons and downside are separate.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates, each anchored at 00:00 UTC.
#### Raises

- `TypeError` — If an argument or sequence element has an incompatible representation.
- `KiyosiError` — If the core rejects the rates, levels, schedule, state, or dates.

### `knock_out_coupon_rates`

Annualized coupon rate for each observation date.

### `maturity_coupon_rate`

Annualized coupon rate used at maturity when applicable.

### `observations`

Owning copy of the complete observation records.

### `knock_out_levels`

Knock-out level for each observation date.

### `observation_dates`

Copy of the ordered observation dates.

### `principal_ratio`

Normalized principal repayment component; coupons and downside are separate.

### `barrier_state`

State before valuation, or None when not supplied.

### `effective_date`

First date on which the note is effective.

### `expiry_date`

Note expiry date.

## `CashOrNothingOption`

```python
CashOrNothingOption(self, *, option_type: typing.Literal['call', 'put'], strike: float, payout: float, effective_date: datetime.date, expiry_date: datetime.date) -> None
```

Immutable validated cash-or-nothing digital option.

### Constructor

Create a validated cash-or-nothing option.

#### Parameters

- **`option_type`** (`{'call', 'put'}`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive strike price.
- **`payout`** (`float`) — Fixed cash amount paid when the option finishes in the money.
- **`effective_date`** (`datetime.date`) — First date on which the contract is effective.
- **`expiry_date`** (`datetime.date`) — Contract expiry at 00:00 UTC.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the payoff terms or date ordering.

### `payout`

Fixed in-the-money cash payout.

### `option_type`

Call or put payoff direction.

### `strike`

Positive strike price.

### `effective_date`

First date on which the contract is effective.

### `expiry_date`

Contract expiry at 00:00 UTC.

## `EuropeanOption`

```python
EuropeanOption(self, *, option_type: typing.Literal['call', 'put'], strike: float, effective_date: datetime.date, expiry_date: datetime.date) -> None
```

Immutable validated European vanilla option.

The payoff can be exercised only at expiry.

### Constructor

Create a validated European option.

#### Parameters

- **`option_type`** (`{'call', 'put'}`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive strike price.
- **`effective_date`** (`datetime.date`) — First date on which the contract is effective.
- **`expiry_date`** (`datetime.date`) — Contract expiry at 00:00 UTC.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the strike or date ordering.

### `option_type`

Call or put payoff direction.

### `strike`

Positive strike price.

### `effective_date`

First date on which the contract is effective.

### `expiry_date`

Contract expiry at 00:00 UTC.

## `GeometricAveragePriceOption`

```python
GeometricAveragePriceOption(self, *, option_type: typing.Literal['call', 'put'], strike: float, averaging_start_date: datetime.date, effective_date: datetime.date, expiry_date: datetime.date, realized_average: float = 0.0) -> None
```

Immutable validated average-price option.

### Constructor

Create a validated average-price option.

#### Parameters

- **`option_type`** (`{'call', 'put'}`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive strike price.
- **`averaging_start_date`** (`datetime.date`) — First date included in the averaging period. Equality with expiry denotes a single fixing.
- **`effective_date`** (`datetime.date`) — First date on which the contract is effective.
- **`expiry_date`** (`datetime.date`) — Contract expiry at 00:00 UTC.
- **`realized_average`** (`float, optional`) — Average realized before valuation time, or zero before averaging begins. Geometric averaging requires a positive value after averaging starts. Defaults to the core-owned pre-averaging value.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the terms or date ordering.

### `averaging_start_date`

First date included in the averaging period; equality with expiry denotes a single fixing.

### `realized_average`

Average realized before valuation, or zero before averaging begins; geometric averaging requires a positive value after averaging starts.

### `option_type`

Call or put payoff direction.

### `strike`

Positive strike price.

### `effective_date`

First date on which the contract is effective.

### `expiry_date`

Contract expiry at 00:00 UTC.

## `KnockInObservationMode`

```python
KnockInObservationMode = typing.Literal['every_trading_day', 'at_expiry']
```

## `ObservationMode`

```python
ObservationMode = typing.Literal['continuous', 'scheduled']
```

## `OptionType`

```python
OptionType = typing.Literal['call', 'put']
```

## `PayoffType`

```python
PayoffType = typing.Literal['cash', 'asset']
```

## `PhoenixOption`

```python
PhoenixOption(self, *, coupon_rate: float, initial_spot: float, knock_in_level: float, upper_strike: float, lower_strike: float, knock_in_observation_mode: typing.Literal['every_trading_day', 'at_expiry'], barrier_state: typing.Literal['none', 'knocked_out', 'knocked_in'] | None = None, principal_ratio: float = 1.0, effective_date: datetime.date, expiry_date: datetime.date, observations: collections.abc.Iterable[AutocallableObservation]) -> None
```

Immutable validated Phoenix autocallable option.

### Constructor

Create a validated Phoenix option.

#### Parameters

- **`observations`** (`iterable[AutocallableObservation]`) — Ordered contractual observations at 00:00 UTC.
- **`coupon_rate`** (`float`) — Annualized coupon rate, accrued from the previous observation (the effective date for the first coupon) using Actual/365 Fixed, in principal-ratio units.
- **`initial_spot`** (`float`) — Positive reference spot.
- **`knock_in_level`** (`float`) — Lower knock-in barrier level.
- **`upper_strike, lower_strike`** (`float`) — Terminal participation strikes.
- **`knock_in_observation_mode`** (`{'every_trading_day', 'at_expiry'}`) — Trading-day or expiry-only knock-in observation rule.
- **`barrier_state`** (`{'none', 'knocked_out', 'knocked_in'} | None, optional`) — State before valuation; required after an observation has occurred.
- **`principal_ratio`** (`float, optional`) — Principal repayment component in normalized payoff units; coupons are separate.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates, each anchored at 00:00 UTC.
#### Raises

- `TypeError` — If an argument or sequence element has an incompatible representation.
- `KiyosiError` — If the core rejects the rates, levels, schedule, state, or dates.

### `coupon_rate`

Annualized coupon rate per observation period (Actual/365 Fixed).

### `coupon_barrier_levels`

Coupon barrier level for each observation date.

### `observations`

Owning copy of the complete observation records.

### `knock_out_levels`

Knock-out level for each observation date.

### `observation_dates`

Copy of the ordered observation dates.

### `principal_ratio`

Normalized principal repayment component; coupons and downside are separate.

### `barrier_state`

State before valuation, or None when not supplied.

### `effective_date`

First date on which the note is effective.

### `expiry_date`

Note expiry date.

### `initial_spot`

Reference spot used to define relative terms.

### `upper_strike`

Upper terminal participation strike.

### `lower_strike`

Lower terminal participation strike.

### `knock_in_level`

Lower knock-in barrier level.

### `knock_in_observation_mode`

Trading-day or expiry-only knock-in observation rule.

## `RebateTiming`

```python
RebateTiming = typing.Literal['at_hit', 'at_expiry']
```

## `SettlementTiming`

```python
SettlementTiming = typing.Literal['at_hit', 'at_expiry']
```

## `SnowballOption`

```python
SnowballOption(self, *, maturity_coupon_rate: float, initial_spot: float, knock_in_level: float, upper_strike: float, lower_strike: float, knock_in_observation_mode: typing.Literal['every_trading_day', 'at_expiry'], barrier_state: typing.Literal['none', 'knocked_out', 'knocked_in'] | None = None, principal_ratio: float = 1.0, effective_date: datetime.date, expiry_date: datetime.date, observations: collections.abc.Iterable[AutocallableObservation]) -> None
```

Immutable validated snowball option.

### Constructor

Create a validated snowball option.

Provide observations as AutocallableObservation records. Use autocallable_observations
to associate parallel sequences before construction. Domain validation runs in the core.

#### Parameters

- **`observations`** (`iterable[AutocallableObservation]`) — Ordered contractual observations at 00:00 UTC.
- **`maturity_coupon_rate`** (`float`) — Annualized coupon rate used at maturity when applicable.
- **`initial_spot`** (`float`) — Positive reference spot.
- **`knock_in_level`** (`float`) — Lower knock-in barrier level.
- **`upper_strike, lower_strike`** (`float`) — Terminal participation strikes.
- **`knock_in_observation_mode`** (`{'every_trading_day', 'at_expiry'}`) — Trading-day or expiry-only knock-in observation rule.
- **`barrier_state`** (`{'none', 'knocked_out', 'knocked_in'} | None, optional`) — State before valuation; required after an observation has occurred.
- **`principal_ratio`** (`float, optional`) — Normalized principal repayment component; coupons and downside are separate.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates, each anchored at 00:00 UTC.
#### Raises

- `TypeError` — If an argument or sequence element has an incompatible representation.
- `KiyosiError` — If the core rejects the rates, levels, schedule, state, or dates.

### `knock_out_coupon_rates`

Annualized coupon rate for each observation date.

### `maturity_coupon_rate`

Annualized coupon rate used at maturity when applicable.

### `observations`

Owning copy of the complete observation records.

### `knock_out_levels`

Knock-out level for each observation date.

### `observation_dates`

Copy of the ordered observation dates.

### `principal_ratio`

Normalized principal repayment component; coupons and downside are separate.

### `barrier_state`

State before valuation, or None when not supplied.

### `effective_date`

First date on which the note is effective.

### `expiry_date`

Note expiry date.

### `initial_spot`

Reference spot used to define relative terms.

### `upper_strike`

Upper terminal participation strike.

### `lower_strike`

Lower terminal participation strike.

### `knock_in_level`

Lower knock-in barrier level.

### `knock_in_observation_mode`

Trading-day or expiry-only knock-in observation rule.

## `TernarySnowballOption`

```python
TernarySnowballOption(self, *, maturity_coupon_rate: float, minimum_coupon_rate: float, knock_in_level: float, knock_in_observation_mode: typing.Literal['every_trading_day', 'at_expiry'], barrier_state: typing.Literal['none', 'knocked_out', 'knocked_in'] | None = None, principal_ratio: float = 1.0, effective_date: datetime.date, expiry_date: datetime.date, observations: collections.abc.Iterable[AutocallableObservation]) -> None
```

Immutable validated ternary snowball option.

### Constructor

Create a validated ternary snowball option.

Provide observations as AutocallableObservation records. Use autocallable_observations
to associate parallel sequences before construction. Domain validation runs in the core.

#### Parameters

- **`observations`** (`iterable[AutocallableObservation]`) — Ordered contractual observations at 00:00 UTC.
- **`maturity_coupon_rate`** (`float`) — Annualized coupon rate used at maturity when applicable.
- **`minimum_coupon_rate`** (`float`) — Minimum annualized coupon rate for the third payoff region.
- **`knock_in_level`** (`float`) — Lower knock-in barrier level.
- **`knock_in_observation_mode`** (`{'every_trading_day', 'at_expiry'}`) — Trading-day or expiry-only knock-in observation rule.
- **`barrier_state`** (`{'none', 'knocked_out', 'knocked_in'} | None, optional`) — State before valuation; required after an observation has occurred.
- **`principal_ratio`** (`float, optional`) — Normalized principal repayment component; coupons and downside are separate.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates, each anchored at 00:00 UTC.
#### Raises

- `TypeError` — If an argument or sequence element has an incompatible representation.
- `KiyosiError` — If the core rejects the rates, levels, schedule, state, or dates.

### `knock_out_coupon_rates`

Annualized coupon rate for each observation date.

### `maturity_coupon_rate`

Annualized coupon rate used at maturity when applicable.

### `minimum_coupon_rate`

Minimum annualized coupon rate for the third payoff region.

### `observations`

Owning copy of the complete observation records.

### `knock_out_levels`

Knock-out level for each observation date.

### `observation_dates`

Copy of the ordered observation dates.

### `principal_ratio`

Normalized principal repayment component; coupons and downside are separate.

### `barrier_state`

State before valuation, or None when not supplied.

### `effective_date`

First date on which the note is effective.

### `expiry_date`

Note expiry date.

### `knock_in_level`

Lower knock-in barrier level.

### `knock_in_observation_mode`

Trading-day or expiry-only knock-in observation rule.

## `TouchOption`

Immutable validated one-touch or no-touch option.

Instances are created by the ``cash_*_touch_*`` and ``asset_*_touch_*``
factory functions.

### `effective_date`

First date on which the contract is effective.

### `expiry_date`

Contract expiry at 00:00 UTC.

### `barrier_level`

Positive barrier level.

### `is_one_touch`

Whether hitting the barrier activates the payoff.

### `is_up`

Whether the contract uses an upper barrier.

### `payoff_type`

Cash or asset delivery form.

### `payout`

Cash payout, or None for an asset payoff.

### `settlement_timing`

Settlement time for a one-touch payoff.

### `observation_mode`

Continuous or scheduled monitoring mode.

### `touch_state`

Barrier touch history before valuation.

### `observation_dates`

Copy of the scheduled observations at 00:00 UTC.

## `asset_binary_barrier_option`

```python
asset_binary_barrier_option(*, option_type: typing.Literal['call', 'put'], strike: float, effective_date: datetime.date, expiry_date: datetime.date, barrier_level: float, barrier_type: typing.Literal['up_and_in', 'up_and_out', 'down_and_in', 'down_and_out'], observation_mode: typing.Literal['continuous', 'scheduled'] = 'continuous', observation_dates: collections.abc.Iterable[datetime.date] = (), touch_state: typing.Literal['untouched', 'touched'] | None = None) -> BinaryBarrierOption
```

Create an asset-or-nothing binary barrier option.

#### Parameters

- **`option_type`** (`{'call', 'put'}`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive strike price.
- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates, each anchored at 00:00 UTC.
- **`barrier_level`** (`float`) — Positive barrier level.
- **`barrier_type`** (`{'up_and_in', 'up_and_out', 'down_and_in', 'down_and_out'}`) — Barrier direction and activation behavior.
- **`observation_mode`** (`{'continuous', 'scheduled'}, optional`) — Continuous or scheduled monitoring.
- **`observation_dates`** (`iterable[datetime.date], optional`) — Required schedule for scheduled monitoring.
- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — History strictly before valuation. Required once prior monitoring was possible.
#### Returns

- `BinaryBarrierOption` — Validated immutable asset binary barrier option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the payoff, barrier, dates, or observation schedule.

## `asset_no_touch_down`

```python
asset_no_touch_down(*, effective_date: datetime.date, expiry_date: datetime.date, barrier_level: float, observation_mode: typing.Literal['continuous', 'scheduled'] = 'continuous', observation_dates: collections.abc.Iterable[datetime.date] = (), touch_state: typing.Literal['untouched', 'touched'] | None = None) -> TouchOption
```

Create an asset no-touch option.

The factory name selects an upper or lower barrier. No-touch payoffs settle at
expiry.
``touch_state`` describes observations before the valuation time.

#### Parameters

- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates, each anchored at 00:00 UTC.
- **`barrier_level`** (`float`) — Positive barrier level.
- **`observation_mode`** (`{'continuous', 'scheduled'}, optional`) — Continuous or scheduled monitoring.
- **`observation_dates`** (`iterable[datetime.date], optional`) — Required schedule for scheduled monitoring.
- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — History strictly before valuation. Required once prior monitoring was possible.
#### Returns

- `TouchOption` — Validated immutable asset no-touch option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the barrier, dates, or observation schedule.

## `asset_no_touch_up`

```python
asset_no_touch_up(*, effective_date: datetime.date, expiry_date: datetime.date, barrier_level: float, observation_mode: typing.Literal['continuous', 'scheduled'] = 'continuous', observation_dates: collections.abc.Iterable[datetime.date] = (), touch_state: typing.Literal['untouched', 'touched'] | None = None) -> TouchOption
```

Create an asset no-touch option.

The factory name selects an upper or lower barrier. No-touch payoffs settle at
expiry.
``touch_state`` describes observations before the valuation time.

#### Parameters

- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates, each anchored at 00:00 UTC.
- **`barrier_level`** (`float`) — Positive barrier level.
- **`observation_mode`** (`{'continuous', 'scheduled'}, optional`) — Continuous or scheduled monitoring.
- **`observation_dates`** (`iterable[datetime.date], optional`) — Required schedule for scheduled monitoring.
- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — History strictly before valuation. Required once prior monitoring was possible.
#### Returns

- `TouchOption` — Validated immutable asset no-touch option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the barrier, dates, or observation schedule.

## `asset_one_touch_down`

```python
asset_one_touch_down(*, effective_date: datetime.date, expiry_date: datetime.date, barrier_level: float, settlement_timing: typing.Literal['at_hit', 'at_expiry'] = 'at_expiry', observation_mode: typing.Literal['continuous', 'scheduled'] = 'continuous', observation_dates: collections.abc.Iterable[datetime.date] = (), touch_state: typing.Literal['untouched', 'touched'] | None = None) -> TouchOption
```

Create an asset one-touch option.

The factory name selects an upper or lower barrier.
``touch_state`` describes observations before the valuation time.

#### Parameters

- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates, each anchored at 00:00 UTC.
- **`barrier_level`** (`float`) — Positive barrier level.
- **`settlement_timing`** (`{'at_hit', 'at_expiry'}, optional`) — Settle at the barrier hit or at expiry.
- **`observation_mode`** (`{'continuous', 'scheduled'}, optional`) — Continuous or scheduled monitoring.
- **`observation_dates`** (`iterable[datetime.date], optional`) — Required schedule for scheduled monitoring.
- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — History strictly before valuation. Required once prior monitoring was possible.
#### Returns

- `TouchOption` — Validated immutable asset one-touch option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the barrier, dates, or observation schedule.

## `asset_one_touch_up`

```python
asset_one_touch_up(*, effective_date: datetime.date, expiry_date: datetime.date, barrier_level: float, settlement_timing: typing.Literal['at_hit', 'at_expiry'] = 'at_expiry', observation_mode: typing.Literal['continuous', 'scheduled'] = 'continuous', observation_dates: collections.abc.Iterable[datetime.date] = (), touch_state: typing.Literal['untouched', 'touched'] | None = None) -> TouchOption
```

Create an asset one-touch option.

The factory name selects an upper or lower barrier.
``touch_state`` describes observations before the valuation time.

#### Parameters

- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates, each anchored at 00:00 UTC.
- **`barrier_level`** (`float`) — Positive barrier level.
- **`settlement_timing`** (`{'at_hit', 'at_expiry'}, optional`) — Settle at the barrier hit or at expiry.
- **`observation_mode`** (`{'continuous', 'scheduled'}, optional`) — Continuous or scheduled monitoring.
- **`observation_dates`** (`iterable[datetime.date], optional`) — Required schedule for scheduled monitoring.
- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — History strictly before valuation. Required once prior monitoring was possible.
#### Returns

- `TouchOption` — Validated immutable asset one-touch option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the barrier, dates, or observation schedule.

## `autocallable_observations`

```python
autocallable_observations(observation_dates: collections.abc.Iterable[datetime.date], knock_out_levels: collections.abc.Iterable[float], *, knock_out_coupon_rates: collections.abc.Iterable[float] | None = None, coupon_barrier_levels: collections.abc.Iterable[float] | None = None) -> list[AutocallableObservation]
```

Associate parallel sequences into owning observation records.

Dates, knock-out levels, and supplied coupon sequences must have equal lengths.
Omitted coupon sequences use the core record defaults. Dates and contractual
values are validated when an autocallable note is constructed from the records.

#### Raises

- `TypeError` — If a sequence or element has an incompatible representation.
- `KiyosiError` — With category INVALID_SCHEDULE if sequence lengths differ.

## `both_down_snowball`

```python
both_down_snowball(*, initial_coupon_rate: float, coupon_rate_decrement: float, initial_spot: float, knock_in_level: float, initial_knock_out_level: float, knock_out_level_decrement: float, observation_dates: collections.abc.Iterable[datetime.date], effective_date: datetime.date, expiry_date: datetime.date, barrier_state: typing.Literal['none', 'knocked_out', 'knocked_in'] | None = None, principal_ratio: float = 1.0) -> SnowballOption
```

Create a snowball with decreasing coupons and knock-out barriers.

#### Parameters

- **`initial_coupon_rate`** (`float`) — Annualized coupon rate at the first observation.
- **`coupon_rate_decrement`** (`float`) — Amount subtracted from each successive coupon rate.
- **`initial_spot`** (`float`) — Positive reference spot.
- **`knock_in_level`** (`float`) — Lower knock-in barrier level.
- **`initial_knock_out_level`** (`float`) — Knock-out level at the first observation.
- **`knock_out_level_decrement`** (`float`) — Amount subtracted from each successive knock-out level.
- **`observation_dates`** (`iterable[datetime.date]`) — Ordered knock-out observations at 00:00 UTC.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates, each anchored at 00:00 UTC.
- **`barrier_state`** (`{'none', 'knocked_out', 'knocked_in'} | None, optional`) — State before valuation; required after an observation has occurred.
- **`principal_ratio`** (`float, optional`) — Normalized principal repayment component; coupons and downside are separate.
#### Returns

- `SnowballOption` — Validated immutable snowball option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the rates, levels, schedule, state, or dates.

## `cash_binary_barrier_option`

```python
cash_binary_barrier_option(*, option_type: typing.Literal['call', 'put'], strike: float, effective_date: datetime.date, expiry_date: datetime.date, barrier_level: float, barrier_type: typing.Literal['up_and_in', 'up_and_out', 'down_and_in', 'down_and_out'], payout: float, observation_mode: typing.Literal['continuous', 'scheduled'] = 'continuous', observation_dates: collections.abc.Iterable[datetime.date] = (), touch_state: typing.Literal['untouched', 'touched'] | None = None) -> BinaryBarrierOption
```

Create a cash-or-nothing binary barrier option.

#### Parameters

- **`option_type`** (`{'call', 'put'}`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive strike price.
- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates, each anchored at 00:00 UTC.
- **`barrier_level`** (`float`) — Positive barrier level.
- **`barrier_type`** (`{'up_and_in', 'up_and_out', 'down_and_in', 'down_and_out'}`) — Barrier direction and activation behavior.
- **`payout`** (`float`) — Fixed cash amount paid when the payoff and barrier conditions hold.
- **`observation_mode`** (`{'continuous', 'scheduled'}, optional`) — Continuous or scheduled monitoring.
- **`observation_dates`** (`iterable[datetime.date], optional`) — Required schedule for scheduled monitoring.
- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — History strictly before valuation. Required once prior monitoring was possible.
#### Returns

- `BinaryBarrierOption` — Validated immutable cash binary barrier option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the payoff, barrier, dates, or observation schedule.

## `cash_no_touch_down`

```python
cash_no_touch_down(*, effective_date: datetime.date, expiry_date: datetime.date, barrier_level: float, payout: float, observation_mode: typing.Literal['continuous', 'scheduled'] = 'continuous', observation_dates: collections.abc.Iterable[datetime.date] = (), touch_state: typing.Literal['untouched', 'touched'] | None = None) -> TouchOption
```

Create a cash no-touch option.

The factory name selects an upper or lower barrier. No-touch payoffs settle at
expiry.
``touch_state`` describes observations before the valuation time.

#### Parameters

- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates, each anchored at 00:00 UTC.
- **`barrier_level`** (`float`) — Positive barrier level.
- **`payout`** (`float`) — Fixed cash payout.
- **`observation_mode`** (`{'continuous', 'scheduled'}, optional`) — Continuous or scheduled monitoring.
- **`observation_dates`** (`iterable[datetime.date], optional`) — Required schedule for scheduled monitoring.
- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — History strictly before valuation. Required once prior monitoring was possible.
#### Returns

- `TouchOption` — Validated immutable cash no-touch option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the payoff, barrier, dates, or observation schedule.

## `cash_no_touch_up`

```python
cash_no_touch_up(*, effective_date: datetime.date, expiry_date: datetime.date, barrier_level: float, payout: float, observation_mode: typing.Literal['continuous', 'scheduled'] = 'continuous', observation_dates: collections.abc.Iterable[datetime.date] = (), touch_state: typing.Literal['untouched', 'touched'] | None = None) -> TouchOption
```

Create a cash no-touch option.

The factory name selects an upper or lower barrier. No-touch payoffs settle at
expiry.
``touch_state`` describes observations before the valuation time.

#### Parameters

- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates, each anchored at 00:00 UTC.
- **`barrier_level`** (`float`) — Positive barrier level.
- **`payout`** (`float`) — Fixed cash payout.
- **`observation_mode`** (`{'continuous', 'scheduled'}, optional`) — Continuous or scheduled monitoring.
- **`observation_dates`** (`iterable[datetime.date], optional`) — Required schedule for scheduled monitoring.
- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — History strictly before valuation. Required once prior monitoring was possible.
#### Returns

- `TouchOption` — Validated immutable cash no-touch option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the payoff, barrier, dates, or observation schedule.

## `cash_one_touch_down`

```python
cash_one_touch_down(*, effective_date: datetime.date, expiry_date: datetime.date, barrier_level: float, payout: float, settlement_timing: typing.Literal['at_hit', 'at_expiry'] = 'at_expiry', observation_mode: typing.Literal['continuous', 'scheduled'] = 'continuous', observation_dates: collections.abc.Iterable[datetime.date] = (), touch_state: typing.Literal['untouched', 'touched'] | None = None) -> TouchOption
```

Create a cash one-touch option.

The factory name selects an upper or lower barrier.
``touch_state`` describes observations before the valuation time.

#### Parameters

- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates, each anchored at 00:00 UTC.
- **`barrier_level`** (`float`) — Positive barrier level.
- **`payout`** (`float`) — Fixed cash payout.
- **`settlement_timing`** (`{'at_hit', 'at_expiry'}, optional`) — Settle at the barrier hit or at expiry.
- **`observation_mode`** (`{'continuous', 'scheduled'}, optional`) — Continuous or scheduled monitoring.
- **`observation_dates`** (`iterable[datetime.date], optional`) — Required schedule for scheduled monitoring.
- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — History strictly before valuation. Required once prior monitoring was possible.
#### Returns

- `TouchOption` — Validated immutable cash one-touch option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the payoff, barrier, dates, or observation schedule.

## `cash_one_touch_up`

```python
cash_one_touch_up(*, effective_date: datetime.date, expiry_date: datetime.date, barrier_level: float, payout: float, settlement_timing: typing.Literal['at_hit', 'at_expiry'] = 'at_expiry', observation_mode: typing.Literal['continuous', 'scheduled'] = 'continuous', observation_dates: collections.abc.Iterable[datetime.date] = (), touch_state: typing.Literal['untouched', 'touched'] | None = None) -> TouchOption
```

Create a cash one-touch option.

The factory name selects an upper or lower barrier.
``touch_state`` describes observations before the valuation time.

#### Parameters

- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates, each anchored at 00:00 UTC.
- **`barrier_level`** (`float`) — Positive barrier level.
- **`payout`** (`float`) — Fixed cash payout.
- **`settlement_timing`** (`{'at_hit', 'at_expiry'}, optional`) — Settle at the barrier hit or at expiry.
- **`observation_mode`** (`{'continuous', 'scheduled'}, optional`) — Continuous or scheduled monitoring.
- **`observation_dates`** (`iterable[datetime.date], optional`) — Required schedule for scheduled monitoring.
- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — History strictly before valuation. Required once prior monitoring was possible.
#### Returns

- `TouchOption` — Validated immutable cash one-touch option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the payoff, barrier, dates, or observation schedule.

## `dual_coupon_snowball`

```python
dual_coupon_snowball(*, knock_out_coupon_rate: float, maturity_coupon_rate: float, initial_spot: float, knock_in_level: float, knock_out_level: float, observation_dates: collections.abc.Iterable[datetime.date], effective_date: datetime.date, expiry_date: datetime.date, barrier_state: typing.Literal['none', 'knocked_out', 'knocked_in'] | None = None, principal_ratio: float = 1.0) -> SnowballOption
```

Create a snowball with separate knock-out and maturity coupons.

#### Parameters

- **`knock_out_coupon_rate`** (`float`) — Annualized coupon rate paid after knock-out.
- **`maturity_coupon_rate`** (`float`) — Annualized coupon rate paid at maturity when applicable.
- **`initial_spot`** (`float`) — Positive reference spot.
- **`knock_in_level`** (`float`) — Lower knock-in barrier level.
- **`knock_out_level`** (`float`) — Knock-out level applied to every observation.
- **`observation_dates`** (`iterable[datetime.date]`) — Ordered knock-out observations at 00:00 UTC.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates, each anchored at 00:00 UTC.
- **`barrier_state`** (`{'none', 'knocked_out', 'knocked_in'} | None, optional`) — State before valuation; required after an observation has occurred.
- **`principal_ratio`** (`float, optional`) — Normalized principal repayment component; coupons and downside are separate.
#### Returns

- `SnowballOption` — Validated immutable snowball option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the rates, levels, schedule, state, or dates.

## `european_snowball`

```python
european_snowball(*, coupon_rate: float, initial_spot: float, knock_in_level: float, knock_out_level: float, observation_dates: collections.abc.Iterable[datetime.date], effective_date: datetime.date, expiry_date: datetime.date, barrier_state: typing.Literal['none', 'knocked_out', 'knocked_in'] | None = None, principal_ratio: float = 1.0) -> SnowballOption
```

Create a standard or European snowball preset.

The called factory determines whether the knock-in barrier is observed every
trading day or only at expiry.

#### Parameters

- **`coupon_rate`** (`float`) — Annualized coupon rate used for knock-out and maturity coupons.
- **`initial_spot`** (`float`) — Positive reference spot.
- **`knock_in_level`** (`float`) — Lower knock-in barrier level.
- **`knock_out_level`** (`float`) — Knock-out level applied to every observation.
- **`observation_dates`** (`iterable[datetime.date]`) — Ordered knock-out observations at 00:00 UTC.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates, each anchored at 00:00 UTC.
- **`barrier_state`** (`{'none', 'knocked_out', 'knocked_in'} | None, optional`) — State before valuation; required after an observation has occurred.
- **`principal_ratio`** (`float, optional`) — Normalized principal repayment component; coupons and downside are separate.
#### Returns

- `SnowballOption` — Validated immutable snowball option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the rates, levels, schedule, state, or dates.

## `loss_capped_snowball`

```python
loss_capped_snowball(*, coupon_rate: float, initial_spot: float, knock_in_level: float, knock_out_level: float, lower_strike: float, observation_dates: collections.abc.Iterable[datetime.date], effective_date: datetime.date, expiry_date: datetime.date, barrier_state: typing.Literal['none', 'knocked_out', 'knocked_in'] | None = None, principal_ratio: float = 1.0) -> SnowballOption
```

Create a snowball with a lower loss-capping strike.

#### Parameters

- **`coupon_rate`** (`float`) — Annualized coupon rate.
- **`initial_spot`** (`float`) — Positive reference spot.
- **`knock_in_level`** (`float`) — Lower knock-in barrier level.
- **`knock_out_level`** (`float`) — Knock-out level applied to every observation.
- **`lower_strike`** (`float`) — Lower terminal strike that caps downside loss.
- **`observation_dates`** (`iterable[datetime.date]`) — Ordered knock-out observations at 00:00 UTC.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates, each anchored at 00:00 UTC.
- **`barrier_state`** (`{'none', 'knocked_out', 'knocked_in'} | None, optional`) — State before valuation; required after an observation has occurred.
- **`principal_ratio`** (`float, optional`) — Normalized principal repayment component; coupons and downside are separate.
#### Returns

- `SnowballOption` — Validated immutable loss-capped snowball option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the rates, levels, schedule, state, or dates.

## `otm_snowball`

```python
otm_snowball(*, coupon_rate: float, initial_spot: float, knock_in_level: float, knock_out_level: float, upper_strike: float, observation_dates: collections.abc.Iterable[datetime.date], effective_date: datetime.date, expiry_date: datetime.date, barrier_state: typing.Literal['none', 'knocked_out', 'knocked_in'] | None = None, principal_ratio: float = 1.0) -> SnowballOption
```

Create a snowball with a custom upper terminal strike.

#### Parameters

- **`coupon_rate`** (`float`) — Annualized coupon rate.
- **`initial_spot`** (`float`) — Positive reference spot.
- **`knock_in_level`** (`float`) — Lower knock-in barrier level.
- **`knock_out_level`** (`float`) — Knock-out level applied to every observation.
- **`upper_strike`** (`float`) — Upper terminal participation strike.
- **`observation_dates`** (`iterable[datetime.date]`) — Ordered knock-out observations at 00:00 UTC.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates, each anchored at 00:00 UTC.
- **`barrier_state`** (`{'none', 'knocked_out', 'knocked_in'} | None, optional`) — State before valuation; required after an observation has occurred.
- **`principal_ratio`** (`float, optional`) — Normalized principal repayment component; coupons and downside are separate.
#### Returns

- `SnowballOption` — Validated immutable out-of-the-money snowball option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the rates, levels, schedule, state, or dates.

## `parachute_snowball`

```python
parachute_snowball(*, coupon_rate: float, initial_spot: float, knock_in_level: float, knock_out_level: float, final_knock_out_level: float, observation_dates: collections.abc.Iterable[datetime.date], effective_date: datetime.date, expiry_date: datetime.date, barrier_state: typing.Literal['none', 'knocked_out', 'knocked_in'] | None = None, principal_ratio: float = 1.0) -> SnowballOption
```

Create a snowball with a distinct final knock-out barrier.

#### Parameters

- **`coupon_rate`** (`float`) — Annualized coupon rate.
- **`initial_spot`** (`float`) — Positive reference spot.
- **`knock_in_level`** (`float`) — Lower knock-in barrier level.
- **`knock_out_level`** (`float`) — Knock-out level before the final observation.
- **`final_knock_out_level`** (`float`) — Knock-out level at the final observation.
- **`observation_dates`** (`iterable[datetime.date]`) — Ordered knock-out observations at 00:00 UTC.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates, each anchored at 00:00 UTC.
- **`barrier_state`** (`{'none', 'knocked_out', 'knocked_in'} | None, optional`) — State before valuation; required after an observation has occurred.
- **`principal_ratio`** (`float, optional`) — Normalized principal repayment component; coupons and downside are separate.
#### Returns

- `SnowballOption` — Validated immutable snowball option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the rates, levels, schedule, state, or dates.

## `standard_snowball`

```python
standard_snowball(*, coupon_rate: float, initial_spot: float, knock_in_level: float, knock_out_level: float, observation_dates: collections.abc.Iterable[datetime.date], effective_date: datetime.date, expiry_date: datetime.date, barrier_state: typing.Literal['none', 'knocked_out', 'knocked_in'] | None = None, principal_ratio: float = 1.0) -> SnowballOption
```

Create a standard or European snowball preset.

The called factory determines whether the knock-in barrier is observed every
trading day or only at expiry.

#### Parameters

- **`coupon_rate`** (`float`) — Annualized coupon rate used for knock-out and maturity coupons.
- **`initial_spot`** (`float`) — Positive reference spot.
- **`knock_in_level`** (`float`) — Lower knock-in barrier level.
- **`knock_out_level`** (`float`) — Knock-out level applied to every observation.
- **`observation_dates`** (`iterable[datetime.date]`) — Ordered knock-out observations at 00:00 UTC.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates, each anchored at 00:00 UTC.
- **`barrier_state`** (`{'none', 'knocked_out', 'knocked_in'} | None, optional`) — State before valuation; required after an observation has occurred.
- **`principal_ratio`** (`float, optional`) — Normalized principal repayment component; coupons and downside are separate.
#### Returns

- `SnowballOption` — Validated immutable snowball option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the rates, levels, schedule, state, or dates.

## `step_down_snowball`

```python
step_down_snowball(*, coupon_rate: float, initial_spot: float, knock_in_level: float, initial_knock_out_level: float, knock_out_level_decrement: float, observation_dates: collections.abc.Iterable[datetime.date], effective_date: datetime.date, expiry_date: datetime.date, barrier_state: typing.Literal['none', 'knocked_out', 'knocked_in'] | None = None, principal_ratio: float = 1.0) -> SnowballOption
```

Create a snowball with linearly decreasing knock-out barriers.

#### Parameters

- **`coupon_rate`** (`float`) — Annualized coupon rate.
- **`initial_spot`** (`float`) — Positive reference spot.
- **`knock_in_level`** (`float`) — Lower knock-in barrier level.
- **`initial_knock_out_level`** (`float`) — Knock-out level at the first observation.
- **`knock_out_level_decrement`** (`float`) — Amount subtracted from each successive knock-out level.
- **`observation_dates`** (`iterable[datetime.date]`) — Ordered knock-out observations at 00:00 UTC.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates, each anchored at 00:00 UTC.
- **`barrier_state`** (`{'none', 'knocked_out', 'knocked_in'} | None, optional`) — State before valuation; required after an observation has occurred.
- **`principal_ratio`** (`float, optional`) — Normalized principal repayment component; coupons and downside are separate.
#### Returns

- `SnowballOption` — Validated immutable snowball option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the rates, levels, schedule, state, or dates.
