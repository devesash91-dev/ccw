"""
Golden Ratio Properties (خصائص النسبة الذهبية)
=================================================
Proves mathematically (via high-precision computation) the key properties
of φ = (1+√5)/2:

  1.  φ²     = φ + 1
  2.  1/φ    = φ − 1
  3.  φ·(1/φ)= 1
  4.  φ + 1/φ= √5
  5.  φ − 1/φ= 1
  6.  φ^n    = F(n)·φ + F(n−1)   (for any positive integer n)
  7.  φ²−(1/φ)² = √5   (derived from 1 and 2)

All properties are verified to 10,000 decimal places by default.
"""

from mpmath import mp, mpf, sqrt, power, fabs, phi as _phi_exact


def _fibonacci_pair(n: int):
    """Return (F(n), F(n+1)) as Python ints using fast doubling."""
    if n == 0:
        return (0, 1)
    a, b = _fibonacci_pair(n // 2)
    c = a * (2 * b - a)
    d = a * a + b * b
    if n % 2 == 0:
        return (c, d)
    return (d, c + d)


def verify_all_properties(decimal_places: int = 10000, verbose: bool = True) -> dict:
    """
    Verify all known mathematical properties of φ.

    Parameters
    ----------
    decimal_places : int
        Precision for verification (default 10,000).
    verbose : bool
        Print a human-readable report.

    Returns
    -------
    dict
        {property_name: {'passed': bool, 'residual': mpf}}
    """
    mp.dps = decimal_places + 20
    phi = +_phi_exact
    inv_phi = mpf(1) / phi
    sqrt5 = sqrt(mpf(5))
    tol = mpf(10) ** (-(decimal_places - 5))

    checks = {}

    def check(name: str, lhs: "mpf", rhs: "mpf"):
        residual = fabs(lhs - rhs)
        passed = residual < tol
        checks[name] = {"passed": passed, "residual": residual}
        if verbose:
            status = "✅" if passed else "❌"
            print(f"  {status}  {name:<35s}  residual={residual:.3e}")

    # 1. φ² = φ + 1
    check("φ² = φ + 1", phi ** 2, phi + 1)

    # 2. 1/φ = φ − 1
    check("1/φ = φ − 1", inv_phi, phi - 1)

    # 3. φ·(1/φ) = 1
    check("φ·(1/φ) = 1", phi * inv_phi, mpf(1))

    # 4. φ + 1/φ = √5
    check("φ + 1/φ = √5", phi + inv_phi, sqrt5)

    # 5. φ − 1/φ = 1
    check("φ − 1/φ = 1", phi - inv_phi, mpf(1))

    # 6. φ^n = F(n)·φ + F(n−1)  for n = 1..10
    for n in range(1, 11):
        fn, fn1 = _fibonacci_pair(n - 1)  # F(n-1), F(n)
        # fn = F(n-1), fn1 = F(n)
        rhs = mpf(fn1) * phi + mpf(fn)
        lhs = power(phi, n)
        check(f"φ^{n} = F({n})·φ + F({n-1})", lhs, rhs)

    # 7. φ² − (1/φ)² = √5
    check("φ² − (1/φ)² = √5", phi ** 2 - inv_phi ** 2, sqrt5)

    # 8. φ^2 - φ - 1 = 0   (characteristic equation)
    check("φ² − φ − 1 = 0", phi ** 2 - phi - 1, mpf(0))

    all_passed = all(v["passed"] for v in checks.values())
    if verbose:
        print()
        if all_passed:
            print(f"✅ All {len(checks)} properties verified to {decimal_places} decimal places!")
        else:
            failed = [k for k, v in checks.items() if not v["passed"]]
            print(f"❌ {len(failed)} propert(ies) FAILED: {failed}")

    return checks
