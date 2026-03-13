"""
Method 1: Algebraic (الطريقة الجبرية)
=======================================
φ = (1 + √5) / 2

This is the most direct method — derived from solving x² = x + 1.
Uses mpmath for arbitrary-precision arithmetic.

Convergence: Instant (single computation), limited only by precision of √5.
"""

from mpmath import mp, mpf, sqrt


def golden_ratio_algebraic(decimal_places: int = 1000) -> "mpf":
    """
    Compute φ directly from the algebraic definition.

    φ = (1 + √5) / 2

    Parameters
    ----------
    decimal_places : int
        Number of decimal places of precision (default 1000).

    Returns
    -------
    mpf
        φ rounded to the requested precision.
    """
    mp.dps = decimal_places + 10  # extra guard digits
    phi = (mpf(1) + sqrt(mpf(5))) / mpf(2)
    mp.dps = decimal_places
    return +phi


def convergence_data_algebraic(decimal_places: int = 100) -> list:
    """
    Return convergence data for the algebraic method.

    Since this is a direct computation there is no iteration — a single
    entry is returned.

    Parameters
    ----------
    decimal_places : int
        Precision to use.

    Returns
    -------
    list of (iteration, value, error)
    """
    from mpmath import phi as _phi_exact, fabs, log10

    mp.dps = decimal_places + 10
    exact = +_phi_exact
    value = golden_ratio_algebraic(decimal_places)
    error = fabs(value - exact)
    correct_digits = int(-log10(error)) if error > 0 else decimal_places
    return [(1, value, error, correct_digits)]
