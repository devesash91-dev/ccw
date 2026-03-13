"""
Ultra-Precision φ Engine (محرك الدقة الفائقة)
===============================================
Uses mpmath's built-in phi constant (which internally uses the AGM algorithm
for computing √5, giving quadratic convergence — the number of correct digits
doubles with each iteration).

Supports from 10 to 1,000,000 decimal places.
"""

from mpmath import mp, mpf, sqrt, phi as _mpmath_phi


def ultra_precision_phi(decimal_places: int = 10000) -> "mpf":
    """
    Compute φ at arbitrary precision using mpmath's built-in phi.

    Also validates by comparing with the manual formula (1+√5)/2.

    Parameters
    ----------
    decimal_places : int
        Number of decimal places (10 to 1,000,000).

    Returns
    -------
    mpf
        φ at the requested precision.

    Raises
    ------
    AssertionError
        If mpmath.phi and the manual formula disagree.
    """
    if decimal_places < 1:
        raise ValueError("decimal_places must be at least 1.")

    mp.dps = decimal_places + 20

    # Method 1: mpmath built-in (uses AGM internally for sqrt)
    phi_builtin = +_mpmath_phi

    # Method 2: manual formula
    phi_manual = (mpf(1) + sqrt(mpf(5))) / mpf(2)

    # Verify they agree to the requested precision
    diff = abs(phi_builtin - phi_manual)
    # Allow rounding in the last few guard digits
    threshold = mpf(10) ** (-(decimal_places + 10))
    assert diff < threshold, (
        f"MISMATCH between mpmath.phi and manual formula! diff={diff}"
    )

    mp.dps = decimal_places
    return +phi_builtin


def phi_to_n_digits(n: int) -> str:
    """
    Return φ as a string with exactly n significant decimal digits.

    Parameters
    ----------
    n : int
        Number of decimal digits to display (after the decimal point).

    Returns
    -------
    str
        String representation, e.g. '1.6180339887...' with n decimal places.
    """
    mp.dps = n + 10
    value = +_mpmath_phi
    # Build fixed-point string
    mp.dps = n + 5
    s = mp.nstr(value, n + 1, strip_zeros=False)
    return s


def phi_digits_list(n: int) -> list:
    """
    Return the first n decimal digits of φ as a list of integers.

    Parameters
    ----------
    n : int
        Number of decimal digits (not counting the leading 1).

    Returns
    -------
    list of int
        Decimal digits of φ after the decimal point.
    """
    s = phi_to_n_digits(n)
    # Remove "1." prefix
    if "." in s:
        decimal_part = s.split(".")[1]
    else:
        decimal_part = ""
    return [int(d) for d in decimal_part[:n]]
