# Changes — lambda2c-emissiongap-verification

## 2026-07-01 — closure-guard exactness fix + regression coverage (90 → 95 claims)

Corpus-wide FIX-INSTRUCTIONS, Part B (the one genuine code bug + its regression coverage).
No proven result changed; the emission-gap theorem and every prior claim are unaffected.

- **B1 — `emission_closure_guard.py::sign_in_Qsqrt5`.** The `b == 0` branch computed the sign
  as `(a > 0) - (a < 0)`; for a sympy `Rational`, `a > 0` is a `BooleanAtom`, so this raised
  `TypeError: BooleanAtom not allowed` whenever `R(φ)` is a **pure rational** — e.g. the degree-6
  Salem `x⁶−x⁵−x³−x+1` has `R(φ)=2`. The path was not exercised by the old suite (90/90 stayed
  green) but is on the guaranteed-exact decision boundary. Fixed by taking signs with `sp.sign`
  (`−1/0/+1`, never a BooleanAtom). Verified to preserve the β₄ verdict (`FORCED_ABOVE_FLOOR`)
  and the Lehmer-carrier verdict (`INVALID_CLOSURE`).
- **B1 regression** (`tests/test_p2_08_closure_guard.py`, `P2-GUARD-06`): `sign_in_Qsqrt5` on
  `2, −3, 3−2√5, 1+√5`; the deg-6 Salem carrier (traceless; previously crashed) → `INVALID_CLOSURE`.
- **B2 on-circle tensor** (`tests/test_p2_01_algebra.py`, `P2-ALG-05`): asserts `M(φ⊗φ)=φ²` (the
  tropical value), **not** `φ⁴`. Every other tensor case is off-circle, exactly where the wrong
  multiplicative formula and the correct tropical `(max,+)` law coincide — this guards that class.
- **B3 Salem factory** (new `tests/test_p2_10_salem_factory.py`, `P2-FACTORY-01…03`): the family
  `Sₙ = xⁿ(x²−x−1) − reverse` routes a sub-φ Salem for `n ∈ {6,10,12}` (`M = 1.50614, 1.60545,
  1.61340`) → `INVALID_CLOSURE`; each Salem's totally-real trace-down → `FORCED`; and the verdict
  does not track the trace (INVALID at trace 0 and 1, FORCED at trace 1 and 7).

Every fact above was re-derived in exact arithmetic (`sympy` + `mpmath`, floats for display only)
before the change. **Suite: 90 → 95 claims, all FORCED, 0 failed** (emission_gap 40 → 45).
