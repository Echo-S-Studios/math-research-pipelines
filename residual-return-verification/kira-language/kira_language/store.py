"""store.py -- exact JSON persistence + a sha256 hash-chain for the growing lexicon (increment 5).

Persist and restore the increment-4 `Lexicon` EXACTLY, with a tamper-evident witness chain -- mirroring
the substrate's `vector_substrate_store` (anchors + records + a `sha256(prev + json)[:16]` chain from a
"genesis" seed). The chain makes the persisted dictionary auditable: any edited record breaks it.

    manifest(lex)        -> the witnessed dict: format/genesis/count/head + per-record chain hashes
    persist(path, lex)   -> write that manifest as ASCII JSON; return it
    load(path)           -> read the manifest back
    verify(manifest)     -> bool: recompute the chain and check every link + the head (never raises)
    restore(path)        -> verify, then EXACTLY re-derive the lexicon and return it (raises ChainError)

EXACT RE-DERIVATION, not lossy deserialization: values are stored as canonical Fraction strings, so
restore reconstructs each holding bit-identically and REPLAYS it through the acquisition loop
(`Lexicon.add`), which recomputes the id/coords/word from the exact value -- then cross-checks them
against the persisted record. So `restore(persist(lex)) == lex` exactly (same entries, same ids, same
dedup), and a record whose value and metadata disagree is rejected, not silently trusted.

POSTURE
  * EXACT (G8): Fraction round-trips exactly (1/5 stays 1/5, never floated); deterministic bytes for a
    given lexicon (sorted keys, fixed separators).
  * ASCII-SAFE: `ensure_ascii=True` + the file is written/read as ASCII (the chain is hex, values are
    Fraction strings, words are ASCII) -- KIRA can shell it raw.
  * FIREWALL (decision b): persisted entries stay COMPUTED. jurisdiction is inside the hashed record AND
    re-derived on restore, so a record silently promoted to THEOREM fails BOTH the chain and the
    re-derivation cross-check.
  * IMPORT-SAFE + ONE-WAY: importing does no I/O (only function defs); pure stdlib + `lexicon`/`holding`;
    no numpy, no loom. I/O happens only when persist/restore are called with a path.

SCOPE (increment 5): persist / restore / the chain / verify. The KIRA-shell dispatch over these (the
`persist`/`restore` endpoints) is increment 6 and is NOT built here.
"""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from typing import List

from kira_language.holding import H
from kira_language.lexicon import Lexicon, COMPUTED

GENESIS = "genesis"
FORMAT = "kira-language.lexicon.store/v1"
_FIELDS = ("id", "value", "coords", "word", "jurisdiction")   # the hashed (chain-bound) record fields


class ChainError(Exception):
    """Raised when a persisted lexicon fails hash-chain verification or exact re-derivation."""


def _canon(bare: dict) -> str:
    """Deterministic canonical JSON of a bare record (sorted keys, no spaces, ASCII)."""
    return json.dumps(bare, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _chain_hash(prev: str, bare: dict) -> str:
    return hashlib.sha256((prev + _canon(bare)).encode("ascii")).hexdigest()[:16]


def manifest(lexicon: Lexicon) -> dict:
    """Build the witnessed manifest for a lexicon (no I/O). The chain binds record order to the head."""
    prev = GENESIS
    records: List[dict] = []
    for rec in lexicon.snapshot():
        bare = {k: rec[k] for k in _FIELDS}
        prev = _chain_hash(prev, bare)
        records.append({**bare, "chain": prev})
    return {"format": FORMAT, "genesis": GENESIS, "count": len(records), "head": prev, "records": records}


def persist(path, lexicon: Lexicon) -> dict:
    """Write the lexicon's manifest as deterministic ASCII JSON to `path`; return the manifest."""
    m = manifest(lexicon)
    with open(path, "w", encoding="ascii", newline="\n") as f:
        json.dump(m, f, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return m


def load(path) -> dict:
    with open(path, "r", encoding="ascii") as f:
        return json.load(f)


def verify(m: dict) -> bool:
    """Recompute the chain from the genesis seed and check every link + the head. Never raises."""
    try:
        prev = m.get("genesis", GENESIS)
        for rec in m["records"]:
            bare = {k: rec[k] for k in _FIELDS}
            prev = _chain_hash(prev, bare)
            if prev != rec.get("chain"):
                return False
        return prev == m.get("head") and len(m["records"]) == m.get("count")
    except Exception:
        return False


def restore(path) -> Lexicon:
    """Load, VERIFY the chain, then EXACTLY re-derive the lexicon (replay values through acquisition,
    cross-checking id/coords/word/jurisdiction). Raises ChainError on tamper or any mismatch."""
    m = load(path)
    if not verify(m):
        raise ChainError("hash-chain verification failed (tampered or corrupt store)")
    lex = Lexicon()
    for rec in m["records"]:
        value = H(*[Fraction(s) for s in rec["value"]])
        entry = lex.add(value)                                # re-derive through the exact loop
        if (entry.id != rec["id"]
                or [str(c) for c in entry.coords] != rec["coords"]
                or list(entry.word) != rec["word"]
                or entry.jurisdiction != rec["jurisdiction"]
                or rec["jurisdiction"] != COMPUTED):          # learned entries are COMPUTED, never promoted
            raise ChainError(f"re-derived entry disagrees with persisted record {rec.get('id')!r}")
    if len(lex) != m["count"]:
        raise ChainError("restored entry count does not match the manifest")
    return lex


def _demo() -> None:                                          # pragma: no cover -- human-facing, ASCII-only
    import tempfile
    import os
    from kira_language.holding import E1, I, ONE
    lex = Lexicon()
    for X in (E1, E1 + ONE, I, 2 * I, -I):
        lex.add(X)
    path = os.path.join(tempfile.gettempdir(), "kira_lexicon_store_demo.json")
    m = persist(path, lex)
    back = restore(path)
    print(f"  persisted {m['count']} entries, head={m['head']}, chain verifies={verify(m)}")
    print(f"  restore bit-identical: {back.snapshot() == lex.snapshot()}")
    os.remove(path)


if __name__ == "__main__":
    _demo()
