"""
Convergence Plot (رسم التقارب)
================================
Plots the convergence of each method toward φ as a function of iterations.
The y-axis shows the number of correct decimal digits.
"""

from __future__ import annotations


def plot_convergence(
    save_path: str | None = None,
    max_iterations: int = 150,
    decimal_places: int = 120,
    show: bool = True,
) -> None:
    """
    Plot the number of correct decimal digits vs. iteration for all iterative
    methods.

    Parameters
    ----------
    save_path : str or None
        If given, save the figure to this path.
    max_iterations : int
        Maximum iterations to evaluate.
    decimal_places : int
        Working precision.
    show : bool
        If True, call plt.show().
    """
    import matplotlib.pyplot as plt
    from golden_ratio_engine.core.method2_continued_fraction import convergence_data_cf
    from golden_ratio_engine.core.method3_nested_sqrt import convergence_data_nested_sqrt
    from golden_ratio_engine.core.method4_fibonacci import convergence_data_fibonacci
    from golden_ratio_engine.core.method5_lucas import convergence_data_lucas

    datasets = {
        "Continued Fraction": convergence_data_cf(max_iterations, decimal_places),
        "Nested Sqrt": convergence_data_nested_sqrt(max_iterations, decimal_places),
        "Fibonacci": convergence_data_fibonacci(max_iterations, decimal_places),
        "Lucas": convergence_data_lucas(max_iterations, decimal_places),
    }

    fig, ax = plt.subplots(figsize=(10, 6))
    for name, data in datasets.items():
        iters = [d[0] for d in data]
        digits = [d[3] for d in data]
        ax.plot(iters, digits, label=name, linewidth=2)

    ax.set_xlabel("Iterations", fontsize=13)
    ax.set_ylabel("Correct Decimal Digits", fontsize=13)
    ax.set_title(
        "Convergence of φ Computation Methods\n"
        "تقارب طرق حساب النسبة الذهبية",
        fontsize=14,
    )
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.4)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150)
    if show:
        plt.show()
    plt.close(fig)
