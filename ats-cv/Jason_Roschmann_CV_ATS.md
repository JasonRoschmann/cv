# Jason Roschmann

Junior Softwareentwickler / Software Engineer · Python · FastAPI · TypeScript · Next.js · PostgreSQL · Docker

E-Mail: jason@roschmann-digital.de | Telefon: +49 155 612 953 91\
LinkedIn: linkedin.com/in/jason-roschmann-1091512b2 | GitHub: github.com/JasonRoschmann | Web-CV: jasonroschmann.github.io/cv\
Wohnort: Hamburg, Deutschland | Gesucht: Hamburg oder remote; Umzug nach Zürich für eine passende Rolle möglich | Start nach Absprache

## Profil

Ich entwickle Weboberflächen und Python-Abläufe für konkrete Arbeitsprozesse: Content-Produktion, E-Commerce und Community-Werkzeuge. Meine Schwerpunkte sind die Verbindung von Oberfläche und Backend, nachvollziehbare Zustände und gezielte Fehlerprüfungen – mit KI-Agenten als Werkzeug und eigener Verantwortung für Anforderungen und Abnahme. Aus vier Jahren Vertrieb bringe ich Erfahrung darin mit, Anforderungen im direkten Gespräch zu verstehen.

Kennzahlen: <span data-pr="flowki">50</span> eigene Pull Requests gemergt (Flowki Studio) · 21 → 0 rote Tests (hermes-studio) · rund 66 Discord-Mitglieder FlowKI Club (Stand 29.09.2026) · 4 Jahre B2B-Vertrieb (2019–2023)

## Projekte

### Flowki Studio — internes Social-Media-Studio, Teamprojekt (Aug. 2026 – heute)

Zweck: Internes Social-Media-Studio für Themenrecherche, KI-gestützte Content-Produktion, redaktionelle Prüfung und Plattformübergabe; mein Beitrag im Team (<span data-pr="flowki">50</span> eigene Pull Requests gemergt): Produktoberflächen, Workflow-Integration, Clip-Verarbeitung und Publishing.

- Produktoberfläche: Produktions-, Freigabe- und Veröffentlichungsansichten weiterentwickelt – Bearbeitungsstände, Phasendauer und erforderliche Nutzeraktionen sichtbar gemacht.
- Redaktionelle Zusammenarbeit: Ablehnungsgründe durch Oberfläche, API-Client und Freigabeprotokoll verbunden – Rückgaben zur Überarbeitung mit nachvollziehbarer Begründung ermöglicht.
- Fehlerbehandlung: Erfolgreiche Produktion bzw. Lizenzierung von nachfolgenden Status- und Zuordnungsfehlern getrennt – irreführende Fehlermeldungen und Anreize für erneute, kostenwirksame Aufrufe beseitigt.
- Videoverarbeitung: Speaker-Reframe, Schnittvarianten und reproduzierbaren Neu-Render nach Korrekturen umgesetzt – Langvideos in bearbeitbare Hochformat-Clips überführt.
- Publishing: TikTok-Entwurfsweg mit eigenem Status und Nutzerhinweis integriert – hochgeladene Entwürfe eindeutig von veröffentlichten Posts unterschieden.

Tools: Python, FastAPI, Celery, SQLAlchemy/Alembic, PostgreSQL, Redis, Next.js, TypeScript

### FlowKI Club — Mitgründer, Website, Discord-Bot, Newsletter (Apr. 2026 – heute)

Zweck: Deutschsprachige KI-Community – rund 66 Mitglieder im Discord (Stand 29.09.2026) – mit Fachartikeln, Online-Calls und gemeinsamer Projektarbeit; ich verbinde Community-Arbeit mit technischer Produktentwicklung.

- Community-Werkzeuge: Discord-Bot um /ask und Self-Service-Themenrollen erweitert; discord.js und Testwerkzeuge aktualisiert.
- KI-Antwortqualität: Artikelinhalte als Wissensgrundlage des FAQ-Bots angebunden und einen Relevanz-Prüfschritt ergänzt – Verhalten bei unpassenden Treffern mit gezielten Tests abgesichert.
- Website & Newsletter: Newsletter mit Double-Opt-In und Empfehlungslinks, Plausible-Ereignisse für Anmeldung und Klicks auf Discord-Beitrittslinks; Autoren-, FAQ- und HowTo-Markup in der Artikelausgabe.
- Community: Mitglieder beim Einstieg begleitet, Online-Calls organisiert und moderiert, bei Projekten unterstützt.

Tools: TypeScript, discord.js, Claude-API, PostgreSQL, Vitest, Next.js

### hermes-studio — Beitrag zu fremdem Projekt, Fehleranalyse (Sep. 2026)

- Ursache: 21 rote Tests mit zwei Ursachen – 20× ein nie geschlossenes SQLite-Handle, das unter Windows das Aufräumen sperrt, 1× ein veralteter Test gegen eine Sicherheitsregel; Handle geschlossen, Regel behalten, Test korrigiert.
- Nachweis: Mutationsprobe – mit abgeschwächter Sicherheitsregel scheitert der korrigierte Test; grüne Tests: 177 → 199.
- Eigener Beitrag: Stillen Datenverlust im Task-Store behoben, mit fünf neuen Tests.

Beleg: Fallstudie im Web-CV <https://jasonroschmann.github.io/cv/#fs-01>

### duftkumpels.shop — Kundenprojekt, Shopify, API- & Übersetzungsautomatisierung (Juni 2026 – heute)

- Automatisierung: Übersetzungs-Pipeline DE/EN/FR mit HTML-Extraktion, Strukturprüfung und Import per CSV bzw. GraphQL; Verfügbarkeitsabgleich über die Admin-GraphQL-API mit Sicherung und Rücklesen.
- SEO-Technik: Search-Console-Auswertung automatisiert, 700 URLs auf Indexierung geprüft; JSON-LD ergänzt und automatisiert geprüft.
- Theme & Qualität: Gekauftes Theme in Liquid, CSS und JavaScript umgebaut; wöchentliche Lighthouse-Prüfung gegen den Live-Shop per GitHub Actions.
- E-Mail: Klaviyo-Abbruchmail auf wiederherstellbaren Checkout-Link korrigiert.

Tools: Shopify Liquid, Admin-GraphQL-API, Python, GitHub Actions, Klaviyo

### KI-gestützte Bewerbungsverwaltung — Eigenprojekt, Python (Juli 2026 – heute)

Zweck: Python-Pipeline für Stellensuche über Job-APIs (u. a. Bundesagentur für Arbeit, Greenhouse, Lever), Anschreiben, Prüfungen, Versand und Antwortzuordnung.

- Nachvollziehbarkeit: Kanalübergreifendes Hauptbuch für Erstbewerbungen mit Reservierung – keine Doppelbewerbung über Mail und Portal, höchstens eine Bewerbung je Firma in 14 Tagen.
- Prüfungen vor dem Versand: Unbrauchbare Modellantworten stoppen den Lauf; Modell-Kaskade (Claude, Gemini, Groq) mit Sperrzeiten.
- Bewertungsqualität: LLM-Bewertungen gegen blinde Referenzurteile geprüft; eine überarbeitete Analyse nach unvollständiger Messung ohne belegte Verbesserung nicht ausgerollt.
- Betrieb: Rollouts mit Prüfsummen, Tests vor und nach dem Tausch und automatischem Rückbau bei abgefangenen Fehlern.

Belege: Fallstudie Antwortzuordnung <https://jasonroschmann.github.io/cv/#fs-02> · Fallstudie LLM-Bewertung <https://jasonroschmann.github.io/cv/#fs-03>

## Berufserfahrung

### KI-Automation & Webentwicklung — Eigene Projekte, Team- und Kundenprojekte (2024 – heute)

- Python-Backends und Next.js-Frontends entwickelt, getestet und auf Linux-Servern betrieben (Docker Compose, Cron, Deployment mit Rollback); Shopify-Themes angepasst; im Team über Branches, Pull Requests und gemeinsame Test-Suites.
- Kunden-Websites im Team gebaut: Next.js, GSAP, CI mit TypeScript-Check, ESLint, Vitest und Playwright.

### B2B-Direktvertrieb — Außendienst bundesweit, EWE TEL und Ranger Marketing (2019 – 2023)

- Kaltakquise und Bedarfsgespräche mit Inhabern und Geschäftsführern, Verhandlung und Abschluss vor Ort.
- Täglicher Umgang mit Absagen – und der Blick dafür, welche Probleme ein Betrieb wirklich hat.

## Kenntnisse & Arbeitsweise

- Entwicklung: Python, REST-APIs mit FastAPI · TypeScript, React, Next.js, discord.js · React Native (Eigenprojekt)
- KI & Agenten: Claude Code, LLM-APIs (Claude, Gemini, Groq), MCP, Agenten-Orchestrierung, n8n
- Daten & Jobs: SQL/PostgreSQL, SQLAlchemy/Alembic, Celery, Redis, Supabase
- Qualität: Git, CI/CD mit GitHub Actions, pytest, Vitest, Playwright, Lighthouse-CI
- Betrieb: Linux-Server, Docker Compose, Cron, flock, SMTP/IMAP, SPF/DKIM
- Web & Commerce: Shopify Liquid, Tailwind, GSAP, PWA, Canvas/WebGL
- Mit KI-Agenten: Fehler zuerst als roter Test · Agent setzt um · ein zweites Modell prüft zusätzlich als Reviewer · Rollout mit Prüfsummen und automatischem Rückbau bei abgefangenen Fehlern
- GitHub: <span data-pr="gesamt">61</span> meiner Pull Requests gemergt (Stand <span data-pr="stand-de">29.09.2026</span>): Flowki Studio <span data-pr="flowki">50</span>, eigene Repos <span data-pr="eigen">8</span>, Kundenprojekte <span data-pr="kunden">3</span>
- Öffentliche Codebeispiele: Web-CV <https://github.com/JasonRoschmann/cv> · MCP-Server für Club-Inhalte <https://github.com/Jokersystems-online/flowki-knowledge-mcp>

## Weiterbildung, Zertifikat & Sprachen

- Weiterbildung: Webentwicklung (2024, 6 Monate): HTML, CSS, JavaScript, Web-Architektur
- Zertifikat: Google Ads Search Certification (Skillshop), Dezember 2025, gültig bis 03.12.2026 – verifizierbar: <https://www.credential.net/cd05c77a-a7ef-48e0-809e-5147135f810e>
- Sprachen: Deutsch (Muttersprache) · Englisch (B1, Richtung B2) · Polnisch (mündlich)
- Remote-Arbeit: Verteilte Teamarbeit über GitHub (Branches, Pull Requests), Discord und Online-Calls
