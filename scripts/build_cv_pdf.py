#!/usr/bin/env python3
"""Erzeugt Jason_Roschmann_CV.pdf (DE) und _EN.pdf aus cv-print*.html und die ATS-Fassungen
(txt, docx, pdf) aus ats-cv/*.md.

Warum es das gibt: Am 22.09.2026 war das zum Download verlinkte PDF Monate
aelter als die Seite. Es trug "Hamburg -> Zuerich", "in Produktion" und die
nachweislich falsche Aussage, die Bewerbungs-Fabrik reiche "autonom ueber
Portale und E-Mail ein". Wer auf "CV herunterladen" klickte, bekam genau das.
Ohne Build-Schritt passiert das wieder - auch bei den ATS-Dateien, die bis
28.09.2026 von Hand erzeugt wurden und der Markdown-Quelle hinterherhingen.

Aufruf:  py -3 scripts/build_cv_pdf.py      (braucht Edge und pandoc)
"""
import http.server
import socketserver
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DRUCK = [("cv-print.html", REPO / "Jason_Roschmann_CV.pdf"), ("cv-print-en.html", REPO / "Jason_Roschmann_CV_EN.pdf"),
         ("cv-print-marketing.html", REPO / "Jason_Roschmann_CV_Marketing.pdf"),
         ("cv-belegmappe.html", REPO / "Jason_Roschmann_Belegmappe.pdf")]
ATS = [REPO / "ats-cv" / "Jason_Roschmann_CV_ATS.md", REPO / "ats-cv" / "Jason_Roschmann_CV_ATS_EN.md",
       REPO / "ats-cv" / "Jason_Roschmann_CV_Marketing_ATS.md"]
ATS_STIL = """<style>
@page { size: A4; margin: 12mm 15mm }
html, body { font-family: Arial, Helvetica, sans-serif; font-size: 10pt; line-height: 1.25; max-width: none; padding: 0; margin: 0 }
@media print { body { font-size: 10pt } }
h1 { font-size: 19pt; margin: 0 0 3pt } h2 { font-size: 12.5pt; margin: 9pt 0 3pt; padding-bottom: 2pt; border-bottom: 1px solid #999; break-after: avoid }
h2 + p { break-after: avoid } ul + p { break-before: avoid }
h3 { font-size: 10.5pt; margin: 8pt 0 2pt; break-after: avoid } p, li { margin: 2pt 0; break-inside: avoid } ul { padding-left: 15pt; margin: 2pt 0 }
</style>
"""
PORT = 8913
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def drucke(url: str, ziel: Path, mindestgroesse: int) -> None:
    """Druckt url per Edge nach ziel; wirft, wenn kein frisches, plausibles PDF entsteht."""
    # Altes PDF weg: Am 28.09.2026 meldete ein Lauf Erfolg, obwohl Edge den Druck an eine noch
    # laufende Instanz abgegeben und nichts geschrieben hatte - geprueft wurde das alte PDF.
    ziel.unlink(missing_ok=True)
    # Eigenes Profil, damit Edge den Auftrag nicht an ein schon laufendes Fenster weiterreicht.
    subprocess.run(
        [EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer",
         "--user-data-dir=" + tempfile.mkdtemp(prefix="cvpdf_edge_"),
         "--print-to-pdf=" + str(ziel), url],
        check=True, timeout=120)
    if not ziel.exists():
        raise RuntimeError("kein PDF erzeugt: %s" % ziel.name)
    groesse = ziel.stat().st_size
    print("PDF:", ziel.name, groesse, "Bytes")
    # Grobe Plausibilitaet: ein leeres oder Fehlerseiten-PDF ist winzig.
    if groesse < mindestgroesse:
        raise RuntimeError("%s verdaechtig klein - vermutlich Fehlerseite gerendert" % ziel.name)


def druck_cv() -> None:
    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(
        *a, directory=str(REPO), **k)
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        # Ueber HTTP statt file://, damit Schriften und Bilder wirklich laden.
        for quelle, ziel in DRUCK:
            drucke("http://127.0.0.1:%d/%s" % (PORT, quelle), ziel, 20_000)
    finally:
        server.shutdown()


def ats(md: Path) -> None:
    """md -> txt, docx und (ueber HTML) pdf daneben, gleicher Dateiname."""
    pandoc = ["pandoc", str(md), "--from", "markdown"]
    subprocess.run(pandoc + ["-t", "plain", "-o", str(md.with_suffix(".txt"))], check=True)
    # Eine gerade geschriebene .docx haelt Windows (Scanner/Indexer) kurz offen; Ueberschreiben scheitert dann sporadisch.
    for _ in range(3):
        if subprocess.run(pandoc + ["-o", str(md.with_suffix(".docx"))]).returncode == 0:
            break
        time.sleep(3)
    else:
        raise RuntimeError("DOCX-Erzeugung nach drei Versuchen fehlgeschlagen: %s" % md.with_suffix(".docx").name)
    with tempfile.TemporaryDirectory(prefix="cv_ats_") as tmp:
        html, stil = Path(tmp) / (md.stem + ".html"), Path(tmp) / "stil.html"
        # pandocs Vorlage druckt mit 12pt und schmaler Spalte -> 4 Seiten; schlicht und dicht bleibt es ATS-lesbar
        stil.write_text(ATS_STIL, encoding="utf-8")
        subprocess.run(pandoc + ["-s", "--metadata", "pagetitle=" + md.stem, "-H", str(stil), "-o", str(html)], check=True)
        drucke(html.as_uri(), md.with_suffix(".pdf"), 5_000)
    print("ATS:", md.stem, "txt/docx/pdf")


def main() -> int:
    for pfad in [REPO / q for q, _ in DRUCK] + [REPO / "cv-print.css", REPO / "cv-v4.css"] + ATS:
        if not pfad.exists():
            print("FEHLER:", pfad.name, "fehlt"); return 1
    try:
        druck_cv()
        for md in ATS:
            ats(md)
    except (RuntimeError, subprocess.SubprocessError) as ex:
        print("FEHLER:", ex); return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
