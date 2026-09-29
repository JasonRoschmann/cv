"""Prüft die CV-PDFs: 2 Seiten, Pflichtinhalte, Reihenfolge der Projekte, verbotene Aussagen, saubere Textschicht."""
import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
# Poppler aus scoop bevorzugt (xpdf aus Git kennt -bbox nicht), sonst pdftotext aus PATH
_SCOOP = Path(r"C:\Users\Jason Roschmann\scoop\shims\pdftotext.exe")
PDFTOTEXT = str(_SCOOP) if _SCOOP.exists() else "pdftotext"
PDFINFO = "pdfinfo"
KONTAKT = ["jason@roschmann-digital.de", "jasonroschmann.github.io/cv"]
VERBOTEN = ["Commits", "commits", "aktive Mitglieder", "active members", "gewachsen", "grown to", "aufgebaut auf", "nk247"]
REGELN = {
    "Jason_Roschmann_CV_Marketing.pdf": {
        "pflicht": ["Mitgründer", "Outreach", "Stand 29.09.2026", "Junior E-Commerce & Technical SEO", "Begleit-Repositories zu Club-Artikeln",
                    "SEO: Technisches SEO", "Zertifikat: Google Ads", "Weiterbildung: Webentwicklung",
                    "Außendienst (Door-to-Door) 2019 – 2023"],
        "reihenfolge": ["duftkumpels.shop —", "FlowKI Club —", "Flowki Studio —"], "links": ["https://duftkumpels.shop", "https://jasonroschmann.github.io/cv/Jason_Roschmann_Belegmappe.pdf"]},
    "ats-cv/Jason_Roschmann_CV_Marketing_ATS.pdf": {
        "pflicht": ["Mitgründer", "Outreach", "Stand 29.09.2026", "Begleit-Repositories zu Club-Artikeln"],
        "reihenfolge": ["duftkumpels.shop —", "FlowKI Club —", "Flowki Studio —"], "links": ["https://duftkumpels.shop", "https://jasonroschmann.github.io/cv/Jason_Roschmann_Belegmappe.pdf"]},
    "Jason_Roschmann_CV.pdf": {
        "pflicht": ["Mitgründer", "Stand 29.09.2026", "Junior Softwareentwickler", "57 meiner Pull Requests gemergt", "Kundenprojekte 3",
                    "Entwicklung: Python", "Zertifikat: Google Ads", "Weiterbildung: Webentwicklung",
                    "Außendienst (Door-to-Door) 2019 – 2023"],
        "reihenfolge": ["Flowki Studio —", "FlowKI Club —", "duftkumpels.shop —"], "links": ["https://jasonroschmann.github.io/cv/#fs-01", "https://jasonroschmann.github.io/cv/#fs-02", "https://jasonroschmann.github.io/cv/#fs-03", "https://github.com/JasonRoschmann/cv", "https://github.com/Jokersystems-online/flowki-knowledge-mcp"]},
    "ats-cv/Jason_Roschmann_CV_ATS.pdf": {
        "pflicht": ["Mitgründer", "Stand 29.09.2026", "57 meiner Pull Requests gemergt", "Kundenprojekte 3"],
        "reihenfolge": ["Flowki Studio —", "FlowKI Club —", "duftkumpels.shop —"], "links": ["https://jasonroschmann.github.io/cv/#fs-01", "https://jasonroschmann.github.io/cv/#fs-02", "https://jasonroschmann.github.io/cv/#fs-03", "https://github.com/JasonRoschmann/cv", "https://github.com/Jokersystems-online/flowki-knowledge-mcp"]},
    "Jason_Roschmann_CV_EN.pdf": {
        "pflicht": ["Co-founder", "as of 29 Sep 2026", "Junior Software", "57 of my pull requests merged", "client projects 3",
                    "Development: Python", "Certificate: Google Ads", "Training: Web development",
                    "Field sales (door-to-door) 2019 – 2023"],
        "reihenfolge": ["Flowki Studio —", "FlowKI Club —", "duftkumpels.shop —"], "links": ["https://jasonroschmann.github.io/cv/#fs-01", "https://jasonroschmann.github.io/cv/#fs-02", "https://jasonroschmann.github.io/cv/#fs-03", "https://github.com/JasonRoschmann/cv", "https://github.com/Jokersystems-online/flowki-knowledge-mcp"]},
    "ats-cv/Jason_Roschmann_CV_ATS_EN.pdf": {
        "pflicht": ["Co-founder", "as of 29 Sep 2026", "57 of my pull requests merged", "client projects 3"],
        "reihenfolge": ["Flowki Studio —", "FlowKI Club —", "duftkumpels.shop —"], "links": ["https://jasonroschmann.github.io/cv/#fs-01", "https://jasonroschmann.github.io/cv/#fs-02", "https://jasonroschmann.github.io/cv/#fs-03", "https://github.com/JasonRoschmann/cv", "https://github.com/Jokersystems-online/flowki-knowledge-mcp"]},
}


def text(pdf: Path, seite: int = 0) -> str:
    # -layout wie in der Spezifikation (OpenCATS-Methode); der Rohmodus ordnet rechtsbündige Zeiträume unzuverlässig ein.
    bereich = ["-f", str(seite), "-l", str(seite)] if seite else []
    return subprocess.run([PDFTOTEXT, "-layout", "-enc", "UTF-8", *bereich, str(pdf), "-"], capture_output=True, check=True).stdout.decode("utf-8")


def fusszeile_frei(pdf: Path, abstand_pt: float = 8.0) -> list[str]:
    # Druck-Seiten haben feste Höhe mit overflow:hidden: zu viel Text erzeugt keine 3. Seite,
    # sondern läuft in die Fußzeile. Deshalb Abstand zwischen tiefstem Inhalt und Fußzeile messen.
    xml = subprocess.run([PDFTOTEXT, "-bbox", "-enc", "UTF-8", str(pdf), "-"], capture_output=True, check=True).stdout.decode("utf-8")
    return fusszeilen_fehler(xml, abstand_pt)


def fusszeilen_fehler(xml: str, abstand_pt: float = 8.0) -> list[str]:
    fehler = []
    for nr, seite in enumerate(xml.split("<page ")[1:], 1):
        w = [(float(a), float(b), s) for a, b, s in re.findall(r'yMin="([\d.]+)" xMax="[\d.]+" yMax="([\d.]+)">([^<]*)<', seite)]
        # Fußzeile = Wörter mit exakt derselben Grundlinie und Schrifthöhe wie "Seite"/"Page"; alles andere
        # ist Inhalt – auch eine Inhaltszeile, die auf Höhe der Fußzeile mit ihr kollidiert
        fy, fb = max((a, b) for a, b, s in w if s in ("Seite", "Page"))
        tief = max(b for a, b, s in w if abs(a - fy) > 0.05 or abs(b - fb) > 0.05)
        if tief > fy - abstand_pt:
            fehler.append(f"Seite {nr}: Inhalt reicht an/unter die Fußzeile ({fy - tief:.1f} pt)")
    return fehler


def links(pdf: Path) -> str:
    # Klickbare Belege: Link-Ziele aus den PDF-Annotationen, nicht aus dem sichtbaren Text
    return subprocess.run([PDFINFO, "-url", str(pdf)], capture_output=True, check=True).stdout.decode("utf-8", "replace")


def seiten(pdf: Path) -> int:
    out = subprocess.run([PDFINFO, str(pdf)], capture_output=True, check=True).stdout.decode("utf-8", "replace")
    return int(next(z.split()[-1] for z in out.splitlines() if z.startswith("Pages:")))


def pruefe(pdf: Path, regel: dict) -> list[str]:
    fehler = []
    if (n := seiten(pdf)) != 2:
        fehler.append(f"{n} Seiten statt 2")
    t = " ".join(text(pdf).split())
    fehler += [f"fehlt: {p}" for p in regel["pflicht"] + KONTAKT if p not in t]
    fehler += [f"verboten: {v}" for v in VERBOTEN if v in t]
    ziele = links(pdf)
    fehler += [f"Link fehlt: {u}" for u in regel["links"] if u not in ziele]
    if "_ATS" not in pdf.stem:  # nur Druck-PDFs haben die Fußzeile
        fehler += fusszeile_frei(pdf)
    if any(chr(c) in t for c in range(0xFB00, 0xFB07)) or "\ufffd" in t:
        fehler.append("Ligatur oder Ersatzzeichen in der Textschicht")
    # Eine Tools-Zeile gehört zu ihrem Eintrag; allein oben auf Seite 2 ist sie verwaist.
    if " ".join(text(pdf, 2).split()).startswith("Tools:"):
        fehler.append("Tools-Zeile verwaist oben auf Seite 2")
    pos = [t.find(m) for m in regel["reihenfolge"]]
    if -1 in pos or pos != sorted(pos):
        fehler.append(f"Reihenfolge falsch: {dict(zip(regel['reihenfolge'], pos))}")
    return fehler


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf-dir", type=Path, default=REPO, help="Ersatzort für gesperrte PDFs (gleiche Dateinamen)")
    args = ap.parse_args()
    rot = False
    for name, regel in REGELN.items():
        ersatz = args.pdf_dir / Path(name).name
        pdf = ersatz if ersatz.exists() else REPO / name
        fehler = pruefe(pdf, regel)
        rot |= bool(fehler)
        quelle = "" if pdf == REPO / name else f"  [geprüft: {pdf}]"
        print(("ROT  " if fehler else "GRÜN ") + name + quelle + "".join("\n     - " + f for f in fehler))
    return 1 if rot else 0


if __name__ == "__main__":
    sys.exit(main())
