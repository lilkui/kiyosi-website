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

#### Attributes

- **`strike`** (`float`) — Positive purchase strike.
- **`knock_out_level`** (`float`) — Positive upper knock-out level.
- **`daily_quantity`** (`float`) — Base quantity accumulated per trading day.
- **`acceleration_factor`** (`float`) — Quantity multiplier applied below the strike.
- **`accumulated_quantity`** (`float`) — Quantity already accumulated at valuation.
- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates.

### Constructor

Create a validated accumulator contract.

#### Parameters

- **`strike`** (`float`) — Positive purchase strike.
- **`knock_out_level`** (`float`) — Positive upper knock-out level.
- **`daily_quantity`** (`float`) — Non-negative base quantity accumulated per trading day.
- **`acceleration_factor`** (`float`) — Non-negative quantity multiplier below the strike.
- **`accumulated_quantity`** (`float, optional`) — Non-negative quantity already accumulated at valuation.
- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates.
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

Contract expiry date.

## `AmericanOption`

```python
AmericanOption(self, *, option_type: OptionType, strike: float, effective_date: datetime.date, expiry_date: datetime.date) -> None
```

Immutable validated American vanilla option.

The payoff may be exercised from the effective date through expiry.

#### Attributes

- **`option_type`** (`OptionType`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive strike price.
- **`effective_date`** (`datetime.date`) — First exercise date.
- **`expiry_date`** (`datetime.date`) — Last exercise date.

### Constructor

Create a validated American option.

#### Parameters

- **`option_type`** (`OptionType`) — Call or put payoff direction.
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

Contract expiry date.

## `ArithmeticAveragePriceOption`

```python
ArithmeticAveragePriceOption(self, *, option_type: OptionType, strike: float, averaging_start_date: datetime.date, effective_date: datetime.date, expiry_date: datetime.date, realized_average: float = 0.0) -> None
```

Immutable validated average-price option.

#### Attributes

- **`option_type`** (`OptionType`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive strike price.
- **`averaging_start_date`** (`datetime.date`) — First date included in the averaging period.
- **`realized_average`** (`float`) — Average realized before the valuation date, or zero before averaging begins.
- **`effective_date`** (`datetime.date`) — First date on which the contract is effective.
- **`expiry_date`** (`datetime.date`) — Contract expiry date.

### Constructor

Create a validated average-price option.

#### Parameters

- **`option_type`** (`OptionType`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive strike price.
- **`averaging_start_date`** (`datetime.date`) — First date included in the averaging period.
- **`effective_date`** (`datetime.date`) — First date on which the contract is effective.
- **`expiry_date`** (`datetime.date`) — Contract expiry date.
- **`realized_average`** (`float, optional`) — Average already realized; defaults to the core-owned pre-averaging value.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the terms or date ordering.

### `option_type`

Call or put payoff direction.

### `strike`

Positive strike price.

### `averaging_start_date`

First date included in the averaging period.

### `realized_average`

Average realized before valuation.

### `effective_date`

First date on which the contract is effective.

### `expiry_date`

Contract expiry date.

## `AssetOrNothingOption`

```python
AssetOrNothingOption(self, *, option_type: OptionType, strike: float, effective_date: datetime.date, expiry_date: datetime.date) -> None
```

Immutable validated asset-or-nothing digital option.

#### Attributes

- **`option_type`** (`OptionType`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive strike price.
- **`effective_date`** (`datetime.date`) — First date on which the contract is effective.
- **`expiry_date`** (`datetime.date`) — Contract expiry date.

### Constructor

Create a validated asset-or-nothing option.

#### Parameters

- **`option_type`** (`OptionType`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive strike price.
- **`effective_date`** (`datetime.date`) — First date on which the contract is effective.
- **`expiry_date`** (`datetime.date`) — Contract expiry date.
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

Contract expiry date.

## `AutocallableBarrierState`

Barrier history known at valuation time.

#### Attributes

- `NONE` — No barrier event has occurred.
- `KNOCKED_OUT` — The instrument has already knocked out.
- `KNOCKED_IN` — The knock-in barrier has already been breached.

### Values

- `NONE` = `0`
- `KNOCKED_OUT` = `1`
- `KNOCKED_IN` = `2`

## `BarrierOption`

```python
BarrierOption(self, *, option_type: OptionType, strike: float, effective_date: datetime.date, expiry_date: datetime.date, barrier_level: float, barrier_type: BarrierType, rebate: float = 0.0, rebate_timing: RebateTiming = RebateTiming.AT_EXPIRY, observation_mode: ObservationMode = ObservationMode.CONTINUOUS, observation_dates: collections.abc.Iterable[datetime.date] = ()) -> None
```

Immutable validated barrier option.

Scheduled barriers are observed only on ``observation_dates``; continuous
barriers require no schedule.

#### Attributes

- **`option_type`** (`OptionType`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive strike price.
- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates.
- **`barrier_level`** (`float`) — Positive barrier level.
- **`barrier_type`** (`BarrierType`) — Barrier direction and knock-in or knock-out behavior.
- **`rebate`** (`float`) — Rebate amount.
- **`rebate_timing`** (`RebateTiming`) — Time at which the rebate is paid.
- **`observation_mode`** (`ObservationMode`) — Continuous or scheduled monitoring.
- **`observation_dates`** (`list[datetime.date]`) — Ordered scheduled monitoring dates.

### Constructor

Create a validated barrier option.

#### Parameters

- **`option_type`** (`OptionType`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive strike price.
- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates.
- **`barrier_level`** (`float`) — Positive barrier level.
- **`barrier_type`** (`BarrierType`) — Barrier direction and knock-in or knock-out behavior.
- **`rebate`** (`float, optional`) — Rebate amount. Uses the core default when omitted.
- **`rebate_timing`** (`RebateTiming, optional`) — Time at which the rebate is paid.
- **`observation_mode`** (`ObservationMode, optional`) — Continuous or scheduled monitoring.
- **`observation_dates`** (`iterable[datetime.date], optional`) — Required schedule for scheduled monitoring; omitted for continuous monitoring.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the payoff, barrier, dates, or observation schedule.

### `option_type`

Call or put payoff direction.

### `strike`

Positive strike price.

### `effective_date`

First date on which the contract is effective.

### `expiry_date`

Contract expiry date.

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

### `observation_dates`

Copy of the ordered scheduled observation dates.

## `BarrierType`

Direction and activation behavior of a barrier.

#### Attributes

- `UP_AND_IN` — Activate when spot reaches an upper barrier.
- `UP_AND_OUT` — Terminate when spot reaches an upper barrier.
- `DOWN_AND_IN` — Activate when spot reaches a lower barrier.
- `DOWN_AND_OUT` — Terminate when spot reaches a lower barrier.

### Values

- `UP_AND_IN` = `0`
- `UP_AND_OUT` = `1`
- `DOWN_AND_IN` = `2`
- `DOWN_AND_OUT` = `3`

## `BinaryBarrierOption`

Immutable validated strike-based binary barrier option.

Instances are created by `cash_binary_barrier_option` or
`asset_binary_barrier_option`.

#### Attributes

- **`option_type`** (`OptionType`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive strike price.
- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates.
- **`barrier_level`** (`float`) — Positive barrier level.
- **`barrier_type`** (`BarrierType`) — Barrier direction and activation behavior.
- **`payoff_type`** (`PayoffType`) — Cash or asset delivery.
- **`payout`** (`float or None`) — Cash payout, or ``None`` for an asset payoff.
- **`observation_mode`** (`ObservationMode`) — Continuous or scheduled monitoring.
- **`observation_dates`** (`list[datetime.date]`) — Ordered scheduled monitoring dates.

### `option_type`

Call or put payoff direction.

### `strike`

Positive strike price.

### `effective_date`

First date on which the contract is effective.

### `expiry_date`

Contract expiry date.

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

### `observation_dates`

Copy of the ordered scheduled observation dates.

## `BinarySnowballOption`

```python
BinarySnowballOption(self, *, knock_out_coupon_rates: collections.abc.Iterable[float], maturity_coupon_rate: float, initial_spot: float, knock_out_levels: collections.abc.Iterable[float], upper_strike: float, lower_strike: float, observation_dates: collections.abc.Iterable[datetime.date], barrier_state: AutocallableBarrierState = AutocallableBarrierState.NONE, principal_ratio: float = 1.0, effective_date: datetime.date, expiry_date: datetime.date) -> None
```

Immutable validated binary snowball option.

#### Attributes

- **`knock_out_coupon_rates`** (`list[float]`) — Annualized coupon rate for each observation date.
- **`maturity_coupon_rate`** (`float`) — Annualized coupon rate used at maturity when applicable.
- **`initial_spot`** (`float`) — Reference spot used to define relative terms.
- **`knock_out_levels`** (`list[float]`) — Knock-out level for each observation date.
- **`upper_strike, lower_strike`** (`float`) — Terminal binary payoff thresholds.
- **`observation_dates`** (`list[datetime.date]`) — Ordered knock-out observation dates.
- **`barrier_state`** (`AutocallableBarrierState`) — Barrier history known at valuation time.
- **`principal_ratio`** (`float`) — Principal scaling applied to the payoff.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates.

### Constructor

Create a validated binary snowball option.

#### Parameters

- **`knock_out_coupon_rates`** (`iterable[float]`) — Annualized coupon rate for each observation date.
- **`maturity_coupon_rate`** (`float`) — Annualized coupon rate used at maturity when applicable.
- **`initial_spot`** (`float`) — Positive reference spot.
- **`knock_out_levels`** (`iterable[float]`) — Knock-out level for each observation date.
- **`upper_strike, lower_strike`** (`float`) — Terminal binary payoff thresholds.
- **`observation_dates`** (`iterable[datetime.date]`) — Ordered knock-out observation dates.
- **`barrier_state`** (`AutocallableBarrierState, optional`) — Barrier history known at valuation time.
- **`principal_ratio`** (`float, optional`) — Principal scaling applied to the payoff.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates.
#### Raises

- `TypeError` — If an argument or sequence element has an incompatible representation.
- `KiyosiError` — If the core rejects the rates, levels, schedule, state, or dates.

### `knock_out_coupon_rates`

Annualized coupon rate for each observation date.

### `maturity_coupon_rate`

Annualized coupon rate used at maturity when applicable.

### `initial_spot`

Reference spot used to define relative terms.

### `knock_out_levels`

Knock-out level for each observation date.

### `upper_strike`

Upper terminal participation strike.

### `lower_strike`

Lower terminal participation strike.

### `observation_dates`

Copy of the ordered observation dates.

### `principal_ratio`

Principal scaling applied to the payoff.

### `barrier_state`

Barrier history known at valuation time.

### `effective_date`

First date on which the note is effective.

### `expiry_date`

Note expiry date.

## `CashOrNothingOption`

```python
CashOrNothingOption(self, *, option_type: OptionType, strike: float, payout: float, effective_date: datetime.date, expiry_date: datetime.date) -> None
```

Immutable validated cash-or-nothing digital option.

#### Attributes

- **`option_type`** (`OptionType`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive strike price.
- **`payout`** (`float`) — Fixed cash amount paid when the option finishes in the money.
- **`effective_date`** (`datetime.date`) — First date on which the contract is effective.
- **`expiry_date`** (`datetime.date`) — Contract expiry date.

### Constructor

Create a validated cash-or-nothing option.

#### Parameters

- **`option_type`** (`OptionType`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive strike price.
- **`payout`** (`float`) — Fixed cash amount paid when the option finishes in the money.
- **`effective_date`** (`datetime.date`) — First date on which the contract is effective.
- **`expiry_date`** (`datetime.date`) — Contract expiry date.
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

Contract expiry date.

## `EuropeanOption`

```python
EuropeanOption(self, *, option_type: OptionType, strike: float, effective_date: datetime.date, expiry_date: datetime.date) -> None
```

Immutable validated European vanilla option.

The payoff can be exercised only at expiry.

#### Attributes

- **`option_type`** (`OptionType`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive strike price.
- **`effective_date`** (`datetime.date`) — First date on which the contract is effective.
- **`expiry_date`** (`datetime.date`) — Contract expiry date.

### Constructor

Create a validated European option.

#### Parameters

- **`option_type`** (`OptionType`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive strike price.
- **`effective_date`** (`datetime.date`) — First date on which the contract is effective.
- **`expiry_date`** (`datetime.date`) — Contract expiry date.
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

Contract expiry date.

## `GeometricAveragePriceOption`

```python
GeometricAveragePriceOption(self, *, option_type: OptionType, strike: float, averaging_start_date: datetime.date, effective_date: datetime.date, expiry_date: datetime.date, realized_average: float = 0.0) -> None
```

Immutable validated average-price option.

#### Attributes

- **`option_type`** (`OptionType`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive strike price.
- **`averaging_start_date`** (`datetime.date`) — First date included in the averaging period.
- **`realized_average`** (`float`) — Average realized before the valuation date, or zero before averaging begins.
- **`effective_date`** (`datetime.date`) — First date on which the contract is effective.
- **`expiry_date`** (`datetime.date`) — Contract expiry date.

### Constructor

Create a validated average-price option.

#### Parameters

- **`option_type`** (`OptionType`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive strike price.
- **`averaging_start_date`** (`datetime.date`) — First date included in the averaging period.
- **`effective_date`** (`datetime.date`) — First date on which the contract is effective.
- **`expiry_date`** (`datetime.date`) — Contract expiry date.
- **`realized_average`** (`float, optional`) — Average already realized; defaults to the core-owned pre-averaging value.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the terms or date ordering.

### `option_type`

Call or put payoff direction.

### `strike`

Positive strike price.

### `averaging_start_date`

First date included in the averaging period.

### `realized_average`

Average realized before valuation.

### `effective_date`

First date on which the contract is effective.

### `expiry_date`

Contract expiry date.

## `KnockInObservationMode`

Observation rule for an autocallable knock-in barrier.

#### Attributes

- `EVERY_TRADING_DAY` — Observe on every trading day through expiry.
- `AT_EXPIRY` — Observe only at expiry.

### Values

- `EVERY_TRADING_DAY` = `0`
- `AT_EXPIRY` = `1`

## `ObservationMode`

Barrier observation frequency.

#### Attributes

- `CONTINUOUS` — Observe throughout the instrument lifetime.
- `SCHEDULED` — Observe only on the supplied observation dates.

### Values

- `CONTINUOUS` = `0`
- `SCHEDULED` = `1`

## `OptionType`

Option payoff direction.

#### Attributes

- `CALL` — Right to benefit from prices above the strike.
- `PUT` — Right to benefit from prices below the strike.

### Values

- `CALL` = `0`
- `PUT` = `1`

## `PayoffType`

Delivery form of a binary payoff.

#### Attributes

- `CASH` — Deliver a fixed cash amount.
- `ASSET` — Deliver the underlying asset value.

### Values

- `CASH` = `0`
- `ASSET` = `1`

## `PhoenixOption`

```python
PhoenixOption(self, *, coupon_rate: float, initial_spot: float, knock_in_level: float, knock_out_levels: collections.abc.Iterable[float], coupon_barrier_levels: collections.abc.Iterable[float], upper_strike: float, lower_strike: float, observation_dates: collections.abc.Iterable[datetime.date], knock_in_observation_mode: KnockInObservationMode, barrier_state: AutocallableBarrierState = AutocallableBarrierState.NONE, principal_ratio: float = 1.0, effective_date: datetime.date, expiry_date: datetime.date) -> None
```

Immutable validated Phoenix autocallable option.

#### Attributes

- **`coupon_rate`** (`float`) — Annualized coupon rate.
- **`coupon_barrier_levels`** (`list[float]`) — Coupon barrier level for each observation date.
- **`initial_spot`** (`float`) — Reference spot used to define relative terms.
- **`knock_in_level`** (`float`) — Lower knock-in barrier level.
- **`knock_out_levels`** (`list[float]`) — Knock-out level for each observation date.
- **`upper_strike, lower_strike`** (`float`) — Terminal participation strikes.
- **`observation_dates`** (`list[datetime.date]`) — Ordered coupon and knock-out observation dates.
- **`knock_in_observation_mode`** (`KnockInObservationMode`) — Trading-day or expiry-only knock-in observation rule.
- **`barrier_state`** (`AutocallableBarrierState`) — Barrier history known at valuation time.
- **`principal_ratio`** (`float`) — Principal scaling applied to the payoff.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates.

### Constructor

Create a validated Phoenix option.

#### Parameters

- **`coupon_rate`** (`float`) — Annualized coupon rate.
- **`initial_spot`** (`float`) — Positive reference spot.
- **`knock_in_level`** (`float`) — Lower knock-in barrier level.
- **`knock_out_levels`** (`iterable[float]`) — Knock-out level for each observation date.
- **`coupon_barrier_levels`** (`iterable[float]`) — Coupon barrier level for each observation date.
- **`upper_strike, lower_strike`** (`float`) — Terminal participation strikes.
- **`observation_dates`** (`iterable[datetime.date]`) — Ordered coupon and knock-out observation dates.
- **`knock_in_observation_mode`** (`KnockInObservationMode`) — Trading-day or expiry-only knock-in observation rule.
- **`barrier_state`** (`AutocallableBarrierState, optional`) — Barrier history known at valuation time.
- **`principal_ratio`** (`float, optional`) — Principal scaling applied to the payoff.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates.
#### Raises

- `TypeError` — If an argument or sequence element has an incompatible representation.
- `KiyosiError` — If the core rejects the rates, levels, schedule, state, or dates.

### `coupon_rate`

Annualized coupon rate.

### `coupon_barrier_levels`

Coupon barrier level for each observation date.

### `initial_spot`

Reference spot used to define relative terms.

### `knock_out_levels`

Knock-out level for each observation date.

### `upper_strike`

Upper terminal participation strike.

### `lower_strike`

Lower terminal participation strike.

### `observation_dates`

Copy of the ordered observation dates.

### `principal_ratio`

Principal scaling applied to the payoff.

### `barrier_state`

Barrier history known at valuation time.

### `effective_date`

First date on which the note is effective.

### `expiry_date`

Note expiry date.

### `knock_in_level`

Lower knock-in barrier level.

### `knock_in_observation_mode`

Trading-day or expiry-only knock-in observation rule.

## `RebateTiming`

Payment time for a barrier-option rebate.

#### Attributes

- `AT_HIT` — Pay when the barrier is hit.
- `AT_EXPIRY` — Pay at expiry.

### Values

- `AT_HIT` = `0`
- `AT_EXPIRY` = `1`

## `SettlementTiming`

Settlement time for a one-touch payoff.

#### Attributes

- `AT_HIT` — Settle when the barrier is hit.
- `AT_EXPIRY` — Settle at expiry.

### Values

- `AT_HIT` = `0`
- `AT_EXPIRY` = `1`

## `SnowballOption`

```python
SnowballOption(self, *, knock_out_coupon_rates: collections.abc.Iterable[float], maturity_coupon_rate: float, initial_spot: float, knock_in_level: float, knock_out_levels: collections.abc.Iterable[float], upper_strike: float, lower_strike: float, observation_dates: collections.abc.Iterable[datetime.date], knock_in_observation_mode: KnockInObservationMode, barrier_state: AutocallableBarrierState = AutocallableBarrierState.NONE, principal_ratio: float = 1.0, effective_date: datetime.date, expiry_date: datetime.date) -> None
```

Immutable validated snowball option.

#### Attributes

- **`knock_out_coupon_rates`** (`list[float]`) — Annualized coupon rate for each observation date.
- **`maturity_coupon_rate`** (`float`) — Annualized coupon rate used at maturity when applicable.
- **`initial_spot`** (`float`) — Reference spot used to define relative terms.
- **`knock_in_level`** (`float`) — Lower knock-in barrier level.
- **`knock_out_levels`** (`list[float]`) — Knock-out level for each observation date.
- **`upper_strike, lower_strike`** (`float`) — Terminal participation strikes.
- **`observation_dates`** (`list[datetime.date]`) — Ordered knock-out observation dates.
- **`knock_in_observation_mode`** (`KnockInObservationMode`) — Trading-day or expiry-only knock-in observation rule.
- **`barrier_state`** (`AutocallableBarrierState`) — Barrier history known at valuation time.
- **`principal_ratio`** (`float`) — Principal scaling applied to the payoff.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates.

### Constructor

Create a validated snowball option.

#### Parameters

- **`knock_out_coupon_rates`** (`iterable[float]`) — Annualized coupon rate for each observation date.
- **`maturity_coupon_rate`** (`float`) — Annualized coupon rate used at maturity when applicable.
- **`initial_spot`** (`float`) — Positive reference spot.
- **`knock_in_level`** (`float`) — Lower knock-in barrier level.
- **`knock_out_levels`** (`iterable[float]`) — Knock-out level for each observation date.
- **`upper_strike, lower_strike`** (`float`) — Terminal participation strikes.
- **`observation_dates`** (`iterable[datetime.date]`) — Ordered knock-out observation dates.
- **`knock_in_observation_mode`** (`KnockInObservationMode`) — Trading-day or expiry-only knock-in observation rule.
- **`barrier_state`** (`AutocallableBarrierState, optional`) — Barrier history known at valuation time.
- **`principal_ratio`** (`float, optional`) — Principal scaling applied to the payoff.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates.
#### Raises

- `TypeError` — If an argument or sequence element has an incompatible representation.
- `KiyosiError` — If the core rejects the rates, levels, schedule, state, or dates.

### `knock_out_coupon_rates`

Annualized coupon rate for each observation date.

### `maturity_coupon_rate`

Annualized coupon rate used at maturity when applicable.

### `initial_spot`

Reference spot used to define relative terms.

### `knock_out_levels`

Knock-out level for each observation date.

### `upper_strike`

Upper terminal participation strike.

### `lower_strike`

Lower terminal participation strike.

### `observation_dates`

Copy of the ordered observation dates.

### `principal_ratio`

Principal scaling applied to the payoff.

### `barrier_state`

Barrier history known at valuation time.

### `effective_date`

First date on which the note is effective.

### `expiry_date`

Note expiry date.

### `knock_in_level`

Lower knock-in barrier level.

### `knock_in_observation_mode`

Trading-day or expiry-only knock-in observation rule.

## `TernarySnowballOption`

```python
TernarySnowballOption(self, *, knock_out_coupon_rates: collections.abc.Iterable[float], maturity_coupon_rate: float, minimum_coupon_rate: float, initial_spot: float, knock_in_level: float, knock_out_levels: collections.abc.Iterable[float], upper_strike: float, lower_strike: float, observation_dates: collections.abc.Iterable[datetime.date], knock_in_observation_mode: KnockInObservationMode, barrier_state: AutocallableBarrierState = AutocallableBarrierState.NONE, principal_ratio: float = 1.0, effective_date: datetime.date, expiry_date: datetime.date) -> None
```

Immutable validated ternary snowball option.

#### Attributes

- **`knock_out_coupon_rates`** (`list[float]`) — Annualized coupon rate for each observation date.
- **`maturity_coupon_rate`** (`float`) — Annualized coupon rate used at maturity when applicable.
- **`minimum_coupon_rate`** (`float`) — Minimum annualized coupon rate for the third payoff region.
- **`initial_spot`** (`float`) — Reference spot used to define relative terms.
- **`knock_in_level`** (`float`) — Lower knock-in barrier level.
- **`knock_out_levels`** (`list[float]`) — Knock-out level for each observation date.
- **`upper_strike, lower_strike`** (`float`) — Terminal payoff thresholds.
- **`observation_dates`** (`list[datetime.date]`) — Ordered knock-out observation dates.
- **`knock_in_observation_mode`** (`KnockInObservationMode`) — Trading-day or expiry-only knock-in observation rule.
- **`barrier_state`** (`AutocallableBarrierState`) — Barrier history known at valuation time.
- **`principal_ratio`** (`float`) — Principal scaling applied to the payoff.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates.

### Constructor

Create a validated ternary snowball option.

#### Parameters

- **`knock_out_coupon_rates`** (`iterable[float]`) — Annualized coupon rate for each observation date.
- **`maturity_coupon_rate`** (`float`) — Annualized coupon rate used at maturity when applicable.
- **`minimum_coupon_rate`** (`float`) — Minimum annualized coupon rate for the third payoff region.
- **`initial_spot`** (`float`) — Positive reference spot.
- **`knock_in_level`** (`float`) — Lower knock-in barrier level.
- **`knock_out_levels`** (`iterable[float]`) — Knock-out level for each observation date.
- **`upper_strike, lower_strike`** (`float`) — Terminal payoff thresholds.
- **`observation_dates`** (`iterable[datetime.date]`) — Ordered knock-out observation dates.
- **`knock_in_observation_mode`** (`KnockInObservationMode`) — Trading-day or expiry-only knock-in observation rule.
- **`barrier_state`** (`AutocallableBarrierState, optional`) — Barrier history known at valuation time.
- **`principal_ratio`** (`float, optional`) — Principal scaling applied to the payoff.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates.
#### Raises

- `TypeError` — If an argument or sequence element has an incompatible representation.
- `KiyosiError` — If the core rejects the rates, levels, schedule, state, or dates.

### `knock_out_coupon_rates`

Annualized coupon rate for each observation date.

### `maturity_coupon_rate`

Annualized coupon rate used at maturity when applicable.

### `minimum_coupon_rate`

Minimum annualized coupon rate for the third payoff region.

### `initial_spot`

Reference spot used to define relative terms.

### `knock_out_levels`

Knock-out level for each observation date.

### `upper_strike`

Upper terminal participation strike.

### `lower_strike`

Lower terminal participation strike.

### `observation_dates`

Copy of the ordered observation dates.

### `principal_ratio`

Principal scaling applied to the payoff.

### `barrier_state`

Barrier history known at valuation time.

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

#### Attributes

- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates.
- **`barrier_level`** (`float`) — Positive barrier level.
- **`is_one_touch`** (`bool`) — Whether hitting the barrier activates rather than cancels the payoff.
- **`is_up`** (`bool`) — Whether the barrier is above the spot direction.
- **`payoff_type`** (`PayoffType`) — Cash or asset delivery.
- **`payout`** (`float or None`) — Cash payout, or ``None`` for an asset payoff.
- **`settlement_timing`** (`SettlementTiming`) — Settlement time for a one-touch payoff.
- **`observation_mode`** (`ObservationMode`) — Continuous or scheduled monitoring.
- **`observation_dates`** (`list[datetime.date]`) — Ordered scheduled monitoring dates.

### `effective_date`

First date on which the contract is effective.

### `expiry_date`

Contract expiry date.

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

### `observation_dates`

Copy of the ordered scheduled observation dates.

## `asset_binary_barrier_option`

```python
asset_binary_barrier_option(*, option_type: OptionType, strike: float, effective_date: datetime.date, expiry_date: datetime.date, barrier_level: float, barrier_type: BarrierType, observation_mode: ObservationMode = ObservationMode.CONTINUOUS, observation_dates: collections.abc.Iterable[datetime.date] = ()) -> BinaryBarrierOption
```

Create an asset-or-nothing binary barrier option.

#### Parameters

- **`option_type`** (`OptionType`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive strike price.
- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates.
- **`barrier_level`** (`float`) — Positive barrier level.
- **`barrier_type`** (`BarrierType`) — Barrier direction and activation behavior.
- **`observation_mode`** (`ObservationMode, optional`) — Continuous or scheduled monitoring.
- **`observation_dates`** (`iterable[datetime.date], optional`) — Required schedule for scheduled monitoring.
#### Returns

- `BinaryBarrierOption` — Validated immutable asset binary barrier option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the payoff, barrier, dates, or observation schedule.

## `asset_no_touch_down`

```python
asset_no_touch_down(*, effective_date: datetime.date, expiry_date: datetime.date, barrier_level: float, observation_mode: ObservationMode = ObservationMode.CONTINUOUS, observation_dates: collections.abc.Iterable[datetime.date] = ()) -> TouchOption
```

Create an asset no-touch option.

The factory name selects an upper or lower barrier. No-touch payoffs settle at
expiry.

#### Parameters

- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates.
- **`barrier_level`** (`float`) — Positive barrier level.
- **`observation_mode`** (`ObservationMode, optional`) — Continuous or scheduled monitoring.
- **`observation_dates`** (`iterable[datetime.date], optional`) — Required schedule for scheduled monitoring.
#### Returns

- `TouchOption` — Validated immutable asset no-touch option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the barrier, dates, or observation schedule.

## `asset_no_touch_up`

```python
asset_no_touch_up(*, effective_date: datetime.date, expiry_date: datetime.date, barrier_level: float, observation_mode: ObservationMode = ObservationMode.CONTINUOUS, observation_dates: collections.abc.Iterable[datetime.date] = ()) -> TouchOption
```

Create an asset no-touch option.

The factory name selects an upper or lower barrier. No-touch payoffs settle at
expiry.

#### Parameters

- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates.
- **`barrier_level`** (`float`) — Positive barrier level.
- **`observation_mode`** (`ObservationMode, optional`) — Continuous or scheduled monitoring.
- **`observation_dates`** (`iterable[datetime.date], optional`) — Required schedule for scheduled monitoring.
#### Returns

- `TouchOption` — Validated immutable asset no-touch option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the barrier, dates, or observation schedule.

## `asset_one_touch_down`

```python
asset_one_touch_down(*, effective_date: datetime.date, expiry_date: datetime.date, barrier_level: float, settlement_timing: SettlementTiming = SettlementTiming.AT_EXPIRY, observation_mode: ObservationMode = ObservationMode.CONTINUOUS, observation_dates: collections.abc.Iterable[datetime.date] = ()) -> TouchOption
```

Create an asset one-touch option.

The factory name selects an upper or lower barrier.

#### Parameters

- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates.
- **`barrier_level`** (`float`) — Positive barrier level.
- **`settlement_timing`** (`SettlementTiming, optional`) — Settle at the barrier hit or at expiry.
- **`observation_mode`** (`ObservationMode, optional`) — Continuous or scheduled monitoring.
- **`observation_dates`** (`iterable[datetime.date], optional`) — Required schedule for scheduled monitoring.
#### Returns

- `TouchOption` — Validated immutable asset one-touch option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the barrier, dates, or observation schedule.

## `asset_one_touch_up`

```python
asset_one_touch_up(*, effective_date: datetime.date, expiry_date: datetime.date, barrier_level: float, settlement_timing: SettlementTiming = SettlementTiming.AT_EXPIRY, observation_mode: ObservationMode = ObservationMode.CONTINUOUS, observation_dates: collections.abc.Iterable[datetime.date] = ()) -> TouchOption
```

Create an asset one-touch option.

The factory name selects an upper or lower barrier.

#### Parameters

- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates.
- **`barrier_level`** (`float`) — Positive barrier level.
- **`settlement_timing`** (`SettlementTiming, optional`) — Settle at the barrier hit or at expiry.
- **`observation_mode`** (`ObservationMode, optional`) — Continuous or scheduled monitoring.
- **`observation_dates`** (`iterable[datetime.date], optional`) — Required schedule for scheduled monitoring.
#### Returns

- `TouchOption` — Validated immutable asset one-touch option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the barrier, dates, or observation schedule.

## `both_down_snowball`

```python
both_down_snowball(*, initial_coupon_rate: float, coupon_rate_decrement: float, initial_spot: float, knock_in_level: float, initial_knock_out_level: float, knock_out_level_decrement: float, observation_dates: collections.abc.Iterable[datetime.date], effective_date: datetime.date, expiry_date: datetime.date, barrier_state: AutocallableBarrierState = AutocallableBarrierState.NONE, principal_ratio: float = 1.0) -> SnowballOption
```

Create a snowball with decreasing coupons and knock-out barriers.

#### Parameters

- **`initial_coupon_rate`** (`float`) — Annualized coupon rate at the first observation.
- **`coupon_rate_decrement`** (`float`) — Amount subtracted from each successive coupon rate.
- **`initial_spot`** (`float`) — Positive reference spot.
- **`knock_in_level`** (`float`) — Lower knock-in barrier level.
- **`initial_knock_out_level`** (`float`) — Knock-out level at the first observation.
- **`knock_out_level_decrement`** (`float`) — Amount subtracted from each successive knock-out level.
- **`observation_dates`** (`iterable[datetime.date]`) — Ordered knock-out observation dates.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates.
- **`barrier_state`** (`AutocallableBarrierState, optional`) — Barrier history known at valuation time.
- **`principal_ratio`** (`float, optional`) — Principal scaling applied to the payoff.
#### Returns

- `SnowballOption` — Validated immutable snowball option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the rates, levels, schedule, state, or dates.

## `cash_binary_barrier_option`

```python
cash_binary_barrier_option(*, option_type: OptionType, strike: float, effective_date: datetime.date, expiry_date: datetime.date, barrier_level: float, barrier_type: BarrierType, payout: float, observation_mode: ObservationMode = ObservationMode.CONTINUOUS, observation_dates: collections.abc.Iterable[datetime.date] = ()) -> BinaryBarrierOption
```

Create a cash-or-nothing binary barrier option.

#### Parameters

- **`option_type`** (`OptionType`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive strike price.
- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates.
- **`barrier_level`** (`float`) — Positive barrier level.
- **`barrier_type`** (`BarrierType`) — Barrier direction and activation behavior.
- **`payout`** (`float`) — Fixed cash amount paid when the payoff and barrier conditions hold.
- **`observation_mode`** (`ObservationMode, optional`) — Continuous or scheduled monitoring.
- **`observation_dates`** (`iterable[datetime.date], optional`) — Required schedule for scheduled monitoring.
#### Returns

- `BinaryBarrierOption` — Validated immutable cash binary barrier option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the payoff, barrier, dates, or observation schedule.

## `cash_no_touch_down`

```python
cash_no_touch_down(*, effective_date: datetime.date, expiry_date: datetime.date, barrier_level: float, payout: float, observation_mode: ObservationMode = ObservationMode.CONTINUOUS, observation_dates: collections.abc.Iterable[datetime.date] = ()) -> TouchOption
```

Create a cash no-touch option.

The factory name selects an upper or lower barrier. No-touch payoffs settle at
expiry.

#### Parameters

- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates.
- **`barrier_level`** (`float`) — Positive barrier level.
- **`payout`** (`float`) — Fixed cash payout.
- **`observation_mode`** (`ObservationMode, optional`) — Continuous or scheduled monitoring.
- **`observation_dates`** (`iterable[datetime.date], optional`) — Required schedule for scheduled monitoring.
#### Returns

- `TouchOption` — Validated immutable cash no-touch option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the payoff, barrier, dates, or observation schedule.

## `cash_no_touch_up`

```python
cash_no_touch_up(*, effective_date: datetime.date, expiry_date: datetime.date, barrier_level: float, payout: float, observation_mode: ObservationMode = ObservationMode.CONTINUOUS, observation_dates: collections.abc.Iterable[datetime.date] = ()) -> TouchOption
```

Create a cash no-touch option.

The factory name selects an upper or lower barrier. No-touch payoffs settle at
expiry.

#### Parameters

- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates.
- **`barrier_level`** (`float`) — Positive barrier level.
- **`payout`** (`float`) — Fixed cash payout.
- **`observation_mode`** (`ObservationMode, optional`) — Continuous or scheduled monitoring.
- **`observation_dates`** (`iterable[datetime.date], optional`) — Required schedule for scheduled monitoring.
#### Returns

- `TouchOption` — Validated immutable cash no-touch option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the payoff, barrier, dates, or observation schedule.

## `cash_one_touch_down`

```python
cash_one_touch_down(*, effective_date: datetime.date, expiry_date: datetime.date, barrier_level: float, payout: float, settlement_timing: SettlementTiming = SettlementTiming.AT_EXPIRY, observation_mode: ObservationMode = ObservationMode.CONTINUOUS, observation_dates: collections.abc.Iterable[datetime.date] = ()) -> TouchOption
```

Create a cash one-touch option.

The factory name selects an upper or lower barrier.

#### Parameters

- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates.
- **`barrier_level`** (`float`) — Positive barrier level.
- **`payout`** (`float`) — Fixed cash payout.
- **`settlement_timing`** (`SettlementTiming, optional`) — Settle at the barrier hit or at expiry.
- **`observation_mode`** (`ObservationMode, optional`) — Continuous or scheduled monitoring.
- **`observation_dates`** (`iterable[datetime.date], optional`) — Required schedule for scheduled monitoring.
#### Returns

- `TouchOption` — Validated immutable cash one-touch option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the payoff, barrier, dates, or observation schedule.

## `cash_one_touch_up`

```python
cash_one_touch_up(*, effective_date: datetime.date, expiry_date: datetime.date, barrier_level: float, payout: float, settlement_timing: SettlementTiming = SettlementTiming.AT_EXPIRY, observation_mode: ObservationMode = ObservationMode.CONTINUOUS, observation_dates: collections.abc.Iterable[datetime.date] = ()) -> TouchOption
```

Create a cash one-touch option.

The factory name selects an upper or lower barrier.

#### Parameters

- **`effective_date, expiry_date`** (`datetime.date`) — Contract effective and expiry dates.
- **`barrier_level`** (`float`) — Positive barrier level.
- **`payout`** (`float`) — Fixed cash payout.
- **`settlement_timing`** (`SettlementTiming, optional`) — Settle at the barrier hit or at expiry.
- **`observation_mode`** (`ObservationMode, optional`) — Continuous or scheduled monitoring.
- **`observation_dates`** (`iterable[datetime.date], optional`) — Required schedule for scheduled monitoring.
#### Returns

- `TouchOption` — Validated immutable cash one-touch option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the payoff, barrier, dates, or observation schedule.

## `dual_coupon_snowball`

```python
dual_coupon_snowball(*, knock_out_coupon_rate: float, maturity_coupon_rate: float, initial_spot: float, knock_in_level: float, knock_out_level: float, observation_dates: collections.abc.Iterable[datetime.date], effective_date: datetime.date, expiry_date: datetime.date, barrier_state: AutocallableBarrierState = AutocallableBarrierState.NONE, principal_ratio: float = 1.0) -> SnowballOption
```

Create a snowball with separate knock-out and maturity coupons.

#### Parameters

- **`knock_out_coupon_rate`** (`float`) — Annualized coupon rate paid after knock-out.
- **`maturity_coupon_rate`** (`float`) — Annualized coupon rate paid at maturity when applicable.
- **`initial_spot`** (`float`) — Positive reference spot.
- **`knock_in_level`** (`float`) — Lower knock-in barrier level.
- **`knock_out_level`** (`float`) — Knock-out level applied to every observation.
- **`observation_dates`** (`iterable[datetime.date]`) — Ordered knock-out observation dates.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates.
- **`barrier_state`** (`AutocallableBarrierState, optional`) — Barrier history known at valuation time.
- **`principal_ratio`** (`float, optional`) — Principal scaling applied to the payoff.
#### Returns

- `SnowballOption` — Validated immutable snowball option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the rates, levels, schedule, state, or dates.

## `european_snowball`

```python
european_snowball(*, coupon_rate: float, initial_spot: float, knock_in_level: float, knock_out_level: float, observation_dates: collections.abc.Iterable[datetime.date], effective_date: datetime.date, expiry_date: datetime.date, barrier_state: AutocallableBarrierState = AutocallableBarrierState.NONE, principal_ratio: float = 1.0) -> SnowballOption
```

Create a standard or European snowball preset.

The called factory determines whether the knock-in barrier is observed every
trading day or only at expiry.

#### Parameters

- **`coupon_rate`** (`float`) — Annualized coupon rate used for knock-out and maturity coupons.
- **`initial_spot`** (`float`) — Positive reference spot.
- **`knock_in_level`** (`float`) — Lower knock-in barrier level.
- **`knock_out_level`** (`float`) — Knock-out level applied to every observation.
- **`observation_dates`** (`iterable[datetime.date]`) — Ordered knock-out observation dates.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates.
- **`barrier_state`** (`AutocallableBarrierState, optional`) — Barrier history known at valuation time.
- **`principal_ratio`** (`float, optional`) — Principal scaling applied to the payoff.
#### Returns

- `SnowballOption` — Validated immutable snowball option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the rates, levels, schedule, state, or dates.

## `loss_capped_snowball`

```python
loss_capped_snowball(*, coupon_rate: float, initial_spot: float, knock_in_level: float, knock_out_level: float, lower_strike: float, observation_dates: collections.abc.Iterable[datetime.date], effective_date: datetime.date, expiry_date: datetime.date, barrier_state: AutocallableBarrierState = AutocallableBarrierState.NONE, principal_ratio: float = 1.0) -> SnowballOption
```

Create a snowball with a lower loss-capping strike.

#### Parameters

- **`coupon_rate`** (`float`) — Annualized coupon rate.
- **`initial_spot`** (`float`) — Positive reference spot.
- **`knock_in_level`** (`float`) — Lower knock-in barrier level.
- **`knock_out_level`** (`float`) — Knock-out level applied to every observation.
- **`lower_strike`** (`float`) — Lower terminal strike that caps downside loss.
- **`observation_dates`** (`iterable[datetime.date]`) — Ordered knock-out observation dates.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates.
- **`barrier_state`** (`AutocallableBarrierState, optional`) — Barrier history known at valuation time.
- **`principal_ratio`** (`float, optional`) — Principal scaling applied to the payoff.
#### Returns

- `SnowballOption` — Validated immutable loss-capped snowball option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the rates, levels, schedule, state, or dates.

## `otm_snowball`

```python
otm_snowball(*, coupon_rate: float, initial_spot: float, knock_in_level: float, knock_out_level: float, upper_strike: float, observation_dates: collections.abc.Iterable[datetime.date], effective_date: datetime.date, expiry_date: datetime.date, barrier_state: AutocallableBarrierState = AutocallableBarrierState.NONE, principal_ratio: float = 1.0) -> SnowballOption
```

Create a snowball with a custom upper terminal strike.

#### Parameters

- **`coupon_rate`** (`float`) — Annualized coupon rate.
- **`initial_spot`** (`float`) — Positive reference spot.
- **`knock_in_level`** (`float`) — Lower knock-in barrier level.
- **`knock_out_level`** (`float`) — Knock-out level applied to every observation.
- **`upper_strike`** (`float`) — Upper terminal participation strike.
- **`observation_dates`** (`iterable[datetime.date]`) — Ordered knock-out observation dates.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates.
- **`barrier_state`** (`AutocallableBarrierState, optional`) — Barrier history known at valuation time.
- **`principal_ratio`** (`float, optional`) — Principal scaling applied to the payoff.
#### Returns

- `SnowballOption` — Validated immutable out-of-the-money snowball option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the rates, levels, schedule, state, or dates.

## `parachute_snowball`

```python
parachute_snowball(*, coupon_rate: float, initial_spot: float, knock_in_level: float, knock_out_level: float, final_knock_out_level: float, observation_dates: collections.abc.Iterable[datetime.date], effective_date: datetime.date, expiry_date: datetime.date, barrier_state: AutocallableBarrierState = AutocallableBarrierState.NONE, principal_ratio: float = 1.0) -> SnowballOption
```

Create a snowball with a distinct final knock-out barrier.

#### Parameters

- **`coupon_rate`** (`float`) — Annualized coupon rate.
- **`initial_spot`** (`float`) — Positive reference spot.
- **`knock_in_level`** (`float`) — Lower knock-in barrier level.
- **`knock_out_level`** (`float`) — Knock-out level before the final observation.
- **`final_knock_out_level`** (`float`) — Knock-out level at the final observation.
- **`observation_dates`** (`iterable[datetime.date]`) — Ordered knock-out observation dates.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates.
- **`barrier_state`** (`AutocallableBarrierState, optional`) — Barrier history known at valuation time.
- **`principal_ratio`** (`float, optional`) — Principal scaling applied to the payoff.
#### Returns

- `SnowballOption` — Validated immutable snowball option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the rates, levels, schedule, state, or dates.

## `standard_snowball`

```python
standard_snowball(*, coupon_rate: float, initial_spot: float, knock_in_level: float, knock_out_level: float, observation_dates: collections.abc.Iterable[datetime.date], effective_date: datetime.date, expiry_date: datetime.date, barrier_state: AutocallableBarrierState = AutocallableBarrierState.NONE, principal_ratio: float = 1.0) -> SnowballOption
```

Create a standard or European snowball preset.

The called factory determines whether the knock-in barrier is observed every
trading day or only at expiry.

#### Parameters

- **`coupon_rate`** (`float`) — Annualized coupon rate used for knock-out and maturity coupons.
- **`initial_spot`** (`float`) — Positive reference spot.
- **`knock_in_level`** (`float`) — Lower knock-in barrier level.
- **`knock_out_level`** (`float`) — Knock-out level applied to every observation.
- **`observation_dates`** (`iterable[datetime.date]`) — Ordered knock-out observation dates.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates.
- **`barrier_state`** (`AutocallableBarrierState, optional`) — Barrier history known at valuation time.
- **`principal_ratio`** (`float, optional`) — Principal scaling applied to the payoff.
#### Returns

- `SnowballOption` — Validated immutable snowball option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the rates, levels, schedule, state, or dates.

## `step_down_snowball`

```python
step_down_snowball(*, coupon_rate: float, initial_spot: float, knock_in_level: float, initial_knock_out_level: float, knock_out_level_decrement: float, observation_dates: collections.abc.Iterable[datetime.date], effective_date: datetime.date, expiry_date: datetime.date, barrier_state: AutocallableBarrierState = AutocallableBarrierState.NONE, principal_ratio: float = 1.0) -> SnowballOption
```

Create a snowball with linearly decreasing knock-out barriers.

#### Parameters

- **`coupon_rate`** (`float`) — Annualized coupon rate.
- **`initial_spot`** (`float`) — Positive reference spot.
- **`knock_in_level`** (`float`) — Lower knock-in barrier level.
- **`initial_knock_out_level`** (`float`) — Knock-out level at the first observation.
- **`knock_out_level_decrement`** (`float`) — Amount subtracted from each successive knock-out level.
- **`observation_dates`** (`iterable[datetime.date]`) — Ordered knock-out observation dates.
- **`effective_date, expiry_date`** (`datetime.date`) — Note effective and expiry dates.
- **`barrier_state`** (`AutocallableBarrierState, optional`) — Barrier history known at valuation time.
- **`principal_ratio`** (`float, optional`) — Principal scaling applied to the payoff.
#### Returns

- `SnowballOption` — Validated immutable snowball option.
#### Raises

- `TypeError` — If an argument has an incompatible representation.
- `KiyosiError` — If the core rejects the rates, levels, schedule, state, or dates.
