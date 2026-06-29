# CHANGES — post-pin repackaging ledger

## lambda = 2c closure (this revision)

This revision DERIVES the information exchange rate and inscribes it across the engine, the probes, and
both papers.

- **DERIVED the exchange rate: `lambda = 2c`** (companion Thm 4.6), closing open problem O1 and collapsing
  it with O4. The "2" is the structural 1/2 of the quadratic KL term, inverted; the residual freedom is the
  single conformal constant `c`. By Cencov's theorem `c` is a DECLARED scale (the Fisher metric is unique
  only up to a positive scale): `c=1` (Jeffreys) and `c=n` (degree-invariant) are the two readings already
  carried in `capacity.py` as `mult = (ambient_degree if degree_aware else 1)`; a third, framework-native
  value `c = sqrt(1+4C)/(2C)` (golden gate `sqrt5/2`) is selected by the self-action eigenframe at a gate.
  NOT claimed: that `c` is derived — it is a principled choice, per Cencov.
- **Forced flip / gates / frame-shift.** The discriminant `D = 1+4C` flips sign at `C = -1/4`: the
  frame-shift `c` (hence the metric `G/c`) goes real -> imaginary, the totally-real boundary. The gate
  ladder is `sqrt(1+4C)` in `{sqrt2, sqrt3, sqrt5}`; the self-action spectrum is `{-sqrt5, 0, +sqrt5}`.
- **`capacity.py`** (engine): documented that `mult` IS the conformal constant `c` and the floor is
  `2c*log(mu_S)`; and made the certified cost scale with `c` (`mult`) so the gate is consistently
  `lambda = 2c`. The **`info_threshold=False` default path is unchanged byte-for-byte** (and imports no
  mpmath on that path).
- **New probe** `L00M/training/test_a3p2c_lambda_conformal.py` (6 tests): derives `lambda = 2c` (the shipped
  `2` emerges as the `c=1` instance), unifies the floors `0.5624 / 2.2496 / 4.4992`, proves the self-action
  spectrum and the gate ladder, the frame-shift `c = sqrt5/2`, and the forced flip at `C = -1/4`. Written
  for extrapolation (the identity is solved at run time, not asserted as a constant).
- **Papers** updated in cadence: `residual_return_learning.tex` new Section 4.3 (Thm 4.6, Rem 4.7, Prop 4.9,
  Def 4.10, Table 2, Rem 4.11, Rem 4.12) plus open-problem and honesty-ledger updates; `vector_substrate.tex`
  `conj:model` forward-note. Both recompiled (30 / 29 pp, 0 undefined references).
- **Probes/audit extended**: companion probe +3 (17 -> 20); third witness `residual_return_audit.py` +3
  exact checks (the one documented 'shorthand' flag is intact); research probe `test_a3p2b_threshold.py`
  has `LAMBDA` annotated as the derived `2c`.
- **Seals**: `claim_map.json` +5 claims (50 -> 55); `MANIFEST.txt` counts and inventory updated;
  `SHA256SUMS` regenerated over the final tree (76 -> 77 entries — the new probe).
- **Re-seal polish** (this build): synced the published suite counts that were left stale by the additions
  above — `verify.py`'s Part-A label (companion probe `17 -> 20`) and the companion paper's reproducibility
  table + computational-aspects section (`17 -> 20` companion probe, `131 -> 137` training suite,
  `565 -> 574` full L00M repository suite, `17 -> 20` tests-total). No code or test logic changed; the
  companion PDF was recompiled (30 pp, 0 undefined references).
- **Re-verification**: `python3 verify.py` -> ALL GREEN (probes; walkthrough 55/55; training 137,
  kira-language 121). `sha256sum -c SHA256SUMS` -> all OK.
- **Still OPEN** (explicitly not claimed closed): the reciprocal-seed floor (the unsolved core of Lehmer's
  problem) and the perception/encoder front-end.

---

## Provenance — the F1/F2 repackaging (predates the lambda = 2c closure above)

This tree descends from the pinned-head verification package (L00M `f238d6b`, kira-language `44829ff`,
tag `b1-ready` = `a5892c7`). Before the lambda = 2c work recorded above, two delivery defects were fixed
and an integrity sidecar (`SHA256SUMS`) was added; both fixes are retained here. The lambda = 2c revision
then changed engine, probe, paper, and `claim_map.json` content on top of that base — so the earlier
"documentation/packaging only" and "bit-identical to the originals" framing no longer holds and has been
removed. The authoritative account of what changed, and the current re-verification, is the
**lambda = 2c closure** section above.

- **F1 — archive was double-gzipped.** The originally delivered artifact was gzip-of-gzip-of-tar, so the
  documented one-paste `tar -xzf ...tar.gz` failed. The repackage is a **single** gzip layer, so `tar -xzf`
  (or the suffix-agnostic `tar -xf`) works verbatim.

- **F2 — `pytest` was required but undeclared.** `verify.py` drives every probe, the walkthrough, and the
  full suites through `pytest`, but `requirements.txt` had listed only `sympy`, `mpmath`, `numpy`, so a
  literal `pip install -r requirements.txt && py verify.py` failed at Part A.1 on a machine without pytest.
  `pytest>=7.0` is now declared, and the inexact "`--quick` needs only sympy+mpmath" wording (which
  conflated the probe FILES' imports with the pytest RUNNER) is corrected in `requirements.txt`, `README.md`,
  and the `verify.py` docstring. The probe files do import only sympy+mpmath; pytest is the runner. The
  third witness (`paper/residual_return_audit.py`) remains genuinely pytest-free.

Per-file content hashes for the current tree are in `SHA256SUMS` (77 entries; verify with
`sha256sum -c SHA256SUMS` from the package root).
