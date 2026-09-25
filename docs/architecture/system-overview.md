# System overview

## Mission
The repository should ship production-grade software with deterministic behavior, explicit validation, and safe operational characteristics.

## Architectural expectations
- Frontend is responsible for user experience, local interaction, and safe presentation.
- Backend is responsible for validation, business rules, access control, and durable effects.
- Persistence and data movement are explicit and observable.
- Infrastructure is treated as code and validated like application code.
- Every critical path is diagnosable in production.

## Golden rules
- Domain logic belongs in domain or service layers, not in transport adapters.
- Trust boundaries must be explicit.
- New complexity requires stronger verification, not stronger confidence language.
- Features are incomplete unless success, failure, and operational visibility are addressed.

## Required reasoning sequence
1. Locate affected boundaries.
2. Identify failure modes.
3. Determine required validations.
4. Implement the minimum coherent increment.
5. Validate before continuing.
