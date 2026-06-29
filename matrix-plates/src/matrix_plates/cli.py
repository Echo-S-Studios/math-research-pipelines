"""Command-line interface for matrix_plates.

Subcommands
-----------
gen        build a single plate from a construction and print its invariants
batch      reproduce the tool's *Seed batch* and print a summary table
analyze    full spectral data + companion (rational-canonical) form for a matrix
spectrum   the Mahler spectrum (Goal 1); ``histogram`` is a synonym
extend     lift a plate through Φ and show its lineage / what it extends (Goal 2)
compare    compare two matrices: spectrum, Mahler, house, similarity
lift       (alias of the lift half of ``extend``)
demo       the φ ⊕ φ similarity-class demonstration
verify     run the build-spec verification checklist
export     write JSON / LaTeX / SymPy / HTML for a plate or the seed batch

A *target* (for analyze / compare / extend / export) is either a seed id
(``phi``, ``sq2``, … → its companion) or a matrix literal — JSON
(``"[[0,1],[1,1]]"``) or ``"a b; c d"`` rows.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import List, Tuple

from .canonical import is_similar, rational_canonical_form
from .closure import (Registry, lift, similarity_class_demo, similarity_classes,
                      spectrum_contains)
from .export import export_json, export_latex, export_sympy
from .histogram import (build_histogram, comparison_table, render_ascii,
                        render_svg, sorted_reflow)
from .operators import Built, build, build_companion, build_custom, build_kron
from .plates import Gallery, Plate, build_plate
from .render_html import gallery_html, spectrum_html
from .seeds import SEED_BY_ID
from .text import fmt_num, poly_str


# --- matrix parsing / target resolution ----------------------------------------
def _parse_matrix(s: str) -> List[List[int]]:
    s = s.strip()
    if s.startswith("["):
        return [[int(round(float(x))) for x in row] for row in json.loads(s)]
    rows = [r for r in s.replace("\n", ";").split(";") if r.strip()]
    return [[int(round(float(x))) for x in r.replace(",", " ").split()] for r in rows]


def _resolve_target(s: str) -> Built:
    """Resolve a CLI target to a :class:`Built`: a seed id or a matrix literal."""
    if s in SEED_BY_ID:
        return build_companion(s)
    try:
        return build_custom(_parse_matrix(s), name="A")
    except (ValueError, json.JSONDecodeError) as exc:
        seeds = ", ".join(sorted(SEED_BY_ID))
        raise SystemExit(
            f"could not read target {s!r}: not a known seed and not a valid matrix.\n"
            f"  seeds: {seeds}\n"
            f"  matrix: '[[0,1],[1,1]]' or '0 1; 1 1'\n  ({exc})")


# --- pretty printers ------------------------------------------------------------
def _matrix_lines(M: List[List[int]], indent: str = "    ") -> List[str]:
    if not M:
        return [indent + "[]"]
    cols = len(M[0])
    widths = [max(len(fmt_num(M[i][j])) for i in range(len(M))) for j in range(cols)]
    out = []
    for i, row in enumerate(M):
        cells = "  ".join(fmt_num(v).rjust(widths[j]) for j, v in enumerate(row))
        left = "⎡" if i == 0 else ("⎣" if i == len(M) - 1 else "⎢")
        right = "⎤" if i == 0 else ("⎦" if i == len(M) - 1 else "⎥")
        out.append(f"{indent}{left} {cells} {right}")
    return out


def _print_plate(p: Plate, show_companion: bool = False) -> None:
    a = p.analysis
    print(f"\n{p.name}    [{p.prov}]")
    for ln in _matrix_lines(p.M):
        print(ln)
    flags = []
    if a.integer:
        flags.append("integer")
    if a.unimodular:
        flags.append("unimodular")
    if a.derogatory:
        flags.append("derogatory")
    if a.defective:
        flags.append("defective")
    if a.at_floor:
        flags.append("cyclotomic floor (M=1)")
    chip = (f"  {a.n}×{a.n} · det {fmt_num(a.det)} · tr {fmt_num(a.tr)} · "
            f"house {round(a.house, 3)} · M {round(a.mahler, 3)} · "
            f"‖·‖F {round(a.frob, 2)} · rank {a.rank}")
    if flags:
        chip += "   [" + ", ".join(flags) + "]"
    print(chip)
    print(f"  char-poly         : {poly_str(a.coeffs)}   (deg {a.deg_char})")
    tag = "  ← derogatory: NOT similar to its companion" if a.derogatory \
          else "  (= char-poly; non-derogatory)"
    print(f"  min-poly          : {poly_str(a.minpoly)}   (deg {a.deg_min}){tag}")
    facs = "  ·  ".join(poly_str(f) for f in a.invariant_factors)
    print(f"  invariant factors : {facs}   ({a.num_invariant_factors} factor"
          f"{'s' if a.num_invariant_factors != 1 else ''})")
    print(f"  spectrum          : {a.outside} outside · {a.on} on · {a.inside} "
          f"inside the unit circle")
    if show_companion:
        rcf = rational_canonical_form(p.M)
        same = (rcf == p.M)
        print("  rational canonical form" + ("  (= A; A is already in RCF)" if same else ":"))
        if not same:
            for ln in _matrix_lines(rcf, indent="      "):
                print(ln)
    if p.note:
        print(f"  note              : {p.note}")


def _summary_row(p: Plate) -> str:
    a = p.analysis
    d = "Y" if a.derogatory else "·"
    u = "Y" if a.unimodular else "·"
    return (f"  {p.name:<14} {a.n:>2}×{a.n:<2} det {fmt_num(a.det):>6} "
            f"tr {fmt_num(a.tr):>4} house {round(a.house, 3):>8} M {round(a.mahler, 3):>11} "
            f"min/char {a.deg_min}/{a.deg_char}  derog {d}  uni {u}  [{p.family[:4]}]")


def _build_from_args(ns: argparse.Namespace) -> Built:
    try:
        return build(ns.op, a=ns.seed_a, b=ns.seed_b, ctype=ns.type, word=ns.word,
                     n=ns.n, seed=ns.rng)
    except ValueError as exc:
        raise SystemExit(f"cannot build: {exc}")


# --- subcommand handlers --------------------------------------------------------
def cmd_gen(ns: argparse.Namespace) -> int:
    _print_plate(build_plate(_build_from_args(ns), 1))
    return 0


def cmd_batch(ns: argparse.Namespace) -> int:
    g = Gallery.seed_batch()
    print(f"Seed batch — {len(g)} plates\n")
    for p in g:
        print(_summary_row(p))
    classes = similarity_classes(g.plates)
    print(f"\n{len(classes)} distinct similarity classes among {len(g)} plates")
    return 0


def cmd_analyze(ns: argparse.Namespace) -> int:
    _print_plate(build_plate(_resolve_target(ns.target), 1), show_companion=True)
    return 0


def cmd_histogram(ns: argparse.Namespace) -> int:
    g = Gallery.seed_batch()
    plates = g.plates
    if ns.mode == "reflow":
        print("Sorted reflow (ascending M):\n")
        for p in sorted_reflow(plates):
            print(f"  {round(p.mahler, 3):>11}   {p.name}  [{p.family}]")
        print("\n" + comparison_table())
    else:
        hist = build_histogram(plates, max_log_m=g.max_log_m)
        print(render_ascii(hist))
        if ns.svg:
            open(ns.svg, "w", encoding="utf-8").write(render_svg(hist))
            print(f"\nwrote SVG -> {ns.svg}")
        if ns.html:
            open(ns.html, "w", encoding="utf-8").write(spectrum_html(hist))
            print(f"wrote HTML -> {ns.html}")
    return 0


def cmd_extend(ns: argparse.Namespace) -> int:
    built = _resolve_target(ns.target)
    g = Gallery()
    parent = g.add(built)
    reg = Registry()
    res = lift(parent, reg, gallery=g)
    print("PARENT")
    _print_plate(parent)
    print("\nLIFT  Φ = companion ∘ charpoly")
    _print_plate(res.child)
    print("\nVERDICT")
    print(f"  spectrum preserved : {res.spectrum_preserved}")
    print(f"  idempotent         : {res.idempotent}")
    print(f"  similar to parent  : {res.similar}")
    print(f"  seed               : {res.seed.glyph}  ({'reused' if res.reused else 'new'})")
    print(f"  lineage            : {' → '.join(p.name for p in g.lineage(res.child))}")
    print(f"  {res.note}")
    if getattr(ns, "in_batch", False) and ns.target in SEED_BY_ID:
        batch = Gallery.seed_batch().plates
        ext = [p.name for p in batch if spectrum_contains(p, SEED_BY_ID[ns.target])]
        print(f"\nIn the seed batch, plates whose spectrum contains {ns.target}: "
              f"{', '.join(ext) or '(none)'}")
    return 0


def cmd_compare(ns: argparse.Namespace) -> int:
    pa = build_plate(_resolve_target(ns.a), 1)
    pb = build_plate(_resolve_target(ns.b), 2)
    aa, ab = pa.analysis, pb.analysis
    print(f"A: {pa.name}    B: {pb.name}\n")
    rows: List[Tuple[str, str, str]] = [
        ("size", f"{aa.n}×{aa.n}", f"{ab.n}×{ab.n}"),
        ("det", fmt_num(aa.det), fmt_num(ab.det)),
        ("trace", fmt_num(aa.tr), fmt_num(ab.tr)),
        ("house ⌈·⌉", str(round(aa.house, 4)), str(round(ab.house, 4))),
        ("Mahler M", str(round(aa.mahler, 4)), str(round(ab.mahler, 4))),
        ("char-poly", poly_str(aa.coeffs), poly_str(ab.coeffs)),
        ("min-poly", poly_str(aa.minpoly), poly_str(ab.minpoly)),
        ("# inv. factors", str(aa.num_invariant_factors), str(ab.num_invariant_factors)),
    ]
    w = max(len(r[1]) for r in rows + [("", "A", "")])
    w2 = max(len(r[2]) for r in rows + [("", "", "B")])
    print(f"  {'':18}{'A':>{w}}   {'B':>{w2}}")
    for label, va, vb in rows:
        print(f"  {label:18}{va:>{w}}   {vb:>{w2}}")
    same_spectrum = aa.coeffs == ab.coeffs
    similar = (aa.n == ab.n) and is_similar(pa.M, pb.M)
    print(f"\n  same spectrum (char-poly) : {same_spectrum}")
    print(f"  same Mahler measure       : {abs(aa.mahler - ab.mahler) < 1e-9}")
    print(f"  same house                : {abs(aa.house - ab.house) < 1e-9}")
    print(f"  SIMILAR (rational canon.) : {similar}", end="")
    if same_spectrum and not similar:
        print("   ← equal char-poly but NOT similar (different invariant factors)")
    else:
        print()
    return 0


def cmd_lift(ns: argparse.Namespace) -> int:
    ns.in_batch = False
    return cmd_extend(ns)


def cmd_demo(ns: argparse.Namespace) -> int:
    d = similarity_class_demo()
    print("Similarity-class demonstration:  φ ⊕ φ   vs   companion(charpoly(φ ⊕ φ))\n")
    print("PARENT  φ ⊕ φ   (block-diagonal, derogatory)")
    _print_plate(d.parent)
    print("\nCHILD   companion of (x²−x−1)²   (companion form, non-derogatory)")
    _print_plate(d.child)
    print("\nINVARIANTS")
    print(f"  same characteristic polynomial : {d.same_char_poly}")
    print(f"  same det / trace / Mahler      : {d.same_det and d.same_trace and d.same_mahler}"
          f"   (M = φ² ≈ {round(d.parent.mahler, 6)})")
    print(f"  same minimal polynomial        : {d.same_min_poly}   "
          f"(deg {d.parent.analysis.deg_min} vs {d.child.analysis.deg_min})")
    print(f"  same invariant factors         : {d.same_invariant_factors}   "
          f"([x²−x−1, x²−x−1] vs [(x²−x−1)²])")
    print(f"  => SIMILAR                      : {d.similar}")
    print("\nEqual characteristic polynomial ⇏ similar. The minimal polynomial / "
          "invariant\nfactors separate the classes.")
    return 0


def cmd_export(ns: argparse.Namespace) -> int:
    if ns.target:
        plates = [build_plate(_resolve_target(ns.target), 1)]
    else:
        plates = Gallery.seed_batch().plates
    if ns.format == "html":
        mx = max((p.log_mahler for p in plates), default=None)
        text = gallery_html(plates, max_log_m=mx)
    elif ns.format == "json":
        text = export_json(plates if len(plates) != 1 else plates[0])
    elif ns.format == "latex":
        text = "\n\n".join(export_latex(p) for p in plates)
    else:  # sympy
        text = "\n\n".join(export_sympy(p) for p in plates)
    if ns.out:
        open(ns.out, "w", encoding="utf-8").write(text)
        print(f"wrote {ns.format} -> {ns.out}  ({len(plates)} plate"
              f"{'s' if len(plates) != 1 else ''})")
    else:
        print(text)
    return 0


# --- verification checklist -----------------------------------------------------
def _checks() -> List[Tuple[str, bool, str]]:
    out: List[Tuple[str, bool, str]] = []
    reg = Registry()
    g = Gallery.seed_batch()
    hist = build_histogram(g.plates, max_log_m=g.max_log_m)
    out.append(("G1 floor pinned at M=1 (lo_logm == 0)", hist.lo_logm == 0.0,
                f"lo_logm={hist.lo_logm}"))
    band = hist.lehmer_band_occupants()
    out.append(("G1 (1, Lehmer) band empty for stock seeds", not band,
                f"min M = {round(min(p.mahler for p in g.plates), 4)} > L"))
    g2 = Gallery()
    cphi = g2.add(build_companion("phi"))
    r1 = lift(cphi, Registry(), gallery=g2)
    out.append(("G2 C(φ) lift is a fixed point (identical matrix)",
                r1.idempotent and r1.child.M == [[0, 1], [1, 1]],
                f"child={r1.child.M}"))
    d = similarity_class_demo()
    ok = (d.same_char_poly and d.same_det and d.same_trace and d.same_mahler
          and (not d.same_min_poly) and (not d.same_invariant_factors) and (not d.similar))
    out.append(("G2 φ⊕φ: equal char-poly but NOT similar (invariant factors differ)", ok,
                f"min deg {d.parent.analysis.deg_min} vs {d.child.analysis.deg_min}"))
    p1 = build_plate(build_custom([[7]]), 1)
    r_deg1 = lift(p1, Registry())
    out.append(("G2 degree-1 fixed point [[7]] → x−7 → [[7]]",
                r_deg1.child.M == [[7]], f"child={r_deg1.child.M}"))
    g3 = Gallery()
    base = g3.add(build("dsum", a="phi", b="phi"))
    first = lift(base, reg, gallery=g3)
    second = lift(first.child, reg, gallery=g3)
    out.append(("G2 mint a new seed, then Φ∘Φ reuses it",
                (not first.reused) and second.reused, f"seed={second.seed.glyph}"))
    try:
        ok_kron = len(build_kron(first.seed.id, "sq2", reg.by_id).M) == 8
    except Exception:  # noqa: BLE001
        ok_kron = False
    out.append(("G2 generated seed usable in ⊗ (p̂ ⊗ √2 = 8×8)", ok_kron, ""))
    gc = Gallery()
    par = gc.add(build("dsum", a="phi", b="phi"))
    lr = lift(par, Registry(), gallery=gc)
    histc = build_histogram(gc.plates, max_log_m=gc.max_log_m)
    out.append(("Compose: lifted companion shares parent's Mahler bin",
                histc.bin_of(par) == histc.bin_of(lr.child),
                f"bin {histc.bin_of(par)} == {histc.bin_of(lr.child)}"))
    out.append(("Invariants: φ⊕φ has 2 invariant factors (derogatory)",
                par.analysis.num_invariant_factors == 2, ""))
    cyc = build_plate(build_custom([[0, -1], [1, 0]]), 1)   # companion of x²+1
    out.append(("House: cyclotomic plate has house 1 and M=1 (Kronecker floor)",
                abs(cyc.house - 1.0) < 1e-9 and cyc.analysis.at_floor, ""))
    return out


def cmd_verify(ns: argparse.Namespace) -> int:
    checks = _checks()
    print("Build-spec verification\n")
    n_pass = sum(int(ok) for _, ok, _ in checks)
    for name, ok, detail in checks:
        extra = f"   ({detail})" if detail else ""
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}{extra}")
    print(f"\n{n_pass}/{len(checks)} checks passed")
    return 0 if n_pass == len(checks) else 1


# --- argument parsing -----------------------------------------------------------
def _add_build_args(sp: argparse.ArgumentParser) -> None:
    sp.add_argument("op", choices=["companion", "kron", "dsum", "comm", "cartan",
                                   "circ", "ring", "rand"], help="construction")
    sp.add_argument("--seed-a", default="phi", help="Seed A id (default: phi)")
    sp.add_argument("--seed-b", default="sq2", help="Seed B id (default: sq2)")
    sp.add_argument("--type", default="A", choices=["A", "D", "E8"], help="Cartan diagram")
    sp.add_argument("--word", default="fib", choices=["fib", "lucas"], help="circulant row")
    sp.add_argument("-n", type=int, default=5, help="size/rank/order (default: 5)")
    sp.add_argument("--rng", type=int, default=42, help="RNG seed (default: 42)")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="matrix-plates", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("gen", help="build & print one plate")
    _add_build_args(g)
    g.set_defaults(fn=cmd_gen)

    b = sub.add_parser("batch", help="reproduce the seed batch (summary table)")
    b.set_defaults(fn=cmd_batch)

    an = sub.add_parser("analyze", help="full spectral data + companion form for a matrix")
    an.add_argument("target", help="seed id (e.g. phi) or matrix literal")
    an.set_defaults(fn=cmd_analyze)

    for name in ("spectrum", "histogram"):
        h = sub.add_parser(name, help="Mahler spectrum (Goal 1)")
        h.add_argument("--mode", choices=["spectrum", "reflow"], default="spectrum")
        h.add_argument("--svg", help="write SVG to this path")
        h.add_argument("--html", help="write spectrum HTML to this path")
        h.set_defaults(fn=cmd_histogram)

    ex = sub.add_parser("extend", help="lift a plate through Φ; show lineage (Goal 2)")
    ex.add_argument("target", help="seed id or matrix literal")
    ex.add_argument("--in-batch", action="store_true",
                    help="also list seed-batch plates whose spectrum contains the seed")
    ex.set_defaults(fn=cmd_extend)

    cp = sub.add_parser("compare", help="compare two matrices (spectrum/Mahler/house/similarity)")
    cp.add_argument("a", help="seed id or matrix literal")
    cp.add_argument("b", help="seed id or matrix literal")
    cp.set_defaults(fn=cmd_compare)

    l = sub.add_parser("lift", help="(alias) build a plate, lift it through Φ")
    l.add_argument("target", nargs="?", default="phi", help="seed id or matrix literal")
    l.set_defaults(fn=cmd_lift)

    d = sub.add_parser("demo", help="φ ⊕ φ similarity-class demonstration")
    d.set_defaults(fn=cmd_demo)

    v = sub.add_parser("verify", help="run the build-spec verification checklist")
    v.set_defaults(fn=cmd_verify)

    e = sub.add_parser("export", help="export a plate or the seed batch")
    e.add_argument("target", nargs="?", default=None,
                   help="seed id / matrix literal (default: seed batch)")
    e.add_argument("--format", choices=["json", "latex", "sympy", "html"], default="json")
    e.add_argument("--out", help="write to this path (default: stdout)")
    e.set_defaults(fn=cmd_export)
    return p


def main(argv: List[str] | None = None) -> int:
    ns = build_parser().parse_args(argv)
    return ns.fn(ns)


if __name__ == "__main__":
    sys.exit(main())
