"""test_store.py -- exact persistence + the sha256 hash-chain (increment 5), at zero tolerance.

Load-bearing per the foundation audit's lesson: exact-VALUE pins (1/5 must survive, not float), an
independent re-derivation, and explicit TAMPER cases -- so a lossy round-trip, a chain that doesn't
actually detect tampering, or a non-deterministic serialization would be caught, not rubber-stamped.
"""
import json
from fractions import Fraction

import pytest

from kira_language import store as S
from kira_language.store import persist, restore, load, verify, manifest, ChainError, GENESIS, FORMAT
from kira_language.lexicon import Lexicon, COMPUTED
from kira_language.holding import H, ONE, E1, E2, I


def _lex(*tokens):
    lex = Lexicon()
    for t in tokens:
        lex.add(t)
    return lex


SEED = (E1, E1 + ONE, I, 2 * I, -I, E2)        # residues: r(E1)=r(E1+ONE); i; 2i; -i; r(E2) -> 5 distinct


# --- round-trip is bit-identical and EXACT ------------------------------------------------------ #
def test_round_trip_bit_identical(tmp_path):
    lex = _lex(*SEED)
    p = tmp_path / "store.json"
    persist(p, lex)
    back = restore(p)
    assert back.snapshot() == lex.snapshot()              # exact, ordered, every field
    assert manifest(back) == manifest(lex)                 # incl. ids + the whole chain + head
    assert len(back) == len(lex) == 5


def test_exact_fraction_survives_round_trip(tmp_path):
    lex = _lex(E1)                                          # E1 commits to H(0, 1/5, 2/5, 0)
    p = tmp_path / "s.json"
    persist(p, lex)
    text = p.read_text(encoding="ascii")
    assert '"1/5"' in text and '"2/5"' in text             # stored as exact Fractions, NOT 0.2/0.4
    assert "0.2" not in text and "0.4" not in text
    e = restore(p).lookup(E1)
    assert e.value == H(0, "1/5", "2/5", 0)
    assert e.coords == (Fraction(1, 5), Fraction(0)) and all(isinstance(c, Fraction) for c in e.coords)


# --- the chain verifies, and is TAMPER-EVIDENT -------------------------------------------------- #
def test_chain_verifies_and_head_is_bound(tmp_path):
    lex = _lex(*SEED)
    p = tmp_path / "s.json"
    m = persist(p, lex)
    assert m["format"] == FORMAT and m["genesis"] == GENESIS and m["count"] == 5
    assert verify(load(p)) is True
    assert m["head"] == m["records"][-1]["chain"]          # head == last link
    assert all(len(r["chain"]) == 16 for r in m["records"])


def test_tamper_on_value_is_detected(tmp_path):
    lex = _lex(E1, I)
    p = tmp_path / "s.json"
    persist(p, lex)
    m = load(p)
    m["records"][0]["value"] = ["0", "1/4", "2/5", "0"]    # change 1/5 -> 1/4
    p.write_text(json.dumps(m), encoding="ascii")
    assert verify(load(p)) is False
    with pytest.raises(ChainError):
        restore(p)


def test_tamper_on_jurisdiction_is_detected(tmp_path):
    """Firewall: silently promoting a persisted entry to THEOREM breaks the chain AND re-derivation."""
    lex = _lex(I)
    p = tmp_path / "s.json"
    persist(p, lex)
    m = load(p)
    m["records"][0]["jurisdiction"] = "THEOREM"
    p.write_text(json.dumps(m), encoding="ascii")
    assert verify(load(p)) is False
    with pytest.raises(ChainError):
        restore(p)


def test_tamper_on_chain_hash_is_detected(tmp_path):
    lex = _lex(E1, I, E2)
    p = tmp_path / "s.json"
    persist(p, lex)
    m = load(p)
    m["records"][1]["chain"] = "0000000000000000"
    p.write_text(json.dumps(m), encoding="ascii")
    assert verify(load(p)) is False
    with pytest.raises(ChainError):
        restore(p)


def test_reordering_records_breaks_chain(tmp_path):
    """The chain binds ORDER (h_k folds in h_{k-1}); swapping records must break verification."""
    lex = _lex(E1, I, E2)
    p = tmp_path / "s.json"
    persist(p, lex)
    m = load(p)
    m["records"][0], m["records"][1] = m["records"][1], m["records"][0]
    p.write_text(json.dumps(m), encoding="ascii")
    assert verify(load(p)) is False
    with pytest.raises(ChainError):
        restore(p)


# --- deterministic serialization ---------------------------------------------------------------- #
def test_serialization_is_deterministic(tmp_path):
    lex = _lex(*SEED)
    a, b = tmp_path / "a.json", tmp_path / "b.json"
    persist(a, lex)
    persist(b, lex)
    assert a.read_bytes() == b.read_bytes()                # same lexicon -> byte-identical file
    assert manifest(lex) == manifest(lex)


# --- firewall preserved across persistence ------------------------------------------------------ #
def test_restored_entries_are_computed(tmp_path):
    from kira_language.semantic_kernel import THEOREM
    lex = _lex(E1, I, 2 * I)
    p = tmp_path / "s.json"
    persist(p, lex)
    back = restore(p)
    assert all(e.jurisdiction == COMPUTED for e in back.entries())
    assert all(e.jurisdiction != THEOREM for e in back.entries())


# --- edges + posture ---------------------------------------------------------------------------- #
def test_empty_lexicon_round_trips(tmp_path):
    lex = Lexicon()
    p = tmp_path / "empty.json"
    m = persist(p, lex)
    assert m["count"] == 0 and m["head"] == GENESIS and m["records"] == []
    assert verify(m) is True
    assert len(restore(p)) == 0


def test_persisted_file_is_pure_ascii(tmp_path):
    lex = _lex(*SEED)
    p = tmp_path / "s.json"
    persist(p, lex)
    raw = p.read_bytes()
    assert all(b < 128 for b in raw)                       # ASCII-safe wire


def test_module_is_numpy_and_loom_free():
    import inspect
    import subprocess
    import sys
    src = inspect.getsource(S)
    assert "import numpy" not in src and "from numpy" not in src
    assert "import loom" not in src and "loom_bridge" not in src
    out = subprocess.run(
        [sys.executable, "-c",
         "import sys, kira_language.store; print('numpy' in sys.modules, 'loom' in sys.modules)"],
        capture_output=True, text=True,
    )
    assert out.returncode == 0, out.stderr
    assert out.stdout.strip() == "False False"
