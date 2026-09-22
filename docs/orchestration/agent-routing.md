# Agent routing and orchestration

## Routing guidance

### Single session
Use for:
- small features
- simple bugs
- documentation
- tightly sequential work
- token-sensitive tasks

### Subagents
Use for:
- specialized analysis
- code review
- security scan
- migration audit
- test planning
- observability review

### Agent teams
Use only when:
- backend and frontend can progress in parallel
- multiple layers truly can be implemented independently
- communication overhead is justified
- the quality bar is explicitly restated to all participants

## Model routing guidance

- Orchestrator / high-risk review: Opus-level reasoning
- Implementation specialists: Sonnet-level execution
- Security and final code review: Opus-level reasoning preferred
- Browser/live QA: Sonnet-level execution is usually sufficient

## Domain routing examples

### Backend + frontend feature
1. `solution-architect`
2. parallel implementation via `backend-developer` and `frontend-developer` if independent
3. `test-engineer`
4. `backend-reviewer` and `frontend-reviewer`
5. `security-reviewer` when auth, payments, PII, uploads, or trust boundaries changed
6. `code-reviewer`

### Backend-only change
- single session or `backend-developer`
- then `test-engineer`
- then `backend-reviewer`

### DB schema change
- `database-engineer`
- `migration-auditor`
- `test-engineer`
- `release-manager`

### Pre-launch gate
- `security-reviewer`
- `qa-engineer`
- `code-reviewer`
- `release-manager`

## Quality bar to restate to all specialists

- Production-ready code only
- No placeholder logic
- Validation required before completion
- Tests must be green before claiming success
- Final summaries must separate evidence from inference
