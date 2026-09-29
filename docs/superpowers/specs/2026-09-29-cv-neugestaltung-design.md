# CV-Neugestaltung v4 – Design-Spezifikation

Stand: 29.09.2026 · Branch `feat/cv-v4-design`

## Ziel

Jasons Chancen auf einen **Remote-Job** erhöhen. Wirkung „wow“, aber wahr und seriös.

**Abnahmekriterium (Astra):** Nach Seite 1 kann ein unabhängiger Leser die Zielrolle, das wichtigste Projekt und Jasons eigenen Beitrag benennen. Erinnert er sich vor allem an „viele Tools, viele Commits“, ist die Gewichtung falsch.

## Entscheidungen

Jasons Entscheidungen vom 29.09.2026:

- **Gewichtung nach Bedeutung, nicht nach Belegmenge.**
  - Der FlowKI Club ist ein Hauptprojekt.
  - Flowki Studio wird als ganzes Produkt beschrieben; das Clip-Studio ist nur ein Teil davon.
- **Design: Richtung B, Swiss-Raster mit Kennzahlen.** Jason: „das, was beweislich das Beste ist“. Die Belege dafür:
  - Formale Layouts werden gegenüber kreativen bevorzugt (Arnulf et al. 2010, N = 90).
  - Die Verweildauer auf der Berufserfahrung sagt das Weiterreichen voraus (Pina et al. 2023, 221 Recruiter).
  - Mehrspaltigkeit ist das größte Risiko für Bewerbermanagement-Systeme.
  - Zahlenverständnis ist in 30 von 44 Anzeigen gefragt.
- **Marketing-CV:** duftkumpels steht auf Seite 1 zuerst, der FlowKI Club direkt danach.
- **FlowKI Club:** Jason ist Mitgründer seit dem Start im April 2026 (Discord-Server angelegt am 16.04.2026). Seine Aufgaben laut eigener Angabe:
  - Mitglieder gewinnen und onboarden,
  - Calls organisieren und moderieren,
  - Mitgliedern bei ihren Projekten helfen,
  - Inhalte und Themen planen.
- **Zweck des Clubs:** Er ist KI-Community und dient zugleich der Gewinnung von Kundenaufträgen über Outreach-Marketing (Jasons Angabe, 29.09.2026). Das ist eine Brücke zu seinen vier Jahren B2B-Vertrieb.
  - Offene Frage an Jason: Sind aus dem Club schon konkrete Aufträge entstanden?
  - Bis zur Antwort wird nur der Zweck genannt, kein Ergebnis.
- **Beide CVs werden erneuert:** zuerst Marketing/E-Commerce, danach Entwicklung (DE und EN).

## Designsystem (Richtung B)

- **Schriften:**
  - Inter Tight (Name und Überschriften, 700–800)
  - Inter (Fließtext, 10–10,5 px)
  - IBM Plex Mono (Zahlen, Zeiträume, Tools-Zeilen) mit `tabular-nums`
- **Akzentfarbe:** Tannengrün, eine einzige, damit Druck-CV, Web-CV und GitHub-Profil wie eine Marke wirken. Keine Farbflächen, keine Skill-Balken.
- **Kopf:**
  - Name groß, darunter die Zielrolle in der Akzentfarbe
  - eine Unterzeile in Mono
  - Profil mit 3 Zeilen
  - Kontaktzeile
  - Foto rechts
- **Kennzahlen-Leiste:** vier belegte Fakten mit Stichtag bzw. Quelle.
  - Marketing: 700 URLs geprüft · rund 66 Discord-Mitglieder (Stand 29.09.2026) · 4 Jahre B2B-Vertrieb · Google Ads Search zertifiziert
  - Entwicklung: 50 gemergte Pull Requests in Flowki Studio · Test-Suite von 177 auf 199 grüne Tests (hermes-studio) · rund 66 Discord-Mitglieder (Stand 29.09.2026) · 4 Jahre B2B-Vertrieb. Astra prüft vor dem Merge, ob diese Auswahl trägt.
  - Keine Commit-Zahlen als Blickfang.
- **Hauptfluss:**
  - eine Lesespalte mit nummerierten Abschnitten (01, 02 …)
  - je Eintrag: Titel, Rolle und Zeitraum rechtsbündig
  - Stichpunkte im Muster „**Bereich:** Tätigkeit – Wirkung“ (Muster aus Jonas' CV und XYZ-Formel)
  - am Ende jedes Eintrags eine Tools-Zeile in Mono
- **Seite 2:**
  - Fortsetzung, danach Kenntnisse und Tools gruppiert, Zertifikat, Weiterbildung, Sprachen
  - Fußzeile „Name · Seite x/2“ mit QR-Code zum Web-CV

## Inhalt Marketing-CV (DE + ATS)

- **Überschrift:** Junior E-Commerce & Technical SEO | Shopify · Marketing-Automation
- **Profil:** nach Astras Vorschlag: Kundenverständnis aus dem Vertrieb, Shopify und Mehrsprachigkeit, Marketing-Automation, FlowKI Club als Mitgründer.
- **Seite 1:**
  - duftkumpels als größter Block (Auffindbarkeit, Sprachen, Kaufen und Nachfassen, Messung, Gegenprüfung)
  - FlowKI Club: zuerst Community-Zweck und Jasons Community-Aufgaben, dann Outreach-Marketing zur Auftragsgewinnung, danach Newsletter, Distribution, Messbarkeit und Discord-Bot
- **Seite 2:**
  - Flowki Studio als Werkzeug für Content-Produktion im Team, mit 2–3 marketingrelevanten Beiträgen
  - Vertrieb
  - AtopicV und nk247 kurz, mit sichtbarem Status
  - Kenntnisse, Zertifikat, Weiterbildung, Sprachen
- **Raus:** Bewerbungsverwaltung (bleibt im Kompetenz-Atlas).

## Inhalt Entwickler-CV (DE, EN + ATS)

- **Überschrift:** Junior Softwareentwickler / Software Engineer | Python · TypeScript · KI-Automation
- **Seite 1:**
  - Flowki Studio als Produkt: Themenrecherche, KI-gestützte Content-Produktion, redaktionelle Prüfung, Übergabe an die Plattformen.
    Jasons Beiträge: Produktoberflächen, redaktionelle Zusammenarbeit, Fehlerbehandlung, Videoverarbeitung, Publishing, Qualitätssicherung.
  - FlowKI Club: Mitgründer, technische Produktentwicklung (Website, Discord-Bot, Newsletter)
- **Seite 2:**
  - duftkumpels (API- und Übersetzungsautomatisierung, Liquid)
  - Bewerbungsverwaltung
  - hermes-studio kurz
  - Vertrieb, Kenntnisse, Weiterbildung, Sprachen
- **Raus:** Shinobi und kleine Webprojekte (bleiben im Kompetenz-Atlas).

## Abgleich der übrigen Auftritte

- **Web-CV:**
  - FlowKI Club und Flowki Studio neu gewichten und neu formulieren (Projekte, Atlas, Werdegang)
  - Designsprache bleibt, die Akzentfarbe ist dieselbe
- **GitHub-Profil-README, LinkedIn-Texte:** FlowKI Club als Mitgründer seit April 2026, Flowki Studio als Ganzes.
- **Belegmappe:** unverändert.

## Wahrheitsgrenzen

- **Community-Zahl:** „rund 66 Mitglieder laut Discord-Zählung vom 29.09.2026“. Nicht erlaubt sind „aufgebaut auf“, „aktive Mitglieder“ oder eine Wachstumsrate.
- **Community-Aufgaben:** Sie beruhen auf Jasons Angaben (vermerkt im Faktenblatt). Den Rhythmus der Calls nicht nennen, solange er unbekannt ist.
- **Flowki Studio:**
  - Kein autonomer Betrieb auf sieben Plattformen.
  - Keine Reichweitensteigerung.
  - Der Umbauplan ist kein Fertigstellungsbeleg.
- **Bot-Funktionen:** Sie sind als Umsetzung und Tests belegt, nicht als Live-Betrieb.
- **Alle neuen Formulierungen:** Sie brauchen ein Astra-GO vor dem Merge.

## Prüfungen

- Jeder CV hat genau 2 Seiten (`pdfinfo`).
- ATS-Extraktion mit `pdftotext -layout` bleibt sauber: Reihenfolge, Umlaute, keine Ligaturen, Links am Stück.
- Visuelle Prüfung der Renderings.
- Web-CV in 390 px ohne Overflow und ohne Konsolenfehler.
- Live-Prüfung nach dem Merge, den Jason klickt.
