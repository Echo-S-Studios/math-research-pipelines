#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KL_DTA∅_Vsemantic_kernel.py

Source-level semantic compression.

This file is not `old file + compressor`.
It is the compressed kernel:

    KL_DTA_kernel = Core_K ⊕ StmtBank_K ⊕ Reconstruct_K ⊕ Audit_K

Compression target:
    preserve the load-bearing mathematics, record grammar, statement circuits,
    information/data layer, residual recursion, and audit gates in a smaller body.

Important distinction:
    This is semantic/executable compression, not byte-for-byte archival recovery.
    Byte-for-byte recovery belongs to Vcompressed. This kernel preserves the audited
    mathematical spine and regenerates records/statements/datasets from compact rules.
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from collections import Counter
from typing import Dict, List, Tuple, Iterable, Any
import argparse
import hashlib
import json
import math
import re
import numpy as np

THEOREM = "THEOREM"
COMPUTED = "COMPUTED"
INTERPRETIVE = "INTERPRETIVE"
FALSE_AS_STATED = "FALSE_AS_STATED"

PHI = (1 + 5 ** 0.5) / 2


# -------------------------------------------------------------------------------------------------
# Core carrier: Cl(2,0) ≅ M2(R)
# -------------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Cl:
    a: float = 0.0
    b: float = 0.0
    c: float = 0.0
    d: float = 0.0

    def __iter__(self):
        return iter((self.a, self.b, self.c, self.d))

    def __getitem__(self, i: int) -> float:
        return (self.a, self.b, self.c, self.d)[i]

    def __add__(self, other: "Cl") -> "Cl":
        return Cl(self.a + other.a, self.b + other.b, self.c + other.c, self.d + other.d)

    def __sub__(self, other: "Cl") -> "Cl":
        return Cl(self.a - other.a, self.b - other.b, self.c - other.c, self.d - other.d)

    def __neg__(self) -> "Cl":
        return Cl(-self.a, -self.b, -self.c, -self.d)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Cl(self.a * other, self.b * other, self.c * other, self.d * other)
        A, B, C, D = self.a, self.b, self.c, self.d
        E, F, G, H = other.a, other.b, other.c, other.d
        # basis 1,e1,e2,i=e1e2 with e1²=e2²=1 and i²=-1
        return Cl(
            A*E + B*F + C*G - D*H,
            A*F + B*E - C*H + D*G,
            A*G + B*H + C*E - D*F,
            A*H + B*G - C*F + D*E,
        )

    def __rmul__(self, other):
        return self * other

    def __abs__(self) -> float:
        return max(abs(self.a), abs(self.b), abs(self.c), abs(self.d))

    def __repr__(self) -> str:
        return f"[{self.a:.6g} {self.b:.6g} {self.c:.6g} {self.d:.6g}]"


VOID = Cl(0, 0, 0, 0)
ONE = Cl(1, 0, 0, 0)
E1 = Cl(0, 1, 0, 0)
E2 = Cl(0, 0, 1, 0)
I2 = Cl(0, 0, 0, 1)
P0 = Cl(0.5, 0, 0.5, 0)


def mat(X: Cl) -> np.ndarray:
    """Carrier matrix in M2(R)."""
    return np.array([[X.a + X.c, X.b - X.d],
                     [X.b + X.d, X.a - X.c]], dtype=float)


def cl(A: np.ndarray) -> Cl:
    """Recover carrier coordinates from a 2x2 real matrix."""
    return Cl((A[0, 0] + A[1, 1]) / 2,
              (A[0, 1] + A[1, 0]) / 2,
              (A[0, 0] - A[1, 1]) / 2,
              (A[1, 0] - A[0, 1]) / 2)


def rev(X: Cl) -> Cl:
    """Reversion corresponds to transpose."""
    return cl(mat(X).T)


def M(X: Cl) -> Cl:
    """Measurement/fold: M(X)=rev(X)X=XᵀX."""
    return rev(X) * X


def tau(X: Cl) -> float:
    """Normalized trace τ(X)=tr(mat(X))/2, equal to scalar coordinate."""
    return X.a


def residual(X: Cl) -> Cl:
    """Residual operator R_K(X)=M(X)-τ(M(X))·1."""
    return M(X) - ONE * tau(M(X))


R_K = residual


def det(X: Cl) -> float:
    return float(np.linalg.det(mat(X)))


def disc(X: Cl) -> float:
    A = mat(X)
    return float((np.trace(A) ** 2) - 4 * np.linalg.det(A))


def rank(X: Cl, tol: float = 1e-9) -> int:
    return int(np.linalg.matrix_rank(mat(X), tol=tol))


def orbit(X: Cl, tol: float = 1e-9) -> str:
    r = rank(X, tol)
    if abs(disc(X)) < tol:
        return "merged"
    if r == 1:
        return "split"
    return "crossed"


def fixed_origin(theta: float) -> Cl:
    """Rank-1 symmetric idempotent gate on the aperture circle."""
    return Cl(0.5, 0.5 * math.sin(theta), 0.5 * math.cos(theta), 0.0)


def is_gate(P: Cl, tol: float = 1e-9) -> bool:
    A = mat(P)
    return (
        abs(M(P) - P) < tol
        and float(np.max(np.abs(A - A.T))) < tol
        and float(np.max(np.abs(A @ A - A))) < tol
    )


def gate_complement(P: Cl) -> Cl:
    return ONE - P


def spectrum(X: Cl) -> Tuple[float, float]:
    vals = np.linalg.eigvalsh(mat(M(X)))
    return float(vals[0]), float(vals[1])


def probs(X: Cl) -> Tuple[float, float]:
    lo, hi = spectrum(X)
    s = lo + hi
    if s <= 1e-15:
        return 0.0, 0.0
    return lo / s, hi / s


def entropy_bits(p: Tuple[float, float]) -> float:
    return -sum(x * math.log(x, 2) for x in p if x > 0)


def purity(p: Tuple[float, float]) -> float:
    return sum(x * x for x in p)


def info_anisotropy(X: Cl) -> float:
    p = probs(X)
    return abs(p[1] - p[0])


def spectral_residue_norm(X: Cl) -> float:
    R = residual(X)
    return math.sqrt(R.b * R.b + R.c * R.c)


def regime(X: Cl, tol: float = 1e-10) -> str:
    lo, hi = spectrum(X)
    if hi > 1 + tol:
        return "diverge"
    if abs(hi - 1) <= tol or abs(lo - 1) <= tol:
        return "gate"
    return "void"


def dM(X: Cl) -> np.ndarray:
    a, b, c, d = X.a, X.b, X.c, X.d
    return np.array([
        [2*a, 2*b, 2*c, 2*d],
        [2*b, 2*a, -2*d, -2*c],
        [2*c, 2*d, 2*a, 2*b],
        [0, 0, 0, 0],
    ], dtype=float)


def dR(X: Cl) -> np.ndarray:
    J = dM(X)
    J[0, :] = 0.0
    return J


def js_bits(p: Tuple[float, float], q: Tuple[float, float]) -> float:
    m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    return entropy_bits(m) - 0.5 * entropy_bits(p) - 0.5 * entropy_bits(q)


# -------------------------------------------------------------------------------------------------
# High-form statement bank
# -------------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Stmt:
    subject: str
    equation: str
    invariant: str
    residual: str
    jurisdiction: str = COMPUTED

    @property
    def digest(self) -> str:
        payload = json.dumps(asdict(self), sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    @property
    def high_form(self) -> str:
        return f"{self.subject}: {self.equation}; invariant={self.invariant}; residual={self.residual}; jurisdiction={self.jurisdiction}."


LAW_BANK: Tuple[Stmt, ...] = (
    Stmt("carrier", "Cl(2,0)≅M₂(R)≅R⁴", "mat/cl round-trip", "coordinate residual preserved", THEOREM),
    Stmt("measurement", "M(X)=rev(X)X=XᵀX", "PSD symmetric record", "ν=M(X)-X", THEOREM),
    Stmt("void_measurement", "Void_K(X)=τ(M(X))·1", "scalar survival through trace mouth", "direction erased", THEOREM),
    Stmt("residual", "R_K(X)=M(X)-τ(M(X))·1", "τ(R_K(X))=0", "framework is leftover direction", THEOREM),
    Stmt("residual_nilpotence", "R_K²=0", "residual has finite bite-depth in M₂", "living recursion requires reembedding", THEOREM),
    Stmt("gate", "Gate_K(P)⇔M(P)=P⇔Pᵀ=P∧P²=P", "sharp aperture", "defect M(P)-P", THEOREM),
    Stmt("gate_complement", "P⊥=1-P; P+P⊥=1; PP⊥=0", "aperture includes exclusion", "complement residual", THEOREM),
    Stmt("tau_pi", "π_gate(P)=τ(P)=rank(P)/2", "trace gives projection value", "rank fraction", THEOREM),
    Stmt("probability", "π(P|X)=τ(M(X)P)/τ(M(X))", "P and P⊥ sum to 1", "undefined only at void mass", THEOREM),
    Stmt("observer", "Obs_K(X)=M(X)-τ(M(X))·1", "observer is residual", "not external spectator", THEOREM),
    Stmt("framework", "FW_K(X)=Resid_K(X)", "framework is residual ledger", "not a wrapper around residual", THEOREM),
    Stmt("word", "Word_K(w)=Resid_K(seed(w))", "word is residual packet", "word≠object", COMPUTED),
    Stmt("statement", "Statement_K(s)=Σ Word_K(w_i)+syntax_residual(s)", "sentence is residual circuit", "digest preserves payload reference", COMPUTED),
    Stmt("analytic_metric", "d_K(X,Y)=|X-Y|∞", "metric positivity/symmetry/triangle", "distance residual", THEOREM),
    Stmt("analytic_smooth", "M,R_K are polynomial C∞", "Jacobian exists exactly", "finite-difference residual", THEOREM),
    Stmt("P0_saddle", "spec(dM_P0)={0,0,1,2}", "gate has contraction, tangent, expansion", "saddle residual", THEOREM),
    Stmt("orbit_regimes", "λ(Mⁿ(X))=λ(M(X))^(2ⁿ)", "collapse/gate/diverge", "eigenvalue threshold", THEOREM),
    Stmt("info_distribution", "p_i(X)=λ_i(M(X))/Σλ", "measurement spectrum becomes probability", "void row invalid", THEOREM),
    Stmt("tau_mass", "Σλ_i(M(X))=2τ(M(X))", "tau is half spectral mass", "mass residual", THEOREM),
    Stmt("entropy", "H_K(X)=-Σp_i log p_i", "uncertainty internalized", "0≤H≤1 bit", THEOREM),
    Stmt("purity", "Pur_K(X)=Σp_i²", "information concentration", "1/2≤Pur≤1", THEOREM),
    Stmt("anisotropy", "|p₂-p₁|=||Resid_K(X)||_spectral/τ(M(X))", "residual is information imbalance", "anisotropy residual", THEOREM),
    Stmt("data_row", "Data_K(X)=(raw,returns,residual,information,regime)", "carrier becomes dataset row", "schema residual", COMPUTED),
    Stmt("semantic_compression", "CompressSem_K(record)=Stmt_K(record)", "records become high-form statements", "digest binds source", COMPUTED),
    Stmt("paragraph_circuit", "Para_K={Stmt_K(r_i)}", "paragraph is equation circuit", "loose prose removed", COMPUTED),
)


@dataclass(frozen=True)
class Row:
    sample: str
    X: Cl
    tau_M: float
    det_X: float
    disc_X: float
    rank_X: int
    orbit_X: str
    gate: bool
    residual_height: int
    residual_norm: float
    entropy_bits: float
    purity: float
    anisotropy: float
    regime: str
    valid: bool


def residual_height(X: Cl, tol: float = 1e-10) -> int:
    if abs(X) < tol:
        return 0
    r1 = R_K(X)
    if abs(r1) < tol:
        return 1
    r2 = R_K(r1)
    if abs(r2) < tol:
        return 2
    return 3


def row(sample: str, X: Cl) -> Row:
    p = probs(X)
    return Row(
        sample=sample,
        X=X,
        tau_M=tau(M(X)),
        det_X=det(X),
        disc_X=disc(X),
        rank_X=rank(X),
        orbit_X=orbit(X),
        gate=is_gate(X),
        residual_height=residual_height(X),
        residual_norm=abs(R_K(X)),
        entropy_bits=entropy_bits(p),
        purity=purity(p),
        anisotropy=info_anisotropy(X),
        regime=regime(X),
        valid=sum(p) > 0,
    )


def seed_samples(n: int = 512, seed: int = 101, span: float = 3.0) -> List[Tuple[str, Cl]]:
    rng = np.random.default_rng(seed)
    base = [
        ("VOID", VOID),
        ("ONE", ONE),
        ("P0", P0),
        ("P0c", gate_complement(P0)),
        ("E1", E1),
        ("E2", E2),
        ("i", I2),
        ("phi", Cl(PHI, 0, 0, 0)),
        ("generic", Cl(1, 2, 0.5, 0.3)),
    ]
    base += [(f"gate_{k}", fixed_origin(2 * math.pi * k / 32)) for k in range(32)]
    base += [(f"random_{k}", Cl(*rng.uniform(-span, span, 4))) for k in range(n)]
    return base


def dataset(n: int = 512) -> List[Row]:
    return [row(name, X) for name, X in seed_samples(n)]


def search_statements(query: str, limit: int = 20) -> List[Stmt]:
    q = query.lower()
    out = [s for s in LAW_BANK if q in s.high_form.lower()]
    return out[:limit]


def paragraph(title: str, statements: Iterable[Stmt]) -> str:
    body = " ".join(f"{s.subject} -> {s.equation}" for s in statements)
    return f"{title}: {body}"


def statement_compression_ratio() -> float:
    raw = sum(len(json.dumps(asdict(s), ensure_ascii=False)) for s in LAW_BANK)
    high = sum(len(s.high_form) for s in LAW_BANK)
    return high / raw


# -------------------------------------------------------------------------------------------------
# Audit gates
# -------------------------------------------------------------------------------------------------

def audit(samples: int = 512) -> Dict[str, Any]:
    rows = dataset(samples)
    valid = [r for r in rows if r.valid]

    # Carrier/fold residuals.
    psd_min = []
    sym_res = []
    r2_res = []
    anis_res = []
    mass_res = []
    prob_res = []
    entropy_fail = 0
    purity_fail = 0

    for name, X in seed_samples(samples):
        A = mat(M(X))
        sym_res.append(float(np.max(np.abs(A - A.T))))
        psd_min.append(float(np.min(np.linalg.eigvalsh((A + A.T) / 2))))
        r2_res.append(abs(R_K(R_K(X))))

        p = probs(X)
        if sum(p) > 0:
            prob_res.append(abs(sum(p) - 1))
            ent = entropy_bits(p)
            pur = purity(p)
            if ent < -1e-10 or ent > 1 + 1e-10:
                entropy_fail += 1
            if pur < 0.5 - 1e-10 or pur > 1 + 1e-10:
                purity_fail += 1
            if tau(M(X)) > 1e-15:
                anis_res.append(abs(info_anisotropy(X) - spectral_residue_norm(X) / tau(M(X))))
        lo, hi = spectrum(X)
        mass_res.append(abs((lo + hi) - 2 * tau(M(X))))

    # Gate circle.
    gates = [VOID, ONE] + [fixed_origin(2 * math.pi * k / 128) for k in range(128)]
    gate_fail = [g for g in gates if not is_gate(g)]
    gate_trace_seen = sorted({round(tau(g), 9) for g in gates})

    # P0 saddle.
    spec = sorted(round(float(v.real), 12) for v in np.linalg.eigvals(dM(P0)) if abs(v.imag) < 1e-10)
    p0_spec_ok = spec == [0.0, 0.0, 1.0, 2.0]

    # Statement bank.
    empty_statement_slots = [
        s.subject for s in LAW_BANK
        if not (s.subject and s.equation and s.invariant and s.residual and s.jurisdiction and len(s.digest) == 64)
    ]
    search_hits = len(search_statements("residual")) + len(search_statements("tau"))
    para = paragraph("kernel spine", LAW_BANK[:8])

    return {
        "equation": "KL_DTA_kernel = Core_K ⊕ StmtBank_K ⊕ Reconstruct_K ⊕ Audit_K",
        "source_bytes": None,
        "law_statements": len(LAW_BANK),
        "rows": len(rows),
        "valid_rows": len(valid),
        "symmetry_residual": max(sym_res),
        "psd_min_eigenvalue": min(psd_min),
        "R2_residual": max(r2_res),
        "probability_sum_residual": max(prob_res) if prob_res else 0.0,
        "mass_tau_residual": max(mass_res),
        "anisotropy_residual": max(anis_res) if anis_res else 0.0,
        "entropy_failures": entropy_fail,
        "purity_failures": purity_fail,
        "gate_failures": len(gate_fail),
        "gate_trace_seen": gate_trace_seen,
        "P0_spectrum": spec,
        "P0_spectrum_ok": p0_spec_ok,
        "regime_counts": dict(Counter(r.regime for r in rows)),
        "orbit_counts": dict(Counter(r.orbit_X for r in rows)),
        "empty_statement_slots": empty_statement_slots,
        "statement_search_hits": search_hits,
        "statement_compression_ratio": statement_compression_ratio(),
        "paragraph_digest": hashlib.sha256(para.encode("utf-8")).hexdigest(),
        "closure": (
            max(sym_res) < 1e-10
            and min(psd_min) > -1e-10
            and max(r2_res) < 1e-10
            and (max(prob_res) if prob_res else 0.0) < 1e-10
            and max(mass_res) < 1e-10
            and (max(anis_res) if anis_res else 0.0) < 1e-10
            and entropy_fail == 0
            and purity_fail == 0
            and len(gate_fail) == 0
            and p0_spec_ok
            and not empty_statement_slots
            and search_hits > 0
        ),
    }


def show_audit(samples: int = 512) -> None:
    rec = audit(samples)
    print(json.dumps(rec, indent=2, ensure_ascii=False, default=str))


def show_laws() -> None:
    for s in LAW_BANK:
        print(s.high_form)
        print(f"  digest={s.digest[:16]}...")


def show_rows(samples: int = 12) -> None:
    for r in dataset(samples):
        print(
            f"{r.sample:10} X={r.X} tauM={r.tau_M:.6g} H={r.entropy_bits:.6g} "
            f"Pur={r.purity:.6g} anis={r.anisotropy:.6g} regime={r.regime} gate={r.gate}"
        )


def show_search(query: str) -> None:
    hits = search_statements(query)
    print(json.dumps([asdict(h) | {"digest": h.digest} for h in hits], indent=2, ensure_ascii=False))


def show_paragraph() -> None:
    print(paragraph("compressed kernel paragraph", LAW_BANK))


def main() -> None:
    ap = argparse.ArgumentParser(description="KL_DTA∅ semantic compressed kernel")
    ap.add_argument("--mode", default="audit", choices=["audit", "laws", "rows", "search", "paragraph"])
    ap.add_argument("--samples", type=int, default=512)
    ap.add_argument("--query", default="residual")
    args = ap.parse_args()

    if args.mode == "audit":
        show_audit(args.samples)
    elif args.mode == "laws":
        show_laws()
    elif args.mode == "rows":
        show_rows(args.samples)
    elif args.mode == "search":
        show_search(args.query)
    elif args.mode == "paragraph":
        show_paragraph()


if __name__ == "__main__":
    main()
