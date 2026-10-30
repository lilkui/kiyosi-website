---
description: kiyosi.instruments 的 Python API 参考文档。
outline: [2, 4]
---

# `kiyosi.instruments`

Validated derivative contracts, snowball presets and observation adapters.

``OptionType`` selects ``"call"`` or ``"put"``. Contract dates are inclusive,
with expiry at midnight UTC. Constructors validate terms; pricing validates
their consistency with the market snapshot, calendar and supplied history.
History describes events strictly before valuation; a current observation
is evaluated from the current spot. Replacement returns a new contract.

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

## `Accumulator`

```python
Accumulator(*, strike, knock_out_level, daily_quantity, acceleration_factor, effective_date, expiry_date, **history)
```

Trading-date purchases settled at knock-out or expiry.

#### Parameters

- **`strike`** (`float`) — Positive finite exercise or purchase price.
- **`knock_out_level`** (`float`) — Positive inclusive knock-out threshold.
- **`daily_quantity`** (`float`) — Nonnegative finite quantity purchased on each trading date.
- **`acceleration_factor`** (`float`) — Nonnegative quantity multiplier applied strictly below strike.
- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`accumulated_quantity`** (`float, optional`) — Caller-asserted outstanding quantity strictly before valuation.
#### Raises

- `InvalidInputError` — If strike or knock-out level is invalid, quantities are negative or non-finite, or expiry precedes effective_date.
#### Notes

A current midnight knock-out precedes purchases and purchases no units.
Acceleration applies strictly below strike. History is caller asserted;
do not value a contract whose settlement has already occurred.

### `acceleration_factor`

Return nonnegative quantity multiplier applied strictly below strike.

### `accumulated_quantity`

Return caller-asserted outstanding quantity strictly before valuation.

### `daily_quantity`

Return nonnegative finite quantity purchased on each trading date.

### `effective_date`

Return inclusive first contract date.

### `expiry_date`

Return final contract date; expiry is at midnight UTC.

### `knock_out_level`

Return positive inclusive knock-out threshold.

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

Return the exercise or purchase price in underlying price units.

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
replace(self, /, **fields)
```

Return a validated replacement without changing this value.

#### Parameters

- **`option_type`** (`{'call', 'put'}, optional`) — Call or put payoff direction.
- **`strike`** (`float, optional`) — Positive finite exercise or purchase price.
- **`effective_date`** (`datetime.date, optional`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date, optional`) — Final contract date; expiry is at midnight UTC.
#### Returns

- `object` — New instance of the same class; omitted fields retain their values.
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
replace(self, /, **fields)
```

Return a validated replacement without changing this value.

#### Parameters

- **`realized_average`** (`float, optional`) — Prior average; zero denotes no history. Pricing checks time consistency.
#### Returns

- `object` — New instance of the same class; omitted fields retain their values.
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
replace(self, /, **fields)
```

Return a validated replacement without changing this value.

#### Parameters

- **`option_type`** (`{'call', 'put'}, optional`) — Call or put payoff direction.
- **`strike`** (`float, optional`) — Positive finite exercise or purchase price.
- **`payout`** (`float, optional`) — Positive finite cash payment; accepted only for CashOrNothingOption.
- **`effective_date`** (`datetime.date, optional`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date, optional`) — Final contract date; expiry is at midnight UTC.
#### Returns

- `object` — New instance of the same class; omitted fields retain their values.
#### Raises

- `KiyosiError` — If replacement terms fail domain validation. The original is unchanged.

### `strike`

Return the exercise or purchase price in underlying price units.

## `AutocallableObservation`

```python
AutocallableObservation(date, knock_out_level, **fields)
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
BarrierOption(*, option_type, strike, effective_date, expiry_date, barrier_level, barrier_type, **settings)
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

Return inclusive first contract date.

### `expiry_date`

Return final contract date; expiry is at midnight UTC.

### `mean_observation_year_fraction`

Return mean fixing spacing in Actual/365 Fixed years.

### `observation_dates`

Return a copy of the contractual observation dates.

### `observation_mode`

Return continuous monitoring or observations on the supplied dates.

### `observation_schedule`

Return an owned copy of the monitoring schedule.

### `option_type`

Return call or put payoff direction.

### `rebate`

Return nonnegative finite cash rebate; defaults to zero.

### `rebate_timing`

Return payment timing; at-hit rebates are valid only for knock-outs.

### `replace`

```python
replace(self, /, **fields)
```

Return a validated replacement without changing this value.

#### Parameters

- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — Strictly prior history. None means unknown; untouched means known no hit.
#### Returns

- `object` — New instance of the same class; omitted fields retain their values.
#### Raises

- `KiyosiError` — If replacement terms fail domain validation. The original is unchanged.

### `strike`

Return the exercise or purchase price in underlying price units.

### `touch_state`

Return strictly prior touch history, or None if unknown.

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

Return inclusive first contract date.

### `expiry_date`

Return final contract date; expiry is at midnight UTC.

### `mean_observation_year_fraction`

Return mean fixing spacing in Actual/365 Fixed years.

### `observation_dates`

Return a copy of the contractual observation dates.

### `observation_mode`

Return continuous monitoring or observations on the supplied dates.

### `observation_schedule`

Return an owned copy of the monitoring schedule.

### `option_type`

Return call or put payoff direction.

### `payoff_type`

Return cash or asset settlement as a choice string.

### `payout`

Return the cash payout, or None for asset settlement.

### `replace`

```python
replace(self, /, **fields)
```

Return a validated replacement without changing this value.

#### Parameters

- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — Strictly prior history. None means unknown; untouched means known no hit.
#### Returns

- `object` — New instance of the same class; omitted fields retain their values.
#### Raises

- `KiyosiError` — If replacement terms fail domain validation. The original is unchanged.

### `strike`

Return the exercise or purchase price in underlying price units.

### `touch_state`

Return strictly prior touch history, or None if unknown.

## `BinarySnowballOption`

```python
BinarySnowballOption(*, maturity_coupon_rate, effective_date, expiry_date, observations, barrier_state=None, **fields)
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

Return strictly prior autocallable history, or None if unknown.

### `effective_date`

Return inclusive first contract date.

### `expiry_date`

Return final contract date; expiry is at midnight UTC.

### `knock_out_coupon_rates`

Return copied annual knock-out coupons in observation order.

### `knock_out_levels`

Return copied knock-out thresholds in observation order.

### `maturity_coupon_rate`

Return finite annual maturity coupon rate in decimal units.

### `observation_dates`

Return a copy of the contractual observation dates.

### `observations`

Return owned copies of the contractual observations.

### `principal_ratio`

Return nonnegative normalized principal, independent of coupons and losses.

### `replace`

```python
replace(self, /, *, barrier_state)
```

Return a validated replacement without changing this value.

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
replace(self, /, **fields)
```

Return a validated replacement without changing this value.

#### Parameters

- **`option_type`** (`{'call', 'put'}, optional`) — Call or put payoff direction.
- **`strike`** (`float, optional`) — Positive finite exercise or purchase price.
- **`payout`** (`float, optional`) — Positive finite cash payment; accepted only for CashOrNothingOption.
- **`effective_date`** (`datetime.date, optional`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date, optional`) — Final contract date; expiry is at midnight UTC.
#### Returns

- `object` — New instance of the same class; omitted fields retain their values.
#### Raises

- `KiyosiError` — If replacement terms fail domain validation. The original is unchanged.

### `strike`

Return the exercise or purchase price in underlying price units.

## `DoubleBarrierOption`

```python
DoubleBarrierOption(*, option_type, strike, effective_date, expiry_date, lower_barrier, upper_barrier, barrier_type, **settings)
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

Return inclusive first contract date.

### `expiry_date`

Return final contract date; expiry is at midnight UTC.

### `lower_barrier`

Return positive finite lower trigger; equality counts as a touch.

### `observation_dates`

Return a copy of the contractual observation dates.

### `observation_mode`

Return continuous monitoring or observations on the supplied dates.

### `observation_schedule`

Return an owned copy of the monitoring schedule.

### `option_type`

Return call or put payoff direction.

### `rebate`

Return nonnegative finite cash rebate; defaults to zero.

### `rebate_timing`

Return payment timing; at-hit rebates are valid only for knock-outs.

### `replace`

```python
replace(self, /, **fields)
```

Return a validated replacement without changing this value.

#### Parameters

- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — Strictly prior history. None means unknown; untouched means known no hit.
#### Returns

- `object` — New instance of the same class; omitted fields retain their values.
#### Raises

- `KiyosiError` — If replacement terms fail domain validation. The original is unchanged.

### `strike`

Return the exercise or purchase price in underlying price units.

### `touch_state`

Return strictly prior touch history, or None if unknown.

### `upper_barrier`

Return finite upper trigger, strictly above the lower trigger.

## `DoubleTouchOption`

Cash one-touch or no-touch contract with two inclusive boundaries.

#### Notes

Construct with cash_double_touch or cash_double_no_touch. Prior at-hit
payments have no remaining value.

### `effective_date`

Return inclusive first contract date.

### `expiry_date`

Return final contract date; expiry is at midnight UTC.

### `is_one_touch`

Return whether touching activates payment.

### `lower_barrier`

Return positive finite lower trigger; equality counts as a touch.

### `observation_dates`

Return a copy of the contractual observation dates.

### `observation_mode`

Return continuous monitoring or observations on the supplied dates.

### `observation_schedule`

Return an owned copy of the monitoring schedule.

### `payout`

Return the nonnegative finite cash payout.

### `replace`

```python
replace(self, /, **fields)
```

Return a validated replacement without changing this value.

#### Parameters

- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — Strictly prior history. None means unknown; untouched means known no hit.
#### Returns

- `object` — New instance of the same class; omitted fields retain their values.
#### Raises

- `KiyosiError` — If replacement terms fail domain validation. The original is unchanged.

### `settlement_timing`

Return at-hit or expiry payment; no-touch contracts settle only at expiry.

### `touch_state`

Return strictly prior touch history, or None if unknown.

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
replace(self, /, **fields)
```

Return a validated replacement without changing this value.

#### Parameters

- **`realized_average`** (`float, optional`) — Prior average; zero denotes no history. Pricing checks time consistency.
#### Returns

- `object` — New instance of the same class; omitted fields retain their values.
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
PhoenixOption(*, coupon_rate, initial_spot, knock_in_level, upper_strike, lower_strike, knock_in_observation_mode, effective_date, expiry_date, observations, barrier_state=None, **fields)
```

Autocallable with conditional period coupons and capped downside loss.

#### Parameters

- **`coupon_rate`** (`float`) — Finite annual coupon rate in decimal units.
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

- `InvalidInputError` — If amounts, strikes, life dates or observations are invalid. Observation coupon_rate must be zero; coupon_barrier_level is nonnegative.
#### Notes

Coupons accrue over contractual observation periods on Actual/365 Fixed.
Coupon and knock-out barriers are inclusive; knock-in is strict. Past
coupons are settled. There is no coupon memory or maturity coupon.

### `barrier_state`

Return strictly prior autocallable history, or None if unknown.

### `coupon_barrier_levels`

Return copied Phoenix coupon thresholds in observation order.

### `coupon_rate`

Return finite annual coupon rate in decimal units.

### `effective_date`

Return inclusive first contract date.

### `expiry_date`

Return final contract date; expiry is at midnight UTC.

### `initial_spot`

Return positive reference spot used to normalize downside losses.

### `knock_in_level`

Return positive strict downside threshold.

### `knock_in_observation_mode`

Return the knock-in monitoring choice string.

### `knock_out_levels`

Return copied knock-out thresholds in observation order.

### `lower_strike`

Return nonnegative lower terminal strike, at most the upper strike.

### `observation_dates`

Return a copy of the contractual observation dates.

### `observations`

Return owned copies of the contractual observations.

### `principal_ratio`

Return nonnegative normalized principal, independent of coupons and losses.

### `replace`

```python
replace(self, /, *, barrier_state)
```

Return a validated replacement without changing this value.

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
replace(self, /, **fields)
```

Return a validated replacement without changing this value.

#### Parameters

- **`realized_hit_count`** (`int or None, optional`) — Hits strictly before valuation, or None for unknown history.
#### Returns

- `object` — New instance of the same class; omitted fields retain their values.
#### Raises

- `KiyosiError` — If replacement terms fail domain validation. The original is unchanged.

### `upper_bound`

Return inclusive finite upper spot boundary, above the lower boundary.

## `SnowballOption`

```python
SnowballOption(*, maturity_coupon_rate, initial_spot, knock_in_level, upper_strike, lower_strike, knock_in_observation_mode, effective_date, expiry_date, observations, barrier_state=None, **fields)
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

Return strictly prior autocallable history, or None if unknown.

### `effective_date`

Return inclusive first contract date.

### `expiry_date`

Return final contract date; expiry is at midnight UTC.

### `initial_spot`

Return positive reference spot used to normalize downside losses.

### `knock_in_level`

Return positive strict downside threshold.

### `knock_in_observation_mode`

Return the knock-in monitoring choice string.

### `knock_out_coupon_rates`

Return copied annual knock-out coupons in observation order.

### `knock_out_levels`

Return copied knock-out thresholds in observation order.

### `lower_strike`

Return nonnegative lower terminal strike, at most the upper strike.

### `maturity_coupon_rate`

Return finite annual maturity coupon rate in decimal units.

### `observation_dates`

Return a copy of the contractual observation dates.

### `observations`

Return owned copies of the contractual observations.

### `principal_ratio`

Return nonnegative normalized principal, independent of coupons and losses.

### `replace`

```python
replace(self, /, *, barrier_state)
```

Return a validated replacement without changing this value.

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
TernarySnowballOption(*, maturity_coupon_rate, minimum_coupon_rate, knock_in_level, knock_in_observation_mode, effective_date, expiry_date, observations, barrier_state=None, **fields)
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

Return strictly prior autocallable history, or None if unknown.

### `effective_date`

Return inclusive first contract date.

### `expiry_date`

Return final contract date; expiry is at midnight UTC.

### `knock_in_level`

Return positive strict downside threshold.

### `knock_in_observation_mode`

Return the knock-in monitoring choice string.

### `knock_out_coupon_rates`

Return copied annual knock-out coupons in observation order.

### `knock_out_levels`

Return copied knock-out thresholds in observation order.

### `maturity_coupon_rate`

Return finite annual maturity coupon rate in decimal units.

### `minimum_coupon_rate`

Return the annual knocked-in maturity coupon.

### `observation_dates`

Return a copy of the contractual observation dates.

### `observations`

Return owned copies of the contractual observations.

### `principal_ratio`

Return nonnegative normalized principal, independent of coupons and losses.

### `replace`

```python
replace(self, /, *, barrier_state)
```

Return a validated replacement without changing this value.

#### Parameters

- **`barrier_state`** (`{'none', 'knocked_in', 'knocked_out'} or None`) — Strictly prior events. None is unknown; the string none means no event.
#### Returns

- `object` — New instance of the same class; omitted fields retain their values.
#### Raises

- `KiyosiError` — If replacement terms fail domain validation. The original is unchanged.

## `TouchOption`

Strike-free cash or asset one-touch or no-touch contract.

#### Notes

Use a directional factory such as cash_one_touch_up or asset_no_touch_down.
Prior at-hit payments are settled.

### `barrier_level`

Return positive finite trigger level; equality counts as a touch.

### `barrier_type`

Return trigger direction and knock-in or knock-out behavior.

### `effective_date`

Return inclusive first contract date.

### `expiry_date`

Return final contract date; expiry is at midnight UTC.

### `is_one_touch`

Return whether touching activates payment.

### `is_up`

Return whether the barrier triggers upward.

### `mean_observation_year_fraction`

Return mean fixing spacing in Actual/365 Fixed years.

### `observation_dates`

Return a copy of the contractual observation dates.

### `observation_mode`

Return continuous monitoring or observations on the supplied dates.

### `observation_schedule`

Return an owned copy of the monitoring schedule.

### `payoff_type`

Return cash or asset settlement as a choice string.

### `payout`

Return the cash payout, or None for asset settlement.

### `replace`

```python
replace(self, /, **fields)
```

Return a validated replacement without changing this value.

#### Parameters

- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — Strictly prior history. None means unknown; untouched means known no hit.
#### Returns

- `object` — New instance of the same class; omitted fields retain their values.
#### Raises

- `KiyosiError` — If replacement terms fail domain validation. The original is unchanged.

### `settlement_timing`

Return at-hit or expiry payment; no-touch contracts settle only at expiry.

### `touch_state`

Return strictly prior touch history, or None if unknown.

## `asset_binary_barrier_option`

```python
asset_binary_barrier_option(*, option_type, strike, effective_date, expiry_date, barrier_level, barrier_type, **settings)
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

## `asset_no_touch_down`

```python
asset_no_touch_down(*, effective_date, expiry_date, barrier_level, **settings)
```

Create an asset payment requiring no downward barrier touch.

#### Parameters

- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`barrier_level`** (`float`) — Positive finite trigger level; equality counts as a touch.
- **`observation_mode`** (`{'continuous', 'scheduled'}, optional`) — Continuous monitoring or observations on the supplied dates.
- **`observation_dates`** (`iterable of date, optional`) — Strictly increasing observation dates within the contract life.
- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — Strictly prior history. None means unknown; untouched means known no hit.
#### Returns

- `TouchOption` — Validated owned contract.
#### Raises

- `InvalidInputError` — If contractual amounts, life dates or observation terms are invalid.
#### Notes

Barrier equality counts as a touch. Strictly prior history and trading
calendar compatibility are checked during pricing. A current at-hit
payment transfers spot; future continuous hits transfer the barrier
amount. No-touch payments occur only at expiry.

## `asset_no_touch_up`

```python
asset_no_touch_up(*, effective_date, expiry_date, barrier_level, **settings)
```

Create an asset payment requiring no upward barrier touch.

#### Parameters

- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`barrier_level`** (`float`) — Positive finite trigger level; equality counts as a touch.
- **`observation_mode`** (`{'continuous', 'scheduled'}, optional`) — Continuous monitoring or observations on the supplied dates.
- **`observation_dates`** (`iterable of date, optional`) — Strictly increasing observation dates within the contract life.
- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — Strictly prior history. None means unknown; untouched means known no hit.
#### Returns

- `TouchOption` — Validated owned contract.
#### Raises

- `InvalidInputError` — If contractual amounts, life dates or observation terms are invalid.
#### Notes

Barrier equality counts as a touch. Strictly prior history and trading
calendar compatibility are checked during pricing. A current at-hit
payment transfers spot; future continuous hits transfer the barrier
amount. No-touch payments occur only at expiry.

## `asset_one_touch_down`

```python
asset_one_touch_down(*, effective_date, expiry_date, barrier_level, **settings)
```

Create an asset payment activated by downward barrier touch.

#### Parameters

- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`barrier_level`** (`float`) — Positive finite trigger level; equality counts as a touch.
- **`settlement_timing`** (`{'at_hit', 'at_expiry'}, optional`) — At-hit or expiry payment; no-touch contracts settle only at expiry.
- **`observation_mode`** (`{'continuous', 'scheduled'}, optional`) — Continuous monitoring or observations on the supplied dates.
- **`observation_dates`** (`iterable of date, optional`) — Strictly increasing observation dates within the contract life.
- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — Strictly prior history. None means unknown; untouched means known no hit.
#### Returns

- `TouchOption` — Validated owned contract.
#### Raises

- `InvalidInputError` — If contractual amounts, life dates or observation terms are invalid.
#### Notes

Barrier equality counts as a touch. Strictly prior history and trading
calendar compatibility are checked during pricing. A current at-hit
payment transfers spot; future continuous hits transfer the barrier
amount. No-touch payments occur only at expiry.

## `asset_one_touch_up`

```python
asset_one_touch_up(*, effective_date, expiry_date, barrier_level, **settings)
```

Create an asset payment activated by upward barrier touch.

#### Parameters

- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`barrier_level`** (`float`) — Positive finite trigger level; equality counts as a touch.
- **`settlement_timing`** (`{'at_hit', 'at_expiry'}, optional`) — At-hit or expiry payment; no-touch contracts settle only at expiry.
- **`observation_mode`** (`{'continuous', 'scheduled'}, optional`) — Continuous monitoring or observations on the supplied dates.
- **`observation_dates`** (`iterable of date, optional`) — Strictly increasing observation dates within the contract life.
- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — Strictly prior history. None means unknown; untouched means known no hit.
#### Returns

- `TouchOption` — Validated owned contract.
#### Raises

- `InvalidInputError` — If contractual amounts, life dates or observation terms are invalid.
#### Notes

Barrier equality counts as a touch. Strictly prior history and trading
calendar compatibility are checked during pricing. A current at-hit
payment transfers spot; future continuous hits transfer the barrier
amount. No-touch payments occur only at expiry.

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
both_down_snowball(*, initial_coupon_rate, initial_spot, knock_in_level, initial_knock_out_level, coupon_rate_decrement, knock_out_level_decrement, observation_dates, effective_date, expiry_date, barrier_state=None, **fields)
```

Create a snowball with decreasing coupons and knock-out levels.

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

Daily knock-in monitoring, unit principal, zero lower strike and initial
spot as upper strike are used unless the preset overrides them. History
and trading-calendar consistency are checked during pricing.
Decrements apply after each observation; the first uses the initial
value. Signed coupons and decrements are accepted if all expanded terms
remain valid. Maturity uses the final observation coupon.

## `cash_binary_barrier_option`

```python
cash_binary_barrier_option(*, option_type, strike, effective_date, expiry_date, barrier_level, barrier_type, payout, **settings)
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
cash_double_no_touch(*, effective_date, expiry_date, lower_barrier, upper_barrier, payout, **settings)
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
cash_double_touch(*, effective_date, expiry_date, lower_barrier, upper_barrier, payout, **settings)
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

## `cash_no_touch_down`

```python
cash_no_touch_down(*, effective_date, expiry_date, barrier_level, payout, **settings)
```

Create a cash payment requiring no downward barrier touch.

#### Parameters

- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`barrier_level`** (`float`) — Positive finite trigger level; equality counts as a touch.
- **`payout`** (`float`) — Positive finite cash payment.
- **`observation_mode`** (`{'continuous', 'scheduled'}, optional`) — Continuous monitoring or observations on the supplied dates.
- **`observation_dates`** (`iterable of date, optional`) — Strictly increasing observation dates within the contract life.
- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — Strictly prior history. None means unknown; untouched means known no hit.
#### Returns

- `TouchOption` — Validated owned contract.
#### Raises

- `InvalidInputError` — If contractual amounts, life dates or observation terms are invalid.
#### Notes

Barrier equality counts as a touch. Strictly prior history and trading
calendar compatibility are checked during pricing. Prior at-hit
payments have no remaining value. No-touch payments occur only at
expiry.

## `cash_no_touch_up`

```python
cash_no_touch_up(*, effective_date, expiry_date, barrier_level, payout, **settings)
```

Create a cash payment requiring no upward barrier touch.

#### Parameters

- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`barrier_level`** (`float`) — Positive finite trigger level; equality counts as a touch.
- **`payout`** (`float`) — Positive finite cash payment.
- **`observation_mode`** (`{'continuous', 'scheduled'}, optional`) — Continuous monitoring or observations on the supplied dates.
- **`observation_dates`** (`iterable of date, optional`) — Strictly increasing observation dates within the contract life.
- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — Strictly prior history. None means unknown; untouched means known no hit.
#### Returns

- `TouchOption` — Validated owned contract.
#### Raises

- `InvalidInputError` — If contractual amounts, life dates or observation terms are invalid.
#### Notes

Barrier equality counts as a touch. Strictly prior history and trading
calendar compatibility are checked during pricing. Prior at-hit
payments have no remaining value. No-touch payments occur only at
expiry.

## `cash_one_touch_down`

```python
cash_one_touch_down(*, effective_date, expiry_date, barrier_level, payout, **settings)
```

Create a cash payment activated by downward barrier touch.

#### Parameters

- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`barrier_level`** (`float`) — Positive finite trigger level; equality counts as a touch.
- **`payout`** (`float`) — Positive finite cash payment.
- **`settlement_timing`** (`{'at_hit', 'at_expiry'}, optional`) — At-hit or expiry payment; no-touch contracts settle only at expiry.
- **`observation_mode`** (`{'continuous', 'scheduled'}, optional`) — Continuous monitoring or observations on the supplied dates.
- **`observation_dates`** (`iterable of date, optional`) — Strictly increasing observation dates within the contract life.
- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — Strictly prior history. None means unknown; untouched means known no hit.
#### Returns

- `TouchOption` — Validated owned contract.
#### Raises

- `InvalidInputError` — If contractual amounts, life dates or observation terms are invalid.
#### Notes

Barrier equality counts as a touch. Strictly prior history and trading
calendar compatibility are checked during pricing. Prior at-hit
payments have no remaining value. No-touch payments occur only at
expiry.

## `cash_one_touch_up`

```python
cash_one_touch_up(*, effective_date, expiry_date, barrier_level, payout, **settings)
```

Create a cash payment activated by upward barrier touch.

#### Parameters

- **`effective_date`** (`datetime.date`) — Inclusive first contract date.
- **`expiry_date`** (`datetime.date`) — Final contract date; expiry is at midnight UTC.
- **`barrier_level`** (`float`) — Positive finite trigger level; equality counts as a touch.
- **`payout`** (`float`) — Positive finite cash payment.
- **`settlement_timing`** (`{'at_hit', 'at_expiry'}, optional`) — At-hit or expiry payment; no-touch contracts settle only at expiry.
- **`observation_mode`** (`{'continuous', 'scheduled'}, optional`) — Continuous monitoring or observations on the supplied dates.
- **`observation_dates`** (`iterable of date, optional`) — Strictly increasing observation dates within the contract life.
- **`touch_state`** (`{'untouched', 'touched'} or None, optional`) — Strictly prior history. None means unknown; untouched means known no hit.
#### Returns

- `TouchOption` — Validated owned contract.
#### Raises

- `InvalidInputError` — If contractual amounts, life dates or observation terms are invalid.
#### Notes

Barrier equality counts as a touch. Strictly prior history and trading
calendar compatibility are checked during pricing. Prior at-hit
payments have no remaining value. No-touch payments occur only at
expiry.

## `dual_coupon_snowball`

```python
dual_coupon_snowball(*, knock_out_coupon_rate, initial_spot, knock_in_level, knock_out_level, maturity_coupon_rate, observation_dates, effective_date, expiry_date, barrier_state=None, **fields)
```

Create a snowball with separate knock-out and maturity coupons.

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

Daily knock-in monitoring, unit principal, zero lower strike and initial
spot as upper strike are used unless the preset overrides them. History
and trading-calendar consistency are checked during pricing.

## `european_snowball`

```python
european_snowball(*, coupon_rate, initial_spot, knock_in_level, knock_out_level, observation_dates, effective_date, expiry_date, barrier_state=None, **fields)
```

Create a snowball with knock-in observed only at expiry.

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

Daily knock-in monitoring, unit principal, zero lower strike and initial
spot as upper strike are used unless the preset overrides them. History
and trading-calendar consistency are checked during pricing. Knock-in is
observed only at expiry.

## `loss_capped_snowball`

```python
loss_capped_snowball(*, coupon_rate, initial_spot, knock_in_level, knock_out_level, lower_strike, observation_dates, effective_date, expiry_date, barrier_state=None, **fields)
```

Create a snowball whose lower terminal strike caps downside loss.

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

Daily knock-in monitoring, unit principal, zero lower strike and initial
spot as upper strike are used unless the preset overrides them. History
and trading-calendar consistency are checked during pricing.

## `otm_snowball`

```python
otm_snowball(*, coupon_rate, initial_spot, knock_in_level, knock_out_level, upper_strike, observation_dates, effective_date, expiry_date, barrier_state=None, **fields)
```

Create a snowball with a replaced upper terminal strike.

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

Daily knock-in monitoring, unit principal, zero lower strike and initial
spot as upper strike are used unless the preset overrides them. History
and trading-calendar consistency are checked during pricing.

## `parachute_snowball`

```python
parachute_snowball(*, coupon_rate, initial_spot, knock_in_level, knock_out_level, final_knock_out_level, observation_dates, effective_date, expiry_date, barrier_state=None, **fields)
```

Create a snowball with a distinct final knock-out level.

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

Daily knock-in monitoring, unit principal, zero lower strike and initial
spot as upper strike are used unless the preset overrides them. History
and trading-calendar consistency are checked during pricing.

## `standard_snowball`

```python
standard_snowball(*, coupon_rate, initial_spot, knock_in_level, knock_out_level, observation_dates, effective_date, expiry_date, barrier_state=None, **fields)
```

Create constant knock-out coupons and levels with daily knock-in
monitoring.

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

Daily knock-in monitoring, unit principal, zero lower strike and initial
spot as upper strike are used unless the preset overrides them. History
and trading-calendar consistency are checked during pricing.

## `step_down_snowball`

```python
step_down_snowball(*, coupon_rate, initial_spot, knock_in_level, initial_knock_out_level, knock_out_level_decrement, observation_dates, effective_date, expiry_date, barrier_state=None, **fields)
```

Create a snowball with decreasing knock-out levels.

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

Daily knock-in monitoring, unit principal, zero lower strike and initial
spot as upper strike are used unless the preset overrides them. History
and trading-calendar consistency are checked during pricing.
Decrements apply after each observation; the first uses the initial
value. Signed coupons and decrements are accepted if all expanded terms
remain valid.
