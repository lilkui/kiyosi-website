---
description: kiyosi.instruments 的 Python API 参考文档。
outline: [2, 4]
---

# `kiyosi.instruments`

Validated derivative contracts, autocallable presets and observation adapters.

``OptionType`` selects ``"call"`` or ``"put"``. Contract dates are inclusive,
with expiry at midnight UTC. Constructors validate terms; pricing validates
their consistency with the market snapshot, calendar and supplied history.
History describes events strictly before valuation; a current observation
is evaluated from the current spot. Replacement returns a new contract.
``replace()`` exposes named keyword-only fields through ``inspect.signature``.
Omitted fields, or the displayed default ``...`` (``Ellipsis``), retain their
values. Explicit ``None`` clears nullable history and is rejected for fields
that require a value.

``fixed_coupon_note`` and ``digital_coupon_note`` return Phoenix contracts
with fixed ``coupon_per_period`` and expiry-only knock-in. Explicit Phoenix
construction requires exactly one of annual ``coupon_rate`` or fixed
``coupon_per_period``; the unused property is None. ``early_profit_snowball``
and ``butterfly_snowball`` use two or three annual coupon stages with inclusive
cutoff dates. Knock-out applies the selected rate over the whole holding period;
maturity uses the final stage rate.

## Examples

Construct a digital call, then create an independent strike replacement.
Cash and asset digitals pay zero when the expiry spot equals the strike:

```python
>>> from datetime import date
>>> option = CashOrNothingOption(
...     option_type="call", strike=100, payout=10,
...     effective_date=date(2025, 1, 1), expiry_date=date(2026, 1, 1),
... )
>>> replacement = option.replace(strike=105)
>>> (option.strike, replacement.strike, replacement.payout)
(100.0, 105.0, 10.0)
```


Construct a cash no-touch contract using the same barrier choices as barrier options.
Use ``asset_touch_option`` for asset settlement. At-hit settlement is available
only for one-touch contracts (``up_and_in`` or ``down_and_in``):

```python
>>> touch = cash_touch_option(
...     effective_date=date(2025, 1, 1), expiry_date=date(2026, 1, 1),
...     barrier_level=80, barrier_type="down_and_out", payout=10,
... )
>>> (touch.barrier_type, touch.is_one_touch, touch.settlement_timing)
('down_and_out', False, 'at_expiry')
```

## `Accumulator`

```python
Accumulator(*, strike, knock_out_level, daily_quantity, acceleration_factor, effective_date, expiry_date, accumulated_quantity=Ellipsis, option_type=Ellipsis, knock_out_observation_dates=None)
```

Accumulates purchases or sales daily, settling at scheduled knock-out or expiry.

#### Parameters

- **`strike`** (`float`) — Positive finite purchase or sale strike.
- **`knock_out_level`** (`float`) — Positive inclusive knock-out threshold.
- **`daily_quantity`** (`float`) — Nonnegative finite quantity bought or sold on each trading date.
- **`acceleration_factor`** (`float`) — Nonnegative multiplier below strike for calls or above strike for puts.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`accumulated_quantity`** (`float, optional`) — Caller-asserted outstanding quantity strictly before valuation.
- **`option_type`** (`{'call', 'put'}, optional`) — Call accumulates purchases (the default); put accumulates sales.
- **`knock_out_observation_dates`** (`iterable of date or None, optional`) — Strictly increasing, unique dates within the inclusive contract life. None observes knock-out every trading date; an empty sequence disables early knock-out. Dates need not include either contract endpoint.
#### Raises

- `InvalidInputError` — If strike or knock-out level is invalid, quantities are negative or non-finite, expiry precedes effective_date, or explicit dates are invalid. Trading-date compatibility is checked against the calendar at pricing.
#### Notes

Events occur at midnight UTC on trading dates. On a knock-out observation
date, calls knock out at or above the barrier and puts at or below it.
Knock-out precedes accumulation and adds no units. Other trading dates
accumulate even beyond the barrier. At strike, the base quantity applies.
Expiry settles after its event, whether or not it is a knock-out date.
Calls pay quantity * (settlement spot - strike); puts pay its negative.
Intraday history includes that day's earlier accumulation. Do not value a
contract whose settlement has already occurred.

### `acceleration_factor`

Returns the quantity multiplier below strike for calls or above it for puts.

### `accumulated_quantity`

Return caller-asserted outstanding quantity strictly before valuation.

### `daily_quantity`

Returns the nonnegative base quantity bought or sold on each trading date.

### `effective_date`

Return inclusive first contract date.

### `expiry_date`

Return final contract date; expiry is at midnight UTC.

### `knock_out_level`

Return positive inclusive knock-out threshold.

### `knock_out_observation_dates`

Returns owned knock-out dates, or None for every trading date.

### `option_type`

Returns call for purchases or put for sales.

### `replace`

```python
replace(self, /, *, accumulated_quantity)
```

Return a validated replacement without changing this value.

#### Parameters

- **`accumulated_quantity`** (`float`) — Caller-asserted outstanding quantity strictly before valuation.
#### Returns

- `object` — New instance of the same class; omitted fields retain their values.
#### Raises

- `KiyosiError` — If replacement terms fail domain validation. The original is unchanged.

### `strike`

Returns the purchase or sale strike in underlying price units.

## `AmericanOption`

```python
AmericanOption(*, option_type, strike, effective_date, expiry_date)
```

Vanilla option exercisable throughout its inclusive contract life.

#### Parameters

- **`option_type`** (`{'call', 'put'}`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive finite exercise or purchase price.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
#### Raises

- `InvalidInputError` — If strike is nonpositive or non-finite, or expiry precedes effective_date.

### `effective_date`

Return inclusive first contract date.

### `expiry_date`

Return final contract date; expiry is at midnight UTC.

### `option_type`

Return call or put payoff direction.

### `replace`

```python
replace(self, /, *, option_type=Ellipsis, strike=Ellipsis, effective_date=Ellipsis, expiry_date=Ellipsis)
```

Return a validated replacement without changing this value.

#### Parameters

- **`option_type`** (`{'call', 'put'}, optional`) — Call or put payoff direction.
- **`strike`** (`float, optional`) — Positive finite exercise or purchase price.
- **`effective_date`** (`datetime.date, optional`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date, optional`) — Final contract date; expiry is at midnight UTC.
#### Returns

- `object` — New instance of the same class; omitted fields or Ellipsis retain their values.
#### Raises

- `KiyosiError` — If replacement terms fail domain validation. The original is unchanged.

### `strike`

Return the exercise or purchase price in underlying price units.

## `ArithmeticAveragePriceOption`

```python
ArithmeticAveragePriceOption(*, option_type, strike, effective_date, averaging_start_date, expiry_date, realized_average=Ellipsis)
```

Continuous average-price option with explicit history.

#### Parameters

- **`option_type`** (`{'call', 'put'}`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive finite exercise or purchase price.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`averaging_start_date`** (`datetime.date`) — First averaging date, within the contract life.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`realized_average`** (`float, optional`) — Nonnegative finite prior average; defaults to zero. Must be zero at or before averaging starts, and positive strictly after it; time consistency is checked at pricing.
#### Raises

- `InvalidInputError` — If strike, realized_average, life dates or the averaging window are invalid.

### `averaging_start_date`

Return first averaging date, within the contract life.

### `effective_date`

Return inclusive first contract date.

### `expiry_date`

Return final contract date; expiry is at midnight UTC.

### `option_type`

Return call or put payoff direction.

### `realized_average`

Return the supplied historical average; zero denotes no history.

### `replace`

```python
replace(self, /, *, realized_average=Ellipsis)
```

Return a validated replacement without changing this value.

#### Parameters

- **`realized_average`** (`float, optional`) — Prior average; zero denotes no history. Pricing checks time consistency.
#### Returns

- `object` — New instance of the same class; omitted fields or Ellipsis retain their values.
#### Raises

- `KiyosiError` — If replacement terms fail domain validation. The original is unchanged.

### `strike`

Return the exercise or purchase price in underlying price units.

## `AssetOrNothingOption`

```python
AssetOrNothingOption(*, option_type, strike, effective_date, expiry_date)
```

European digital paying the asset strictly in the money.

#### Parameters

- **`option_type`** (`{'call', 'put'}`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive finite exercise or purchase price.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
#### Raises

- `InvalidInputError` — If strike is nonpositive/non-finite, or expiry precedes effective_date.

### `effective_date`

Return inclusive first contract date.

### `expiry_date`

Return final contract date; expiry is at midnight UTC.

### `option_type`

Return call or put payoff direction.

### `replace`

```python
replace(self, /, *, option_type=Ellipsis, strike=Ellipsis, effective_date=Ellipsis, expiry_date=Ellipsis)
```

Return a validated replacement without changing this value.

#### Parameters

- **`option_type`** (`{'call', 'put'}, optional`) — Call or put payoff direction.
- **`strike`** (`float, optional`) — Positive finite exercise or purchase price.
- **`payout`** (`float, optional`) — Positive finite cash payment; accepted only for CashOrNothingOption.
- **`effective_date`** (`datetime.date, optional`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date, optional`) — Final contract date; expiry is at midnight UTC.
#### Returns

- `object` — New instance of the same class; omitted fields or Ellipsis retain their values.
#### Raises

- `KiyosiError` — If replacement terms fail domain validation. The original is unchanged.

### `strike`

Return the exercise or purchase price in underlying price units.

## `AutocallableObservation`

```python
AutocallableObservation(date, knock_out_level, *, coupon_rate=Ellipsis, coupon_barrier_level=Ellipsis)
```

Input observation validated when its note is constructed.

#### Parameters

- **`date`** (`datetime.date`) — Observation date at midnight UTC.
- **`knock_out_level`** (`float`) — Positive inclusive knock-out threshold.
- **`coupon_rate`** (`float, optional`) — Finite annual coupon rate in decimal units.
- **`coupon_barrier_level`** (`float, optional`) — Inclusive Phoenix coupon threshold; must be zero for snowballs.
#### Notes

This record checks Python representations only. Note construction
validates contractual levels and coupons.

### `coupon_barrier_level`

Return the supplied Phoenix coupon threshold; note construction validates it.

### `coupon_rate`

Return the supplied annual coupon in decimal units; note construction validates it.

### `date`

Return observation date at midnight UTC.

### `knock_out_level`

Return the supplied knock-out threshold; the note constructor validates it.

## `BarrierOption`

```python
BarrierOption(*, option_type, strike, effective_date, expiry_date, barrier_level, barrier_type, rebate=Ellipsis, rebate_timing=Ellipsis, observation_mode=Ellipsis, observation_dates=Ellipsis, touch_state=None)
```

Single-barrier vanilla option with inclusive barrier touches.

#### Parameters

- **`option_type`** (`{'call', 'put'}`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive finite exercise or purchase price.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`barrier_level`** (`float`) — Positive finite trigger level; equality counts as a touch.
- **`barrier_type`** (`{'up_and_in', 'up_and_out', 'down_and_in', 'down_and_out'}`) — Trigger direction and knock-in or knock-out behavior.
- **`rebate`** (`float, optional`) — Nonnegative finite cash rebate; defaults to zero.
- **`rebate_timing`** (`{'at_hit', 'at_expiry'}, optional`) — Payment timing; at-hit rebates are valid only for knock-outs.
- **`observation_mode`** (`{'continuous', 'scheduled'}, optional`) — Continuous monitoring or observations on the supplied dates.
- **`observation_dates`** (`iterable of date, optional`) — Strictly increasing observation dates within the contract life.
- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — Strictly prior history. None means unknown; untouched means known no hit.
#### Raises

- `InvalidInputError` — If levels, rebate, life dates, monitoring schedule or rebate timing are invalid. Trading-day and valuation-history checks occur at pricing.

### `barrier_level`

Return positive finite trigger level; equality counts as a touch.

### `barrier_type`

Return trigger direction and knock-in or knock-out behavior.

### `effective_date`

Returns inclusive first contract date.

### `expiry_date`

Returns final contract date; expiry is at midnight UTC.

### `mean_observation_year_fraction`

Return mean fixing spacing in Actual/365 Fixed years.

### `observation_dates`

Returns a copy of the contractual observation dates.

### `observation_mode`

Returns continuous monitoring or observations on the supplied dates.

### `observation_schedule`

Returns an owned copy of the monitoring schedule.

### `option_type`

Return call or put payoff direction.

### `rebate`

Return nonnegative finite cash rebate; defaults to zero.

### `rebate_timing`

Return payment timing; at-hit rebates are valid only for knock-outs.

### `replace`

```python
replace(self, /, *, touch_state=Ellipsis)
```

Returns a validated replacement without changing this value.

#### Parameters

- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — Strictly prior history. None means unknown; untouched means known no hit.
#### Returns

- `object` — New instance of the same class; omitted fields or Ellipsis retain their values.
#### Raises

- `TypeError` — If a field is unknown or touch_state is not a string, None or Ellipsis.
- `ValueError` — If touch_state is an unknown choice.

### `strike`

Return the exercise or purchase price in underlying price units.

### `touch_state`

Returns strictly prior touch history, or None if unknown.

## `BinaryBarrierOption`

Cash or asset digital with barrier monitoring and strict exercise.

#### Notes

Construct with cash_binary_barrier_option or asset_binary_barrier_option.
Barrier equality touches; terminal strike equality pays zero.

### `barrier_level`

Return positive finite trigger level; equality counts as a touch.

### `barrier_type`

Return trigger direction and knock-in or knock-out behavior.

### `effective_date`

Returns inclusive first contract date.

### `expiry_date`

Returns final contract date; expiry is at midnight UTC.

### `mean_observation_year_fraction`

Return mean fixing spacing in Actual/365 Fixed years.

### `observation_dates`

Returns a copy of the contractual observation dates.

### `observation_mode`

Returns continuous monitoring or observations on the supplied dates.

### `observation_schedule`

Returns an owned copy of the monitoring schedule.

### `option_type`

Return call or put payoff direction.

### `payoff_type`

Return cash or asset settlement as a choice string.

### `payout`

Return the cash payout, or None for asset settlement.

### `replace`

```python
replace(self, /, *, touch_state=Ellipsis)
```

Returns a validated replacement without changing this value.

#### Parameters

- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — Strictly prior history. None means unknown; untouched means known no hit.
#### Returns

- `object` — New instance of the same class; omitted fields or Ellipsis retain their values.
#### Raises

- `TypeError` — If a field is unknown or touch_state is not a string, None or Ellipsis.
- `ValueError` — If touch_state is an unknown choice.

### `strike`

Return the exercise or purchase price in underlying price units.

### `touch_state`

Returns strictly prior touch history, or None if unknown.

## `BinarySnowballOption`

```python
BinarySnowballOption(*, maturity_coupon_rate, effective_date, expiry_date, observations, barrier_state=None, principal_ratio=Ellipsis)
```

Snowball with knock-out coupons and no knock-in or downside loss.

#### Parameters

- **`maturity_coupon_rate`** (`float`) — Finite annual maturity coupon rate in decimal units.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`observations`** (`iterable of AutocallableObservation`) — Nonempty, strictly ordered contractual observations within life.
- **`barrier_state`** (`{'none', 'knocked_in', 'knocked_out'} or None, optional`) — Strictly prior events. None is unknown; the string none means no event.
- **`principal_ratio`** (`float, optional`) — Nonnegative normalized principal, independent of coupons and losses.
#### Raises

- `InvalidInputError` — If coupons, principal, dates or observations are invalid, or barrier_state is knocked_in; this contract has no knock-in barrier.

### `barrier_state`

Returns strictly prior autocallable history, or None if unknown.

### `effective_date`

Returns inclusive first contract date.

### `expiry_date`

Returns final contract date; expiry is at midnight UTC.

### `knock_out_coupon_rates`

Return copied annual knock-out coupons in observation order.

### `knock_out_levels`

Returns copied knock-out thresholds in observation order.

### `maturity_coupon_rate`

Return finite annual maturity coupon rate in decimal units.

### `observation_dates`

Returns a copy of the contractual observation dates.

### `observations`

Returns owned copies of the contractual observations.

### `principal_ratio`

Returns nonnegative normalized principal, independent of coupons and losses.

### `replace`

```python
replace(self, /, *, barrier_state)
```

Returns a validated replacement without changing this value.

#### Parameters

- **`barrier_state`** (`{'none', 'knocked_in', 'knocked_out'} or None`) — Strictly prior events. None is unknown; the string none means no event.
#### Returns

- `object` — New instance of the same class; omitted fields retain their values.
#### Raises

- `KiyosiError` — If replacement terms fail domain validation. The original is unchanged.

## `CashOrNothingOption`

```python
CashOrNothingOption(*, option_type, strike, payout, effective_date, expiry_date)
```

European digital paying cash strictly in the money.

#### Parameters

- **`option_type`** (`{'call', 'put'}`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive finite exercise or purchase price.
- **`payout`** (`float`) — Positive finite cash payment.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
#### Raises

- `InvalidInputError` — If payout or strike is nonpositive/non-finite, or expiry precedes effective_date.

### `effective_date`

Return inclusive first contract date.

### `expiry_date`

Return final contract date; expiry is at midnight UTC.

### `option_type`

Return call or put payoff direction.

### `payout`

Return the fixed cash payout.

### `replace`

```python
replace(self, /, *, option_type=Ellipsis, strike=Ellipsis, payout=Ellipsis, effective_date=Ellipsis, expiry_date=Ellipsis)
```

Return a validated replacement without changing this value.

#### Parameters

- **`option_type`** (`{'call', 'put'}, optional`) — Call or put payoff direction.
- **`strike`** (`float, optional`) — Positive finite exercise or purchase price.
- **`payout`** (`float, optional`) — Positive finite cash payment; accepted only for CashOrNothingOption.
- **`effective_date`** (`datetime.date, optional`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date, optional`) — Final contract date; expiry is at midnight UTC.
#### Returns

- `object` — New instance of the same class; omitted fields or Ellipsis retain their values.
#### Raises

- `KiyosiError` — If replacement terms fail domain validation. The original is unchanged.

### `strike`

Return the exercise or purchase price in underlying price units.

## `DoubleBarrierOption`

```python
DoubleBarrierOption(*, option_type, strike, effective_date, expiry_date, lower_barrier, upper_barrier, barrier_type, rebate=Ellipsis, rebate_timing=Ellipsis, observation_mode=Ellipsis, observation_dates=Ellipsis, touch_state=None)
```

Vanilla option activated or terminated by either inclusive boundary.

#### Parameters

- **`option_type`** (`{'call', 'put'}`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive finite exercise or purchase price.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`lower_barrier`** (`float`) — Positive finite lower trigger; equality counts as a touch.
- **`upper_barrier`** (`float`) — Finite upper trigger, strictly above the lower trigger.
- **`barrier_type`** (`{'knock_in', 'knock_out'}`) — Trigger direction and knock-in or knock-out behavior.
- **`rebate`** (`float, optional`) — Nonnegative finite cash rebate; defaults to zero.
- **`rebate_timing`** (`{'at_hit', 'at_expiry'}, optional`) — Payment timing; at-hit rebates are valid only for knock-outs.
- **`observation_mode`** (`{'continuous', 'scheduled'}, optional`) — Continuous monitoring or observations on the supplied dates.
- **`observation_dates`** (`iterable of date, optional`) — Strictly increasing observation dates within the contract life.
- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — Strictly prior history. None means unknown; untouched means known no hit.
#### Raises

- `InvalidInputError` — If boundaries, strike, rebate, life dates, monitoring schedule or rebate timing are invalid. Calendar and history checks occur at pricing.

### `barrier_type`

Return trigger direction and knock-in or knock-out behavior.

### `effective_date`

Returns inclusive first contract date.

### `expiry_date`

Returns final contract date; expiry is at midnight UTC.

### `lower_barrier`

Return positive finite lower trigger; equality counts as a touch.

### `observation_dates`

Returns a copy of the contractual observation dates.

### `observation_mode`

Returns continuous monitoring or observations on the supplied dates.

### `observation_schedule`

Returns an owned copy of the monitoring schedule.

### `option_type`

Return call or put payoff direction.

### `rebate`

Return nonnegative finite cash rebate; defaults to zero.

### `rebate_timing`

Return payment timing; at-hit rebates are valid only for knock-outs.

### `replace`

```python
replace(self, /, *, touch_state=Ellipsis)
```

Returns a validated replacement without changing this value.

#### Parameters

- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — Strictly prior history. None means unknown; untouched means known no hit.
#### Returns

- `object` — New instance of the same class; omitted fields or Ellipsis retain their values.
#### Raises

- `TypeError` — If a field is unknown or touch_state is not a string, None or Ellipsis.
- `ValueError` — If touch_state is an unknown choice.

### `strike`

Return the exercise or purchase price in underlying price units.

### `touch_state`

Returns strictly prior touch history, or None if unknown.

### `upper_barrier`

Return finite upper trigger, strictly above the lower trigger.

## `DoubleTouchOption`

Cash one-touch or no-touch contract with two inclusive boundaries.

#### Notes

Construct with cash_double_touch or cash_double_no_touch. Prior at-hit
payments have no remaining value.

### `effective_date`

Returns inclusive first contract date.

### `expiry_date`

Returns final contract date; expiry is at midnight UTC.

### `is_one_touch`

Return whether touching activates payment.

### `lower_barrier`

Return positive finite lower trigger; equality counts as a touch.

### `observation_dates`

Returns a copy of the contractual observation dates.

### `observation_mode`

Returns continuous monitoring or observations on the supplied dates.

### `observation_schedule`

Returns an owned copy of the monitoring schedule.

### `payout`

Return the nonnegative finite cash payout.

### `replace`

```python
replace(self, /, *, touch_state=Ellipsis)
```

Returns a validated replacement without changing this value.

#### Parameters

- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — Strictly prior history. None means unknown; untouched means known no hit.
#### Returns

- `object` — New instance of the same class; omitted fields or Ellipsis retain their values.
#### Raises

- `TypeError` — If a field is unknown or touch_state is not a string, None or Ellipsis.
- `ValueError` — If touch_state is an unknown choice.

### `settlement_timing`

Return at-hit or expiry payment; no-touch contracts settle only at expiry.

### `touch_state`

Returns strictly prior touch history, or None if unknown.

### `upper_barrier`

Return finite upper trigger, strictly above the lower trigger.

## `EuropeanOption`

```python
EuropeanOption(*, option_type, strike, effective_date, expiry_date)
```

European vanilla option with a positive strike.

#### Parameters

- **`option_type`** (`{'call', 'put'}`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive finite exercise or purchase price.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
#### Raises

- `InvalidInputError` — If strike is nonpositive or non-finite, or expiry precedes effective_date.

### `effective_date`

Return inclusive first contract date.

### `expiry_date`

Return final contract date; expiry is at midnight UTC.

### `option_type`

Return call or put payoff direction.

### `strike`

Return the exercise or purchase price in underlying price units.

## `GeometricAveragePriceOption`

```python
GeometricAveragePriceOption(*, option_type, strike, effective_date, averaging_start_date, expiry_date, realized_average=Ellipsis)
```

Continuous average-price option with explicit history.

#### Parameters

- **`option_type`** (`{'call', 'put'}`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive finite exercise or purchase price.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`averaging_start_date`** (`datetime.date`) — First averaging date, within the contract life.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`realized_average`** (`float, optional`) — Nonnegative finite prior average; defaults to zero. Must be zero at or before averaging starts, and positive strictly after it; time consistency is checked at pricing.
#### Raises

- `InvalidInputError` — If strike, realized_average, life dates or the averaging window are invalid.

### `averaging_start_date`

Return first averaging date, within the contract life.

### `effective_date`

Return inclusive first contract date.

### `expiry_date`

Return final contract date; expiry is at midnight UTC.

### `option_type`

Return call or put payoff direction.

### `realized_average`

Return the supplied historical average; zero denotes no history.

### `replace`

```python
replace(self, /, *, realized_average=Ellipsis)
```

Return a validated replacement without changing this value.

#### Parameters

- **`realized_average`** (`float, optional`) — Prior average; zero denotes no history. Pricing checks time consistency.
#### Returns

- `object` — New instance of the same class; omitted fields or Ellipsis retain their values.
#### Raises

- `KiyosiError` — If replacement terms fail domain validation. The original is unchanged.

### `strike`

Return the exercise or purchase price in underlying price units.

## `OptionType`

```python
OptionType = typing.Literal['call', 'put']
```

## `PhoenixOption`

```python
PhoenixOption(*, coupon_rate=Ellipsis, coupon_per_period=Ellipsis, initial_spot, knock_in_level, upper_strike, lower_strike, knock_in_observation_mode, effective_date, expiry_date, observations, barrier_state=None, principal_ratio=Ellipsis)
```

Autocallable with conditional period coupons and capped downside loss.

#### Parameters

- **`coupon_rate`** (`float, optional`) — Finite signed annual coupon rate. Supply exactly one of coupon_rate and coupon_per_period; omission or Ellipsis leaves a choice unspecified.
- **`coupon_per_period`** (`float, optional`) — Finite signed fixed coupon proportion per qualifying observation, without day accrual. The unused coupon property returns None.
- **`initial_spot`** (`float`) — Positive reference spot used to normalize downside losses.
- **`knock_in_level`** (`float`) — Positive strict downside threshold.
- **`upper_strike`** (`float`) — Positive upper terminal settlement strike.
- **`lower_strike`** (`float`) — Nonnegative lower terminal strike, at most the upper strike.
- **`knock_in_observation_mode`** (`{'every_trading_day', 'at_expiry'}`) — Observe knock-in on every trading day or only at expiry.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`observations`** (`iterable of AutocallableObservation`) — Nonempty, strictly ordered contractual observations within life.
- **`barrier_state`** (`{'none', 'knocked_in', 'knocked_out'} or None, optional`) — Strictly prior events. None is unknown; the string none means no event.
- **`principal_ratio`** (`float, optional`) — Nonnegative normalized principal, independent of coupons and losses.
#### Raises

- `TypeError` — If both coupon choices or neither are supplied, or a supplied value is not real.
- `InvalidInputError` — If amounts, strikes, life dates or observations are invalid. Observation coupon_rate must be zero; coupon_barrier_level is nonnegative.
#### Notes

Annual coupons accrue over contractual observation periods on Actual/365 Fixed.
Fixed per-period coupons pay once per qualifying observation, even for an
observation on the effective date. Explicit None is not a coupon value.
Coupon and knock-out barriers are inclusive; knock-in is strict. Past
coupons are settled. There is no coupon memory or maturity coupon.

### `barrier_state`

Returns strictly prior autocallable history, or None if unknown.

### `coupon_barrier_levels`

Return copied Phoenix coupon thresholds in observation order.

### `coupon_per_period`

Returns the fixed per-period coupon, or None for an annual coupon.

### `coupon_rate`

Returns the annual coupon rate, or None for a fixed per-period coupon.

### `effective_date`

Returns inclusive first contract date.

### `expiry_date`

Returns final contract date; expiry is at midnight UTC.

### `initial_spot`

Return positive reference spot used to normalize downside losses.

### `knock_in_level`

Return positive strict downside threshold.

### `knock_in_observation_mode`

Return the knock-in monitoring choice string.

### `knock_out_levels`

Returns copied knock-out thresholds in observation order.

### `lower_strike`

Return nonnegative lower terminal strike, at most the upper strike.

### `observation_dates`

Returns a copy of the contractual observation dates.

### `observations`

Returns owned copies of the contractual observations.

### `principal_ratio`

Returns nonnegative normalized principal, independent of coupons and losses.

### `replace`

```python
replace(self, /, *, barrier_state)
```

Returns a validated replacement without changing this value.

#### Parameters

- **`barrier_state`** (`{'none', 'knocked_in', 'knocked_out'} or None`) — Strictly prior events. None is unknown; the string none means no event.
#### Returns

- `object` — New instance of the same class; omitted fields retain their values.
#### Raises

- `KiyosiError` — If replacement terms fail domain validation. The original is unchanged.

### `upper_strike`

Return positive upper terminal settlement strike.

## `RangeAccrualOption`

```python
RangeAccrualOption(*, notional, annual_coupon_rate, lower_bound, upper_bound, effective_date, expiry_date, realized_hit_count=None)
```

Range coupon paid at expiry without principal repayment.

#### Parameters

- **`notional`** (`float`) — Positive finite coupon notional, without principal repayment.
- **`annual_coupon_rate`** (`float`) — Nonnegative finite annual coupon rate in decimal units.
- **`lower_bound`** (`float`) — Inclusive nonnegative lower spot boundary.
- **`upper_bound`** (`float`) — Inclusive finite upper spot boundary, above the lower boundary.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`realized_hit_count`** (`int or None, optional`) — Hits strictly before valuation, or None for unknown history.
#### Raises

- `InvalidInputError` — If amounts, bounds or history are invalid, or expiry is not after effective_date. Pricing checks history against elapsed observations.
#### Notes

Observe trading dates in (effective_date, expiry_date]. Bounds are
inclusive. Payment is notional times annual coupon times Actual/365 Fixed
life times the fraction of observations inside the range.

### `annual_coupon_rate`

Return nonnegative finite annual coupon rate in decimal units.

### `effective_date`

Return inclusive first contract date.

### `expiry_date`

Return final contract date; expiry is at midnight UTC.

### `lower_bound`

Return inclusive nonnegative lower spot boundary.

### `notional`

Return positive finite coupon notional, without principal repayment.

### `realized_hit_count`

Return hits strictly before valuation, or None for unknown history.

### `replace`

```python
replace(self, /, *, realized_hit_count=Ellipsis)
```

Return a validated replacement without changing this value.

#### Parameters

- **`realized_hit_count`** (`int or None, optional`) — Hits strictly before valuation, or None for unknown history.
#### Returns

- `object` — New instance of the same class; omitted fields or Ellipsis retain their values.
#### Raises

- `KiyosiError` — If replacement terms fail domain validation. The original is unchanged.

### `upper_bound`

Return inclusive finite upper spot boundary, above the lower boundary.

## `SnowballOption`

```python
SnowballOption(*, maturity_coupon_rate, initial_spot, knock_in_level, upper_strike, lower_strike, knock_in_observation_mode, effective_date, expiry_date, observations, barrier_state=None, principal_ratio=Ellipsis)
```

Snowball with knock-out coupons and capped knock-in downside loss.

#### Parameters

- **`maturity_coupon_rate`** (`float`) — Finite annual maturity coupon rate in decimal units.
- **`initial_spot`** (`float`) — Positive reference spot used to normalize downside losses.
- **`knock_in_level`** (`float`) — Positive strict downside threshold.
- **`upper_strike`** (`float`) — Positive upper terminal settlement strike.
- **`lower_strike`** (`float`) — Nonnegative lower terminal strike, at most the upper strike.
- **`knock_in_observation_mode`** (`{'every_trading_day', 'at_expiry'}`) — Observe knock-in on every trading day or only at expiry.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`observations`** (`iterable of AutocallableObservation`) — Nonempty, strictly ordered contractual observations within life.
- **`barrier_state`** (`{'none', 'knocked_in', 'knocked_out'} or None, optional`) — Strictly prior events. None is unknown; the string none means no event.
- **`principal_ratio`** (`float, optional`) — Nonnegative normalized principal, independent of coupons and losses.
#### Raises

- `InvalidInputError` — If amounts, strikes, life dates or observation terms are invalid. Pricing checks the calendar and prior barrier history.

### `barrier_state`

Returns strictly prior autocallable history, or None if unknown.

### `effective_date`

Returns inclusive first contract date.

### `expiry_date`

Returns final contract date; expiry is at midnight UTC.

### `initial_spot`

Return positive reference spot used to normalize downside losses.

### `knock_in_level`

Return positive strict downside threshold.

### `knock_in_observation_mode`

Return the knock-in monitoring choice string.

### `knock_out_coupon_rates`

Return copied annual knock-out coupons in observation order.

### `knock_out_levels`

Returns copied knock-out thresholds in observation order.

### `lower_strike`

Return nonnegative lower terminal strike, at most the upper strike.

### `maturity_coupon_rate`

Return finite annual maturity coupon rate in decimal units.

### `observation_dates`

Returns a copy of the contractual observation dates.

### `observations`

Returns owned copies of the contractual observations.

### `principal_ratio`

Returns nonnegative normalized principal, independent of coupons and losses.

### `replace`

```python
replace(self, /, *, barrier_state)
```

Returns a validated replacement without changing this value.

#### Parameters

- **`barrier_state`** (`{'none', 'knocked_in', 'knocked_out'} or None`) — Strictly prior events. None is unknown; the string none means no event.
#### Returns

- `object` — New instance of the same class; omitted fields retain their values.
#### Raises

- `KiyosiError` — If replacement terms fail domain validation. The original is unchanged.

### `upper_strike`

Return positive upper terminal settlement strike.

## `TernarySnowballOption`

```python
TernarySnowballOption(*, maturity_coupon_rate, minimum_coupon_rate, knock_in_level, knock_in_observation_mode, effective_date, expiry_date, observations, barrier_state=None, principal_ratio=Ellipsis)
```

Snowball with distinct intact and knocked-in maturity coupons.

#### Parameters

- **`maturity_coupon_rate`** (`float`) — Finite annual maturity coupon rate in decimal units.
- **`minimum_coupon_rate`** (`float`) — Knocked-in maturity coupon, at most the intact maturity coupon.
- **`knock_in_level`** (`float`) — Positive strict downside threshold.
- **`knock_in_observation_mode`** (`{'every_trading_day', 'at_expiry'}`) — Observe knock-in on every trading day or only at expiry.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`observations`** (`iterable of AutocallableObservation`) — Nonempty, strictly ordered contractual observations within life.
- **`barrier_state`** (`{'none', 'knocked_in', 'knocked_out'} or None, optional`) — Strictly prior events. None is unknown; the string none means no event.
- **`principal_ratio`** (`float, optional`) — Nonnegative normalized principal, independent of coupons and losses.
#### Raises

- `InvalidInputError` — If coupons, principal, barriers, dates or observations are invalid. minimum_coupon_rate must not exceed maturity_coupon_rate.

### `barrier_state`

Returns strictly prior autocallable history, or None if unknown.

### `effective_date`

Returns inclusive first contract date.

### `expiry_date`

Returns final contract date; expiry is at midnight UTC.

### `knock_in_level`

Return positive strict downside threshold.

### `knock_in_observation_mode`

Return the knock-in monitoring choice string.

### `knock_out_coupon_rates`

Return copied annual knock-out coupons in observation order.

### `knock_out_levels`

Returns copied knock-out thresholds in observation order.

### `maturity_coupon_rate`

Return finite annual maturity coupon rate in decimal units.

### `minimum_coupon_rate`

Return the annual knocked-in maturity coupon.

### `observation_dates`

Returns a copy of the contractual observation dates.

### `observations`

Returns owned copies of the contractual observations.

### `principal_ratio`

Returns nonnegative normalized principal, independent of coupons and losses.

### `replace`

```python
replace(self, /, *, barrier_state)
```

Returns a validated replacement without changing this value.

#### Parameters

- **`barrier_state`** (`{'none', 'knocked_in', 'knocked_out'} or None`) — Strictly prior events. None is unknown; the string none means no event.
#### Returns

- `object` — New instance of the same class; omitted fields retain their values.
#### Raises

- `KiyosiError` — If replacement terms fail domain validation. The original is unchanged.

## `TouchOption`

Strike-free cash or asset one-touch or no-touch contract.

#### Notes

Construct with cash_touch_option or asset_touch_option and an explicit barrier_type.
Prior at-hit payments are settled.

### `barrier_level`

Return positive finite trigger level; equality counts as a touch.

### `barrier_type`

Return trigger direction and knock-in or knock-out behavior.

### `effective_date`

Returns inclusive first contract date.

### `expiry_date`

Returns final contract date; expiry is at midnight UTC.

### `is_one_touch`

Return whether touching activates payment.

### `is_up`

Return whether the barrier triggers upward.

### `mean_observation_year_fraction`

Return mean fixing spacing in Actual/365 Fixed years.

### `observation_dates`

Returns a copy of the contractual observation dates.

### `observation_mode`

Returns continuous monitoring or observations on the supplied dates.

### `observation_schedule`

Returns an owned copy of the monitoring schedule.

### `payoff_type`

Return cash or asset settlement as a choice string.

### `payout`

Return the cash payout, or None for asset settlement.

### `replace`

```python
replace(self, /, *, touch_state=Ellipsis)
```

Returns a validated replacement without changing this value.

#### Parameters

- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — Strictly prior history. None means unknown; untouched means known no hit.
#### Returns

- `object` — New instance of the same class; omitted fields or Ellipsis retain their values.
#### Raises

- `TypeError` — If a field is unknown or touch_state is not a string, None or Ellipsis.
- `ValueError` — If touch_state is an unknown choice.

### `settlement_timing`

Return at-hit or expiry payment; no-touch contracts settle only at expiry.

### `touch_state`

Returns strictly prior touch history, or None if unknown.

## `asset_binary_barrier_option`

```python
asset_binary_barrier_option(*, option_type, strike, effective_date, expiry_date, barrier_level, barrier_type, observation_mode=Ellipsis, observation_dates=Ellipsis, touch_state=None)
```

Create an asset digital with barrier monitoring and strict terminal
exercise.

#### Parameters

- **`option_type`** (`{'call', 'put'}`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive finite exercise or purchase price.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`barrier_level`** (`float`) — Positive finite trigger level; equality counts as a touch.
- **`barrier_type`** (`{'up_and_in', 'up_and_out', 'down_and_in', 'down_and_out'}`) — Trigger direction and knock-in or knock-out behavior.
- **`observation_mode`** (`{'continuous', 'scheduled'}, optional`) — Continuous monitoring or observations on the supplied dates.
- **`observation_dates`** (`iterable of date, optional`) — Strictly increasing observation dates within the contract life.
- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — Strictly prior history. None means unknown; untouched means known no hit.
#### Returns

- `BinaryBarrierOption` — Validated owned contract.
#### Raises

- `InvalidInputError` — If contractual amounts, life dates or observation terms are invalid.
#### Notes

Barrier equality counts as a touch. Strictly prior history and trading
calendar compatibility are checked during pricing. Terminal strike
equality pays zero.

## `asset_touch_option`

```python
asset_touch_option(*, effective_date, expiry_date, barrier_level, barrier_type, settlement_timing=Ellipsis, observation_mode=Ellipsis, observation_dates=Ellipsis, touch_state=None)
```

Creates a cash or asset one-touch or no-touch contract.

#### Parameters

- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`barrier_level`** (`float`) — Positive finite trigger level; equality counts as a touch.
- **`barrier_type`** (`{'up_and_in', 'up_and_out', 'down_and_in', 'down_and_out'}`) — In selects one-touch; out selects no-touch. Up/down selects direction.
- **`settlement_timing`** (`{'at_hit', 'at_expiry'}, optional`) — Defaults to expiry. At-hit settlement requires a one-touch contract.
- **`observation_mode`** (`{'continuous', 'scheduled'}, optional`) — Continuous monitoring or observations on the supplied dates.
- **`observation_dates`** (`iterable of date, optional`) — Strictly increasing observation dates within the contract life.
- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — Strictly prior history. None is unknown; untouched means known no hit.
#### Returns

- `TouchOption` — Validated owned contract. Asset settlement has no cash payout.
#### Raises

- `InvalidInputError` — If amounts, life dates or observation terms are invalid, or at-hit settlement is requested for a no-touch contract.
#### Notes

History and trading-calendar consistency are checked during pricing.
Prior at-hit payments have no remaining value. A current asset hit
transfers spot; a future continuous asset hit transfers the barrier amount.
See the kiyosi.instruments module examples for construction.

## `autocallable_observations`

```python
autocallable_observations(observation_dates, knock_out_levels, *, knock_out_coupon_rates=None, coupon_barrier_levels=None)
```

Associate parallel sequences into input observation records.

#### Parameters

- **`observation_dates`** (`iterable of date`) — Strictly increasing observation dates within the contract life.
- **`knock_out_levels`** (`iterable of float`) — Positive inclusive knock-out levels, one per observation date.
- **`knock_out_coupon_rates`** (`iterable of float or None, optional`) — Annual snowball coupons; None uses zero for every observation.
- **`coupon_barrier_levels`** (`iterable of float or None, optional`) — Phoenix coupon thresholds; None uses zero for every observation.
#### Returns

- `list of AutocallableObservation` — Owned result; no input is mutated.
#### Raises

- `InvalidInputError` — If sequence lengths differ.
#### Notes

The note constructor validates contractual values and ordering.

## `both_down_snowball`

```python
both_down_snowball(*, initial_coupon_rate, initial_spot, knock_in_level, initial_knock_out_level, coupon_rate_decrement, knock_out_level_decrement, observation_dates, effective_date, expiry_date, barrier_state=None, principal_ratio=Ellipsis)
```

Creates a snowball with decreasing coupons and knock-out levels.

#### Parameters

- **`initial_coupon_rate`** (`float`) — Annual coupon rate at the first observation.
- **`initial_spot`** (`float`) — Positive reference spot used to normalize downside losses.
- **`knock_in_level`** (`float`) — Positive strict downside threshold.
- **`initial_knock_out_level`** (`float`) — Positive knock-out threshold at the first observation.
- **`coupon_rate_decrement`** (`float`) — Absolute decimal-rate decrement after each observation.
- **`knock_out_level_decrement`** (`float`) — Absolute price decrement after each observation; may be negative.
- **`observation_dates`** (`iterable of date`) — Strictly increasing observation dates within the contract life.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`barrier_state`** (`{'none', 'knocked_in', 'knocked_out'} or None, optional`) — Strictly prior events. None is unknown; the string none means no event.
- **`principal_ratio`** (`float, optional`) — Nonnegative normalized principal, independent of coupons and losses.
#### Returns

- `SnowballOption` — Validated owned contract.
#### Raises

- `InvalidInputError` — If contractual amounts, life dates or observation terms are invalid.
#### Notes

Knock-in is observed on every trading day.
Unit principal, zero lower strike and initial spot as upper strike are used
unless the preset overrides them. History and trading-calendar consistency
are checked during pricing.
Decrements apply after each observation; the first uses the initial
value. Signed coupons and decrements are accepted if all expanded terms
remain valid. Maturity uses the final observation coupon.

## `butterfly_snowball`

```python
butterfly_snowball(*, first_coupon_rate, initial_spot, knock_in_level, knock_out_level, second_coupon_rate, third_coupon_rate, first_stage_end_date, second_stage_end_date, observation_dates, effective_date, expiry_date, barrier_state=None, principal_ratio=Ellipsis)
```

Creates a three-stage butterfly snowball.

#### Parameters

- **`first_coupon_rate`** (`float`) — Finite signed annual coupon through first_stage_end_date.
- **`initial_spot`** (`float`) — Positive reference spot used to normalize downside losses.
- **`knock_in_level`** (`float`) — Positive strict downside threshold.
- **`knock_out_level`** (`float`) — Positive inclusive knock-out threshold.
- **`second_coupon_rate`** (`float`) — Finite signed annual coupon in the second stage.
- **`third_coupon_rate`** (`float`) — Finite signed annual coupon in the third stage and at maturity.
- **`first_stage_end_date`** (`datetime.date`) — Inclusive first-stage end within life and before second_stage_end_date.
- **`second_stage_end_date`** (`datetime.date`) — Inclusive second-stage end strictly before expiry.
- **`observation_dates`** (`iterable of date`) — Strictly increasing observation dates within the contract life.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`barrier_state`** (`{'none', 'knocked_in', 'knocked_out'} or None, optional`) — Strictly prior events. None is unknown; the string none means no event.
- **`principal_ratio`** (`float, optional`) — Nonnegative normalized principal, independent of coupons and losses.
#### Returns

- `SnowballOption` — Validated owned contract.
#### Raises

- `InvalidInputError` — If contractual amounts, life dates or observation terms are invalid.
#### Notes

Knock-in is observed on every trading day.
Unit principal, zero lower strike and initial spot as upper strike are used
unless the preset overrides them. History and trading-calendar consistency
are checked during pricing.
Knock-out uses the observation's stage rate over the whole holding period.
Maturity uses the final stage rate. Cutoffs need not be observation or trading
dates, stages may have no observations, and rates need not decrease.

## `cash_binary_barrier_option`

```python
cash_binary_barrier_option(*, option_type, strike, effective_date, expiry_date, barrier_level, barrier_type, payout, observation_mode=Ellipsis, observation_dates=Ellipsis, touch_state=None)
```

Create a cash digital with barrier monitoring and strict terminal
exercise.

#### Parameters

- **`option_type`** (`{'call', 'put'}`) — Call or put payoff direction.
- **`strike`** (`float`) — Positive finite exercise or purchase price.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`barrier_level`** (`float`) — Positive finite trigger level; equality counts as a touch.
- **`barrier_type`** (`{'up_and_in', 'up_and_out', 'down_and_in', 'down_and_out'}`) — Trigger direction and knock-in or knock-out behavior.
- **`payout`** (`float`) — Positive finite cash payment.
- **`observation_mode`** (`{'continuous', 'scheduled'}, optional`) — Continuous monitoring or observations on the supplied dates.
- **`observation_dates`** (`iterable of date, optional`) — Strictly increasing observation dates within the contract life.
- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — Strictly prior history. None means unknown; untouched means known no hit.
#### Returns

- `BinaryBarrierOption` — Validated owned contract.
#### Raises

- `InvalidInputError` — If contractual amounts, life dates or observation terms are invalid.
#### Notes

Barrier equality counts as a touch. Strictly prior history and trading
calendar compatibility are checked during pricing. Terminal strike
equality pays zero.

## `cash_double_no_touch`

```python
cash_double_no_touch(*, effective_date, expiry_date, lower_barrier, upper_barrier, payout, observation_mode=Ellipsis, observation_dates=Ellipsis, touch_state=None)
```

Create an expiry cash payment requiring neither boundary to be touched.

#### Parameters

- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`lower_barrier`** (`float`) — Positive finite lower trigger; equality counts as a touch.
- **`upper_barrier`** (`float`) — Finite upper trigger, strictly above the lower trigger.
- **`payout`** (`float`) — Positive finite cash payment.
- **`observation_mode`** (`{'continuous', 'scheduled'}, optional`) — Continuous monitoring or observations on the supplied dates.
- **`observation_dates`** (`iterable of date, optional`) — Strictly increasing observation dates within the contract life.
- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — Strictly prior history. None means unknown; untouched means known no hit.
#### Returns

- `DoubleTouchOption` — Validated owned contract.
#### Raises

- `InvalidInputError` — If contractual amounts, life dates or observation terms are invalid.
#### Notes

Barrier equality counts as a touch. Strictly prior history and trading
calendar compatibility are checked during pricing. Prior at-hit
payments have no remaining value. No-touch payments occur only at
expiry.

## `cash_double_touch`

```python
cash_double_touch(*, effective_date, expiry_date, lower_barrier, upper_barrier, payout, settlement_timing=Ellipsis, observation_mode=Ellipsis, observation_dates=Ellipsis, touch_state=None)
```

Create a cash payment activated by either inclusive boundary.

#### Parameters

- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`lower_barrier`** (`float`) — Positive finite lower trigger; equality counts as a touch.
- **`upper_barrier`** (`float`) — Finite upper trigger, strictly above the lower trigger.
- **`payout`** (`float`) — Positive finite cash payment.
- **`settlement_timing`** (`{'at_hit', 'at_expiry'}, optional`) — At-hit or expiry payment; no-touch contracts settle only at expiry.
- **`observation_mode`** (`{'continuous', 'scheduled'}, optional`) — Continuous monitoring or observations on the supplied dates.
- **`observation_dates`** (`iterable of date, optional`) — Strictly increasing observation dates within the contract life.
- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — Strictly prior history. None means unknown; untouched means known no hit.
#### Returns

- `DoubleTouchOption` — Validated owned contract.
#### Raises

- `InvalidInputError` — If contractual amounts, life dates or observation terms are invalid.
#### Notes

Barrier equality counts as a touch. Strictly prior history and trading
calendar compatibility are checked during pricing. Prior at-hit
payments have no remaining value. No-touch payments occur only at
expiry.

## `cash_touch_option`

```python
cash_touch_option(*, effective_date, expiry_date, barrier_level, barrier_type, payout, settlement_timing=Ellipsis, observation_mode=Ellipsis, observation_dates=Ellipsis, touch_state=None)
```

Creates a cash or asset one-touch or no-touch contract.

#### Parameters

- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`barrier_level`** (`float`) — Positive finite trigger level; equality counts as a touch.
- **`barrier_type`** (`{'up_and_in', 'up_and_out', 'down_and_in', 'down_and_out'}`) — In selects one-touch; out selects no-touch. Up/down selects direction.
- **`payout`** (`float`) — Positive finite cash payment.
- **`settlement_timing`** (`{'at_hit', 'at_expiry'}, optional`) — Defaults to expiry. At-hit settlement requires a one-touch contract.
- **`observation_mode`** (`{'continuous', 'scheduled'}, optional`) — Continuous monitoring or observations on the supplied dates.
- **`observation_dates`** (`iterable of date, optional`) — Strictly increasing observation dates within the contract life.
- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — Strictly prior history. None is unknown; untouched means known no hit.
#### Returns

- `TouchOption` — Validated owned contract. Asset settlement has no cash payout.
#### Raises

- `InvalidInputError` — If amounts, life dates or observation terms are invalid, or at-hit settlement is requested for a no-touch contract.
#### Notes

History and trading-calendar consistency are checked during pricing.
Prior at-hit payments have no remaining value. A current asset hit
transfers spot; a future continuous asset hit transfers the barrier amount.
See the kiyosi.instruments module examples for construction.

## `digital_coupon_note`

```python
digital_coupon_note(*, coupon_per_period, initial_spot, knock_in_level, knock_out_level, coupon_barrier_level, observation_dates, effective_date, expiry_date, barrier_state=None, principal_ratio=Ellipsis)
```

Creates a DCN with fixed per-period coupons conditional on an explicit barrier.

#### Parameters

- **`coupon_per_period`** (`float`) — Finite signed coupon proportion per qualifying observation; not annualized.
- **`initial_spot`** (`float`) — Positive reference spot used to normalize downside losses.
- **`knock_in_level`** (`float`) — Positive strict expiry knock-in threshold and upper settlement strike.
- **`knock_out_level`** (`float`) — Positive inclusive knock-out threshold.
- **`coupon_barrier_level`** (`float`) — Finite nonnegative inclusive coupon threshold, also tested on KO dates.
- **`observation_dates`** (`iterable of datetime.date`) — Strictly increasing observation and payment dates within life.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date at midnight UTC.
- **`barrier_state`** (`{'none', 'knocked_in', 'knocked_out'} or None, optional`) — Strictly prior events; None means unknown history.
- **`principal_ratio`** (`float, optional`) — Nonnegative normalized principal, independent of coupon and loss components.
#### Returns

- `PhoenixOption` — Validated owned contract, with expiry-only knock-in and zero lower strike.
#### Raises

- `InvalidInputError` — If numeric terms, dates or observations are invalid.
#### Notes

Coupons pay once per qualifying observation, including a qualifying KO,
with no day accrual or memory. KO and coupon barriers are inclusive;
knock-in is strict. Observation dates are payment dates; no observation
is implicitly added at expiry. Calendar and history consistency are
checked during pricing. Past coupons are settled.

## `dual_coupon_snowball`

```python
dual_coupon_snowball(*, knock_out_coupon_rate, initial_spot, knock_in_level, knock_out_level, maturity_coupon_rate, observation_dates, effective_date, expiry_date, barrier_state=None, principal_ratio=Ellipsis)
```

Creates a snowball with separate knock-out and maturity coupons.

#### Parameters

- **`knock_out_coupon_rate`** (`float`) — Annual coupon rate for knock-out settlement.
- **`initial_spot`** (`float`) — Positive reference spot used to normalize downside losses.
- **`knock_in_level`** (`float`) — Positive strict downside threshold.
- **`knock_out_level`** (`float`) — Positive inclusive knock-out threshold.
- **`maturity_coupon_rate`** (`float`) — Finite annual maturity coupon rate in decimal units.
- **`observation_dates`** (`iterable of date`) — Strictly increasing observation dates within the contract life.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`barrier_state`** (`{'none', 'knocked_in', 'knocked_out'} or None, optional`) — Strictly prior events. None is unknown; the string none means no event.
- **`principal_ratio`** (`float, optional`) — Nonnegative normalized principal, independent of coupons and losses.
#### Returns

- `SnowballOption` — Validated owned contract.
#### Raises

- `InvalidInputError` — If contractual amounts, life dates or observation terms are invalid.
#### Notes

Knock-in is observed on every trading day.
Unit principal, zero lower strike and initial spot as upper strike are used
unless the preset overrides them. History and trading-calendar consistency
are checked during pricing.

## `early_profit_snowball`

```python
early_profit_snowball(*, first_coupon_rate, initial_spot, knock_in_level, knock_out_level, second_coupon_rate, first_stage_end_date, observation_dates, effective_date, expiry_date, barrier_state=None, principal_ratio=Ellipsis)
```

Creates a two-stage early-profit snowball.

#### Parameters

- **`first_coupon_rate`** (`float`) — Finite signed annual coupon through first_stage_end_date.
- **`initial_spot`** (`float`) — Positive reference spot used to normalize downside losses.
- **`knock_in_level`** (`float`) — Positive strict downside threshold.
- **`knock_out_level`** (`float`) — Positive inclusive knock-out threshold.
- **`second_coupon_rate`** (`float`) — Finite signed annual coupon after the cutoff and at maturity.
- **`first_stage_end_date`** (`datetime.date`) — Inclusive first-stage end within life and strictly before expiry.
- **`observation_dates`** (`iterable of date`) — Strictly increasing observation dates within the contract life.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`barrier_state`** (`{'none', 'knocked_in', 'knocked_out'} or None, optional`) — Strictly prior events. None is unknown; the string none means no event.
- **`principal_ratio`** (`float, optional`) — Nonnegative normalized principal, independent of coupons and losses.
#### Returns

- `SnowballOption` — Validated owned contract.
#### Raises

- `InvalidInputError` — If contractual amounts, life dates or observation terms are invalid.
#### Notes

Knock-in is observed on every trading day.
Unit principal, zero lower strike and initial spot as upper strike are used
unless the preset overrides them. History and trading-calendar consistency
are checked during pricing.
Knock-out uses the observation's stage rate over the whole holding period.
Maturity uses the final stage rate. Cutoffs need not be observation or trading
dates, stages may have no observations, and rates need not decrease.

## `european_snowball`

```python
european_snowball(*, coupon_rate, initial_spot, knock_in_level, knock_out_level, observation_dates, effective_date, expiry_date, barrier_state=None, principal_ratio=Ellipsis)
```

Creates a snowball with knock-in observed only at expiry.

#### Parameters

- **`coupon_rate`** (`float`) — Finite annual coupon rate in decimal units.
- **`initial_spot`** (`float`) — Positive reference spot used to normalize downside losses.
- **`knock_in_level`** (`float`) — Positive strict downside threshold.
- **`knock_out_level`** (`float`) — Positive inclusive knock-out threshold.
- **`observation_dates`** (`iterable of date`) — Strictly increasing observation dates within the contract life.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`barrier_state`** (`{'none', 'knocked_in', 'knocked_out'} or None, optional`) — Strictly prior events. None is unknown; the string none means no event.
- **`principal_ratio`** (`float, optional`) — Nonnegative normalized principal, independent of coupons and losses.
#### Returns

- `SnowballOption` — Validated owned contract.
#### Raises

- `InvalidInputError` — If contractual amounts, life dates or observation terms are invalid.
#### Notes

Knock-in is observed only at expiry.
Unit principal, zero lower strike and initial spot as upper strike are used
unless the preset overrides them. History and trading-calendar consistency
are checked during pricing.

## `fixed_coupon_note`

```python
fixed_coupon_note(*, coupon_per_period, initial_spot, knock_in_level, knock_out_level, observation_dates, effective_date, expiry_date, barrier_state=None, principal_ratio=Ellipsis)
```

Creates an FCN with an unconditional fixed coupon at each surviving observation.

#### Parameters

- **`coupon_per_period`** (`float`) — Finite signed coupon proportion per qualifying observation; not annualized.
- **`initial_spot`** (`float`) — Positive reference spot used to normalize downside losses.
- **`knock_in_level`** (`float`) — Positive strict expiry knock-in threshold and upper settlement strike.
- **`knock_out_level`** (`float`) — Positive inclusive knock-out threshold.
- **`observation_dates`** (`iterable of datetime.date`) — Strictly increasing observation and payment dates within life.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date at midnight UTC.
- **`barrier_state`** (`{'none', 'knocked_in', 'knocked_out'} or None, optional`) — Strictly prior events; None means unknown history.
- **`principal_ratio`** (`float, optional`) — Nonnegative normalized principal, independent of coupon and loss components.
#### Returns

- `PhoenixOption` — Validated owned contract, with expiry-only knock-in and zero lower strike.
#### Raises

- `InvalidInputError` — If numeric terms, dates or observations are invalid.
#### Notes

Coupons pay once per qualifying observation, including a qualifying KO,
with no day accrual or memory. KO and coupon barriers are inclusive;
knock-in is strict. Observation dates are payment dates; no observation
is implicitly added at expiry. Calendar and history consistency are
checked during pricing. Past coupons are settled.

## `loss_capped_snowball`

```python
loss_capped_snowball(*, coupon_rate, initial_spot, knock_in_level, knock_out_level, lower_strike, observation_dates, effective_date, expiry_date, barrier_state=None, principal_ratio=Ellipsis)
```

Creates a snowball whose lower terminal strike caps downside loss.

#### Parameters

- **`coupon_rate`** (`float`) — Finite annual coupon rate in decimal units.
- **`initial_spot`** (`float`) — Positive reference spot used to normalize downside losses.
- **`knock_in_level`** (`float`) — Positive strict downside threshold.
- **`knock_out_level`** (`float`) — Positive inclusive knock-out threshold.
- **`lower_strike`** (`float`) — Nonnegative lower terminal strike, at most the upper strike.
- **`observation_dates`** (`iterable of date`) — Strictly increasing observation dates within the contract life.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`barrier_state`** (`{'none', 'knocked_in', 'knocked_out'} or None, optional`) — Strictly prior events. None is unknown; the string none means no event.
- **`principal_ratio`** (`float, optional`) — Nonnegative normalized principal, independent of coupons and losses.
#### Returns

- `SnowballOption` — Validated owned contract.
#### Raises

- `InvalidInputError` — If contractual amounts, life dates or observation terms are invalid.
#### Notes

Knock-in is observed on every trading day.
Unit principal, zero lower strike and initial spot as upper strike are used
unless the preset overrides them. History and trading-calendar consistency
are checked during pricing.

## `otm_snowball`

```python
otm_snowball(*, coupon_rate, initial_spot, knock_in_level, knock_out_level, upper_strike, observation_dates, effective_date, expiry_date, barrier_state=None, principal_ratio=Ellipsis)
```

Creates a snowball with a replaced upper terminal strike.

#### Parameters

- **`coupon_rate`** (`float`) — Finite annual coupon rate in decimal units.
- **`initial_spot`** (`float`) — Positive reference spot used to normalize downside losses.
- **`knock_in_level`** (`float`) — Positive strict downside threshold.
- **`knock_out_level`** (`float`) — Positive inclusive knock-out threshold.
- **`upper_strike`** (`float`) — Positive upper terminal settlement strike.
- **`observation_dates`** (`iterable of date`) — Strictly increasing observation dates within the contract life.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`barrier_state`** (`{'none', 'knocked_in', 'knocked_out'} or None, optional`) — Strictly prior events. None is unknown; the string none means no event.
- **`principal_ratio`** (`float, optional`) — Nonnegative normalized principal, independent of coupons and losses.
#### Returns

- `SnowballOption` — Validated owned contract.
#### Raises

- `InvalidInputError` — If contractual amounts, life dates or observation terms are invalid.
#### Notes

Knock-in is observed on every trading day.
Unit principal, zero lower strike and initial spot as upper strike are used
unless the preset overrides them. History and trading-calendar consistency
are checked during pricing.

## `parachute_snowball`

```python
parachute_snowball(*, coupon_rate, initial_spot, knock_in_level, knock_out_level, final_knock_out_level, observation_dates, effective_date, expiry_date, barrier_state=None, principal_ratio=Ellipsis)
```

Creates a snowball with a distinct final knock-out level.

#### Parameters

- **`coupon_rate`** (`float`) — Finite annual coupon rate in decimal units.
- **`initial_spot`** (`float`) — Positive reference spot used to normalize downside losses.
- **`knock_in_level`** (`float`) — Positive strict downside threshold.
- **`knock_out_level`** (`float`) — Positive inclusive knock-out threshold.
- **`final_knock_out_level`** (`float`) — Positive threshold replacing only the final knock-out level.
- **`observation_dates`** (`iterable of date`) — Strictly increasing observation dates within the contract life.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`barrier_state`** (`{'none', 'knocked_in', 'knocked_out'} or None, optional`) — Strictly prior events. None is unknown; the string none means no event.
- **`principal_ratio`** (`float, optional`) — Nonnegative normalized principal, independent of coupons and losses.
#### Returns

- `SnowballOption` — Validated owned contract.
#### Raises

- `InvalidInputError` — If contractual amounts, life dates or observation terms are invalid.
#### Notes

Knock-in is observed on every trading day.
Unit principal, zero lower strike and initial spot as upper strike are used
unless the preset overrides them. History and trading-calendar consistency
are checked during pricing.

## `standard_snowball`

```python
standard_snowball(*, coupon_rate, initial_spot, knock_in_level, knock_out_level, observation_dates, effective_date, expiry_date, barrier_state=None, principal_ratio=Ellipsis)
```

Creates constant knock-out coupons and levels with daily knock-in monitoring.

#### Parameters

- **`coupon_rate`** (`float`) — Finite annual coupon rate in decimal units.
- **`initial_spot`** (`float`) — Positive reference spot used to normalize downside losses.
- **`knock_in_level`** (`float`) — Positive strict downside threshold.
- **`knock_out_level`** (`float`) — Positive inclusive knock-out threshold.
- **`observation_dates`** (`iterable of date`) — Strictly increasing observation dates within the contract life.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`barrier_state`** (`{'none', 'knocked_in', 'knocked_out'} or None, optional`) — Strictly prior events. None is unknown; the string none means no event.
- **`principal_ratio`** (`float, optional`) — Nonnegative normalized principal, independent of coupons and losses.
#### Returns

- `SnowballOption` — Validated owned contract.
#### Raises

- `InvalidInputError` — If contractual amounts, life dates or observation terms are invalid.
#### Notes

Knock-in is observed on every trading day.
Unit principal, zero lower strike and initial spot as upper strike are used
unless the preset overrides them. History and trading-calendar consistency
are checked during pricing.

## `step_down_snowball`

```python
step_down_snowball(*, coupon_rate, initial_spot, knock_in_level, initial_knock_out_level, knock_out_level_decrement, observation_dates, effective_date, expiry_date, barrier_state=None, principal_ratio=Ellipsis)
```

Creates a snowball with decreasing knock-out levels.

#### Parameters

- **`coupon_rate`** (`float`) — Finite annual coupon rate in decimal units.
- **`initial_spot`** (`float`) — Positive reference spot used to normalize downside losses.
- **`knock_in_level`** (`float`) — Positive strict downside threshold.
- **`initial_knock_out_level`** (`float`) — Positive knock-out threshold at the first observation.
- **`knock_out_level_decrement`** (`float`) — Absolute price decrement after each observation; may be negative.
- **`observation_dates`** (`iterable of date`) — Strictly increasing observation dates within the contract life.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`barrier_state`** (`{'none', 'knocked_in', 'knocked_out'} or None, optional`) — Strictly prior events. None is unknown; the string none means no event.
- **`principal_ratio`** (`float, optional`) — Nonnegative normalized principal, independent of coupons and losses.
#### Returns

- `SnowballOption` — Validated owned contract.
#### Raises

- `InvalidInputError` — If contractual amounts, life dates or observation terms are invalid.
#### Notes

Knock-in is observed on every trading day.
Unit principal, zero lower strike and initial spot as upper strike are used
unless the preset overrides them. History and trading-calendar consistency
are checked during pricing.
Decrements apply after each observation; the first uses the initial
value. Signed coupons and decrements are accepted if all expanded terms
remain valid.
