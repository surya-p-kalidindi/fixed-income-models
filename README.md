# fixed-income-models

Bond analytics implemented from scratch in Python — no financial libraries
perform the mathematics.

## Implemented

**Yield-based analytics**
- Bond price (arbitrary payment frequency)
- Yield to maturity (bisection solver)
- Macaulay duration, modified duration
- DV01 — analytic and bump-and-reprice
- Convexity — analytic and second-difference bump

**Curve-based analytics**
- Pricing off a spot-rate curve (one rate per payment period)
- Effective duration and effective convexity from parallel curve shocks

## Validation

Analytic and numerical methods are computed independently and cross-checked.
For a 3-year 5% semiannual bond at par:

| Metric | Analytic | Numerical |
|---|---|---|
| Modified duration | 2.7541 | 2.7543 |
| DV01 | 0.27541 | 0.27536 |
| Convexity | 9.2107 | 9.2103 |

Yield-based and curve-based duration agree closely for a bullet bond because
its cash flows are invariant to rate moves. That equivalence breaks for
instruments with embedded optionality — which is why effective duration is
the relevant measure for mortgage-backed securities.

## Roadmap

- Mortgage pool cash flows: CPR/SMM, CDR/MDR, defaults, recoveries, losses
- Spot-curve bootstrapping from par yields
- Z-spread solver
- Option-adjusted spread (Monte Carlo rate paths with rate-dependent prepayment)