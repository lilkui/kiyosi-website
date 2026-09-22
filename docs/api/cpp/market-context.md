---
description: C++ API declarations from kiyosi/market/context.hpp.
outline: [2, 4]
---

# `<kiyosi/market/context.hpp>`

```cpp
#include <kiyosi/market/context.hpp>
```

## `make_pricing_context`

```cpp
Result< PricingContext > kiyosi::make_pricing_context(BlackScholesMertonParameters model_parameters, double spot_price, Timestamp valuation_time, TradingCalendar calendar)
```

Creates a pricing context at an intraday valuation time with an explicit calendar. 
**Returns:** The context, or an `invalid_spot_price` or `invalid_date` error.

## `make_pricing_context`

```cpp
Result< PricingContext > kiyosi::make_pricing_context(BlackScholesMertonParameters model_parameters, double spot_price, Timestamp valuation_time)
```

Creates a pricing context at an intraday valuation time using `weekdays_calendar()`. 
**Returns:** The context, or an `invalid_spot_price` or `invalid_date` error.

## `make_pricing_context`

```cpp
Result< PricingContext > kiyosi::make_pricing_context(BlackScholesMertonParameters model_parameters, double spot_price, Date valuation_date, TradingCalendar calendar)
```

Creates a midnight pricing context for a date with an explicit calendar. 
**Returns:** The context, or an `invalid_spot_price` or `invalid_date` error.

## `make_pricing_context`

```cpp
Result< PricingContext > kiyosi::make_pricing_context(BlackScholesMertonParameters model_parameters, double spot_price, Date valuation_date)
```

Creates a midnight pricing context for a date using `weekdays_calendar()`. 
**Returns:** The context, or an `invalid_spot_price` or `invalid_date` error.

## `kiyosi::PricingContext`

```cpp
class kiyosi::PricingContext
```

Valuation-time snapshot: model parameters, the observable spot, and the trading calendar.

### Members

#### `model_parameters`

```cpp
const BlackScholesMertonParameters & kiyosi::PricingContext::model_parameters() const noexcept
```

Returns the Black-Scholes-Merton model parameters.

#### `spot_price`

```cpp
double kiyosi::PricingContext::spot_price() const noexcept
```

Returns the positive observable spot price.

#### `valuation_date`

```cpp
Date kiyosi::PricingContext::valuation_date() const noexcept
```

Returns the civil date containing the valuation time.

#### `valuation_time`

```cpp
Timestamp kiyosi::PricingContext::valuation_time() const noexcept
```

Returns the valuation timestamp.

#### `calendar`

```cpp
const TradingCalendar & kiyosi::PricingContext::calendar() const noexcept
```

Returns the trading calendar.
