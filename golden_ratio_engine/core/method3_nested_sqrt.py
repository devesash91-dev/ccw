"""
Method 3: Nested Square Roots (الجذور المتداخلة)
=================================================
φ = √(1 + √(1 + √(1 + ...)))

Starting from any positive value x₀ and iterating x ← √(1+x),
the sequence converges to φ (the positive fixed point of x² = 1+x).

Convergence: Linear — similar speed to the continued fraction.
"""

from mpmath import mp, mpf, sqrt, phi as _phi_exact, fabs, log10


def golden_ratio_nested_sqrt(
    iterations: int = 10000, decimal_places: int = 50
) -> "mpf":
    """
    Compute φ via nested (iterated) square roots.

    φ = √(1 + √(1 + √(1 + ...)))

    Parameters
    ----------
    iterations : int
        Number of iterations.
    decimal_places : int
        Working precision.

    Returns
    -------
    mpf
        Approximation of φ.
    """
    mp.dps = decimal_places + 10
    result = mpf(1)
    for _ in range(iterations):
        result = sqrt(mpf(1) + result)
    mp.dps = decimal_places
    return +result


def convergence_data_nested_sqrt(
    max_iterations: int = 200, decimal_places: int = 100
) -> list:
    """
    Return convergence data for each iteration.

    Parameters
    ----------
    max_iterations : int
        Maximum number of iterations.
    decimal_places : int
        Working precision.

    Returns
    -------
    list of (iteration, value, error, correct_digits)
    """
    mp.dps = decimal_places + 10
    exact = +_phi_exact
    results = []
    result = mpf(1)
    for i in range(1, max_iterations + 1):
        result = sqrt(mpf(1) + result)
        error = fabs(result - exact)
        correct_digits = int(-log10(error)) if error > 0 else decimal_places
        results.append((i, +result, error, correct_digits))
    return results
