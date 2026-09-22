---
description: What kiyosi does, how its pricing API fits together, and the current model scope.
---

# Introduction

Kiyosi is an open-source derivatives-pricing library. Its native C++23 implementation is exposed through a Python-first API for vanilla options, exotic instruments, and structured products.

::: warning Alpha software
The API may change without backward-compatibility guarantees. Check the upstream project when upgrading.
:::

## How pricing fits together

A pricing calculation brings together three objects:

1. An **instrument** describes the contract, including its strike, dates, and payoff type.
2. A **market context** supplies model parameters, the spot price, and the valuation time.
3. An **engine** applies a pricing method to the instrument and context.

The engine returns a result containing the price. Kiyosi also provides Greeks through its result types. Available methods depend on the instrument; see [pricing engines](./engines).

## Model scope

The current models use Black-Scholes-Merton inputs with flat risk-free rate, dividend yield, and volatility. Volatility surfaces and rate curves are outside the current API.

The library includes trading calendars and observation schedule builders, including SSE holidays. Supported instruments range from European and American options to accumulators, phoenix products, and snowball variants.

## Validation

Upstream pricing tests compare against reference values generated independently using QuantLib. QuantLib supports reference generation and calendar maintenance; it is not a build or runtime dependency of the C++ core.

## Where to begin

- [Install the Python package](./installation) for the shortest route to a calculation.
- [Price your first option](./first-price) for a complete example.
- [Build the C++ library](../cpp/building) to use the native API.

Source: [kiyosi README](https://github.com/lilkui/kiyosi#readme). Kiyosi is released under the [MIT License](https://github.com/lilkui/kiyosi/blob/main/LICENSE.txt).
