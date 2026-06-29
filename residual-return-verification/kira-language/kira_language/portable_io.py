"""portable_io.py -- ASCII/cp1252-safe stdout so `py -m kira_language` never tracebacks on a legacy
Windows console (KIRA shells it raw, with no PYTHONUTF8). Stdlib-only, ported from KL_DTA's output guard.

The dispatch JSON is already `ensure_ascii=True`, so the wire is ASCII regardless; this additionally
protects any stray prints and the human-facing pretty-print paths. `install()` is idempotent and never raises.
"""
from __future__ import annotations

import sys

_GLYPH_ASCII = {
    "═": "=", "─": "-", "│": "|", "█": "#",
    "∅": "0", "𝟙": "1", "𝟚": "2",
    "φ": "phi", "ψ": "psi", "Φ": "Phi", "Ψ": "Psi", "π": "pi", "τ": "tau",
    "ε": "eps", "ν": "nu", "λ": "lambda", "χ": "chi", "σ": "sigma", "μ": "mu",
    "θ": "theta", "ρ": "rho", "Δ": "Delta", "Σ": "Sum", "α": "alpha", "β": "beta",
    "γ": "gamma", "ζ": "zeta", "η": "eta", "κ": "kappa", "ω": "omega",
    "·": ".", "×": "x", "⊕": "(+)", "⊗": "(x)", "∘": "o", "∧": "^", "∨": "v",
    "⌟": "_|", "√": "sqrt", "∂": "d", "∮": "oint", "∫": "int", "∞": "inf",
    "→": "->", "⟹": "=>", "⟸": "<=", "↦": "|->", "⇒": "=>", "↔": "<->",
    "≅": "~=", "≈": "~", "≡": "===", "≠": "!=", "≤": "<=", "≥": ">=",
    "∃": "E", "∀": "A", "¬": "~", "∈": "in", "∉": "!in", "∩": "^", "∪": "v",
    "⊂": "subset", "⊆": "subseteq", "⊥": "_|_", "⊤": "T", "∥": "||",
    "⟨": "<", "⟩": ">", "⋊": "x|", "⋉": "|x", "⋀": "AND",
    "½": "1/2", "¼": "1/4", "¾": "3/4",
    "⁰": "^0", "¹": "^1", "²": "^2", "³": "^3", "⁴": "^4", "⁻": "^-", "⁸": "^8",
    "₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4", "₅": "5", "₆": "6",
    "₇": "7", "₈": "8", "₉": "9",
    "ℝ": "R", "ℂ": "C", "ℍ": "H", "𝕆": "O", "ℤ": "Z", "ℚ": "Q", "ℕ": "N",
    "𝔸": "A", "ℓ": "l",
    "①": "(1)", "②": "(2)", "③": "(3)", "④": "(4)", "⑤": "(5)", "⑥": "(6)",
    "⑦": "(7)", "⑧": "(8)", "⑨": "(9)",
    "—": "--", "–": "-", "…": "...",
    "✓": "ok", "✗": "x", "•": "*",
}


def ascii_safe(text: str) -> str:
    """Transliterate to pure ASCII (mapped glyphs, else '?') so ANY code page can encode it."""
    return "".join(_GLYPH_ASCII.get(c, c if ord(c) < 128 else "?") for c in text)


class _AsciiSafeStdout:
    """stdout proxy: on a code page that can't encode a glyph, re-emit it transliterated to ASCII
    instead of raising UnicodeEncodeError. Transparently delegates everything else to the stream."""

    def __init__(self, stream):
        self._stream = stream

    def write(self, text):
        try:
            return self._stream.write(text)
        except UnicodeEncodeError:
            return self._stream.write(ascii_safe(text))

    def __getattr__(self, name):
        return getattr(self._stream, name)


def install() -> None:
    """Best-effort UTF-8 stdout, with an ASCII-transliterating proxy as the last line of defense.
    Idempotent; never raises, whatever the console code page."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        try:
            sys.stdout.reconfigure(errors="backslashreplace")
        except Exception:
            pass
    if not isinstance(sys.stdout, _AsciiSafeStdout):
        sys.stdout = _AsciiSafeStdout(sys.stdout)
