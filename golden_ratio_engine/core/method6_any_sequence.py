"""
Method 6: Any Additive Sequence (أي متتالية جمعية)
====================================================
Start with any two positive numbers a, b (not both zero).
Apply the same recurrence: s(n) = s(n-1) + s(n-2).
The ratio s(n+1)/s(n) always converges to φ regardless of starting values.

This is the *universal* property of the golden ratio — it is the attractor
of any additive recurrence.

Convergence: Linear — same rate as Fibonacci/Lucas.
"""

from mpmath import mp, mpf, phi as _phi_exact, fabs, log10


def golden_ratio_any_sequence(
    a: float = 7.0,
    b: float = 3.0,
    n_terms: int = 5000,
    decimal_places: int = 1000,
) -> "mpf":
    """
    Compute φ from an arbitrary additive sequence starting with (a, b).

    Parameters
    ----------
    a : float
        First term of the sequence (must be positive).
    b : float
        Second term of the sequence (must be positive).
    n_terms : int
        Number of steps to iterate.
    decimal_places : int
        Output precision.

    Returns
    -------
    mpf
        Ratio of the last two terms, converging to φ.

    Raises
    ------
    ValueError
        If both a and b are zero, or either is negative.
    """
    if a <= 0 or b <= 0:
        raise ValueError("Both starting values must be positive.")
    mp.dps = decimal_places + 10
    # Use mpf for exact tracking (values grow quickly so stay as mpf)
    x, y = mpf(a), mpf(b)
    for _ in range(n_terms):
        x, y = y, x + y
    phi = y / x
    mp.dps = decimal_places
    return +phi


def convergence_data_any_sequence(
    a: float = 7.0,
    b: float = 3.0,
    max_terms: int = 200,
    decimal_places: int = 100,
) -> list:
    """
    Return convergence data for each step.

    Parameters
    ----------
    a, b : float
        Starting values.
    max_terms : int
        Maximum number of iterations.
    decimal_places : int
        Working precision.

    Returns
    -------
    list of (iteration, value, error, correct_digits)
    """
    if a <= 0 or b <= 0:
        raise ValueError("Both starting values must be positive.")
    mp.dps = decimal_places + 10
    exact = +_phi_exact
    results = []
    x, y = mpf(a), mpf(b)
    for i in range(1, max_terms + 1):
        x, y = y, x + y
        value = y / x
        error = fabs(value - exact)
        correct_digits = int(-log10(error)) if error > 0 else decimal_places
        results.append((i, +value, error, correct_digits))
    return results
