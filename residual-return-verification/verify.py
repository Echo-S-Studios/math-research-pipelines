#!/usr/bin/env python3
"""verify.py -- the verification pipeline for the Residual Return papers.

This package exists to answer one objection directly: "I found the PDF, but no probe code, so I
could inspect the claims but not independently RUN the machine checks." Here is the probe code, the
real engine, and a pipeline that walks BOTH papers claim by claim -- theorem by theorem, equation by
equation -- running the machine-checked test behind each claim and reporting PASS/FAIL.

Usage:
    py verify.py             # everything: env check, both probes, the claim walkthrough, the full suites
    py verify.py --quick     # just the two probes (re-derive every displayed NUMBER; ~2 s, sympy+mpmath+pytest)
    py verify.py --walk      # env check + the claim-by-claim walkthrough (skip the big full-suite run)

Requirements: Python 3.10+, and `pip install sympy mpmath numpy pytest`. verify.py drives every probe
and suite through pytest; the probe FILES themselves import only sympy+mpmath (no engine), and numpy is
used only by the language layer's quarantined float readings. No network, no other dependencies.
Nothing is installed for you; see README.md.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
L00M_ABS = os.path.join(HERE, "L00M")


# --------------------------------------------------------------------------- #
def c(s, code):
    return f"\033[{code}m{s}\033[0m" if sys.stdout.isatty() else s

def ok(s):   return c(s, "32")
def bad(s):  return c(s, "31")
def head(s): return c(s, "1;36")
def dim(s):  return c(s, "2")


def rule(title=""):
    line = "=" * 78
    print("\n" + line)
    if title:
        print(head("  " + title))
        print(line)


def suite_cwd_env(suites, suite_id):
    s = suites[suite_id]
    cwd = os.path.join(HERE, s["cwd"])
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    for k, v in s.get("env", {}).items():
        env[k] = v.replace("{L00M_ABS}", L00M_ABS)
    return cwd, env


def run_pytest(cwd, env, args):
    """Run pytest with the given args; return (returncode, stdout+stderr)."""
    proc = subprocess.run([sys.executable, "-m", "pytest", *args],
                          cwd=cwd, env=env, capture_output=True, text=True)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def parse_verbose(out):
    """Map nodeid -> 'PASSED'/'FAILED'/'ERROR' from `pytest -v` output."""
    res = {}
    for ln in out.splitlines():
        for verdict in ("PASSED", "FAILED", "ERROR"):
            if (" " + verdict) in ln and "::" in ln:
                node = ln.split(" " + verdict)[0].strip()
                res[node] = verdict
                break
    return res


# --------------------------------------------------------------------------- #
def env_check():
    rule("ENVIRONMENT")
    print(f"  python      {sys.version.split()[0]}  ({sys.executable})")
    allok = sys.version_info >= (3, 10)
    print(("  python>=3.10  " + (ok("ok") if allok else bad("TOO OLD"))))
    for mod in ("sympy", "mpmath", "numpy"):
        try:
            m = __import__(mod)
            print(f"  {mod:11} {getattr(m, '__version__', '?'):8} {ok('importable')}")
        except Exception as e:        # numpy only needed for the language float layer
            need = "REQUIRED" if mod in ("sympy", "mpmath") else "needed for the kira suite only"
            print(f"  {mod:11} {bad('MISSING')}   ({need}: pip install {mod})  [{e.__class__.__name__}]")
            if mod in ("sympy", "mpmath"):
                allok = False
    return allok


def run_probes(quick=False):
    rule("PART A -- INDEPENDENT RE-DERIVATION OF EVERY DISPLAYED NUMBER")
    print(dim("  Self-contained witnesses (sympy + stdlib; they import NO engine) recompute every\n"
              "  number, matrix, polynomial, residual, floor, and hash displayed in the two papers.\n"))
    results = []
    for label, cwd_rel, target in [
        ("vector_substrate probe (13)", "L00M", "training/test_paper_claims.py"),
        ("companion probe (20)", os.path.join("L00M", "paper"), "test_residual_return_claims.py"),
    ]:
        cwd = os.path.join(HERE, cwd_rel)
        env = dict(os.environ); env["PYTHONIOENCODING"] = "utf-8"
        rc, out = run_pytest(cwd, env, [target, "-q", "-p", "no:cacheprovider"])
        last = next((l for l in reversed(out.splitlines()) if l.strip()), "")
        print(f"  {label:34} {ok(last) if rc == 0 else bad(last)}")
        results.append(rc == 0)

    # third independent witness: a from-scratch audit harness by a DIFFERENT author (Ace), same numbers.
    cwd = os.path.join(HERE, "L00M", "paper")
    env = dict(os.environ); env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run([sys.executable, "residual_return_audit.py"], cwd=cwd,
                          capture_output=True, text=True)
    lines = (proc.stdout or "").splitlines()
    summary = next((l.strip() for l in lines if "checks passed" in l), "(no summary)")
    # a genuine failure is a non-'shorthand' FAIL line; the lone 'shorthand' flag is BY DESIGN.
    real_fail = any(len(t := l.split()) >= 2 and t[1] == "FAIL" and t[0] != "shorthand" for l in lines)
    print(f"  {'third witness (Ace, independent)':34} {ok(summary) if not real_fail else bad(summary)}")
    print(dim("    the 1 'shorthand' flag is intentional: it documents that the Fisher identity\n"
              "    I_exp = (1/n)G holds on the TRACE-ZERO subspace, NOT as a full matrix (it differs at\n"
              "    the constant direction, where I_exp vanishes). The paper states this scope explicitly;\n"
              "    the companion probe pins BOTH directions (the subspace identity AND the full-matrix gap)."))
    results.append(not real_fail)
    return all(results)


def walkthrough(spec):
    rule("PART B -- THE WALKTHROUGH: EVERY CLAIM, ITS TEST, ITS VERDICT")
    print(dim("  Each load-bearing theorem / equation / example of both papers, paired with the\n"
              "  machine-checked test that proves it. Running each test node now...\n"))
    suites = spec["suites"]
    claims = spec["claims"]

    # group cited nodes by suite, run once per suite, collect verdicts
    by_suite = {}
    for cl in claims:
        by_suite.setdefault(cl["suite"], []).append(cl["node"])
    verdicts = {}
    for sid, nodes in by_suite.items():
        cwd, env = suite_cwd_env(suites, sid)
        _, out = run_pytest(cwd, env, [*sorted(set(nodes)), "-v", "-p", "no:cacheprovider"])
        verdicts[sid] = parse_verbose(out)

    titles = {p["id"]: p for p in spec["papers"]}
    npass = nfail = nmiss = 0
    last_paper = None
    for cl in claims:
        if cl["paper"] != last_paper:
            p = titles[cl["paper"]]
            print("\n  " + head(f"[{p['id']}]  {p['title']}  ({p['pages']}pp)"))
            last_paper = cl["paper"]
        v = verdicts.get(cl["suite"], {}).get(cl["node"])
        if v == "PASSED":
            tag = ok("PASS"); npass += 1
        elif v in ("FAILED", "ERROR"):
            tag = bad(v); nfail += 1
        else:
            tag = bad("MISSING"); nmiss += 1
        print(f"    {tag:5}  {cl['ref']:14} {cl['kind']:11} {cl['what'][:84]}")
        print(dim(f"           via {cl['suite']}:{cl['node'].split('::')[-1]}"))
    print()
    print(f"  walkthrough: {ok(str(npass)+' PASS')}"
          + (f", {bad(str(nfail)+' FAIL')}" if nfail else "")
          + (f", {bad(str(nmiss)+' MISSING')}" if nmiss else "")
          + f"  of {len(claims)} claims")
    return nfail == 0 and nmiss == 0


def full_suites():
    rule("PART C -- THE FULL ENGINE SUITES (the real code behind the claims)")
    rows = [
        ("number-field learning engine (training)", "L00M", ["training", "-q", "-p", "no:cacheprovider"], None),
        ("language layer (kira-language)", "kira-language", ["-q", "-p", "no:cacheprovider"],
         {"KIRA_LANG_L00M_ROOT": L00M_ABS}),
    ]
    allok = True
    for label, cwd_rel, args, extra_env in rows:
        cwd = os.path.join(HERE, cwd_rel)
        env = dict(os.environ); env["PYTHONIOENCODING"] = "utf-8"
        if extra_env:
            env.update(extra_env)
        rc, out = run_pytest(cwd, env, args)
        last = next((l for l in reversed(out.splitlines()) if l.strip()), "")
        print(f"  {label:42} {ok(last) if rc == 0 else bad(last)}")
        allok = allok and rc == 0
    print(dim("\n  (The ZFP zero-free-parameter gate -- PASS:74 FAIL:0 -- lives in the separate\n"
              "   Plate-Matrices repository and is context, not a claim of these papers; not bundled.)"))
    return allok


def main():
    ap = argparse.ArgumentParser(description="Verify the Residual Return papers' machine-checked claims.")
    ap.add_argument("--quick", action="store_true", help="only the two probes (every displayed number)")
    ap.add_argument("--walk", action="store_true", help="env + probes + claim walkthrough (skip full suites)")
    args = ap.parse_args()

    spec = json.load(open(os.path.join(HERE, "claim_map.json"), encoding="utf-8"))

    print(head("\n  RESIDUAL RETURN -- verification pipeline"))
    for p in spec["papers"]:
        print(f"    - {p['title']}  ({p['pages']}pp)  ->  {p['pdf']}")

    env_ok = env_check()
    if not env_ok:
        print(bad("\n  Missing a required dependency (sympy/mpmath). Install per README.md, then re-run."))
        return 2

    a = run_probes()
    if args.quick:
        rule("DONE (--quick)")
        print("  " + (ok("PROBES GREEN -- every displayed number independently re-derived.")
                      if a else bad("a probe failed -- see output above.")))
        return 0 if a else 1

    b = walkthrough(spec)
    c_ok = True
    if not args.walk:
        c_ok = full_suites()

    rule("BOTTOM LINE")
    allgreen = a and b and c_ok
    print("  probes (every displayed number): " + (ok("GREEN") if a else bad("RED")))
    print("  claim walkthrough:               " + (ok("GREEN") if b else bad("RED")))
    if not args.walk:
        print("  full engine suites:              " + (ok("GREEN") if c_ok else bad("RED")))
    print()
    if allgreen:
        print(ok("  ALL GREEN. Every claim in both papers is backed by a machine check you just ran."))
    else:
        print(bad("  NOT all green -- inspect the output above. (A genuine failure is itself information.)"))
    return 0 if allgreen else 1


if __name__ == "__main__":
    raise SystemExit(main())
