# CV-Neugestaltung v4 – Umsetzungsplan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Die Druck-CVs (Marketing, Entwicklung DE/EN), ATS-Fassungen, der Web-CV, das GitHub-Profil und die LinkedIn-Texte werden nach Bedeutung gewichtet und im Design B erneuert.

**Architecture:**
- Ein neues gemeinsames Stylesheet `cv-v4.css` trägt Design B für alle drei Druck-CVs. Die Belegmappe behält `cv-print.css`.
- Inhalte stehen direkt im HTML bzw. Markdown, gebaut wird weiter mit `scripts/build_cv_pdf.py`.
- Ein neues Prüfskript `scripts/cv_pruefung.py` sichert Seitenzahl, Pflichtinhalte, Reihenfolge, verbotene Aussagen und eine saubere Textschicht ab. Es ist der Test dieses Projekts.

**Tech Stack:**
- HTML/CSS (Google Fonts Inter Tight, Inter, IBM Plex Mono)
- Edge headless über `build_cv_pdf.py`
- pandoc für ATS
- Poppler `pdftotext`/`pdfinfo`
- Python 3.12, Playwright-MCP für den Web-CV
- Codex-MCP „Astra“ für Wahrheits-Reviews

**Spec:** `docs/superpowers/specs/2026-09-29-cv-neugestaltung-design.md`

## Global Constraints

- Jeder Druck-CV und jede ATS-PDF hat **genau 2 Seiten**.
- Es gibt **eine** Akzentfarbe: Tannengrün `#17784a`, auf Dunkel `#3fdc84`. Keine Farbflächen, keine Skill-Balken, keine Karten-Sammlung.
- Die Community-Zahl steht nur als „rund 66 Mitglieder (Discord, Stand 29.09.2026)“ bzw. EN „about 66 members (Discord, as of 29 Sep 2026)“.
- **Keine Commit-Zahlen** in irgendeiner Fassung.
- Den Rhythmus der Calls nicht nennen. Keine durch Outreach gewonnenen Aufträge behaupten.
- **Flowki Studio:**
  - Kein autonomer Betrieb auf sieben Plattformen.
  - Keine Reichweitensteigerung.
  - Das Clip-Studio höchstens als ein Stichpunkt.
- Überschriften von Projekten und Stationen immer im Format `Name — Rolle`, mit Gedankenstrich und Leerzeichen, damit die Reihenfolge prüfbar ist.
- Deutsche Monatsabkürzungen mit Punkt (Apr., Aug., Sep.), englische ohne.
- Vor jedem Merge braucht jede neue Formulierung ein **Astra-GO**. Den Merge klickt Jason; `gh pr merge` ist per Hook gesperrt.
- BSOD-Regel: keine zwei rekursiven Dateisuchen im selben Block. Ein Fan-out von Sub-Agents ist nicht nötig.

## Review Focus

1. **Seite 2 läuft über** (3 Seiten) nach Textänderungen. Das Prüfskript meldet jede Seitenzahl ungleich 2.
2. **Die PDF-Textschicht verliert die Reihenfolge** bei Kennzahlen-Leiste oder Kopf mit Foto: Poppler stellt kleinere Beschriftungen um. Das Prüfskript kontrolliert die Reihenfolge der Projektüberschriften und Pflichtbegriffe im extrahierten Text.
3. **Verbotene Aussagen schleichen sich ein** („Commits“, „aktive Mitglieder“, „gewachsen“). Das Prüfskript hat eine Verbotsliste für alle Fassungen.
4. **Das Marketing-PDF ist im Viewer gesperrt.** Der Build schreibt dann in den Scratchpad, eingetragen wird über den Git-Index (`git hash-object -w` + `git update-index --cacheinfo`).
5. **Der Web-CV bricht auf 390 px um oder läuft über**, nachdem die Texte länger geworden sind. Das prüft eine Playwright-Messung wie bisher (Overflow, Konsolenfehler).

---

### Task 1: Prüfskript (der Test)

**Files:**
- Create: `scripts/cv_pruefung.py`

**Interfaces:**
- Produces: `python scripts/cv_pruefung.py [--pdf-dir DIR]` → Exit 0 bei Erfolg, sonst Exit 1 mit einer Liste der Verstöße. Wird ab Task 3 nach jedem Build aufgerufen.

- [ ] **Step 1: Prüfskript schreiben**

```python
"""Prüft die CV-PDFs: 2 Seiten, Pflichtinhalte, Reihenfolge der Projekte, verbotene Aussagen, saubere Textschicht."""
import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PDFTOTEXT = r"C:\Users\Jason Roschmann\scoop\shims\pdftotext.exe"
PDFINFO = r"C:\Users\Jason Roschmann\scoop\shims\pdfinfo.exe"
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
        pdf = args.pdf_dir / Path(name).name if (args.pdf_dir / Path(name).name).exists() else REPO / name
        fehler = pruefe(pdf, regel)
        rot |= bool(fehler)
        print(("ROT  " if fehler else "GRÜN ") + name + ("".join("\n     - " + f for f in fehler)))
    return 1 if rot else 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Gegen den aktuellen Stand laufen lassen; er muss ROT sein**

Run: `PYTHONIOENCODING=utf-8 py -3 scripts/cv_pruefung.py`
Expected: Exit 1. Unter anderem fehlen „Mitgründer“, „Outreach“ und „Stand 29.09.2026“, und die Reihenfolge ist falsch.

- [ ] **Step 3: Commit**

```bash
git add scripts/cv_pruefung.py
git commit -m "test(cv): Pruefskript fuer v4 (2 Seiten, Pflicht, Reihenfolge, Verbote, Textschicht) - rot gegen v3"
```

### Task 2: Faktenblatt v5 und Astra-Formulierungen

**Files:**
- Create: `<scratchpad>/cv_fakten_v5.md` (nicht im Repo, weil Kundendetails)

**Interfaces:**
- Consumes: Astras Konzept vom 29.09.2026 (Positionierung, Stichpunkte, Grenzen), Jasons Antworten, Discord-API-Zählung
- Produces: die freigegebenen Textbausteine, die Task 4–8 wörtlich verwenden

- [ ] **Step 1: Faktenblatt schreiben.** Es gibt je Projekt die Quelle an: `[J]` = Jasons Angabe, `[A]` = API/Repo, `[C]` = Commit/Datei. Inhalt:
  - **FlowKI Club:**
    - Mitgründer seit April 2026 [J]
    - Discord-Server angelegt am 16.04.2026 [A]
    - rund 66 Mitglieder, Stand 29.09.2026 [A]
    - Calls, Projekthilfe, Onboarding, Themenplanung [J]
    - Outreach-Marketing zur Auftragsgewinnung [J]
    - Newsletter DOI und Referral, Plausible-Ereignisse, Social-Pakete, Bot `/ask`, Self-Service-Rollen, FAQ-Wissensbasis, Autoren-/FAQ-/HowTo-Markup [C: a6a97df, c625ec9, 717a8bd, 325a00e, 202b49d, 8513059, a50dcff, 704b8b0, 46f4f87]
  - **Flowki Studio:**
    - Produkt als Ganzes; Rollenverteilung laut `docs/umbauplan-v2/01-zwei-teams.md`
    - Beiträge laut Astra [C: 81034022, e14c151a, 1af33df4, 1cec68b6]
  - **duftkumpels, Vertrieb, Zertifikat, Weiterbildung:** unverändert gegenüber v3.

- [ ] **Step 2: Astra um fertige Texte bitten.** Anfrage im bestehenden Thread: Kopf, Profil und Stichpunkte für beide CVs in Design B, im Muster „Bereich: Tätigkeit – Wirkung“ und mit den Global Constraints. Ziel: Astra-GO auf den Wortlaut, bevor HTML entsteht.

### Task 3: Stylesheet Design B

**Files:**
- Create: `cv-v4.css`

**Interfaces:**
- Produces: die CSS-Klassen, die Task 4, 6 und 7 verwenden:
  - `.page`, `.kopf`, `.kopf-text`, `.foto`, `.rolle`, `.unter`, `.lead`, `.kontakt`
  - `.kpi` mit `div > b / span / i`
  - `.sek` mit `span` (Nummer), `.eintrag`, `.ekopf`, `h3` mit `span.r` (Rolle), `.zeit`
  - `ul.b > li` mit `b` (Bereichslabel), `.zweck`, `.tools`
  - `.sk` mit `.k` (Kenntnisse), `.fuss`, `.qr`

- [ ] **Step 1: `cv-v4.css` schreiben.** Grundlage ist der freigegebene Entwurf B (`<scratchpad>/mockups/b_swiss.html`) mit diesen Änderungen:
  - Akzent `--acc:#17784a`
  - Fließtext 10.2px, Zeilenhöhe 1.45
  - `li::before` als Quadrat in der Akzentfarbe, `font-size:inherit`, damit Poppler die Reihenfolge nicht vertauscht
  - `.nw{white-space:nowrap}`
  - `@page{size:A4;margin:0}`
  - `.page{width:210mm;height:297mm;padding:15mm 16mm 12mm;position:relative;overflow:hidden}`
  - `.fuss{position:absolute;left:16mm;right:16mm;bottom:8mm}`
  - `.eintrag{break-inside:avoid}`

- [ ] **Step 2: Commit** (`git add cv-v4.css`, `git commit -m "feat(cv): Design-B-Stylesheet cv-v4.css"`)

### Task 4: Marketing-CV v4

**Files:**
- Modify (neu aufbauen): `cv-print-marketing.html`
- Modify: `ats-cv/Jason_Roschmann_CV_Marketing_ATS.md`

**Interfaces:**
- Consumes: `cv-v4.css` (Task 3), die Texte aus Task 2
- Produces: `Jason_Roschmann_CV_Marketing.pdf` und die ATS-Dateien

- [ ] **Step 1: Seite 1 aufbauen**
  - **Kopf:** Name; Rolle „Junior E-Commerce & Technical SEO“; Unterzeile „Shopify · Marketing-Automation · KI-Community · Hamburg / remote“; Profil (Astra); Kontakt; Foto
  - **Kennzahlen:**
    - 700 · URLs auf Indexierung geprüft · Kundenshop
    - 66 · Mitglieder im FlowKI-Discord · Stand 29.09.2026
    - 4 J. · B2B-Vertrieb mit Kundenkontakt · 2019–2023
    - Ads · Google Ads Search zertifiziert · verifizierbar
  - **01 Projekte & Praxis:**
    - `duftkumpels.shop — Kundenprojekt · Shopify DE/EN/FR` (Juni 2026 – heute), Zweckzeile, 4 Bereiche aus v3, Gegenprüfung, Tools
    - `FlowKI Club — Mitgründer · KI-Community & Magazin` (Apr. 2026 – heute), Zweckzeile mit „rund 66 Mitglieder (Discord, Stand 29.09.2026)“ und Outreach, 5 Stichpunkte (Task 2), Tools
- [ ] **Step 2: Seite 2 aufbauen**
  - `Flowki Studio — Social-Media-Studio · Teamprojekt` (Aug. 2026 – heute) mit 3 marketingrelevanten Stichpunkten
  - `02 Berufserfahrung`: E-Commerce, Webentwicklung & KI-Automation (2024 – heute); `B2B-Direktvertrieb — Außendienst` (2019–2023)
  - `03 Weitere Web- & Shop-Projekte`: AtopicV mit Status
  - `04 Kenntnisse & Tools` (6 Gruppen aus v3), Zertifikat, Weiterbildung, Sprachen, QR-Code, Fußzeile
- [ ] **Step 3: ATS-Markdown im gleichen Wortlaut und in gleicher Reihenfolge**, Überschriften `### Name — Rolle (Zeitraum)`
- [ ] **Step 4: Bauen** (mit Ersatzpfad, falls das PDF gesperrt ist), dann `PYTHONIOENCODING=utf-8 py -3 scripts/cv_pruefung.py --pdf-dir <scratchpad>`. Expected: GRÜN für beide Marketing-Einträge. Die Entwickler-Einträge sind noch ROT, das ist erwartet.
- [ ] **Step 5: Rendern und ansehen.** `pdftoppm -r 80` für beide Seiten; kein Text unter dem Foto, keine Ein-Wort-Umbrüche in Überschriften.
- [ ] **Step 6: Astra-Review** von Druck und ATS. Befunde einarbeiten, bis GO.
- [ ] **Step 7: Commit** (HTML, MD/TXT/DOCX/PDF; das Druck-PDF über den Index, falls gesperrt)

### Task 5: Entwickler-CV DE v4

**Files:**
- Modify (neu aufbauen): `cv-print.html`, `ats-cv/Jason_Roschmann_CV_ATS.md`

- [ ] **Step 1: Seite 1 aufbauen**
  - **Kopf:** Rolle „Junior Softwareentwickler / Software Engineer“; Unterzeile „Python · TypeScript · KI-Automation · Hamburg / remote“; Profil (Astra)
  - **Kennzahlen:**
    - 50 · gemergte Pull Requests in Flowki Studio
    - 177→199 · grüne Tests nach Fehleranalyse (hermes-studio)
    - 66 · Mitglieder im FlowKI-Discord · Stand 29.09.2026
    - 4 J. · B2B-Vertrieb
  - **01 Projekte:**
    - `Flowki Studio — Social-Media-Studio · Team-SaaS` mit Produktzeile und 6 Stichpunkten (Astra)
    - `FlowKI Club — Mitgründer · Website, Discord-Bot, Newsletter`
- [ ] **Step 2: Seite 2 aufbauen:** `duftkumpels.shop — Kundenprojekt`, `KI-gestützte Bewerbungsverwaltung — Eigenprojekt`, hermes-studio kurz, Berufserfahrung, Kenntnisse, Weiterbildung, Zertifikat, Sprachen
- [ ] **Step 3: ATS-Markdown gleichziehen, bauen, Prüfskript laufen lassen.** Expected: die DE-Entwickler-Einträge GRÜN.
- [ ] **Step 4: Rendern und ansehen, Astra-Review bis GO, Commit**

### Task 6: Entwickler-CV EN v4

**Files:**
- Modify: `cv-print-en.html`, `ats-cv/Jason_Roschmann_CV_ATS_EN.md`

- [ ] **Step 1: Die DE-Fassung aus Task 5 übersetzen**
  - „Co-founder“, „about 66 members (Discord, as of 29 Sep 2026)“
  - Monatsnamen ohne Punkt
- [ ] **Step 2: Bauen, Prüfskript** (alle 6 Einträge GRÜN), rendern und ansehen, Astra-Review bis GO, Commit

### Task 7: Web-CV-Abgleich

**Files:**
- Modify: `index.html` (Projekte-, Werdegang- und Kompetenzen-Ansicht, Startseiten-Widget, FAQ, JSON-LD `knowsAbout`)

- [ ] **Step 1: FlowKI Club und Flowki Studio anpassen**
  - Bestehende Einträge suchen (`Grep` nach `FlowKI Club` und `Flowki Studio`, ein Aufruf nach dem anderen)
  - Texte durch die Astra-Fassungen ersetzen
  - FlowKI Club als Mitgründer mit Community und Outreach nach vorn
  - Flowki Studio als Produkt; Clip-Studio als ein Punkt
- [ ] **Step 2: Lokal prüfen.** `py -3 -m http.server` im Hintergrund, Playwright bei 390 px und 1280 px: kein Overflow, 0 Konsolenfehler, alle Ansichten öffnen.
- [ ] **Step 3: Astra-Review der geänderten Web-Texte, Commit**

### Task 8: GitHub-Profil und LinkedIn-Texte

**Files:**
- Modify: `<scratchpad>/gh_profile/README.md` (veröffentlicht über `gh api PUT`), `<scratchpad>/linkedin_texte.md`

- [ ] **Step 1: README-Tabelle umbauen**
  - FlowKI Club (Mitgründer seit Apr. 2026, Community, Outreach) an erster oder zweiter Stelle
  - Flowki Studio als Produkt
  - Monatsabkürzungen mit Punkt
- [ ] **Step 2: LinkedIn-Info, Projekte und Überschrift nachziehen**
  - FlowKI-Club-Projekt als Mitgründer ab April 2026
  - Flowki-Studio-Beschreibung als Ganzes
- [ ] **Step 3: Astra-Review, Secret-Scan (grep), README veröffentlichen, zurücklesen**

### Task 9: Abschluss und Livegang

- [ ] **Step 1:** Alle PDFs neu bauen, `scripts/cv_pruefung.py` vollständig GRÜN (Ausgabe zitieren), Web-Check GRÜN.
- [ ] **Step 2:** Branch pushen, PR anlegen, Jason klickt den Merge. Danach die Live-Prüfung: alle PDFs byte-identisch mit main, JSON-LD live.
- [ ] **Step 3:** Memory `project-goal-bewerbungsfabrik-autonom` nachziehen; offene Punkte an Jason (Aufträge aus Outreach? Rhythmus der Calls?).
