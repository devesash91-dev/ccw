# Golden Ratio Engine — محرك اكتشاف النسبة الذهبية

> φ = (1 + √5) / 2 = **1.6180339887498948482...**

A high-precision, multi-method engine for computing and validating the
golden ratio φ (phi) using Python and [mpmath](https://mpmath.org/).
Supports **up to 1,000,000 decimal places**.

---

## الوصف بالعربي

محرك احترافي لاكتشاف النسبة الذهبية (φ) بأعلى دقة ممكنة.
يستخدم **8 طرق مستقلة** كلها تصل إلى نفس النتيجة ويتحقق منها عبر cross-validation.
يعتمد على مكتبة `mpmath` التي تدعم دقة حتى ملايين الأرقام العشرية.

---

## Methods — الطرق الثماني

| # | Method | الطريقة | Convergence |
|---|--------|---------|-------------|
| 1 | Algebraic: φ = (1+√5)/2 | جبرية | Instant (single eval) |
| 2 | Continued Fraction: [1;1,1,1,...] | كسر مستمر | Linear ~0.209 digit/step |
| 3 | Nested Square Roots: √(1+√(1+...)) | جذور متداخلة | Linear ~0.209 digit/step |
| 4 | Fibonacci: lim F(n+1)/F(n) | فيبوناتشي | Linear ~0.209 digit/step |
| 5 | Lucas: lim L(n+1)/L(n) | لوكاس | Linear ~0.209 digit/step |
| 6 | Any Additive Sequence | أي متتالية جمعية | Linear ~0.209 digit/step |
| 7 | Trigonometric: 2·cos(π/5) | مثلثية | Instant (single eval) |
| 8 | Q-Matrix: Q^n[0][0]/Q^n[0][1] | مصفوفة Q | O(log n) steps |

---

## Project Structure — بنية المشروع

```
golden_ratio_engine/
├── __init__.py
├── main.py                          # Entry point
├── requirements.txt
├── README.md
│
├── core/                            # 8 independent methods
│   ├── method1_algebraic.py
│   ├── method2_continued_fraction.py
│   ├── method3_nested_sqrt.py
│   ├── method4_fibonacci.py
│   ├── method5_lucas.py
│   ├── method6_any_sequence.py
│   ├── method7_trigonometric.py
│   └── method8_matrix.py
│
├── precision/                       # High-precision engine
│   ├── mpmath_engine.py
│   ├── convergence_analyzer.py
│   ├── error_analysis.py
│   └── cross_validator.py
│
├── properties/
│   └── golden_properties.py         # Proves φ²=φ+1, 1/φ=φ-1, etc.
│
├── visualization/
│   ├── convergence_plot.py
│   ├── golden_spiral.py
│   └── error_comparison.py
│
└── tests/
    ├── test_all_methods.py
    ├── test_precision.py
    ├── test_properties.py
    └── test_convergence.py
```

---

## Installation — التثبيت

```bash
cd golden_ratio_engine
pip install -r requirements.txt
```

---

## Usage — الاستخدام

```bash
# Default: 1000 decimal places
python main.py

# Custom precision
python main.py --digits 10000

# With visualizations
python main.py --digits 1000 --visualize

# Everything
python main.py --digits 10000 --all
```

---

## Running Tests — تشغيل الاختبارات

```bash
cd golden_ratio_engine
pytest tests/ -v
```

---

## Key Results — النتائج الرئيسية

All 8 methods agree to the requested precision. Example cross-validation
output (50 decimal places):

```
  ✅ PASS  Method 1 - Algebraic                    error=0.000e+0
  ✅ PASS  Method 2 - Continued Fraction           error=0.000e+0
  ✅ PASS  Method 3 - Nested Sqrt                  error=0.000e+0
  ✅ PASS  Method 4 - Fibonacci                    error=0.000e+0
  ✅ PASS  Method 5 - Lucas                        error=0.000e+0
  ✅ PASS  Method 6 - Any Sequence (7,3)           error=0.000e+0
  ✅ PASS  Method 7 - Trigonometric                error=0.000e+0
  ✅ PASS  Method 8 - Matrix                       error=0.000e+0

✅ ALL METHODS PASSED cross-validation!
```

---

## Mathematical Properties Verified — الخصائص الرياضية المثبتة

| Property | Value |
|----------|-------|
| φ² = φ + 1 | ✅ 2.618... = 1.618... + 1 |
| 1/φ = φ − 1 | ✅ 0.618... = 1.618... − 1 |
| φ·(1/φ) = 1 | ✅ exactly |
| φ + 1/φ = √5 | ✅ 2.236... |
| φ − 1/φ = 1 | ✅ exactly |
| φ^n = F(n)·φ + F(n−1) | ✅ for all n |

---

## How mpmath.phi works — كيف يعمل mpmath.phi

`mpmath.phi` internally uses the **AGM (Arithmetic-Geometric Mean)** algorithm
to compute √5 with quadratic convergence (the number of correct digits *doubles*
each iteration). This is why it can compute millions of digits efficiently.

The algebraic method `(1 + sqrt(5)) / 2` piggy-backs on this same algorithm,
making it just as fast as the built-in constant.

---

## License

MIT
