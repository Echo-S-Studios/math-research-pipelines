#!/usr/bin/env python3
"""fold_w_series.py -- fold the executed N4 (degrees 6-7) into the pisot
whitepaper: v1.1 -> v1.2.

Edits (W-series):
  W1  date line: v1.2 marker
  W2  abstract addendum sentence extended with N4
  W3  section retitled "Box and degree extensions"; N4 subsection appended
      (census + in-run adjudication incl. the degenerate-chain Pisot at
      degree 7; scans; P7 resolution; GP corroboration)
  W4  next-steps item N4 marked executed
  W5  predictions table: P7 resolved, P8 range extended, P1 status line
      extended to the full evidence base
  W6  appendix: N4 runtimes

All-or-nothing anchored edits; output <input .v11.tex> -> .v12.tex.
Usage: python3 fold_w_series.py pisot_residue_whitepaper.v11.tex
"""
import sys

E = []

E.append(("W1", r"""\date{July 2, 2026; v1.1 addendum (box extensions executed) folded same day \\ \small Session note; all computations exact, artifact manifest in Appendix~A.}""",
r"""\date{July 2, 2026; v1.1 (box extensions) and v1.2 (degree extensions N4) addenda folded same day \\ \small Session note; all computations exact, artifact manifest in Appendix~A.}"""))

E.append(("W2", r"""Salem twist-classes in $\{-2,\dots,2\}^6$, all inert (P5, P6 confirmed); zero
falsifiers, nothing promoted.
\end{abstract}""",
r"""Salem twist-classes in $\{-2,\dots,2\}^6$, all inert (P5, P6 confirmed); zero
falsifiers, nothing promoted. \emph{v1.2 addendum:} N4 is executed
(\S\ref{sec:boxext}): $160$ Pisot sextics and $414$ Pisot septics in
$[-2,2]^n$ --- including the first three-pair population ($309$ instances)
and a degree-$7$ Pisot invisible to all four certificate paths, caught only
by exact adjudication --- all scans inert, P7 resolved affirmatively
($3$ reducible-$\Rat^{\circ}$ instances, $S^{*}$ shrinking to degrees
$12/12/24$, still inert).
\end{abstract}"""))

E.append(("W3a", r"""\section{Box extensions, executed (v1.1 addendum)}\label{sec:boxext}""",
r"""\section{Box and degree extensions, executed (v1.1--v1.2 addenda)}\label{sec:boxext}"""))

E.append(("W3b", r"""so exclusivity holds in the weaker, sufficient form ``both straddle
$\Rightarrow$ both reducible.'' \F

\section{Next steps and predictions}\label{sec:next}""",
r"""so exclusivity holds in the weaker, sufficient form ``both straddle
$\Rightarrow$ both reducible.'' \F

\subsection{N4: degrees $6$ and $7$, boxes $[-2,2]^n$ (v1.2)}
\label{sec:n4}

\textbf{Census, with in-run adjudication.} The four-path chain is now
computed \emph{unconditionally} and the degenerate-chain population is
adjudicated exactly in the same run (reciprocal $\Rightarrow$ not Pisot;
reducible $\Rightarrow$ rejected; otherwise $P\neq\pm\mathrm{rev}(P)$ with
$P$ irreducible forces $\gcd(P,\mathrm{rev}\,P)=1$, hence no unimodular
roots, and a scaled Schur--Cohn sandwich at rational radii straddling $1$
pins the interior count) --- zero candidates left unadjudicated, by
construction. A degree-$5$ regression run reproduces the archived census
and all $67$ scans exactly. Degree $6$ ($15625$ candidates): $\mathbf{160}$
Pisot sextics --- $159$ two-pair with real spectator
$(\theta,r,\lambda_1,\bar\lambda_1,\lambda_2,\bar\lambda_2)$, $1$ one-pair,
$0$ totally real; degenerate chains $2950$ ($150$ reciprocal / $2794$
reducible / $6$ irreducible non-Pisot / $0$ Pisot). Degree $7$ ($78125$
candidates): $\mathbf{414}$ Pisot septics --- $\mathbf{309}$ three-pair
(the first three-pair population) and $105$ two-pair with two real
spectators; degenerate chains $13598$ ($250/13316/31/\mathbf{1}$). The
$1$ is load-bearing: the degenerate-chain population contains a genuine
Pisot,
\[
x^7-2x^6+2x^5+2x^4-2x^3-x^2+1\qquad c=(1,-1,-2,2,2,-2,-2),
\]
invisible to all four certificate paths (its $c_0=1$ degenerates
Schur--Cohn at the first step and both M\"obius--Routh tables) and caught
only by the adjudication. At degree $7$ the empty-chain gap is no longer
hypothetical: unconditional adjudication is mandatory census discipline.
\C\ (censuses); \F\ (per instance).

\textbf{Decision.} Rat scans: $160/160$ and $414/414$ returned exactly
$\{\Phi_1^{n}\}$ (P3, as Theorem~\ref{thm:pin} forces). All $573$ live
instances ($159$ two-pair sextics; $105$ two-pair and $309$ three-pair
septics): $\Rat_p^{\circ}$ squarefree; detector $=$ number of non-real
pairs on \emph{every} instance (no merged shells anywhere); composed-square
scans returned exactly $\{\Phi_1^{\deg S^{*}}\}$ with $\Phi_2$-multiplicity
$0$ and no higher cyclotomic content: \emph{zero mirrored cross-shell
classes through degree $7$}. The three-pair pattern executes with the
machinery unchanged --- every pairwise $\nu$ is a product of two $u$'s,
all covered by the single composed square ($\deg S^{*}=42$,
$\deg C_2=1764$). Prediction P7 is resolved affirmatively: $3$ sextic
instances have reducible $\Rat_p^{\circ}$ (factor shapes $12{+}18$,
$12{+}18$, $6{+}24$), the qualifying product $S^{*}$ shrinking to degrees
$12/12/24$, scans still inert. Cross-engine: \gp\ spot checks (full
\texttt{factor} $+$ \texttt{poliscyclo}, an independent decision path)
agree $4/4$, including the adjudicated instance. \F\ per instance; \C\
over the boxes.

\section{Next steps and predictions}\label{sec:next}"""))

E.append(("W4", r"""\item[\textbf{N4.}] Degrees $6$--$7$: degree $6$ contributes patterns
$(\theta,r,\lambda_1,\bar\lambda_1,\lambda_2,\bar\lambda_2)$ (two-pair with a
real spectator --- machinery unchanged) and real-heavy patterns closed by
Theorem~\ref{thm:pisot1pair}; the first three-pair pattern appears at degree
$7$, and $C_2$ still suffices there since every pairwise $\nu$ is a product of
two $u$'s.""",
r"""\item[\textbf{N4.}] Degrees $6$--$7$: degree $6$ contributes patterns
$(\theta,r,\lambda_1,\bar\lambda_1,\lambda_2,\bar\lambda_2)$ (two-pair with a
real spectator --- machinery unchanged) and real-heavy patterns closed by
Theorem~\ref{thm:pisot1pair}; the first three-pair pattern appears at degree
$7$, and $C_2$ still suffices there since every pairwise $\nu$ is a product of
two $u$'s. \emph{Executed:} \S\ref{sec:n4}."""))

E.append(("W5a", r"""Status: \F\ for at most one non-real pair (Theorem~\ref{thm:pisot1pair});
\C-empty on the first $67$ live instances (Theorem~\ref{thm:box}) and on all
$313$ two-pair instances of $[-3,3]^5$ (\S\ref{sec:boxext});""",
r"""Status: \F\ for at most one non-real pair (Theorem~\ref{thm:pisot1pair});
\C-empty on the first $67$ live instances (Theorem~\ref{thm:box}), on all
$313$ two-pair instances of $[-3,3]^5$, and on all $573$ live instances of
the degree-$6$/$7$ boxes including the first $309$ three-pair instances
(\S\ref{sec:boxext}, \S\ref{sec:n4});"""))

E.append(("W5b", r"""P7 & Two-pair instances with $\Rat_p^{\circ}$ reducible (smaller $S^{*}$)
exist for non-generic Galois groups. & \Pl & exhaustive extensions showing
irreducibility persists\\""",
r"""P7 & Two-pair instances with $\Rat_p^{\circ}$ reducible (smaller $S^{*}$)
exist for non-generic Galois groups. & \C\ (resolved: $3$ instances in
$[-2,2]^6$, shapes $12{+}18$, $12{+}18$, $6{+}24$; scans still inert,
\S\ref{sec:n4}) & ---\\"""))

E.append(("W5c", r"""P8 & Same-shell two-pair Pisot quintics (shell detector $=12$): none occurred
in $[-2,2]^5$ or $[-3,3]^5$ (\S\ref{sec:boxext},
Remark~\ref{rem:detector}); existence elsewhere undetermined. & \Op & (either
outcome informative)\\""",
r"""P8 & Same-shell two-pair Pisot quintics (shell detector $=12$): none occurred
in $[-2,2]^5$ or $[-3,3]^5$ (\S\ref{sec:boxext},
Remark~\ref{rem:detector}), and no merged shell occurred in any live
degree-$6$/$7$ instance (\S\ref{sec:n4}); existence elsewhere undetermined.
& \Op & (either outcome informative)\\"""))

E.append(("W6", r"""$69$\,s; ledger-M run 3 $1.8$\,s. v1.1 additions (authoring / verification
rerun): N2 scans $154/207$\,s; N3 census-and-scans $33/46$\,s; every v1.1
artifact regenerates byte-identically under both Python~3.12.3 and 3.11.15.""",
r"""$69$\,s; ledger-M run 3 $1.8$\,s. v1.1 additions (authoring / verification
rerun): N2 scans $154/207$\,s; N3 census-and-scans $33/46$\,s; every v1.1
artifact regenerates byte-identically under both Python~3.12.3 and 3.11.15.
v1.2 additions (N4, Python 3.11.15 / \sy~1.14.0 / \gp~2.15.4): censuses
$42$\,s (degrees $5$--$7$, degree-$5$ regression gate included); scans
$415$\,s (degree $6$) $+$ 1794\,s (degree $7$, four shards); \gp\ spot
deck $4/4$."""))


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    path = sys.argv[1]
    src = open(path, encoding="utf-8").read()
    bad = [(eid, src.count(old)) for eid, old, _ in E if src.count(old) != 1]
    if bad:
        for eid, n in bad:
            print(f"ANCHOR-FAIL {eid}: found {n} occurrences (need exactly 1).")
        sys.exit(1)
    out = src
    for eid, old, new in E:
        out = out.replace(old, new, 1)
        print(f"{eid} applied.")
    dst = path.replace(".v11.tex", ".v12.tex")
    open(dst, "w", encoding="utf-8").write(out)
    print(f"wrote {dst}")


if __name__ == "__main__":
    main()
