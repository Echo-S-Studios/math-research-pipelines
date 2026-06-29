"""test_dispatch_full.py -- the FULL KIRA-shell dispatch surface (increment 6), load-bearing.

Covers the increment-6 additions on top of the existing test_language_api.py: local-equivalence for
every NEW endpoint, the robustness fix (non-dict / invalid-JSON / BOM stdin -> soft error, no crash),
deterministic fact-only render, the observe->propose->commit loop growing the lexicon END-TO-END
through the wire, persist/restore round-trip through the wire, and the firewall on the new verbs.
"""
import json
import os
import subprocess
import sys

import pytest

from kira_language import dispatch as D
from kira_language.semantic_kernel import INTERPRETIVE, FALSE_AS_STATED, WIRED_JURISDICTIONS, COMPUTED

HERE = os.path.dirname(os.path.abspath(__file__))

# a known lexicon record (only "value" is load-bearing for re-derivation) -- i = pseudoscalar
_REC_I = {"id": "ab113d678fd4b6a3", "value": ["0", "0", "0", "1"],
          "coords": ["0", "1"], "word": ["+i"], "jurisdiction": "COMPUTED"}

NEW_REQUESTS = [
    {"endpoint": "read", "exact": True, "x": ["1/2", 1, "-1/2", 0]},
    {"endpoint": "lexicon"},
    {"endpoint": "lexicon", "lexicon": [_REC_I]},
    {"endpoint": "render", "x": ["1/2", 1, "-1/2", 0]},
    {"endpoint": "speak", "x": [0, 0, 0, 1]},
    {"endpoint": "observe", "x": [0, 1, 0, 0]},
    {"endpoint": "observe", "x": [0, 0, 0, 1], "lexicon": [_REC_I]},
    {"endpoint": "propose", "x": [0, 0, 0, 1]},
    {"endpoint": "commit", "x": [0, 0, 0, 1]},
]


def _shell(payload_text, env_utf8=False):
    env = dict(os.environ)
    if env_utf8:
        env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [sys.executable, "-m", "kira_language"],
        cwd=HERE, input=payload_text, capture_output=True, text=True, encoding="utf-8", env=env,
    )


def _shell_json(req):
    proc = _shell(json.dumps(req))
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout.strip().splitlines()[-1])


# --- local equivalence: in-process dispatch == subprocess, for every NEW endpoint -------------- #
@pytest.mark.parametrize("req", NEW_REQUESTS,
                         ids=[r["endpoint"] + ("_exact" if r.get("exact") else "")
                              + ("_state" if r.get("lexicon") else "") for r in NEW_REQUESTS])
def test_local_equivalence_new_endpoints(req):
    inproc = json.loads(json.dumps(D.dispatch(req), default=str))
    assert inproc == _shell_json(req)


# --- the robustness fix: bad stdin SOFT-ERRORS, never crashes ---------------------------------- #
@pytest.mark.parametrize("bad", ["[1,2,3]", "42", '"hello"', "null", "true", "{not valid json", ""])
def test_non_dict_or_invalid_json_soft_errors(bad):
    proc = _shell(bad)
    assert proc.returncode == 0, proc.stderr                  # NO crash (the pre-existing gap, fixed)
    out = json.loads(proc.stdout.strip().splitlines()[-1])
    assert "error" in out and "endpoints" in out              # soft error with the endpoint list
    # in-process is equivalently soft for the non-dict cases:
    if bad in ("[1,2,3]", "42", '"hello"', "null", "true"):
        r = D.dispatch(json.loads(bad))
        assert "error" in r and "endpoints" in r


def test_utf8_bom_on_stdin_is_handled():
    """A UTF-8 BOM prefix must not crash and must still parse (the request is otherwise valid)."""
    req = {"endpoint": "read", "exact": True, "x": ["1/2", 1, "-1/2", 0]}
    proc = _shell("﻿" + json.dumps(req), env_utf8=True)
    assert proc.returncode == 0, proc.stderr
    out = json.loads(proc.stdout.strip().splitlines()[-1])
    assert out.get("exact") is True and out.get("TYPE") == ["gen"]   # parsed despite the BOM


# --- render: deterministic, fact-only, COMPUTED ------------------------------------------------ #
def test_render_is_deterministic_and_fact_only():
    import re
    req = {"endpoint": "render", "x": ["1/2", 1, "-1/2", 0]}    # the phi keystone: gen, det -1, rank 2
    a = D.dispatch(req)
    assert a == D.dispatch(req)                                # deterministic
    assert a["jurisdiction"] == COMPUTED and a["wired"] is True

    # FACT-ONLY (the load-bearing guarantee): the sentence asserts ONLY what the fields contain --
    # no invented fact may survive (a prepended "AXIOM:" or an appended " It is sacred." must fail).
    # (1) full-string equality to the EXACT expected sentence for this holding:
    assert a["sentence"] == ("A holding of type {gen} (mass 1): "
                             "trace 1, det -1, rank 2, not a gate, residual height 2.")
    # (2) generically: the sentence equals the template rebuilt from ONLY the returned fields, so an
    #     additive claim that is not itself a field is impossible to hide:
    f = a["fields"]
    gate_phrase = "a gate" if f["gate"] else "not a gate"
    rebuilt = ("A holding of type {%s} (mass %s): trace %s, det %s, rank %s, %s, residual height %s." % (
        "+".join(f["TYPE"]), f["MASS"], f["tr"], f["det"], f["rank"], gate_phrase, f["residual_height"]))
    assert a["sentence"] == rebuilt
    # (3) no claim-token outside the fixed template vocabulary + this holding's actual TYPE words:
    allowed = {"a", "holding", "of", "type", "mass", "trace", "det", "rank",
               "not", "gate", "residual", "height"} | {t.lower() for t in f["TYPE"]}
    words = set(re.findall(r"[a-z]+", a["sentence"].lower()))
    assert words <= allowed, f"render invented non-field tokens: {words - allowed}"

    assert a["fields"]["TYPE"] == ["gen"] and a["fields"]["det"] == "-1"
    assert _shell_json(req) == json.loads(json.dumps(a, default=str))


# --- the ingest loop grows the lexicon END-TO-END through the wire (stateless) ------------------ #
def test_observe_propose_commit_loop_through_wire():
    # observe is OUT-only (no growth)
    obs = _shell_json({"endpoint": "observe", "x": [0, 0, 0, 1]})
    assert obs["captured"] is True and obs["word"] == ["+i"] and obs["in_lexicon"] is False
    # propose is gated (a candidate, not added)
    prop = _shell_json({"endpoint": "propose", "x": [0, 0, 0, 1]})
    assert prop["is_new"] is True and prop["proposal"]["value"] == ["0", "0", "0", "1"]
    # commit grows; thread the returned lexicon state forward
    c1 = _shell_json({"endpoint": "commit", "x": [0, 0, 0, 1]})
    assert c1["added"] is True and c1["count"] == 1 and len(c1["witness"]) == 16
    # re-commit the SAME residue with the carried state -> idempotent, no growth
    c2 = _shell_json({"endpoint": "commit", "x": [0, 0, 0, 1], "lexicon": c1["lexicon"]})
    assert c2["added"] is False and c2["count"] == 1
    # commit a DISTINCT residue (2i) with the state -> grows to 2 (same word, different value)
    c3 = _shell_json({"endpoint": "commit", "x": [0, 0, 0, 2], "lexicon": c2["lexicon"]})
    assert c3["added"] is True and c3["count"] == 2
    # observe under the grown state now reports in_lexicon
    obs2 = _shell_json({"endpoint": "observe", "x": [0, 0, 0, 1], "lexicon": c3["lexicon"]})
    assert obs2["in_lexicon"] is True
    # the lexicon endpoint reflects the grown dictionary
    lx = _shell_json({"endpoint": "lexicon", "lexicon": c3["lexicon"]})
    assert lx["count"] == 2 and len(lx["ids"]) == 2


# --- persist / restore round-trip through the wire --------------------------------------------- #
def test_persist_restore_through_wire(tmp_path):
    c1 = D.dispatch({"endpoint": "commit", "x": [0, 1, 0, 0]})
    c2 = D.dispatch({"endpoint": "commit", "x": [0, 0, 0, 1], "lexicon": c1["lexicon"]})
    path = str(tmp_path / "wire_store.json")
    wrote = _shell_json({"endpoint": "persist", "path": path, "lexicon": c2["lexicon"]})
    assert wrote["wrote"] is True and wrote["count"] == 2 and len(wrote["head"]) == 16
    got = _shell_json({"endpoint": "restore", "path": path})
    assert got["verified"] is True and got["count"] == 2
    assert got["lexicon"] == c2["lexicon"]                     # exact round-trip through the wire
    # tamper -> restore soft-errors (verified False), still no crash
    m = json.loads(open(path, encoding="ascii").read())
    m["records"][0]["value"] = ["0", "1/4", "2/5", "0"]
    open(path, "w", encoding="ascii").write(json.dumps(m))
    bad = _shell_json({"endpoint": "restore", "path": path})
    assert bad["verified"] is False and "error" in bad


# --- firewall on the new verbs ----------------------------------------------------------------- #
def test_new_endpoints_are_computed_never_interpretive():
    for req in ({"endpoint": "render", "x": [0, 0, 0, 1]},
                {"endpoint": "observe", "x": [0, 1, 0, 0]},
                {"endpoint": "propose", "x": [0, 0, 0, 1]},
                {"endpoint": "commit", "x": [0, 0, 0, 1]}):
        out = D.dispatch(req)
        assert out["jurisdiction"] == COMPUTED and out["wired"] is True
        assert out["jurisdiction"] not in (INTERPRETIVE, FALSE_AS_STATED)
    # the law firewall is unchanged: default laws still exclude INTERPRETIVE
    juris = {s["jurisdiction"] for s in D.dispatch({"endpoint": "laws"})["statements"]}
    assert INTERPRETIVE not in juris and FALSE_AS_STATED not in juris


# --- the five existing endpoints remain byte-identical in behavior ----------------------------- #
def test_existing_endpoints_unchanged():
    r = D.dispatch({"endpoint": "read", "x": [0.5, 0.0, 0.5, 0.0]})
    assert r["exact"] is False and r["tol"] == D.READ_TOL and r["gate"] is True and r["rank"] == 1
    assert D.dispatch({"endpoint": "audit", "samples": 64})["closure"] is True
    assert D.dispatch({"endpoint": "bridge"})["agree"] is True
    unknown = D.dispatch({"endpoint": "nope"})
    assert "error" in unknown and "endpoints" in unknown
    # read-exact lives alongside, byte-distinct (exact True):
    assert D.dispatch({"endpoint": "read", "exact": True, "x": [0.5, 0.0, 0.5, 0.0]})["exact"] is True
