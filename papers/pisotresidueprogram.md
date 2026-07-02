# The Pisot Cross-Shell Residue — program record

One day of machine mathematics, 2026-07-02: a session note, four rounds of
executed extensions, three independent verification passes, and a referee
pass — every load-bearing claim decided in exact arithmetic, every artifact
SHA-pinned, nothing promoted past its evidence.

## The question

The relational-charge framework grades the conjugates of an algebraic number
into *coherence classes*: two roots cohere when their angle difference is
rational. For Pisot numbers (one real root $\theta > 1$, all other conjugates
strictly inside the unit circle) the framework's modulus-pinning theorem
kills almost every possible coherence — except one: **mirrored cross-shell
classes** between two non-real conjugate pairs on distinct shells. That
residue is invisible to transport arguments (no level-2 pin exists), so it
must be *executed*: for each certified Pisot, build the ratio object
$\mathrm{Rat}_p = \mathrm{Res}_y(p(y), p(xy))$, isolate the unimodular-root
factor $S^*$, form the composed square $C_2$ (all ordered products of
$S^*$-roots, degree up to $1764$), and scan its cyclotomic content
completely. The negative certificate $\{\Phi_1^{\deg S^*}\}$ — nothing but
the forced diagonal — means *no product of two conjugate-ratio values is a
root of unity*: no mirrored class.

## What was executed

| round | population | result |
|---|---|---|
| session note (v1.0) | $[-2,2]^5$: 83 Pisot quintics, 67 two-pair | 67/67 inert |
| N2 (v1.1) | $[-3,3]^5$: 431 Pisots, 313 two-pair | 313/313 inert |
| N3 (v1.1) | $\{-2..2\}^6$ degree-12 Salem census: 7 875 classes, 589 Salem | 589/589 inert |
| N4 (v1.2) | $[-2,2]^6$: 160 sextics; $[-2,2]^7$: 414 septics incl. the **first 309 three-pair instances** | 573/573 live scans inert |
| P-series (v1.3) | $[-4,4]^5$: 1 545 quintics, 1 063 two-pair; totally-real sweep degrees 2–7 | 1 063/1 063 inert; $\theta \ge \varphi$ certified 13/13 |
| referee errata (v1.4) | independent referee pass | E1–E3 verified & folded; no theorem touched |

**Bottom line: 2 016 live instances across degrees 5–7 and three quintic
boxes, zero mirrored cross-shell classes, zero falsifiers.** The general
Pisot-inertness conjecture (P1) stays `[OPEN]` — the point of the falsifier
table is that it *could* have failed today and did not.

## Three census surprises

1. **Genuine Pisots hide in the degenerate-chain population.** The
   Schur–Cohn and Möbius–Routh certificate paths all degenerate on some
   candidates (e.g. every $|c_0| = 1$ case kills Schur–Cohn at
   $\delta_1 = c_0^2 - 1 = 0$). Three of those candidates — at degrees 4, 5,
   and 7 — turned out to be genuine Pisot polynomials, caught only by exact
   in-run adjudication (a scaled Schur–Cohn sandwich at rational radii
   straddling 1). A census that silently skips its degenerate chains
   undercounts. Unconditional adjudication is now mandatory discipline.
2. **The reciprocal shortcut fails exactly at degree 2** (referee erratum
   E1): $x^2 - 3x + 1$ — the minimal polynomial of $\varphi^2$ — is
   reciprocal *and* Pisot. "Reciprocal ⇒ not Pisot" is forced only for
   degree ≥ 3.
3. **Non-generic Galois groups exist and stay inert** (prediction P7,
   resolved): twelve instances whose ratio object factors (three sextic,
   nine quintic), shrinking the scan instrument — the scans stay clean.

## Verify it yourself

Everything here regenerates from pinned drivers: the
[`n4-degree67/`](https://github.com/Echo-S-Studios/math-research-pipelines/tree/main/n4-degree67)
and
[`p-series/`](https://github.com/Echo-S-Studios/math-research-pipelines/tree/main/p-series)
packages each carry a zero-shot `RUNBOOK.sh` (manifest check → full
regeneration → byte-comparison against the pins), and the
[campaign reports](https://github.com/Echo-S-Studios/math-research-pipelines/tree/main/pisot-residue-verification)
record three independent verification sessions, including a 15-agent
adversarial referee pass over every `[FORCED]` certificate. Engines:
sympy 1.14.0 and PARI/GP 2.15.4 — two stacks sharing no computer-algebra
code, agreeing on every signature (237/237 ledger, 474 dual-path
executions, 4/4 N4 spot checks). Explore the full census interactively in
the [Pisot Census Explorer](pisot_census_explorer.html), or read the
[whitepaper v1.4](pisot_residue_whitepaper_v14.pdf).
