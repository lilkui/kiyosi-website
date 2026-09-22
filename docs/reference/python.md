---
description: Navigate kiyosi's instruments, market, and pricing Python modules.
---

# Python API overview

Kiyosi groups its public Python API into three modules. This page is a navigation guide; consult the linked upstream modules for the current export list.

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
- [Upstream examples](https://github.com/lilkui/kiyosi/tree/main/examples) cover additional instrument and engine families.

::: info API stability
This scaffold does not generate an exhaustive class reference. The upstream repository is the source of truth for signatures while the API is in alpha.
:::
