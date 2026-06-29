"""test_lexicon.py -- the growing lexicon (increment 4), decided at zero tolerance.

Load-bearing per the foundation audit's lesson: exact-VALUE pins (not loose bounds), an INDEPENDENT
id recompute, and explicit same-residue / distinct-residue cases -- so a lexicon that deduped by the
coarse WORD (merging i and 2*i) or used a non-deterministic id would be caught, not rubber-stamped.
"""
import hashlib
import json
from fractions import Fraction

from kira_language import lexicon as L
from kira_language.lexicon import Lexicon, Entry, COMPUTED, _content_id
from kira_language import acquisition as acq
from kira_language.holding import H, VOID, ONE, E1, E2, I

Q0 = Fraction(0)


# --- add / lookup are exact -------------------------------------------------------------------- #
def test_add_returns_exact_entry():
    lex = Lexicon()
    e = lex.add(E1)
    assert isinstance(e, Entry)
    assert e.value == H(0, "1/5", "2/5", 0)          # the exact committed value
    assert e.coords == (Fraction(1, 5), Q0)
    assert e.word == ("+e1+2e2",)
    assert e.jurisdiction == COMPUTED
    assert lex.lookup(E1) is e                        # found by its own residue
    assert len(lex) == 1


def test_lookup_holding_and_word():
    lex = Lexicon()
    lex.add(I)
    lex.add(2 * I)                                     # same word "+i", DISTINCT value
    assert lex.lookup(E1) is None                      # unseen residue
    by_word = lex.lookup(("+i",))
    assert len(by_word) == 2                            # both i and 2i carry "+i"
    assert {e.value for e in by_word} == {H(0, 0, 0, 1), H(0, 0, 0, 2)}
    assert lex.lookup(("+e1+2e2",)) == ()              # word not present


# --- generalization by return-to-zero: EXACT dedup keyed on the residue ------------------------- #
def test_same_residue_dedups_idempotent():
    lex = Lexicon()
    a = lex.add(E1)
    b = lex.add(E1 + ONE)                              # ONE is orthogonal to ker -> SAME committed value
    c = lex.add(E1)                                    # re-add the same token
    assert a is b is c                                 # one entry, idempotent
    assert len(lex) == 1
    assert acq.project(E1 + ONE) == acq.project(E1)    # the exact reason they merge
    assert (E1 + ONE) in lex and I not in lex


def test_distinct_residues_stay_distinct():
    lex = Lexicon()
    e_i = lex.add(I)                                   # value (0,0,0,1)
    e_2i = lex.add(2 * I)                              # value (0,0,0,2) -- distinct, SAME word
    e_e1 = lex.add(E1)                                 # value (0,1/5,2/5,0)
    assert e_i.id != e_2i.id != e_e1.id and e_i.id != e_e1.id
    assert len(lex) == 3
    # the coarse word must NOT be the dedup key (this is the audit-style blind-spot guard):
    assert e_i.word == e_2i.word == ("+i",)
    assert e_i.value != e_2i.value


def test_lexicon_grows_and_dedups():
    lex = Lexicon()
    tokens = [E1, E1 + ONE, I, 2 * I, -I]              # residues: r(E1)=r(E1+ONE); i; 2i; -i  -> 4 distinct
    for t in tokens:
        lex.add(t)
    assert len(lex) == 4
    values = {e.value for e in lex.entries()}
    assert values == {H(0, "1/5", "2/5", 0), H(0, 0, 0, 1), H(0, 0, 0, 2), H(0, 0, 0, -1)}


def test_generalize_predicate():
    lex = Lexicon()
    assert lex.generalize(E1, E1 + ONE) is True        # same residue
    assert lex.generalize(I, E1) is False              # distinct residues
    assert lex.generalize(I, 2 * I) is False           # distinct values (same word)


# --- stable, deterministic, reproducible IDs (content hash of the exact value) ------------------ #
def test_ids_are_deterministic_and_order_independent():
    lex1 = Lexicon(); lex1.add(E1); lex1.add(I)
    lex2 = Lexicon(); lex2.add(I); lex2.add(2 * I); lex2.add(E1)   # different order + an extra token
    assert lex1.lookup(I).id == lex2.lookup(I).id                  # same value -> same id, any order/instance
    assert lex1.lookup(E1).id == lex2.lookup(E1).id


def test_id_matches_independent_recompute():
    lex = Lexicon()
    e = lex.add(I)                                     # value H(0,0,0,1) -> canon "0|0|0|1"
    expected = hashlib.sha256(b"0|0|0|1").hexdigest()[:16]
    assert e.id == expected
    assert e.id == _content_id(H(0, 0, 0, 1))
    assert all(ch in "0123456789abcdef" for ch in e.id)   # ASCII hex, stable
    # equal value via a different construction hashes identically (exact, reduced Fraction):
    assert _content_id(H(0, 0, 0, "2/2")) == _content_id(I)


# --- firewall: learned entries are COMPUTED, never THEOREM -------------------------------------- #
def test_entries_are_computed_not_theorem():
    from kira_language.semantic_kernel import COMPUTED as SK_COMPUTED, THEOREM
    assert COMPUTED == SK_COMPUTED                     # no drift from the firewall vocabulary
    lex = Lexicon()
    for t in (E1, I, 2 * I, E2):
        assert lex.add(t).jurisdiction == COMPUTED
    assert all(e.jurisdiction != THEOREM for e in lex.entries())


# --- JSON-serializable (persistence is increment 5, but the shape must round-trip exactly) ------ #
def test_snapshot_is_json_serializable_and_exact():
    lex = Lexicon()
    lex.add(E1); lex.add(I); lex.add(-I)
    snap = lex.snapshot()
    blob = json.dumps(snap)                            # must not raise (pure strings/lists)
    back = json.loads(blob)
    assert len(back) == 3
    # exact round-trip: reconstruct the holding from the stored strings and compare to the live value
    for rec, e in zip(back, lex.entries()):
        assert rec["id"] == e.id and rec["jurisdiction"] == COMPUTED
        assert H(*[Fraction(s) for s in rec["value"]]) == e.value
        assert tuple(rec["word"]) == e.word


# --- exactness / posture ------------------------------------------------------------------------ #
def test_everything_exact_no_float():
    lex = Lexicon()
    for t in (E1, I, 2 * I, E2, VOID):
        e = lex.add(t)
        for comp in e.value:
            assert isinstance(comp, Fraction)
        for c in e.coords:
            assert isinstance(c, Fraction)


def test_module_is_numpy_and_loom_free():
    """No numpy and no loom IMPORT (the docstring may mention 'loom' in prose; that's fine). The
    subprocess check proves importing lexicon pulls neither dependency, independent of test order."""
    import inspect
    import subprocess
    import sys
    src = inspect.getsource(L)
    assert "import numpy" not in src and "from numpy" not in src
    assert "import loom" not in src and "loom_bridge" not in src
    out = subprocess.run(
        [sys.executable, "-c",
         "import sys, kira_language.lexicon; print('numpy' in sys.modules, 'loom' in sys.modules)"],
        capture_output=True, text=True,
    )
    assert out.returncode == 0, out.stderr
    assert out.stdout.strip() == "False False"
