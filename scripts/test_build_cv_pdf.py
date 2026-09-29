"""Selbsttest der Eingangs-Prüfsumme und Browserwahl: py -3 scripts/test_build_cv_pdf.py"""
import tempfile
from pathlib import Path

import build_cv_pdf as b


def test_hash_ist_stabil_und_browser_gefunden():
    h1 = b.quellen_hash()
    assert h1 == b.quellen_hash() and len(h1) == 64
    assert b.browser() and ("msedge" in b.browser() or "chrome" in b.browser() or "chromium" in b.browser())


def test_hash_gleich_bei_crlf_und_lf_aber_neu_bei_inhalt():
    # Windows checkt mit CRLF aus, die CI mit LF: gleicher Inhalt muss gleichen Hash geben
    with tempfile.TemporaryDirectory() as tmp:
        basis = Path(tmp)
        for name in b.QUELLEN:
            (basis / name).parent.mkdir(parents=True, exist_ok=True)
            (basis / name).write_bytes(b"a\nb\n")
        lf = b.quellen_hash(basis)
        for name in b.QUELLEN:
            (basis / name).write_bytes(b"a\r\nb\r\n")
        assert b.quellen_hash(basis) == lf
        (basis / b.QUELLEN[0]).write_bytes(b"a\r\nc\r\n")
        assert b.quellen_hash(basis) != lf


if __name__ == "__main__":
    rot = 0
    for name, f in list(globals().items()):
        if name.startswith("test_"):
            try:
                f(); print("OK  ", name)
            except AssertionError as e:
                rot += 1; print("FAIL", name, e)
    raise SystemExit(1 if rot else 0)
