"""lexicon.py -- the GROWING dictionary (increment 4, the NLP axis), built on the acquisition loop.

A WORD is a residual packet: returning a holding to ker(L) (acquisition) commits it to an EXACT
learned value (a point in the phi-slack) and labels it with a sign-aware sparse word. This module is
the live, GROWING lexicon over those captures -- the working realization of the kernel's static
word/statement notion as a dictionary that grows as new residues commit:

    add(X)        -> return X to ker(L), commit, and LEARN its value (idempotent)
    lookup(key)   -> by holding (its residue's entry) or by word (all entries carrying that word)
    generalize    -> do two tokens return to the SAME exact residue? (would share one entry)

GENERALIZATION BY RETURN-TO-ZERO is the whole point: the dedup key is the EXACT committed residue
(`acquisition.project(X)`), decided with == on Fraction (zero tolerance). Tokens that commit to the
same exact value collapse to ONE entry (e.g. X and X+ONE, since ONE is orthogonal to the slack);
DISTINCT residues stay DISTINCT entries (e.g. i and 2*i -- same word, different exact value). Stable
IDs are a content hash of the exact value, so they are deterministic and reproducible regardless of
insertion order or instance.

POSTURE
  * EXACT (G8): keys/values are exact (Fraction / exact word); membership + dedup decided at zero
    tolerance; IDs deterministic. NO float, NO numpy, NO loom (pure algebra over `holding`/`acquisition`).
  * FIREWALL (decision b): a learned entry is COMPUTED (it was learned, not proven) -- NEVER a THEOREM.
    The fixed LAW_BANK in `semantic_kernel` (the law dictionary) is separate and untouched; THIS is the
    learned dictionary. (The "COMPUTED" tag here matches semantic_kernel.COMPUTED; cross-checked in tests.)
  * IMPORT-SAFE + ASCII-SAFE: importing does no I/O; ids are hex, words/records are pure ASCII.

SCOPE (increment 4): the in-memory growing dictionary + add/lookup/generalize/IDs. Records are kept
JSON-serializable (`Entry.to_record` / `Lexicon.snapshot`), but the sha256-hash-chain JSON STORE
(persist/restore) is DEFERRED to increment 5 (`store.py`) and is NOT built here.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, List, Optional, Tuple, Union

from kira_language.holding import H
from kira_language import acquisition as acq

# Firewall tag: a learned lexicon entry is COMPUTED, never THEOREM. Mirrors semantic_kernel.COMPUTED
# (kept as a local literal so the lexicon stays numpy-free / light; test_lexicon pins they agree).
COMPUTED = "COMPUTED"


def _content_id(value: H) -> str:
    """Deterministic, order-independent stable id = sha256 of the exact value's canonical Fraction
    string. Equal exact values -> identical id (this IS the exact dedup key). ASCII hex, 16 chars."""
    canon = "|".join(str(c) for c in value.coords)      # reduced Fraction strings, e.g. "0|1/5|2/5|0"
    return hashlib.sha256(canon.encode("ascii")).hexdigest()[:16]


@dataclass(frozen=True)
class Entry:
    """One learned dictionary entry: an exact value in ker(L), its kernel coordinates, its sign word,
    and the firewall jurisdiction (COMPUTED -- learned, never proven)."""
    id: str
    value: H                            # the exact committed value (a point in the phi-slack)
    coords: Tuple[Fraction, ...]        # its kernel-basis coordinates (exact)
    word: Tuple[str, ...]               # its sign-aware sparse code
    jurisdiction: str = COMPUTED

    def to_record(self) -> dict:
        """JSON-serializable shape (exact Fraction as string). Persistence itself is increment 5."""
        return {
            "id": self.id,
            "value": [str(c) for c in self.value.coords],
            "coords": [str(c) for c in self.coords],
            "word": list(self.word),
            "jurisdiction": self.jurisdiction,
        }


class Lexicon:
    """A growing word->value dictionary keyed by the EXACT residue. Insertion-ordered; grows on a new
    residue, dedups (idempotent) on a known one."""

    def __init__(self) -> None:
        self._by_id: Dict[str, Entry] = {}              # id -> Entry, insertion-ordered

    def __len__(self) -> int:
        return len(self._by_id)

    def __contains__(self, key: Union[H, str]) -> bool:
        """`X in lex` for a holding tests whether X's residue is learned; `id in lex` for a str id."""
        if isinstance(key, H):
            return _content_id(acq.project(key)) in self._by_id
        return key in self._by_id

    def entries(self) -> Tuple[Entry, ...]:
        return tuple(self._by_id.values())

    def get(self, entry_id: str) -> Optional[Entry]:
        return self._by_id.get(entry_id)

    def add(self, X: H) -> Entry:
        """Return X to ker(L), commit, and learn its value. Idempotent: re-adding any token whose
        residue is already known returns the SAME entry and does NOT grow the lexicon."""
        cap = acq.acquire(X)
        eid = _content_id(cap.committed)
        existing = self._by_id.get(eid)
        if existing is not None:
            return existing
        entry = Entry(id=eid, value=cap.committed, coords=cap.coords, word=cap.word)
        self._by_id[eid] = entry
        return entry

    def lookup(self, key: Union[H, Tuple[str, ...], List[str]]):
        """lookup(holding) -> the single Entry for its exact residue, or None.
        lookup(word)    -> the tuple of entries carrying that exact word (0, 1, or several, since
        distinct values can share a word). The two return shapes mirror 'by residue' vs 'by label'."""
        if isinstance(key, H):
            return self._by_id.get(_content_id(acq.project(key)))
        wanted = tuple(key)
        return tuple(e for e in self._by_id.values() if e.word == wanted)

    def generalize(self, X: H, Y: H) -> bool:
        """True iff X and Y return to the SAME exact residue (they would share one entry)."""
        return acq.project(X) == acq.project(Y)

    def snapshot(self) -> List[dict]:
        """A JSON-serializable list of records (what increment-5 persistence will consume)."""
        return [e.to_record() for e in self._by_id.values()]


def _demo() -> None:                                    # pragma: no cover -- human-facing, ASCII-only
    from kira_language.holding import E1, E2, I, ONE
    lex = Lexicon()
    for X in (E1, E1 + ONE, I, 2 * I, -I):
        e = lex.add(X)
        print(f"  add({X!r:18}) -> id={e.id} value={e.value!r} word={e.word}")
    print(f"  {len(lex)} entries (E1 and E1+ONE share a residue; i, 2i, -i are distinct values).")


if __name__ == "__main__":
    _demo()
