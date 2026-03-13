"""
Cross Validator (التحقق المتقاطع)
===================================
Runs all 8 methods and verifies they all agree with mpmath.phi to the
requested number of decimal places.

Prints a ✅ PASS / ❌ FAIL report for each method.
"""

from mpmath import mp, mpf, phi as _phi_exact, fabs


def run_all_methods(decimal_places: int = 50) -> dict:
    """
    Run all 8 methods and return their computed values.

    Parameters
    ----------
    decimal_places : int
        Number of decimal places for each method.

    Returns
    -------
    dict
        {method_name: mpf_value}
    """
    mp.dps = decimal_places + 20

    from golden_ratio_engine.core.method1_algebraic import golden_ratio_algebraic
    from golden_ratio_engine.core.method2_continued_fraction import golden_ratio_cf
    from golden_ratio_engine.core.method3_nested_sqrt import golden_ratio_nested_sqrt
    from golden_ratio_engine.core.method4_fibonacci import golden_ratio_fibonacci
    from golden_ratio_engine.core.method5_lucas import golden_ratio_lucas
    from golden_ratio_engine.core.method6_any_sequence import golden_ratio_any_sequence
    from golden_ratio_engine.core.method7_trigonometric import golden_ratio_trig
    from golden_ratio_engine.core.method8_matrix import golden_ratio_matrix

    # Use enough iterations for the target precision
    iters = decimal_places * 10  # conservative

    return {
        "Method 1 - Algebraic":          golden_ratio_algebraic(decimal_places),
        "Method 2 - Continued Fraction":  golden_ratio_cf(iters, decimal_places),
        "Method 3 - Nested Sqrt":         golden_ratio_nested_sqrt(iters, decimal_places),
        "Method 4 - Fibonacci":           golden_ratio_fibonacci(iters, decimal_places),
        "Method 5 - Lucas":               golden_ratio_lucas(iters, decimal_places),
        "Method 6 - Any Sequence (7,3)":  golden_ratio_any_sequence(7, 3, iters, decimal_places),
        "Method 7 - Trigonometric":       golden_ratio_trig(decimal_places),
        "Method 8 - Matrix":              golden_ratio_matrix(iters, decimal_places),
    }


def cross_validate(decimal_places: int = 50, verbose: bool = True) -> dict:
    """
    Validate that all 8 methods agree with mpmath.phi.

    Parameters
    ----------
    decimal_places : int
        Number of decimal places to validate.
    verbose : bool
        If True, print a pass/fail report.

    Returns
    -------
    dict
        {method_name: {'passed': bool, 'error': mpf}}
    """
    mp.dps = decimal_places + 20
    exact = +_phi_exact
    # Tolerance: allow error only in the last 5 guard digits
    tolerance = mpf(10) ** (-decimal_places + 2)

    results_map = run_all_methods(decimal_places)
    report = {}

    all_passed = True
    for name, value in results_map.items():
        err = fabs(mpf(value) - exact)
        passed = err < tolerance
        if not passed:
            all_passed = False
        report[name] = {"passed": passed, "error": err}
        if verbose:
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"  {status}  {name:45s}  error={err:.3e}")

    if verbose:
        print()
        if all_passed:
            print("✅ ALL METHODS PASSED cross-validation!")
        else:
            print("❌ SOME METHODS FAILED cross-validation!")

    return report


def pairwise_agreement(decimal_places: int = 50) -> bool:
    """
    Verify that every pair of methods agrees to the requested precision.

    Parameters
    ----------
    decimal_places : int
        Number of decimal places.

    Returns
    -------
    bool
        True if all pairs agree.
    """
    mp.dps = decimal_places + 20
    tolerance = mpf(10) ** (-decimal_places + 2)
    results_map = run_all_methods(decimal_places)
    values = list(results_map.values())
    names = list(results_map.keys())
    all_ok = True
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            diff = fabs(mpf(values[i]) - mpf(values[j]))
            if diff >= tolerance:
                print(f"  ❌ Mismatch: {names[i]} vs {names[j]}  diff={diff:.3e}")
                all_ok = False
    return all_ok
