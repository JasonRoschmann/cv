"""Prüft die CV-PDFs: 2 Seiten, Pflichtinhalte, Reihenfolge der Projekte, verbotene Aussagen, saubere Textschicht."""
import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PDFTOTEXT = r"C:\Users\Jason Roschmann\scoop\shims\pdftotext.exe"
PDFINFO = "pdfinfo"
KONTAKT = ["jason@roschmann-digital.de", "jasonroschmann.github.io/cv"]
VERBOTEN = ["Commits", "commits", "aktive Mitglieder", "active members", "gewachsen", "grown to"]
REGELN = {
    "Jason_Roschmann_CV_Marketing.pdf": {
        "pflicht": ["Mitgründer", "Outreach", "Stand 29.09.2026", "Junior E-Commerce & Technical SEO"],
        "reihenfolge": ["duftkumpels.shop —", "FlowKI Club —", "Flowki Studio —"]},
    "ats-cv/Jason_Roschmann_CV_Marketing_ATS.pdf": {
        "pflicht": ["Mitgründer", "Outreach", "Stand 29.09.2026"],
        "reihenfolge": ["duftkumpels.shop —", "FlowKI Club —", "Flowki Studio —"]},
    "Jason_Roschmann_CV.pdf": {
        "pflicht": ["Mitgründer", "Stand 29.09.2026", "Junior Softwareentwickler"],
        "reihenfolge": ["Flowki Studio —", "FlowKI Club —", "duftkumpels.shop —"]},
    "ats-cv/Jason_Roschmann_CV_ATS.pdf": {
        "pflicht": ["Mitgründer", "Stand 29.09.2026"],
        "reihenfolge": ["Flowki Studio —", "FlowKI Club —", "duftkumpels.shop —"]},
    "Jason_Roschmann_CV_EN.pdf": {
        "pflicht": ["Co-founder", "as of 29 Sep 2026", "Junior Software"],
        "reihenfolge": ["Flowki Studio —", "FlowKI Club —", "duftkumpels.shop —"]},
    "ats-cv/Jason_Roschmann_CV_ATS_EN.pdf": {
        "pflicht": ["Co-founder", "as of 29 Sep 2026"],
        "reihenfolge": ["Flowki Studio —", "FlowKI Club —", "duftkumpels.shop —"]},
}


def text(pdf: Path) -> str:
    return subprocess.run([PDFTOTEXT, "-enc", "UTF-8", str(pdf), "-"], capture_output=True, check=True).stdout.decode("utf-8")


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
    if any(chr(c) in t for c in range(0xFB00, 0xFB07)) or "\ufffd" in t:
        fehler.append("Ligatur oder Ersatzzeichen in der Textschicht")
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
        print(("ROT  " if fehler else "GRÜN ") + name + "".join("\n     - " + f for f in fehler))
    return 1 if rot else 0


if __name__ == "__main__":
    sys.exit(main())
