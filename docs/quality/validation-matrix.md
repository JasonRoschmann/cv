# Validation matrix

Use this matrix to decide what must run before claiming completion.

## By change type

### UI-only change
- component or unit tests
- relevant route or flow test
- accessibility spot checks
- visual or manual verification of loading, error, empty, and success states

### API or service change
- unit tests for core logic
- integration tests for request or persistence boundary
- contract validation where applicable
- auth and failure-path coverage

### Persistence or migration change
- migration syntax or dry-run validation
- ordering and rollout review
- integration tests against realistic schema assumptions
- migration-auditor review for medium/high risk changes

### Infra or runtime-config change
- lint and static validation
- plan or diff review
- environment compatibility review
- deployment or runtime assumptions explicitly documented

## Risk tiers

### Low risk
Small, localized change with unchanged contracts and obvious validation.
Minimum: targeted tests + lint/typecheck.

### Medium risk
Multiple files or changed behavior with at least one boundary crossing.
Minimum: targeted tests + one specialist review.

### High risk
Auth, migrations, external integrations, broad refactors, payment/billing, concurrency, or operational impact.
Minimum: implementation plan + targeted tests + at least two specialist reviews + release-manager check.
