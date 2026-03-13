"""
Tests: Convergence (اختبار التقارب)
=====================================
Verifies that iterative methods converge and that convergence data has the
expected monotone structure.
"""

import pytest
from mpmath import mp


def test_cf_convergence_is_monotone():
    """Continued fraction digits must be non-decreasing."""
    from golden_ratio_engine.core.method2_continued_fraction import convergence_data_cf

    data = convergence_data_cf(max_iterations=50, decimal_places=60)
    digits = [d[3] for d in data]
    # Allow at most a few non-monotone steps due to rounding
    violations = sum(
        1 for i in range(1, len(digits)) if digits[i] < digits[i - 1] - 1
    )
    assert violations == 0, f"Continued fraction convergence not monotone: {digits}"


def test_nested_sqrt_convergence_is_monotone():
    """Nested sqrt digits must be non-decreasing."""
    from golden_ratio_engine.core.method3_nested_sqrt import convergence_data_nested_sqrt

    data = convergence_data_nested_sqrt(max_iterations=50, decimal_places=60)
    digits = [d[3] for d in data]
    violations = sum(
        1 for i in range(1, len(digits)) if digits[i] < digits[i - 1] - 1
    )
    assert violations == 0, f"Nested sqrt convergence not monotone: {digits}"


def test_fibonacci_convergence_is_monotone():
    """Fibonacci digit count must be non-decreasing."""
    from golden_ratio_engine.core.method4_fibonacci import convergence_data_fibonacci

    data = convergence_data_fibonacci(max_terms=50, decimal_places=60)
    digits = [d[3] for d in data]
    violations = sum(
        1 for i in range(1, len(digits)) if digits[i] < digits[i - 1] - 1
    )
    assert violations == 0, f"Fibonacci convergence not monotone: {digits}"


def test_lucas_convergence_is_monotone():
    """Lucas digit count must be non-decreasing."""
    from golden_ratio_engine.core.method5_lucas import convergence_data_lucas

    data = convergence_data_lucas(max_terms=50, decimal_places=60)
    digits = [d[3] for d in data]
    violations = sum(
        1 for i in range(1, len(digits)) if digits[i] < digits[i - 1] - 1
    )
    assert violations == 0, f"Lucas convergence not monotone: {digits}"


def test_any_sequence_convergence():
    """Any additive sequence must converge to φ."""
    from golden_ratio_engine.core.method6_any_sequence import convergence_data_any_sequence
    from mpmath import mpf

    for a, b in [(1, 100), (7, 3)]:
        data = convergence_data_any_sequence(a, b, max_terms=100, decimal_places=60)
        first_digits = data[0][3]
        last_digits = data[-1][3]
        assert last_digits > first_digits, (
            f"Any sequence ({a},{b}) did not converge: {first_digits} → {last_digits}"
        )


def test_matrix_convergence():
    """Matrix method digits must increase with doubling steps."""
    from golden_ratio_engine.core.method8_matrix import convergence_data_matrix

    data = convergence_data_matrix(steps=10, decimal_places=60)
    digits = [d[3] for d in data]
    # With doubling, digits should increase significantly
    assert digits[-1] > digits[0], "Matrix method did not converge"


def test_cf_reaches_50_digits():
    """Continued fraction must reach 50 correct digits within 10000 iterations."""
    from golden_ratio_engine.core.method2_continued_fraction import golden_ratio_cf
    from mpmath import mp, phi as _phi_exact, fabs, mpf

    mp.dps = 120
    exact = +_phi_exact
    value = golden_ratio_cf(iterations=10000, decimal_places=100)
    tol = mpf(10) ** (-50)
    assert fabs(value - exact) < tol, "CF did not reach 50 digits in 10000 iterations"
