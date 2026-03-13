"""
Tests: Precision (اختبار الدقة)
=================================
The algebraic method and mpmath engine must produce φ correct to at least
10,000 decimal places.
"""

import pytest
from mpmath import mp, phi as _phi_exact, fabs, mpf


PRECISION_DIGITS = 1000  # use 1000 in tests for reasonable speed


def test_algebraic_high_precision():
    """Algebraic method must match mpmath.phi to PRECISION_DIGITS places."""
    from golden_ratio_engine.core.method1_algebraic import golden_ratio_algebraic

    mp.dps = PRECISION_DIGITS + 20
    exact = +_phi_exact
    value = golden_ratio_algebraic(PRECISION_DIGITS)
    tol = mpf(10) ** (-PRECISION_DIGITS + 2)
    assert fabs(value - exact) < tol, (
        f"Algebraic method failed {PRECISION_DIGITS}-digit precision check"
    )


def test_mpmath_engine_precision():
    """ultra_precision_phi must return φ correct to PRECISION_DIGITS places."""
    from golden_ratio_engine.precision.mpmath_engine import ultra_precision_phi

    mp.dps = PRECISION_DIGITS + 20
    exact = +_phi_exact
    value = ultra_precision_phi(PRECISION_DIGITS)
    tol = mpf(10) ** (-PRECISION_DIGITS + 2)
    assert fabs(value - exact) < tol, (
        f"ultra_precision_phi failed {PRECISION_DIGITS}-digit precision check"
    )


def test_phi_to_n_digits_format():
    """phi_to_n_digits should return a string starting with '1.'."""
    from golden_ratio_engine.precision.mpmath_engine import phi_to_n_digits

    s = phi_to_n_digits(50)
    assert s.startswith("1."), f"Expected string starting with '1.', got {s!r}"


def test_phi_digits_list_length():
    """phi_digits_list should return the correct number of digits."""
    from golden_ratio_engine.precision.mpmath_engine import phi_digits_list

    digits = phi_digits_list(100)
    assert len(digits) >= 100, f"Expected ≥100 digits, got {len(digits)}"
    assert all(0 <= d <= 9 for d in digits), "All digits must be 0-9"


def test_trigonometric_high_precision():
    """Trigonometric method must match mpmath.phi to PRECISION_DIGITS places."""
    from golden_ratio_engine.core.method7_trigonometric import golden_ratio_trig

    mp.dps = PRECISION_DIGITS + 20
    exact = +_phi_exact
    value = golden_ratio_trig(PRECISION_DIGITS)
    tol = mpf(10) ** (-PRECISION_DIGITS + 2)
    assert fabs(value - exact) < tol, (
        f"Trigonometric method failed {PRECISION_DIGITS}-digit precision check"
    )
