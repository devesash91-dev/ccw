"""
Method 5: Lucas Numbers (أرقام لوكاس)
=======================================
L(0) = 2, L(1) = 1, L(n) = L(n-1) + L(n-2)
φ = lim_{n→∞} L(n+1) / L(n)

Lucas numbers share the same recurrence as Fibonacci but with different
initial conditions. The ratio of consecutive Lucas numbers converges to φ
just as fast as Fibonacci ratios.

Convergence: Linear — same rate as Fibonacci (~0.209 digits per step).
"""

from mpmath import mp, mpf, phi as _phi_exact, fabs, log10


def golden_ratio_lucas(
    n_terms: int = 5000, decimal_places: int = 1000
) -> "mpf":
    """
    Compute φ as the ratio of consecutive Lucas numbers.

    Parameters
    ----------
    n_terms : int
        Number of Lucas terms to compute.
    decimal_places : int
        Output precision.

    Returns
    -------
    mpf
        L(n_terms) / L(n_terms - 1), an approximation of φ.
    """
    mp.dps = decimal_places + 10
    a, b = 2, 1  # L(0), L(1)
    for _ in range(n_terms):
        a, b = b, a + b
    phi = mpf(b) / mpf(a)
    mp.dps = decimal_places
    return +phi


def convergence_data_lucas(
    max_terms: int = 200, decimal_places: int = 100
) -> list:
    """
    Return convergence data for each Lucas step.

    Parameters
    ----------
    max_terms : int
        Maximum number of Lucas terms.
    decimal_places : int
        Working precision.

    Returns
    -------
    list of (iteration, value, error, correct_digits)
    """
    mp.dps = decimal_places + 10
    exact = +_phi_exact
    results = []
    a, b = 2, 1
    for i in range(1, max_terms + 1):
        a, b = b, a + b
        value = mpf(b) / mpf(a)
        error = fabs(value - exact)
        correct_digits = int(-log10(error)) if error > 0 else decimal_places
        results.append((i, +value, error, correct_digits))
    return results
