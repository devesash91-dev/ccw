"""
Method 2: Continued Fraction (الكسر المستمر)
=============================================
φ = 1 + 1/(1 + 1/(1 + 1/(1 + ...)))

φ has the *simplest* possible continued fraction: [1; 1, 1, 1, ...]
This also makes it the *slowest* converging continued fraction
(hardest number to approximate by rationals — most irrational number).

Convergence: Linear — each iteration adds ~0.209 correct decimal digits.
"""

from mpmath import mp, mpf, phi as _phi_exact, fabs, log10


def golden_ratio_cf(iterations: int = 10000, decimal_places: int = 50) -> "mpf":
    """
    Compute φ via the infinite continued fraction [1; 1, 1, 1, ...].

    Parameters
    ----------
    iterations : int
        Number of back-substitution steps.
    decimal_places : int
        Working precision.

    Returns
    -------
    mpf
        Approximation of φ.
    """
    mp.dps = decimal_places + 10
    phi = mpf(1)
    for _ in range(iterations):
        phi = mpf(1) + mpf(1) / phi
    mp.dps = decimal_places
    return +phi


def convergence_data_cf(
    max_iterations: int = 200, decimal_places: int = 100
) -> list:
    """
    Return convergence data for each iteration.

    Parameters
    ----------
    max_iterations : int
        Maximum number of iterations to evaluate.
    decimal_places : int
        Working precision.

    Returns
    -------
    list of (iteration, value, error, correct_digits)
    """
    mp.dps = decimal_places + 10
    exact = +_phi_exact
    results = []
    phi = mpf(1)
    for i in range(1, max_iterations + 1):
        phi = mpf(1) + mpf(1) / phi
        error = fabs(phi - exact)
        correct_digits = int(-log10(error)) if error > 0 else decimal_places
        results.append((i, +phi, error, correct_digits))
    return results
