#!/usr/bin/env python3
"""Erzeugt Jason_Roschmann_CV.pdf aus cv-print.html.

Warum es das gibt: Am 22.09.2026 war das zum Download verlinkte PDF Monate
aelter als die Seite. Es trug die tote Adresse jason@roschmann-digital.de,
"Hamburg -> Zuerich", "in Produktion" und die nachweislich falsche Aussage,
die Bewerbungs-Fabrik reiche "autonom ueber Portale und E-Mail ein". Wer auf
"CV herunterladen" klickte, bekam genau das. Ohne Build-Schritt passiert das
wieder.

Aufruf:  py -3 scripts/build_cv_pdf.py
"""
import http.server
import socketserver
import subprocess
import sys
import threading
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
QUELLE = "cv-print.html"
ZIEL = REPO / "Jason_Roschmann_CV.pdf"
PORT = 8913
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def main() -> int:
    if not (REPO / QUELLE).exists():
        print("FEHLER:", QUELLE, "fehlt"); return 1

    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(
        *a, directory=str(REPO), **k)
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        # Ueber HTTP statt file://, damit Schriften und Bilder wirklich laden.
        subprocess.run(
            [EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer",
             "--print-to-pdf=" + str(ZIEL),
             "http://127.0.0.1:%d/%s" % (PORT, QUELLE)],
            check=True, timeout=120)
    finally:
        server.shutdown()

    if not ZIEL.exists():
        print("FEHLER: kein PDF erzeugt"); return 1
    roh = ZIEL.read_bytes()
    print("PDF:", ZIEL.name, len(roh), "Bytes")
    # Grobe Plausibilitaet: ein leeres oder Fehlerseiten-PDF ist winzig.
    if len(roh) < 20_000:
        print("FEHLER: PDF verdaechtig klein - vermutlich Fehlerseite gerendert")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
