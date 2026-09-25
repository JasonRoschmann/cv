# Claude Code Pro Setup v3

This is a high-discipline Claude Code repository template designed for production delivery.
It is intentionally opinionated around these principles:

- Plan before risky edits.
- Implement in small, reviewable increments.
- Validate after every meaningful change.
- Route risky domains through dedicated reviewers and auditors.
- Never declare completion without explicit evidence.
- Keep always-on context small; load specialized guidance only when relevant.

## Included layers

1. `CLAUDE.md` and imported core guidance
2. `.claude/rules/` for unconditional and path-scoped rules
3. `.claude/skills/` for reusable workflows
4. `.claude/agents/` for isolated specialized agents
5. `.claude/settings.json`, hooks, MCP and runtime scripts for enforcement

## Expected adoption steps

1. Replace stack placeholders in `docs/stack/stack-profile.md`.
2. Adjust the commands in `docs/quality/validation-matrix.md`.
3. Replace placeholder MCP servers in `.mcp.json`.
4. Tune `scripts/claude/post-edit-validate.sh` to your package manager, test runner, and repository layout.
5. Review permissions and deny risky tools you never want Claude to invoke.

## Notes

- This template is deliberately stronger than a typical generic setup.
- It is still a reference implementation: the last mile comes from tailoring it to your stack.
- The shell scripts are POSIX-safe where practical, but should be adapted to your environment.
