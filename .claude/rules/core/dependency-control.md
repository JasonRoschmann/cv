# Dependency control rules

- Pin production-critical dependencies exactly; avoid `^`, `~`, floating tags, and `latest`.
- Commit lockfiles where the ecosystem expects them.
- Prefer reproducible install commands (`npm ci`, locked Poetry/pip constraints, pinned Docker tags).
- Review security audits before release for critical packages/images.
