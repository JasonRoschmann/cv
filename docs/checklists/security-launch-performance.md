# Security, launch, and performance checklists

## Security checklist

- Every endpoint has explicit auth checks where required.
- Every data access path has explicit ownership/authorization checks where required.
- Rate limiting exists on abuse-prone endpoints.
- CORS is not wildcarded in production.
- Security headers are configured when a web edge is involved.
- `.env` and secrets are excluded from version control.
- API keys and secrets are not stored or logged insecurely.
- LLM features use input sanitization and output validation when applicable.
- JWT/session expiration and refresh policy are explicit.
- Password hashing parameters are strong and explicit.
- No user-controlled raw SQL or equivalent injection vector.
- No dangerous HTML injection pattern without sanitization.
- PII is not leaked in logs.
- Dependency audits have no known critical findings or are explicitly waived.
- Secret keys are strong and not default values.

## Pre-launch checklist

### Backend
- Tests green with evidence
- Lint/typecheck green with evidence
- Health endpoint or equivalent passes
- Migrations exercised safely when applicable
- Background workers start and process known-good jobs
- Monitoring/error capture configured for production
- Dependency audit reviewed
- Dependencies pinned

### Frontend
- Production build succeeds with evidence
- Typecheck succeeds with evidence
- Audit reviewed
- Loading, error, empty, and success states covered
- No stray debug logging in production paths
- Consent and analytics behavior respects policy

### Infrastructure
- Containers or services show healthy status
- TLS and redirect policy are correct where applicable
- Firewalls/security groups are minimal
- Backups and restore path are known
- Monitoring and alerting exist for critical paths
- Deployment script/process has been exercised in a safe environment
- Images and runtime versions are pinned

## Performance checklist

- CRUD/API latency targets are defined and checked on critical endpoints.
- DB queries are reviewed for indexing and N+1 risks.
- Pagination exists on collection endpoints.
- Expensive work is cached or made async where appropriate.
- Frontend bundle size and image delivery are reviewed for user-facing performance.
- Compression and static asset policies are enabled where relevant.
