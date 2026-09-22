---
description: Compare kiyosi's pricing methods by instrument and select the CPU or CUDA Monte Carlo backend.
---

# Pricing engines

Choose an engine supported by your instrument. A common `price(instrument, context)` interface does not mean every engine accepts every product.

## Instrument coverage

| Instrument family | Available methods |
| --- | --- |
| European vanilla | Analytic, CRR binomial, finite difference, integral, Monte Carlo |
| American vanilla | Bjerksund-Stensland, CRR binomial, finite difference, Monte Carlo |
| Cash-or-nothing and asset-or-nothing digital | Analytic, finite difference, integral |
| Barrier | Analytic, finite difference |
| Binary barrier and touch | Analytic |
| Geometric-average Asian | Closed form |
| Arithmetic-average Asian | Turnbull-Wakeman approximation |
| Accumulator | Finite difference, Monte Carlo |
| Phoenix and snowball variants | Finite difference, Monte Carlo |

This coverage follows the [kiyosi pricing matrix](https://github.com/lilkui/kiyosi#pricing-coverage). Check the source repository for changes as the alpha API evolves.

## Select a backend

Monte Carlo engines use the CPU by default. For CUDA, reuse the `option` and `context` from [Your first price](./first-price):

```python
from kiyosi.pricing import MonteCarloBackend, MonteCarloVanillaEngine

engine = MonteCarloVanillaEngine(backend=MonteCarloBackend.CUDA)
result = engine.price(option, context)
print(result.price)
```

CUDA requires a compatible NVIDIA GPU and driver. It is a Monte Carlo backend; selecting it does not move analytic or finite-difference engines onto the GPU.

## Compare methods carefully

Keep the contract and market inputs identical when comparing engines. Analytic methods evaluate a formula; numerical methods introduce approximation or simulation error. Review engine-specific settings in the [pricing module](https://github.com/lilkui/kiyosi/blob/main/python/kiyosi/pricing.py) and [source examples](https://github.com/lilkui/kiyosi/tree/main/examples).

All current models share the [Black-Scholes-Merton model scope](./introduction#model-scope).
