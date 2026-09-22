# CLAUDE.md — JokerSystems Projekt

> Automatisch angelegt via SessionStart-Hook. Die Sektion „Projekt-Info" unten
> wird beim ersten Start mit Stack-Detection befüllt — bitte vervollständigen.

## Regeln

Es gelten die globalen JokerSystems-Regeln aus `~/.claude/CLAUDE.md` und
`~/.claude/rules/` (Karpathy-Prinzipien, kritische Verbote, 20 Coding-Rules,
Definition of Done, Beweis-Protokoll, Orchestrierung). Hier nichts duplizieren —
nur projekt-spezifische Abweichungen und Ergänzungen gehören in diese Datei.

## Arbeitsweise (Kurzfassung)

1. Projektstand unten lesen (✅ / 🚧 / 🐛), dann erst arbeiten
2. Eine Einheit auf einmal — Test-Plan formulieren BEVOR Code geschrieben wird
3. Beweis-Protokoll: `make test` / `make lint` mit vollständiger Ausgabe zeigen —
   niemals „sollte funktionieren"
4. Nach jeder Einheit: Projektstand unten aktualisieren

## Orchestrierung

Verfügbare Subagents: backend-developer, frontend-developer, test-engineer,
database-engineer, devops-engineer, security-auditor, code-reviewer, qa-engineer,
integration-tester, migration-specialist, orchestrator.
Routing-Regeln: `~/.claude/rules/orchestration.md`

## Sprache

Alle Dokumentation und Antworten auf **Deutsch**.

---

## Projekt-Info (cv-deploy)

**Angelegt:** 2026-08-03 via SessionStart-Hook

### Auto-detected Stack
(kein Stack automatisch erkannt — bitte manuell ergänzen)

### Details
- Git-Repository
- Remote: https://github.com/JasonRoschmann/cv.git

### Projekt-Beschreibung (BITTE AUSFÜLLEN)
- **Was ist dieses Projekt?** (2-3 Sätze)
- **Zielgruppe:** (B2B / B2C / Developer / intern / Kunde)
- **Monetarisierung:** (SaaS / E-Commerce / Content / intern / Kundenprojekt)
- **Status:** (Idee / MVP / Live / Maintenance)
- **Repo:** (GitHub-URL wenn vorhanden)

### URLs
- **Local:** http://localhost:3000 / http://localhost:8000
- **Staging:** (wenn vorhanden)
- **Production:** (wenn vorhanden)

### Projektstand

#### ✅ Fertig
- Projekt initialisiert

#### 🚧 In Arbeit
- (wird beim Arbeiten dokumentiert)

#### 🐛 Bugs / P0-P1
- (keine bekannt)

#### 📋 Next Steps
1. Diese CLAUDE.md-Sektion anpassen (Projekt-Beschreibung, URLs)
2. `docs/stack/stack-profile.md` mit echten Befehlen ausfüllen (ersetzt \<replace\>)
3. Falls Docker: `docker compose up -d`
