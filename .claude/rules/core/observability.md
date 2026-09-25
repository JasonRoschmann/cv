# Observability rules

- Critical paths require actionable logs, metrics, or traces.
- Error handling should preserve triage value without leaking sensitive data.
- New background jobs, external calls, or async flows must expose enough evidence for production diagnosis.
- If a production operator could not detect or investigate failure, the change is incomplete.
