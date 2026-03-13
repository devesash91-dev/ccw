"""
Error Comparison Plot (رسم مقارنة الخطأ)
==========================================
Bar chart comparing the absolute error of all 8 methods at a fixed
number of iterations / evaluation cost.
"""

from __future__ import annotations


def plot_error_comparison(
    decimal_places: int = 50,
    save_path: str | None = None,
    show: bool = True,
) -> None:
    """
    Plot a bar chart of the absolute error for all 8 methods.

    Parameters
    ----------
    decimal_places : int
        Precision used when computing each method's value.
    save_path : str or None
        If given, save the figure to this path.
    show : bool
        If True, call plt.show().
    """
    import matplotlib.pyplot as plt
    import math
    from mpmath import mp, fabs, log10, phi as _phi_exact, mpf

    from golden_ratio_engine.core.method1_algebraic import golden_ratio_algebraic
    from golden_ratio_engine.core.method2_continued_fraction import golden_ratio_cf
    from golden_ratio_engine.core.method3_nested_sqrt import golden_ratio_nested_sqrt
    from golden_ratio_engine.core.method4_fibonacci import golden_ratio_fibonacci
    from golden_ratio_engine.core.method5_lucas import golden_ratio_lucas
    from golden_ratio_engine.core.method6_any_sequence import golden_ratio_any_sequence
    from golden_ratio_engine.core.method7_trigonometric import golden_ratio_trig
    from golden_ratio_engine.core.method8_matrix import golden_ratio_matrix

    mp.dps = decimal_places + 20
    exact = +_phi_exact
    iters = decimal_places * 10

    methods = {
        "Algebraic":          golden_ratio_algebraic(decimal_places),
        "Continued Fraction": golden_ratio_cf(iters, decimal_places),
        "Nested Sqrt":        golden_ratio_nested_sqrt(iters, decimal_places),
        "Fibonacci":          golden_ratio_fibonacci(iters, decimal_places),
        "Lucas":              golden_ratio_lucas(iters, decimal_places),
        "Any Sequence":       golden_ratio_any_sequence(7, 3, iters, decimal_places),
        "Trigonometric":      golden_ratio_trig(decimal_places),
        "Matrix":             golden_ratio_matrix(iters, decimal_places),
    }

    names = list(methods.keys())
    errors = []
    for v in methods.values():
        err = fabs(mpf(v) - exact)
        if err == 0:
            errors.append(decimal_places + 5)  # perfect precision
        else:
            errors.append(float(-log10(err)))  # correct digits

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(names, errors, color="steelblue", edgecolor="navy", alpha=0.8)

    ax.set_ylabel("Correct Decimal Digits  (-log₁₀ |error|)", fontsize=12)
    ax.set_xlabel("Method", fontsize=12)
    ax.set_title(
        f"Error Comparison of 8 φ Methods  (working precision = {decimal_places} dp)\n"
        "مقارنة دقة 8 طرق لحساب النسبة الذهبية",
        fontsize=13,
    )
    ax.set_xticklabels(names, rotation=30, ha="right", fontsize=10)
    ax.grid(axis="y", alpha=0.4)

    for bar, val in zip(bars, errors):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.3,
            f"{val:.1f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150)
    if show:
        plt.show()
    plt.close(fig)
