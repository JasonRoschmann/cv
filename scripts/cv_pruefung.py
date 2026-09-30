"""Prüft die CV-PDFs: 2 Seiten, Pflichtinhalte, Reihenfolge der Projekte, verbotene Aussagen, saubere Textschicht."""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
# Poppler aus scoop bevorzugt (xpdf aus Git kennt -bbox nicht), sonst pdftotext aus PATH
_SCOOP = Path(r"C:\Users\Jason Roschmann\scoop\shims\pdftotext.exe")
PDFTOTEXT = str(_SCOOP) if _SCOOP.exists() else "pdftotext"
PDFINFO = "pdfinfo"
PDFFONTS = "pdffonts"
PR_STAND = REPO / "pr-stand.json"   # Sollwerte der PR-Zahlen (täglich vom Zähler), nie von Hand
KONTAKT = ["jason@roschmann-digital.de", "jasonroschmann.github.io/cv"]
VERBOTEN = ["Commits", "commits", "aktive Mitglieder", "active members", "gewachsen", "grown to", "aufgebaut auf", "nk247", "Produktteam", "product team", "Hamburg oder remote", "Hamburg or remote", "Hamburg · remote"]
REGELN = {
    # Belegmappe: 2 Seiten, drei Fälle in Reihenfolge, Schlussband mit Abstand zur Fußzeile
    "Jason_Roschmann_Belegmappe.pdf": {
        "pflicht": ["Fall 1", "Fall 2", "Fall 3", "Bereinigte Auszüge"],
        "reihenfolge": ["Fall 1", "Fall 2", "Fall 3"], "links": ["https://jasonroschmann.github.io/cv/"], "pr": None, "schriften": ["Fraunces", "JetBrainsMono"]},
    # v6: Stationen statt Einzelprojekte – Mitgründer zuerst (jüngste Station, Hauptprojekt), dann die freiberufliche
    # Station mit ihren Mandaten; Pflichttexte sichern Rollentitel, Station, Zeitraum und Vertrieb
    "Jason_Roschmann_CV_Marketing.pdf": {
        "pflicht": ["Mitgründer", "Outreach", "Stand 29.09.2026", "2024 – heute", "E-Commerce & Technical SEO · Marketing-Automation", "Remote · Zürich",
                    "Freiberuflich: Web, E-Commerce & Technical SEO", "Begleit-Repositories zu Club-Artikeln",
                    "SEO: Technisches SEO", "Zertifikat: Google Ads", "Weiterbildung: Webentwicklung",
                    "Außendienst B2B-Direktvertrieb", "2019 – 2023", "Nächster Schritt"],
        "reihenfolge": ["Mitgründer —", "duftkumpels.shop —", "Flowki Studio —"], "links": ["https://duftkumpels.shop", "https://jasonroschmann.github.io/cv/Jason_Roschmann_Belegmappe.pdf"],
        "pr": "marketing", "schriften": ["Inter", "IBMPlexMono"]},
    "ats-cv/Jason_Roschmann_CV_Marketing_ATS.pdf": {
        "pflicht": ["Mitgründer", "Outreach", "Stand 29.09.2026", "2024 – heute", "Freiberuflich: Web, E-Commerce & Technical SEO", "Begleit-Repositories zu Club-Artikeln", "vor Ort in Zürich"],
        "reihenfolge": ["Mitgründer —", "duftkumpels.shop —", "Flowki Studio —"], "links": ["https://duftkumpels.shop", "https://jasonroschmann.github.io/cv/Jason_Roschmann_Belegmappe.pdf"],
        "pr": "marketing", "schriften": []},
    "Jason_Roschmann_CV.pdf": {
        "pflicht": ["Mitgründer", "Stand 29.09.2026", "Softwareentwickler · KI-Automation & E-Commerce", "Freiberuflicher Softwareentwickler", "Remote · Zürich", "Node.js", "React Native", "RAG-Muster",
                    "Backend & APIs: Python", "2024 – heute", "Zertifikat: Google Ads", "Weiterbildung: Webentwicklung",
                    "Außendienst B2B-Direktvertrieb", "2019 – 2023", "Nächster Schritt"],
        "reihenfolge": ["Mitgründer —", "Flowki Studio —", "duftkumpels.shop —"], "links": ["https://jasonroschmann.github.io/cv/#fs-01", "https://jasonroschmann.github.io/cv/#fs-03", "https://github.com/JasonRoschmann/cv", "https://github.com/Jokersystems-online/flowki-knowledge-mcp"],
        "pr": "de", "schriften": ["Inter", "IBMPlexMono"]},
    "ats-cv/Jason_Roschmann_CV_ATS.pdf": {
        "pflicht": ["Mitgründer", "Stand 29.09.2026", "Kompetenzen", "2024 – heute", "Freiberuflicher Softwareentwickler", "vor Ort in Zürich"],
        "reihenfolge": ["Mitgründer —", "Flowki Studio —", "duftkumpels.shop —"], "links": ["https://jasonroschmann.github.io/cv/#fs-01", "https://jasonroschmann.github.io/cv/#fs-03", "https://github.com/JasonRoschmann/cv", "https://github.com/Jokersystems-online/flowki-knowledge-mcp"],
        "pr": "de", "schriften": []},
    "Jason_Roschmann_CV_EN.pdf": {
        "pflicht": ["Co-founder", "as of 29 Sep 2026", "Software Engineer · AI Automation & E-Commerce", "Freelance Software Engineer", "Remote · Zürich", "Node.js", "React Native", "RAG pattern",
                    "Backend & APIs: Python", "2024 – present", "Certificate: Google Ads", "Training: Web development",
                    "Field Sales, B2B Direct Sales", "2019 – 2023", "Next step"],
        "reihenfolge": ["Co-founder —", "Flowki Studio —", "duftkumpels.shop —"], "links": ["https://jasonroschmann.github.io/cv/#fs-01", "https://jasonroschmann.github.io/cv/#fs-03", "https://github.com/JasonRoschmann/cv", "https://github.com/Jokersystems-online/flowki-knowledge-mcp"],
        "pr": "en", "schriften": ["Inter", "IBMPlexMono"]},
    "ats-cv/Jason_Roschmann_CV_ATS_EN.pdf": {
        "pflicht": ["Co-founder", "as of 29 Sep 2026", "Core skills", "2024 – present", "Freelance Software Engineer", "on site in Zurich"],
        "reihenfolge": ["Co-founder —", "Flowki Studio —", "duftkumpels.shop —"], "links": ["https://jasonroschmann.github.io/cv/#fs-01", "https://jasonroschmann.github.io/cv/#fs-03", "https://github.com/JasonRoschmann/cv", "https://github.com/Jokersystems-online/flowki-knowledge-mcp"],
        "pr": "en", "schriften": []},
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


def pr_pflicht(d: dict, art: str) -> list[str]:
    # PR-Zahlen stehen in pr-stand.json; die Prüfung erwartet genau diese, damit Druck und Zähler nie auseinanderlaufen
    g = d["gemergt"]
    if art == "marketing":
        return [f"{g['flowki']} eigene Pull Requests gemergt"]
    if art == "en":
        return [f"{g['gesamt']} of my pull requests merged", f"own repos {g['eigen']}", f"client projects {g['kunden']}"]
    return [f"{g['gesamt']} meiner Pull Requests gemergt", f"eigene Repos {g['eigen']}", f"Kundenprojekte {g['kunden']}"]


def schrift_fehler(ausgabe: str, erwartet: list[str]) -> list[str]:
    # Fehlt eine Webfont beim Drucken, setzt Chrome still eine Ersatzschrift ein (z. B. DejaVu unter Linux)
    zeilen = ausgabe.splitlines()
    start = next((i + 1 for i, z in enumerate(zeilen) if z.startswith("-")), len(zeilen))
    namen = [z.split()[0].split("+", 1)[-1].replace("-", "") for z in zeilen[start:] if z.strip()]
    return [f"Schrift fehlt (Ersatzschrift?): {e}" for e in erwartet if not any(n.startswith(e) for n in namen)]


def schriften(pdf: Path) -> str:
    return subprocess.run([PDFFONTS, str(pdf)], capture_output=True, check=True).stdout.decode("utf-8", "replace")


def seiten(pdf: Path) -> int:
    out = subprocess.run([PDFINFO, str(pdf)], capture_output=True, check=True).stdout.decode("utf-8", "replace")
    return int(next(z.split()[-1] for z in out.splitlines() if z.startswith("Pages:")))


def pruefe(pdf: Path, regel: dict) -> list[str]:
    fehler = []
    if (n := seiten(pdf)) != 2:
        fehler.append(f"{n} Seiten statt 2")
    t = " ".join(text(pdf).split())
    pr = pr_pflicht(json.loads(PR_STAND.read_text(encoding="utf-8")), regel["pr"]) if regel["pr"] else []
    fehler += [f"fehlt: {p}" for p in regel["pflicht"] + pr + KONTAKT if p not in t]
    fehler += [f"verboten: {v}" for v in VERBOTEN if v in t]
    ziele = links(pdf)
    fehler += [f"Link fehlt: {u}" for u in regel["links"] if u not in ziele]
    if regel["schriften"]:
        fehler += schrift_fehler(schriften(pdf), regel["schriften"])
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
