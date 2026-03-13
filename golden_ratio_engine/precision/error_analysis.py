"""
Error Analysis (تحليل الخطأ)
==============================
For each method and at each iteration, computes:
  - Absolute error  : |φ_approx − φ_exact|
  - Relative error  : |φ_approx − φ_exact| / φ_exact
  - Correct digits  : ⌊−log₁₀(|φ_approx − φ_exact|)⌋
  - Convergence rate: ratio of correct digits between consecutive steps
"""

from mpmath import mp, mpf, phi as _phi_exact, fabs, log10, log


def absolute_error(approx: "mpf", decimal_places: int = 100) -> "mpf":
    """
    Compute the absolute error |approx − φ_exact|.

    Parameters
    ----------
    approx : mpf
        Approximate value of φ.
    decimal_places : int
        Working precision.

    Returns
    -------
    mpf
        |approx − φ_exact|.
    """
    mp.dps = decimal_places + 10
    exact = +_phi_exact
    return fabs(mpf(approx) - exact)


def relative_error(approx: "mpf", decimal_places: int = 100) -> "mpf":
    """
    Compute the relative error |approx − φ_exact| / φ_exact.

    Parameters
    ----------
    approx : mpf
        Approximate value of φ.
    decimal_places : int
        Working precision.

    Returns
    -------
    mpf
        Relative error.
    """
    mp.dps = decimal_places + 10
    exact = +_phi_exact
    return fabs(mpf(approx) - exact) / exact


def correct_digits(approx: "mpf", decimal_places: int = 100) -> int:
    """
    Count the number of correct decimal digits in approx.

    Parameters
    ----------
    approx : mpf
        Approximate value of φ.
    decimal_places : int
        Working precision.

    Returns
    -------
    int
        Number of correct decimal digits (−log₁₀ of absolute error).
    """
    mp.dps = decimal_places + 10
    err = absolute_error(approx, decimal_places)
    if err == 0:
        return decimal_places
    return int(-log10(err))


def error_report(methods_results: dict, decimal_places: int = 100) -> dict:
    """
    Generate a full error report for a dictionary of method results.

    Parameters
    ----------
    methods_results : dict
        {method_name: mpf_value} mapping of computed φ values.
    decimal_places : int
        Working precision.

    Returns
    -------
    dict
        {method_name: {'abs_error': mpf, 'rel_error': mpf, 'correct_digits': int}}
    """
    mp.dps = decimal_places + 10
    exact = +_phi_exact
    report = {}
    for name, value in methods_results.items():
        v = mpf(value)
        abs_err = fabs(v - exact)
        rel_err = abs_err / exact
        cd = int(-log10(abs_err)) if abs_err > 0 else decimal_places
        report[name] = {
            "abs_error": abs_err,
            "rel_error": rel_err,
            "correct_digits": cd,
        }
    return report


def convergence_rate_from_series(correct_digits_series: list) -> list:
    """
    Estimate per-step convergence rate from a series of correct-digit counts.

    Parameters
    ----------
    correct_digits_series : list of int
        Correct digit counts at each iteration.

    Returns
    -------
    list of float
        Ratio digits[i+1] / digits[i] for each consecutive pair.
    """
    rates = []
    for i in range(1, len(correct_digits_series)):
        prev = correct_digits_series[i - 1]
        curr = correct_digits_series[i]
        if prev > 0:
            rates.append(curr / prev)
        else:
            rates.append(None)
    return rates
