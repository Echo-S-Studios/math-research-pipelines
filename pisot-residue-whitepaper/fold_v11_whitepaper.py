#!/usr/bin/env python3
"""fold_v11_whitepaper.py -- fold the executed N2/N3 box extensions, harness
note H4, and the verification session's pinned corrections into a v1.1 of the
pisot-residue whitepaper.

Edits (V-series, continuing the K-series idiom):
  V1  date line gains the v1.1 marker
  V2  abstract gains the one-sentence v1.1 addendum
  V3  H4 appended to the harness itemize (tagged [DECLARED], non-reproduction
      disclosed)
  V4  new section "Box extensions, executed" inserted before the next-steps
      section (N2 census + audit + scans, detector-semantics remark; N3 census
      + twist-exclusivity correction)
  V5  next-steps items N1/N2/N3/N5 marked executed
  V6  predictions table rows P2/P5/P6/P8 updated to observed status
  V7  conjecture status line extended to the 313-instance evidence base
  V8  appendix: v1.1 runtimes + bundle manifest pointer

Discipline: all-or-nothing. Every anchor must occur exactly once or nothing is
written. Output: <input>.v11.tex (the input file is never modified in place).

Usage:  python3 fold_v11_whitepaper.py path/to/pisot_residue_whitepaper.tex
"""
import sys

E = []

# ------------------------------------------------------------- V1: date line
E.append(("V1", r"""\date{July 2, 2026 \\ \small Session note; all computations exact, artifact manifest in Appendix~A.}""",
r"""\date{July 2, 2026; v1.1 addendum (box extensions executed) folded same day \\ \small Session note; all computations exact, artifact manifest in Appendix~A.}"""))

# -------------------------------------------------------------- V2: abstract
E.append(("V2", r"""Next steps are enumerated with falsifiable predictions, including the general
Pisot-inertness conjecture \Op\ in its multiplicative-torsion formulation.
\end{abstract}""",
r"""Next steps are enumerated with falsifiable predictions, including the general
Pisot-inertness conjecture \Op\ in its multiplicative-torsion formulation.
\emph{v1.1 addendum:} the box extensions N2--N3 are executed and independently
verified (\S\ref{sec:boxext}): $431$ Pisot quintics in $[-3,3]^5$ with all
$313$ two-pair instances inert (P2 resolved: $0$ mirrored classes), and $589$
Salem twist-classes in $\{-2,\dots,2\}^6$, all inert (P5, P6 confirmed); zero
falsifiers, nothing promoted.
\end{abstract}"""))

# ------------------------------------------------------------------- V3: H4
E.append(("V3", r"""\item[\textbf{H3.}] Positive pattern: the dual-path
$\mathrm{sig}(P)=\mathrm{scan}_{\mathrm{td}}(P)\overset{!}{=}\mathrm{scan}_{\mathrm{fp}}(P)$
assertion (trial division vs.\ factorization) as the in-engine standard for
\gp-side scans.
\end{itemize}""",
r"""\item[\textbf{H3.}] Positive pattern: the dual-path
$\mathrm{sig}(P)=\mathrm{scan}_{\mathrm{td}}(P)\overset{!}{=}\mathrm{scan}_{\mathrm{fp}}(P)$
assertion (trial division vs.\ factorization) as the in-engine standard for
\gp-side scans.
\item[\textbf{H4.}] \Dc\ Container-class observation, disclosed rather than
promoted: one execution container reaped backgrounded processes at call
teardown nondeterministically (the N3 driver survived only because its launch
call outlived it; the N2 driver was killed mid-import with an empty log); a
second container of the same family did \emph{not} reproduce it (five
harness-tracked background runs, up to $15$ minutes, all completed). Binding
pattern regardless: foreground execution with checkpointed, restart-safe
drivers.
\end{itemize}"""))

# --------------------------------------------- V4: executed box extensions
E.append(("V4", r"""\section{Next steps and predictions}\label{sec:next}""",
r"""\section{Box extensions, executed (v1.1 addendum)}\label{sec:boxext}

Both box extensions of \S\ref{sec:next} (N2, N3) were executed post-archive
and independently re-verified end-to-end (zero-shot verification session,
2026-07-02: manifest integrity, full regeneration of every pinned artifact ---
byte-identical, also under Python~3.11.15 --- and an adversarial referee pass
over every \F-tagged certificate). The corrections below are recorded per the
project discipline that load-bearing corrections are pinned rather than
papered over.

\subsection{N2: quintic box $[-3,3]^5$}
\textbf{Census.} $16807$ candidates; $14406$ with $e\neq0$; exact certificate
partition $862$ (interior count $4$ on every non-degenerate path)
$/\,10942$ (exact count $\neq4$) $/\,2602$ (all paths degenerate). The $862$
pass the Sturm and irreducibility gates down to $\mathbf{431}$ certified
Pisot quintics ($313$ two-pair, $118$ mixed, $0$ totally real); the
$[-2,2]^5$ restriction reproduces \S\ref{sec:quintic} exactly ($83/67/16$,
row-for-row). The $2602$ degenerate-chain candidates were adjudicated exactly
by two \emph{independent} methods (certified rational root enclosures;
scaled Schur--Cohn sandwich at rational radii straddling $1$), agreeing
instance-for-instance: $2594$ reducible, $8$ irreducible with interior count
in $\{2,3\}$, $0$ Pisot --- the census is complete. \C\ Disclosure: the
four-path certificate chain $\{\mathrm{SC},\mathrm{RH}\}$ on
$\{p(x),-p(-x)\}$ collapses to \emph{two} independent methods (both
transforms commute with $x\mapsto-x$; verified with $0$ exceptions and $0$
cross-path disagreements over all $14406$ candidates), so per-instance
certificates carry at most two independent computations. \F

\textbf{Decision.} $313/313$ complete $C_2$ scans returned exactly
$\{\Phi_1^{20}\}$, with $\Phi_2$-multiplicity $0$ and no higher cyclotomic
content anywhere; the $67$ instances shared with \S\ref{sec:quintic} agree
row-for-row with run~1. \F\ per instance; \C\ over the box. No same-shell
two-pair instance occurred (P8 extended to $[-3,3]^5$).

\begin{remark}[shell-detector semantics, corrected]\label{rem:detector}
Proposition~\ref{prop:shells} counts unimodular roots \emph{with
multiplicity} ($4$ vs.\ $12$). An implementation reading the trace-square
Sturm count on $(-2,2)$ counts \emph{distinct} values instead; in the merged
case the $12$ ratios provably collapse to at most $4$ distinct trace values
(the cross ratios pair off), so a merged branch keyed to the distinct count
$6$ is unreachable, and a torsion-merged configuration can present the
distinct-shell count silently. The merged case is nonetheless excluded on
every instance by the joint certificate actually asserted --- distinct-shell
count, $\Phi_2$-free, no higher cyclotomic content, no count anomaly ---
since any silent collapse forces torsion ratios that the $C_2$/torsion scan
exhibits. In the $[-2,2]^5$ run the verified squarefreeness of
$\Rat_p^{\circ}$ already equates the two counts. \F
\end{remark}

\subsection{N3: census family $\{-2,\dots,2\}^6$}
$15625$ vectors, $125$ twist-fixed, $\mathbf{7875}$ classes (P5, asserted
in-run). Cascade, with \Dc\ category labels (a three-way partition, not
claimed comparable to the archived cascade tallies): $6548$ straddle-fail
$/\,738$ straddle-pass-reducible $/\,\mathbf{589}$ Salem classes. The
$\{-1,0,1\}^6$ restriction reproduces the archived census exactly ($378$
classes, $37$ Salem, $37/37$ inert). All $589$ scans returned exactly
$\{\Phi_1^{12}\}$ with the $\Phi_2$-impossibility assertion holding per
instance: the corroboration base of the modulus-pinning theorem on Salem
classes grows $37\to589$ with zero falsifiers (P6). \F\ per instance; \C\
over the box. Correction, pinned: the twist-exclusivity shortcut (``the two
class members cannot both straddle'') fails at Sturm endpoints --- $160$
classes both straddle, each provably with $P(\pm1)=0$, hence reducible ---
so exclusivity holds in the weaker, sufficient form ``both straddle
$\Rightarrow$ both reducible.'' \F

\section{Next steps and predictions}\label{sec:next}"""))

# ------------------------------------------------- V5: next-steps markers
E.append(("V5a", r"""\item[\textbf{N1.}] Symmetrize $C_2$ coverage: full \sy-side scans of all $67$
composed squares ($\approx67\times10$\,s $\approx11$\,min).""",
r"""\item[\textbf{N1.}] Symmetrize $C_2$ coverage: full \sy-side scans of all $67$
composed squares ($\approx67\times10$\,s $\approx11$\,min). \emph{Executed:}
$67/67$ returned $\{\Phi_1^{20}\}$; instance~1 additionally re-derived by a
fully symbolic degree-$400$ resultant, identical to the Newton route."""))

E.append(("V5b", r"""\item[\textbf{N2.}] Quintic box extension to $[-3,3]^5$ ($16807$ candidates;
certification $\approx6\times$ stage-1 cost).""",
r"""\item[\textbf{N2.}] Quintic box extension to $[-3,3]^5$ ($16807$ candidates;
certification $\approx6\times$ stage-1 cost). \emph{Executed:}
\S\ref{sec:boxext}."""))

E.append(("V5c", r"""\item[\textbf{N3.}] Census family extension $c\in\{-2,\dots,2\}^6$: $15625$
vectors; twist-fixed $5^3=125$; Burnside gives \emph{exactly}
$(15625+125)/2=7875$ twist-classes (forced arithmetic); cascade tallies to be
computed.""",
r"""\item[\textbf{N3.}] Census family extension $c\in\{-2,\dots,2\}^6$: $15625$
vectors; twist-fixed $5^3=125$; Burnside gives \emph{exactly}
$(15625+125)/2=7875$ twist-classes (forced arithmetic); cascade tallies to be
computed. \emph{Executed:} \S\ref{sec:boxext}."""))

E.append(("V5d", r"""\item[\textbf{N5.}] Codify H1--H3 into the repository's cross-engine
verification standard beside the engine version pins.""",
r"""\item[\textbf{N5.}] Codify H1--H3 into the repository's cross-engine
verification standard beside the engine version pins. \emph{Partially
executed:} H1--H2 and the ledger-M live replication folded into the parent
deposit (v1.1, K-series); H4 recorded in \S\ref{sec:harness}."""))

# ----------------------------------------------------- V6: prediction rows
E.append(("V6a", r"""P2 & N2 yields $0$ mirrored classes among all two-pair instances in
$[-3,3]^5$. & \Op\ (P1-implied) & a single hit\\""",
r"""P2 & N2 yields $0$ mirrored classes among all two-pair instances in
$[-3,3]^5$. & \C\ (resolved: $0/313$, \S\ref{sec:boxext}) & a single hit in
any further extension\\"""))

E.append(("V6b", r"""P5 & N3 Burnside count is exactly $7875$ twist-classes. & \F\ (arithmetic) & ---\\""",
r"""P5 & N3 Burnside count is exactly $7875$ twist-classes. & \F\ (arithmetic;
observed $7875$) & ---\\"""))

E.append(("V6c", r"""P6 & Every Salem class found by N3 is inert with scan $\{\Phi_1^{12}\}$.
& \F\ (\cite[Cor.~7.14]{relcharge}) & ---\\""",
r"""P6 & Every Salem class found by N3 is inert with scan $\{\Phi_1^{12}\}$.
& \F\ (\cite[Cor.~7.14]{relcharge}; observed $589/589$) & ---\\"""))

E.append(("V6d", r"""P8 & Same-shell two-pair Pisot quintics (shell detector $=12$): none occurred
in $[-2,2]^5$; existence elsewhere undetermined. & \Op & (either outcome
informative)\\""",
r"""P8 & Same-shell two-pair Pisot quintics (shell detector $=12$): none occurred
in $[-2,2]^5$ or $[-3,3]^5$ (\S\ref{sec:boxext},
Remark~\ref{rem:detector}); existence elsewhere undetermined. & \Op & (either
outcome informative)\\"""))

# ------------------------------------------------ V7: conjecture status line
E.append(("V7", r"""Status: \F\ for at most one non-real pair (Theorem~\ref{thm:pisot1pair});
\C-empty on the first $67$ live instances (Theorem~\ref{thm:box});""",
r"""Status: \F\ for at most one non-real pair (Theorem~\ref{thm:pisot1pair});
\C-empty on the first $67$ live instances (Theorem~\ref{thm:box}) and on all
$313$ two-pair instances of $[-3,3]^5$ (\S\ref{sec:boxext});"""))

# ------------------------------------------------------- V8: appendix block
E.append(("V8a", r"""Engines: \sy~1.14.0 / Python 3.12.3; \gp~2.15.4 / GMP 6.3.0. Runtimes:
canonical corroboration $1.5$\,s; census $60$\,s; quartic sweep $4$\,s;
cross-engine run 2 $0.5$\,s; quintic certification $64$\,s; quintic decision
$69$\,s; ledger-M run 3 $1.8$\,s.""",
r"""Engines: \sy~1.14.0 / Python 3.12.3; \gp~2.15.4 / GMP 6.3.0. Runtimes:
canonical corroboration $1.5$\,s; census $60$\,s; quartic sweep $4$\,s;
cross-engine run 2 $0.5$\,s; quintic certification $64$\,s; quintic decision
$69$\,s; ledger-M run 3 $1.8$\,s. v1.1 additions (authoring / verification
rerun): N2 scans $154/207$\,s; N3 census-and-scans $33/46$\,s; every v1.1
artifact regenerates byte-identically under both Python~3.12.3 and 3.11.15."""))

E.append(("V8b", r"""pisot103.json & fb349dc136e149718726df2e729184681b33fd22abb68585e077df7b0dfe792d\\
\hline
\end{tabular}
\end{center}""",
r"""pisot103.json & fb349dc136e149718726df2e729184681b33fd22abb68585e077df7b0dfe792d\\
\hline
\end{tabular}
\end{center}

\begin{center}
\scriptsize\ttfamily
\begin{tabular}{ll}
\hline
v1.1 artifact & SHA-256\\
\hline
filesfixed.zip (box-extension bundle) & 8432455c20b07e9b6c2be5987484e8b720ceb27cefdaf7add6b34a28362ed3a1\\
\hline
\end{tabular}
\end{center}

{\sloppy
\noindent The bundle's top-level manifest pins its four component manifests
(\texttt{n1-symmetrize}, \texttt{n2-n3-box-extensions},
\texttt{n2-chain-audit}, \texttt{deposit-crossengine-fold}), the runbook, and
the fix-log README. Changed pin, disclosed there: \texttt{pisot83.jsonl}
re-pinned to the byte-exact output of its pinned generator
(\texttt{aeff3c3d\ldots}); mathematical fields unchanged, the dropped
\texttt{certs} column preserved verbatim in \texttt{pisot\_n2.jsonl}'s
$[-2,2]^5$ restriction.\par}"""))


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    path = sys.argv[1]
    src = open(path, encoding="utf-8").read()

    bad = [(eid, src.count(old)) for eid, old, _ in E if src.count(old) != 1]
    if bad:
        for eid, n in bad:
            print(f"ANCHOR-FAIL {eid}: found {n} occurrences (need exactly 1). "
                  f"Nothing written.")
        sys.exit(1)

    out = src
    for eid, old, new in E:
        out = out.replace(old, new, 1)
        print(f"{eid} applied.")

    dst = path[:-4] + ".v11.tex" if path.endswith(".tex") else path + ".v11"
    open(dst, "w", encoding="utf-8").write(out)
    print(f"wrote {dst}")


if __name__ == "__main__":
    main()
