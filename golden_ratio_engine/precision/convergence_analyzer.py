"""
Convergence Analyzer (محلل التقارب)
=====================================
Measures how many iterations each method needs to reach a target precision.

Classifies convergence speed:
  - Linear    : correct digits grow proportionally to iterations
  - Quadratic : correct digits double each iteration (Newton-Raphson class)
  - Exponential: correct digits double with each *doubling* of the index
"""

from mpmath import mp, mpf, phi as _phi_exact, fabs, log10


def _correct_digits(approx: "mpf", exact: "mpf") -> float:
    """Return the number of correct decimal digits in approx vs exact."""
    err = fabs(approx - exact)
    if err == 0:
        return float("inf")
    return float(-log10(err))


def iterations_for_precision(method_func, target_digits: int, max_iter: int = 100000) -> int:
    """
    Find the minimum number of iterations for *method_func* to achieve
    *target_digits* correct decimal digits.

    Parameters
    ----------
    method_func : callable
        A function (iterations, decimal_places) -> mpf.
    target_digits : int
        Target number of correct decimal digits.
    max_iter : int
        Upper bound on iterations to try.

    Returns
    -------
    int
        Number of iterations needed, or -1 if not achieved within max_iter.
    """
    working = target_digits + 20
    mp.dps = working
    exact = +_phi_exact

    # Binary search for the minimum iteration count
    lo, hi = 1, max_iter
    if _correct_digits(method_func(hi, working), exact) < target_digits:
        return -1  # can't reach target within max_iter

    while lo < hi:
        mid = (lo + hi) // 2
        if _correct_digits(method_func(mid, working), exact) >= target_digits:
            hi = mid
        else:
            lo = mid + 1
    return lo


def analyze_all_methods(
    target_digits_list: list = None,
    decimal_places: int = 200,
) -> dict:
    """
    Analyze convergence speed for all iterative methods.

    Parameters
    ----------
    target_digits_list : list of int
        Target digit counts to evaluate (default: [10, 50, 100]).
    decimal_places : int
        Working precision.

    Returns
    -------
    dict
        {method_name: {target_digits: iterations_needed}}
    """
    if target_digits_list is None:
        target_digits_list = [10, 50, 100]

    from golden_ratio_engine.core.method2_continued_fraction import golden_ratio_cf
    from golden_ratio_engine.core.method3_nested_sqrt import golden_ratio_nested_sqrt
    from golden_ratio_engine.core.method4_fibonacci import golden_ratio_fibonacci
    from golden_ratio_engine.core.method5_lucas import golden_ratio_lucas

    methods = {
        "Continued Fraction": golden_ratio_cf,
        "Nested Sqrt": golden_ratio_nested_sqrt,
        "Fibonacci": golden_ratio_fibonacci,
        "Lucas": golden_ratio_lucas,
    }

    results = {}
    for name, func in methods.items():
        results[name] = {}
        for target in target_digits_list:
            n = iterations_for_precision(func, target, max_iter=50000)
            results[name][target] = n
    return results


def convergence_rates(method_data: list) -> dict:
    """
    Estimate the convergence rate from a list of (iteration, value, error, digits).

    The convergence rate r is estimated as:
        r ≈ digits(2n) / digits(n)

    r ≈ 1 → linear; r ≈ 2 → quadratic.

    Parameters
    ----------
    method_data : list
        Output from any convergence_data_* function.

    Returns
    -------
    dict
        {'rate': float, 'classification': str}
    """
    if len(method_data) < 4:
        return {"rate": None, "classification": "insufficient data"}

    # Compare mid-point vs end-point digits
    mid = len(method_data) // 2
    digits_mid = method_data[mid][3]
    digits_end = method_data[-1][3]
    iter_mid = method_data[mid][0]
    iter_end = method_data[-1][0]

    if digits_mid <= 0 or iter_mid <= 0:
        return {"rate": None, "classification": "cannot compute"}

    # Digit growth factor
    if iter_end != iter_mid:
        rate = (digits_end - digits_mid) / (iter_end - iter_mid) * iter_mid / max(digits_mid, 1)
    else:
        rate = None

    if rate is None:
        classification = "unknown"
    elif rate < 1.5:
        classification = "linear"
    elif rate < 3.0:
        classification = "quadratic"
    else:
        classification = "super-quadratic"

    return {"rate": rate, "classification": classification}
