<!--
AUTO-DETECTED am 2026-08-03 im Ordner cv-deploy:
(kein Stack automatisch erkannt — bitte manuell ergänzen)

- Git-Repository
- Remote: https://github.com/JasonRoschmann/cv.git
-->

# Stack profile

> ⚠️ DIESES DOKUMENT MUSS VOR DER ERSTEN NUTZUNG BEFÜLLT WERDEN.
> Ersetze alle `<replace>` Platzhalter mit den echten Befehlen deines Projekts.
> Claude liest diese Datei als erste Referenz für Build-, Test- und Lint-Befehle.

## Paketmanager

- Package manager: <replace>  (z.B. pnpm / npm / yarn / pip / poetry / cargo / go)

## Tech-Stack

- Frontend framework: <replace>  (z.B. Next.js / React / Vue / SvelteKit)
- Backend framework: <replace>  (z.B. FastAPI / NestJS / Express / Django / Rails)
- Database: <replace>  (z.B. PostgreSQL / MySQL / SQLite / MongoDB)
- ORM / Migration layer: <replace>  (z.B. Prisma / Drizzle / SQLAlchemy / Flyway)
- Unit test runner: <replace>  (z.B. Vitest / Jest / Pytest / Go test)
- E2E runner: <replace>  (z.B. Playwright / Cypress)
- Linting: <replace>  (z.B. ESLint / Ruff / golangci-lint)
- Type checking: <replace>  (z.B. TypeScript / Pyright / mypy)

## Befehle

- Install: <replace>
- Lint: <replace>
- Typecheck: <replace>
- Unit tests: <replace>
- Integration tests: <replace>
- E2E tests: <replace>
- Build: <replace>
- Migration lint or dry-run: <replace>

## Beispiel (Next.js + FastAPI)

```
Package manager: pnpm (frontend) / poetry (backend)
Frontend: Next.js 14
Backend: FastAPI
Database: PostgreSQL 16
ORM: SQLAlchemy + Alembic
Unit tests: Vitest (frontend) / pytest (backend)
E2E: Playwright

Install:    pnpm install / poetry install
Lint:       pnpm lint / ruff check .
Typecheck:  pnpm typecheck / mypy .
Tests:      pnpm test / pytest -q
Build:      pnpm build
Migration:  alembic upgrade head
```
