---
description: kiyosi/instruments/autocallable/note.hpp 中的 C++ API 声明。
outline: [2, 4]
---

# `<kiyosi/instruments/autocallable/note.hpp>`

```cpp
#include <kiyosi/instruments/autocallable/note.hpp>
```

## `KnockInObservationMode`

```cpp
enum class KnockInObservationMode
```

Monitoring frequency for an autocallable knock-in barrier.

**枚举值**

- `every_trading_day` — Observe on every trading day in the contract life.
- `at_expiry` — Observe only at expiry.

## `AutocallableBarrierState`

```cpp
enum class AutocallableBarrierState
```

Barrier events known before valuation.

**枚举值**

- `none` — No barrier event has occurred.
- `knocked_out` — The note has already knocked out.
- `knocked_in` — The downside barrier has already been breached.

## `make_autocallable_observations`

```cpp
Result<std::vector<AutocallableObservation>> kiyosi::make_autocallable_observations(const std::vector<Date> &dates, const std::vector<double> &levels, std::optional<std::vector<double>> coupons=std::nullopt, std::optional<std::vector<double>> coupon_barriers=std::nullopt)
```

Associates parallel inputs before note construction. Omitted coupon sequences use record defaults. Validates sequence lengths; contractual values and dates are validated by the note factory.

## `validate_autocallable_note`

```cpp
template <AutocallableProduct Note>
Result<void> kiyosi::validate_autocallable_note(const Note &note)
```

Revalidates all terms of a complete product, including a moved-from observation schedule.

## `validate_autocallable_history`

```cpp
template <typename Note>
Result<void> kiyosi::validate_autocallable_history(const Note &note, const PricingContext &context)
```

Validates the caller's history snapshot against events before valuation.

## `kiyosi::AutocallableNote`

```cpp
template <AutocallableTerms Terms>
class kiyosi::AutocallableNote
```

Complete immutable autocallable product, owning its validated construction terms. Valuation excludes cashflows settled before the valuation time. Principal, coupons and downside components use normalized payoff units and are added independently. Observation views borrow this note. Destruction, moving from, or assignment invalidates them. Convenience getters return owning copies independent of this note. Concurrent const access follows the library default; assignment must not overlap access.

### 成员

#### `replace`

```cpp
Result<AutocallableNote> kiyosi::AutocallableNote<Terms>::replace(std::optional<AutocallableBarrierState> barrier_state) const
```

Returns a validated owning copy with only the supplied history replaced. Preserves all contract terms and never changes this object, including on failure. History is caller-supplied; time consistency is checked during pricing. Concurrent calls and reads are safe without concurrent assignment or mutation. nullopt means unknown history; none means known absence of barrier events. Uses the same validation and error categories as the product factory.

#### `AutocallableNote`

```cpp
kiyosi::AutocallableNote<Terms>::AutocallableNote(const AutocallableNote &)=default
```

#### `AutocallableNote`

```cpp
kiyosi::AutocallableNote<Terms>::AutocallableNote(AutocallableNote &&) noexcept=default
```

#### `~AutocallableNote`

```cpp
kiyosi::AutocallableNote<Terms>::~AutocallableNote()=default
```

#### `operator=`

```cpp
AutocallableNote & kiyosi::AutocallableNote<Terms>::operator=(AutocallableNote &&) noexcept=default
```

#### `operator=`

```cpp
AutocallableNote & kiyosi::AutocallableNote<Terms>::operator=(const AutocallableNote &other)
```

Copies terms without changing this note if allocation fails.

#### `knock_out_levels`

```cpp
std::vector<double> kiyosi::AutocallableNote<Terms>::knock_out_levels() const
```

Returns an owning copy of the positive knock-out levels.

#### `observation_dates`

```cpp
std::vector<Date> kiyosi::AutocallableNote<Terms>::observation_dates() const
```

Returns an owning copy of the strictly ordered observation dates.

#### `observations_view`

```cpp
std::span<const AutocallableObservation> kiyosi::AutocallableNote<Terms>::observations_view() const noexcept
```

Borrows complete immutable observations with the lifetime documented above.

#### `principal_ratio`

```cpp
double kiyosi::AutocallableNote<Terms>::principal_ratio() const noexcept
```

Returns the non-negative normalized principal component.

#### `effective_date`

```cpp
Date kiyosi::AutocallableNote<Terms>::effective_date() const noexcept
```

Returns the first date of the note life.

#### `expiry_date`

```cpp
Date kiyosi::AutocallableNote<Terms>::expiry_date() const noexcept
```

Returns the final date of the note life.

#### `barrier_state`

```cpp
std::optional<AutocallableBarrierState> kiyosi::AutocallableNote<Terms>::barrier_state() const noexcept
```

Returns the prior barrier state, or nullopt for unknown history.

#### `initial_spot`

```cpp
double kiyosi::AutocallableNote<Terms>::initial_spot() const noexcept
```

Returns the positive reference spot.

#### `upper_strike`

```cpp
double kiyosi::AutocallableNote<Terms>::upper_strike() const noexcept
```

Returns the positive upper settlement strike.

#### `lower_strike`

```cpp
double kiyosi::AutocallableNote<Terms>::lower_strike() const noexcept
```

Returns the non-negative lower settlement strike.

#### `knock_in_level`

```cpp
double kiyosi::AutocallableNote<Terms>::knock_in_level() const noexcept
```

Returns the positive downside knock-in level.

#### `knock_in_observation_mode`

```cpp
KnockInObservationMode kiyosi::AutocallableNote<Terms>::knock_in_observation_mode() const noexcept
```

Returns the knock-in monitoring frequency.

#### `coupon_rate`

```cpp
double kiyosi::AutocallableNote<Terms>::coupon_rate() const noexcept
```

Returns the annualized conditional observation coupon.

#### `maturity_coupon_rate`

```cpp
double kiyosi::AutocallableNote<Terms>::maturity_coupon_rate() const noexcept
```

Returns the finite maturity coupon rate.

#### `minimum_coupon_rate`

```cpp
double kiyosi::AutocallableNote<Terms>::minimum_coupon_rate() const noexcept
```

Returns the finite maturity-coupon floor after knock-in.

#### `knock_out_coupon_rates`

```cpp
std::vector<double> kiyosi::AutocallableNote<Terms>::knock_out_coupon_rates() const
```

Returns an owning copy of the finite knock-out coupon rates.

#### `coupon_barrier_levels`

```cpp
std::vector<double> kiyosi::AutocallableNote<Terms>::coupon_barrier_levels() const
```

Returns an owning copy of the non-negative coupon barriers.

## `kiyosi::AutocallableObservation`

```cpp
struct kiyosi::AutocallableObservation
```

One contractual observation; its date, knock-out level, and coupon terms travel together.

### 成员

#### `date`

```cpp
Date kiyosi::AutocallableObservation::date
```

#### `knock_out_level`

```cpp
double kiyosi::AutocallableObservation::knock_out_level
```

#### `coupon_rate`

```cpp
double kiyosi::AutocallableObservation::coupon_rate
```

Snowball knock-out annual coupon; zero for Phoenix.

#### `coupon_barrier_level`

```cpp
double kiyosi::AutocallableObservation::coupon_barrier_level
```

Phoenix coupon threshold; zero for snowballs.
