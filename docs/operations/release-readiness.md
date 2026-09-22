# Release readiness

## Release gate questions
- Is the behavior validated at the right layer?
- Have critical failure paths been exercised or reasoned about with evidence?
- Are schema changes rollout-safe?
- Are logs, metrics, and traces sufficient for triage?
- Are any feature flags, config toggles, or migration windows required?
- Is there a rollback or forward-fix path?

## No-go examples
- Typecheck or build failures remain.
- A changed critical path has no operator-visible signals.
- A migration is syntactically valid but rollout behavior is unclear.
- The only proof is a happy-path manual statement.
- Required specialist review was skipped.
