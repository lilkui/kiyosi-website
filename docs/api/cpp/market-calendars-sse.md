---
description: C++ API declarations from kiyosi/market/calendars/sse.hpp.
outline: [2, 4]
---

# `<kiyosi/market/calendars/sse.hpp>`

```cpp
#include <kiyosi/market/calendars/sse.hpp>
```

## `sse_calendar`

```cpp
TradingCalendar kiyosi::sse_calendar()
```

Shanghai Stock Exchange: weekdays excluding recorded XSHG and forecast holidays. The table spans 1991..2099; dates beyond the upstream list are estimates. Outside that span, queries fall back to a holiday-unaware weekday calendar.
**Returns:** The SSE trading calendar with a 243-day annualization basis.
