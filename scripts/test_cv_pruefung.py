"""Selbsttest der Fußzeilenprüfung mit synthetischer pdftotext-bbox-Ausgabe: py -3 scripts/test_cv_pruefung.py"""
from cv_pruefung import fusszeilen_fehler


def wort(y_min: float, y_max: float, text: str) -> str:
    return f'<word xMin="50.0" yMin="{y_min}" xMax="90.0" yMax="{y_max}">{text}</word>'


FUSS = [wort(800.0, 807.0, "Jason"), wort(800.0, 807.0, "Seite"), wort(800.0, 807.0, "1/2")]


def seite(*worte: str) -> str:
    return '<doc><page width="595" height="842">' + "".join(worte) + "</page></doc>"


def test_inhalt_mit_abstand_ist_ok():
    assert fusszeilen_fehler(seite(wort(700.0, 710.0, "Inhalt"), *FUSS)) == []


def test_inhalt_knapp_ueber_fusszeile_wird_gemeldet():
    assert len(fusszeilen_fehler(seite(wort(785.0, 795.0, "Inhalt"), *FUSS))) == 1


def test_inhalt_auf_hoehe_der_fusszeile_wird_gemeldet():
    # Inhaltszeile kollidiert genau mit der Fußzeile, darüber viel Luft (z. B. nach einem Abschnittsabstand)
    assert len(fusszeilen_fehler(seite(wort(700.0, 710.0, "Inhalt"), wort(800.5, 810.5, "Kollision"), *FUSS))) == 1


if __name__ == "__main__":
    rot = 0
    for name, f in list(globals().items()):
        if name.startswith("test_"):
            try:
                f(); print("OK  ", name)
            except AssertionError:
                rot += 1; print("FAIL", name)
    raise SystemExit(1 if rot else 0)
