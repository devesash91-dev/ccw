"""
Tests: Mathematical Properties (اختبار الخصائص الرياضية)
==========================================================
All fundamental properties of φ must hold to at least 1e-100 precision.
"""

import pytest
from mpmath import mp, phi as _phi_exact, fabs, sqrt, power, mpf


DECIMAL_PLACES = 200
TOL = mpf(10) ** (-100)


@pytest.fixture(autouse=True)
def set_precision():
    mp.dps = DECIMAL_PLACES + 20


def _phi():
    mp.dps = DECIMAL_PLACES + 20
    return +_phi_exact


def test_phi_squared_equals_phi_plus_one():
    phi = _phi()
    assert fabs(phi ** 2 - (phi + 1)) < TOL, "φ² ≠ φ+1"


def test_reciprocal_equals_phi_minus_one():
    phi = _phi()
    assert fabs(mpf(1) / phi - (phi - 1)) < TOL, "1/φ ≠ φ-1"


def test_phi_times_reciprocal_equals_one():
    phi = _phi()
    assert fabs(phi * (mpf(1) / phi) - 1) < TOL, "φ·(1/φ) ≠ 1"


def test_phi_plus_reciprocal_equals_sqrt5():
    phi = _phi()
    assert fabs(phi + mpf(1) / phi - sqrt(mpf(5))) < TOL, "φ + 1/φ ≠ √5"


def test_phi_minus_reciprocal_equals_one():
    phi = _phi()
    assert fabs(phi - mpf(1) / phi - 1) < TOL, "φ − 1/φ ≠ 1"


def test_characteristic_equation():
    phi = _phi()
    assert fabs(phi ** 2 - phi - 1) < TOL, "φ² − φ − 1 ≠ 0"


@pytest.mark.parametrize("n", [1, 2, 3, 4, 5, 7, 10])
def test_power_fibonacci_relation(n):
    """φ^n = F(n)·φ + F(n-1)."""
    from golden_ratio_engine.properties.golden_properties import _fibonacci_pair

    phi = _phi()
    fn_minus1, fn = _fibonacci_pair(n - 1)  # returns (F(n-1), F(n))
    expected = mpf(fn) * phi + mpf(fn_minus1)
    assert fabs(power(phi, n) - expected) < TOL, f"φ^{n} ≠ F({n})·φ + F({n-1})"


def test_verify_all_properties():
    """The full properties checker must report all passed."""
    from golden_ratio_engine.properties.golden_properties import verify_all_properties

    results = verify_all_properties(decimal_places=500, verbose=False)
    failed = [k for k, v in results.items() if not v["passed"]]
    assert not failed, f"Properties failed: {failed}"
