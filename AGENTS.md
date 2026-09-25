# Agent catalog and delegation contracts

This file describes the intent of each specialist. The executable subagent definitions live under `.claude/agents/`.
Claude Code reads `CLAUDE.md`, not this file directly; `CLAUDE.md` imports this document.

## Architecture and planning

### solution-architect
Use before broad, cross-cutting, or ambiguous work.
Answer: what should change, in what order, with what risk tier, and how it will be verified.

## Implementation specialists

### backend-developer
Use for backend implementation, API endpoints, services, auth, background jobs, and integrations.
Answer: what concrete backend code change satisfies the requirement with production-ready validation.

### frontend-developer
Use for UI implementation, forms, routing, state, design-system aligned components, and client behavior.
Answer: what user-facing implementation delivers the change with complete states and accessibility.

### database-engineer
Use for migrations, schema design, indexes, persistence correctness, and rollout-compatible data changes.
Answer: what schema/data change is correct, safe, and rollout-ready.

### devops-engineer
Use for containers, runtime config, CI/CD, deployment scripts, health checks, and infra validation.
Answer: what operational change is needed and how it is validated safely.

### test-engineer
Use for writing or strengthening validation: unit, integration, contract, E2E, regression tests.
Answer: what minimum high-signal validation proves the behavior.

### qa-engineer
Use for browser flows, Playwright, screenshots, live checks, and manual proof collection.
Answer: what the user actually sees and whether the flow works end to end.

## Review and release specialists

### frontend-reviewer
Use after user-facing changes.
Answer: are UI states complete, accessible, consistent, and behaviorally correct.

### backend-reviewer
Use after API, service, auth, worker, or persistence changes.
Answer: is the change correct, safe under failure, and supported by adequate tests.

### migration-auditor
Use for schema, data, or rollout changes.
Answer: is deployment sequencing safe, reversible enough, and compatible with real production data.

### security-reviewer
Use for trust-boundary changes.
Answer: do inputs, permissions, secrets, uploads, and external integrations remain safe.

### test-architect
Use when validation strategy is weak or unclear.
Answer: which minimum high-signal tests are required to trust the change.

### observability-auditor
Use when critical behavior changes.
Answer: would an operator be able to detect, diagnose, and triage failure in production.

### code-reviewer
Use as the final engineering quality gate.
Answer: would a senior engineer approve the code for merge.

### release-manager
Use before considering the change complete for production.
Answer: is the work release-ready, with blockers and validation gaps clearly identified.

## Orchestration notes

- Use a single session for small, sequential work.
- Use subagents for specialized analysis or review.
- Use agent teams only when work is truly parallel and independent enough to justify the cost.
- Do not use agent teams for sequential tasks.

## Handoff standard
Every specialist should return:
- scope examined
- evidence used
- findings by severity
- validation gaps
- go/no-go verdict
