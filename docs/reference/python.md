---
description: Navigate kiyosi's instruments, market, and pricing Python modules.
---

# Python API overview

For signatures, members, exceptions, and docstrings for every public export, use the [complete Python API reference](../api/python/).

Kiyosi groups its public Python API into three modules. This page is a navigation guide; consult the linked source modules for the current export list.

## `kiyosi.instruments`

Contract definitions and structured-product presets live here. The [first pricing example](../guide/first-price) uses `EuropeanOption` and `OptionType` to define a call option.

Supported families include vanilla, digital, Asian, barrier, accumulator, phoenix, and snowball instruments. See [engine coverage](../guide/engines#instrument-coverage) before selecting a pricing method.

[Browse the instruments module →](https://github.com/lilkui/kiyosi/blob/main/python/kiyosi/instruments.py)

## `kiyosi.market`

Market inputs, valuation contexts, calendars, and observation schedules live here.

`BlackScholesMertonParameters` holds the flat risk-free rate, dividend yield, and volatility. `PricingContext` combines those model parameters with `spot_price` and `valuation_time`.

[Browse the market module →](https://github.com/lilkui/kiyosi/blob/main/python/kiyosi/market.py)

## `kiyosi.pricing`

This module exposes pricing engines, numerical analytics, scenarios, and implied-value solvers.

Use `AnalyticVanillaEngine` for the European call example. `MonteCarloVanillaEngine` provides a simulation-based alternative, with `MonteCarloBackend` selecting the backend. Both use `price(option, context)`, returning an object with a `price` member.

[Browse the pricing module →](https://github.com/lilkui/kiyosi/blob/main/python/kiyosi/pricing.py)

## Working examples

- [Your first price](../guide/first-price) contains a complete Python script.
- [Select a backend](../guide/engines#select-a-backend) demonstrates CUDA configuration.
- [Source examples](https://github.com/lilkui/kiyosi/tree/main/examples) cover additional instrument and engine families.

::: info API stability
The API is in alpha. Regenerate the complete reference whenever the kiyosi package changes.
:::
