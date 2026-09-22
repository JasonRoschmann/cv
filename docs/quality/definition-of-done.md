# Definition of done

A change is not done until all applicable statements below are true.

## Correctness
- The behavior matches the intended requirement.
- Failure behavior is explicit and acceptable.
- No known broken path is left behind silently.

## Validation
- The smallest high-signal validations have run.
- Bugs fixed in code include regression validation when practical.
- Changed contracts are covered by contract, integration, or equivalent behavioral tests.

## Production readiness
- Config and environment assumptions are explicit.
- Observability exists for critical paths and failures.
- Operational impact is understood.
- Rollout and rollback implications are documented for risky changes.

## Security and access
- Inputs are validated.
- Authorization is correct.
- Sensitive data is not overexposed in logs, errors, or responses.

## Communication
- Remaining risks are explicitly stated.
- Unverified assumptions are explicitly stated.
- The final summary distinguishes verified evidence from inference.
