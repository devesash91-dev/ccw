"""
Method 7: Trigonometric (الطرق المثلثية)
==========================================
φ appears naturally in regular pentagons and 36-72-72 triangles:

    φ = 2 · cos(π/5)
    φ = 1 + 2 · sin(π/10)
    φ = 2 · sin(3π/10)

All three identities give exact φ in a single evaluation using mpmath trig.

Convergence: Instant (single computation).
"""

from mpmath import mp, mpf, cos, sin, pi, phi as _phi_exact, fabs, log10


def golden_ratio_trig(decimal_places: int = 1000) -> "mpf":
    """
    Compute φ using the trigonometric identity φ = 2·cos(π/5).

    Parameters
    ----------
    decimal_places : int
        Output precision.

    Returns
    -------
    mpf
        φ = 2·cos(π/5).
    """
    mp.dps = decimal_places + 10
    phi = 2 * cos(pi / 5)
    mp.dps = decimal_places
    return +phi


def golden_ratio_trig_sin(decimal_places: int = 1000) -> "mpf":
    """
    Compute φ using the identity φ = 1 + 2·sin(π/10).

    Parameters
    ----------
    decimal_places : int
        Output precision.

    Returns
    -------
    mpf
        φ = 1 + 2·sin(π/10).
    """
    mp.dps = decimal_places + 10
    phi = mpf(1) + 2 * sin(pi / 10)
    mp.dps = decimal_places
    return +phi


def golden_ratio_trig_sin2(decimal_places: int = 1000) -> "mpf":
    """
    Compute φ using the identity φ = 2·sin(3π/10).

    Parameters
    ----------
    decimal_places : int
        Output precision.

    Returns
    -------
    mpf
        φ = 2·sin(3π/10).
    """
    mp.dps = decimal_places + 10
    phi = 2 * sin(3 * pi / 10)
    mp.dps = decimal_places
    return +phi


def convergence_data_trig(decimal_places: int = 100) -> list:
    """
    Return results from all three trigonometric formulas.

    Returns
    -------
    list of (formula_name, value, error, correct_digits)
    """
    mp.dps = decimal_places + 10
    exact = +_phi_exact
    results = []
    for name, func in [
        ("2·cos(π/5)", golden_ratio_trig),
        ("1+2·sin(π/10)", golden_ratio_trig_sin),
        ("2·sin(3π/10)", golden_ratio_trig_sin2),
    ]:
        value = func(decimal_places)
        error = fabs(value - exact)
        correct_digits = int(-log10(error)) if error > 0 else decimal_places
        results.append((name, value, error, correct_digits))
    return results
