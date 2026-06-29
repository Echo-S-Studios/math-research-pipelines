"""dispatch.py -- the KIRA-shell JSON-in/out surface for kira-language (mirrors L00M's vector_api).

One request JSON on stdin -> one result JSON on stdout, so a KIRA endpoint is exactly:

    py -m kira_language        with the request JSON on stdin

verifiable by LOCAL EQUIVALENCE: call dispatch(req) in-process and diff against that same subprocess
(test_language_api.py), exactly as vector_api/test_vector_api do.

THE SURFACE (PREP_PLAN section 4; survey taxonomy in [brackets]):
  QUERY    read [/exact] . laws . search . audit . bridge . lexicon
  GENERATE render (alias speak)            -- deterministic, fact-only template-NLG
  INGEST   observe . propose . commit      -- the acquisition+lexicon loop (propose-for-confirm)
  STORE    persist . restore               -- the sha256-chain JSON store

POSTURE
  * Stateless shell: the lexicon/accumulator travel IN the request ("lexicon": [records]) and persist
    via the store (mirroring vector_api's stateless + server-held-observable pattern). `commit` is the
    SOLE state-growing verb (propose-for-confirm): observe/propose never grow the dictionary.
  * EXACT where it matters: read[/exact], render, observe, propose, commit return exact Fraction-as-string
    readings/values. Plain `read` stays FLOAT (declared tolerance), byte-identical to prior behavior; the
    HARD RULE holds -- no float from here crosses into an L00M exact decision.
  * FIREWALL (decision b): only WIRED_JURISDICTIONS (THEOREM, COMPUTED) cross as fact. INTERPRETIVE /
    FALSE_AS_STATED are returned ONLY when explicitly requested and ALWAYS carry their jurisdiction +
    a `wired` flag. Learned/derived output (lexicon entries, render, observe/propose/commit) is COMPUTED.
  * NEVER raises across the wire (G6): a non-dict / invalid-JSON / BOM stdin soft-errors with the
    endpoint list; every endpoint catches its own exceptions; ASCII output (ensure_ascii).
  * One-way disjoint: loom is reached ONLY through loom_bridge (read-only); L00M never imports this.
"""
from __future__ import annotations

import io
import json
import sys
from dataclasses import asdict
from fractions import Fraction

from kira_language import semantic_kernel as K
from kira_language.semantic_kernel import Cl, WIRED_JURISDICTIONS, COMPUTED
from kira_language import loom_bridge
from kira_language import holding as Hq
from kira_language.holding import H
from kira_language import acquisition as acq
from kira_language.lexicon import Lexicon, Entry, _content_id

READ_TOL = 1e-9        # declared tolerance for the float (read-only) readings


# --- helpers --------------------------------------------------------------- #
def _holding(req) -> Cl:
    x = req.get("x", req.get("holding"))
    if x is None:
        raise ValueError("provide x=[a,b,c,d] (the holding)")
    if len(x) != 4:
        raise ValueError("holding must have 4 coordinates [a,b,c,d]")
    a, b, c, d = (float(v) for v in x)
    return Cl(a, b, c, d)


def _exact_holding(req) -> H:
    """Build an EXACT holding from the request. Pass coords as strings ('1/2') for true exactness;
    numbers go through holding's documented decimal-faithful boundary."""
    x = req.get("x", req.get("holding"))
    if x is None:
        raise ValueError("provide x=[a,b,c,d] (the holding)")
    if len(x) != 4:
        raise ValueError("holding must have 4 coordinates [a,b,c,d]")
    return H(*x)


def _stmt_dict(s) -> dict:
    return {**asdict(s), "digest": s.digest, "wired": s.jurisdiction in WIRED_JURISDICTIONS}


def _lexicon_from_req(req) -> Lexicon:
    """Rebuild the stateless lexicon carried in the request ('lexicon': [records]) by EXACTLY
    re-deriving each value through the acquisition loop (same path as store.restore)."""
    lex = Lexicon()
    for rec in req.get("lexicon", []) or []:
        lex.add(H(*[Fraction(s) for s in rec["value"]]))
    return lex


def _coords_str(X: H):
    return [str(c) for c in X.coords]


# --- QUERY (read-only) ----------------------------------------------------- #
def read_payload(req) -> dict:
    """All readings of a holding (the semantics layer). Float by default; exact:true -> Fraction core."""
    if req.get("exact"):
        return _read_exact_payload(req)
    X = _holding(req)
    p = K.probs(X)
    return {
        "holding": list(X),
        "tau_M": K.tau(K.M(X)),
        "det": K.det(X),
        "disc": K.disc(X),
        "rank": K.rank(X),
        "orbit": K.orbit(X),
        "gate": K.is_gate(X),
        "residual_height": K.residual_height(X),
        "residual_norm": abs(K.R_K(X)),
        "entropy_bits": K.entropy_bits(p),
        "purity": K.purity(p),
        "anisotropy": K.info_anisotropy(X),
        "regime": K.regime(X),
        "exact": False,
        "tol": READ_TOL,
    }


def _read_exact_payload(req) -> dict:
    """EXACT (Fraction-as-string) readings of a holding -- the wire path that may feed L00M (decision d)."""
    X = _exact_holding(req)
    return {
        "holding": _coords_str(X),
        "tr": str(Hq.tr(X)),
        "det": str(Hq.det(X)),
        "disc": str(Hq.disc(X)),
        "rank": Hq.rank(X),
        "TYPE": Hq.TYPE(X),
        "MASS": Hq.MASS(X),
        "gate": Hq.is_gate(X),
        "residual_height": Hq.residual_height(X),
        "R_K": _coords_str(Hq.R_K(X)),
        "exact": True,
    }


def laws_payload(req) -> dict:
    """The LAW_BANK (the dictionary). Firewalled: wired_only (default) hides INTERPRETIVE/FALSE."""
    wired_only = bool(req.get("wired_only", True))
    stmts = [s for s in K.LAW_BANK if (s.jurisdiction in WIRED_JURISDICTIONS or not wired_only)]
    return {"wired_only": wired_only, "count": len(stmts),
            "statements": [_stmt_dict(s) for s in stmts]}


def search_payload(req) -> dict:
    """Search the statement bank. Firewalled by default (wired_only)."""
    q = req.get("query", "")
    wired_only = bool(req.get("wired_only", True))
    hits = K.search_statements(q, limit=int(req.get("limit", 20)))
    if wired_only:
        hits = [s for s in hits if s.jurisdiction in WIRED_JURISDICTIONS]
    return {"query": q, "wired_only": wired_only, "count": len(hits),
            "statements": [_stmt_dict(s) for s in hits]}


def audit_payload(req) -> dict:
    """The kernel's closure audit (all gates). Read-only; deterministic (fixed-seed)."""
    return K.audit(int(req.get("samples", 512)))


def bridge_payload(req) -> dict:
    """The one-way phi-keystone bridge to LIVE loom (read-only; never raises)."""
    return loom_bridge.phi_keystone()


def lexicon_payload(req) -> dict:
    """The grown dictionary carried in the request (entries + stable ids). Stateless."""
    lex = _lexicon_from_req(req)
    return {"count": len(lex), "entries": lex.snapshot(), "ids": [e.id for e in lex.entries()]}


# --- GENERATE (deterministic, fact-only template-NLG) ---------------------- #
def render_payload(req) -> dict:
    """Render a holding to ONE fact-only sentence keyed off the exact readings (TYPE/MASS/det/rank/
    residual). SURFACE-ONLY: it asserts only what the fields already contain -- no ML, no new fact.
    Tagged COMPUTED (a derived statement), so it is wired."""
    X = _exact_holding(req)
    types = "+".join(Hq.TYPE(X))
    gate = "a gate" if Hq.is_gate(X) else "not a gate"
    sentence = (f"A holding of type {{{types}}} (mass {Hq.MASS(X)}): "
                f"trace {Hq.tr(X)}, det {Hq.det(X)}, rank {Hq.rank(X)}, {gate}, "
                f"residual height {Hq.residual_height(X)}.")
    return {
        "sentence": sentence,
        "jurisdiction": COMPUTED,
        "wired": True,
        "fields": {
            "TYPE": Hq.TYPE(X), "MASS": Hq.MASS(X), "tr": str(Hq.tr(X)),
            "det": str(Hq.det(X)), "rank": Hq.rank(X), "gate": Hq.is_gate(X),
            "residual_height": Hq.residual_height(X),
        },
        "exact": True,
    }


# --- INGEST (the acquisition+lexicon loop; propose-for-confirm) ------------- #
def observe_payload(req) -> dict:
    """observe(holding) -> residue/word + captured? (OUT-only; never grows). Mirrors ResidualLearner.observe."""
    X = _exact_holding(req)
    cap = acq.acquire(X)
    lex = _lexicon_from_req(req)
    return {
        "captured": cap.captured,
        "residual_before": _coords_str(cap.residual_before),
        "committed": _coords_str(cap.committed),
        "coords": [str(c) for c in cap.coords],
        "word": list(cap.word),
        "in_lexicon": cap.committed in lex,
        "jurisdiction": COMPUTED,
        "wired": True,
        "exact": True,
    }


def _proposal(cap) -> dict:
    e = Entry(id=_content_id(cap.committed), value=cap.committed, coords=cap.coords, word=cap.word)
    return e.to_record()


def propose_payload(req) -> dict:
    """propose(holding) -> a candidate entry (gated; NOT added). Mirrors ResidualLearner.propose."""
    X = _exact_holding(req)
    cap = acq.acquire(X)
    lex = _lexicon_from_req(req)
    return {
        "proposal": _proposal(cap),
        "is_new": cap.committed not in lex,
        "captured": cap.captured,
        "jurisdiction": COMPUTED,
        "wired": True,
        "exact": True,
    }


def commit_payload(req) -> dict:
    """commit(proposal | holding, + lexicon state) -> grown lexicon + witness. The SOLE grow verb
    (propose-for-confirm). Mirrors ResidualLearner.confirm. Stateless: returns the new lexicon to thread."""
    from kira_language import store as store_mod
    lex = _lexicon_from_req(req)
    if "proposal" in req and req["proposal"] is not None:
        X = H(*[Fraction(s) for s in req["proposal"]["value"]])
    else:
        X = _exact_holding(req)
    before = len(lex)
    entry = lex.add(X)
    return {
        "entry": entry.to_record(),
        "added": len(lex) > before,
        "count": len(lex),
        "lexicon": lex.snapshot(),
        "witness": store_mod.manifest(lex)["head"],   # tamper-evident chain head over the grown lexicon
        "jurisdiction": COMPUTED,
        "wired": True,
        "exact": True,
    }


# --- STORE (the sha256-chain JSON persistence) ----------------------------- #
def persist_payload(req) -> dict:
    from kira_language import store as store_mod
    path = req.get("path")
    if not path:
        raise ValueError("provide path")
    m = store_mod.persist(path, _lexicon_from_req(req))
    return {"path": path, "head": m["head"], "count": m["count"], "wrote": True}


def restore_payload(req) -> dict:
    from kira_language import store as store_mod
    path = req.get("path")
    if not path:
        raise ValueError("provide path")
    try:
        lex = store_mod.restore(path)
    except store_mod.ChainError as e:
        return {"path": path, "verified": False, "error": str(e)}
    return {"path": path, "verified": True, "count": len(lex), "lexicon": lex.snapshot()}


_DISPATCH = {
    "read": read_payload,
    "laws": laws_payload,
    "search": search_payload,
    "audit": audit_payload,
    "bridge": bridge_payload,
    "lexicon": lexicon_payload,
    "render": render_payload,
    "speak": render_payload,            # alias
    "observe": observe_payload,
    "propose": propose_payload,
    "commit": commit_payload,
    "persist": persist_payload,
    "restore": restore_payload,
}


def dispatch(req) -> dict:
    if not isinstance(req, dict):
        return {"error": "request must be a JSON object", "endpoints": sorted(_DISPATCH)}
    fn = _DISPATCH.get(req.get("endpoint"))
    if fn is None:
        return {"error": f"unknown endpoint {req.get('endpoint')!r}",
                "endpoints": sorted(_DISPATCH)}
    try:
        return fn(req)
    except Exception as e:                       # never raise across the wire (G6 posture)
        return {"error": str(e)}


def _read_request_text() -> str:
    """Read stdin and strip a UTF-8 BOM (text or byte) so a BOM-prefixed request still parses."""
    data = sys.stdin.read()
    if isinstance(data, bytes):
        return data.decode("utf-8-sig", errors="replace")
    return data.lstrip("\ufeff")


def main() -> None:
    """stdin (one request JSON) -> stdout (one result JSON). NEVER raises: a non-dict / invalid-JSON /
    BOM payload soft-errors with the endpoint list. Stray prints during compute are swallowed so stdout
    carries ONLY the JSON the endpoint parses. ASCII-safe (ensure_ascii)."""
    real_out = sys.stdout
    sys.stdout = io.StringIO()
    try:
        try:
            req = json.loads(_read_request_text())
        except Exception as e:
            result = {"error": f"invalid JSON request: {e}", "endpoints": sorted(_DISPATCH)}
        else:
            result = dispatch(req)
    finally:
        sys.stdout = real_out
    real_out.write(json.dumps(result, ensure_ascii=True, default=str))
    real_out.flush()


if __name__ == "__main__":
    main()
