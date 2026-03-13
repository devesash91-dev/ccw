"""
Tests: All 8 Methods (اختبار كل الطرق)
========================================
Each method must produce φ correct to at least 50 decimal places.
"""

import pytest
from mpmath import mp, phi as _phi_exact, fabs, mpf


@pytest.fixture(autouse=True)
def set_precision():
    mp.dps = 120


TOLERANCE_50 = mpf(10) ** (-50)


def _exact():
    mp.dps = 120
    return +_phi_exact


def test_method1_algebraic():
    from golden_ratio_engine.core.method1_algebraic import golden_ratio_algebraic
    value = golden_ratio_algebraic(100)
    assert fabs(value - _exact()) < TOLERANCE_50, "Method 1 (Algebraic) failed 50-digit check"


def test_method2_continued_fraction():
    from golden_ratio_engine.core.method2_continued_fraction import golden_ratio_cf
    value = golden_ratio_cf(iterations=5000, decimal_places=100)
    assert fabs(value - _exact()) < TOLERANCE_50, "Method 2 (Continued Fraction) failed 50-digit check"


def test_method3_nested_sqrt():
    from golden_ratio_engine.core.method3_nested_sqrt import golden_ratio_nested_sqrt
    value = golden_ratio_nested_sqrt(iterations=5000, decimal_places=100)
    assert fabs(value - _exact()) < TOLERANCE_50, "Method 3 (Nested Sqrt) failed 50-digit check"


def test_method4_fibonacci():
    from golden_ratio_engine.core.method4_fibonacci import golden_ratio_fibonacci
    value = golden_ratio_fibonacci(n_terms=5000, decimal_places=100)
    assert fabs(value - _exact()) < TOLERANCE_50, "Method 4 (Fibonacci) failed 50-digit check"


def test_method5_lucas():
    from golden_ratio_engine.core.method5_lucas import golden_ratio_lucas
    value = golden_ratio_lucas(n_terms=5000, decimal_places=100)
    assert fabs(value - _exact()) < TOLERANCE_50, "Method 5 (Lucas) failed 50-digit check"


def test_method6_any_sequence():
    from golden_ratio_engine.core.method6_any_sequence import golden_ratio_any_sequence
    for a, b in [(7, 3), (100, 1), (42, 99), (1, 1000)]:
        value = golden_ratio_any_sequence(a, b, n_terms=5000, decimal_places=100)
        assert fabs(value - _exact()) < TOLERANCE_50, (
            f"Method 6 (Any Sequence a={a}, b={b}) failed 50-digit check"
        )


def test_method7_trigonometric():
    from golden_ratio_engine.core.method7_trigonometric import (
        golden_ratio_trig,
        golden_ratio_trig_sin,
        golden_ratio_trig_sin2,
    )
    for func, name in [
        (golden_ratio_trig,      "trig cos"),
        (golden_ratio_trig_sin,  "trig sin"),
        (golden_ratio_trig_sin2, "trig sin2"),
    ]:
        value = func(100)
        assert fabs(value - _exact()) < TOLERANCE_50, f"Method 7 ({name}) failed 50-digit check"


def test_method8_matrix():
    from golden_ratio_engine.core.method8_matrix import golden_ratio_matrix
    value = golden_ratio_matrix(n=5000, decimal_places=100)
    assert fabs(value - _exact()) < TOLERANCE_50, "Method 8 (Matrix) failed 50-digit check"


def test_method6_invalid_inputs():
    from golden_ratio_engine.core.method6_any_sequence import golden_ratio_any_sequence
    with pytest.raises(ValueError):
        golden_ratio_any_sequence(-1, 3)
    with pytest.raises(ValueError):
        golden_ratio_any_sequence(1, -2)
