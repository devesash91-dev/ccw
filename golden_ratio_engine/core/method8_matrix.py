"""
Method 8: Fibonacci Q-Matrix (مصفوفة فيبوناتشي)
=================================================
The Fibonacci Q-matrix is defined as:

    Q = [[1, 1],
         [1, 0]]

It satisfies Q^n = [[F(n+1), F(n)],
                    [F(n),   F(n-1)]]

Therefore φ ≈ Q^n[0][0] / Q^n[0][1] = F(n+1) / F(n).

Using matrix exponentiation by squaring (fast doubling principle) this runs
in O(log n) integer multiplications rather than O(n), making it much faster
than iterative Fibonacci for large n.

Convergence: Linear in the number of *Fibonacci terms* computed, but each
doubling step doubles the term index, so it takes only O(log n) steps.
"""

from mpmath import mp, mpf, phi as _phi_exact, fabs, log10


def _mat_mul(A: list, B: list) -> list:
    """
    Multiply two 2×2 integer matrices.

    Parameters
    ----------
    A, B : list of list of int
        2×2 integer matrices.

    Returns
    -------
    list of list of int
        Product A @ B.
    """
    return [
        [A[0][0] * B[0][0] + A[0][1] * B[1][0],
         A[0][0] * B[0][1] + A[0][1] * B[1][1]],
        [A[1][0] * B[0][0] + A[1][1] * B[1][0],
         A[1][0] * B[0][1] + A[1][1] * B[1][1]],
    ]


def _mat_pow(M: list, n: int) -> list:
    """
    Raise a 2×2 integer matrix to power n using fast exponentiation.

    Parameters
    ----------
    M : list of list of int
        2×2 integer matrix.
    n : int
        Non-negative exponent.

    Returns
    -------
    list of list of int
        M^n.
    """
    if n == 0:
        return [[1, 0], [0, 1]]  # identity
    if n == 1:
        return M
    if n % 2 == 0:
        half = _mat_pow(M, n // 2)
        return _mat_mul(half, half)
    return _mat_mul(M, _mat_pow(M, n - 1))


def golden_ratio_matrix(n: int = 5000, decimal_places: int = 1000) -> "mpf":
    """
    Compute φ via the Fibonacci Q-matrix raised to power n.

    Q^n = [[F(n+1), F(n)],
           [F(n),   F(n-1)]]
    φ ≈ F(n+1) / F(n)

    Parameters
    ----------
    n : int
        Matrix power (corresponds to the n-th Fibonacci number).
    decimal_places : int
        Output precision.

    Returns
    -------
    mpf
        F(n+1) / F(n), converging to φ.
    """
    mp.dps = decimal_places + 10
    Q = [[1, 1], [1, 0]]
    Qn = _mat_pow(Q, n)
    # Qn[0][0] = F(n+1), Qn[0][1] = F(n)
    phi = mpf(Qn[0][0]) / mpf(Qn[0][1])
    mp.dps = decimal_places
    return +phi


def convergence_data_matrix(
    steps: int = 20, decimal_places: int = 100
) -> list:
    """
    Return convergence data at exponentially-spaced matrix powers.

    Each step doubles the Fibonacci index, so convergence is geometric in
    the number of doubling steps.

    Parameters
    ----------
    steps : int
        Number of doubling steps to evaluate.
    decimal_places : int
        Working precision.

    Returns
    -------
    list of (n, value, error, correct_digits)
    """
    mp.dps = decimal_places + 10
    exact = +_phi_exact
    results = []
    for k in range(1, steps + 1):
        n = 2 ** k  # doubling
        value = golden_ratio_matrix(n, decimal_places)
        error = fabs(value - exact)
        correct_digits = int(-log10(error)) if error > 0 else decimal_places
        results.append((n, +value, error, correct_digits))
    return results
