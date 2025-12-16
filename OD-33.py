#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OD-33 — Decimal-first (Asymptotic Prime Density Estimator)

Modello:
    L(x) = ln(x) - B + C / (ln(x) - A)
    pi_hat(x) ≈ x / L(x)

Questo file esegue la STIMA della densità e il calcolo dei parametri.
NON esegue fattorizzazione. Serve a calcolare K e guidare le strategie.
"""

from __future__ import annotations
from decimal import Decimal, getcontext, ROUND_HALF_EVEN
from typing import List, Tuple
import argparse
import math

# =============================================================================
#  PARAMETRI CONGELATI — OD-33 v1b (Max-opt vincolata, DEFAULT)
# =============================================================================

A_33 = Decimal("4.576944500732421875")
B_33 = Decimal("1.07654")
C_33 = Decimal("0.26067")

# =============================================================================
#  TABELLA RIFERIMENTO pi(10^k)
# =============================================================================

PI10_REF: List[int] = [
    0,4,25,168,1229,9592,78498,664579,5761455,50847534,
    455052511,4118054813,37607912018,346065536839,
    3204941750802,29844570422669,279238341033925,
    2623557157654233,24739954287740860,
    234057667276344607,2220819602560918840,
    21127269486018731928,201467286689315906290,
    1925320391606803968923,18435599767349200867866,
    176846309399143769411680,1699246750872437141327603,
    16352460426841680446427399,157589269275973410412739598,
    1520698109714272166094258063
]

# =============================================================================
#  DECIMAL UTILS
# =============================================================================

def set_ctx(prec: int) -> None:
    getcontext().prec = max(60, int(prec))
    getcontext().rounding = ROUND_HALF_EVEN

def lnD(x: Decimal) -> Decimal:
    if hasattr(x, "ln"):
        return x.ln()
    import mpmath as mp
    mp.mp.dps = getcontext().prec + 30
    return Decimal(str(mp.log(mp.mpf(str(x)))))

# =============================================================================
#  CORE ESTIMATION LOGIC
# =============================================================================

def legendre_factor(x: Decimal, A: Decimal, B: Decimal, C: Decimal) -> Decimal:
    L = lnD(x)
    d = L - A
    if abs(d) < Decimal("1e-30"):
        d = Decimal("1e-30") if d >= 0 else Decimal("-1e-30")
    return L - B + (C / d)

def pi_hat(x: Decimal, A: Decimal, B: Decimal, C: Decimal) -> Decimal:
    if x < 2:
        return Decimal(0)
    L = lnD(x)
    Lx = legendre_factor(x, A, B, C)
    if Lx <= 0:
        return x / L
    return x / Lx

def metrics(A: Decimal, B: Decimal, C: Decimal, k_min: int = 3, k_max: int = 29) -> Tuple[Decimal, Decimal, int]:
    s = Decimal(0)
    max_abs = Decimal(0)
    k_of_max = k_min
    n = Decimal(0)

    for k in range(k_min, k_max + 1):
        x = Decimal(10) ** k
        true = Decimal(PI10_REF[k])
        est = pi_hat(x, A, B, C)
        rel_pct = (est - true) / true * Decimal(100)
        a = abs(rel_pct)
        s += a
        n += 1
        if a > max_abs:
            max_abs = a
            k_of_max = k

    return (s / n), max_abs, k_of_max

# =============================================================================
#  SELF TEST
# =============================================================================

def self_test(A: Decimal, B: Decimal, C: Decimal, k_min: int = 3, k_max: int = 29) -> None:
    print("\n=== OD-33 self-test (Estimation Only) ===")
    print(f"A={A}\nB={B}\nC={C}\n")
    print(" k   pi(10^k)        OD33_hat        rel_err %")
    print("-"*50)

    max_abs = Decimal(0)
    k_of_max = k_min
    s_abs = Decimal(0)
    n = Decimal(0)

    for k in range(k_min, k_max + 1):
        x = Decimal(10) ** k
        true = Decimal(PI10_REF[k])
        est = pi_hat(x, A, B, C)
        rel = (est - true) / true * Decimal(100)

        print(f"{k:2d} {int(true):>14d} {est:.6E} {rel:9.6f}")

        a = abs(rel)
        s_abs += a
        n += 1
        if a > max_abs:
            max_abs = a
            k_of_max = k

    mean_abs = s_abs / n
    print("\nMean abs rel err = ", mean_abs)
    print("Max  abs rel err = ", max_abs, " (k =", k_of_max, ")")

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prec", type=int, default=300, help="Decimal precision")
    ap.add_argument("--kmin", type=int, default=3)
    ap.add_argument("--kmax", type=int, default=29)
    args = ap.parse_args()
    
    set_ctx(args.prec)
    self_test(A_33, B_33, C_33, args.kmin, args.kmax)

if __name__ == "__main__":
    main()