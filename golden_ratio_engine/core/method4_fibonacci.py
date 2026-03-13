"""
Method 4: Fibonacci Sequence (متتالية فيبوناتشي)
=================================================
φ = lim_{n→∞} F(n+1) / F(n)

Fibonacci numbers grow as φⁿ/√5, so consecutive ratios converge to φ.

Key implementation detail: Python's built-in integers have arbitrary precision,
so we compute F(n) exactly as integers, then divide using mpmath for the
final high-precision result.

Convergence: Linear — approximately 0.209 digits per step (same as CF).
"""

from mpmath import mp, mpf, phi as _phi_exact, fabs, log10


def golden_ratio_fibonacci(
    n_terms: int = 5000, decimal_places: int = 1000
) -> "mpf":
    """
    Compute φ as the ratio of consecutive Fibonacci numbers.

    Uses Python arbitrary-precision integers for exact Fibonacci computation,
    then converts to mpf for the final division.

    Parameters
    ----------
    n_terms : int
        Number of Fibonacci terms to compute.
    decimal_places : int
        Output precision.

    Returns
    -------
    mpf
        F(n_terms) / F(n_terms - 1), an approximation of φ.
    """
    mp.dps = decimal_places + 10
    a, b = 0, 1
    for _ in range(n_terms):
        a, b = b, a + b
    # a = F(n_terms), b = F(n_terms+1) after the loop
    phi = mpf(b) / mpf(a)
    mp.dps = decimal_places
    return +phi


def convergence_data_fibonacci(
    max_terms: int = 200, decimal_places: int = 100
) -> list:
    """
    Return convergence data for each Fibonacci step.

    Parameters
    ----------
    max_terms : int
        Maximum number of Fibonacci terms.
    decimal_places : int
        Working precision.

    Returns
    -------
    list of (iteration, value, error, correct_digits)
    """
    mp.dps = decimal_places + 10
    exact = +_phi_exact
    results = []
    a, b = 0, 1
    for i in range(1, max_terms + 1):
        a, b = b, a + b
        if a == 0:
            continue
        value = mpf(b) / mpf(a)
        error = fabs(value - exact)
        correct_digits = int(-log10(error)) if error > 0 else decimal_places
        results.append((i, +value, error, correct_digits))
    return results
