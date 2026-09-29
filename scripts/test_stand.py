"""Selbsttest des Stempels: py -3 scripts/test_stand.py"""
import re

from stand import werte, stempel_text, diagramm, badge, veraltet, fehlende_marker

D = {"version": 1, "stand": "2026-09-30T05:40:00Z", "zahlen_stand": "2026-09-29T18:00:00Z",
     "gemergt": {"gesamt": 59, "flowki": 50, "eigen": 6, "kunden": 3, "weitere": 0},
     "eroeffnet": {"flowki": 64}, "erster_merge": "2026-08-07",
     "verlauf": [["2026-08-07", 1], ["2026-08-09", 4], ["2026-09-29", 59]]}


def test_werte_web_nutzen_stand_druck_nutzen_zahlen_stand():
    assert werte(D, druck=False)["stand-de"] == "30.09.2026"
    assert werte(D, druck=True)["stand-de"] == "29.09.2026"
    assert werte(D, druck=True)["stand-en"] == "29 Sep 2026"
    assert werte(D, druck=False)["seit-de"] == "Aug. 2026" and werte(D, druck=False)["seit-en"] == "Aug 2026"


def test_spans_flex_und_js_werden_gesetzt():
    t = ('<b><span data-pr="gesamt">58</span></b> <i data-pr-flex="eigen" style="flex:5"></i>'
         'var PR=/*pr-daten*/{"gesamt":1}/*pr-daten-ende*/;')
    neu = stempel_text(t, werte(D, druck=True), D)
    assert '<span data-pr="gesamt">59</span>' in neu
    assert 'data-pr-flex="eigen" style="flex:6"' in neu
    assert '/*pr-daten*/{"gesamt": 59, "flowki": 50, "eigen": 6, "kunden": 3, "flowkiEroeffnet": 64}/*pr-daten-ende*/' in neu


def test_stempeln_ist_idempotent():
    t = '<span data-pr="flowki">1</span><!-- pr-diagramm:start --><!-- pr-diagramm:end -->'
    einmal = stempel_text(t, werte(D, druck=False), D)
    assert stempel_text(einmal, werte(D, druck=False), D) == einmal


def test_unbekannter_schluessel_ist_fehler():
    try:
        stempel_text('<span data-pr="erfunden">1</span>', werte(D, druck=False), D)
    except KeyError:
        return
    raise AssertionError("unbekannter Schlüssel wurde still übergangen")


def test_diagramm_enthaelt_endwert_und_beschriftung():
    svg = diagramm(D)
    assert "59" in svg and "aria-label" in svg and "Flowki Studio 50" in svg
    assert "<script" not in svg


def test_badge_zeigt_gesamtzahl():
    assert ">59<" in badge(D)


def test_frische():
    assert veraltet(D, tage=3, heute="2026-10-04") and not veraltet(D, tage=3, heute="2026-10-02")
    assert veraltet(D, tage=3, heute="2026-09-28")   # Stand in der Zukunft = von Hand gesetzt, unplausibel


def test_endzahl_passt_auch_dreistellig_ins_diagramm():
    d = {**D, "gemergt": {**D["gemergt"], "gesamt": 999}, "verlauf": [["2026-08-07", 1], ["2026-09-29", 999]]}
    x = float(re.search(r'<text x="([\d.]+)" y="[\d.]+" class="end">', diagramm(d)).group(1))
    assert x + 3 * 0.6 * 26 <= 640   # mobil 26 SVG-Einheiten Schrift, Monospace ~0,6 em je Ziffer


def test_fehlende_marker_werden_gemeldet():
    voll = ('<span data-pr="gesamt">1</span><span data-pr="flowki">1</span><span data-pr="flowki-eroeffnet">1</span>'
            '<span data-pr="stand-de">x</span><span data-pr="seit-de">x</span>/*pr-daten*/{}/*pr-daten-ende*/'
            '<!-- pr-diagramm:start --><!-- pr-diagramm:end -->')
    assert fehlende_marker("index.html", voll) == []
    assert fehlende_marker("index.html", voll.replace('data-pr="gesamt"', 'class="x" data-pr="gesamt"'))
    assert fehlende_marker("index.html", voll.replace("<!-- pr-diagramm:end -->", ""))
    assert fehlende_marker("cv-print.html", "58 meiner Pull Requests") and not fehlende_marker("cv-print.html", voll)


if __name__ == "__main__":
    rot = 0
    for name, f in list(globals().items()):
        if name.startswith("test_"):
            try:
                f(); print("OK  ", name)
            except AssertionError as e:
                rot += 1; print("FAIL", name, e)
    raise SystemExit(1 if rot else 0)
