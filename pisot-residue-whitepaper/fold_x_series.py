#!/usr/bin/env python3
"""fold_x_series.py -- fold the fully-executed P-series into the pisot
whitepaper: v1.2 -> v1.3.

Edits (X-series):
  X1  date line: v1.3 marker
  X2  P-series subsection appended to the extensions section
  X3  predictions table: P1 status (2016-instance base), P2 next-box
      corollary, P3 observed aggregate, P4 standalone evidence, P7 degree-5
      witnesses, P8 range extended
  X4  appendix runtimes

All-or-nothing anchors; output .v12.tex -> .v13.tex.
Usage: python3 fold_x_series.py pisot_residue_whitepaper.v12.tex
"""
import sys

E = []

E.append(("X1", r"""\date{July 2, 2026; v1.1 (box extensions) and v1.2 (degree extensions N4) addenda folded same day \\ \small Session note; all computations exact, artifact manifest in Appendix~A.}""",
r"""\date{July 2, 2026; v1.1 (box extensions), v1.2 (degree extensions N4), and v1.3 (P-series executed in full) addenda folded same day \\ \small Session note; all computations exact, artifact manifest in Appendix~A.}"""))

E.append(("X2", r"""\texttt{factor} $+$ \texttt{poliscyclo}, an independent decision path)
agree $4/4$, including the adjudicated instance. \F\ per instance; \C\
over the boxes.

\section{Next steps and predictions}\label{sec:next}""",
r"""\texttt{factor} $+$ \texttt{poliscyclo}, an independent decision path)
agree $4/4$, including the adjudicated instance. \F\ per instance; \C\
over the boxes.

\subsection{The P-series, executed in full (v1.3)}\label{sec:pseries}

Every row of the falsifier table below received a definitive pass: the
resolved rows re-asserted from pinned records, the open rows given fresh
falsifier searches. Two new computations. \textbf{P4 (first standalone
execution):} the totally-real populations of the boxes $[-3,3]^{2,3,4}$
($6/5/1$ instances of $6/37/103$ Pisots; the degree-$4$ census re-derived
under the v1.2 discipline matches the archived sweep, $103=103$) and the
degree-$5$--$7$ boxes ($0$ totally real, including $[-4,4]^5$) give $12$
totally-real Pisot instances; for each, $P(\varphi)$ is evaluated exactly
in $\Z[\varphi]$ ($\varphi^2=\varphi+1$ reduction; the sign of $a+b\varphi$
decided by integer squares against $\sqrt5$), and since $\theta$ is the
unique root above $1$: $\theta>\varphi\iff P(\varphi)<0$,
$\theta=\varphi\iff P=x^2-x-1$. Result: eleven strict certificates, one
equality (exactly the golden minimal polynomial), zero falsifiers. \F\ per
instance; \C\ over the populations. \textbf{P8/P1/P2 at $[-4,4]^5$:}
census $59049$ candidates $\to$ $\mathbf{1545}$ Pisot quintics ($1063$
two-pair, $482$ one-pair, $0$ totally real); the degenerate-chain
population ($7416$: $162/7220/33/\mathbf{1}$) again contains a genuine
Pisot, $x^5-4x^4+2x^3+x^2-3x+1$ --- the phenomenon reaches degree $5$ one
box out (it lies outside $[-3,3]^5$, so Theorem~\ref{thm:box}'s census
remains complete); it is one-pair, its typing closed by
Theorem~\ref{thm:pisot1pair}. Scans: $1545/1545$ Rat $=\{\Phi_1^5\}$;
$1063/1063$ live: detector $=2$ everywhere, composed squares exactly
$\{\Phi_1^{20}\}$; \emph{nine} instances have reducible $\Rat_p^{\circ}$
(shape $10{+}10$, both factors carrying unimodular roots, $S^{*}$ still
degree $20$) --- P7 witnesses now exist at degree $5$. Aggregates: P3
observed on $2661/2661$ certified Pisots across degrees $2$--$7$ and five
boxes; P1's zero-falsifier base is now $2016$ live instances. \F\ per
instance; \C\ over the ranges; nothing promoted.

\section{Next steps and predictions}\label{sec:next}"""))

E.append(("X3a", r"""Status: \F\ for at most one non-real pair (Theorem~\ref{thm:pisot1pair});
\C-empty on the first $67$ live instances (Theorem~\ref{thm:box}), on all
$313$ two-pair instances of $[-3,3]^5$, and on all $573$ live instances of
the degree-$6$/$7$ boxes including the first $309$ three-pair instances
(\S\ref{sec:boxext}, \S\ref{sec:n4});""",
r"""Status: \F\ for at most one non-real pair (Theorem~\ref{thm:pisot1pair});
\C-empty on all $2016$ live instances on record --- $67$ ($[-2,2]^5$),
$313$ ($[-3,3]^5$), $1063$ ($[-4,4]^5$), and the $573$ live instances of
the degree-$6$/$7$ boxes including the first $309$ three-pair instances
(\S\ref{sec:boxext}, \S\ref{sec:n4}, \S\ref{sec:pseries});"""))

E.append(("X3b", r"""$[-3,3]^5$. & \C\ (resolved: $0/313$, \S\ref{sec:boxext}) & a single hit in
any further extension\\""",
r"""$[-3,3]^5$. & \C\ (resolved: $0/313$; next box $0/1063$ in $[-4,4]^5$,
\S\ref{sec:pseries}) & a single hit in any further extension\\"""))

E.append(("X3c", r"""P3 & Every certified Pisot's $\Rat$ scan returns exactly $\{\Phi_1^{\deg p}\}$
in any box extension. & \F\ (Thm.~\ref{thm:pin}) & --- (a deviation would
falsify the pinning theorem)\\""",
r"""P3 & Every certified Pisot's $\Rat$ scan returns exactly $\{\Phi_1^{\deg p}\}$
in any box extension. & \F\ (Thm.~\ref{thm:pin}; observed $2661/2661$,
degrees $2$--$7$, \S\ref{sec:pseries}) & --- (a deviation would
falsify the pinning theorem)\\"""))

E.append(("X3d", r"""P4 & Every totally-real Pisot number satisfies $\theta\ge\varphi$, equality
only at $\theta=\varphi$ (degree $2$). & emission-gap--implied; standalone
\Op & a totally-real Pisot with $\theta<\varphi$ (would falsify the gap on
admissible objects)\\""",
r"""P4 & Every totally-real Pisot number satisfies $\theta\ge\varphi$, equality
only at $\theta=\varphi$ (degree $2$). & emission-gap--implied; standalone
\Op\ ($12/12$ certified exactly, equality once, \S\ref{sec:pseries}) & a
totally-real Pisot with $\theta<\varphi$ (would falsify the gap on
admissible objects)\\"""))

E.append(("X3e", r"""exist for non-generic Galois groups. & \C\ (resolved: $3$ instances in
$[-2,2]^6$, shapes $12{+}18$, $12{+}18$, $6{+}24$; scans still inert,
\S\ref{sec:n4}) & ---\\""",
r"""exist for non-generic Galois groups. & \C\ (resolved: $3$ instances in
$[-2,2]^6$, shapes $12{+}18$, $12{+}18$, $6{+}24$; $9$ more at degree $5$
in $[-4,4]^5$, shapes $10{+}10$; all inert, \S\ref{sec:n4},
\S\ref{sec:pseries}) & ---\\"""))

E.append(("X3f", r"""Remark~\ref{rem:detector}), and no merged shell occurred in any live
degree-$6$/$7$ instance (\S\ref{sec:n4}); existence elsewhere undetermined.
& \Op & (either outcome informative)\\""",
r"""Remark~\ref{rem:detector}), in $[-4,4]^5$ ($1063$ live instances,
\S\ref{sec:pseries}), or in any live degree-$6$/$7$ instance
(\S\ref{sec:n4}); existence elsewhere undetermined.
& \Op & (either outcome informative)\\"""))

E.append(("X4", r"""v1.2 additions (N4, Python 3.11.15 / \sy~1.14.0 / \gp~2.15.4): censuses
$42$\,s (degrees $5$--$7$, degree-$5$ regression gate included); scans
$415$\,s (degree $6$) $+$ 1794\,s (degree $7$, four shards); \gp\ spot
deck $4/4$.""",
r"""v1.2 additions (N4, Python 3.11.15 / \sy~1.14.0 / \gp~2.15.4): censuses
$42$\,s (degrees $5$--$7$, degree-$5$ regression gate included); scans
$415$\,s (degree $6$) $+$ 1794\,s (degree $7$, four shards); \gp\ spot
deck $4/4$. v1.3 additions (P-series): P4 sweep $1$\,s; $[-4,4]^5$ census
$23$\,s, $1063$ live scans $\approx$$11$\,min (four shards), one-pair Rat
batch $5$\,s; P3 aggregate (fresh degrees $2$--$4$) $8$\,s."""))


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
    dst = path.replace(".v12.tex", ".v13.tex")
    open(dst, "w", encoding="utf-8").write(out)
    print(f"wrote {dst}")


if __name__ == "__main__":
    main()
