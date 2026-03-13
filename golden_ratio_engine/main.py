"""
Golden Ratio Engine — Main Entry Point
=======================================
محرك اكتشاف النسبة الذهبية - نقطة الدخول

Usage
-----
  python main.py                     # default 1000 digits
  python main.py --digits 10000      # 10000 digits
  python main.py --visualize         # generate plots
  python main.py --all               # everything (long run)

The script:
  1. Displays φ to the requested precision
  2. Runs all 8 methods and shows results
  3. Shows the convergence report
  4. Shows the error report
  5. Shows the cross-validation report
  6. Proves mathematical properties
"""

import argparse
import sys
import os

# Allow running as `python main.py` from inside the golden_ratio_engine folder
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PARENT = os.path.dirname(_THIS_DIR)
if _PARENT not in sys.path:
    sys.path.insert(0, _PARENT)


def _hr(char: str = "─", width: int = 72) -> str:
    return char * width


def display_phi(digits: int) -> None:
    """Print φ to *digits* decimal places."""
    from golden_ratio_engine.precision.mpmath_engine import phi_to_n_digits

    s = phi_to_n_digits(digits)
    print(_hr("═"))
    print(f"  φ = {s[:80]}...")
    if digits > 80:
        print(f"      ... ({digits} decimal places)")
    print(_hr("═"))


def run_methods(digits: int) -> dict:
    """Run all 8 methods and print results."""
    from mpmath import mp, phi as _phi_exact, fabs, log10, mpf

    mp.dps = digits + 20
    exact = +_phi_exact
    iters = digits * 10

    from golden_ratio_engine.core.method1_algebraic import golden_ratio_algebraic
    from golden_ratio_engine.core.method2_continued_fraction import golden_ratio_cf
    from golden_ratio_engine.core.method3_nested_sqrt import golden_ratio_nested_sqrt
    from golden_ratio_engine.core.method4_fibonacci import golden_ratio_fibonacci
    from golden_ratio_engine.core.method5_lucas import golden_ratio_lucas
    from golden_ratio_engine.core.method6_any_sequence import golden_ratio_any_sequence
    from golden_ratio_engine.core.method7_trigonometric import golden_ratio_trig
    from golden_ratio_engine.core.method8_matrix import golden_ratio_matrix

    methods = {
        "Method 1  Algebraic          φ = (1+√5)/2":          lambda: golden_ratio_algebraic(digits),
        "Method 2  Continued Fraction  [1;1,1,1,...]":         lambda: golden_ratio_cf(iters, digits),
        "Method 3  Nested Sqrt         √(1+√(1+...))":         lambda: golden_ratio_nested_sqrt(iters, digits),
        "Method 4  Fibonacci           F(n+1)/F(n)":           lambda: golden_ratio_fibonacci(iters, digits),
        "Method 5  Lucas               L(n+1)/L(n)":           lambda: golden_ratio_lucas(iters, digits),
        "Method 6  Any Sequence        (a=7,b=3)":             lambda: golden_ratio_any_sequence(7, 3, iters, digits),
        "Method 7  Trigonometric       2·cos(π/5)":            lambda: golden_ratio_trig(digits),
        "Method 8  Q-Matrix            Q^n[0][0]/Q^n[0][1]":  lambda: golden_ratio_matrix(iters, digits),
    }

    results = {}
    print(f"\n{'Method':<50}  {'Correct digits':>15}")
    print(_hr())
    for name, fn in methods.items():
        value = fn()
        err = fabs(value - exact)
        cd = int(-log10(err)) if err > 0 else digits
        results[name] = value
        print(f"  {name:<48}  {cd:>15d}")
    return results


def run_convergence_report(digits: int = 50) -> None:
    """Print a short convergence summary."""
    from golden_ratio_engine.core.method2_continued_fraction import convergence_data_cf
    from golden_ratio_engine.core.method3_nested_sqrt import convergence_data_nested_sqrt
    from golden_ratio_engine.core.method4_fibonacci import convergence_data_fibonacci

    print("\n  Convergence (iterations needed for N correct digits):")
    print(f"  {'Method':<25}  {'10 digits':>10}  {'20 digits':>10}  {'30 digits':>10}")
    print("  " + _hr("-", 60))

    datasets = {
        "Continued Fraction": convergence_data_cf(300, digits + 10),
        "Nested Sqrt":        convergence_data_nested_sqrt(300, digits + 10),
        "Fibonacci":          convergence_data_fibonacci(300, digits + 10),
    }

    for name, data in datasets.items():
        targets = {10: None, 20: None, 30: None}
        for it, val, err, cd in data:
            for t in targets:
                if targets[t] is None and cd >= t:
                    targets[t] = it
        row = "  ".join(f"{targets[t] or '>300':>10}" for t in sorted(targets))
        print(f"  {name:<25}  {row}")


def run_cross_validation(digits: int) -> None:
    """Run cross-validation and print report."""
    from golden_ratio_engine.precision.cross_validator import cross_validate

    print()
    cross_validate(decimal_places=digits, verbose=True)


def run_properties(digits: int) -> None:
    """Verify mathematical properties."""
    from golden_ratio_engine.properties.golden_properties import verify_all_properties

    print()
    verify_all_properties(decimal_places=digits, verbose=True)


def run_visualizations(digits: int) -> None:
    """Generate and save all visualization plots."""
    import os

    out_dir = os.path.join(_THIS_DIR, "output")
    os.makedirs(out_dir, exist_ok=True)

    from golden_ratio_engine.visualization.convergence_plot import plot_convergence
    from golden_ratio_engine.visualization.golden_spiral import plot_golden_spiral
    from golden_ratio_engine.visualization.error_comparison import plot_error_comparison

    print("  Generating convergence plot...")
    plot_convergence(save_path=os.path.join(out_dir, "convergence.png"), show=False)

    print("  Generating golden spiral...")
    plot_golden_spiral(save_path=os.path.join(out_dir, "golden_spiral.png"), show=False)

    print("  Generating error comparison...")
    plot_error_comparison(
        decimal_places=min(digits, 50),
        save_path=os.path.join(out_dir, "error_comparison.png"),
        show=False,
    )
    print(f"  Plots saved to {out_dir}/")


def main():
    parser = argparse.ArgumentParser(
        description="Golden Ratio Engine — محرك اكتشاف النسبة الذهبية"
    )
    parser.add_argument(
        "--digits", type=int, default=1000,
        help="Number of decimal places to compute (default: 1000)"
    )
    parser.add_argument(
        "--visualize", action="store_true",
        help="Generate and save visualization plots"
    )
    parser.add_argument(
        "--all", dest="all_steps", action="store_true",
        help="Run everything including high-precision and visualisations"
    )
    args = parser.parse_args()

    digits = args.digits
    do_all = args.all_steps

    print()
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║          Golden Ratio Engine  |  محرك اكتشاف النسبة الذهبية        ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print(f"\n  Requested precision: {digits} decimal places")

    print(f"\n{'φ to requested precision':}")
    display_phi(digits)

    print(f"\n{'8 Methods — error summary':}")
    run_methods(digits)

    print(f"\n{'Convergence report':}")
    run_convergence_report(digits)

    print(f"\n{'Cross-validation':}")
    run_cross_validation(digits)

    print(f"\n{'Mathematical properties':}")
    run_properties(min(digits, 1000))

    if args.visualize or do_all:
        print(f"\n{'Visualizations':}")
        run_visualizations(digits)

    print("\nDone! ✅\n")


if __name__ == "__main__":
    main()
