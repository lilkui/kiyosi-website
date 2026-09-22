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
KIYOSI_EXPORT TradingCalendar kiyosi::sse_calendar()
```

Shanghai Stock Exchange: weekdays excluding the published mainland holiday closures. 
**Returns:** The SSE trading calendar with a 252-day annualization basis.
