"""`py -m kira_language` -- the KIRA shell entry.

ASCII/cp1252-safe stdout (so KIRA can shell it RAW, without PYTHONUTF8) + the dispatch loop:
one JSON request on stdin -> one JSON result on stdout. Import-safe (guarded): importing this
module runs nothing.
"""
from kira_language import dispatch, portable_io


def main() -> None:
    portable_io.install()        # ASCII-safe stdout (belt-and-suspenders; dispatch JSON is ensure_ascii too)
    dispatch.main()


if __name__ == "__main__":
    main()
