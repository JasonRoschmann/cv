# Security baseline rules

- Validate all untrusted input.
- Prefer allowlists, explicit parsing, and safe defaults.
- Avoid logging sensitive identifiers, secrets, tokens, or raw personal data.
- Treat file paths, URLs, webhooks, uploads, and third-party payloads as hostile until validated.
- Permission checks must be explicit and testable.
- Route trust-boundary changes through the security-reviewer.
