# Domain boundaries

## Boundary categories
- UI boundary: user input, rendering, accessibility, client-side state.
- API boundary: request parsing, validation, response contracts, authn/authz.
- Domain boundary: business invariants, workflows, policies, orchestration.
- Persistence boundary: transactions, migrations, data shape, concurrency, idempotency.
- Integration boundary: third-party APIs, queues, storage, webhooks, files.
- Operational boundary: logs, metrics, traces, deploys, runtime configuration.

## Rules of movement
- Data should become more validated as it moves inward.
- Errors should become more contextual as they move outward.
- Privilege should only narrow, never widen accidentally.
- Side effects should be explicit and recoverable where possible.

## Escalation cues
Use specialized auditors when a change crosses boundaries or raises questions about:
- auth or permissions
- contract compatibility
- migration safety
- external side effects
- observability gaps
