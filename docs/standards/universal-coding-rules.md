# Universal coding rules

## Rule 01 — No stub code
Do not leave `pass`, `...`, empty catch blocks, TODO implementations, fake return values, or placeholder branches in production behavior.

## Rule 02 — Endpoints need validation and error handling
Every externally reachable boundary must validate input, use explicit schemas/types where available, and define expected error handling.

## Rule 03 — Data access needs authorization context
Where ownership or authorization matters, every DB/data access path must enforce it explicitly and testably.

## Rule 04 — LLM calls need a safety pipeline
LLM features require at least input sanitization, prompt hardening/system policy, and output validation/shape checks.

## Rule 05 — Paid APIs require approval before retries
After an error, diagnose first. Do not auto-retry paid API requests without explicit approval.

## Rule 06 — Session/token policy must be explicit
Short-lived access and explicit refresh/session semantics are required where auth tokens are used.

## Rule 07 — No wildcard production CORS
Allow only known origins in production.

## Rule 08 — Abuse-prone endpoints need rate limiting
Especially auth, login, signup, reset, billing, and heavy endpoints.

## Rule 09 — Background jobs need retry and logging policy
Retries, backoff, and start/success/failure logging should be explicit.

## Rule 10 — Migrations need both forward and rollback thinking
Do not leave downgrade/rollback strategy blank unless the migration strategy is intentionally forward-only and documented.

## Rule 11 — Frontend must cover loading, error, empty, success states
Do not ship user-facing changes that only handle the happy path.

## Rule 12 — No stray debug logging
Use structured/project logging instead of `console.log`/`print` in production paths.

## Rule 13 — Use timezone-safe time handling
Use UTC or explicit timezone-aware handling for persisted or distributed time.

## Rule 14 — Password hashing/settings must be explicit and strong
No silent defaults or weak settings.

## Rule 15 — Runtime health must be visible
Containers/services should expose health/readiness where relevant.

## Rule 16 — Web edges require security headers where relevant
CSP, HSTS, frame, content-type, and related policy should be consciously configured.

## Rule 17 — Secrets never belong in version control
`.env`, key files, and secret material must remain uncommitted.

## Rule 18 — Compliance-critical surfaces need explicit handling
If privacy/regulatory obligations apply, treat them as product requirements, not optional follow-ups.

## Rule 19 — Billing/critical monetization logic should be feature-flagged or safely gated
Do not make hard-to-reverse billing changes unsafe by default.

## Rule 20 — API keys and secrets should be protected at rest and in transit
No casual plaintext handling when secure key management is available.
