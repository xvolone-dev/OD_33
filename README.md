# OD-33 — Asymptotic Prime Density Estimator

OD-33 is a lightweight asymptotic model designed to estimate **local prime density**
and to **guide integer factorization strategies**.

⚠️ **OD-33 does NOT perform factorization by itself.**  
It provides a *density signal* used to decide **how** to factor, not **to factor**.

---

## Core idea

Given a large integer `N`, OD-33 computes a normalized density coefficient **K(N)**,
derived from asymptotic corrections to the logarithmic integral.

This coefficient is used as a **decision signal**, not as a bound.

---

## What OD-33 is used for

OD-33 helps to:

- allocate time budgets,
- select the most appropriate method (Trial, Blitz, Pollard, ECM),
- prioritize deterministic vs probabilistic scans,
- guide hybrid factorization pipelines.

OD-33 is designed to be **fast**, **stable**, and **algorithm-agnostic**.

---

## Typical usage

```python
from OD_33 import od33_density

K = od33_density(N)

The returned value **K** is a relative density indicator:

- **K > 1** → locally dense (trial / deterministic scans favored)
- **K ≈ 1** → neutral
- **K < 1** → sparse (probabilistic / ECM favored)

---

## Design principles

- asymptotic, not heuristic
- no factor leakage
- no dependency on specific factorization engines
- compatible with hybrid pipelines

---

## Status

This repository contains the **OD-33 density model only**.

Hybrid factorization suites, benchmarks, and experimental engines  
(Blitz, HybridBC, ECM-OD, etc.) are intentionally **not included** here.

They will be documented separately.

---

## Disclaimer

OD-33 is a research tool.  
No cryptographic guarantees are provided.  
Use responsibly.
