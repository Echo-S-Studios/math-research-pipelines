#!/usr/bin/env python3
"""n4_lib.py -- N4: generic-degree Pisot census + cross-shell scan machinery.

Degree-n Pisot census over the box [-2,2]^n and the full scan instrument
(Rat scan; S*/C2 composed square) for the live patterns (>= 2 non-real
pairs). Exact arithmetic only: Fractions / Python ints / Sturm counts at
rational endpoints; no float crosses a decision boundary.

Census discipline (supersedes the N2 chain semantics; closes its audited
completeness gap BY CONSTRUCTION):
  * all four exact interior-count paths {SC, RH} x {P(x), (-1)^n P(-x)}
    are computed unconditionally;
  * any disagreement among non-degenerate paths is a hard AssertionError
    (soundness falsifier);
  * a fully degenerate (empty) chain is adjudicated exactly IN-RUN:
    reciprocal => not Pisot (a reciprocal polynomial has root pairs a, 1/a,
    so it cannot have exactly one root outside the closed unit disk unless
    a unimodular root exists, which Pisot forbids); reducible => not a
    Pisot minimal polynomial; otherwise P != +-rev(P) with P irreducible
    forces gcd(P, rev P) = 1, hence no unimodular roots, and a scaled
    Schur-Cohn sandwich at rational radii straddling 1 pins the interior
    count exactly. Zero candidates are left unadjudicated.

Pisot certificate: irreducible AND interior count == n-1 AND exactly one
real root in (1,4) (Cauchy bound 1 + 2 = 3 < 4 for the box).

Scan instrument, per certified instance:
  * Rat = Res_y(P(y), P(xy)), degree n^2; strip (x-1)^n exactly (forced
    multiplicity n for squarefree P); Rat° := primitive remainder;
  * complete torsion scan of Rat° (Phi_2 and all Phi_M, M >= 3, with
    phi(M) <= deg Rat°; candidate list complete by the PROVEN bound
    M <= 2 phi(M)^2 -- whitepaper Lemma 2.3, proof not sweep): pinning
    (Thm 7.13) forces the empty verdict, i.e. Rat contacts {Phi_1^n};
  * live patterns: Rat° squarefree (else the degenerate u_1 = u_2 offset,
    LOUD); factor over Z; S* = product of the self-reciprocal irreducible
    factors carrying unimodular roots (trace-down Sturm count > 0 on
    (-2,2); factors with unimodular roots are necessarily self-reciprocal);
    detector := distinct trace values of S* in (-2,2) -- with Rat°
    squarefree this equals the number of unimodular-root PAIRS (expected:
    the number of non-real shell pairs, for distinct shells);
  * C2 = composed square of S* (root multiset all ordered products), built
    by the Newton route (p_k(C2) = p_k(S*)^2) and cross-asserted against
    Res_y(S*(y), y^d S*(x0/y)) == C2(x0) at x0 in {2,3,5} (exact identity,
    S* monic); complete torsion scan of C2: negative certificate
    {Phi_1^{deg S*}} <=> no product of two S*-roots is a root of unity
    <=> no mirrored cross-shell class (and no u_i u_j^{+-1} torsion at
    all, covering every pairwise nu at any number of pairs).
"""
import json
import time
import types
from fractions import Fraction as F
from itertools import product
from math import gcd as igcd

from sympy import Poly, Symbol, ZZ, QQ, resultant, gcd as sgcd, factor_list

x, y = Symbol("x"), Symbol("y")

_SRC = open("/home/claude/n1/stage_a_certify.py").read().replace(
    'if __name__ == "__main__":\n    main()', '')
sa = types.ModuleType("sa")
exec(_SRC, sa.__dict__)


# ===================================================================== census
def neg_coeffs(coeffs):
    """Ascending coefficients of (-1)^n P(-x) (monic when P is monic)."""
    n = len(coeffs) - 1
    return tuple(c * (-1) ** ((i + n) % 2) for i, c in enumerate(coeffs))


def four_paths(coeffs):
    """Unconditional {SC, RH} x {P, negP}. Returns (values dict, empty?)."""
    neg = neg_coeffs(coeffs)
    vals = {}
    v, st = sa.schur_cohn_interior(coeffs)
    if st == "ok":
        vals["SC"] = v
    v, st = sa.routh_lhp(coeffs)
    if st.startswith("ok"):
        vals["RH"] = v
    v, st = sa.routh_lhp(neg)
    if st.startswith("ok"):
        vals["RHneg"] = v
    v, st = sa.schur_cohn_interior(neg)
    if st == "ok":
        vals["SCneg"] = v
    return vals


def interior_sandwich(coeffs):
    """Exact #{|z| < 1} for P with no unimodular roots (proved upstream)."""
    for k in (6, 10, 14, 20, 30, 44, 60):
        lo, hi = F(2 ** k - 1, 2 ** k), F(2 ** k + 1, 2 ** k)
        counts = []
        for lam in (lo, hi):
            scaled = [c * lam ** i for i, c in enumerate(coeffs)]
            cnt, st = sa.schur_cohn_interior(scaled)
            if st != "ok":
                counts = None
                break
            counts.append(cnt)
        if counts and counts[0] == counts[1]:
            return counts[0]
    raise AssertionError(("sandwich failed to separate", coeffs))


def census(n, out_path, log=print):
    """Exhaustive Pisot census over [-2,2]^n. Returns (rows, tallies)."""
    t0 = time.time()
    tal = dict(candidates=0, c0_zero=0, chain_target=0, chain_reject=0,
               empty=0, empty_reciprocal=0, empty_reducible=0,
               empty_interior=0, empty_pisot=0,
               sturm_reject=0, reducible=0, pisot=0)
    rows = []
    target = n - 1
    for c in product(range(-2, 3), repeat=n):
        tal["candidates"] += 1
        if c[0] == 0:
            tal["c0_zero"] += 1
            continue
        coeffs = c + (1,)
        vals = four_paths(coeffs)
        desc = [1] + [c[i] for i in range(n - 1, -1, -1)]
        if not vals:
            tal["empty"] += 1
            P = Poly(desc, x, domain=ZZ)
            rev = Poly(list(reversed(desc)), x, domain=ZZ)
            if P == rev or P == -rev:
                # [FORCED] for n >= 3 only (erratum E1): at degree 2 the
                # reciprocals x^2 - kx + 1, k >= 3, ARE Pisot (theta, 1/theta)
                if n >= 3:
                    tal["empty_reciprocal"] += 1
                    continue
                if not P.is_irreducible:
                    tal["empty_reducible"] += 1
                    continue
                # degree-2 self-inversive, irreducible: decide by the exact
                # discriminant (the sandwich cannot separate unimodular pairs)
                disc = c[1] * c[1] - 4 * c[0]
                if disc < 0:                      # unimodular pair: not Pisot
                    tal["empty_interior"] += 1
                    continue
                # real pair theta, 1/theta: interior count 1 automatically
                if int(P.count_roots(1, len(coeffs) + 3)) == 1:
                    tal["empty_pisot"] += 1
                    log(f"*** ADJUDICATED PISOT (degenerate chain): {c} ***")
                    rows.append(_certify_row(c, P, n, "adjudicated"))
                else:
                    tal["empty_interior"] += 1
                continue
            if not P.is_irreducible:
                tal["empty_reducible"] += 1
                continue
            assert Poly(sgcd(P, rev), x).degree() == 0, ("unimodular risk", c)
            # the sandwich is self-certifying: count agreement at rational
            # radii straddling 1 forces #{|z|<1} == #{|z|<=1} (no circle roots)
            inside = interior_sandwich(coeffs)
            if inside == target and int(P.count_roots(1, 4)) == 1:
                tal["empty_pisot"] += 1
                log(f"*** ADJUDICATED PISOT (degenerate chain): {c} ***")
                rows.append(_certify_row(c, P, n, "adjudicated"))
            else:
                tal["empty_interior"] += 1
            continue
        assert len(set(vals.values())) == 1, ("cross-path disagreement", c, vals)
        if next(iter(vals.values())) != target:
            tal["chain_reject"] += 1
            continue
        tal["chain_target"] += 1
        P = Poly(desc, x, domain=ZZ)
        if int(P.count_roots(1, 4)) != 1:
            tal["sturm_reject"] += 1
            continue
        if not P.is_irreducible:
            tal["reducible"] += 1
            continue
        rows.append(_certify_row(c, P, n, sorted(vals)))
        tal["pisot"] += 1
    tal["pisot"] += tal["empty_pisot"]
    with open(out_path, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    log(f"deg {n}: {json.dumps(tal)}")
    log(f"deg {n}: {len(rows)} Pisot, patterns "
        f"{_pattern_tally(rows)}  {time.time()-t0:.1f}s")
    return rows, tal


def _certify_row(c, P, n, certs):
    assert int(P.count_roots(-4, -1)) == 0, c
    r_total = int(P.count_roots(-4, 4))
    pairs = (n - r_total) // 2
    assert r_total >= 1 and (n - r_total) % 2 == 0, (c, r_total)
    return dict(c=list(c), real_roots=r_total, pairs=pairs,
                pattern=f"{r_total}r{pairs}p", certs=certs)


def _pattern_tally(rows):
    tal = {}
    for r in rows:
        tal[r["pattern"]] = tal.get(r["pattern"], 0) + 1
    return dict(sorted(tal.items()))


# ================================================================== scan core
def poly_from_asc(fr_list, sym):
    from sympy import Rational
    return Poly([Rational(c.numerator, c.denominator)
                 for c in reversed(fr_list)], sym, domain=QQ)


def horner(asc, v):
    acc = F(0)
    for cf in reversed(asc):
        acc = acc * v + cf
    return acc


def strip_root(asc, a):
    m, cur = 0, asc[:]
    while len(cur) > 1:
        out, acc = [], F(0)
        for cf in reversed(cur):
            acc = acc * a + cf
            out.append(acc)
        rem = out.pop()
        if rem != 0:
            break
        m += 1
        cur = list(reversed(out))
    return m, cur


def clear_denoms(asc):
    from math import lcm
    L = 1
    for cf in asc:
        L = lcm(L, cf.denominator)
    ints = [int(cf * L) for cf in asc]
    g = 0
    for v in ints:
        g = igcd(g, v)
    if g > 1:
        ints = [v // g for v in ints]
    return ints


_PHI_CACHE = {}


def totients(limit):
    """phi table to `limit`, asserting the (proven) bound 2 phi^2 >= M in-run."""
    if limit in _PHI_CACHE:
        return _PHI_CACHE[limit]
    phi = list(range(limit + 1))
    for i in range(2, limit + 1):
        if phi[i] == i:
            for j in range(i, limit + 1, i):
                phi[j] -= phi[j] // i
    for M in range(1, limit + 1):
        assert 2 * phi[M] * phi[M] >= M, ("2*phi^2 >= M fails in-table", M)
    _PHI_CACHE[limit] = phi
    return phi


def cyclo_eval(M, v):
    from sympy import divisors, mobius
    num, den = 1, 1
    for d in divisors(M):
        mu = int(mobius(M // d))
        if mu == 1:
            num *= v ** d - 1
        elif mu == -1:
            den *= v ** d - 1
    assert num % den == 0
    return num // den


_CAND_CACHE = {}


def torsion_candidates(degmax):
    """All M >= 3 with phi(M) <= degmax, with sieve values at 2,3,5.
    Complete by Lemma 2.3 (2 phi(M)^2 >= M, proven): sieve to 2*degmax^2."""
    if degmax in _CAND_CACHE:
        return _CAND_CACHE[degmax]
    limit = 2 * degmax * degmax
    phi = totients(limit)
    cand = [M for M in range(3, limit + 1) if phi[M] <= degmax]
    table = {M: (cyclo_eval(M, 2), cyclo_eval(M, 3), cyclo_eval(M, 5))
             for M in cand}
    _CAND_CACHE[degmax] = (phi, cand, table)
    return phi, cand, table


def scan_torsion(rem_asc, phi, cand, table):
    """Cyclotomic content (M >= 3, with multiplicity) of the stripped remainder."""
    from sympy import cyclotomic_poly
    A = clear_denoms(rem_asc)
    dA = len(A) - 1
    if dA == 0:
        return []
    A2, A3, A5 = (sum(cf * (v ** i) for i, cf in enumerate(A))
                  for v in (2, 3, 5))
    found = []
    for M in cand:
        if phi[M] > dA:
            continue
        e2, e3, e5 = table[M]
        if (A2 and A2 % e2) or (A3 and A3 % e3) or (A5 and A5 % e5):
            continue
        Ap = poly_from_asc([F(v) for v in A], x)
        PhM = Poly(cyclotomic_poly(M, x), x, domain=QQ)
        mult = 0
        while True:
            q, r = Ap.div(PhM)
            if not r.is_zero:
                break
            mult += 1
            Ap = q
        if mult:
            found.append((M, mult))
    return found


def build_rat(c, n):
    """Rat = Res_y(P(y), P(xy)); returns (m1, rat0_asc_primitive_int)."""
    coeffs = list(c) + [1]
    Py = sum(coeffs[k] * y ** k for k in range(n + 1))
    Pxy = sum(coeffs[k] * (x * y) ** k for k in range(n + 1))
    R = Poly(resultant(Py, Pxy, y), x, domain=ZZ)
    assert R.degree() == n * n, R.degree()
    asc = [F(v) for v in reversed(R.all_coeffs())]
    m1, rem = strip_root(asc, F(1))
    assert m1 == n, ("Phi1 multiplicity of Rat != n", c, m1)
    m2, rem = strip_root(rem, F(-1))
    A = clear_denoms(rem)
    return m2, [F(v) for v in A]


def newton_power_sums(asc_monic, K):
    """p_1..p_K of a monic poly given ascending coeffs (Newton's identities)."""
    d = len(asc_monic) - 1
    assert asc_monic[d] == 1
    e = [F(0)] * (d + 1)
    e[0] = F(1)
    for j in range(1, d + 1):
        e[j] = (-1) ** j * asc_monic[d - j]
    p = [None] * (K + 1)
    for k in range(1, K + 1):
        s = F(0)
        for i in range(1, min(k - 1, d) + 1):
            if e[i] and p[k - i]:
                s += (-1) ** (i - 1) * e[i] * p[k - i]
        if k <= d:
            s += (-1) ** (k - 1) * e[k] * k
        p[k] = s
    return p


def newton_from_power_sums(pr, N):
    """Monic ascending coeffs of the degree-N poly with power sums pr[1..N]."""
    e = [F(1)] + [F(0)] * N
    for k in range(1, N + 1):
        s, sign = F(0), 1
        for i in range(1, k + 1):
            if pr[i]:
                s += sign * e[k - i] * pr[i]
            sign = -sign
        e[k] = s / k
    asc = [F(0)] * (N + 1)
    for k in range(N + 1):
        asc[N - k] = e[k] if k % 2 == 0 else -e[k]
    return asc


def trace_down(asc, m):
    """D with  A(x) = x^m D(x + 1/x)  for self-reciprocal A of degree 2m."""
    T = [[F(2)], [F(0), F(1)]]
    for k in range(2, m + 1):
        nxt = [F(0)] * (len(T[k - 1]) + 1)
        for i, a in enumerate(T[k - 1]):
            nxt[i + 1] += a
        for i, a in enumerate(T[k - 2]):
            nxt[i] -= a
        T.append(nxt)
    D = [F(0)] * (m + 1)
    D[0] += asc[m]
    for k in range(1, m + 1):
        for i, a in enumerate(T[k]):
            D[i] += asc[m + k] * a
    return D


def is_self_reciprocal(asc):
    return asc == asc[::-1]


def sturm_unimodular_pairs(asc):
    """Distinct trace values in (-2,2) of a self-reciprocal even-degree poly."""
    d = len(asc) - 1
    assert d % 2 == 0 and is_self_reciprocal(asc)
    D = trace_down(asc, d // 2)
    Dp = poly_from_asc(D, x)
    return int(Dp.count_roots(-2, 2))


def build_sstar(rat0_asc):
    """Factor Rat°; S* = product of self-reciprocal factors carrying
    unimodular roots. Returns (sstar_asc_monic, factor_shape, n_qual)."""
    A = clear_denoms(rat0_asc)
    Ap = Poly(list(reversed(A)), x, domain=ZZ)
    # squarefree (degenerate-offset detector, LOUD)
    assert Poly(sgcd(Ap, Ap.diff(x)), x).degree() == 0, "Rat° not squarefree"
    _, facs = factor_list(Ap)
    shape = sorted(int(f.degree()) for f, m in facs)
    assert all(m == 1 for _, m in facs)
    parts = []
    for f, _ in facs:
        fa = [F(v) for v in reversed(Poly(f, x).all_coeffs())]
        if fa[-1] < 0:
            fa = [-v for v in fa]
        if len(fa) % 2 == 1 and is_self_reciprocal([v / fa[-1] for v in fa]):
            if sturm_unimodular_pairs([v / fa[-1] for v in fa]) > 0:
                parts.append([v / fa[-1] for v in fa])
    if not parts:
        return None, shape, 0
    s = [F(1)]
    for pa in parts:
        new = [F(0)] * (len(s) + len(pa) - 1)
        for i, a in enumerate(s):
            if a:
                for j, b in enumerate(pa):
                    if b:
                        new[i + j] += a * b
        s = new
    return s, shape, len(parts)


def composed_square(sstar_asc):
    """C2 via Newton (p_k(C2) = p_k(S*)^2), with dual-path resultant asserts."""
    d = len(sstar_asc) - 1
    N = d * d
    p = newton_power_sums(sstar_asc, N)
    pr = [None] + [p[k] * p[k] for k in range(1, N + 1)]
    c2 = newton_from_power_sums(pr, N)
    assert c2[N] == 1 and c2[0] == 1, "C2 not monic with C2(0)=1"
    assert c2 == c2[::-1], "C2 not self-reciprocal"
    assert sum(c2) == 0, "C2(1) != 0"
    Sy = poly_from_asc(sstar_asc, y)
    for x0 in (2, 3, 5):
        g_asc = [sstar_asc[d - j] * F(x0) ** (d - j) for j in range(d + 1)]
        G = poly_from_asc(g_asc, y)
        rv = resultant(Sy.as_expr(), G.as_expr(), y)
        from sympy import Rational
        lhs = F(int(Rational(rv).numerator), int(Rational(rv).denominator))
        assert lhs == horner(c2, F(x0)), ("dual-path mismatch", x0)
    return c2


def scan_instance(c, n, pairs, phi_rat, cand_rat, table_rat):
    """Full per-instance decision. Returns the record dict."""
    t0 = time.time()
    m2, rat0 = build_rat(c, n)
    rec = dict(c=list(c), n=n, pairs=pairs, rat_m2=m2)
    higher_rat = scan_torsion(rat0, phi_rat, cand_rat, table_rat)
    rec["rat_higher"] = higher_rat
    rec["rat_verdict"] = f"Phi1^{n}" + (f" Phi2^{m2}" if m2 else "") + \
        "".join(f" Phi{M}^{k}" for M, k in higher_rat)
    if pairs >= 2:
        sstar, shape, nq = build_sstar(rat0)
        rec["rat0_factor_shape"] = shape
        assert sstar is not None, ("no qualifying factor with >=2 pairs?!", c)
        d = len(sstar) - 1
        rec["deg_sstar"] = d
        rec["detector"] = sturm_unimodular_pairs(sstar)
        c2 = composed_square(sstar)
        m1c, rem = strip_root(c2, F(1))
        m2c, rem = strip_root(rem, F(-1))
        rec["c2_m1"], rec["c2_m2"] = m1c, m2c
        phi2, cand2, table2 = torsion_candidates(d * d - d)
        rec["c2_higher"] = scan_torsion(rem, phi2, cand2, table2)
        rec["c2_verdict"] = f"Phi1^{m1c}" + (f" Phi2^{m2c}" if m2c else "") + \
            "".join(f" Phi{M}^{k}" for M, k in rec["c2_higher"])
        rec["clean"] = (m2 == 0 and not higher_rat and m1c == d and
                        m2c == 0 and not rec["c2_higher"] and
                        rec["detector"] == pairs)
    else:
        rec["clean"] = (m2 == 0 and not higher_rat)
    rec["secs"] = round(time.time() - t0, 2)
    return rec
