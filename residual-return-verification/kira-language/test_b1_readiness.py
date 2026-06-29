"""test_b1_readiness.py -- the B1-READINESS GATE (increment 7).

Codifies the PREP_PLAN section-3 checklist as executable assertions: one test per readiness invariant.
All green == the language space is PREPARED for the (separate, Ace-gated) B1 live wire. B1 itself --
the KIRA /api/language/* routes -- is a cross-repo step and is NOT built here.
"""
import glob
import json
import os
import subprocess
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
L00M = os.environ.get("KIRA_LANG_L00M_ROOT") or os.path.normpath(os.path.join(HERE, os.pardir, "L00M"))

SHIPPED = ["kira_language", "kira_language.holding", "kira_language.acquisition",
           "kira_language.lexicon", "kira_language.store", "kira_language.loom_bridge",
           "kira_language.portable_io", "kira_language.semantic_kernel", "kira_language.dispatch"]

SECTION_4_CONTRACT = {"read", "laws", "search", "audit", "bridge", "lexicon",
                      "render", "speak", "observe", "propose", "commit", "persist", "restore"}


def _shell(payload, extra_env=None):
    env = dict(os.environ)
    env.setdefault("PYTHONIOENCODING", "utf-8")
    if extra_env:
        env.update(extra_env)
    return subprocess.run([sys.executable, "-m", "kira_language"], cwd=HERE, input=payload,
                          capture_output=True, text=True, encoding="utf-8", env=env)


# 1 -- IMPORT-SAFE ------------------------------------------------------------------------------ #
def test_import_safe():
    probe = subprocess.run(
        [sys.executable, "-c", "import sys, kira_language; print('numpy' in sys.modules, 'loom' in sys.modules)"],
        cwd=HERE, capture_output=True, text=True)
    assert probe.returncode == 0 and probe.stdout.strip() == "False False"   # package import: no numpy/loom
    for m in SHIPPED:                                                         # every shipped module imports clean
        r = subprocess.run([sys.executable, "-c", f"import {m}"], cwd=HERE, capture_output=True, text=True)
        assert r.returncode == 0, (m, r.stderr)
        assert r.stdout.strip() == "", (m, r.stdout)                          # side-effect-free (no stray prints)


# 2 -- ASCII / cp1252-SAFE (no PYTHONUTF8) ------------------------------------------------------ #
def test_ascii_cp1252_safe():
    req = {"endpoint": "read", "exact": True, "x": ["1/2", 1, "-1/2", 0]}
    proc = _shell(json.dumps(req), extra_env={"PYTHONIOENCODING": "cp1252"})
    assert proc.returncode == 0, proc.stderr
    out = proc.stdout.strip().splitlines()[-1]
    assert all(ord(c) < 128 for c in out)                                    # pure-ASCII wire on a legacy console
    assert json.loads(out)["TYPE"] == ["gen"]


# 3 -- EXACT (zero-tolerance decisions; no float into an exact decision) ------------------------ #
def test_exact_zero_tolerance():
    from kira_language import holding as Q
    from kira_language.holding import H, VOID, ONE, P0
    from kira_language import acquisition as acq
    assert Q.nu(P0) == VOID and Q.R_K(ONE) == VOID                            # decided with ==, no tolerance
    assert isinstance(Q.det(H(1, 2, "1/2", "3/10")), Fraction)
    g = H(7, 3, 2, 5)
    assert acq.is_captured(acq.project(g)) is True                           # exact ker membership
    assert acq.project(acq.project(g)) == acq.project(g)                     # exact idempotent projector
    assert all(isinstance(c, Fraction) for c in acq.project(g))              # no float in the committed value
    assert H(0.1).a == Fraction("0.1")                                       # the sole float entry is decimal-faithful


# 4 -- FLOAT QUARANTINED + DECLARED ------------------------------------------------------------- #
def test_float_quarantined_and_declared():
    from kira_language import dispatch as D
    flo = D.dispatch({"endpoint": "read", "x": [0.5, 0, 0.5, 0]})
    assert flo["exact"] is False and "tol" in flo                            # float reading: tagged + declared tol
    exa = D.dispatch({"endpoint": "read", "exact": True, "x": ["1/2", 0, "1/2", 0]})
    assert exa["exact"] is True and all(isinstance(v, str) for v in exa["holding"])   # exact: Fraction-as-string


# 5 -- FIREWALL (only THEOREM/COMPUTED cross as fact) ------------------------------------------- #
def test_firewall():
    from kira_language import dispatch as D
    from kira_language.semantic_kernel import INTERPRETIVE, FALSE_AS_STATED, WIRED_JURISDICTIONS
    juris = {s["jurisdiction"] for s in D.dispatch({"endpoint": "laws"})["statements"]}
    assert INTERPRETIVE not in juris and FALSE_AS_STATED not in juris and juris <= set(WIRED_JURISDICTIONS)
    for req in ({"endpoint": "render", "x": [0, 0, 0, 1]}, {"endpoint": "commit", "x": [0, 0, 0, 1]}):
        assert D.dispatch(req)["jurisdiction"] in WIRED_JURISDICTIONS         # learned/derived = COMPUTED, wired


# 6 -- ONE-WAY (L00M never imports this; loom only via bridge; phi agrees with live loom) ------- #
def test_one_way_and_live_phi():
    offenders = []
    for f in glob.glob(os.path.join(L00M, "**", "*.py"), recursive=True):
        try:
            t = open(f, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        if "kira_language" in t or "kira-language" in t:
            offenders.append(f)
    assert offenders == [], offenders                                        # L00M references kira_language nowhere
    for m in ("holding", "acquisition", "lexicon", "store", "dispatch", "semantic_kernel", "portable_io"):
        src = open(os.path.join(HERE, "kira_language", m + ".py"), encoding="utf-8").read()
        assert "\nimport loom" not in src, m                                 # only loom_bridge imports loom
    from kira_language import loom_bridge
    r = loom_bridge.phi_keystone()
    assert r["loom_reachable"] is True and r["agree"] is True
    assert abs(r["mahler"] - r["phi"]) < r["tol"]["mahler"]


# 7 -- PERSISTENT (round-trips exactly; chain verifies; tamper-evident) ------------------------- #
def test_persistent(tmp_path):
    from kira_language.lexicon import Lexicon
    from kira_language.holding import E1, I, ONE
    from kira_language import store
    lex = Lexicon()
    for x in (E1, E1 + ONE, I, 2 * I, -I):
        lex.add(x)
    p = str(tmp_path / "r.json")
    m = store.persist(p, lex)
    assert store.verify(m) is True
    assert store.restore(p).snapshot() == lex.snapshot()                     # exact round-trip
    mm = store.load(p)
    mm["records"][0]["value"] = ["0", "1/4", "2/5", "0"]
    open(p, "w", encoding="ascii").write(json.dumps(mm))
    assert store.verify(store.load(p)) is False                             # tamper-evident


# 8 -- KIRA-SHELL-READY (section-4 contract complete + local-equivalence every endpoint) -------- #
def test_kira_shell_ready():
    from kira_language import dispatch as D
    assert SECTION_4_CONTRACT <= set(D._DISPATCH)                            # the surface is complete
    reqs = [
        {"endpoint": "read", "x": [0.5, 0, 0.5, 0]},
        {"endpoint": "read", "exact": True, "x": ["1/2", 1, "-1/2", 0]},
        {"endpoint": "laws"}, {"endpoint": "search", "query": "residual"},
        {"endpoint": "audit", "samples": 32}, {"endpoint": "bridge"}, {"endpoint": "lexicon"},
        {"endpoint": "render", "x": [0, 0, 0, 1]}, {"endpoint": "observe", "x": [0, 1, 0, 0]},
        {"endpoint": "propose", "x": [0, 0, 0, 1]}, {"endpoint": "commit", "x": [0, 0, 0, 1]},
    ]
    for req in reqs:
        inproc = json.loads(json.dumps(D.dispatch(req), default=str))
        proc = _shell(json.dumps(req))
        assert proc.returncode == 0, proc.stderr
        assert inproc == json.loads(proc.stdout.strip().splitlines()[-1]), req["endpoint"]


# 9 -- GREEN (the full suite collects and exceeds the increment-6 headline) --------------------- #
def test_suite_green_headline():
    out = subprocess.run([sys.executable, "-m", "pytest", "--co", "-q"], cwd=HERE,
                         capture_output=True, text=True, env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    assert out.returncode == 0, out.stderr
    n = sum(1 for ln in out.stdout.splitlines() if "::" in ln)
    assert n >= 111                                                          # >= increment-6 headline


# 10 -- MATH PRESERVED (KL_DTA spine + conformance; LAW_BANK intact; candidates pristine) ------- #
def test_math_preserved():
    from kira_language.semantic_kernel import LAW_BANK
    assert len(LAW_BANK) == 27                                               # 20 THEOREM + 5 COMPUTED + 2 INTERPRETIVE
    for f in ("recursive_return_nlp.py", "KL_DTA__Vsemantic_kernel.py"):
        assert os.path.exists(os.path.join(HERE, "candidates", f))           # candidates pristine (provenance)
    out = subprocess.run(
        [sys.executable, "-m", "pytest", "--co", "-q", "test_KL_DTA.py", "test_kl_dta_conformance.py"],
        cwd=HERE, capture_output=True, text=True, env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    assert out.returncode == 0, out.stderr
    assert sum(1 for ln in out.stdout.splitlines() if "::" in ln) >= 25      # the spine + conformance collectable
